# -*- coding: utf8

from bs4 import BeautifulSoup
import requests
import datetime
import time

import sqlite3

def crawl(url):
    pre_fix = 'http://www.newsmth.net/nForum/#!'
    temp = datetime.datetime.now()
    year, month, day = str(temp.year), str(temp.month), str(temp.day)

    soup = BeautifulSoup(requests.get(url).text)
    uls = soup.find('ul', class_='list sec').findAll('li')
    for ul in uls:
        divp, diva = ul.findAll('div')
        if not divp.find('a', class_='top'):
            div_url = pre_fix + divp.find('a').get('href')[1:]
            div_txt = divp.find('a').text

            a = diva.find('a')
            user = a.text
            post_time = a.previous_sibling
            post_time = post_time if post_time[2] != ':' else '-'.join([year, month, day])
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if div_txt.startswith('Re') or div_txt.startswith(u'版面积分变更记录') or div_txt.find('HouseRent') != -1:
                continue

            # print div_txt, user, post_time
            conn = sqlite3.connect('../db/test.db')
            c = conn.cursor()
            try:
                sqltext = '''
                    INSERT OR IGNORE INTO HOUSE (SOURCE,URL,TITLE,USER,POST_TIME,CRAWL_TIME)
                    VALUES ('newsmth', '%s', '%s', '%s', '%s', '%s');
                    UPDATE HOUSE SET CRAWL_TIME='%s' WHERE URL='%s';
                    ''' % (div_url, div_txt, user, post_time, nowTime, nowTime, div_url)
                c.executescript(sqltext)
                conn.commit()
            except:
                pass

            conn.close()


if __name__ == '__main__':
    for i in range(60):
        print i
        crawl('http://m.newsmth.net/board/HouseRent?p=%d' % (i))
        time.sleep(4)