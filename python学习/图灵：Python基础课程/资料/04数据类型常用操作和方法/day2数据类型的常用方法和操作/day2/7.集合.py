#一：基本使用:set
# 1 用途: 关系运算
# 2 定义方式: 在{}内用逗号分开个的多个值
# 3. 1.元素不能重复(定义不能这样写相同的)
#    2.集合里面的元素是无序
# s = {1,2,'大海'}
# # print(s)
# # print(type(s))
# # s1 = {'a','b','c'}
# # s2 = {'a','c','d'}
# #
# # print(s1 & s2) # # 拿2个集合相同的元素 shift + 7交集符合  交集
# # print(s1 | s2)# 拿2个集合所有的元素  并集
# # print(s1 - s2)# s1 去 抵消它们的交集 差集
#
# # 补充
# # 3 每一个值都必须是不可变类型
# # 错误示范
# # sss = {'aa',1,{'name':'dahai'}}
# # 增  add
# s.add('小海')
# # 集合是可变类型
# print(s)
# # 删 pop 看你的pycharm是怎样无序排列的，从第一个元素删除
# s.pop()
# print(s)
# # 指定删除remove
# # s.remove('大海')
# print(s)
# # 改
# # update
# s.update(['蓝海','紫海'])
# print(s)
#
# s1=list(s)
# s1[0]=8
# s=set(list(s1))
# print(type(s))
# print(s)

# 集合去重
# 局限性
#1、无法保证原数据类型的顺序
#2、当某一个数据中包含的多个值全部为不可变的类型时才能用集合去重
names =['dahai','xialuo','xishi','dahai','dahai','dahai']
s = set(names)
print(s)
l=list(s)
print(l)

# 要用for循环和if判断去重就可以保证顺序和对可变类型去重
# 总结
# 字符串，数字，布尔，复数 都是一个值，改变需要重新赋值，都是不可变类型
# 容器元组是不可变类型，字典，列表，集合都是可变类型