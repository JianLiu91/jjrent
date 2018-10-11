# -*- coding: utf8

import logging
import sqlite3
import pymongo
from pymongo import MongoClient

from scripts.util import area, subway, xiaoqu

def get_db():
    client = MongoClient('mongodb://ryan:8325357@localhost:27017/house')
    return client.house

def setup_logger():
    logFile = 'web.log'
    log_formatter = logging.Formatter("%(message)s - %(asctime)s")

    file_handler = logging.FileHandler(logFile)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.WARNING)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    stream_handler.setLevel(logging.WARNING)

    log = logging.getLogger('')
    log.setLevel(logging.WARNING)
    log.addHandler(file_handler)
    log.addHandler(stream_handler)
    return log


def db_open():
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()
    return conn, c


def write_ip_time(ip, nowTime):
    conn, c = db_open()
    sqltext = '''
        INSERT INTO VISIT (IP,VISIT_TIME)
        VALUES ('%s', '%s');
        ''' % (ip, nowTime)
    c.executescript(sqltext)
    conn.commit()
    conn.close()


def read_ip_count():

    def _query(c, sqlscript):
        cursor = c.execute(sqlscript)
        return cursor.fetchall()[0][0]

    conn, c = db_open()
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
    return sta


def get_sub_option_values(value, type_p):
    value = area[value] if type_p == 'area' else subway[value]
    return value

    

def process_sqlite(limit, offset, method, m_area, m_subway,
    suboption, zffs, jushi, filr, tag, search):
    
    sqlscript = ' '

    if len(search) != 0:
        sqlscript += " and ( "
        search = search.encode('utf8')
        all_sub = [" TITLE GLOB '*%s*' " % (search)]
        try:
            sub_xiaoqu = [" TITLE GLOB '*%s*' " % t for t in xiaoqu[search]]
            all_sub += sub_xiaoqu
        except Exception, e:
            pass

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

        all_area = ["TITLE GLOB '*%s*'" % t for t in [m_area] + area[m_area]]
        all_area = all_area + ["TITLE GLOB '*%s*'" % t for t in xiaoqu[m_area]][:10]
        sql_area = " or ".join(all_area)
        sqlscript += temp + sql_area + ')'
        
    elif m_subway != u'不限':
        temp = ' and ( '
        m_subway = m_subway.encode('utf8')
        all_subway = ["TITLE GLOB '*%s*'" % t for t in [m_subway] + subway[m_subway]]
        for elem in subway[m_subway]:
            try:
                all_subway += ["TITLE GLOB '*%s*'" % t for t in xiaoqu[elem]][:5]
            except Exception, e:
                pass
        print len(all_subway)
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

    sqlscript = 'SELECT * from %s %s' % (all_user, 'ORDER BY date(POST_TIME) DESC, SOURCE DESC, POST_TIME DESC')

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
    return {'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]}


def process_mongo(mongo, limit, offset, method, m_area, m_subway,
    suboption, zffs, jushi, filr, tag, search):
    
    match_patterns = []

    if len(search) != 0:
        search = search.encode('utf8')
        match_patterns.append(search)
        try:
            match_patterns += [t for t in xiaoqu[search]]
        except:
            pass

    elif not (suboption == u'不限' or len(suboption.strip()) == 0):
        suboption = suboption.encode('utf8')
        match_patterns.append(suboption)
        try:
            match_patterns += [t for t in xiaoqu[suboption]]
        except:
            pass
    
    elif m_area != u'不限':
        m_area = m_area.encode('utf8')
        match_patterns.append(m_area)
        match_patterns += [t for t in area[m_area]]
        match_patterns += [t for t in xiaoqu[m_area]]
        
    elif m_subway != u'不限':
        m_subway = m_subway.encode('utf8')
        match_patterns.append(m_subway)
        match_patterns += [t for t in subway[m_subway]]
        for elem in subway[m_subway]:
            try:
                match_patterns += [t for t in xiaoqu[elem]]
            except Exception, e:
                pass

    reg = '.*' + '|'.join(match_patterns) + '.*'

    condition_list = []
    condition_list.append({'title': {'$regex': reg}})

    if zffs != u'不限':
        zffs = zffs[0].encode('utf8')
        reg = '.*' + zffs + '.*'
        condition_list.append({'title': {'$regex': reg}})

    if jushi != u'不限':
        n = jushi[0]
        if n == '1':
            temp = ['1', '一']
        elif n == '2':
            temp = ['2', '二', '两']
        else:
            temp = ['3', '三']
        temp = ["%s居" % x for x in temp]
        reg = '.*' + '|'.join(temp) + '.*'
        condition_list.append({'title': {'$regex': reg}})

    if filr == u'开启':
        t = ' AND USER NOT IN (SELECT USER from HOUSE GROUP BY USER HAVING count(TITLE) >= 3) '
        sqlscript = sqlscript + t

    if tag != u'不限':
        t = 'newsmth' if tag==u'水木' else 'douban'
        condition_list.append({'source': t})


    # normal_user = 'SELECT *, 0 from HOUSE where 1=1 ' + sqlscript + ' AND USER NOT IN (SELECT USER from HOUSE GROUP BY USER HAVING count(TITLE) >= 4)'
    # cheat_user  = 'SELECT *, 1 from HOUSE where 1=1 ' + sqlscript + ' AND USER IN (SELECT USER from HOUSE GROUP BY USER HAVING count(TITLE) >= 4)'

    # all_user = ' ( %s UNION ALL %s ) ' %  (normal_user, cheat_user)

    # sqlscript = 'SELECT * from %s %s' % (all_user, 'ORDER BY POST_TIME DESC')

    # data = []
    # conn = sqlite3.connect('db/test.db')
    # c = conn.cursor()

    # cursor = c.execute(sqlscript).fetchall()
    # for row in cursor:
    #     d = {}
    #     d['source'], d['title'], d['user'], d['post_time'] = (
    #         row[0], 
    #         {'href':row[1], 'title': row[2][:40], 'flag': row[6]}, 
    #         {'u':row[3], 'flag': row[6]}, 
    #         row[4].split()[0])
    #     data.append(d)
    
    # conn.close()

    data = []
    for elem in mongo.rent.find({"$and": condition_list}):
        d = {}
        d['source'], d['title'], d['user'], d['post_time'] = (
            elem['source'],
            {'href':elem['url'], 'title': elem['title'][:40], 'flag': 0},
            {'u':elem['user'], 'flag': 0},
            elem['post_time'].strftime('%Y-%m-%d')
            )
        data.append(d)


    return {'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]}