# -*- coding: utf-8 -*-
import os
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAR_MESSAGE_TOPIC = 'car_message'
INTERVAL = 1  #小车运行时间单位
CAR_STATUS_LOG = os.path.join(BASEDIR,'config/realtime.log')
SYSTEM_LOG = os.path.join(BASEDIR,'config/system.log')
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

#3D平台mqtt服务器信息
MQTT_HOST = '10.129.5.11'
MQTT_PORT = 1883
CAR_TOPIC = 'mqtt1' #'/test/mq'   #mqtt1
KEEPALIVE = 60
QOS = 0
'''format
[{
 "name": "car1",
 "position": {x:100, y:100,z:200},
 "speed": 10,
 "timestamp": "2020-01-03,10:48:32"
}]
'''

cars = [
	{
		'name': 'car1',
		'id': 'ax001',
		'speed': 10,
		'poistion': [300, 900],
		'target': [200, 500],
		'graph': {
			'1': ['2', '4', '5'],
			'2': ['1', '3'],
			'3': ['2', '5'],
			'4': ['1', '5'],
			'5': ['3', '4', '1']
		},
		'sites': {'1': [100, 900],'2': [300, 900],'3': [300, 700],'4': [100, 700],'5': [200, 500]},
        'markPoint': {
			'animation': True,
	        'animationDuratio':50,
	        'data':[
				{'name':'car1','value':'1','speed':10,'symbol': 'circle','symbolSize':20,'xAxis':150,'yAxis':700},
                {'symbol': 'pin','value':'站点1','symbolSize':50,'xAxis':100,'yAxis':900},
                {'symbol': 'pin','value':'站点2','symbolSize':50,'xAxis':300,'yAxis':700},
	        ]
        }
	},
{
		'name': 'car2',
		'id': 'ax002',
		'speed': 10,
		'poistion': [500, 300],
		'target': [800, 300],
		'graph': {
			'1': ['2', '4'],
			'2': ['1', '3'],
			'3': ['2', '4'],
			'4': ['1', '5','3'],
			'5': ['4']
		},
		'sites': {'1': [500, 300],'2': [500, 500],'3': [800, 500],'4': [800, 300],'5': [800, 200]},
		'markPoint': {
	        'data':[
		        {'name':'car2','value': '2','speed':10,'symbol': 'circle',  'symbolSize': 20, 'xAxis': 700, 'yAxis': 300},
		        {'symbol': 'pin', 'value': '充电', 'xAxis': 800, 'yAxis': 200},
	        ]
	}
}
]
