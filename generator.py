# -*- coding: utf-8 -*-
from lib.connector import Connector

def read_data(file):
    result = []
    with open(file,'r') as f:
        while True:
            re = f.readline().replace('\n','')
            if re:
                result.append(re)
            else:
                break
    return result

def save_data(data):
    index = 0
    for item in data:
        key = 't'+str(index)
        Connector().set(key,item)
        index = index+1

def get_data(robot):
    pass

def compute(curr,target):
    if curr[0] == target[0]:
        pass
    elif curr[1] == curr[1]:
        pass



if __name__ == '__main__':
    #datalist = read_data('test_HK.txt')
    #save_data(datalist)
    for i in range(5,21,3):
        print(i)