# -*- coding: utf8

import sqlite3

conn = sqlite3.connect('test.db')
print "Opened database successfully";
c = conn.cursor()

c.execute('''
    INSERT INTO HOUSE (SOURCE,URL,TITLE,USER,POST_TIME,CRAWL_TIME)
      VALUES ('newsmth', 'http://www.newsmth.net/nForum/#!article/HouseRent/524599', 
      ' 【个人求租】个人寻租，华严北里', ' wanghg127', '2018-08-26', '2018-09-09 20:28:19' )''');

conn.commit()
conn.close()