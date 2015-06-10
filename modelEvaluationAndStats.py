import sys
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import classification_report
from sklearn.cross_validation import StratifiedKFold


def cathParser(db,level=1):
    domnames, vects, classifs = [], [], []
    fin = open(db)
    for l in fin:
        l = l.strip().split(',')
        domnames.append(l[0])
        vects.append( map(float,l[1:-1]) )
        classifs.append(  '_'.join(l[-1].split('_')[:level])  )

    dataDict = dict()
    dataDict['domain_names'] = np.asarray(domnames)
    dataDict['vectors'] = np.asarray(vects)
    dataDict['target_names'] = np.asarray(classifs)
    return dataDict



def makeAllEvals(dataset,dbtype='CATH',level=1):

    if dbtype == 'CATH':
        dataDict = cathParser(dataset,level=level)
        print dataDict

        labels = dataDict['target_names']
        skf = StratifiedKFold(labels, 3)

        clf = ExtraTreesClassifier()

        for train, test in skf:
            _train = [dataDict['vectors'][i] for i in train]
            _test = [dataDict['vectors'][i] for i in test]
            _targets = [dataDict['target_names'][i] for i in train]

            clf.fit(_train,_targets)

            y_true = [labels[i] for i in test]
            y_pred = clf.predict(_test)

            print(classification_report(y_true, y_pred))


def main():
    fn = sys.argv[1]
    level = int(sys.argv[2])

    makeAllEvals(dataset=fn,level=level)

if __name__ == '__main__':
    main()
