# -*- coding: utf-8 -*-
import math,time
from lib.connector import Connector
class Car():
    def __init__(self,name,curr,target,sites,graph,speed):
        self.curr = curr   #[0,0]
        self.target = target    #[100,100]
        self.path = None
        self.willpath = None
        self.sites = sites
        self.graph = graph
        self.speed = speed  #10
        self.status = 'normal'
        self.x_step = 0
        self.y_step = 0
        self.name = name
        self.id = 'ax001'
        self.init_path(target)
        self.con = Connector()

        '''
        self.sites = {
            '1':[100, 900],
            '2':[300, 900],
            '3':[300, 700],
            '4':[100, 700]
        }

        self.graph = {
            '1':['2','4'],
            '2':['1','3'],
            '3':['2','4'],
            '4':['1','3']
        }
        


    def change_target1(self,target):
        if self.curr[0] != self.target[0] and self.curr[1] != self.target[1]:
            pass
        elif self.curr[0] != self.target[0]:
            tmp = self.curr[0]
            if  self.curr[0] < self.target[0]:
                while(tmp<self.target[0]):
                    tmp = tmp+self.speed
                    if tmp>self.target[0]:
                        self.path.append([self.curr[1], self.target[0]])
                    else:
                        self.path.append([self.curr[1],tmp])
            else:
                while (tmp > self.target[0]):
                    tmp = tmp - self.speed
                    if tmp < self.target[0]:
                        self.path.append([self.curr[1], self.target[0]])
                    else:
                        self.path.append([self.curr[1], tmp])
        elif self.curr[1] != self.target[1]:
            tmp = self.curr[1]
            if  self.curr[1] < self.target[1]:
                while(tmp<self.target[1]):
                    tmp = tmp+self.speed
                    if tmp>self.target[1]:
                        self.path.append([self.curr[0], self.target[1]])
                    else:
                        self.path.append([self.curr[0],tmp])
            else:
                while (tmp > self.target[1]):
                    tmp = tmp - self.speed
                    if tmp < self.target[1]:
                        self.path.append([self.curr[0], self.target[1]])
                    else:
                        self.path.append([self.curr[0], tmp])

        return self.path
'''
    def get_near_site(self):
        for k,v in self.graph.items():
            if self.curr == self.sites[k]:
                return [k]
            else:
                s1 = self.sites[k]
                for dst in v:
                    s2 = self.sites[dst]
                    if self.three_point_online(s1,self.curr,s2):
                        return [k,dst]

    def three_point_online(self,p1,p2,p3):
        if p3[1] != p1[1]:
            if (p2[0]-p1[0])/(p2[1]-p1[1]) == (p3[0]-p3[0])/(p3[1]-p1[1]) and (p2[0]-p1[0])*(p2[0]-p3[0])<=0:
                return True
        else:
            if p2[1] == p1[1] and (p2[0]-p1[0])*(p2[0]-p3[0])<=0:
                return True

    #找出一条路径
    def find_a_path(self,graph,start,end,path=[]):
        path = path + [start]
        if start == end:
            return path
        for node in graph[start]:
            if node not in path:
                newpath = self.find_a_path(graph, node, end, path)
                if newpath:
                    return newpath
        return None

    def find_all_path(self,graph,start,end,path=[]):
        path = path + [start]
        if start == end:
            return [path]
        paths = []  # 存储所有路径
        for node in graph[start]:
            if node not in path:
                newpaths = self.find_all_path(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_shartest_path(self,graph,start,end,path=[]):
        path = path + [start]
        if start == end:
            return path
        shortestPath = []
        for node in graph[start]:
            if node not in path:
                newpath = self.find_shartest_path(graph, node, end, path)
                if newpath:
                    if not shortestPath or len(newpath) < len(shortestPath):
                        shortestPath = newpath
        return shortestPath

    def compute_distance(self,curr=None,nextp=None):
        if curr == None:
            curr = self.curr
        if nextp == None:
            nextp = self.sites[self.willpath[0]]
        x_dis = nextp[0]-curr[0]
        y_dis =  nextp[1]-curr[1]
        distance = math.sqrt((x_dis**2)+(y_dis**2))
        #x_step = round(x_dis/self.speed,3)
        #y_step = round(y_dis/self.speed,3)
        if distance != 0 :
            x_step = round(self.speed/distance,10)*(x_dis)
            y_step = round(self.speed/distance,10)*(y_dis)
        else:
            x_step = 0
            y_step = 0
        result = {'nextp':nextp,'distance':distance,'x_step':x_step,'y_step':y_step}
        return result

    def compute_path_distance(self,curr=None,path=None):
        #计算当前坐标到路径终点的距离
        if curr == None:
            curr = self.curr
        distance = 0
        tmps = curr
        for pxy in path:
            x_dis = self.sites[pxy][0] - tmps[0]
            y_dis = self.sites[pxy][1] - tmps[1]
            distance = distance+(math.sqrt((x_dis ** 2) + (y_dis ** 2)))
            tmps = self.sites[pxy]
        return distance

    def align_step(self):
        #校准小车位置到站点
        if len(self.willpath) != 0:
            nextp = self.willpath[0]
            nextpxy = self.sites[nextp][:]
            x = self.curr[0]-nextpxy[0]
            y = self.curr[1]-nextpxy[1]
            if abs(self.curr[0]-nextpxy[0])<=abs(self.x_step) and abs(self.curr[1]-nextpxy[1])<=abs(self.y_step):
                self.x_step = nextpxy[0]-self.curr[0]
                self.y_step = nextpxy[1]-self.curr[1]
                return nextpxy
            else:
                return None

    def change_target(self,target):
        target = self.get_sites_key(target)
        if self.target == target:
            return self.target
        else:
            self.target = target
        nearsites = self.get_near_site()
        tmppath = []
        #待改进，暂没有运算路径间距离
        for near in nearsites:
            x=self.find_shartest_path(self.graph,near,target)
            tmppath.append(x)
        shortnear = []  #下一个点到离最近的一个站点
        for p in tmppath:
            dist = self.compute_distance(self.curr,p[0])
            if shortnear == []:
                shortnear.append(dist,p)
            elif dist<shortnear[0]:
                shortnear[0] = dist
                shortnear[1] = p

        self.path = shortnear[1]
        self.willpath = self.path[1:]
        return self.path

    def init_path(self,target):
        target = self.get_sites_key(target)
        nearsites = self.get_near_site()
        spath = None
        #待改进，暂没有运算路径间距离
        for near in nearsites:
            x=self.find_shartest_path(self.graph,near,target)
            distance = self.compute_path_distance(self.curr,x)
            if not spath:
                spath = [x,distance]
            elif distance<spath[1]:
                spath = [x,distance]
        dist = self.compute_distance(self.curr,self.sites[spath[0][0]])
        '''
        shortnear = []  #
        for p in tmppath:
            pxy = self.sites[p[0]]
            dist = self.compute_distance(self.curr,pxy)
            if shortnear == []:
                shortnear=[dist,p]
            elif dist['distance']<shortnear[0]['distance']:
                shortnear=[dist,p]
        self.path = shortnear[1]
        self.willpath = self.path
        self.x_step = shortnear[0]['x_step']
        self.y_step = shortnear[0]['y_step']
        '''
        self.path = spath[0]
        self.willpath = self.path
        self.x_step = dist['x_step']
        self.y_step = dist['y_step']
        return self.path

    def switch_nextpoint(self):
        del (self.willpath[0])
        if len(self.willpath) != 0:
            nextp = self.compute_distance()
            self.x_step = nextp['x_step']
            self.y_step = nextp['y_step']
        else:
            self.x_step = 0
            self.y_step = 0

    def convert_point_str(self,pstr):
        p = pstr.replace('[', '')
        p = p.replace(']', '')
        p = p.split(',')
        p[0] = float(p[0])
        p[1] = float(p[1])
        return p

    def get_sites_key(self,xy):
        for k,v in self.sites.items():
            if xy == v:
                return k

    def redis_message(self,action,key,value=None):
        rediskey = self.name + '_' + time.strftime('%Y%m%d-%H%M%S')
        if action == 'hset':
            self.con.hset(rediskey, 'target', str(self.target))
            self.con.hset(rediskey, 'name', self.name)
            self.con.hset(rediskey, 'position', str(self.curr))
            self.con.hset(rediskey, 'status', self.status)
            self.con.hset(rediskey, 'id', self.id)
            self.con.hset(rediskey, key,value)
        elif action == 'hget':
            return self.con.hget(rediskey,key)

    def run(self):
        nextp = self.compute_distance()
        self.x_step = nextp['x_step']
        self.y_step = nextp['y_step']
        self.con.hset(self.name, 'target',str(self.target))
        while(1):
            print(self.name,'curr',str(self.curr))
            print('willpath:',self.willpath)
            self.con.hset(self.name,'curr',str(self.curr))

            target = self.con.hget(self.name,'target')
            targetxy = self.convert_point_str(target)
            if targetxy != self.target:
                self.change_target()
            else:
                self.con.hset(self.name, 'curr', str(self.curr))
                if len(self.willpath) == 0:
                    self.x_step = 0
                    self.y_step = 0
                elif self.curr == self.sites[self.willpath[0]]:  # 切换nextp
                    self.switch_nextpoint()
            self.align_step()
            self.curr[0] = self.curr[0] + self.x_step
            self.curr[1] = self.curr[1] + self.y_step
            time.sleep(1)

    def loop(self):
        pass

if __name__ == '__main__':
    graph = {
        '1': ['2', '4','5'],
        '2': ['1', '3'],
        '3': ['2', '5'],
        '4': ['1', '5'],
        '5': ['3','4','1']
    }
    sites={
        '1': [100,900],
        '2': [300,900],
        '3': [300,700],
        '4': [100,700],
        '5': [200,500]
    }
    car = Car('car1',[300,880],[100,700],sites,graph,10)
    car.run()

