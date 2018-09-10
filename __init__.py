# -*- coding: utf8 -*-

from flask import Flask
from flask import render_template, jsonify, request

from random import choice
from scripts.util import area, subway, xiaoqu

import sqlite3

area = area()
subway = subway()
xiaoqu = xiaoqu()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/get_sub_options', methods=['GET'])
def get_sub_options():
    info = request.values
    type_p = info.get('type')
    value = info.get('value').encode('utf8')
    print type_p
    value = area[value] if type_p == 'area' else subway[value]
    return jsonify({'data': value})


@app.route('/jsondata', methods=['GET'])
def jsondata():
    info = request.values
    limit = info.get('limit', 10)
    offset = info.get('offset', 0)

    method = info.get('method')
    m_area = info.get('area')
    m_subway = info.get('subway')
    suboption = info.get('suboption')
    zffs = info.get('zffs')

    print method, m_area, m_subway, suboption, zffs

    sqlscript = 'SELECT * from HOUSE where 1=1 '

    if not (suboption == u'不限' or len(suboption.strip()) == 0):
        sqlscript += " and TITLE GLOB '*%s*' " % (suboption)
    
    elif m_area != u'不限':
        temp = ' and ( '
        m_area = m_area.encode('utf8')
        all_area = ["TITLE GLOB '*%s*'" % t for t in area[m_area]]
        sql_area = " or ".join(all_area)
        sqlscript += temp + sql_area + ')'
        
    elif m_subway != u'不限':
        pass


    if zffs != u'不限':
        zffs = zffs[0]
        sqlscript = sqlscript + " and TITLE GLOB '*%s*' " % zffs

    print sqlscript

    data = []
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()

    cursor = c.execute(sqlscript)
    for row in cursor:
        d = {}
        d['source'], d['title'], d['user'], d['post_time'] = row[0], {'href':row[1], 'title': row[2]}, row[3], row[4]
        data.append(d)
    conn.close()

    return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})