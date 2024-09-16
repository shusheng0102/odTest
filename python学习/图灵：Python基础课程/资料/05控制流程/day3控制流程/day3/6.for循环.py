# # whlie遍历列表
# names = ['dahai','xialuo','guan','xishi']
# # #         0        1      2       3
# # i = 0
# # while i < len(names):
# #     # print(i)
# #     print(names[i])
# #     i += 1
# # # for循环遍历列表(按照索引顺序遍历的)
# # for n in names:
# #     print(n)
# # for循环遍历字典
# namess = {'name1':'dahai','name2':'xialuo','name3':'xishi'}
# # # 默认遍历key值
# # 所有的key
# for i in namess:
#     print(i)
# for i in namess.keys():
#     print(i)
# # # 遍历value值
# for i in namess:
#     # i是namess的key
#     print(namess[i])
#
# for i in namess.values():
#
#     print(i)
#
# # # 遍历键值对
# for i in namess.items():
#
#     print(i)
# # # for可以不依赖于索引取指，是一种通用的循环取值方式
# # # for的循环次数是由被循环对象包含值的个数决定的，而while的循环次数是由条件决定的
#
# # # range(起始索引,结束索引,步长)
# # # range(结束索引,步长) # 相当于起始索引是0
# # a = range(0,5)
# # print(a)
# # print(type(a))
# # # 它是一个迭代器
# # print(list(a))
# # # 为什么不直接变成列表，因为会浪费内存
# # print(range(0,100000000000000000000000))
# # # 一般和for循环连用, 循环一次取一次
# # #  range相当于母鸡下蛋 一次下一个  下了0 1 2 3 4 这5个鸡蛋
# # for i in range(0,5):
# #     print(i)
# # 步长
# for i in range(0,5,2):
#     print(i)
# # 虽然结果一样但是列表浪费内存
# #  列表相当于一筐鸡蛋 一次性就是 0 1 2 3 4 这5个鸡蛋
# for i in [0,1,2,3,4]:
#     print(i)
# for + break  或者 加continue
# names = ['dahai','xialuo','xishi','顾安','欢喜']
# for n in names:
#     if n == '顾安':
#         # continue
#         break
#     print(n)

# for+else 了解
#  else的代码会在for循环没有break打断的情况下最后运行
# for i in range(0,10):
#     if i == 4:
#         print('没有被break打断')
#         # break
#     print(i)
# else:
#     print('=============')

# for循环的嵌套
# 打印9*9乘法口诀表
# i是乘数，j是被乘数
# # print有一个参数end  默认是\n
# print(1,end='')
# print(1,end='')
# print(1,end='')
# 打印9*9乘法口诀表
# i是乘数，j是被乘数
# for i in range(1,10):
#     # 控制9行 #
#     # print('i是%s'%i)
#     for j in range(1,i+1):
#         # 控制每一行出现的公式的个数
#         # 第1次范围是range(1,2)    i  1      (1,2)    j  1  只循环了一次
#         # 第2次范围是range(1,3)    i  2      (1,3)    j  1  j  2  只循环了二次
#         # 第3次范围是range(1,4)    i  3      (1,4)    j  1  j  2   j  3 只循环了三次
#         # print('j是%s'%j)
#         print('%s*%s=%s'%(i,j,i*j),end=' ')
#     # print(end='\n')
#     # 等价于
#     print()
# 集合去重
# 局限性
#1、无法保证原数据类型的顺序
#2、当某一个数据中包含的多个值全部为不可变的类型时才能用集合去重
# names =['dahai','xialuo','xishi','dahai','dahai','dahai']
# s = set(names)
# print(s)
# l=list(s)
# print(l)

# 要用for循环和if判断去重就可以保证顺序和对可变类型去重
info =[
    {'name':'dahai','age':18},
    {'name':'xialuo','age':78},
    {'name':'xishi','age':8},
    {'name':'dahai','age':18},
    {'name':'dahai','age':18}
]
# set(info)
L = []
for i in info:
    # print(i)
    if i not in L:
        L.append(i)
info=L
print(info)