import pymongo
from pymongo.mongo_client import MongoClient
from src.config import config
import logging

class Database:
    def __init__(self):
        self.client = MongoClient(config.mongo_uri)
        self.db = self.client[config.database_name]
        self.join_collection = self.db["Joins"]
        self.ping_collection = self.db["Pings"]
        self.report_collection = self.db["Reports"]

    def insert_join(self, record):
        logging.info("Inserting record into join collection")
        self.join_collection.insert_one(record)
    
    def insert_ping(self, record):
        logging.info("Inserting record into ping collection")
        self.ping_collection.insert_one(record)

    def insert_report(self, record):
        logging.info("Inserting record into report collection")
        self.report_collection.insert_one(record)

    def get_latest_join(self, num=1):
        latest_doc = self.join_collection.find().sort("_id", pymongo.DESCENDING).limit(num)
        return latest_doc

    def get_latest_ping(self, num=1):
        latest_doc = self.ping_collection.find().sort("_id", pymongo.DESCENDING).limit(num)
        return latest_doc

    def get_latest_report(self, num=1):
        latest_doc = self.report_collection.find().sort("_id", pymongo.DESCENDING).limit(num)
        return latest_doc

    def get_join_size(self):
        return self.join_collection.estimated_document_count()

    def get_ping_size(self):
        return self.ping_collection.estimated_document_count()

    def get_report_size(self):
        return self.report_collection.estimated_document_count()

# print(Database().get_latest_join()[0]["_id"].generation_time)