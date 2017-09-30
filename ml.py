import numpy as np

# Get data
data = np.load('data/ML_data.npy')
column_names = data[0,:]
X = data[1:,:-1].astype(int)
y = data[1:,-1].astype(int)
# print('mean',np.mean(y),'std', np.std(y),'sorted', np.sort(y))

# Lasso Regression
from sklearn import linear_model
from sklearn.model_selection import cross_val_score
lasso_reg = linear_model.Lasso(alpha = 0.1)
lasso_scores = cross_val_score(lasso_reg, X, y, cv=5)

# SGD Regression (N>100.000)
sgd_reg = linear_model.SGDRegressor()
sgd_scores = cross_val_score(sgd_reg, X, y, cv=5)

print(lasso_scores)
print(sgd_scores)
