# -*- coding:UTF-8 -*-
import requests
import json
from bs4 import BeautifulSoup


class WeiBo:
    def __init__(self, url):
        self.url = url

    def Host(self, sid=0):
        since = sid
        if since == 0:
            url = self.url
        else:
            url = self.url + "&since_id=" + str(since)
        head = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Referer": "https://m.weibo.cn/",
            "Accept": "application/json, text/plain, */*"
        }
        print(url)
        req = requests.get(url, headers=head)
        req.encoding = "utf-8"
        weibo = []
        data = BeautifulSoup(req.text, "lxml")
        txt = json.loads(data.text)
        i = 0
        for it in txt['data']['cards']:
            i += 1
            user = it['mblog']['user']['screen_name']
            source = it['mblog']['source']
            crtime = it['mblog']['created_at']
            cont = it['mblog']['text']
            pics = it['mblog'].get('pics')
            purl = []
            if pics is not None:
                for p in pics:
                    purl.append(p['url'])
            else:
                purl = ""
            weibo.append({"user": user, "source": source, "crtime": crtime, "cont": cont, "pics": purl})

        return weibo
        # print(weibo)


if __name__ == "__main__":
    WB = WeiBo('https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0')
    WB.Host()
