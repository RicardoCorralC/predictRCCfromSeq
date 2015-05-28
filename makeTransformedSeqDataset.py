import seqVectorizer
import sys
import cPickle as pickle


def main():
	FILENAME = sys.argv[1] #CathDomainSeqs.ATOM.v3.5.0
	COMBLENGTH = sys.argv[2]
	f = open(FILENAME,'r')


	SKIPCLASS = sys.argv[3].strip() #If None, no class is skipped, example 2 or 2_3, or 2_4_5,..
	CATHVDBNAME = sys.argv[4]
	avoidDomains = set() #will contains domains belonging to class SKIPCLASS

	if SKIPCLASS != 'None':
		#Filename with domname,26dvector,classname format

		fin = open(CATHVDBNAME,'r')
		for l in fin:
			l = l.strip().split(',')
			domname, vector, clase = l[0], map(int,l[1:-1]), l[-1]
			if clase.startswith(SKIPCLASS):
				avoidDomains.add(domname)
		fin.close()

	_seqVectorizer = seqVectorizer.seqVectorizer(comblength=int(COMBLENGTH),aaGroupingList='F_Ic4list',verbose=True)

	domainNames = []
	seqs = []

	fout_test = open('CathDomainSeqs_TESTING_'+SKIPCLASS+'.txt','w')

	while True:
		#domainName = f.readline().strip()[8:15] #v 3.5 format
		domainName = f.readline().strip()[12:19]
		if domainName == '': break #testing EOF
		seq = f.readline().strip()

		if domainName in avoidDomains:
			fout_test.write("%s,%s\n" % (domainName,seq) )
			continue

		#if 'X' in seq: break  #No mapping for aminoacid X
		print 'reading', domainName
		domainNames.append(domainName)
		seqs.append(seq)

	fout_test.close()

	print len(domainNames), len(seqs)

	transformedSeqs = _seqVectorizer.fit_transform(seqs)
	pickle.dump( _seqVectorizer , open( "seqVectorizerObj.p", "wb" ) )

	OUTFILENAME = 'transformedSeqDataset_' + COMBLENGTH + '.txt'
	fout = open(OUTFILENAME,'w')

	for i in xrange(len(transformedSeqs)):
		sres = ','.join([str(x) for x in transformedSeqs[i]])
		fout.write('%s,%s\n' % (domainNames[i],sres))

if __name__ == '__main__':
	main()
