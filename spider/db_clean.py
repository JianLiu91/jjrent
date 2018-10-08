# -*- coding: utf8

import sqlite3

if __name__ == '__main__':

    conn = sqlite3.connect('../db/test.db')
    c = conn.cursor()
    # sqltext = '''
    #     SELECT * from HOUSE where CRAWL_TIME < (datetime('now','-10 day')) ORDER BY CRAWL_TIME DESC
    # '''
    sqltext = '''
        DELETE from HOUSE where CRAWL_TIME < (datetime('now','-10 day'))
    '''

    cursor = c.execute(sqltext)
    for elem in cursor:
        print elem[-1]

    conn.commit()
    conn.close()