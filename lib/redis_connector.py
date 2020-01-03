# -*- coding: utf-8 -*-
import redis
import config.config as config

'''
{"podDir":0,"robotDir":180,"battery":88,"speed":0,"posX":36087,"timeStamp":"2019-10-10,15:40:54","posY":31648,"load":0,"commandPath":0,
"podCode":"","name":3601,"exclType":0,"realPath":0,"robotCode":3601,"mapCode":"16675DF3965113P","taskId":"16DB49A9FE53C4C_ECS","status":1}
'''

class Connector():
    def __init__(self):
        self.client = redis.Redis(host=config.REDIS_HOST,port=config.REDIS_PORT,db=0)

    def set(self,key,value):
        return self.client.set(key,value)

    def get(self,key):
        return self.client.get(key).decode('utf-8')
    
    def keys(self):
        return self.client.keys()
    
    def hset(self,name,key,value):
        return self.client.hset(name,key,value)
    
    def hget(self,name,key):
        result = self.client.hget(name,key)
        if result:
            return result.decode('utf-8')
        else:
            return None

    def subscribe(self,topic):
        ps = self.client.pubsub()
        ps.subscribe(topic)
        return ps.listen()

    def publish(self,topic,message):
        try:
            self.client.publish(topic,message)
            return True
        except Exception as error:
            print(error)
            return None

if __name__ == '__main__':
    #Connector().set('d1','{"x":100,"y":200}')
    #Connector().hset('car1','target','[200,500]')
    con = Connector()
    #print(re)
    #print(Connector().keys())
   # re = Connector().get('car1').decode('utf-8')
   # print(Connector().hget('car1','target'))

    for item in con.subscribe('topic1'):
        print(item)


