import pandas as pd
import streamlit as st
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from PIL import Image

Image = Image.open('olympics.jpeg')

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')

df=preprocessor.preprocessing(df,region_df)
st.sidebar.image(Image)
st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    "Select an options",
    ('Medal Tally','Overall Analysis','Country-wise Analysis', 'Athlete-wise Analysis')
)


if user_menu=="Medal Tally":
    st.sidebar.header("Medal Tally")
    year,country=helper.country_year_list(df)


    selected_year=st.sidebar.selectbox('Selected Year',year)
    selected_country=st.sidebar.selectbox('Selected Country',country)
    
    
    if selected_year=="Overall" and selected_country=="All":
        st.title("Overall Tally")
    if selected_year!="Overall" and selected_country=="All":
        st.title("Medal Tally in "+str(selected_year)+ " Olympics")
    if selected_year=="Overall" and selected_country!="All":
        st.title(str(selected_country)+ " overall performance")
    if selected_year!="Overall" and selected_country!="All":
        st.title("Overall performance of "+ selected_country +" in "+str(selected_year))
        
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    st.dataframe(medal_tally)


if user_menu=="Overall Analysis":
    # no. of times,cities,sports,events,atheletes,nations olympics
    editions=df['Year'].nunique()-1
    cities=df['City'].nunique()
    sports=df['Sport'].nunique()
    events=df['Event'].nunique()
    athletes=df['Name'].nunique()
    nations=df['region'].nunique()

    #title
    st.title("Top Statistics")

    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader("Editions")
        st.header(editions)
    with col2:
        st.subheader("Hosts")
        st.header(cities)
    with col3:
        st.subheader("Sports")
        st.header(sports)
    
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader("Events")
        st.header(events)
    with col2:
        st.subheader("Nations")
        st.header(nations)
    with col3:
        st.subheader("Athletes")
        st.header(athletes)
        

    # Nation participated over years analysis
    nation_over_years=helper.data_over_time(df,"region")
    fig = px.line(nation_over_years, x="Edition", y="No of Countries", )
    st.write("---")
    st.title("Participated nations over the years")
    st.plotly_chart(fig)
    
    # Sports played over the year analysis)
    sports_played_over_years=helper.data_over_time(df,"Event")
    fig = px.line(sports_played_over_years, x="Edition", y="No of Sports", )
    st.write("---")
    st.title("Events played over the years")
    st.plotly_chart(fig)

    # Athelets played over the year analysis)
    athelets_played_over_years=helper.data_over_time(df,"Athelet")
    fig = px.line(athelets_played_over_years, x="Edition", y="No of Athelets", )
    st.write("---")
    st.title("Athelets played over the years")
    st.plotly_chart(fig)

    # No. over events in every sports over time
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values="Event",aggfunc='count').fillna(0).astype('int'),annot=True, cmap="Blues")
    st.write("---")
    st.title("Events played in sports over the years")
    st.pyplot(fig)


    st.title("Most Successful Athelets")
    sport_list=list(df['Sport'].unique())
    sport_list.sort()
    sport_list.insert(0,"Overall")
    selcted_sport=st.selectbox("Select a Sport",sport_list)

    x=helper.most_succeful_athelets(df,selcted_sport)
    st.dataframe(x)


if user_menu=="Country-wise Analysis":

    st.sidebar.title("Country-wise Analysis")
    country_list=list(df['region'].dropna().unique())
    country_list.sort()

    selected_country=st.sidebar.selectbox("Select a Country",country_list)
    
    nation_over_years=helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(nation_over_years, x="Year", y="Medal", )
    st.title(selected_country+" Medal Tally over the years ")
    st.plotly_chart(fig)


    # country in sports over time
    fig,ax=plt.subplots(figsize=(20,20))
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==selected_country]
    ax=sns.heatmap(new_df.pivot_table(index='Sport',columns='Year',values="Medal",aggfunc='count').fillna(0),annot=True, cmap="Blues")
    st.write("---")
    st.title("Medal Tally in Various Sports")
    st.pyplot(fig)

    # most successful athelets in country
    atheletes=helper.country_most_succeful(df,selected_country)
    st.write("---")
    st.title("Most Successful Athelets ")
    st.table(atheletes)


if user_menu=="Athlete-wise Analysis":
    st.header("Distribution of Age")
    athelete_df=df.drop_duplicates(subset=['Name','region'])
    x1=athelete_df['Age'].dropna()
    x2=athelete_df[athelete_df['Medal']=="Gold"]['Age'].dropna()
    x3=athelete_df[athelete_df['Medal']=="Silver"]['Age'].dropna()
    x4=athelete_df[athelete_df['Medal']=="Bronze"]['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)

    st.plotly_chart(fig)

    st.write("---")
    st.title("Male & Female Participation over the years")
    men=athelete_df[athelete_df['Sex']=="M"].groupby('Year').count()['Name'].reset_index()
    female=athelete_df[athelete_df['Sex']=="F"].groupby('Year').count()['Name'].reset_index()
    
    final_df=men.merge(female,on='Year',how="left")
    final_df.rename(columns={"Name_x":"Male","Name_y":"Female"},inplace=True)
    final_df.fillna(0, inplace=True)
    fig=px.line(final_df,x="Year",y=["Male","Female"])
    st.plotly_chart(fig)