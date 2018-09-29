# -*- coding: utf8

import sqlite3
import pymongo
import datetime
from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb://ryan:8325357@localhost:27017/house')
    return client.house

db = get_db()

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

sqlscript = "SELECT * FROM HOUSE ORDER BY POST_TIME DESC ;"
cursor = c.execute(sqlscript).fetchall()

for elem in cursor:
    temp = ' '.join([x.strip() for x in  elem[4].split()])
    item = {
        'source': elem[0],
        'url': elem[1],
        'title': elem[2],
        'user': elem[3],
        'post_time': datetime.datetime.strptime(temp, '%Y-%m-%d %H:%M:%S'),
        'crawl_time': datetime.datetime.strptime(elem[5], '%Y-%m-%d %H:%M:%S')
    }
    db.rent.update({'title':item['title']}, {"$set": item}, upsert=True)

conn.commit()
conn.close()