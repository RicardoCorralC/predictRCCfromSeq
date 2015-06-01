import sys
import makeTransformedSeqDataset
import makeUnifiedDatasets
import vect26FromSeq
import make_final_training_datasets
import train_and_save_clf
import getMissingClassAccuracy
import getMissingClassAccuracySEQ
from pymongo import MongoClient
import time

MONGODB_URI = 'mongodb://rcorral:mongolabpass12483@ds043022.mongolab.com:43022/rccvsseqaccs'
collection_name = 'dropedclassaccs'

def main_exec(CathDomainSeqsATOM='CathDomainSeqs.ATOM.v4.0.0',
                combLength=3,
                familyToDrop='3_20_20_120',
                CATHv26DB='CATHFINAL.txt',
                aaGroupingList='F_Ic4list',
                testTrainingLevel=3): #for C, CA, CAT,..


    testClass = '_'.join(familyToDrop.split('_')[:3]) #+ '_'


    #first open db connection
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    collection = db[collection_name]

    print '\n*** Connection to Database established'


    _start = time.time()



    makeTransformedSeqDataset.main_exec(FILENAME=CathDomainSeqsATOM,
                                        COMBLENGTH=combLength,
                                        SKIPCLASS=familyToDrop,
                                        CATHVDBNAME=CATHv26DB,
                                        aaGroupingList=aaGroupingList)

    print '\n*** Finished [makeTransformedSeqDataset]'





    uniqueID = makeUnifiedDatasets.main_exec(seqsFN='transformedSeqDataset_'+str(combLength).strip()+'.txt',
                                                vecsFN=CATHv26DB)
    print '\n*** Finished [makeUnifiedDatasets]'






    vect26FromSeq.main_exec(seqsFN='SEQS_'+uniqueID+'.txt',
                            vecsFN='VECS_'+uniqueID+'.txt',
                            domsFN='DOMS_'+uniqueID+'.txt',
                            id=uniqueID)

    print '\n*** Finished [vect26FromSeq]'






    make_final_training_datasets.main_exec(rawfn='transformedSeqDataset_'+combLength+'.txt',
                                            predfn='predictedVectors_'+uniqueID+'.txt',
                                            realvfn=CATHv26DB,
                                            id=uniqueID)

    print '\n*** Finished [make_final_training_datasets]'







    train_and_save_clf.main_exec(fn='trainable_26dpredicted_'+uniqueID+'.txt',level=testTrainingLevel,seqflag=0)
    print '\n*** Finished [train_and_save_clf for v26predicted]'


    train_and_save_clf.main_exec(fn='trainable_raw_'+uniqueID+'.txt',level=testTrainingLevel,seqflag=1)
    print '\n*** Finished [train_and_save_clf for seq]'






    print ' - testing for class', testClass, 'on v26'
    _ACC_RCC = getMissingClassAccuracy.main_exec(seqsFN='CathDomainSeqs_TESTING_'+familyToDrop+'.txt',
                                        targetClass=testClass)

    print '\n*** Finished [getMissingClassAccuracy] with ACC:', _ACC_RCC







    print ' - testing for class', testClass, 'on seq'
    _ACC_SEQ = getMissingClassAccuracySEQ.main_exec(seqsFN='CathDomainSeqs_TESTING_'+familyToDrop+'.txt',
                                        targetClass=testClass)
    print '\n*** Finished [getMissingClassAccuracySEQ] with ACC:', _ACC_SEQ





    print '\nACCs for RCC and SEQ:', _ACC_RCC, _ACC_SEQ


    _end = time.time()
    _exectimesecs = (_end - _start)
    print '*** Elapsed time: ', _exectimesecs


    collection.update({'droppedfam':familyToDrop},{ '$set': {'RCCacc':_ACC_RCC,
                                                            'SEQacc':_ACC_SEQ,
                                                            'combLength':combLength,
                                                            'aaGroupingList':aaGroupingList,
                                                            '_exectimesecs':_exectimesecs} },**{'upsert':True})

    print '[FINISHED]'

def main():
	FILENAME = 'CathDomainSeqs.ATOM.v4.0.0'
	COMBLENGTH = sys.argv[1]
	SKIPCLASS = sys.argv[2].strip() #If None, no class is skipped, example 2 or 2_3, or 2_4_5,..
	CATHVDBNAME = 'CATHFINAL.txt'
	aaGroupingList='F_Ic4list'
	main_exec(CathDomainSeqsATOM=FILENAME,
                combLength=COMBLENGTH,
                familyToDrop=SKIPCLASS,
                CATHv26DB=CATHVDBNAME,
                aaGroupingList=aaGroupingList)

if __name__ == '__main__':
    main()
