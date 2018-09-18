# -*- coding: utf8

import json
from urllib import urlopen, quote
import requests

def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'

    ak = '29DpqLeOW2EpyvmjXmTGKarM'
    ak = '6f402df225eac8d88e0066ec2a1a457f'


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

#fileo = open('output.txt', 'w')

with open('xiaoqu_all.txt') as filein:
    for line in filein:
        add = line.strip().split('\t')[2]
        try:
            lat, lng = getlnglat(add)
        except:
            lat = -1; lng = -1
        print '\t'.join([add, str(lat), str(lng)])
        #print>>fileo, '\t'.join([add, str(lat), str(lng)])

#fileo.close()
