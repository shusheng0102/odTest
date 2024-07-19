# mongodb与python操作mongdb

## 1.mongodb_test

```
'''
mongodb
可以分散存储到多台服务器上面，分布式存储
利用位置服务器去定位存储信息

数据处理：数据是存储在硬盘上的，只不过需要经常读取的数据会被加载到内存中，将数据存储在物理内存中，从而达到高速读写。

MongoDB是面向文档的数据库，不是关系型数据库。将数据库存储为一个文档，文档类似与json格式,没有表结构，想加就加
适合场景：事件的记录，内容管理或者博客平台等等。(经常变化的数据)
    记录日志
        可以放到mongodb
            {
            时间:2021.9.22
            地点:长沙
            状态:正常
            }
        游戏场景
        用户装备信息，属性信息
            {
            头部:xxx头盔
            上衣:xxx a
            裤子:xxx b
            }

进入mongodb
mongo
退出
exit
mongodb的库
    查看所有数据库
        库里面必须有数据才能查看到
        只是创建了库是隐式创建，只有库里面有数据才会真正意义的存在
        show dbs
    切换/创建数据库
        use mydb2
    查看所在库
        db
    删除库
        db.dropDatabase()
mongodb的集合操作
    创建集合
        db.createCollection('stu')
    查看当前数据库的集合
        show collections
    删除集合
        db.stu.drop()
mongodb的文档操作
    增：
        语法
            db.集合名称.insert(文档)
        实例
            不插入id自动生成id
                db.stu.insert({name:'xiaoming',age:18})
            自己插入id
                db.stu.insert({'_id':3,name:'xiaoming',age:18})
        插入多条
            语法
                db.集合名称.insert([
                        一条文档,
                        二条文档,
                        三条文档
                        ])
            实例
                db.stu.insert([
                    {name:'xiaobai','sex':'男',age:18},
                    {name:'xiaohei','sex':'女',age:16},
                    {name:'xiaohong','sex':'男',age:18}
                    ])
    查：
        整体查询
            语法
                一般
                    db.集合名称.find()
                美观查询
                    db.集合名称.find().pretty()
        指定查询
            语法
                db.stu.find({某个文档})
            实例
                db.stu.find({name:'xiaoming'})
        筛选
            语法
                db.stu.find({某个文档的key:values为1代表显示/values为0代表不显示})
            实例
                db.stu.find({name:'xiaoming'},{age:1})
                db.stu.find({name:'xiaoming'},{age:0})
        逻辑运算符
            and 与
            or 或
        比较运算符
            gt 大于
            lt 小于
            gte 大于或等于
            lte 小于或等于
            ne 不等于
        语法
                {$and:[包含多个条件]}
                {$or:[包含多个条件]}
        实例
            db.stu.find({$and:[{sex:'女'},{age:16}]})
            查询条件1或者条件2的数据
            条件1：性别女并且年龄16岁
            条件2：性别男并且年龄大于或等于18岁

            db.stu.find({$or:
                [{$and:[{sex:'女'},{age:16}]},
                {$and:[{sex:'男'},{age:{$gte:18}}]}]
            })
    改：
        只会修改一条数据 并且其他字段也没有了
            db.stu.update({name:'xiaohong'},{name:'xianghonghong'})
            age:18被去掉了
        只会修改一条数据 并且其他字段保留
            db.stu.update({name:'xiaobai'},{$set:{age:66}})
        修改多条数据 并且其他字段保留
            db.stu.update({name:'xiaobai'},{$set:{age:66}},{multi:true})
    删：
        只删除符合条件的第一条数据
            db.stu.remove({age:66},{justOne:true})
        删除符合条件的所有数据
            db.stu.remove({age:66})
        删除所有数据
            db.stu.remove({})









'''
```

## 2.pymongo_test

```
# python与mongodb进行交互
# 选择虚拟机上面的解释器
# va 对应 home/pyvip
import pymongo
# 建立链接
client = pymongo.MongoClient('127.0.0.1',27017)
# 指定数据库
db = client['mydb22']

# 指定集合
collection = db['stu']

# 增
# 插入一条
# collection.insert_one({'name':'aaa','age':18,'sex':'男'})
# 插入多条
# collection.insert_many([
#                     {'name':'xiaobai','sex':'男','age':18},
#                     {'name':'xiaohei','sex':'女','age':16},
#                     {'name':'xiaohong','sex':'男','age':18}
#                     ])

# 改
# 修改一条
# collection.update_one({'name':'aaa'},{'$set':{'age':888}})
# 修改多条
# collection.update_many({'name':'aaa'},{'$set':{'age':888}})

# 删除
# 删除一条
# collection.delete_one({'name':'aaa'})
# 删除多条
# collection.delete_many({'name':'aaa'})
# 删除所有
collection.delete_many({})

# 查全部
data=collection.find()
# 游标
# print(data)
for i in data:
    print(i)

# 查一条
# data1=collection.find_one()
# print(data1)

# 逻辑和比较查询
# data2=collection.find(
# {'$or':
#                 [{'$and':[{'sex':'女'},{'age':16}]},
#                 {'$and':[{'sex':'男'},{'age':{'$gte':19}}]}]
#             }
# )
# # 游标
# # print(data)
# for i in data2:
#     print(i)
```

## 3.将MongDB封装成类

```
'''
将MongoDB find,insert,update,remove 方法封装成类
提示：就是把增删改查各封装成一个方法，一共8个封装成4个
find_one,find
insert_one ,insert_many
update_one, update_many
delete_one,delete_many
'''
import pymongo
# # 建立链接
# client = pymongo.MongoClient('127.0.0.1',27017)
# # 指定数据库
# db = client['mydb22']
#
# # 指定集合
# collection = db['stu']

class MyMongDB:
    def __init__(self,database,collection):
        # 把服务器建立连接赋值给实例化后的对象属性self.client
        self.client=pymongo.MongoClient('127.0.0.1', 27017)
        # 创建数据库给实例化后的对象属性self.db
        self.db=self.client[database]
        # 创建集合给实例化后的对象属性self.collection
        self.collection=self.db[collection]
    # insert_one ,insert_many
    def insert(self,*data):
        # 是一个元组
        # print(data)
        if len(data)==1:
            # 取元组的第一个值
            # 插入的是字典
            self.collection.insert_one(data[0])
        else:
            # 1 2
            # 元组要转换成列表
            # 插入的是一个列表里面包含的字典
            self.collection.insert_many(list(data))
    # update_one, update_many
    def update(self,data,new_data,m = False):
        if m:
            self.collection.update_many(data, {'$set': new_data})
        else:
            self.collection.update_one(data,{'$set':new_data})
    # delete_one,delete_many
    def remove(self,data,m=False):
        if m:
            self.collection.delete_many(data)
        else:
            self.collection.delete_one(data)


    # find_one,find
    def find(self,data={},m = False):
        if m:
            result = self.collection.find(data)
            # 游标
            for i in result:
                print(i)
        else:
            result = self.collection.find_one()
            print(result)


a=MyMongDB('mydb222','stu')
# 插入一个数据
# a.insert({'name':'dahai1'})
# 插入多个数据
# a.insert({'name':'dahai2'},{'name':'dahai3'})
# 修改一条数据
# a.update({'name':'dahai2'},{'name':'dahai222'})
# 修改多条数据
# a.update({'name':'dahai3'},{'name':'dahai333'},True)
# 删除指定的一条数据
# a.remove({'name':'dahai333'})
# 删除指定的多条数据
a.remove({'name':'dahai2'},True)

# 查找一个数据
# a.find({'name':'dahai1'})
# 查找全部个数据
a.find({},True)
```

## 4.python多版本共存

```
'''
爬虫 python3.7 pip 和 pycharm都可以
gevent python3.6 环境变量删除 模块用pycharm安装
'''

# 考试
# 选择题30  10
# 问答题70  14

# 上次参加考试的同学有分数但是没有奖品
# 跟下一个班期的同学最好不要参加考试
# 爬虫班3.7
    # 爬虫网络编程，并发编程看一下
# 新班3.6
    # 软件安装不用多版本安装一个3.6就可以了
    # 重新跟新班的同学，不能守株待兔等新班，day1到day4
# 学习消化 优 1  良 2  一般 3
'''
学制高升本/专升本2.5年（从学信网查询时间算起）,高升本5年(从学信网查询时间算起)
有想法的同学咨询一下西施老师，VIP学生有优惠
IT行业有技术都可以找到工作
当然同等技术下的同学，学历高的同学，可以要到更高一点的薪资
面试毕竟第一面试的是人事
对于长远来说学历提升是好的，工资和职位，乃至退休金
马克思主义，高等数学
'''
```

## 作业

```
1.把mongodb命令敲一遍
2.将MongoDB find,insert,update,remove 方法封装成类敲一遍
3.操作mongodb命令,插入一条用户的信息，
		1、数据信息包含了用户以下的信息：姓名，年龄，住址，爱好的信息
		2、修改一下用户的爱好，（值自己定）
		3、查询一下用户的信息
		4、删除此条用户的信息
```

