# -*- coding: utf8

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

sqlscript = "SELECT * from COMMENTS"
cursor = c.execute(sqlscript).fetchall()

print cursor

conn.commit()
conn.close()