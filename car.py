# -*- coding: utf-8 -*-
import math
class Car():
    def __init__(self,name,curr,target,sites,graph,speed):
        self.curr = curr   #[0,0]
        self.target = target    #[100,100]
        self.path = None
        self.willpath = None
        #self.sites = sites
        #self.graph = graph
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
        self.name = name
        self.speed = speed  #10
        self.x_step = 0
        self.y_step = 0

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

    def get_near_site(self):
        for k,v in self.graph.items():
            print(k)
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
            if p2[1] == p1[1] and (p2(0)-p1(0))*(p2(0)-p3(0))<=0:
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
            nextp = self.willpath[0]
        x_dis = nextp[0]-curr[0]
        y_dis =  nextp[1]-curr[1]
        distance = math.sqrt((x_dis**2)+(y_dis**2))
        x_step = round(x_dis/self.speed,3)
        y_step = round(y_dis/self.speed,3)
        result = {'next':next,'distance':distance,'x_step':x_step,'y_step':y_step}
        return result

    def check_and_align(self):
        #校准小车位置到站点
        nextp = self.willpath[0]
        if abs(self.curr[0]-nextp[0])<self.x_step and abs(self.curr[1]-nextp[1])<self.x_step:
            self.curr = nextp
            return self.curr
        else:
            pass

    def change_target(self,target):
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
        return self.path


    def loop(self):
        pass

if __name__ == '__main__':
    graph = {
        '1': ['2', '4'],
        '2': ['1', '3'],
        '3': ['2', '4'],
        '4': ['1', '3']
    }
    car = Car(1,2,3,4,5,6)
    #path = car.find_a_path(graph,'1','3')
    #path1 = car.find_all_path(graph, '1', '3')
    #print(path1)
    car.curr = [300,800]
    site = car.get_near_site()
    print(site)
