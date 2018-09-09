# -*- coding: utf8

def area():
    result ={}
    for line in open('scripts/area.txt'):
        key, value = line.strip().split(':')
        value = value.split(' ')
        result[key] = value
    return result

def subway():
    result ={}
    for line in open('scripts/subway.txt'):
        key, value = line.strip().split(':')
        key, value = key.strip(), value.strip()
        value = value.split(' ')
        result[key] = value
    return result 