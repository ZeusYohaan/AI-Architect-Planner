from pymongo import MongoClient
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')


def connect_to_mongo():
    client = MongoClient(config["mongo connection"]["host"]+":"+config["mongo connection"]["port"],
                        username=config["mongo connection"]["username"],
                        password=config["mongo connection"]["password"],
                        authSource=config["mongo connection"]["authSource"],
                        authMechanism=config["mongo connection"]["authMechanism"])
    return client

def get_collection():
    database = config["mongo connection"]["database"]
    collection = config["mongo connection"]["collection"]
    client = connect_to_mongo()
    db = client[database]
    collection = db[collection]
    return collection

