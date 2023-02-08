import pandas as pd

def fetch_medal_tally(df,year,country):
    flag=0
    # Drop multiple player from same teams to get only sports medal tally
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    if year=="Overall" and country=="All":
        new_df=medal_df
    if year=="Overall" and country!="All":
        flag=1
        new_df=medal_df[medal_df['region']==country]
    if year!="Overall" and country=="All":
        new_df=medal_df[medal_df['Year']==int(year)]
    if year!="Overall" and country!="All":
        new_df=medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]
    
    # Create medal dataframe with features=[region, gold, silver,bronze]
    if flag==1:
        medal_tally=new_df.groupby("Year").sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    else:
        medal_tally=new_df.groupby("region").sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    
    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver']=medal_tally['Silver'].astype('int')
    medal_tally['Bronze']=medal_tally['Bronze'].astype('int')
    medal_tally['total']=medal_tally['total'].astype('int')
    return medal_tally


def country_year_list(df):
    year=list(df['Year'].unique())
    year.sort()
    year.insert(0,"Overall")

    country=df['region'].dropna().unique()
    country=list(country)
    country.sort()
    country.insert(0,"All")

    return year,country


# Data over time
def data_over_time(df,col):
    if col=="region":
        return df.drop_duplicates(subset=['Year','region'])['Year'].value_counts().reset_index().sort_values("index").rename(columns={"index":"Edition","Year":"No of Countries"})
    elif col=="Event":
        return df.drop_duplicates(subset=['Year','Event'])['Year'].value_counts().reset_index().sort_values("index").rename(columns={"index":"Edition","Year":"No of Sports"})
    elif col=="Athelet":
        return df.drop_duplicates(subset=['Year','Name'])['Year'].value_counts().reset_index().sort_values("index").rename(columns={"index":"Edition","Year":"No of Athelets"})


# Atheletes with max medal
def most_succeful_athelets(df,sport):
    temp_df=df.dropna(subset=["Medal"])
    
    if sport!="Overall":
        temp_df=temp_df[temp_df['Sport']==sport]
    
    x= temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on="index", right_on="Name", how='left')[['index','Name_x','Sport','region']].drop_duplicates("index")
    x.rename(columns={"index":"Name","Name_x":"Medals"}, inplace=True)
    return x


def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    new_df=temp_df[temp_df['region']==country]

    return new_df.groupby("Year").count()['Medal'].reset_index()

def country_most_succeful(df,country):
    temp_df=df.dropna(subset=["Medal"])
    temp_df=temp_df[temp_df['region']==country]
    
    x= temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on="index", right_on="Name", how='left')[['index','Name_x','Sport']].drop_duplicates("index")
    x.rename(columns={"index":"Name","Name_x":"Medals"}, inplace=True)
    return x