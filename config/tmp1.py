import time,redis,json,argparse

r = redis.Redis(host='127.0.0.1',port=6379,db=0)

r.publish('topic1','123456'+str(time.time()))

def find_shartest_path(graph, start, end, path=[]):
	path = path + [start]
	if start == end:
		return path
	shortestPath = []
	for node in graph[start]:
		if node not in path:
			newpath = find_shartest_path(graph, node, end, path)
			if newpath:
				if not shortestPath or len(newpath) < len(shortestPath):
					shortestPath = newpath
	return shortestPath

graph = {
        '1': ['2', '4', '5'],
        '2': ['1', '3'],
        '3': ['2', '5'],
        '4': ['1', '5'],
        '5': ['3', '4', '1']
    }
sites = {
        '1': [100, 900],
        '2': [300, 900],
        '3': [300, 700],
        '4': [100, 700],
        '5': [200, 500]
    }

print(find_shartest_path(graph,'5','2',[]))

parser = argparse.ArgumentParser()
parser.add_argument('-e',help='eeeeee')
parser.add_argument('-x',help='xxx',action='store_true')
args = parser.parse_args()
print(args.e)

