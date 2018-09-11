import requests
from bs4 import BeautifulSoup


def get_proxies():
    url = 'http://www.xicidaili.com/wn/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        #'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTI5YWNhY2Y3ZjEyZDZkYzIxMWVhZTc2MDlmMTBkNDQwBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTI4VTl1bmV1SjRwMHkvN1ZWb2daWHZWc2xBZ1Mxb0ZjU29QamJSUDFUWDQ9BjsARg%3D%3D--0f8250d96137c02bbed3a36804d9df4b4f29ce66; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1531965758,1531965759,1531965760,1531965761; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1531970576'
        'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTFhMjgxYTVhNjA3MzUwYTcxNTY3OTgxMzAyYTZjMmJmBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVB4Y2dFT0Mxdmh6aHVBQ2hCdnJzRGdiZnFSaWljQXZ1RmpTNmovNkRuaXM9BjsARg%3D%3D--f169dd9846fbcaa1b59468955f709b497448e1d0; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1536672762,1536674701; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1536676772'
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