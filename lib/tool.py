# -*- coding: utf-8 -*-
import math,time
from lib.connector import Connector
con = Connector()

def get_car_position(name):
	rediskey = name+'_'+time.strftime('%Y%m%d-%H%M%S')
	pstr=con.hget(rediskey,'poistion')
	return convert_point_str(pstr)

def convert_point_str(pstr):
	p = pstr.replace('[', '')
	p = p.replace(']', '')
	p = p.split(',')
	p[0] = float(p[0])
	p[1] = float(p[1])
	return p
