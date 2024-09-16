# 文件名是spam.py,模块名则是spam
# 首次导入模块发生3件事
# 1. 会产生一个模块的名称空间
# 2. 执行文件spam.py,将执行过程中产生的名字都放到模块的名称空间中
# 3. 在当前执行文件的名称空间中拿到一个模块名,该名字指向模块的名称空间
# import spam
# # 之后的导入,都是直接引用第一次导入的成果,不会重新执行文件
# import spam
# import spam
# import spam
import spam
# money =100
# 在执行文件中访问模块名称空间中名字的语法:模块名.名字
# 指名道姓地跟spam要名字money,肯定不会与当前执行文件中的名字冲突
# print(spam.money)
# print(spam.read1)
# spam.read1()

# 总结import导入模块:在使用时必须加上前缀:模块名.
# 优点: 指名道姓地向某一个名称空间要名字,肯定不会与当前名称空间中的名字冲突
# 缺点: 但凡应用模块中的名字都需要加前缀,不够简洁
# 一行导入多个模块(不推荐)
# import spam,time
#
# # 可以为模块起别名
# import spam as sm
#
# print(sm.money)





