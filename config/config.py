# -*- coding: utf-8 -*-
import os
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAR_MESSAGE_TOPIC = 'car_message'
INTERVAL = 5  #每秒上报5次位置信息
DEFAULT_SPEED = 100
CAR_STATUS_LOG = os.path.join(BASEDIR,'config/realtime.log')
SYSTEM_LOG = os.path.join(BASEDIR,'config/system.log')

#本地Redis服务器，与web信息交互
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

#3D平台mqtt服务器信息
MQTT_HOST = '10.129.5.11'
MQTT_PORT = 1883
CAR_MQTT_TOPIC = ['car1','car2','car3'] #'/test/mq'   #mqtt1
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

#模拟小车数据
#status : 0-空闲，1-完成任务，2-运行，3-红外防撞，5-暂停，6-货架举放中，7-充电，81-红外防撞，246-待机模式,
#mode: 0-normal 1-loop
CAR_STATUS_MAP = {'idel':'0','finish':'1','run':'2','pause':'5','charge':'7','stop':'9',}
CAR_MODE_MAP = {'normal':'0','loop':'1','circle':'2'}
cars = [
	{
		'name': 'car1',
		'id': 'ax001',
		'speed': DEFAULT_SPEED,
		'poistion': [3000, 9000],
		'target': [2000, 5000],
        'color': '#00ef00',
		'graph': {
			'1': ['2', '4', '5'],
			'2': ['1', '3'],
			'3': ['2', '5'],
			'4': ['1', '5'],
			'5': ['3', '4', '1']
		},
		'sites': {'1': [1000, 9000],'2': [3000, 9000],'3': [3000, 7000],'4': [1000, 7000],'5': [2000, 5000]},
        'markPoint': {
			'animation': True,
	        'animationDuratio':50,
	        'data':[
				{'name':'car1','value':'1','speed':10,'symbol': 'circle','symbolSize':20,'xAxis':1000,'yAxis':7000},
                {'symbol': 'pin','value':'站点1','symbolSize':50,'xAxis':1000,'yAxis':9000},
                {'symbol': 'pin','value':'站点2','symbolSize':50,'xAxis':3000,'yAxis':7000},
	        ]
        }
	},
{
		'name': 'car2',
		'id': 'ax002',
		'speed': DEFAULT_SPEED,
		'poistion': [5000, 3000],
		'target': [8000, 3000],
        'color': '#00ffff',
		'graph': {
			'1': ['2', '4'],
			'2': ['1', '3'],
			'3': ['2', '4'],
			'4': ['1', '5','3'],
			'5': ['4']
		},
		'sites': {'1': [5000, 3000],'2': [5000, 5000],'3': [8000, 5000],'4': [8000, 3000],'5': [8000, 2000]},
		'markPoint': {
            'animation': True,
	        'animationDuratio':50,
	        'data':[
		        {'name':'car2','value': '2','speed':10,'symbol': 'circle',  'symbolSize': 20, 'xAxis': 7000, 'yAxis': 3000},
		        {'symbol': 'pin', 'value': '充电', 'xAxis': 8000, 'yAxis': 2000},
	        ]
	}
},
{
		'name': 'car3',
		'id': 'ax003',
		'speed': DEFAULT_SPEED,
		'poistion': [3000, 4000],
		'target': [3000, 0],
        'color': '#0000ef',
		'graph': {
			'1': ['2', '4'],
			'2': ['1', '3'],
			'3': ['2', '4'],
			'4': ['1', '3'],
		},
		'sites': {'1': [3000, 4000],'2': [4000, 4000],'3': [4000, 0],'4': [3000, 0]},
		'markPoint': {
            'animation': True,
	        'animationDuratio':50,
	        'data':[
		        {'name':'car2','value': '3','speed':10,'symbol': 'circle',  'symbolSize': 20, 'xAxis': 3000, 'yAxis': 4000},
		        {'symbol': 'pin', 'value': '充电', 'xAxis': 3000, 'yAxis': 4000},
	        ]
	}
}
]
