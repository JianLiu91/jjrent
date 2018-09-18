# -*- coding: utf8

import json
from urllib import urlopen, quote
import requests

def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'

    ak = '29DpqLeOW2EpyvmjXmTGKarM'
    #ak = '6f402df225eac8d88e0066ec2a1a457f'


    #add = quote(address)
    add = address
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak 
    req = urlopen(uri)
    res = req.read().decode('utf-8') 
    temp = json.loads(res)
    lat=temp['result']['location']['lat']
    lng=temp['result']['location']['lng']
    precise = temp['result']['precise']
    confidence = temp['result']['confidence']
    return lat, lng

def area():
    result ={}
    for line in open('area.txt'):
        key, value = line.strip().split(':')
        value = value.split(' ')
        result[key] = value
    return result

def subway():
    result ={}
    for line in open('subway.txt'):
        key, value = line.strip().split(':')
        key, value = key.strip(), value.strip()
        value = value.split(' ')
        result[key] = value
    return result 

def xiaoqu():
    result = []
    for line in open('xiaoqu_all.txt'):
        fields = line.strip().split('\t')
        large, small, opt = fields[0], fields[1], fields[2]
        result.append([large, opt])
    return result


if __name__ == '__main__':
    # # for area
    # area = area()
    # for key in area:
    #     if key != '不限':
    #         for elem in area[key]:
    #             add = '北京市'+key+'区'+elem
    #             try:
    #                 lat, lng = getlnglat(add)
    #             except:
    #                 lat = -1; lng = -1
    #             print '\t'.join([elem, str(lat), str(lng)])

    # for subway
    # subway = subway()
    # for key in subway:
    #     if key != '不限':
    #         for elem in subway[key]:
    #             add = '北京市'+key+elem+'地铁站'
    #             try:
    #                 lat, lng = getlnglat(add)
    #             except:
    #                 lat = -1; lng = -1
    #             print '\t'.join([elem, str(lat), str(lng)])


    # for beijing xiaoqu
    # xiaoqu = xiaoqu()
    # for xq in xiaoqu:
    #     a, b = xq
    #     add = '北京市'+a+'区'+b
    #     try:
    #         lat, lng = getlnglat(add)
    #     except:
    #         lat = -1; lng = -1
    #     print '\t'.join([b, str(lat), str(lng)])

    # for xianghe yanjiao xiaoqu
    xiaoqu = xiaoqu()[7977:]
    for xq in xiaoqu:
        a, b = xq
        add = a + b
        try:
            lat, lng = getlnglat(add)
        except:
            lat = -1; lng = -1
        print '\t'.join([b, str(lat), str(lng)])




#fileo.close()
