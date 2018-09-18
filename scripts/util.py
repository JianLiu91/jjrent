# -*- coding: utf8

def area():
    result ={}
    for line in open('resources/area.txt'):
        key, value = line.strip().split(':')
        value = value.split(' ')
        result[key] = value
    return result

def subway():
    result ={}
    for line in open('resources/subway.txt'):
        key, value = line.strip().split(':')
        key, value = key.strip(), value.strip()
        value = value.split(' ')
        result[key] = value
    return result 


def xiaoqu():
    result = {}
    for line in open('resources/xiaoqu_all.txt'):
        fields = line.strip().split('\t')
        large, small, opt = fields[0], fields[1], fields[2]
        result.setdefault(large, set())
        result.setdefault(small, set())

        result[large].add(small)
        result[large].add(opt)
        result[small].add(opt)
    return result


def xiaoquzuobiao():
    result = []
    for line in open('resources/xiaoqu_zuobiao.txt'):
        fields = line.strip().split('\t')
        add, lat, lon = fields[0], fields[1], fields[2]
        result.append((add, lat, lon))
    return result