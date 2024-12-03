import json
from pymongo import MongoClient, errors

class Database:
    def __init__(self, db_name="alumno", collection_name="alumnos"):
        self.client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=5000)
        self.db_name = self.client[db_name]
        self.collection_name = self.db_name[collection_name]

    def guardar(self,documento):
        self.collection_name.insert_many(documento)

    def ping(self):
        try:
            self.client.admin.command("ping")
            return True
        except:
            return False
        
if __name__ == "__main__":
    database = Database("3clases", "alumnos")
    print(database)