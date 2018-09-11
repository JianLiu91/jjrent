# -*- coding: utf8
from bs4 import BeautifulSoup
import requests
import datetime
import time

import sqlite3

def transfer_post_time(post_time):
    fields = post_time.split('-')
    if len(fields[1]) == 1:
        fields[1] = '0' + fields[1]
    return '-'.join(fields)

def crawl(url):
    pre_fix = 'http://www.newsmth.net/nForum/#!'
    temp = datetime.datetime.now()
    year, month, day = str(temp.year), str(temp.month), str(temp.day)

    try:
        soup = BeautifulSoup(requests.get(url).text)
    except:
        return
    uls = soup.find('ul', class_='list sec').findAll('li')
    for ul in uls:
        divp, diva = ul.findAll('div')
        if not divp.find('a', class_='top'):
            div_url = pre_fix + divp.find('a').get('href')[1:]
            div_txt = divp.find('a').text

            a = diva.find('a')
            user = a.text
            post_time = a.next_sibling[1:]
            post_time = post_time + ' 23:59:00' if post_time[2] != ':' else '-'.join([year, month, day]) + ' %s' % post_time
            post_time = transfer_post_time(post_time)

            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if (div_txt.startswith('Re') 
                or div_txt.startswith(u'版面积分变更记录') 
                or div_txt.find('HouseRent') != -1
                or len(div_txt) < 4
                ):
                continue

            conn = sqlite3.connect('../db/test.db')
            c = conn.cursor()
            try:
                sqltext = '''
                    INSERT OR IGNORE INTO HOUSE (SOURCE,URL,TITLE,USER,POST_TIME,CRAWL_TIME)
                    VALUES ('newsmth', '%s', '%s', '%s', '%s', '%s');
                    UPDATE HOUSE SET POST_TIME='%s' WHERE TITLE='%s';
                    ''' % (div_url, div_txt, user, post_time, nowTime, post_time, div_txt)
                c.executescript(sqltext)
                conn.commit()
            except:
                pass

            conn.close()


if __name__ == '__main__':
    for i in range(30):
        url = 'http://m.newsmth.net/board/HouseRent?p=%d' % (i)
        print url
        crawl(url)
        time.sleep(4)