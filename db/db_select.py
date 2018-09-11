# -*- coding: utf8

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

sqlscript = "SELECT *,0 FROM HOUSE WHERE USER IN (SELECT USER from HOUSE GROUP BY USER HAVING count(TITLE) >= 2)"
cursor = c.execute(sqlscript).fetchall()

print cursor

conn.commit()
conn.close()