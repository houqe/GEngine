# coding : utf-8
# @Time : 2022/10/5 10:54
# @Author : hqe
# @File : MongoDB.py
# @Project : GEngine
from bson import json_util
from pymongo import MongoClient
from log.Log import logger as log
from Settings import mongo_url, mongo_db_name, mongo_task_coll

class MongoDB:
    def __init__(self, url, db_name):
        try:
            self.client = MongoClient(url,connect=False, socketTimeoutMS=300, connectTimeoutMS=300,
                                         serverSelectionTimeoutMS=300)
            self.db_name = db_name
        except Exception as e:
            log.error(e)

    def check_connection(self):
        try:
            self.db_client = self.client.get_database(self.db_name)
            return True
        except Exception as e:
            log.error("Failed to connect to mongodb. {}".format(e))
            return False

    def insert_data(self, collection, data):
        try:
            self.db_client[collection].insert_one(data)
            return True
        except Exception as e:
            log.error("Failed to insert data to mongodb. {}".format(e))
            return False

    def update(self, collection, filter, updates):
        try:
            self.db_client[collection].update_one(filter, {"$set": updates})
            return True
        except Exception as e:
            log.error("Failed to update data in mongodb. {}".format(e))
            return False

    def find_one(self, collection, filter):
        try:
            return self.db_client[collection].find_one(filter)
        except Exception as e:
            log.error("Failed to find data in mongodb. {}".format(e))
            return None

    def find(self, collection, filter):
        try:
            return self.db_client[collection].find(filter)
        except Exception as e:
            log.error("Failed to find data in mongodb. {}".format(e))
            return None



class DBClient:
    def __init__(self):
        if mongo_url and mongo_db_name and mongo_task_coll:
            self.mongo = MongoDB(mongo_url, mongo_db_name)
            self.use_mongodb = self.mongo.check_connection()
            self.mongo_task_collection = mongo_task_coll

    def create_task(self, task_id, targets, vids, start_time):
        task_info = {"task_id": task_id,"status":"run",
                      "data": "Have Run Task, Please Wait.",
                      "start_time": start_time,
                      "poc_id": vids, "target": targets,
                     }
        self.mongo.insert_data(self.mongo_task_collection, task_info)

    def save_result(self, task_id, data, stop_time):
        self.mongo.update(self.mongo_task_collection, {"task_id": task_id}, {"data": data, "stop_time": stop_time, "status": "finish"})

    def get_result(self, task_id):
        data = self.mongo.find_one(self.mongo_task_collection, {"task_id": task_id})
        return json_util.dumps(data)
