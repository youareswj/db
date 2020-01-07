import requests, json
import re
from bs4 import BeautifulSoup


class HuPu:
    def __init__(self, url="", page=1):
        self.url = url
        if page == 1:
            self.page = 1
        else:
            self.page = page

    # NBA论坛
    def getUrl(self):
        url = self.url
        self.page = int(self.page)
        if self.page == 1:
            pass
        else:
            url += "-" + str(self.page)
        # print(url)
        return url

    def NBA(self, sect=1):
        url = self.getUrl()
        print("---开始抓取数据---", url)
        list = []
        min = 10 * (int(sect) - 1) + 1
        max = min + 9
        if max > 98:
            max = 98
        index = 0
        req = requests.get(url)
        data = BeautifulSoup(req.text, "lxml")
        ul = data.find('ul', class_='for-list')
        li = ul.contents
        for it in li:
            if it.string is None:
                index += 1
                if index ==1:
                    pass
                elif min <= index <= max:
                    print("-----抓取第", index, "条数据中-----")
                    title = it.find('a', class_='truetit').get_text()
                    href = 'https://bbs.hupu.com' + it.find('a', class_='truetit').get('href')
                    id = href.split('/')[-1].split('.')[0]
                    cont = self.detail(href)[1]
                    txt = re.sub(re.compile(r"</?[^>]+>",re.S),"",cont)
                    author = it.find('div', class_='author box').get_text()
                    views = it.find('span', class_='ansour box').get_text().split('/')[1]
                    tit = re.sub(re.compile(r"\s*", re.S), "", title)
                    aut = re.sub(re.compile(r"\s*", re.S), "", author)
                    vie = re.sub(re.compile(r"\s*", re.S), "", views)
                    list.append({"id":id,"title": tit, "href": href, "author": aut, "views": vie, "cont": cont, "txt": txt})
                    print("-----[标题:]", tit, "抓取成功!-----")
                else:
                    pass
        # print(list)
        return list

    def detail(self, url):
        print("-----抓取文档详细内容-----",url)
        cont = []
        comt = []
        src = []
        req = requests.get(url)
        data = BeautifulSoup(req.text, "lxml")
        title = data.find('div', class_="subhead").find("span")
        tit = str(title)
        tit = re.sub(re.compile(r"<.*?>", re.S), "", tit)
        author = data.find('div',class_="author")
        u = author.find("a",class_="u").get_text()
        media = data.find('video')
        if media is None:
            video = ""
        else:
            video = media.get('src')
        lamp = data.find('div', id="readfloor")
        if lamp is None:
            comt = ""
        else:
            lamps = lamp.contents
            for it in lamps:
                if it.string is None:
                    appoint = it.find('blockquote')
                    com_u = it.find('div',class_="author")
                    u = com_u.find('a',class_="u").get_text()
                    if appoint is not None:
                        p = it.find('td').get_text()
                        p = p.replace(appoint.get_text(),'')
                        comt.append({"comUser":u,"self": appoint.get_text(), "appoint": p})
                    else:
                        comt.append({"comUser":u,"appoint": it.find('td').get_text(), "self": ""})
        html = data.find('div', class_='quote-content')
        pics = html.find_all('img')
        if pics is None:
            src = ""
        else:
            for pic in pics:
                src.append(pic.get('src'))
        text = str(html)
        text = re.sub(re.compile(r"<(?!p|/p).*?>", re.S), "", text)
        cont.append({"title": tit,"user":u, "txt": text,"comment":comt,"pic":src,"video":video})
        return cont,text
        #print(cont)


if __name__ == "__main__":
    Hp = HuPu('https://bbs.hupu.com/vote')
    # Hp.NBA()
    # Hp.getUrl()
    Hp.detail('https://bbs.hupu.com/29599139.html')
