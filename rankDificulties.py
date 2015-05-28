import sys
from scipy.spatial.distance import euclidean
import numpy as np
import operator

def main():
    seqsf = open(sys.argv[1],'r')
    vectf = open(sys.argv[2],'r')

    seqsclass, vectsclass = [],[]
    seqsnames, vectnames = [], []
    seqslist, vectslist = [], []
    sclasses, vclasses = set(), set()

    print '*** Loading data'

    for l in seqsf:
        l = l.strip().split(',')
        seqsnames.append(l[0])
        seqslist.append(map(float,l[1:-1]) )
        seqsclass.append(l[-1])
        sclasses.add(l[-1])

    seqslist = np.array(seqslist)


    for l in vectf:
        l = l.strip().split(',')
        vectnames.append(l[0])
        vectslist.append(map(float,l[1:-1]) )
        vectsclass.append(l[-1])
        vclasses.add(l[-1])

    print '*** Data loaded\n'

    print '*** Computing dificulties'
    scscores = dict()
    for sc in sclasses:
        mindist = 99999999.0
        if not sc.startswith("3_30_70_"): continue
        print '\n * Getting score for class', sc
        for si in xrange(len(seqslist)):
            if seqsclass[si] != sc: continue
            for sj in xrange(len(seqslist)):
                if si == sj: continue
                if seqsclass[sj] == sc: continue
                dist = euclidean(seqslist[si], seqslist[sj])
                if dist < mindist: mindist = dist
        print mindist

        scscores[sc] = mindist

    sortedscores = sorted(scscores.items(), key=operator.itemgetter(1))
    for _a, _b in sortedscores:
        print _a + '   ' + str(_b).ljust(10)

    return scscores, sortedscores

if __name__ == '__main__':
    main()
