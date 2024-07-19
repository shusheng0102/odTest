'''
#字典类型:dict
#作用:记录多个key:value值,优势是每一个值value都有其对应关系/映射关系key,而key对value有描述性的功能
#定义: 在{}内用逗号分隔开多个key:value元素,其中value可以是任意的数据类型,而key通常应该是字符串类型
'''
info = {'name':'大海','age':18}
# name 相当于新华字典里面的偏旁部首
# print(info['name'])
# print(info['age'])
# print(info)
# 列表和字典的区别
# 列表是依靠索引
# 字典是依靠键值对 # key描述性的信息

# 生成字典的方式2
# dic = dict(x=1,y=2)
# print(dic)
# 字典的增加操作
print(info)
# 直接赋值一个不存在的key和value
info['addr']='changsha'
print(info)
# 字典我在添加的时候也没有进行重新赋值，所以字典是可变类型
# 列表却不行,添加和修改必须是操作存在的索引
# 字典 len 查看的是键值对的个数
print(len(info))

# 成员运算in和not in:字典的成员运算判断的是key 返回值是布尔类型
print('name'in info)
print('大海' in info)
# 删
# clear   清空字典
# info.clear()
# print(info)
# del
# del info['name']
# print(info)
# 不存在的key会报错
# del  info['xxx']
# print(info)

# # pop 删除 返回值是value   实际上就是拿走了字典的value
# res = info.pop('addr')
# print(info)
# print(res)
# # 不存在的key会报错
# info.pop('xxx')
# # popitem 最后一对键值对删除 字典无序 返回的是一个元组
# res1=info.popitem()
# print(res1)
# print(info)
# # 改
print(info)
info['name']='红海'
print(info)
info.update({'name':'xiaohai'})
print(info)
# setdefault
# 有则不动/返回原值,无则添加/返回新值
# 字典中已经存在key则不修改,返回已经存在的key对应的value
res=info.setdefault('name','xxx')
print(info)
print(res)
# 字典不存在key则添加"sex":"male",返回新的value
res2 = info.setdefault('sex','male')
print(info)
print(res2)

# 查
# print(info['name'])
# # 查一个不存在的key会报错
# print(info['xxx'])

# print(info.get('name'))
# # 没有key就返回None，不会报错
# print(info.get('xxxx'))

# 取出所有的key
print(list(info.keys()))
# 取出所有的值
print(list(info.values()))
# 取出所有的键值对
print(list(info.items()))







