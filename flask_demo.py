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
    return '{"status":"ok"}'

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
                #try:
                #    message = ws.receive()
                #except WebSocketError:
                #    break
                #print(message)

                #data = [data_generate(30),data_generate(30)]

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
            tmp = {'name':config.cars[index]['name'],'data':[],'markPoint':config.cars[index]['markPoint']}
            for line in linedata[index]:
                for p in line:
                    tmp['data'].append(config.cars[index]['sites'][p])
            linexy.append(tmp)

        response = {"status": "ok", "line": linexy,"markpoint":None}  #发送路径信息给前端
        response = json.dumps(response)
        ws.send(response)

        if not ws:
            return {"status": "error", "message": "request is not websocket"}
        else:
            print("client connected")
            #th = threading.Thread(target = Tool.handler_websocket,args=(ws,))
            #th.start()
            #return {"status": "ok", "message": "connect is aliving"}

            while 1:
                # try:
                #    message = ws.receive()
                # except WebSocketError:
                #    break
                # print(message)
                position = []
                print('in while')
                for car in config.cars:
                    position.append({'name': car['name'], 'data': Tool.get_car_realtime_msg(car['name'])})

                response = {"status": "ok","line":None,"markpoint": position}
                response = json.dumps(response)
                ws.send(response)
                time.sleep(1)

    else:
        return {"status": "error", "message": "request is not websocket"}


#@cross_origin()
@app.route("/submit",methods=["GET","POST"])
def submit():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    print(data)
    for key in data:
        if key != 'car' and data[key] != '':
            if key == 'speed':
                try:
                    float(data[key])
                    Connector().hset(data['car'], key, data[key])
                except Exception as e:
                    print('input speed error!')
            elif key == 'target' and type(eval(data[key])) == type([]):
                try:
                    float(eval(data[key])[0])+float(eval(data[key])[1])
                    Connector().hset(data['car'], key, data[key])
                except Exception as e:
                    print('input target error!')
                    print(e)
            else:
                Connector().hset(data['car'],key,data[key])

    response = {"status": "ok"}
    return jsonify(response)

if __name__=="__main__":
    #app.run(host='0.0.0.0', port=8080, debug=True)
    print("start WSGIServer enter Ctrl+c exit")
    http_server = WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)
    http_server.serve_forever()