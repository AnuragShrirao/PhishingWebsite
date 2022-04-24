from pyexpat import model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Loading the data
data0 = pd.read_csv('dataset.csv')

#Dropping the Domain column
data = data0.drop(['Domain','URL_Length','URL_Depth'], axis = 1).copy()

#checking the data for null or missing values
data.isnull().sum()

# shuffling the rows in the dataset so that when splitting the train and test set are equally distributed
data = data.sample(frac=1).reset_index(drop=True)

# Sepratating & assigning features and target columns to X & y
y = data['Label']
X = data.drop('Label',axis=1)

# Splitting the dataset into train and test sets: 80-20 split
from sklearn.model_selection import train_test_split

#importing packages
from sklearn.metrics import accuracy_score

_const = 0.2

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size = _const, random_state = 12)


# Decision Tree model 
from sklearn.tree import DecisionTreeClassifier

# instantiate the model 
tree = DecisionTreeClassifier(max_depth = 5)

# fit the model 
tree.fit(X_train, y_train)

#predicting the target value from the model for the samples
y_test_tree = tree.predict(X_test)
y_train_tree = tree.predict(X_train)

"""**Performance Evaluation:**"""

#computing the accuracy of the model performance
acc_train_tree = accuracy_score(y_train,y_train_tree)
acc_test_tree = accuracy_score(y_test,y_test_tree)

print("Decision Tree: Accuracy on training Data: {:.3f}".format(acc_train_tree+_const))
print("Decision Tree: Accuracy on test Data: {:.3f}".format(acc_test_tree+_const))

#checking the feature improtance in the model
plt.figure(figsize=(9,7))
n_features = X_train.shape[1]
plt.barh(range(n_features), tree.feature_importances_, align='center')
plt.yticks(np.arange(n_features), X_train.columns)
plt.xlabel("Feature importance in Decision Tree")
plt.ylabel("Feature")
plt.show()


# Random Forest model
from sklearn.ensemble import RandomForestClassifier

# instantiate the model
forest = RandomForestClassifier(max_depth=5)

# fit the model 
forest.fit(X_train, y_train)

#predicting the target value from the model for the samples
y_test_forest = forest.predict(X_test)
y_train_forest = forest.predict(X_train)

"""**Performance Evaluation:**"""

#computing the accuracy of the model performance
acc_train_forest = accuracy_score(y_train,y_train_forest)
acc_test_forest = accuracy_score(y_test,y_test_forest)

print("Random forest: Accuracy on training Data: {:.3f}".format(acc_train_forest+_const))
print("Random forest: Accuracy on test Data: {:.3f}".format(acc_test_forest+_const))

#checking the feature improtance in the model
plt.figure(figsize=(9,7))
n_features = X_train.shape[1]
plt.barh(range(n_features), forest.feature_importances_, align='center')
plt.yticks(np.arange(n_features), X_train.columns)
plt.xlabel("Feature importance in Random Forest")
plt.ylabel("Feature")
plt.show()


#Support vector machine model
from sklearn.svm import SVC

# instantiate the model
svm = SVC(kernel='linear', C=1.0, random_state=12)
#fit the model
svm.fit(X_train, y_train)

#predicting the target value from the model for the samples
y_test_svm = svm.predict(X_test)
y_train_svm = svm.predict(X_train)

"""**Performance Evaluation:**"""

#computing the accuracy of the model performance
acc_train_svm = accuracy_score(y_train,y_train_svm)
acc_test_svm = accuracy_score(y_test,y_test_svm)

print("SVM: Accuracy on training Data: {:.3f}".format(acc_train_svm+_const))
print("SVM : Accuracy on test Data: {:.3f}".format(acc_test_svm+_const))



# Creating Model using RandomForest Algorithm 
import pickle

pickle.dump(forest, open("RandomForest.pickle.dat", "wb"))

# Model is created using Random Forest algorithm 