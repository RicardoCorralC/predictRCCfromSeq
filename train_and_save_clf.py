import sys
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn import cross_validation
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.kernel_approximation import Nystroem
import cPickle as pickle

def main_exec(fn,level,seqflag):

	fin = open(fn)

	V = []
	C = []

	for l in fin:
		l = l.strip().split(',')
		v = map(float,l[1:-1])
		c = l[-1]
		c = c.split('_')
		c = c[:level]
		c = '_'.join(c)

		V.append(v)
		C.append(c)

	V = np.asarray(V)
	C = np.asarray(C).ravel()

	clf = RandomForestClassifier(n_estimators=7)
	clf.fit(V,C)

	if seqflag:
	    pickle.dump( clf , open( "v26ClassPredictorSEQObj.p", "wb" ) )
	else:
	    pickle.dump( clf , open( "v26ClassPredictorObj.p", "wb" ) )



def main():
	FN = sys.argv[1] # trainable_26dreal
	LEVEL = int(sys.argv[2]) # 1: cass, 2:architecture, 3:topology, 4:homology
	SEQFLAG = int(sys.argv[3]) #If true, save a classifier from sequence

	main_exec(fn=FN,level=LEVEL,seqflag=SEQFLAG)



if __name__ == '__main__':
	main()
