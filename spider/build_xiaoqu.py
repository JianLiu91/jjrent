# -*- coding:utf8
import sqlite3

def xiaoquzuobiao():
    result = []
    for line in open('../resources/xiaoqu_zuobiao.txt'):
        fields = line.strip().split('\t')
        add, lat, lon = fields[0], fields[1], fields[2]
        result.append((add, lat, lon))
    return result

if __name__ == '__main__':

    conn = sqlite3.connect('../db/test.db')
    c = conn.cursor()
    xiaoquzuobiao = xiaoquzuobiao()
    result = []
    for xqzb in xiaoquzuobiao:
        xqzb = list(xqzb)
        c.execute("SELECT Count(*) FROM HOUSE WHERE TITLE GLOB '*%s*'" % xqzb[0])   
        rows = c.fetchall()[0][0]
        if rows != 0:
            result.append(tuple(list(xqzb)+[rows]))

    c.execute('DELETE FROM XIAOQUGPS')
    conn.commit()

    for elem in result:
        c.execute("insert OR IGNORE into XIAOQUGPS values ('%s', '%s', '%s', '%d')" % elem)

    conn.commit()
    conn.close()