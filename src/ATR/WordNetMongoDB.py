from pymongo import MongoClient

class ConnectionMongoDB(object):

    def find_terms(self,term):
        client = MongoClient('localhost',27017)
        db = client['Wonef']
        synset_collection = db['SYNSET']
        #count the obtained result
        #count = synset_collection.find({"SYNONYM.LITERAL.#text": {"$regex": '.*'+term + '.*'}}).count()
        count = synset_collection.find({"SYNONYM.LITERAL.#text": {"$regex": "^"+term + "$", "$options": 'i'}}).count()
        return count
