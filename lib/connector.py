# -*- coding: utf-8 -*-
import redis

'''
{"podDir":0,"robotDir":180,"battery":88,"speed":0,"posX":36087,"timeStamp":"2019-10-10,15:40:54","posY":31648,"load":0,"commandPath":0,
"podCode":"","name":3601,"exclType":0,"realPath":0,"robotCode":3601,"mapCode":"16675DF3965113P","taskId":"16DB49A9FE53C4C_ECS","status":1}
'''

class Connector():
    def __init__(self):
        self.client = redis.Redis(host='127.0.0.1',port=6379,db=0)

    def set(self,key,value):
        return self.client.set(key,value)

    def get(self,key):
        return self.client.get(key).decode('utf-8')
    
    def keys(self):
        return self.client.keys()
    
    def hset(self,name,key,value):
        return self.client.hset(name,key,value)
    
    def hget(self,name,key):
        if self.client.hget(name,key):
            return self.client.hget(name,key).decode('utf-8')
        else:
            return None

if __name__ == '__main__':
    #Connector().set('d1','{"x":100,"y":200}')
    Connector().hset('car1','target','[200,500]')
    #re = Connector().get('d1').decode('utf-8')
    #print(re)
    #print(Connector().keys())
   # print(Connector().hget('a','list1').decode('utf-8'))


