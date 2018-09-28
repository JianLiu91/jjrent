# -*- coding: utf8 -*-

import logging
import sqlite3
import datetime
from multiprocessing import Pool

from flask import Flask
from flask import render_template, jsonify, request

from random import choice
from scripts.util import area, subway, xiaoqu, xiaoquzuobiao


logFile = 'web.log'

log_formatter = logging.Formatter("%(message)s - %(asctime)s")

file_handler = logging.FileHandler(logFile)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.WARNING)

#Setup Stream Handler (i.e. console)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.WARNING)

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)

#Add both Handlers
log.addHandler(file_handler)
log.addHandler(stream_handler)

area = area()
subway = subway()
xiaoqu = xiaoqu()
xiaoquzuobiao = xiaoquzuobiao()

app = Flask(__name__)


@app.route("/")
def index():
    ip = request.remote_addr
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log.warning('[%s] %s', str(ip), 'is logging...')

    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()

    sqltext = '''
        INSERT INTO VISIT (IP,VISIT_TIME)
        VALUES ('%s', '%s');
        ''' % (ip, nowTime)

    c.executescript(sqltext)
    conn.commit()

    def _query(c, sqlscript):
        cursor = c.execute(sqlscript)
        return cursor.fetchall()[0][0]

    tpv = _query(c, 'SELECT count(*) FROM VISIT;')
    tip = _query(c, 'SELECT count(distinct IP) FROM VISIT;')

    dpv = _query(c, "SELECT count(*) FROM VISIT where DATE(VISIT_TIME) = DATE('now', '-0 day', 'localtime');")
    dip = _query(c, "SELECT count(distinct IP) FROM VISIT where DATE(VISIT_TIME) = DATE('now', '-0 day', 'localtime');")

    sta = {
        'tpv': tpv,
        'tip': tip,
        'dpv': dpv,
        'dip': dip
    }

    conn.close()

    return render_template('index.html', sta=sta)


# about
@app.route("/about")
def about():
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()

    def _query(c, sqlscript):
        cursor = c.execute(sqlscript)
        return cursor.fetchall()[0][0]

    tpv = _query(c, 'SELECT count(*) FROM VISIT;')
    tip = _query(c, 'SELECT count(distinct IP) FROM VISIT;')

    dpv = _query(c, "SELECT count(*) FROM VISIT where DATE(VISIT_TIME) = DATE('now', '-0 day', 'localtime');")
    dip = _query(c, "SELECT count(distinct IP) FROM VISIT where DATE(VISIT_TIME) = DATE('now', '-0 day', 'localtime');")

    sta = {
        'tpv': tpv,
        'tip': tip,
        'dpv': dpv,
        'dip': dip
    }

    conn.close()

    return render_template('about.html', sta=sta)


@app.route('/get_sub_options', methods=['GET'])
def get_sub_options():
    info = request.values
    type_p = info.get('type')
    value = info.get('value').encode('utf8')
    value = area[value] if type_p == 'area' else subway[value]
    return jsonify({'data': value})


@app.route('/jsondata', methods=['GET'])
def jsondata():
    info = request.values
    limit = info.get('limit',  10)
    offset = info.get('offset', 0)

    method = info.get('method')
    m_area = info.get('area')
    m_subway = info.get('subway')
    suboption = info.get('suboption')
    zffs = info.get('zffs')
    jushi = info.get('jushi')
    filr = info.get('filter')
    tag = info.get('tag')

    search = info.get('search', '')

    ip = request.remote_addr
    log.warning('[%s] %s ["%s" %s %s %s %s %s %s %s %s]', str(ip), 'is searching...', search, method, m_area, m_subway, suboption, zffs, jushi, filr, tag)

    sqlscript = ' '

    if len(search) != 0:
        sqlscript += " and ( "
        search = search.encode('utf8')
        all_sub = [" TITLE GLOB '*%s*' " % (search)]
        try:
            sub_xiaoqu = [" TITLE GLOB '*%s*' " % t for t in xiaoqu[search]]
            all_sub += sub_xiaoqu
        except Exception, e:
            log.warning(e)

        sqlscript += " or ".join(all_sub) + ' ) '

    elif not (suboption == u'不限' or len(suboption.strip()) == 0):
        suboption = suboption.encode('utf8')
        sqlscript += " and ( "
        all_sub = [" TITLE GLOB '*%s*' " % (suboption)]
        try:
            sub_xiaoqu = [" TITLE GLOB '*%s*'" % t for t in xiaoqu[suboption]]
            all_sub += sub_xiaoqu
        except Exception, e:
            print '2', e
        sqlscript += " or ".join(all_sub) + ' ) '
    
    elif m_area != u'不限':
        temp = ' and ( '
        m_area = m_area.encode('utf8')

        all_area = ["TITLE GLOB '*%s*'" % t for t in area[m_area]]
        all_area = all_area + ["TITLE GLOB '*%s*'" % t for t in xiaoqu[m_area]][:100]
        sql_area = " or ".join(all_area)
        sqlscript += temp + sql_area + ')'
        
    elif m_subway != u'不限':
        temp = ' and ( '
        m_subway = m_subway.encode('utf8')
        all_subway = ["TITLE GLOB '*%s*'" % t for t in subway[m_subway]]
        for elem in subway[m_subway]:
            try:
                all_subway += ["TITLE GLOB '*%s*'" % t for t in xiaoqu[elem]][:100]
            except Exception, e:
                pass
        sql_area = " or ".join(all_subway)
        sqlscript += temp + sql_area + ')'


    if zffs != u'不限':
        zffs = zffs[0]
        sqlscript = sqlscript + " and TITLE GLOB '*%s*' " % zffs.encode('utf8')

    if jushi != u'不限':
        n = jushi[0]
        if n == '1':
            temp = ['1', '一']
        elif n == '2':
            temp = ['2', '二', '两']
        else:
            temp = ['3', '三']

        temp = [" TITLE GLOB '*%s居*' " % x for x in temp]
        t = " and ( " + ' OR '.join(temp) + ' ) '

        sqlscript = sqlscript + t

    if filr == u'开启':
        t = ' AND USER NOT IN (SELECT USER from HOUSE GROUP BY USER HAVING count(TITLE) >= 4) '
        sqlscript = sqlscript + t

    if tag != u'不限':

        t = ' and SOURCE="%s" ' % ('newsmth' if tag==u'水木' else 'douban')
        sqlscript = sqlscript + t


    normal_user = 'SELECT *, 0 from HOUSE where 1=1 ' + sqlscript + ' AND USER NOT IN (SELECT USER from HOUSE GROUP BY USER HAVING count(TITLE) >= 4)'
    cheat_user  = 'SELECT *, 1 from HOUSE where 1=1 ' + sqlscript + ' AND USER IN (SELECT USER from HOUSE GROUP BY USER HAVING count(TITLE) >= 4)'

    all_user = ' ( %s UNION ALL %s ) ' %  (normal_user, cheat_user)

    sqlscript = 'SELECT * from %s %s' % (all_user, 'ORDER BY POST_TIME DESC')

    data = []
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()

    cursor = c.execute(sqlscript).fetchall()
    for row in cursor:
        d = {}
        d['source'], d['title'], d['user'], d['post_time'] = (
            row[0], 
            {'href':row[1], 'title': row[2][:40], 'flag': row[6]}, 
            {'u':row[3], 'flag': row[6]}, 
            row[4].split()[0])
        data.append(d)
    
    conn.close()
    return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})



@app.route("/comment")
def comment():
    ip = str(request.remote_addr)
    info = request.values

    comment = 'c' + info.get('comment', '')

    sqltext = '''
        INSERT INTO COMMENTS (IP,COMMENT)
        VALUES (?, ?);
        '''

    log.warning('[%s] says "%s"', ip, comment)

    if len(comment) > 5:
        conn = sqlite3.connect('db/test.db')
        c = conn.cursor()
        c.execute(sqltext, (ip, comment))
        conn.commit()
        conn.close()

    return jsonify({'sucess': True})


@app.route("/xiaoquzuobiao")
def xiaoquzb():
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()
    sqlscript = "SELECT * from  XIAOQUGPS"
    result = c.execute(sqlscript).fetchall()
    return jsonify({'data': result})


if __name__ == '__main__':
    app.run(host="0.0.0.0")