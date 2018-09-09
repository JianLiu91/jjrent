# -*- coding: utf8

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

cursor = c.execute("SELECT * from HOUSE")
for row in cursor:
    print row

conn.commit()
conn.close()