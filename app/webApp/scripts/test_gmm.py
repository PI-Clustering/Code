from GMM_clustering import *

from random import random
import matplotlib.pyplot as plt

n = 100
X = [[random()] for i in range(n)]

res = BayesianGaussianMixture(n_components=2, tol=1, max_iter=10).fit(X)

predictions = res.predict(X)


print(type(predictions))

X1 = []
X2 = []
for i in range(len(predictions)):
	if predictions[i] == 0:
		X1.append(X[i][0])
	else:
		X2.append(X[i][0])

plt.hist(X1)
plt.show()
plt.hist(X2)
plt.show()
