# -*- coding: utf8

import sqlite3
from scripts.util import area, subway, xiaoqu

area = area()
subway = subway()
xiaoqu = xiaoqu()

conn = sqlite3.connect('db/test.db')
print "Opened database successfully";
c = conn.cursor()

sqlscript = 'SELECT * from HOUSE where 1=1 '

m_area = u'东城'.encode('utf8')


temp = ' and ( '
#all_area = ["TITLE GLOB '*%s*'" % t for t in area[m_area]]
all_area = []
print ' '.join(["TITLE GLOB '*%s*'" % t for t in xiaoqu[m_area]][650:660])


cursor = c.execute(sqlscript)  # or '*西城*'")
for row in cursor:
    print row[2]

conn.commit()
conn.close()