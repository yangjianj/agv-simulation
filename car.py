class Car():
    def __init__(self,name,curr,target,site,speed):
        self.curr = curr   #[0,0]
        self.target = target    #[100,100]
        self.site = site
        site = [
            {'1':[100, 900]},{'2':[300, 900]},{'3':[300, 700]},{'4':[100, 700]},
        ]
        graph = {
            '1':['2','4'],
            '2':['1','3'],
            '3':['2','4'],
            '4':['1','3']
        }
        self.name = name
        self.speed = speed  #10
        self.path = []

    def change_target(self,target):
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

    def get_nearest_path(self):
        pass

    def find_path(self,graph,start,end,path=[]):
        path = path + [start]
        if start == end:
            return path
        for node in graph[start]:
            if node not in path:
                newpath = self.find_path(graph, node, end, path)
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
                print(1111)
                print(newpaths)
                for newpath in newpaths:
                    print(222)
                    print(paths)
                    paths.append(newpath)
                    print(paths)
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

    def loop(self):
        pass

if __name__ == '__main__':
    graph = {
        '1': ['2', '4'],
        '2': ['1', '3'],
        '3': ['2', '4'],
        '4': ['1', '3']
    }
    car = Car(1,2,3,4,5)
    path = car.find_path(graph,'1','3')
    path1 = car.find_all_path(graph, '1', '3')
    print(path1)
