import joblib
import re 
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "model.pkl")

lemmatize=WordNetLemmatizer()
model = joblib.load(model_path)
word=stopwords.words("english")

class Attraction_content_based():
    def __init__(self):
        self.tfidf=model["tfidf"]
        self.final_sentence=model["final_sentence"]
        self.data=model["data"]


    def get_word_pos(treebank_tag):
        if treebank_tag.startswith("N"):
            return wordnet.NOUN
        elif treebank_tag.startswith("J"):
            return wordnet.ADJ
        elif treebank_tag.startswith("V"):
            return wordnet.VERB
        elif treebank_tag.startswith("R"):
            return wordnet.ADV
        else:
            return wordnet.NOUN
    
    

    def recommend(self,desc,attractioncity):
        words=[]
        desc=re.sub("[^a-zA-Z0-9]"," ",desc)
        desc=desc.lower().strip().split(" ")
        for i in desc:
            if i not in words and i!="" and i not in  word:   
                words.append(i)
        lemmed=[]
        postag=pos_tag(words)
        lemmed=[lemmatize.lemmatize(words,Attraction_content_based.get_word_pos(pos)) for words,pos in postag]
        final=[" ".join(lemmed)]
        vector=self.tfidf.transform(final)
        cs=np.round(cosine_similarity(vector,self.final_sentence),4)
        temp_data=self.data.copy()
        temp_data["cosine_similarity"]=cs.T
        temp_data=temp_data[self.data.attraction.str.lower()!=final[0]]
        filtered_df=temp_data[temp_data["attractioncity"].str.lower()==attractioncity.lower()]
        recommendations=filtered_df.sort_values(
            ["cosine_similarity","ratingx"]
            ,ascending=False).reset_index()
        return pd.DataFrame(recommendations[["attraction","attractionaddress","ratingx"]].head(5))
    

