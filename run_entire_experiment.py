from pymongo import MongoClient
import computeACCdroppingFamily
from random import shuffle
import settings

MONGODB_URI = settings.MONGODB_URI
collection_name = settings.collection_name



def get_hs(cathfile='CATHFINAL.txt'):
    hs = set()
    for l in open(cathfile,'r'):
        ll = l.strip().split(',')
        _h = ll[-1]
        hs.add(_h)
    hs = list(hs)[:]
    shuffle(hs)
    return hs

def run_experiment(hslist=[]):
    print '\nopening DB connection...'
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    collection = db[collection_name]
    print 'done\n'
    for h in hslist:
        res = collection.find_one({'droppedfam':h})
        print res
        if not res:
            print 'starting experiment for ', h
            computeACCdroppingFamily.main_exec(familyToDrop=h)

if __name__ == '__main__':
    print '\ngetting Hs'
    hslist = get_hs()
    print 'done\n'
    print 'running experiment..'
    run_experiment(hslist=hslist)
