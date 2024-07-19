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

