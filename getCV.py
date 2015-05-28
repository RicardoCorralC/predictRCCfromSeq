import sys
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.kernel_approximation import Nystroem

fin = open(sys.argv[1])

LEVEL = 2

V = []
C = []

for l in fin:
	l = l.strip().split(',')
	v = map(float,l[1:-1])
	c = l[-1]
	c = c.split('_')
	c = c[:LEVEL]
	c = '_'.join(c)

	V.append(v)
	C.append(c)

V = np.asarray(V)
C = np.asarray(C).ravel()

clf = RandomForestClassifier(n_estimators=5)
le = preprocessing.LabelEncoder()

C = le.fit_transform(C)

print V.shape, C.shape
scores = cross_validation.cross_val_score(clf, V, C, cv=10)

print scores
print 'CV', scores.mean()
