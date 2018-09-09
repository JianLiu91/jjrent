from bs4 import BeautifulSoup
import requests
import time

base_url = "https://bj.lianjia.com"
text = requests.get('https://bj.lianjia.com/ditiezufang/').text
soup = BeautifulSoup(text)

res = soup.find('div', class_='option-list').find_all('a')[1:]
for r in res:
    print r.text, ':',
    url = base_url + r.get('href')
    text = requests.get(url).text
    soup = BeautifulSoup(text)
    items = soup.find('div', class_='sub-option-list').find_all('a')[1:]
    for item in items:
        print item.text,
    print

    time.sleep(2)
