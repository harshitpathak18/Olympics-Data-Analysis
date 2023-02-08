import pandas as pd

def preprocessing(df,region_df):    
    # Filtering data for summer olympics
    df=df[df['Season']=="Summer"]
    
    # Merge region with NOC
    df=df.merge(region_df,on="NOC",how="left")
    
    # Drop duplicates columns
    df.drop_duplicates(inplace=True)
    
    # one hot enconding
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    
    return df
