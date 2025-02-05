import os
import sys
import json
import certifi

import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from dotenv import load_dotenv
load_dotenv()

MONGO_URL_KEY=os.getenv("MONGO_URL_KEY")
print(MONGO_URL_KEY)

ca=certifi.where()

class NetworkDataExtraction():
    def __init__(self):
        try:
          pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def cv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records= list(json.loads(data.T.to_json()).values())  ##T- transpose
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client =pymongo.MongoClient(MONGO_URL_KEY)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__=='__main__':
    try:
        FILE_PATH="Network_Data\phisingData.csv"
        database="MongoDbTest"
        collection="NetworkData"
        networkobj=NetworkDataExtraction()
        records=networkobj.cv_to_json_converter(file_path=FILE_PATH)
        print(records)
        no_of_records=networkobj.insert_data_to_mongodb(records, database, collection)
        print( no_of_records)
        logging.info(f"Data inserted successfully, length of data is {no_of_records}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    