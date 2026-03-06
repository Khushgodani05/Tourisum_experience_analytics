import pandas as pd 
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

lemmatize=WordNetLemmatizer()
word=stopwords.words("english")
tfidf=TfidfVectorizer()

data=pd.read_csv("../../Data/final_data.csv")
data=data.drop_duplicates(subset=["useridx","attractionidx","visitmodex"],keep="first")
data=data.iloc[:,9:]
x=data["attraction"]

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
    

tokens=[]
for i in x:
    a=re.sub("[^a-zA-Z0-9]"," ",i)
    a=a.lower().strip().split()
    tokens.append(a)
cleaned=[]
for i in tokens:
    words=[]
    for j in i:
        if j not in words and j not in word and j!="":
            words.append(j)
    cleaned.append(words)
pos_tagging=[]
for i in cleaned:
    pos_tagging.append(pos_tag(i))
lemmed=[]
for i in pos_tagging:
    lemma=[]
    for word,treebank_tag in i:
        lemma.append(lemmatize.lemmatize(word,get_word_pos(treebank_tag)))
    lemmed.append(lemma)
final_sentence=[]
for i in lemmed:
    final_sentence.append(" ".join(i))
final_sentence=tfidf.fit_transform(final_sentence)

metadata=data[[
    "attractionaddress",
    "attraction",
    "ratingx",
    "attractioncity"
]]

joblib.dump(
    {
        "tfidf":tfidf,
        "final_sentence":final_sentence,
        "data":metadata,
    },
    "model.pkl"
)

print("Model trained and saved successfully!")