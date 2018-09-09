# -*- coding: utf8 -*-

from flask import Flask
from flask import render_template, jsonify, request

from random import choice
from scripts.util import area, subway

import sqlite3

area = area()
subway = subway()

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
    limit = info.get('limit', 10)  # 每页显示的条数
    offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点

    method = info.get('method')
    area = info.get('area')
    subway = info.get('subway')
    suboption = info.get('suboption')
    zffs = info.get('zffs')

    data = []
    conn = sqlite3.connect('db/test.db')
    c = conn.cursor()

    cursor = c.execute("SELECT * from HOUSE")
    for row in cursor:
        d = {}
        d['source'], d['title'], d['user'], d['post_time'] = row[0], {'href':row[1], 'title': row[2]}, row[3], row[4]
        data.append(d)
    conn.close()

    return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
    # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
    # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了