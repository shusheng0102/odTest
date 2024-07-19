# asd


**graph** TD
start**(开始处理请求)**--> check_data_size**[检查请求数据大小]**
check_data_size **-->**|大于等于80且小于等于100| direct_calculate**[直接计算]**
check_data_size **-->**|小于80| enqueue**[放入队列]**
check_data_size **-->** check_queue**[检查队列是否有足够的数据合并]**
enqueue **-->** wait**[等待1ms]**
wait **-->** check_queue
check_queue **-->**|可以合并| merge_requests**[合并请求]**
check_queue **-->**|不能合并| calculate_timeout**[超时单独计算]**
merge_requests **-->** merge_calculate**[合并后计算]**
calculate_timeout **-->** single_calculate**[单独计算]**
direct_calculate **-->**|计算结果| send_result**[发送结果]**
merge_calculate **-->**|计算结果| enqueue_result**[放入结果队列]**
single_calculate **-->**|计算结果| enqueue_result
enqueue_result **-->** monitor_results**[监听结果队列]**
monitor_results **-->**|结果就绪| send_result
send_result **-->** end**(请求处理结束)**

# day3.控制流程

## 1.if判断

```
#语法1：
# if 条件:
#     代码体
#     code1
#     code2
#     code3
#     ....
# 语法记忆方法
#   if+空格+条件+冒号
#   tab缩进代码体
#   tab缩进代码体
#   tab缩进代码体
# 键盘Q 左边tab
#  代表电脑需要一个条件进行判断  冒号可以理解成代表计算机要说话了
#  那么通过tab横向换行确定要说的话
# tag = False
# if tag:
#     print('条件满足')
#     print('条件满足')
#     print('条件满足')
#语法2：
# if 条件:
#     代码体
#     code1
#     code2
#     code3
#     ....
#else:
#     代码体
#     code1
#     code2
#     code3
# tag = 1 == 3
# if tag:
#     print('条件满足')
#     print('条件满足')
#     print('条件满足')
# # 其他
# else:
# # tab 右边缩减  shift + tab 左边缩进
#     print('条件不满足')
#     print('条件不满足')
#语法3：多分枝
# 强调：if的多分枝=但凡有一个条件成立，就不会再往下判断其他条件了
# elif可以有无限个
# if 条件1:
#     code1
#     code2
#     code3
#     ....
# elif 条件2:
#     code1
#     code2
#     code3
#     ....
# elif 条件3:
#     code1
#     code2
#     code3
#     ....
# ........
# else:
#     code1
#     code2
#     code3
#     ....

# 优先级if最高  elif 依次从上往下 else
# 注意必须要有if
# 如果：成绩>=90，那么：优秀
#
# 如果成绩>=80且<90,那么：良好
#
# 如果成绩>=70且<80,那么：普通
#
# 其他情况：很差

# score = int(input('>>>'))
# if score >= 90:
#     print('优秀')
# elif score >= 80:
#     print('良好')
# elif score >= 70:
#     print('普通')
# elif score <70:
#     print('很差')
# 等价
# else:
#     print('很差')
# if 嵌套
# 语法
# if 条件:
#     code1
#     code2
#     code3
#     if 条件:
#           code1
#           code2
#           code3
#     else:
#           code1
#           code2
#           code3
# else:
#     code1
#     code2
#     code3
#     if 条件:
#           code1
#           code2
#           code3
#     else:
#           code1
#           code2
#           code3
cls = 'human'
sex = 'female'
age = 20
# 条件都要满足
if cls =='human' and sex == 'female' and age > 18 and age < 26:
    print('开始表白..... 以下省略一万字')
    is_success = input('女孩输入我愿意')
    # 嵌套里面当然也是可以用if 语法 1 2 3
    if is_success == '我愿意':
        print('在一起')
    else:
        print('我逗你玩呢....')
else:
    print('姐姐好')




```

## 2.逻辑运算符

```
#逻辑运算and or not
# and 与:连接左右两个条件,只有在两个条件同时成立的情况下最终结果才为True
# 快速判断方法
# 全部都是and的情况下，如果判断到位假后面都是and就没必要看了，就是假
# 要求全部都是真才是真
name = 'dahai'
num = 20
print(num > 18 and 1>3 and name == 'dahai' and num < 26)
print(num > 18 and 3>1 and name == 'dahai' and num < 26)

# or 或:连接左右两个条件,但凡有一个条件成立最终结果就为True
# 快速判断方法
# 全部都是or的情况下，如果判断到位真后面都是or就没必要看了，就是真
# 全是假才是假
print( 1>3or 1 ==1 or 'x'== 'y' or 2 > 4)
# not 非
print(not 1 > 3)
'''
原理为：
(1) not的优先级最高，就是把紧跟其后的那个条件结果取反，所以not与紧跟其后的条件不可分割

(2) 如果语句中全部是用and连接，或者全部用or连接，那么按照从左到右的顺序依次计算即可

(3) 如果语句中既有and也有or，那么先用括号把and的左右两个条件给括起来，然后再进行运算
'''
print(not 3 > 1 or 3 >1)
#  是先判断not 3>1  而不是 3>1 or 3>1
# not 相当于小学学的乘除法  ，and和or相当于加减法
res=not False and True or False or False or True
# #2、最好使用括号来区别优先级，这样别人容易读懂你的代码
res1 =  (3>4 and 4>3) or (1==3 and ('x'=='x' or 3>3))
print(res1)
```

## 3.if并列

```
# 如果：成绩>=90，那么：优秀
#
# 如果成绩>=80且<90,那么：良好
#
# 如果成绩>=70且<80,那么：普通
#
# 其他情况：很差
score = int(input('>>>'))
if score >= 90:
    print('优秀')
if  90>score >= 80:
    print('良好')
if 80>score >= 70:
    print('普通')
if score < 70:
    print('很差')
# elif 与if并列的区别
# if并列是每个if都是独立的  也就是说每一个if条件 是独立的
# 而elif的条件  是在上个if 或者 上一个elif 不满足的条件下执行的条件

```

## 4.whlie循环

```
'''
1 什么是循环
    循环就是一个重复的过程

2 为何要有循环
    人可以重复的去做某一件事
    程序中必须有一种机制能够控制计算机像人一样重复地去做某一件事

3 如何用循环
'''
# 语法
# while 条件:
#     code1
#     code2
#     code3
# 条件为满足  一直循环
# while + True的情况
# while True:
#     print('1111')
#     print('2222')
# 在登录的情况需要循环
# db_user = 'dahai'
# db_pwd = '123'
# while 1:
#     input_user = input('请输入用户名')
#     input_pwd = input('请输入密码')
#     if input_user == db_user and input_pwd == db_pwd:
#         print('登录成功')
#     else:
#         print('登录失败')
# while + break: break代表结束本层循环
# db_user = 'dahai'
# db_pwd = '123'
# while True:
#     input_user = input('请输入用户名')
#     input_pwd = input('请输入密码')
#     if input_user == db_user and input_pwd == db_pwd:
#         print('登录成功')
#         break
#     else:
#         print('登录失败')

# while + 一个条件范围 不满足这个条件范围就会跳出循环
# start = 0
# while start < 8:
#     start += 1
#     print(start)

# while+continue:continue代表结束本次循环
# （本次循环continue之后的代码不在运行），直接进入下一次循环
start = 0
while start < 8:
    start += 1
    if start == 4:
        continue
    print(start)
    # continue
# 强调：continue一定不要作为循环体的最后一步代码
# 了解
# while + else # break

n = 0
while n < 6:
    n+=1
    if n == 6:
        break
    print(n)
else:
    # else的代码会在while循环没有break打断的情况下最后运行
    print('===================')
print('----------------')


```

## 5.if与whlie结合

```
# 登录取款程序
# 理解while嵌套
user = '大海'
pwd = 123
balance = 5000
tag = True
while True:
    while tag:
        user1 = input('输入用户名')
        if user1 != user:
            print('你输入的用户名有错误，请重新输入')
            continue
        pwd1 = int(input('请输入密码'))
        if pwd == pwd1:
            print('登录成功')
            break
            # 跳出本层循环 ，也就是说这一层while tag循环直接结束
            # 虽然跳出了while tag:
            # 外面的while True还是又会进入while tag
        else:
            print('输入密码错误')
    # 目的只是为了不进入里面的循环
    # 下面我要写取款程序
    tag = False
    # print('走后面取款的代码')
    money = int(input('输入你的取款金额'))
    if balance > money:
        balance = balance - money
        print('恭喜你取走了%s'%money)
        print('还剩%s'%balance)
        break
    else:
        print('余额不足')
```

## 6.for循环

```
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
```

## 断点

```
# 断点
# 打断点
# 启动断点 鼠标右键
# ctrl + F5 重启程序
# ctrl + F2 停止
# F9 绿色的三角形是调到下一个断点
# F8 蓝色朝下的箭头是单步走
# Alt + F9 移动到光标处
```
