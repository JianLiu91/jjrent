# -*- coding: utf8

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

sqlscript = "SELECT * from  ( SELECT *, 0 from HOUSE where 1=1   and (  TITLE GLOB '*万龙社区*'  )  and SOURCE="douban"  AND USER NOT IN (SELECT USER from HOUSE GROUP BY USER HAVING count(TITLE) >= 4) UNION ALL SELECT *, 1 from HOUSE where 1=1   and (  TITLE GLOB '*万龙社区*'  )  and SOURCE="douban"  AND USER IN (SELECT USER from HOUSE GROUP BY USER HAVING count(TITLE) >= 4) )  ORDER BY POST_TIME DESC"
cursor = c.execute(sqlscript).fetchall()

print cursor

conn.commit()
conn.close()