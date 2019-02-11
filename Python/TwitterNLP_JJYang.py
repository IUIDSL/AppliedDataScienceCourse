import json
import pandas
import numpy
import sklearn
import sklearn.feature_extraction
import sklearn.model_selection 
import sklearn.metrics 
import sklearn.naive_bayes
import sklearn.svm
import sklearn.neighbors
from TwitterAPI import TwitterAPI

### Set up the variables for your 'application'
consumerkey = '	rbjlmTKRpuM8exIBPOZyolVQK'
consumersecret = 'zsk27R4iKlINS3xai7XqsBp1VGriMqSAEc9CHgyIHlzVoF6uvl'

### Setup your API key
api = TwitterAPI(consumerkey,consumersecret,auth_type='oAuth2')

def print_score(Ytrue,Ypred):
  s = (sklearn.metrics.precision_score(Ytrue,Ypred),
          sklearn.metrics.recall_score(Ytrue,Ypred),
          sklearn.metrics.f1_score(Ytrue,Ypred))
  print('Precision: {:0.3}\nRecall: {:0.3}\nF-Score: {:0.3}\n'.format(*s))


def searchTwitter(query,feed="search/tweets",api=api,n=100):
  return [t for t in api.request(feed, {'q':query,'count':n})]

### Get JSON from Twitter
cats = searchTwitter('#cats')
dogs = searchTwitter('#dogs')

### Convert the json returned by Twitter into a dataframe
cats_df = pandas.read_json(json.dumps(cats))
dogs_df = pandas.read_json(json.dumps(dogs))

### If you would like to look at the full data frame
### cats_df.info()
### dogs_df.info()

### Get text only and replace hashtags with blanks
### If you want to use the normalizer, import it above and pass x.replace() to the noramlizer function

cats_text = [x.replace('#cats',"") for x in cats_df['text']]
dogs_text = [x.replace('#dogs',"") for x in dogs_df['text']]

### Create features and return sparse matricies
vectorizer = sklearn.feature_extraction.text.CountVectorizer(cats_text+dogs_text)
vectorizer.fit(cats_text+dogs_text)
cats_tdm = vectorizer.transform(cats_text).toarray()
dogs_tdm = vectorizer.transform(dogs_text).toarray()

### Create visible matricies and combine
zeros = numpy.zeros((len(cats_text),1))
ones = numpy.ones((len(dogs_text),1))
catsdogs = numpy.concatenate((cats_tdm,dogs_tdm),axis=0)
y = numpy.ravel(numpy.concatenate((zeros,ones),axis=0))

### Create train/test split for modeling
trainX,Xtest,trainY,Ytest = sklearn.model_selection.train_test_split(catsdogs,y,test_size=.25)


### Naive Bayes
nb = sklearn.naive_bayes.GaussianNB()
nb.fit(trainX,trainY)
Ypred = nb.predict(Xtest)

print("\n\nNaive Bayes Performance")
print_score(Ytest,Ypred)

### SVM
svm = sklearn.svm.SVC()
svm.fit(trainX,trainY)
Ypred = svm.predict(Xtest)

print("\n\nSVM performance")
print_score(Ytest,Ypred)

### Neural Network
from sklearn.neural_network import MLPClassifier
nn = MLPClassifier()
nn.fit(trainX,trainY)
Ypred = nn.predict(Xtest)

print("\n\nNeural Network Performance")
print_score(Ytest,Ypred)

### KNN

knn1 = sklearn.neighbors.KNeighborsClassifier(n_neighbors=1)
knn5 = sklearn.neighbors.KNeighborsClassifier(n_neighbors=5)
knn5d = sklearn.neighbors.KNeighborsClassifier(n_neighbors=5,weights='distance')

knn1.fit(trainX,trainY)
knn5.fit(trainX,trainY)
knn5d.fit(trainX,trainY)

print("\n\nKNN 1 Neighbor Performance")
print_score(Ytest,knn1.predict(Xtest))

print("\n\nKNN 5 Neighbor Performance")
print_score(Ytest,knn5.predict(Xtest))

print("\n\nKNN 5 Neighbor Weighted Performance")
print_score(Ytest,knn5d.predict(Xtest))
