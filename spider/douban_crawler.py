import requests
import sqlite3
import datetime
import time
import logging

from bs4 import BeautifulSoup
from time import gmtime, strftime
from proxy import get_proxies3 as get_proxies

logging.basicConfig(filename='z_douban.log', format='%(asctime)s - %(message)s', level=logging.WARNING)

headers = {
    'content-type': 'application/json',
    'cookie': '',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }


def crawl(url, proxies):
    year = strftime("%Y", gmtime())
    try:
        a = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    except:
        return False
    soup = BeautifulSoup(a.text)

    table = soup.find('table', {"class": "olt"})
    if not table:
        logging.warning('ERROR')
        return False

    for tr in table.find_all('tr')[1:]:
        title = tr.find('a').get('title')
        url = tr.find('a').get('href')
        user_id = tr.find('td', {'nowrap': 'nowrap'}).text

        tm = tr.find('td', {'class': 'time'}).text
        tm = ('%s-%s:00' % (year, tm))

        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('../db/test.db')
        c = conn.cursor()
        try:
            sqltext = '''
                INSERT OR IGNORE INTO HOUSE (SOURCE,URL,TITLE,USER,POST_TIME,CRAWL_TIME)
                VALUES ('douban', '%s', '%s', '%s', '%s', '%s');
                UPDATE HOUSE SET POST_TIME='%s' WHERE TITLE='%s';
                ''' % (url, title, user_id, tm, nowTime, tm, title)
            c.executescript(sqltext)
        except:
            pass
        conn.commit()
        conn.close()
    return True


if __name__ == '__main__':

    douban_add = [
        'https://www.douban.com/group/beijingzufang/discussion?start=',
        'https://www.douban.com/group/26926/discussion?start=',
        'https://www.douban.com/group/279962/discussion?start=',
        'https://www.douban.com/group/zhufang/discussion?start=',
        'https://www.douban.com/group/sweethome/discussion?start=',
        'https://www.douban.com/group/opking/discussion?start=',
        'https://www.douban.com/group/257523/discussion?start='
    ]

    proxy_list = [None] + get_proxies()['https']
    #proxy_list = get_proxies()['https']
    logging.warning('Get %s proxies', str(len(proxy_list)-1))

    for address in douban_add:
        for i in range(0, 500, 25):
            url = '%s%d' % (address, i)
            logging.warning(url)
            for proxy in proxy_list:
                logging.warning('Proxy:%s', proxy)
                requests_proxies = {
                    'https': proxy
                }
                if crawl(url, requests_proxies):
                    logging.warning('OK')
                    break
            else:
                proxy_list = [None] + get_proxies()['https']
                logging.warning('Get %s proxies', str(len(proxy_list)-1))
            time.sleep(20)