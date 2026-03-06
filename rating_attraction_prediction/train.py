from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from category_encoders import BinaryEncoder
from sklearn.decomposition import PCA

model=joblib.load("Attraction_rating_prediction_model.pkl")

data=pd.read_csv("../Data/final_data.csv")
data=data.drop(["attraction","attractionaddress","usercity","attractioncity"],axis=1)

covidyear=[2020,2021]

x=data.drop("ratingx",axis=1)   
y=data["ratingx"]

from sklearn.model_selection import GroupShuffleSplit

gss = GroupShuffleSplit(test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(x,y, groups=data["useridx"]))
x_train = x.iloc[train_idx].copy()
x_test  = x.iloc[test_idx].copy()
y_train = y.iloc[train_idx].copy()
y_test= y.iloc[test_idx].copy()


train_data=data.iloc[train_idx].copy()


attraction_mean_map=train_data.groupby("attractionidx")["ratingx"].mean()
global_mean=train_data["ratingx"].mean()
user_mean_map=train_data.groupby("useridx")["ratingx"].mean()
global_mean_user=user_mean_map.mean()
attraction_count=train_data.groupby("attractionidx")["useridx"].nunique()


categoryx=[cols for cols in x_train.columns if x_train[cols].dtype=="object"]
numx=[cols for cols in x_train.columns if x_train[cols].dtype!="object"]
binenc=[]
ohe=[]
for i in categoryx:
    if x_train[i].nunique()>6:
        binenc.append(i)
    else:
        ohe.append(i)
        

ct=ColumnTransformer(
    [
        ("OneHotEncoding",OneHotEncoder(),ohe),
        ("StandardScaler",StandardScaler(),numx),
        # ("Robustscaler",RobustScaler(),rscales),
        ("BinaryEncoder",BinaryEncoder(),binenc)
    ],
    remainder="drop",
)

pca=PCA(n_components="mle",svd_solver="full")


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
    

pipeline = Pipeline([
    ("feature_builder", RatingFeatureBuilder(
        covidyear=covidyear,
        user_mean_map=user_mean_map,
        global_mean_user=global_mean_user,
        attraction_mean_map=attraction_mean_map,
        global_mean=global_mean,
        attraction_count_map=attraction_count
    )),
    ("preprocessing", ct),
    ("pca", pca),
    ("model", model)
])

pipeline.fit(x_train, y_train)

joblib.dump(pipeline, "rating_model.pkl")

