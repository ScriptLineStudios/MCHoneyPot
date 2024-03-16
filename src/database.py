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