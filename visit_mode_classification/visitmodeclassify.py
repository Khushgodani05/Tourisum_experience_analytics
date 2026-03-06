import pandas as pd 
import numpy as np 
import joblib
import os
from sklearn.base import BaseEstimator,TransformerMixin
import sys

sys.modules['__main__'].visitmodeclassifyfeaturebuilder = None

BASEDIR=os.path.dirname(__file__)
model_path=os.path.join(BASEDIR,"visitmodepipeline.pkl")


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
    
sys.modules['__main__'].visitmodeclassifyfeaturebuilder = visitmodeclassifyfeaturebuilder
    
model=joblib.load(model_path)


def visitmodeclassify(inputdata:dict):
    visitmode={
        0: 'Business', 
        1: 'Couples', 
        2: 'Family', 
        3: 'Friends', 
        4: 'Solo'
    }
    
    df=pd.DataFrame([inputdata])
    classify=model.predict(df)[0]
    res=visitmode[classify]
    return res
       
    
if __name__ == "__main__":
    
    sample_input = {
        "useridx": 73808,
        "continent": "Australia & Oceania",
        "region": "Australia",
        "usercountry": "Australia",
        "usercity": "Eastern Creek",
        "transactionid": 4842,
        "visityearx": 2018,
        "visitmonthx": 4,
        "attractionidx": 640,
        "ratingx": 5,
        "attraction": "Sacred Monkey Forest Sanctuary",
        "attractionaddress": "Jl. Monkey Forest, Ubud 80571 Indonesia",
        "attractiontype": "Nature & Wildlife Areas",
        "attractioncity": "Douala",
        "attractioncountry": "Cameroon"
    }
    
    
    classification=visitmodeclassify(sample_input)
    print(classification)