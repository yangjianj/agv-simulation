import time,redis,json

r = redis.Redis(host='127.0.0.1',port=6379,db=0)

r.publish('topic1','123456'+str(time.time()))

x = {"name": "car1","position": [200.0, 500.0],"speed": 0}
y= {'status': 'ok', 'line': None, 'markpoint': {'type': 'subscribe', 'pattern': None, 'channel': b'car_message', 'data': 1}}
y['markpoint']['channel'] = y['markpoint']['channel'].decode('utf-8')
print(json.dumps(x))
print(json.dumps(y))