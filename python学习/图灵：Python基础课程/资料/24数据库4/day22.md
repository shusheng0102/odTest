## day22.数据库4

## 1.事务

```
'''
# 事务可以包含一系列的sql语句，事务的执行具有原子性 *****
#原子性：
#包含多条sql语句要么都执行成功，要么都执行不成功
create table tt1(id int,name varchar(12));
insert into tt1 values(1,'dahai');
开启事务
start transaction;
提交事务
commit;
回滚
rollback;

#transaction:事务，交易

'''
```

## 2.pymysql

### 创建表

```
# 每次更新本地文件记得上传，运行的是虚拟机上面的文件 *****
# pip install pymysql
import pymysql
# 拿到套接字对象
client = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'qwe123',
    database = 'mysql14',
    charset = 'utf8'
)
# 拿到游标  mysql>
cursor = client.cursor()
# 创建表
sql = '''
create table t1(
    id int not null,
    name varchar(10)
    );
'''
try:
    cursor.execute(sql)
    print('创建成功')
except Exception as e:
    print('创建数据库表失败%s'%e)
finally:
# 关闭游标连接# 相当与exit，关闭mysql
    cursor.close()
# 关闭数据库连接# 回收资源
    client.close()


```

### 其他操作

```
# 每次更新本地文件记得上传，运行的是虚拟机上面的文件 *****
# pip install pymysql
import pymysql
# 拿到套接字对象
client = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'qwe123',
    database = 'mysql14',
    charset = 'utf8'
)
# 拿到游标  mysql>
cursor = client.cursor()
# 插入数据
# sql  = '''
# insert into t1 values (1,'dahai'),(2,'xialuo');
# '''
# 修改数据
# sql = '''
# update t1 set name = 'xialuo' where id = 1;
# '''
# 删除数据
sql = '''
delete from t1 where id = 1;
'''


try:
    res=cursor.execute(sql)
    # # 几行受到影响
    print(res)
    # 需要提交
    client.commit()
except Exception:
    # 回滚
    client.rollback()
cursor.close()
client.close()



```

### executemany

```
# 每次更新本地文件记得上传，运行的是虚拟机上面的文件  *****
# pip install pymysql
import pymysql
# 拿到套接字对象
client = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'qwe123',
    database = 'mysql14',
    charset = 'utf8'
)
# 拿到游标  mysql>
cursor = client.cursor()
# 插入以下列表的数据
userinfo = [
    (3,'aaaaaaa'),
    (4,'bbbbbbb'),
    (5,'ccccccc')

]
# 第一种方法
# for user in userinfo:
#     # print(user)
#     # print(user[0])
#     # print(user[1])
#     sql = 'insert into t1 values (%s,"%s");'%(user[0],user[1])
#     res = cursor.execute(sql)
#     print(res)
# 第二种方法
# 使用executemany的第二个参数，放入占位符的内容,占位符不需要引号，它可以自动识别
sql = 'insert into t1 values (%s,%s);'
res = cursor.executemany(sql,userinfo)
print(res)
client.commit()

cursor.close()
client.close()






```

### 查询

```
# 每次更新本地文件记得上传，运行的是虚拟机上面的文件  *****
# pip install pymysql
import pymysql
# 拿到套接字对象
client = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'qwe123',
    database = 'mysql14',
    charset = 'utf8'
)
# 拿到游标  mysql>
# cursor() 只会把每条记录放入小元组
# cursor = client.cursor()
# 把字段也显示
#  显示成一个列表里面key是字段名 value是数据
cursor = client.cursor(pymysql.cursors.DictCursor)
# 查询
sql = 'select * from user;'

rows = cursor.execute(sql)

# print(rows)
# fetchall一次性拿到所有
# print(cursor.fetchall())
# # 第二次没了返回[]
# print(cursor.fetchall())
# 一次拿一条
# print(cursor.fetchone())
# print(cursor.fetchone())
# print(cursor.fetchone())
# # # 没有呢返回None
# print(cursor.fetchone())
# 拿指定的条数
# print(cursor.fetchmany(2))
# print(cursor.fetchone())
# 读一行指针移动一行
# 可以移动指针
# # 绝对位置移动 scroll(行数,mode='absolute') absolute绝对位置
# cursor.scroll(0,mode='absolute')
# cursor.scroll(1,mode='absolute')
# print(cursor.fetchall())
print(cursor.fetchone())
# 相对位置移动
cursor.scroll(1,mode='relative')
print(cursor.fetchone())

cursor.close()
client.close()










```

## 3.sql注入问题

```
# 每次更新本地文件记得上传，运行的是虚拟机上面的文件
# pip install pymysql
import pymysql
# 拿到套接字对象
client = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'qwe123',
    database = 'mysql14',
    charset = 'utf8'
)
# 拿到游标  mysql>
cursor = client.cursor()
'''
# 创建表
create table user
    (id int,
    name varchar(20),
    password varchar(20)
    );
插入数据
insert into user values
(1,'dahai',123),    
(2,'xialuo',456),    
(3,'xishi',789); 

sql注入
用一些特殊符号来改变sql语句的运行逻辑，不需要账号和密码直接可以登录
-- 注释
第一种
select id from user where name = "dahai" -- dsadsadasdasdaff" and password = "%s";
用户名输入 dahai" -- dsadsadasdasdaff
密码不输入回车
登录成功
第二种
账号和密码都不需要
select id from user where name = "xxx" or 1=1 -- dsafdsafafafasfasfa" and password = "%s";
用户输入 xxx" or 1=1 -- dsafdsafafafasfasfa
相当于
select id from user where name = "xxx" or 1=1
密码不输回车
登录成功

有些网站的账号密码不允许输入特殊符合，为了防止sql注入
前端（浏览器页面）可以筛选，
但是如果用爬虫是不是可以跳过前端，
所以后端也要检测
'''
inp_user = input('输入账号名').strip()
inp_pwd = input('输入密码').strip()

sql = 'select id from user where name = "%s" and password = "%s";'%(inp_user,inp_pwd)

res=cursor.execute(sql)

if res:
    print('登录成功')
else:
    print('用户或密码错误')
cursor.close()
client.close()






```

### 解决注入问题

```
# 每次更新本地文件记得上传，运行的是虚拟机上面的文件  *****
# pip install pymysql
import pymysql
# 拿到套接字对象
client = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = 'qwe123',
    database = 'mysql14',
    charset = 'utf8'
)
# 拿到游标  mysql>
cursor = client.cursor()
'''
# 创建表
create table user
    (id int,
    name varchar(20),
    password varchar(20)
    );
插入数据
insert into user values
(1,'dahai',123),    
(2,'xialuo',456),    
(3,'xishi',789); 

sql注入
用一些特殊符号来改变sql语句的运行逻辑，不需要账号和密码直接可以登录
-- 注释
第一种
select id from user where name = "dahai" -- dsadsadasdasdaff" and password = "%s";
用户名输入 dahai" -- dsadsadasdasdaff
密码不输入回车
登录成功
第二种
账号和密码都不需要
select id from user where name = "xxx" or 1=1 -- dsafdsafafafasfasfa" and password = "%s";
用户输入 xxx" or 1=1 -- dsafdsafafafasfasfa
相当于
select id from user where name = "xxx" or 1=1
密码不输回车
登录成功

有些网站的账号密码不允许输入特殊符合，为了防止sql注入
前端（浏览器页面）可以筛选，
但是如果用爬虫是不是可以跳过前端，
所以后端也要检测
'''
inp_user = input('输入账号名').strip()
inp_pwd = input('输入密码').strip()

# sql = 'select id from user where name = "%s" and password = "%s";'%(inp_user,inp_pwd)
sql = 'select id from user where name = %s and password = %s;'
# 使用execute的第二个参数，放入占位符的内容,占位符不需要引号，它可以自动识别
res=cursor.execute(sql,(inp_user,inp_pwd))

if res:
    print('登录成功')
else:
    print('用户或密码错误')
cursor.close()
client.close()






```

## 4.视图

```
'''
视图是什么?  *****
    本质是一张虚拟的表
    数据来自select语句，在内存里面，是一个临时数据
    那么有没有办法把它保存
    视图可以
    但是它可以永久保存表的结构，数据来源与原始的表，
    保存的是查询语句
    每次查询都是那种select语句去原始表里面查
如何使用
    创建视图
        语法
            create view 视图表的名字 as select语句
        实例
            create view test_view1 as select * from t1 where name = 'xialuo';
有什么用?
    原表安全
    案例:  在一公司中需要一张表保存所有人的薪资信息
           这个表不是所有人都能全看到   老板 财务 可以
           某一个员工 只能看到自己的信息
           所以不能把整个表的信息开发给这个员工
           工资保密协议
    功能1,隐藏部分数据 开放指定的数据
    insert into test_view1 values(7,'xiaohai');
    视图有插入
    但是查询
    select * from test_view1;
    还是 as 后面的 select * from t1 where name = 'xialuo';
    怎么证明
    insert into test_view1 values(3,'xialuo');
    同步到原表
    select * from t1;
    功能2,因为视图可以将查询结果保存特性 我可以用视图 来达到减少书写sql的次数
    技术部门都有那些员工
    select * from emp1 join dep on emp1.dep_id = dep.id where dep.name = '技术';
    将查询结果作为一个视图 以后在使用到这个需求 就直接查看视图
    注意:字段名不能重复
    create view jishu as select emp1.*,dep.name as dep_name from emp1 join dep on emp1.dep_id = dep.id where dep.name = '技术';
修改视图
    语法
        alter view 视图名称 as sql语句
    实例
        alter view test_view1 as select * from t1 where name = 'xiaohai';
删除视图
    语法
        drop view 视图名称
    实例
        drop view test_view1;
特点
     1.每次对视图进行的查询 其实都是再次执行了 as 后面的查询语句
     2.可以对视图进行修改 修改会同步到原表
     3.视图是永久存储的  存储的不是数据  而就是一条 as sql语句
     4.不要改视图，视图很多，只是用来查

'''
```

## 6.redis之string类型

```
'''
概述
    Redis本质上是一个Key-Value类型的内存数据库，整个数据库统统加载在内存当中进行操作，
    定期通过异步操作把数据库数据flush到硬盘上进行保存。因为是纯内存操作，Redis的性能非常出色，
    每秒可以处理超过 10万次读写操作。
    Redis的出色之处不仅仅是性能，Redis最大的魅力是支持保存多种数据结构，此外单个value的最大限制是1GB，
    redis不仅仅支持简单的Key-Value类型，同时还把value分为list,set,zset,hash等数据类型
    Redis的主要缺点是数据库容量受到物理内存的限制，不能用作海量数据的高性能读写，
    因此Redis适合的场景主要局限在较小数据量的高性能操作和运算上。
    效率会远远高于mysql，但是存储的量级不如mysql
Redis有哪些适合的场景？
（1）、会话缓存（Session Cache）
最常用的一种使用Redis的情景是会话缓存（session cache）。用Redis缓存会话比其他存储（如Memcached）的优势在于：
Redis提供持久化。user: password

'''

# Redis的语句 *****
'''
redis是key-value的数据结构,每条数据都是一个键值对
键的类型是字符串
注意:键不能重复
值的类型分为五种
string ------》字符串
list  ------》列表
hash ------》哈希
set ------》集合
zset ------》有序集合
'''
'''
连接redis: 
redis-cli --raw
127.0.0.1:6379> ip 和 端口
退出 exit
默认使用的是0号数据库
数据库是没有名称的，默认有16个，通过0-15来标识
切换到其他数据库：
select n
# 1、string类型  一个key值对应一个value值
                name:dahai  age:18
增（改）
    语法
        set key value 设置一个key 值为value
        如果这个key存在，则更新value值
        如果这个key不存在，则就key value值存下来
    实例
        如果这个key不存在，则就key value值存下来
            set name dahai
        如果这个key存在，则更新value值
            set name xialuo
    追加数据：（在原来的字符上面增加）
        语法
            append key 字符
        实例
            append name 333
    一次设置多个key value(没有就增加)
        语法
            mset key value key value...
        实例
            mset name dahai sex girl age 18
删
    语法
        del key
    实例
        del name
查:
    语法
        get key
    实例
        get name
    一次获取多个value
        语法
            mget key1，key2，key3....
        实例
            mget name age sex
    获取所有的key
        keys *
其他的操作
    set num 333
incr会识别字符串里面的数字并加1
    incr num
decr会识别字符串里面的数字并减1
    decr num
incrby在原有的基础上增加100   
    incrby num 100 
decrby在原有的基础上减少100
    decrby num 100
过期时间(一秒为单位的)
比如会员 ，网盘链接    
    查看时间
        ttl key
        -1代表无限 -2代表不存在 
    expire age 30    
    要在时间还没有过期的时候
        撤销过期时间(续费会员)
        persist key
'''




























```