from pymongo import MongoClient
import computeACCdroppingFamily

MONGODB_URI = 'mongodb://rcorral:mongolabpass12483@ds043022.mongolab.com:43022/rccvsseqaccs'
collection_name = 'dropedclassaccs'



def get_hs(cathfile='CATHFINAL.txt'):
    hs = set()
    for l in open(cathfile,'r'):
        ll = l.strip().split(',')
        _h = ll[-1]
        hs.add(_h)
    return list(hs)

def run_experiment(hslist=[]):
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    collection = db[collection_name]
    for h in hslist:
        if not collection.find_one({'droppedfam':h}):
            computeACCdroppingFamily.main_exec(familyToDrop=familyToDrop)

if __name__ == '__main__':
    print '\ngetting Hs'
    hslist = get_hs()
    print 'done\n'
    print 'running experiment..'
    run_experiment(hslist=hslist)
