import random
res = []
t = set()

for line in open('xiaoqu_zuobiao.txt'):
    name, lat, lon = line.strip().split('\t')
    temp = (lat, lon)
    if not temp in t:
        t.add(temp)
    else:
        a, b = str(float(lat) + random.uniform(0.1, 0.4)), str(float(lon) + random.uniform(0.1, 0.4))
        temp = (a, b)
    print '\t'.join([name, temp[0] ,temp[1]])
