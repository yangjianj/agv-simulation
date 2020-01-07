# -*- coding: utf-8 -*-
from flask_cors import *
import time,json,random
from flask import Flask,render_template,request,jsonify
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from gevent import monkey
import lib.tool as Tool
from lib.connector import Connector
import config.config as config

monkey.patch_all()  #遇到阻塞自动切换协程，程序启动时执行
app= Flask(__name__)
CORS(app,resources={r'/*':{"origins": "*"}})

@app.route("/")
def index():
    return '<h1> hello flask !</h1>'

@app.route("/get_json")
def get_json():
    response = {"status":"ok","data":[],'workmode':list(config.CAR_MODE_MAP.keys())}
    response["data"] = config.cars
    '''
    for index in range(len(config.cars)):
        name = config.cars[index]['name']
        response["data"].append({"id":index,"name":name})
        '''
    return json.dumps(response)

@app.route("/wsocket")
def websocket_connect():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']

        if not ws:
            return {"status":"error","message":"request is not websocket"}
        else:
            #while(1):
            print("client connected")
            data1 = [[100,200],[200,200],[200,400],[100,400]]
            data2 = [[600,300],[800,300],[800,400],[600,400]]

            data = [
                {
                    'name':'a',
                    'site':[[100, 900], [300, 900], [300, 700], [100, 700]],
                    'curr':[100,900],
                    'target':[100,700]
                    },
                {
                    'name': 'b',
                    'site': [[800, 500], [800, 300], [800, 200],[500, 300], [500, 500]],
                    'curr': [800, 500],
                    'target': [800, 200]
                },
            ]
            postdata = [{"offsetX":0,"offsetY":0},{"offsetX":0,"offsetY":0}]
            for i in range(50):
                postdata[0]["offsetX"] = data1[i%4][0]+random.randint(0,15)
                postdata[0]["offsetY"] = data1[i%4][1]+random.randint(0,15)
                postdata[1]["offsetX"] = data2[i%4][0]+random.randint(0,15)
                postdata[1]["offsetY"] = data2[i%4][1]+random.randint(0,15)
                response = {"status":"ok","message":postdata}
                response = json.dumps(response)
                ws.send(response)
                time.sleep(5)

    else:
        return {"status": "error", "message": "request is not websocket"}

@app.route("/markpoint")
def websocket_markpoint():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        linedata = []
        linexy = []
        for index in range(len(config.cars)):
            linedata.append(Tool.build_line(config.cars[index]['graph'],path=[]))
            tmp = {'name':config.cars[index]['name'],'data':[],'markPoint':config.cars[index]['markPoint'],'color':config.cars[index]['color']}
            for line in linedata[index]:
                for p in line:
                    tmp['data'].append(config.cars[index]['sites'][p])
            linexy.append(tmp)

        response = {"status": "ok", "line": linexy,"markpoint":None}  #初始化路径信息
        response = json.dumps(response)
        ws.send(response)

        if not ws:
            return {"status": "error", "message": "request is not websocket"}
        else:
            print("client connected")
            for message in Tool.subscribe(config.CAR_MESSAGE_TOPIC):
                message['channel'] = message['channel'].decode('utf-8')
                if type(message['data']).__name__ == 'bytes':
                    message['data'] = message['data'].decode('utf-8')
                    message['data'] = json.loads(message['data'])
                if type(message['data']) is dict:
                    response = {"status": "ok", "line": None, "markpoint":message}
                    response = json.dumps(response)
                    ws.send(response)
                #time.sleep(config.INTERVAL)
            '''
            while 1:
                # try:
                #    message = ws.receive()
                # except WebSocketError:
                #    break
                # print(message)
                position = []
                for car in config.cars:
                    position.append({'name': car['name'], 'data': Tool.get_car_realtime_msg(car['name'])})

                response = {"status": "ok","line":None,"markpoint": position}
                response = json.dumps(response)
                ws.send(response)
                time.sleep(config.INTERVAL)
                '''
    else:
        return {"status": "error", "message": "request is not websocket"}


#@cross_origin()
@app.route("/submit",methods=["GET","POST"])
def submit():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    print(data)
    result = {}
    try:
        if data['speed'] != '':
            float(data['speed'])
            Connector().hset(data['car'], 'speed', data['speed'])
        if data['source'] != '':
            float(eval(data['source'])[0])+float(eval(data['source'])[1])
            Connector().hset(data['car'], 'source', data['source'])
        if data['target'] != '':
            float(eval(data['target'])[0])+float(eval(data['target'])[1])
            Connector().hset(data['car'], 'target', data['target'])
        if data['status'] != '':
            s_code = config.CAR_STATUS_MAP[data['status']]
            Connector().hset(data['car'], 'status', s_code)
        if data['mode'] != '':
            m_code = config.CAR_MODE_MAP[data['mode']]
            Connector().hset(data['car'], 'mode', m_code)
        result['status'] = 'ok'
    except Exception as e:
        print(e)
        result['status'] = 'error'
    return jsonify(result)

if __name__=="__main__":
    #app.run(host='0.0.0.0', port=8080, debug=True)
    print("start WSGIServer enter Ctrl+c exit")
    http_server = WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)
    http_server.serve_forever()