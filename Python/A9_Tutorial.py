#!/usr/bin/env python3
###
### Tutorial using Python Scikit-Learn
### Dataset: PIMA Diabetes, from the UC Irvine Machine Learning Repository
### https://archive.ics.uci.edu/ml/datasets/Pima+Indians+Diabetes
###
import sys,os,re
import urllib.request
import pandas
import numpy
import sklearn
import sklearn.model_selection
import sklearn.metrics
import sklearn.naive_bayes
import sklearn.neural_network

###
def print_score(true,pred):
  print("precision: %.2f ; recall: %.2f ; F1: %.2f"%(
	sklearn.metrics.precision_score(true,pred),
	sklearn.metrics.recall_score(true,pred),
	sklearn.metrics.f1_score(true,pred)), file=sys.stderr)


###
# Read dataset into pandas DataFrame:
fin = urllib.request.urlopen("http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data")

pima_df = pandas.read_csv(fin, header=None,
	names = [
	"number_of_times_pregnant",
	"plasma_glucose_concentration",
	"diastolic_blood_pressure",
	"triceps_skin_fold_thickness",
	"serum_insulin",
	"body_mass_index",
	"diabetes_pedigree",
	"age",
	"class"])

fin.close()
print(pima_df.head(), file=sys.stderr)
nrows,ncols = pima_df.shape
print("dataset ncols: %d ; nrows: %d:"%(ncols,nrows), file=sys.stderr)

# Read metadata
fin = urllib.request.urlopen("http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.names")
pima_metadata = fin.read().decode('utf8')
fin.close()
print("DEBUG: metadata size: %d bytes"%len(pima_metadata), file=sys.stderr)
 
###
# Separate input variables and class labels into X and y Numpy arrays for sklearn.
y = pima_df['class'].as_matrix()
X = pima_df.iloc[:,0:ncols-1].as_matrix()

###
#Create train/test split for modeling
trainX,testX,trainY,testY = sklearn.model_selection.train_test_split(X, y, test_size=.25)

print("training set: %s ; test set: %s"%(trainX.shape, testX.shape), file=sys.stderr)

###
#Naive Bayes
nb = sklearn.naive_bayes.GaussianNB()
nb.fit(trainX,trainY)

print("\n\nNaive Bayes Performance")
print_score(testY,nb.predict(testX))

###
#Neural Network
nn = sklearn.neural_network.MLPClassifier()
nn.fit(trainX,trainY)

print("\n\nNeural Network Performance")
print_score(testY,nn.predict(testX))

