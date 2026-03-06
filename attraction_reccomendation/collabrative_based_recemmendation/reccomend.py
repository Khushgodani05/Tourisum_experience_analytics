import re 
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "collabrativemodel.pkl")

model=joblib.load(model_path)

class Attractionrecemmond():
    def __init__(self):
        self.attraction_attraction_similarity_df=model["attraction_attraction_similarity_df"]
        self.data=model["attraction_metadata"]

          
    def recemmond(self, desc, attractioncity):

        desc = re.sub("[^a-zA-Z0-9 ]"," ",desc).lower().strip()

        reccomend = self.attraction_attraction_similarity_df.loc[desc].sort_values(ascending=False)[1:6]

        reccom = []
        for i in reccomend.index:
            reccom.append(i)

        filtered_data = self.data[self.data.attractioncity.str.lower()==attractioncity.lower()]

        result = filtered_data[
            filtered_data.attraction.str.lower().isin(reccom)
        ].drop_duplicates(
            subset="attraction"
        ).loc[:,["attraction","attractionaddress","ratingx"]].sort_values(
            by="ratingx",ascending=False
        ).reset_index(drop=True)

        return result
    
