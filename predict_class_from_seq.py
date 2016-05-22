import sys
import cPickle as pickle
import seqVectorizer
from vect26FromSeq import vect26FromSeq

def main_exec(seqsFN):

    print '*** loading seqVectorizerObj... '
    pkl_seq_vectorizer = open('seqVectorizerObj.p', 'rb')
    _seqVectorizer = pickle.load(pkl_seq_vectorizer)
    print '*** seqVectorizerObj LOADED'

    print '*** loading v26ClassPredictorSEQObj...'
    pkl_class_predictor = open('v26ClassPredictorSEQObj.p', 'rb')
    _vClassFromSEQ = pickle.load(pkl_class_predictor)
    print '*** v26ClassPredictorSEQObj LOADED'


    print '*** loading v26ClassPredictorObj...'
    pkl_class_predictor = open('v26ClassPredictorObj.p', 'rb')
    _vClassFrom26 = pickle.load(pkl_class_predictor)
    print '*** v26ClassPredictorObj LOADED'


    domainnames, seqs = [], []

    fin = open(seqsFN,'r')
    for l in fin:
        l = l.strip().split(',')
        domname, seq = l[0], l[1]
        domainnames.append(domname)
        seqs.append(seq)

    transformed_seqs = _seqVectorizer.transform(seqs)
    print transformed_seqs

    predicted_classes_SEQ = _vClassFromSEQ.predict(transformed_seqs)
    print predicted_classes

    predicted_vectors = _v26FS.predict(transformed_seqs)
    print predicted_vectors

    predicted_classes = _vClassFrom26.predict(predicted_vectors)
    print predicted_classes


    for d,cs,cv in zip(domainnames,predicted_classes_SEQ,predicted_classes):
        print d, cs, cv




def main():
    #SEQSFN = sys.argv[1]
    main_exec(seqsFN='CASPSEQS.txt')

if __name__ == '__main__':
    main()
