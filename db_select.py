# -*- coding: utf8
import pymongo
from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb://ryan:8325357@localhost:27017/house')
    return client.house

if __name__ == '__main__':
    db = get_db()
    rent_col = db.rent

    for x in rent_col.find({"title": { "$regex": '.*出租.*', "$options": "si" }}):
        print x['title']