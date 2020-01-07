import time,json
from flask import Flask
from apscheduler.schedulers.blocking import BlockingScheduler
from flask_cors import CORS
from WeiBo import WeiBo

server = Flask(__name__)
CORS(server, resources=r'/*')

@server.route('/DB', methods=['get'])
def DB():
    WB = WeiBo('https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0&since_id=0')
    date = WB.Host()
    # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res = {'success': True, 'data': date}
    return json.dumps(res, ensure_ascii=False)


server.run(port=1110, debug=True, host='0.0.0.0')