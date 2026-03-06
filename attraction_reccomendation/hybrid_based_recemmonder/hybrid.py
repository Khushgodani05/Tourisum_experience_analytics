import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd 
import numpy as np
from content_based_recemmendation.reccomend import Attraction_content_based
from collabrative_based_recemmendation.reccomend import Attractionrecemmond

contentbasedmodel=Attraction_content_based()
collbrativebasedmodel=Attractionrecemmond()


class Hybridmodel():
    def __init__(self,contentmodel,collabrativemodel):
        self.contentmodel=contentmodel
        self.collabrativemodel=collabrativemodel
        
    def reccomend(self,desc,attractioncity):
        res_content=self.contentmodel.recommend(desc,attractioncity)
        res_collab=self.collabrativemodel.recemmond(desc,attractioncity)
        res_content["score"]=0.6*res_content.ratingx
        res_collab["score"]=0.4*res_collab.ratingx
        result=pd.concat([res_content,res_collab]).drop_duplicates(keep="first").reset_index(drop=True).sort_values(ascending=False,by="score")
        result.drop(["score"],inplace=True,axis=1)
        return result
    
model=Hybridmodel(contentbasedmodel,collbrativebasedmodel)
print(model.reccomend("@@@Sacred Monkey Forest Sanctuary !!!!","douala"))