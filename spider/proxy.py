import requests
from bs4 import BeautifulSoup


def get_proxies():
    url = 'http://www.xicidaili.com/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        #'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTI5YWNhY2Y3ZjEyZDZkYzIxMWVhZTc2MDlmMTBkNDQwBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTI4VTl1bmV1SjRwMHkvN1ZWb2daWHZWc2xBZ1Mxb0ZjU29QamJSUDFUWDQ9BjsARg%3D%3D--0f8250d96137c02bbed3a36804d9df4b4f29ce66; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1531965758,1531965759,1531965760,1531965761; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1531970576'
        'Cookie': 'UM_distinctid=16229f47045277-08aff75fb19a48-1421150f-15f900-16229f47046170; _uab_collina=152112232176128814908304; PHPSESSID=3evtqd5c0b8bqpkmlovko2jtp3; CNZZDATA1254842228=936967378-1521117983-https%253A%252F%252Fwww.baidu.com%252F%7C1521425837; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1521122309,1521426613; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1521426613; hasShow=1; acw_tc=AQAAAJUS3V10RwEAhukzPcX3jmxXdssR; zg_did=%7B%22did%22%3A%20%2216229f471262d3-055e010d78987e-1421150f-15f900-16229f471271b%22%7D; _umdata=A502B1276E6D5FEF9E6F13E1A9A304A4A90A9ADCE0D105A437EC4E7C410E01B433DB0C8B9C771EFBCD43AD3E795C914C0BE51CE6374F0D69888809C94F45E1F5; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201521426612549%2C%22updated%22%3A%201521426683444%2C%22info%22%3A%201521122308403%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D'
    }

    soup = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")
    table = soup.find('table', id='ip_list')
    trs = table.findAll('tr')

    results = {}

    for tr in trs:
        tds = tr.findAll('td')
        try:
            int(tds[2].text)
            proxy_type = tds[5].text.lower()
            pro = '%s://%s:%s' % (proxy_type, tds[1].text, tds[2].text)
            results.setdefault(proxy_type, [])
            results[proxy_type].append(pro)
        except Exception, e:
            print e
            pass

    return results


if __name__ == '__main__':
    proxies = get_proxies()
    print proxies