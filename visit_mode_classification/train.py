import pandas as pd 
import numpy as np 
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler,LabelEncoder
from category_encoders import BinaryEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

model=joblib.load("visitmodemodel.pkl")

data=pd.read_csv("../Data/final_data.csv")
data.dropna(subset=["usercity"],axis=0,inplace=True)

x=data.drop("visitmodex",axis=1)
y=data["visitmodex"]
le=LabelEncoder()
y=le.fit_transform(y)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,stratify=y)

a=x_train.groupby("useridx")["attractionidx"].value_counts()
b=x_train.groupby("attractionidx")["transactionid"].value_counts()


x_train["user_attraction_mode"]=x_train.set_index(["useridx","attractionidx"]).index.map(a)
x_train.user_attraction_mode=x_train.user_attraction_mode.astype("float")
x_train["attraction_transaction_mode"]=x_train.set_index(["attractionidx","transactionid"]).index.map(b)
x_train["attraction_transaction_mode"]=x_train["attraction_transaction_mode"].astype("float")
default_user_attraction_mode=x_train.user_attraction_mode.value_counts().sort_values(ascending=False).iloc[0]
default_attraction_transaction_mode=x_train.attraction_transaction_mode.value_counts().sort_values(ascending=False).iloc[0]


finalcat=['continent',
  'region',
  'usercountry',
  'usercity',
  'attraction',
  'attractiontype',
  'attractioncity',
  'attractioncountry']
finalnum=['visityearx',
  'visitmonthx',
  'ratingx',
  'iscovid',
  'user_attraction_mode',
  'attraction_transaction_mode']

covidyear=[2020,2021]


ohe=[]
binenc=[]
for i in finalcat:
    if x_train[i].nunique()>5:
        binenc.append(i)
    else:
        ohe.append(i)
        
        
ct=ColumnTransformer(
    [
        ("OneHotEncoding",OneHotEncoder(),ohe),
        ("StandardScaler",StandardScaler(),finalnum),
        # ("Robustscaler",RobustScaler(),rscales),
        ("BinaryEncoder",BinaryEncoder(),binenc)
    ],
    remainder="drop"
)

from sklearn.base import BaseEstimator,TransformerMixin

class visitmodeclassifyfeaturebuilder(BaseEstimator,TransformerMixin):
    def __init__(self,covidyear,a,b,default_user_attraction_mode,default_attraction_transaction_mode):
        self.covidyear=covidyear
        self.a=a
        self.b=b 
        self.default_user_attraction_mode=default_user_attraction_mode
        self.default_attraction_transaction_mode=default_attraction_transaction_mode
        
    def fit(self,x,y=None):
        return self
    
    def transform(self,x):
        x=x.copy()
        x["iscovid"]=x.visityearx.apply(lambda x: 1 if x in self.covidyear else 0)
        x["user_attraction_mode"]=x.set_index(["useridx","attractionidx"]).index.map(self.a).fillna(self.default_user_attraction_mode)
        x["attraction_transaction_mode"]=x.set_index(["attractionidx","transactionid"]).index.map(self.b).fillna(self.default_attraction_transaction_mode)
        x.user_attraction_mode=x.user_attraction_mode.astype("float")
        x.attraction_transaction_mode=x.attraction_transaction_mode.astype("float")
        return x
    

pipeline=Pipeline(
    steps=[
        ("featurebuilder",visitmodeclassifyfeaturebuilder(covidyear,a,b,default_user_attraction_mode,default_attraction_transaction_mode)),
        ("ColumnTransformer",ct),   
        ("model",model)
    ]
)

pipeline.fit(x_train,y_train)

joblib.dump(pipeline,"visitmodepipeline.pkl")