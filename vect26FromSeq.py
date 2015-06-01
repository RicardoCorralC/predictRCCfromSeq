from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import numpy as np
import sys
import cPickle as pickle
import copy

from sklearn.pipeline import Pipeline
from random_layer import *
from elm import *

DIMS = 26

class vect26FromSeq(object):
	def __init__(self):
		nh = 50
		#r2 = GRBFRandomLayer(n_hidden = nh, centers=ctrs)
		#r3 = RBFRandomLayer( n_hidden = nh, activation_func='multiquadric')


		#elm = GenELMRegressor( hidden_layer = r2 )
		#_clf = Pipeline( [ #('pca',pca),
								#('normalize',normalize()),
								#( 'rl', rl ),
								#('rl',r3),

		#						( 'classifier', LogisticRegression() )] )

		_clf = ExtraTreesClassifier(n_estimators=15,n_jobs=3,verbose=1)#LogisticRegression()#(n_estimators=4)
		self.classifiers = [copy.deepcopy(_clf) for i in xrange(DIMS)]

	def fit(self,rawTransformedSeqs,vectors26):
		for i in xrange(DIMS):
			self.classifiers[i].fit(rawTransformedSeqs,vectors26[:,i])
			print rawTransformedSeqs.shape, vectors26[:,i].shape
			print 'trained classifier for component number', i

	def predict(self,X):
		res = []
		for x in X:
			vpredicted = [self.classifiers[i].predict([x])[0] for i in xrange(DIMS)]
			res.append(vpredicted)
		return res


def main_exec(seqsFN='SEQS_2281725600.txt',vecsFN='VECS_2281725600.txt',domsFN='DOMS_2281725600.txt',id='2281725600'):

	seqsFIN = open(seqsFN)
	vecsFIN = open(vecsFN)
	domsFIN = open(domsFN)
	ID = id

	rawTransformedSeqs = []
	vectors26 = []
	domainNames = []

	for s in seqsFIN:
		s = s.strip().split(',')
		s = map(float,s)
		rawTransformedSeqs.append(s)

	for v in vecsFIN:
		v = v.strip().split(',')
		v = map(int,v)
		vectors26.append(v)

	for d in domsFIN:
		d = d.strip().split(',')[0]
		domainNames.append(d)

	rawTransformedSeqs = np.asarray(rawTransformedSeqs)
	vectors26 = np.asarray(vectors26)

	_v26FS = vect26FromSeq()
	_v26FS.fit(rawTransformedSeqs=rawTransformedSeqs,vectors26=vectors26)

	pickle.dump( _v26FS , open( "v26FSObj.p", "wb" ) )

	#print _v26FS.classifiers[0].intercept_

	res = _v26FS.predict(rawTransformedSeqs)

	predictedVectors = open('predictedVectors_'+ID+'.txt','w')
	for i in xrange(len(res)):
		r = res[i]
		try:
			predictedVectors.write('%s,%s\n' % (domainNames[i],','.join( map(str,r) ) ) )
		except:
			print r

	predictedVectors.close()

def main():
	seqsFN = sys.argv[1],'r'
	vecsFN = sys.argv[2],'r'
	domsFN = sys.argv[3],'r'
	ID = sys.argv[1][5:-4]
	main_exec(seqsFN=seqsFN,vecsFN=vecsFN,domsFN=domsFN,id=ID)


if __name__ == '__main__':
	main()
