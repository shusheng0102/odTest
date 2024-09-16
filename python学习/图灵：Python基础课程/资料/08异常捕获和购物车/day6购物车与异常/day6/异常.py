'''
1.异常
    异常是错误发生的信号,一旦程序出错就会产生一个异常,如果该异常
    没有被应用程序处理,那么该异常就会抛出来,程序的执行也随之终止
    异常包含三个部分:
         1.异常的追踪信息  File "D:/python代码2/day6/异常.py", line 9, in <module>
        2.异常的类型  NameError
        3. 异常的信息   name 'a' is not defined
    错误分为两大类:
        1. 语法上的错误:在程序运行前就应该立即修正  这个好避免
        2. 逻辑上的错误:比如：字典没有key，你非要取key，
                            列表没有索引
                            变量没有名字  这些不好避免
2.为何要异常处理
    避免程序因为异常而崩溃,所以在应用程序中应该对异常进行处理,从而增强程序的健壮性
3. 如何异常处理
try:
    代码1
    代码2
    代码3
    ......
except NameError:
    当抛出的异常是NameError时执行的子代码块
except ....:
    pass
else:
    pass
finally:
    pass
'''
# 常见异常
# NameError
# print(1+'1')# TypeError
# d = {'x':1,'y':2}
# d['z'] # KeyError
# L = [1,2]
# L[3] # IndexError
# 异常处理的单分支
# try:
#     a = 1
# except NameError as e:
#     print('兄弟请检查一些你的代码')
#     print(e)
# else:
#     # 程序没有抛出异常的时候执行
#     print('代码正确')
# finally:
#     # 不管有错没错 一定会执行的部分
#     print('完成了异常捕获')

# 异常处理的多分支
# try:
#     a
#     # 完成了捕获后面的代码不会走了
#     print('========1')
#     print('========1')
#     print('========1')
#     l = [1,2]
#     l[3]
# except IndexError as e:
#     print(e)
# except NameError as e:
#     print(e)
# else:
#     # 程序没有抛出异常的时候执行
#     print('代码正确')
# finally:
#     # 不管有错没错 一定会执行的部分
#     print('完成了异常捕获')


# 合并一下
# try:
#     a
#     # 完成了捕获后面的代码不会走了
#     print('========1')
#     print('========1')
#     print('========1')
#     l = [1,2]
#     l[3]
# except (NameError,IndexError) as e:
#     print(e)
# else:
#     # 程序没有抛出异常的时候执行
#     print('代码正确')
# finally:
#     # 不管有错没错 一定会执行的部分
#     print('完成了异常捕获')


# 万能捕获

# try:
#     # a
#     d = {'x':1,'y':2}
#     d['z'] # KeyError
#     # 完成了捕获后面的代码不会走了
#     print('========1')
#     print('========1')
#     print('========1')
#     l = [1,2]
#     l[3]
# except Exception as e:
#     print(e)
# else:
#     # 程序没有抛出异常的时候执行
#     print('代码正确')
# finally:
#     # 不管有错没错 一定会执行的部分
#     print('完成了异常捕获')

# 了解
# 断言

# 自定义异常
# l = [1,2,3,4]
# # # 4
# # # if len(l) != 5:
# # #     raise TypeError('列表的长度必须为5,这个是我的规则')
# # # 列表的长度必须为5,这个是我的规则
# assert len(l) == 5














