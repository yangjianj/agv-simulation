import time,copy,re
from datetime import datetime
print(1<2<3)

print(round(2/3,2))
print(datetime.now().strftime('%Y%m%d-%H%M%S%f'))
print(time.strftime('%Y%m%d-%H%M%S%f'))

x = {
	'4': ['1', '5'],
	'3': ['2', '5','6'],
	'7':['2'],
	'1': ['2', '4', '5'],
	'2': ['1', '3','5','7'],
	'5': ['3', '4', '1','2'],
	'6': ['3']
		}
print(list(x.keys())[0])
y = x.copy()
print(id(x),id(y))
print(len(x))

def build_line(sgraph,path=[]):
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

print(111111111111)
y1={
			'1': ['2', '4', '5'],
			'2': ['1', '3'],
			'3': ['2', '5'],
			'4': ['1', '5'],
			'5': ['3', '4', '1']
		}

y2= {
			'1': ['2', '4'],
			'2': ['1', '3'],
			'3': ['2', '4'],
			'4': ['1', '5','3'],
			'5': ['4']
		}
for i in (y1,y2):
	print(1111111111)
	print(build_line(i,path=[]))


t = time.time()
print(t)
print(time.localtime(t))
print(time.localtime(t-1))

print(float('12.36'))
xx = '[100,200]'
print(type(eval(xx)) == type([]))

ret = re.match('^\[\]$',xx)
print(ret)