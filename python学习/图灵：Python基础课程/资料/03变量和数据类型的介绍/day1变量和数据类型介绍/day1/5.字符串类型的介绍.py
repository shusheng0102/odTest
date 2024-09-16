#字符类型：str
#作用：记录描述性质的数据，比如人的名字、性别、家庭地址、公司简介
#定义：在引号内按照从左到右的顺序依次包含一个个字符，引号可以是单引号、双引号、三引号
name = '大海1'
name1 = "大海2"
name2 = '''大海3'''
print(name,name1,name2)
# 字符串里面要有引号
print('my name is "dahai"')
print("my name is 'dahai'")

# 字符串还可以加起来
print('大海'+'dsb')
print('大海'*10)

name4 = 'abcdef'
# 索引从0开始，现实中书本的页码从1开始
# 取出第一个英文字符
print(name4[0])
print(name4[1])
print(name4[-1])
# 取出第一个中文字符
print(name[0])



