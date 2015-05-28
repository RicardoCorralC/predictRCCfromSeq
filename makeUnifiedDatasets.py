import sys
import random

if __name__ == '__main__':
	seqsFN = sys.argv[1] #transformedSeqDataset_X.txt
	vecsFN = sys.argv[2] #CATHALL.txt
	seqsFIN = open(seqsFN,'r')
	vecsFIN = open(vecsFN,'r')

	seqsD = dict()
	vecsD = dict()

	for s in seqsFIN:
		s = s.strip().split(',')
		seqsD[s[0]] = s[1:]

	for v in vecsFIN:
		v = v.strip().split(',')
		vecsD[v[0]] = v[1:-1]

	uniqueID = str(hash(random.random()))
	seqsFOUT = open('SEQS_'+uniqueID+'.txt','w')
	vecsFOUT = open('VECS_'+uniqueID+'.txt','w')
	domsFOUT = open('DOMS_'+uniqueID+'.txt','w')

	for kv in vecsD:
		if not kv in seqsD: continue
		seqsFOUT.write('%s\n' % ','.join(seqsD[kv]))
		vecsFOUT.write('%s\n' % ','.join(vecsD[kv]))
		domsFOUT.write('%s\n' % kv)

	print 'finished with ID', uniqueID


