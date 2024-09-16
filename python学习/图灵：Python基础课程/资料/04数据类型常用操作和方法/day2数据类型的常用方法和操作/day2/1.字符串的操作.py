#字符类型：str
#作用：记录描述性质的数据，比如人的名字、性别、家庭地址、公司简介
#定义：在引号内按照从左到右的顺序依次包含一个个字符，引号可以是单引号、双引号、三引号
# name = '大海1'
# name1 = "大海2"
# name2 = '''大海3'''
# print(name,name1,name2)
# # 字符串里面要有引号
# print('my name is "dahai"')
# print("my name is 'dahai'")
#
# # 字符串还可以加起来
# print('大海'+'dsb')
# print('大海'*10)

# name4 = 'abcdef'
# 索引从0开始，现实中书本的页码从1开始
# 取出第一个英文字符
# print(name4[0])
# print(name4[1])
# print(name4[-1])
# # 取出第一个中文字符
# print(name[0])
#字符串不能通过索引修改
# name4[0] = 'g'
# print(name4)
msg = 'hello world'
#      012345
print(msg[0])
print(msg[-1])
#2、切片(顾头不顾尾，步长)查找字符串当中的一段值 [起始值:终止值:步长]
#   相当于切黄瓜 一节一节
print(msg[0:5])
print(msg[0:5:1])
# 提取不会改变原值
print(msg)
print(msg[0:5:2])
# 了解
print(msg[::])
print(msg[0::])
print(msg[0::2])
# 步长是负数
print(msg[::-1])
print(msg[10::-1])
print(msg[10:5:-1])
#3、长度len方法 可以计算长度
print(len(msg))
#4、成员运算in和not in: 判断一个子字符串是否存在于一个大的字符串中
# 返回布尔类型 True False
print('dahai' in 'dahai is dsb')
print('xialuo' not in 'dahai is dsb')

# 字符串的方法
# 增
# 字符串拼接
print('dahai'+'dsb')

# format
print('my name is {}'.format('dahai'))
print('my name is {1} my age is {0}'.format(18,'dahai'))
print('my name is {name} my age is {age}'.format(age=18,name='dahai'))
# join
str1 = '真正的勇士'
str2 = '敢于直面惨淡的人生'
str3 = '敢于正视淋漓的鲜血'
# 可以把列表里面的元素组合成字符串
print(''.join([str1,str2,str3]))
print(','.join([str1,str2,str3]))
print('哇塞'.join([str1,str2,str3]))
# 空格也属于字符
print('  '.join([str1,str2,str3]))
# 删
# name1 = 'dahai'
#
# del name1
# print(name1)
# 改
#1、 字符串字母变大写和变小写 lower,upper
msg1 = 'abc'
msg2=msg1.upper()
# 原值
print(msg1)
print(id(msg1))
# 修改后的值
print(msg2)
print(id(msg2))
# 注意字符串进行改变需要重新赋值，所以它也是不可变类型，它的原值的变量不会变，
# 只是做了一个方法改变了它的值，重新赋值给一个新的变量

# 2把第一个字母转换成大写 capitalize
letter = 'abcd'
print(letter.capitalize())
#3 每个单词的首字母进行大写转换 title
letter_msg = 'hello world'
print(letter_msg.title())

# 4把字符串切分成列表  split 默认空格字符切分
msgg = 'hello world python'
# 默认以空格切分
print(msgg.split())
# 可以切分你想要的字符 比如*
msgg1 = 'hello*world*python'
print(msgg1.split('*'))
#切分split的作用:针对按照某种分隔符组织的字符串，可以用split将其切分成列表，进而进行取值
msggg = 'root:123456'
print(msggg[0:4])
print(msggg.split(':')[0])
print(msggg.split(':')[1])
#5、去掉字符串左右两边的字符strip不写默认是空格字符，不管中间的其他的字符
user = '      dahai      '
print(user)
print(user.strip())
# name = input('请输入用户名').strip()
# print(name)

# 了解
# center,ljust,rjust 多余添加自己想要的字符
print('dahai'.center(11,'*'))
print('dahai'.ljust(11,'*'))
print('dahai'.rjust(11,'*'))
# 查
#1、find,index
# 查找子字符串在大字符串的那个位置（起始索引）
msga = 'hello dahai is dsb dahai'
print(msga.find('dahai'))
# 没找到会返回-1
print(msga.find('ddddd'))


print(msga.index('dahai'))
# 没找到会报错
# print(msga.index('ddddd'))
# 统计一个子字符串在大字符串中出现的次数 count
print(msga.count('dahai'))

# 判断一个字符串里的数据是不是都是数字 isdigit # 返回布尔值
num = '1818'
num1 = '18aaa18'
aaaa = 'aaa'
print(num.isdigit())
print(num1.isdigit())
# print(type(input('>>>')))
# 判断每个元素是不是都是字母 isalpha
print(aaaa.isalpha())
print(num.isalpha())
print(num1.isalpha())
# 比较开头的元素是否相同 startswith
# 比较结尾的元素是否相同 endswith
# 返回布尔类型
mm = 'dahai xialuo'
print(mm.startswith('dahai'))
print(mm.endswith('uo'))
# 判断字符串中的值是否全是小写的 islower
# 判断字符串中的值是否全是大写的 isupper
letter2 = 'ABC'
letter3 = 'abc'
letter4 = 'aAbc'
print(letter2.isupper())
print(letter3.isupper())
print(letter4.isupper())
print(letter2.islower())
print(letter3.islower())
print(letter4.islower())
# 字符串的转义
# 字符串的转义   加了 \  字符不再表示它本身的含义
# 常用的  \n  \t
# \n 换行符
print('hello \n python')
# \n 横向换行符 相当于一个tab
print('hello \t python')

print(r'hello \n python \t')
print('hello \\n python \\t')







