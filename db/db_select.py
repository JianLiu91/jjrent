# -*- coding: utf8

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

sqlscript = "SELECT * FROM HOUSE ORDER BY POST_TIME DESC ;"
cursor = c.execute(sqlscript).fetchall()

print cursor

conn.commit()
conn.close()