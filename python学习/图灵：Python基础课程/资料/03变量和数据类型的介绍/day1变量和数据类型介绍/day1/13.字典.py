'''
#字典类型:dict
#作用:记录多个key:value值,优势是每一个值value都有其对应关系/映射关系key,而key对value有描述性的功能
#定义: 在{}内用逗号分隔开多个key:value元素,其中value可以是任意的数据类型,而key通常应该是字符串类型
'''
info = {'name':'大海','age':18}
# name 相当于新华字典里面的偏旁部首
print(info['name'])
print(info['age'])
print(info)
# 列表和字典的区别
# 列表是依靠索引
# 字典是依靠键值对 # key描述性的信息