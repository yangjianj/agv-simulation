# -*- coding: utf-8 -*-
import math,time
from lib.connector import Connector
con = Connector()

def get_car_position(name):
	rediskey = name+'_'+time.strftime('%Y%m%d-%H%M%S')
	pstr=con.hget(rediskey,'poistion')
	if pstr:
		return convert_point_str(pstr)
	else:
		return None

def set_car_position(name,position):
	rediskey = name + '_' + time.strftime('%Y%m%d-%H%M%S')
	con.hset(rediskey,'poistion',position)

def convert_point_str(pstr):
	p = pstr.replace('[', '')
	p = p.replace(']', '')
	p = p.split(',')
	p[0] = float(p[0])
	p[1] = float(p[1])
	return p


def three_point_online(p1, p2, p3):
	#判断三点按此顺序在一条直线上线
	if p3[1] != p1[1]:
		if (p2[0] - p1[0]) / (p2[1] - p1[1]) == (p3[0] - p3[0]) / (p3[1] - p1[1]) and (p2[0] - p1[0]) * (
				p2[0] - p3[0]) <= 0:
			return True
	else:
		if p2[1] == p1[1] and (p2[0] - p1[0]) * (p2[0] - p3[0]) <= 0:
			return True

def three_point_like_line(p1,p2,p3,offset):
	#找出离当前点最近的两个点，并且当前点在所找两点的直线之间,允许偏移offset
	#通过三者间距离判断
	distance = []
	for p in [p1,p2,p3]:
		if p == p1:
			next
		elif p == p3:
			x_dis = p[0] - p2[0]
			y_dis = p[1] - p2[1]
			distance.append(math.sqrt((x_dis ** 2) + (y_dis ** 2)))
		x_dis = p[0] - p1[0]
		y_dis = p[1] - p1[1]
		distance.append(math.sqrt((x_dis ** 2) + (y_dis ** 2)))
	if distance[0]+distance[2] - distance[1] <= offset:
		return True

if __name__ == '__main__':
	print(three_point_like_line([10,0],[20,0],[30,1],0.005))