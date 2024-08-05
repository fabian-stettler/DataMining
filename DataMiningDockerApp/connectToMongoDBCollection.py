from contextlib import contextmanager

from pymongo import MongoClient

@contextmanager
def connectToMongoDBCollection(database, collection):
    '''
    :param database: database to connect to inside MongoDB
    :param collection_name: collection to connect to inside MongoDB
    :return:
    '''
    client = MongoClient("mongodb://localhost:27017/")
    try:
        db = client[database]
        collection = db[collection]
        yield collection
    finally:
        client.close()
        print("MongoDB connection closed")