# -*- coding: utf-8 -*-
import math,time,json
import threading,argparse
from lib.connector import Connector
import lib.tool as Tool
import config.config as config
class Car():
    def __init__(self,name,position,target,sites,graph,speed):
        self.position = position[:]
        self.source = position[:]
        self.target = target
        self.path = None
        self.appoint = False  #指定路径标志，默认为最短路径
        self.path_appoint = []
        self.willpath = None
        self.sites = sites
        self.graph = graph
        self.speed = speed
        self.status = '0'
        self.x_step = 0
        self.y_step = 0
        self.name = name
        self.id = 'ax001'
        self.mode = '0'
        self.status = None
        self.con = Connector()
        self._init_redis()

    def _init_redis(self):
        self.set_car_msg('position', str(self.position))
        self.set_car_msg('target', str(self.target))
        self.set_car_msg('speed', str(self.speed))
        self.set_car_msg('appoint','false')

    def get_near_site(self):
        for k,v in self.graph.items():
            if self.position == self.sites[k]:
                return [k]
            s1 = self.sites[k]
            for dst in v:
                s2 = self.sites[dst]
                if Tool.three_point_like_line(s1,self.position,s2,3):
                    return [k,dst]

    def compute_distance(self,position=None,nextp=None):
        #计算当前点到下一站点的距离
        if position == None:
            position = self.position
        if nextp == None:
            nextp = self.sites[self.willpath[0]]
        x_dis = nextp[0]-position[0]
        y_dis =  nextp[1]-position[1]
        distance = math.sqrt((x_dis**2)+(y_dis**2))
        if distance != 0 :
            x_step = self.speed/config.INTERVAL/distance*x_dis
            y_step = self.speed/config.INTERVAL/distance*y_dis
        else:
            x_step = 0
            y_step = 0
        result = {'nextp':nextp,'distance':distance,'x_step':x_step,'y_step':y_step}
        return result

    def compute_path_distance(self,position=None,path=None):
        #计算当前坐标到路径终点的距离
        if position == None:
            position = self.position
        distance = 0
        tmps = position
        for pxy in path:
            x_dis = self.sites[pxy][0] - tmps[0]
            y_dis = self.sites[pxy][1] - tmps[1]
            distance = distance+(math.sqrt((x_dis ** 2) + (y_dis ** 2)))
            tmps = self.sites[pxy]
        return distance

    def _align_step(self):
        #校准小车位置到站点
        if len(self.willpath) != 0:
            nextp = self.willpath[0]
            nextpxy = self.sites[nextp][:]
            if abs(self.position[0]-nextpxy[0])<=abs(self.x_step) and abs(self.position[1]-nextpxy[1])<=abs(self.y_step):
                self.x_step = nextpxy[0]-self.position[0]
                self.y_step = nextpxy[1]-self.position[1]
                return nextpxy
            else:
                return None

    def change_target(self,target):
        self.target = target
        self.speed = config.DEFAULT_SPEED if self.speed == 0 else self.speed
        re = self._build_path()
        Tool.log_info("change_target: %s target to: %s" % (self.name, self.target),config.CAR_STATUS_LOG)
        return re

    def change_speed(self,speed):
        self.speed = float(speed)
        if len(self.willpath) == 0:
            return None
        dist = self.compute_distance(self.position, self.sites[self.willpath[0]])
        self.x_step = dist['x_step']
        self.y_step = dist['y_step']
        self.set_car_msg('speed', str(self.speed))
        #Tool.log_info("change_speed: %s speed to: %s"%(self.name,self.speed*config.INTERVAL),config.CAR_STATUS_LOG)

    def run(self):
        self.set_car_msg('status',config.CAR_STATUS_MAP['run'])
        self.set_car_msg('mode',config.CAR_MODE_MAP['normal']) #normal mode
        self._build_path()
        while(1):
            car_msg = self.get_car_msg_all()
            targetxy = car_msg['target']
            sw = self._switch_mode(car_msg)
            if sw == True:
                continue
            if car_msg['appoint'] != False and car_msg['appoint'] != None:
                self._appoint_path()
                if len(self.willpath) != 0:
                    dist = self.compute_distance(self.position, self.sites[self.willpath[0]])
                    self.x_step = dist['x_step']
                    self.y_step = dist['y_step']
            if targetxy != self.target:
                self.change_target(targetxy)
            if car_msg['speed'] != self.speed:
                self.change_speed(car_msg['speed'])
            if len(self.willpath) == 0:
                self.finished_work()
            elif self.position == self.sites[self.willpath[0]]:
                self.switch_nextpoint()
                print(self.name, 'willpath:', self.willpath)
            self._update_position()
            real_message = {'name': self.name, 'position': self.position, 'speed': self.speed,'timestamp': time.strftime('%Y-%m-%d,%H:%M:%S')}
            Tool.publish(config.CAR_MESSAGE_TOPIC, json.dumps(real_message))
            time.sleep(1/config.INTERVAL)

    def _loop_mode(self,msg):
        #loop mode
        if self.appoint != True:
            self.source = msg['source'][:]
            self.target = msg['target'][:]
            self.position = msg['source'][:]
            self.speed = float(msg['speed'])
        self.mode = config.CAR_MODE_MAP['loop']
        self._build_path()
        while(self.mode == config.CAR_MODE_MAP['loop']):
            car_msg = self.get_car_msg_all()
            print('on 55555', self.willpath, len(self.willpath))
            print(self.source)
            print(self.target)
            if self.mode != car_msg['mode']:
                self.mode = car_msg['mode']
                return True  #exit loop mode
            if car_msg['appoint'] != False or car_msg['appoint'] != None:
                self._appoint_path()
                if len(self.willpath) != 0:
                    dist = self.compute_distance(self.position, self.sites[self.willpath[0]])
                    self.x_step = dist['x_step']
                    self.y_step = dist['y_step']
            print('on 55555', self.willpath, len(self.willpath))
            sourcexy = car_msg['source']
            targetxy = car_msg['target']
            if (targetxy != self.target and targetxy != self.source) or (sourcexy != self.target and sourcexy != self.source): #change source and target
                if car_msg['appoint'] == False:
                    self.source = sourcexy[:]
                    self.target = targetxy[:]
                    self.position = sourcexy[:]
                    self.speed = float(car_msg['speed'])
                self._build_path()
            if car_msg['speed'] != str(self.speed):
                self.change_speed(car_msg['speed'])
            print('on 66666',self.willpath,len(self.willpath))
            if len(self.willpath) == 0:  # switch source and target
                print('22222222')
                print(self.appoint)
                if self.appoint == False:
                    print('switch source and target')
                    tmp = self.target
                    self.change_target(self.source)
                    self.source = tmp
                else:
                    self.path_appoint.reverse()
                    self.willpath = self.path_appoint[:]
            elif self.position == self.sites[self.willpath[0]]:  # 切换nextp
                self.switch_nextpoint()
                #print(self.name, 'willpath:', self.willpath)
            self._update_position()
            real_message = {'name': self.name, 'position': self.position, 'speed': self.speed,'timestamp': time.strftime('%Y-%m-%d,%H:%M:%S')}
            Tool.publish(config.CAR_MESSAGE_TOPIC, json.dumps(real_message))
            print('in loop','willpath',self.willpath,'speed',self.speed)
            print(self.source,self.target)
            time.sleep(1 / config.INTERVAL)
        return False

    def _build_path(self):
        #路径：根据当前坐标+目的坐标，初始化行走路径，x_step,y_step
        if self._appoint_path() == True:
            pass
        else:
            target = self.target
            target = self._get_sites_key(target)
            nearsites = self.get_near_site()
            spath = None
            for near in nearsites:
                plist=Tool.find_shartest_path(self.graph,near,target)
                for p in plist:
                    distance = self.compute_path_distance(self.position,p)
                    if not spath:
                        spath = [p,distance]
                    elif distance < spath[1]:
                        spath = [p,distance]
            self.path = spath[0]
            self.willpath = self.path[:]
        if len(self.willpath) != 0:
            dist = self.compute_distance(self.position,self.sites[self.willpath[0]])
            self.x_step = dist['x_step']
            self.y_step = dist['y_step']
        return True

    def _appoint_path(self):
        #appoint  true-将source作为初始值给willpath赋值
        car_msg = self.get_car_msg_all()
        if car_msg['appoint'] == False:
            self.appoint = False
            return False
        if car_msg['appoint'] == None:
            return True
        if car_msg['appoint'] == True:
            self.appoint = True
            source = car_msg['source']
            site = self._get_sites_key(source)
            self.source = car_msg['source'][:]
            self.target = car_msg['target'][:]
            self.willpath = [site]
            self.path = [site]
            self.path_appoint = self.path[:]
            self.position = source
        if self.appoint == True and car_msg['appoint'] != True :
            appoint = car_msg['appoint']
            site = self._get_sites_key(appoint)
            if site != self.path[-1]:
                self.willpath.append(site)
                self.path.append(site)
                self.path_appoint= self.path[:]
        self.set_car_msg('appoint','')
        return True

    def switch_nextpoint(self):
        del (self.willpath[0])
        if len(self.willpath) != 0:
            nextp = self.compute_distance()
            self.x_step = nextp['x_step']
            self.y_step = nextp['y_step']
        else:
            self.x_step = 0
            self.y_step = 0

    def _get_sites_key(self,xy):
        for k,v in self.sites.items():
            if xy == v:
                return k

    def set_car_msg(self,key,value):
        #redis_key: self.name
        #key :target,speed,status
        return self.con.hset(self.name, key,value)

    def get_car_msg(self,key):
        # redis_key: self.name
        # key : name,target,speed,status
        return self.con.hget(self.name, key)

    def get_car_msg_all(self):
        source = Tool.convert_xystr_xylist(self.get_car_msg('source'))
        target = Tool.convert_xystr_xylist(self.get_car_msg('target'))
        status = self.get_car_msg('status')
        speed = float(self.get_car_msg('speed'))
        mode = self.get_car_msg('mode')
        appoint = self.get_car_msg('appoint')
        if appoint == 'false':
            appoint = False
        elif appoint == '' or appoint == None:
            appoint = None
        elif appoint == 'true':
            appoint = True
        else:
            appoint = Tool.convert_xystr_xylist(self.get_car_msg('appoint'))
        return {'source':source,'target':target,'status':status,'speed':speed,'mode':mode,'appoint':appoint}

    def set_realtime_msg(self,key,value=None):
        #key: name,status,osition,
        rediskey = self.name + '_' + time.strftime('%Y%m%d-%H%M%S')
        self.con.hset(rediskey, 'target', str(self.target))
        self.con.hset(rediskey, 'name', self.name)
        self.con.hset(rediskey, 'position', str(self.position))
        self.con.hset(rediskey, 'status', self.status)
        self.con.hset(rediskey, 'id', self.id)
        self.con.hset(rediskey, key, value)

    def _update_position(self):
        self._align_step()
        self.position[0] = round(self.position[0] + self.x_step,8)
        self.position[1] = round(self.position[1] + self.y_step,8)

    def _switch_mode(self,car_msg):
        if car_msg['mode'] == config.CAR_MODE_MAP["loop"]:
            sw = self._loop_mode(car_msg)
            return sw
    
    def _switch_status(self,car_msg):
        if car_msg['status'] == config.CAR_STATUS_MAP['stop']:
            self.set_car_msg('status', str(self.position))

    def finished_work(self):
        self.status = config.CAR_STATUS_MAP['idel']
        self.y_step = 0
        self.y_step = 0
        #self.set_car_msg('speed', str(self.speed))
        self.set_car_msg('status', self.status)  # 运行状态

    def _energy_profiler(self):
        #检测电量，不足时让小车进入充电站充电
        pass

    def _position_conflict(self):
        #防止小车碰撞
        pass

if __name__ == '__main__':
    graph1 = {
        '1': ['2', '4', '5'],
        '2': ['1', '3'],
        '3': ['2', '5'],
        '4': ['1', '5'],
        '5': ['3', '4', '1']
    }
    sites1 = {
        '1': [100, 900],
        '2': [300, 900],
        '3': [300, 700],
        '4': [100, 700],
        '5': [200, 500]
    }
    '''
    car = Car('car1', [100, 900], [200, 500], sites, graph, 10)
    car.run()

    '''

    cars = []
    x=0
    for item in config.cars:
        if x != 0:
            continue
        x=x+1
        id = item['name']
        start = item['poistion']
        target = item['target']
        sites = item['sites']
        graph0 = item['graph']
        speed = item['speed']
        car = Car(id,start,target,sites,graph0,speed)
        #car.run()
        t=threading.Thread(target=car.run,args=())
        cars.append(t)
        t.start()
    for t in cars:
        t.join()


