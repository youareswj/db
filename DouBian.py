# -*- coding:UTF-8 -*-
import requests
import json
import re
from bs4 import BeautifulSoup


class DouBan:
    def __init__(self, url="",page=1):
        self.url = url
        if page==1:
            self.page = 1
        else:
            self.page = page

    #获取请求地址
    def getUrl(self):
        p = self.page
        if p == 1:
            u = self.url
        else:
            p = self.page
            u = self.url + "?start=" + str((int(p)-1) * 20)
        return u

    # 获取最新影评
    def latest(self):
        i = 0
        las_url = self.getUrl()
        print("---获取影评---",las_url)
        db_list = []
        req = requests.get(las_url)
        data = BeautifulSoup(req.text, "lxml")
        las_list = data.find('div', class_='review-list chart')
        item = las_list.contents
        # print(item[1].get('data-cid'))
        # for i,it in enumerate(item):
        for it in item:
            if it.string == None:
                name = it.find('a', class_="name")
                if name:
                    i += 1
                    print("---第",i,"条---")
                    id = it.get('data-cid')  # 影评id
                    img = it.find('a', class_='subject-img')  # 电影封面
                    href = img.contents
                    src = href[1].get('src')
                    title = it.find('h2')  # 影评标题
                    url = title.contents[0].get('href')  # 影评链接
                    abstract = it.find('div', class_='short-content')  # 影评简介
                    txt = abstract.get_text()
                    txt = txt.replace('这篇影评可能有剧透','')
                    txt = txt.replace('(展开)','')
                    txt = txt.replace('\n','').replace(' ','')
                    db_list.append({"id": id, "img": src, "name": name.string, "title": title.string, "url": url, "abstract": txt})
            else:
                pass
        #print(db_list)
        return db_list

    # 获取具体内容
    def detail(self, d_url):
        req = requests.get(d_url)
        data = BeautifulSoup(req.text, "lxml")
        cont = data.find('div', class_="review-content clearfix")
        media = cont.find('video')
        if media is None:
            video = ""
        else:
            video = media.get('src')
        txt = str(cont)
        cont =  re.sub(re.compile(r"<(?!img|p|/p).*?>", re.S), "", txt)
        dbCont = {"cont":cont,"video":video}
        return dbCont
        #return re.sub(re.compile(r"</?[^>]+>", re.S), "", txt)


if __name__ == "__main__":
    db = DouBan('https://movie.douban.com/review/latest/')
    db.latest()
    # db.detail('https://movie.douban.com/review/10455699/')
    # 豆瓣乐评    https://music.douban.com/review/latest/
    # 豆瓣最新影评 https://movie.douban.com/review/latest/
    # 豆瓣最热影评 https://movie.douban.com/review/best/