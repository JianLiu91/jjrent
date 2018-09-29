# -*- coding: utf8 -*-

import logging
import sqlite3
import datetime

from random import choice

from flask import Flask
from flask import render_template, jsonify, request
from flask_pymongo import PyMongo

from models import get_db, setup_logger
from models import write_ip_time, read_ip_count
from models import get_sub_option_values
from models import process_sqlite
from models import process_mongo

log = setup_logger()

app = Flask(__name__)
mongo = get_db()

@app.route("/")
def index():
    ip = request.remote_addr
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log.warning('[%s] %s', str(ip), 'is logging...')
    write_ip_time(ip, nowTime)

    sta = read_ip_count()
    return render_template('index.html', sta=sta)


@app.route("/about")
def about():
    sta = read_ip_count()
    return render_template('about.html', sta=sta)


@app.route('/get_sub_options', methods=['GET'])
def get_sub_options():
    info = request.values
    type_p = info.get('type')
    value = info.get('value').encode('utf8')
    value = get_sub_option_values(value, type_p)
    return jsonify({'data': value})


@app.route('/jsondata', methods=['GET'])
def jsondata():
    ip = request.remote_addr
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

    log.warning('[%s] %s ["%s" %s %s %s %s %s %s %s %s]', str(ip), 'is searching...', search, method, m_area, m_subway, suboption, zffs, jushi, filr, tag)

    result = process_sqlite(limit, offset, method, m_area, m_subway, suboption, zffs, jushi, filr, tag, search)
    #result = process_mongo(mongo, limit, offset, method, m_area, m_subway, suboption, zffs, jushi, filr, tag, search)

    return jsonify(result)


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

    return jsonify({'success': True})


@app.route("/xiaoquzuobiao")
def xiaoquzb():
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()
    sqlscript = "SELECT * from  XIAOQUGPS"
    result = c.execute(sqlscript).fetchall()
    conn.close()
    return jsonify({'data': result})


if __name__ == '__main__':
    app.run(host="0.0.0.0")