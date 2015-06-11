# Ricardo Corral Corral, June 2015
# Easy model evaluation over CATH and SCOP datasets

import sys
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn import grid_search
from collections import Counter



def dbParser(db,level=1,dbtype='CATH',minsamples=100):
    if dbtype == 'CATH':
        sepchar = '_'
    elif dbtype == 'SCOP':
        sepchar = '.'

    _c = Counter()
    domnames, vects, classifs = [], [], []
    domnames2, vects2, classifs2 = [], [], []

    fin = open(db)
    for l in fin:
        l = l.strip().split(',')
        domnames.append(l[0])
        vects.append( map(float,l[1:-1]) )
        _class = '_'.join(l[-1].split( sepchar )[:level])
        classifs.append(  _class  )
        _c[_class] += 1

    skippedclasses = set()
    for i in xrange(len(domnames)):
        if _c[classifs[i]] < minsamples:
            skippedclasses.add( classifs[i] )
            continue
        domnames2.append( domnames[i] )
        vects2.append( vects[i] )
        classifs2.append( classifs[i] )

    print 'Classess skipped having less than ', minsamples, 'samples:\n', '\n'.join(skippedclasses)


    dataDict = dict()
    dataDict['domain_names'] = np.asarray(domnames2)
    dataDict['vectors'] = np.asarray(vects2)
    dataDict['target_names'] = np.asarray(classifs2)
    return dataDict



def makeTuning(dataset,dbtype='CATH',level=1,k_iters=3):
    if dbtype == 'CATH':
        dataDict = dbParser(dataset,level=level,dbtype=dbtype)
        print dataDict

        labels = dataDict['target_names']
        skf = StratifiedKFold(labels, k_iters)

        clf = ExtraTreesClassifier(n_estimators=50)

        parameters = {"min_samples_split":[1,2,3,4,5], "max_depth":[None,1,2,3,4,5]}

        _clf = grid_search.GridSearchCV(clf, parameters)
        _clf.fit(dataDict['vectors'], dataDict['target_names'])
        print _clf.get_params()
        #_clf.fit(iris.data, iris.target)

def makeAllEvals(dataset,dbtype='CATH',level=1,k_iters=10):

    dataDict = dbParser(dataset,level=level,dbtype=dbtype)
    print dataDict

    labels = dataDict['target_names']
    skf = StratifiedKFold(labels, k_iters)

    #Level 1
    #clf = ExtraTreesClassifier(n_estimators=100,min_samples_split=2,max_depth=None)
    #Level 2
    clf = ExtraTreesClassifier(n_estimators=300,min_samples_split=2,max_depth=None)

    accsList = []

    for train, test in skf:
        print '\n--------------------------------------------------\n'
        _train = [dataDict['vectors'][i] for i in train]
        _test = [dataDict['vectors'][i] for i in test]
        _targets = [dataDict['target_names'][i] for i in train]

        clf.fit(_train,_targets)

        y_true = [labels[i] for i in test]
        y_pred = clf.predict(_test)


        localAccuracy = accuracy_score(y_true, y_pred)
        accsList.append(localAccuracy)
        print '*** localAccuracy:', localAccuracy

        print(classification_report(y_true, y_pred))

        cm = confusion_matrix(y_true, y_pred,labels=clf.classes_)
        print cm

    _ACC = np.mean(accsList)
    _ACCstd = np.std(accsList)

    print '\n[ FINAL SUMMARY ]'
    print ' *** ACCURACY: ', _ACC
    print ' *** ACCURACY deviation: ', _ACCstd



def main():
    fn = sys.argv[1]
    level = int(sys.argv[2])
    dbtype = sys.argv[3]

    #makeTuning(dataset=fn,level=level,dbtype=dbtype)
    #exit()
    makeAllEvals(dataset=fn,level=level,dbtype=dbtype)

if __name__ == '__main__':
    main()
