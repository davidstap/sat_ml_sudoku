import numpy as np
import matplotlib.pyplot as plt

# Get data
data = np.load('data/ML_data.npy')
print(data.shape)
column_names = data[0,:]
print('-'*80)
print("Number of sudokus used:",data.shape[0]-1)
print("Features used:\n", column_names[:-1],"\n\n")

X = data[1:,:-1].astype(int)
y = data[1:,-1].astype(int)

# Bin y for classification
histo,bin_edges = np.histogram(y,bins=5)
binned_y = np.ones(y.shape[0])
for i in range(0,y.shape[0]):
    for bin_nr in range(bin_edges.shape[0]-1):
        if y[i] > bin_edges[bin_nr] and y[i] <= bin_edges[bin_nr+1] :
            binned_y[i] = int(bin_nr)
            continue
nr_classes = n_neighbors=np.unique(binned_y).shape[0]

## Lasso Regression
from sklearn import linear_model
from sklearn.model_selection import cross_val_score, cross_val_predict
lasso_reg = linear_model.Lasso(alpha = 0.1)
lasso_pred = cross_val_predict(lasso_reg, X, y, cv=5)

# Analyze Lasso results
diff = abs(y-lasso_pred)
print("Lasso regression error mean and std:\n",np.mean(diff), np.std(diff),"\n\n")

## Naive Bayes Classification
print("Number of classes used:",nr_classes)
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
priors = np.array([hist/y.shape[0] for hist in histo])
nb_clf = GaussianNB(priors = priors)
nb_score = cross_val_score(nb_clf, X,binned_y,cv=3)
print("Naive Bayes Scores:\n ", nb_score)



## KNN Classification
from sklearn.neighbors import KNeighborsClassifier
knn_clf = KNeighborsClassifier(nr_classes)
knn_score = cross_val_score(knn_clf, X,binned_y,cv=5)
print("\n\nK-Nearest Neighbor Scores: \n", knn_score)
#
# ## Dummy classifier
from sklearn.dummy import DummyClassifier
dummy_clf = DummyClassifier(strategy="most_frequent")
dummy_score = cross_val_score(dummy_clf, X,binned_y,cv=5)
print("\n\nPredict most frequent class: \n", dummy_score)

## Plot histogram of data binning
# plt.bar([x for x in range(1,histo.shape[0]+1)],histo)
# plt.xlabel('bins')
# plt.ylabel('number of training examples')
# plt.savefig('histogram.jpg')
