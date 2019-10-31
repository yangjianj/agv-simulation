print(1<2<3)

print(round(2/3,2))

list1 = [4,5,8,6,2,3,]
del(list1[2])
print(list1)
xx = list1[:]
print(xx)
print(id(list1))
print(id(xx))

xx = '[100.0, 900.0]'

xx = xx.replace('[','')
xx = xx.replace(']','')
xx = xx.split(',')

xx[0] = float(xx[0])
xx[1] = float(xx[1])
print(xx)

print(xx[0] == 100)

print(xx == [100,900])