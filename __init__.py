import time, json
from flask import Flask, request
from flask_cors import CORS
from DouBian import DouBan
from HuPu import HuPu
from WeiBo import WeiBo

if __name__ == "__main__":
    server = Flask(__name__)
    CORS(server, resources=r'/*')


    @server.route('/DB', methods=['get'])
    def DB():
        page = request.args.get('p')
        if page is None:
            p = 1
        else:
            p = page
        db = DouBan('https://movie.douban.com/review/best/', p)
        db = db.latest()
        res = {'success': True, 'data': db}
        return res


    @server.route('/DB_latest', methods=['get'])
    def DB_latest():
        db = DouBan('https://movie.douban.com/review/latest/')
        db_list = db.latest()
        res = {'success': True, 'data': db_list}
        return res


    @server.route('/HP', methods=['get'])
    def HP():
        page = request.args.get('p')
        sect = request.args.get('s')
        db = HuPu('https://bbs.hupu.com/vote', page)
        hp_list = db.NBA(sect)
        res = {'success': True, 'data': hp_list}
        return res


    @server.route('/WB', methods=['get'])
    def WB():
        sid = request.args.get('s')
        wb = WeiBo('https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0')
        if sid is None:
            sid = 0
        wb_list = wb.Host(sid)
        res = {'success': True, 'data': wb_list}
        return res


    @server.route('/detail', methods=['get'])
    def detail():
        type = int(request.args.get('t'))
        if type == 1:
            hid = request.args.get('id')
            hUrl = "https://bbs.hupu.com/" + hid + ".html"
            hp = HuPu()
            cont = hp.detail(hUrl)[0]
            res = {'success': True, 'data': cont}
            return res
        elif type == 2:
            did = request.args.get('id')
            dUrl = "https://movie.douban.com/review/" + did
            db = DouBan()
            dbCont = db.detail(dUrl)
            res = {'success': True, 'data': dbCont}
            return res


    server.run(port=1110, debug=True, host='0.0.0.0')
