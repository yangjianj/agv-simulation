import time,copy,re,json
import redis
from datetime import datetime
print(1<2<3)

print(round(2/3,2))
print(datetime.now().strftime('%Y%m%d-%H%M%S%f'))
print(float('12.36'))
xx = '[100,200]'
print(type(eval(xx)) == type([]))
print(type([]))

r = redis.Redis(host='127.0.0.1',port=6379,db=0)

ps = r.pubsub()
ps.subscribe(['topic1','topic2','car_message'])
for item in ps.listen():
	print(item)
	print(type(item['channel']).__name__)

	item['channel'] = item['channel'].decode('utf-8')
	if type(item['data']).__name__ == 'bytes':
		item['data'] = item['data'].decode('utf-8')
	#item['data'] = item['data'].encode('utf-8')
	print(json.dumps(item,ensure_ascii=False))


