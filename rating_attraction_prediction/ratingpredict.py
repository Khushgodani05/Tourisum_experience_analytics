import joblib
import pandas as pd
import os 
import sys

from sklearn.base import BaseEstimator, TransformerMixin

sys.modules["__main__"].RatingFeatureBuilder=None

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "rating_model.pkl")

 
class RatingFeatureBuilder(BaseEstimator, TransformerMixin):
    def __init__(self, covidyear, user_mean_map, global_mean_user,
                 attraction_mean_map, global_mean, attraction_count_map):
        
        self.covidyear = covidyear
        self.user_mean_map = user_mean_map
        self.global_mean_user = global_mean_user
        self.attraction_mean_map = attraction_mean_map
        self.global_mean = global_mean  
        self.attraction_count_map = attraction_count_map

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        X["iscovid"] = X["visityearx"].apply(
            lambda x: 1 if x in self.covidyear else 0
        )

        X["user_mean"] = X["useridx"].map(
            self.user_mean_map
        ).fillna(self.global_mean_user)

        X["attraction_mean"] = X["attractionidx"].map(
            self.attraction_mean_map
        ).fillna(self.global_mean)

        X["attraction_count"] = X["attractionidx"].map(
            self.attraction_count_map
        ).fillna(1)

        X["user_attraction_interaction"] = (
            X["user_mean"] * X["attraction_mean"]
        )
        
        return X
    
sys.modules["__main__"].RatingFeatureBuilder=RatingFeatureBuilder
    
model = joblib.load(model_path)


def predict_rating(input_data: dict):
    
    # convert input into dataframe
    df = pd.DataFrame([input_data])

    # predict rating
    prediction =model.predict(df)

    return prediction[0]


if __name__ == "__main__":

    sample_input = {
    "useridx": 14,
    "continent": "Europe",
    "region": "Southern Europe",
    "usercountry": "Portugal",
    "usercity": "Lagos",
    "transactionid": 5661,
    "visityearx": 2018,
    "visitmonthx": 12,
    "attractionidx": 640,
    "visitmodex": "Friends",
    "attraction": "Sacred Monkey Forest Sanctuary",
    "attractionaddress": "Jl. Monkey Forest, Ubud 80571 Indonesia",
    "attractiontype": "Nature & Wildlife Areas",
    "attractioncity": "Douala",
    "attractioncountry": "Cameroon"
    }

    rating = predict_rating(sample_input)

    print("Predicted Rating:", rating)
                                               

