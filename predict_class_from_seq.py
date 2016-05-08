import sys
import cPickle as pickle
import seqVectorizer
from vect26FromSeq import vect26FromSeq

def main_exec(seqsFN):

    pkl_seq_vectorizer = open('seqVectorizerObj.p', 'rb')
    _seqVectorizer = pickle.load(pkl_seq_vectorizer)


    pkl_class_predictor = open('v26ClassPredictorSEQObj.p', 'rb')
    _vClassFromSEQ = pickle.load(pkl_class_predictor)


    domainnames, seqs = [], []

    fin = open(seqsFN,'r')
    for l in fin:
        l = l.strip().split(',')
        domname, seq = l[0], l[1]
        domainnames.append(domname)
        seqs.append(seq)

    transformed_seqs = _seqVectorizer.transform(seqs)
    print transformed_seqs

    predicted_classes = _vClassFromSEQ.predict(transformed_seqs)
    print predicted_classes

    for d,c in zip(domainnames,predicted_classes):
        print d, c,




def main():
    #SEQSFN = sys.argv[1]
    main_exec(seqsFN='CASPSEQS.txt')

if __name__ == '__main__':
    main()
