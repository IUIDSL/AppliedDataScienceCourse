import json
import pandas as pd
import numpy as np
import sklearn
from sklearn.feature_extraction import text as sk_fe_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, f1_score, recall_score
from TwitterAPI import TwitterAPI

#Set up the variables for your 'application'
consumerkey = 'YOUR-CONSUMER-KEY-HERE'
consumersecret = 'YOUR-CONSUMER-SECRET-HERE'

#Setup your API key
api = TwitterAPI(consumerkey,consumersecret,auth_type='oAuth2')

def score(true,pred):
  return (precision_score(true,pred),
          recall_score(true,pred),
          f1_score(true,pred))

def print_score(s):
  print("""
Precision:  {:0.3}
Recall:     {:0.3}
F-Score:    {:0.3}
""".format(*s))

def searchTwitter(query,feed="search/tweets",api=api,n=100):
  return [t for t in api.request(feed, {'q':query,'count':n})]

#Get JSON from Twitter
cats = searchTwitter('#cats')
dogs = searchTwitter('#dogs')

# Convert the json returned by Twitter into a dataframe
cats_d = pd.read_json(json.dumps(cats))
dogs_d = pd.read_json(json.dumps(dogs))

# If you would like to look at the full data frame
# cats_d.info()
# dogs_d.info()

#Get text only and replace hashtags with blanks
#If you want to use the normalizer, import it above and pass x.replace() to the noramlizer function

cats_text = [x.replace('#cats',"") for x in cats_d['text']]
dogs_text = [x.replace('#dogs',"") for x in dogs_d['text']]

#Create features and return sparse matricies
vectorizer = sk_fe_text.CountVectorizer(cats_text+dogs_text)
vectorizer.fit(cats_text+dogs_text)
cats_tdm = vectorizer.transform(cats_text).toarray()
dogs_tdm = vectorizer.transform(dogs_text).toarray()

#Create visible matricies and combine
zeros = np.zeros((len(cats_text),1))
ones = np.ones((len(dogs_text),1))
catsdogs = np.concatenate((cats_tdm,dogs_tdm),axis=0)
y = np.ravel(np.concatenate((zeros,ones),axis=0))

#Create train/test split for modeling
trainX,testX,trainY,testY = train_test_split(catsdogs,y,test_size=.25)

#Naive Bayes
from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(trainX,trainY)

print("\n\nNaive Bayes Performance")
s = score(testY,nb.predict(testX))
print_score(s)

#SVM
from sklearn.svm import SVC
svm = SVC()
svm.fit(trainX,trainY)

print("\n\nSVM performance")
s = score(testY,svm.predict(testX))
print_score(s)

#Neural Network
from sklearn.neural_network import MLPClassifier
nn = MLPClassifier()
nn.fit(trainX,trainY)

print("\n\nNeural Network Performance")
s = score(testY,nn.predict(testX))
print_score(s)

#KNN
from sklearn.neighbors import KNeighborsClassifier
knn1 = KNeighborsClassifier(n_neighbors=1)
knn5 = KNeighborsClassifier(n_neighbors=5)
knn5d = KNeighborsClassifier(n_neighbors=5,weights='distance')

knn1.fit(trainX,trainY)
knn5.fit(trainX,trainY)
knn5d.fit(trainX,trainY)

print("\n\nKNN 1 Neighbor Performance")
s = score(testY,knn1.predict(testX))
print_score(s)

print("\n\nKNN 5 Neighbor Performance")
s = score(testY,knn5.predict(testX))
print_score(s)

print("\n\nKNN 5 Neighbor Weighted Performance")
s = score(testY,knn5d.predict(testX))
print_score(s)
