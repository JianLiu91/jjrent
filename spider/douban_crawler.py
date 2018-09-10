import requests
import sqlite3
import datetime

from bs4 import BeautifulSoup
from time import gmtime, strftime

# https://www.douban.com/group/26926/discussion?start=0
# https://www.douban.com/group/beijingzufang/discussion?start=50
# https://www.douban.com/group/279962/discussion?start=50
# https://www.douban.com/group/zhufang/discussion?start=50
# https://www.douban.com/group/sweethome/discussion?start=50
# https://www.douban.com/group/opking/discussion?start=50
# https://www.douban.com/group/257523/discussion?start=50


def crawl(url):
    year = strftime("%Y", gmtime())
    a = requests.get(url)
    soup = BeautifulSoup(a.text)

    table = soup.find('table', {"class": "olt"})
    for tr in table.find_all('tr')[1:]:
        title = tr.find('a').get('title')
        url = tr.find('a').get('href')
        user_id = tr.find('td', {'nowrap': 'nowrap'}).text

        tm = tr.find('td', {'class': 'time'}).text
        tm = ('%s-%s:00' % (year, tm)).split(' ')[0]

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('../db/test.db')
        c = conn.cursor()
        sqltext = '''
            INSERT OR IGNORE INTO HOUSE (SOURCE,URL,TITLE,USER,POST_TIME,CRAWL_TIME)
            VALUES ('douban', '%s', '%s', '%s', '%s', '%s');
            UPDATE HOUSE SET CRAWL_TIME='%s' WHERE URL='%s';
            ''' % (url, title, user_id, tm, nowTime, nowTime, url)
        c.executescript(sqltext)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    for i in range(0, 10000, 50):
        print i
        crawl('https://www.douban.com/group/26926/discussion?start=%d' % i)