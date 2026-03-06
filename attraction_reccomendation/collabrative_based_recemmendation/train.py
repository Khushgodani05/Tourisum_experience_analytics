import pandas as pd 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
import re
import joblib


data=pd.read_csv("../../Data/final_data.csv")
data=data.drop_duplicates(subset=["useridx","attractionidx","ratingx"],keep="first")
data.dropna(inplace=True)
data=data.loc[:,["useridx","transactionid","ratingx","attraction","attractionidx","attractionaddress","attractioncity"]]


user_attraction_interaction=data.groupby("useridx")["attractionidx"].nunique()
data["user_attraction_interaction"]=data.useridx.map(user_attraction_interaction)
transaction_per_attraction=data.groupby("attractionidx")["transactionid"].nunique()
data["transaction_per_attraction"]=data.attractionidx.map(transaction_per_attraction)
rating_per_attraction=data.groupby("attractionidx")["ratingx"].mean()
data["rating_per_attraction"]=data.attractionidx.map(rating_per_attraction)

data["interaction_metrics"]=data.user_attraction_interaction*data.transaction_per_attraction*data.rating_per_attraction


user_attraction_matrix=pd.pivot_table(
    data=data,
    index="useridx",
    columns="attraction",
    values="interaction_metrics",
    fill_value=0,
    aggfunc="mean",
)
attraction_user_matrix=user_attraction_matrix.T
attraction_attraction_similarity=cosine_similarity(attraction_user_matrix)

attraction_attraction_similarity_df=pd.DataFrame(
    index=attraction_user_matrix.index.str.lower(),
    columns=attraction_user_matrix.index.str.lower(),
    data=attraction_attraction_similarity
)

metadata=data[[
    "attraction",
    "attractionaddress",
    "ratingx",
    "attractioncity"
]]


joblib.dump(
    {
        "attraction_attraction_similarity_df":attraction_attraction_similarity_df,
        "attraction_metadata":metadata,
    },
    "collabrativemodel.pkl"
)


print("Model saved successfully....")

