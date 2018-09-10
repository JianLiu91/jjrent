# -*- coding: utf8

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

sqlscript = 'SELECT * from HOUSE where 1=1 and SOURCE="douban"'

# m_area = u'东城'


# all_area = ["TITLE GLOB '*%s*'" % t for t in area[m_area]]
# all_area = all_area + ["TITLE GLOB '*%s*'" % t for t in xiaoqu[m_area]][:900]
# sql_area = " or ".join(all_area)
# sqlscript += temp + sql_area + ')'

cursor = c.execute(sqlscript)  # or '*西城*'")
for row in cursor:
    print row

conn.commit()
conn.close()