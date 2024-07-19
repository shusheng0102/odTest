'''
# 程序中经常会有这样场景：要求用户输入信息，然后打印成固定的格式
#
#     比如要求用户输入用户名和年龄，然后打印如下格式：
#
#     My name is xxx，my age is xxx.
这就用到了占位符，如：%s、%d
'''
# name = input('输入名字')
# # 一个值的话直接放到%后面
# print('my name is %s'%name)
# %s 占位符 可以接受所有的数据类型 %d只能接受数字 有局限性
# 多个值的话直接放到%后面要有括号
print('My name is %s，my age is %d'%('dahai',18))
