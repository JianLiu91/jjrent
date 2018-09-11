import requests
import sqlite3
import datetime
import time
import logging

from bs4 import BeautifulSoup
from time import gmtime, strftime

logging.basicConfig(filename='z_douban.log', format='%(asctime)s - %(message)s', level=logging.WARNING)

headers = {
    'content-type': 'application/json',
    'cookie': 'bid=E6H68TbdrsQ; ps=y; ap_v=0,6.0; __yadk_uid=Ddm2MGllmSBhAEAT66BMTv4bAiRgHvFP; douban-fav-remind=1; ll="108288"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1536630183%2C%22https%3A%2F%2Faccounts.douban.com%2Fsafety%2Funlock_sms%2Fresetpassword%3Fconfirmation%3Dc5ffaf65486e8d57%26alias%3D%22%5D; ue="ryanliu1991@gmail.com"; dbcl2="67739701:5auzbbYbvfY"; ck=3Dca; __utmt=1; _pk_id.100001.8cb4=16592f55b1f77443.1536626353.2.1536630213.1536626971.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utma=30149280.740421685.1536626354.1536626354.1536630207.2; __utmb=30149280.21.0.1536630213038; __utmc=30149280; __utmz=30149280.1536626354.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=30149280.6773',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }


def crawl(url):
    year = strftime("%Y", gmtime())
    try:
        a = requests.get(url, headers=headers)
    except:
        return
    soup = BeautifulSoup(a.text)

    table = soup.find('table', {"class": "olt"})
    if not table:
        logging.warning('ERROR')
        return
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


if __name__ == '__main__':

    douban_add = [
        'https://www.douban.com/group/26926/discussion?start=',
        'https://www.douban.com/group/beijingzufang/discussion?start=',
        'https://www.douban.com/group/279962/discussion?start=',
        'https://www.douban.com/group/zhufang/discussion?start=',
        'https://www.douban.com/group/sweethome/discussion?start=',
        'https://www.douban.com/group/opking/discussion?start=',
        'https://www.douban.com/group/257523/discussion?start='
    ]

    for address in douban_add:
        for i in range(0, 500, 25):
            url = '%s%d' % (address, i)
            logging.warning(url)
            crawl(url)
            time.sleep(20)