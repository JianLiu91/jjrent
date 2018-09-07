# -*- coding: utf8 -*-

from flask import Flask
from flask import render_template, jsonify, request

from random import choice

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/jsondata', methods=['POST', 'GET'])
def infos():
    data = []
    names = ['香', '草', '瓜', '果', '桃', '梨', '莓', '橘', '蕉', '苹']
    for i in range(1, 1001):
        d = {}
        d['id'] = i
        d['name'] = choice(names) + choice(names)  # 随机选取汉字并拼接
        d['price'] = '10'
        data.append(d)
    if request.method == 'POST':
        print('post')
    if request.method == 'GET':
        info = request.values
        limit = info.get('limit', 10)  # 每页显示的条数
        offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
        print('get', limit)
        print('get  offset', offset)

        return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
        # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
        # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了