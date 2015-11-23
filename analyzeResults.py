import settings

from pymongo import MongoClient

MONGODB_URI = settings.MONGODB_URI
collection_name = settings.collection_name


class analyzer(object):
    def __init__(self, mongodb_uri=None, collection_name=None):
        client = MongoClient(mongodb_uri)
        db = client.get_default_database()
        self.collection = db[collection_name]

        self.results = [result
                        for result in self.collection.find(
                            {}, {'_id': False})]

        print self.results


if __name__ == '__main__':
    _analyzer = analyzer(mongodb_uri=MONGODB_URI,
                         collection_name=collection_name)
