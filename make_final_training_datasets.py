#########This program is intended to take 
#a dataset with domainid and raw seq attributes,
#a dataset with dimainid and predicted 26d vector,
#a dataset with domainid real 26d vector and a classification
#
#The output is a trainable dataset with raw seq attributes and  with predicted 26dv, both with a classification to learn
##########

import sys

rawfin = open(sys.argv[1]) #transformedSeqDataset_2.txt
predfin = open(sys.argv[2]) #predictedVectors_3450737717.txt
realvfin = open(sys.argv[3]) # CATHALL.txt

fn =  sys.argv[1]
ID = fn[fn.find('_')+1:fn.find('.')]

rawdict = {}
preddict = {}
realclassesdict = {}
realvecsdict = {}


for r in rawfin:
	r = r.strip().split(',')
	domname = r[0]
	attributes = r[1:]
	rawdict[domname] = attributes


for r in predfin:
	r = r.strip().split(',')
	domname = r[0]
	attributes = r[1:]
	preddict[domname] = attributes


for r in realvfin:
	r = r.strip().split(',')
	domname = r[0]
	realvect = r[1:27]
	classif = r[-1]
	realclassesdict[domname] = classif
	realvecsdict[domname] = realvect


rawfout = open('trainable_raw_'+ID+'.txt','w')
predictedfout = open('trainable_26dpredicted_'+ID+'.txt','w')
realfout = open('trainable_26dreal_'+ID+'.txt','w')

print rawdict
print len(rawdict)

for k in realclassesdict:
	if not k in rawdict: continue
	if not k in preddict: continue
	rawfout.write("%s,%s,%s\n" % (k,','.join(rawdict[k]) , realclassesdict[k] ) )
	predictedfout.write("%s,%s,%s\n" % (k,','.join(preddict[k]) , realclassesdict[k] ) )
	realfout.write("%s,%s,%s\n" % (k,','.join(realvecsdict[k]) , realclassesdict[k] ) )



