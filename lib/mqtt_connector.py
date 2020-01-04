# -*- coding: utf-8 -*-
import time
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as client
import config.config as config

class MqttConnecter():
    def __init__(self):
        self.ip = None
        self.port = None
        self.user = None
        self.passwd = None
        self.client = client.Client()
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.on_publish = on_publish
        self.client.on_subscribe = on_subscribe

    def set_user_passwd(self,user,passwd):
        self.user = user
        self.passwd = passwd
        self.client.username_pw_set(username=user, password=passwd)

    def publish(self,topic,payload,qos=1):
        self.client.loop_start()
        self.client.publish(topic,payload,qos)

    def subscribe(self,topic):
        self.client.subscribe(topic)

    def connect(self,ip,port,keep_alive=60):
        self.ip = ip
        self.port = port
        self.client.connect(ip, port, keep_alive)

    def dicconnect(self):
        self.client.disconnect()

def on_connect(client, userdata, flags, rc):
    print("Mqtt connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print('resived message: '+'topic: '+msg.topic + "; message: " + str(msg.payload))

def on_publish(client, userdata, mid):
    print('in publish:'+userdata)

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print('subscribed a topic')

if __name__ == '__main__':
    cl = MqttConnecter()
    #cl.set_user_passwd()
    cl.connect(config.MQTT_HOST,config.MQTT_PORT)
    cl.publish("/test/mq", payload="_"+time.strftime("%Y-%m-%d %H:%M:%S: ")+"xxxxxHello Python!",qos=1)
    #cl.subscribe('/test/mq')
    #cl.client.loop_forever()
    cl.dicconnect()



