import sys
import cPickle as pickle
import seqVectorizer
from vect26FromSeq import vect26FromSeq

def main_exec(seqsFN,targetClass):

    pkl_seq_vectorizer = open('seqVectorizerObj.p', 'rb')
    _seqVectorizer = pickle.load(pkl_seq_vectorizer)

    pkl_v26_predictor = open('v26FSObj.p', 'rb')
    _v26FS = pickle.load(pkl_v26_predictor)

    pkl_class_predictor = open('v26ClassPredictorObj.p', 'rb')
    _vClassFrom26 = pickle.load(pkl_class_predictor)


    domainnames, seqs = [], []

    fin = open(seqsFN,'r')
    for l in fin:
        l = l.strip().split(',')
        domname, seq = l[0], l[1]
        domainnames.append(domname)
        seqs.append(seq)

    transformed_seqs = _seqVectorizer.transform(seqs)
    print transformed_seqs

    predicted_vectors = _v26FS.predict(transformed_seqs)
    print predicted_vectors

    predicted_classes = _vClassFrom26.predict(predicted_vectors)
    print predicted_classes

    for d,c in zip(domainnames,predicted_classes):
        print d, c,
        if c.startswith(targetClass): print '\t*'
        else: print ''


    print len(predicted_classes)
    same_classes = filter(lambda x: x.startswith(targetClass),predicted_classes)
    _ACC =  len(same_classes)/float(len(predicted_classes))
    print '\n***Accuracy for predicting class', targetClass, ':',
    print _ACC, '\n'
    return _ACC


def main():
    SEQSFN = sys.argv[1]
    TARGETCLASS = sys.argv[2]
    main_exec(seqsFN=SEQSFN,targetClass=TARGETCLASS)

if __name__ == '__main__':
    main()
