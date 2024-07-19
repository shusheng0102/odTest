# 常用的内置函数
#1 已经写好的一些函数   美观，强大
#
# 绝对值
# print(abs(-5))
# print(abs(5))
# all(可迭代对象)# 返回的是布尔值
#  可迭代对象里面的值全部为真才是真,其余为假
#  可迭代对象是空则为真
# print(all([1,'',None]))
# print(all([1,'aaa',2]))
# print(all([]))
# # any(可迭代对象)
# #  可迭代对象里面的值全部为假才是假，其余为真
# #  可迭代对象是空则为假
# print(any([0,'',None,1]))
# print(any([0,'',None,[]]))
# print(any([]))
# # 求最大值
# a = [1,2,4,5,7]
# print(max(a))
# # 求最小值
# print(min(a))
# # 求和
# print(sum(a))
# ascll 英文的字符编码
# ord() 可以把字符转换成编码
# chr() 可以把编码转换成字符
# print(ord('a'))
# print(chr(97))
# print(ord('A'))
# print(chr(65))
# 拉链函数 zip
# 序列类型进行拉链
# t1 = ['a','b','c','d','e']
t1 = ('a','b','c','d','e')
# t1 = 'abcde'
# e 被抛弃
t2 = [1,2,3,4]
# 通过索引
print(list(zip(t1,t2)))
print(dict(zip(t1,t2)))
# 介绍 exec 函数   可以执行字符串里面的代码 支持python语法
exec('print(1)')

exec('''
for i in range(0,10):
    print(i)
''')

