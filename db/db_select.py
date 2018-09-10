# -*- coding: utf8

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

cursor = c.execute(u"SELECT * from HOUSE where TITLE glob '*东城*' or TITLE glob '*西城*'")  # or '*西城*'")
for row in cursor:
    print row

conn.commit()
conn.close()