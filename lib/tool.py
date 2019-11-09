# -*- coding: utf-8 -*-
import math,time,copy,json
import logging
from lib.connector import Connector
import config.config as config
con = Connector()


# 找出一条路径
def find_a_path(graph, start, end, path=[]):
	path = path + [start]
	if start == end:
		return path
	for node in graph[start]:
		if node not in path:
			newpath = find_a_path(graph, node, end, path)
			if newpath:
				return newpath
	return None

def find_all_path(graph, start, end, path=[]):
	path = path + [start]
	if start == end:
		return [path]
	paths = []  # 存储所有路径
	for node in graph[start]:
		if node not in path:
			newpaths = find_all_path(graph, node, end, path)
			for newpath in newpaths:
				paths.append(newpath)
	return paths

def find_shartest_path(graph, start, end, path=[]):
	#返回最短路径列表
	path = path + [start]
	if start == end:
		return [path]
	shortestPath = []
	for node in graph[start]:
		if node not in path:
			newpath = find_shartest_path(graph, node, end, path)
			if newpath:
				if not shortestPath or len(newpath[0]) < len(shortestPath[0]):
					shortestPath = newpath
				elif shortestPath and len(newpath[0]) == len(shortestPath[0]):
					shortestPath.append(newpath[0])
	return shortestPath

def subscribe(topic):
	return con.subscribe(topic)

def publish(topic, message):
	return con.publish(topic, message)

def three_point_online(p1, p2, p3):
	#判断三点按此顺序在一条直线上线
	if p1[0] != 0:
		if round(p1[1]/p1[0],5) == round(p2[1]/p2[0]) == round(p3[1]/p3[0],5) and p1[0]<=p2[0]<=p3[0]:
			return True
	elif round(p1[0]/p1[1],5) == round(p2[0]/p2[1]) == round(p3[0]/p3[1],5) and p1[1]<=p2[1]<=p3[1]:
		return True

def three_point_like_line(p1,p2,p3,offset):
	#找出离当前点最近的两个点，并且当前点在所找两点的直线之间,允许偏移offset
	#通过三者间距离判断
	distance = []
	for p in [p1,p2,p3]:
		if p == p1:
			continue
		elif p == p3:
			x_dis = p[0] - p2[0]
			y_dis = p[1] - p2[1]
			distance.append(math.sqrt((x_dis ** 2) + (y_dis ** 2)))
		x_dis = p[0] - p1[0]
		y_dis = p[1] - p1[1]
		distance.append(math.sqrt((x_dis ** 2) + (y_dis ** 2)))
	real = distance[0]+distance[1] - distance[2]
	if distance[0]+distance[1] - distance[2] <= offset:
		return True

def build_line(sgraph,path=[]):
	# 根据图生成line
	graph = copy.deepcopy(sgraph)
	if path == []:
		start = list(graph.keys())[0]
		path.append(start)
	key = path[-1]
	if graph[key] == []:
		index = 0
		while index <= len(graph):  #将graph中剩余元素准确插入path
			for i in graph:
				if len(graph[i]) == 0:
					index = index +1
					if index == len(graph):
						return path
				else:
					try:
						a = path.index(i)
						path.insert(a+1,graph[i][0])
						path.insert(a+2,i)
						graph[graph[i][0]].remove(i)
						del graph[i][0]
						index = 0
					except:
						next
	else:
		path.append(graph[key][0])
		graph[graph[key][0]].remove(key)
		del graph[key][0]
		build_line(graph, path)
	return path

def convert_xystr_xylist(pstr):
	p = pstr.replace('[', '')
	p = p.replace(']', '')
	p = p.split(',')
	p[0] = float(p[0])
	p[1] = float(p[1])
	return p

def log_info(msg,file):
	logger = logging.getLogger()
	logger.setLevel(level=logging.INFO)
	handler = logging.FileHandler(file)
	formatter = logging.Formatter('%(asctime)s -%(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.info(msg)

def log_error(msg,file):
	logger = logging.getLogger()
	handler = logging.FileHandler(file)
	formatter = logging.Formatter('%(asctime)s -%(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.error(msg)



if __name__ == '__main__':
	print(find_shartest_path(config.cars[1]['graph'], '2', '5', path=[]))