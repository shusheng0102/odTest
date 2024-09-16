# day19.MySQL1

## 1.数据库的基本概念

```
'''
1、数据库是什么？
    变量是存储在内存
    数据库本质就是一个C/S的套接字软件
    改的是同一个数据
    安全
    数据库：
        关系型     比如：学生表和课程表  ，学生表有选课，那么它们之间就有关系
            mysql
        非关系型
            redis
            mongodb
2、数据库相关概念
    数据库服务器：运行有数据库管理软件的计算机
    数据库管理软件mysql：就是一个套接字服务端
    库：就是一个文件夹
    表：就是一个文件
    记录：就相当于文件中的一行内容（抽取事物一系列典型的特征拼到一起，）
    数据：用于记录现实世界中的某种状态

'''
```

## 2.mysql数据库的sql语句

```
'''
登录
    mysql -uroot -pqwe123
退出
    exit
mysql的库
    就是一个文件夹
    文件夹:库（create/drop/alter/show）
        增
            语法
                create database 数据库名字 charset 编码格式（不需要加引号）
            实例
                create database dahai1 charset utf8;
        删
            语法
                drop database 数据库名
            实例
                drop database dahai1;
        改 字符编码
            语法
                alter database 需要修改的数据库名字 charset 字符编码
            实例
                alter database dahai1 charset gbk;

        查
            查看所有的库
                show databases;
            查看库的详细信息
                语法
                    show create database 数据库名
                实例
                    show create database dahai1;
字段类型  和  python的数据类型是一个道理
字符串类型 char varchar    整数类型  int   浮点型 float
文件: 表
    1.切换到库（文件夹）
        语法
            use 库名;
        实例
            use dahai1;
    增
        必须要use切换到当前数据库
            语法
                create table 表名(字段名 字段类型(宽度),字段名 字段类型(宽度)....);
            实例
                create table t1(id int,name varchar(11));
        不用切换数据库
            语法
                create table 库名.表名(字段名 字段类型(宽度),字段名 字段类型(宽度)....);
            实例
                create table dahai1.t2(id int,name varchar(11));
    删（彻底删除）
        语法
            drop table 表名
        实例
            drop table t2;
    改(一般不会改)
        1.添加字段
            语法
                alter table 表名 add 字段 类型（宽度）
            实例
                alter table t1 add sex char(11);
        2.删除字段
            语法
                alter table 表名 drop 字段
            实例
                alter table t1 drop sex;
        3.改表字段的字段类型
            1.改字段的类型（不改字段名）
                语法
                    alter table 表名 modify 字段 新类型(宽度)
                实例
                    alter table t1 modify name char(12);
            2.直接改字段和类型
                语法
                    alter table 表名 change 老子段 新字段（宽度）
                实例
                    alter table t1 change sex se varchar(11);
        4.修改表名
            语法
                rename table 表名 to 新表名
            实例
                rename table t1 to ta;
    查
        1.查看表结构
            语法
                desc 表名
            实例
                desc ta;
        2.查看创建的表
            语法
                show create table 表名
            实例
                show create table ta;
        3.查看所有的表
            语法
                show tables;
        4.查看所在的库
            select database();
文件内的一行行内容:记录(insert/delete/update/select)
    增
        1.为想要的字段添加值,多余的会插入空
            语法
                insert into 表名(字段1,字段2) values
                (第一行数据,没有插入的字段会为空),
                (第二行数据,没有插入的字段会为空),
                (第三行数据,没有插入的字段会为空);
            实例
                insert into ta(id,name) values
                (1,'dahai'),
                (2,'xialuo'),
                (3,'guan');
        2.不写添加的字段（所有字段插入）
            语法
                insert into(可以不写) 表名 values
                (第一行数据,记录必须与表的字段数量还有类型要一致),
                (第二行数据,记录必须与表的字段数量还有类型要一致),
                (第三行数据,记录必须与表的字段数量还有类型要一致);
            实例
                insert ta values
                (4,'dahai','man');
    删
        删除表的部分信息
            语法
                delete from 表名 where 条件
                不要用它全删:没有条件全删
            实例

                delete from ta where id = 1;
        清空表信息
            语法
                truncate 表名
            实例
                truncate ta;
    改
        1.直接修改字段
            语法
                update 表名 set 字段名 = 修改值
            实例
                update ta set se = 'woman';
        2.加条件
            语法
                update 表名 set 字段名 = 修改值 where 条件
            实例
                update ta set se = 'man' where id = 3;

    查
        1.查看所有的记录
            语法
                select * from 表名;
            实例
                select * from ta;
        2.查看指定字段
            语法
                select 指定字段 from 表名;
            实例
                select id,name from ta;
        3.查看字段加条件 where
            查看所有的加条件
                语法
                    select * from 表名 where 条件
                实例
                    select * from ta where id > 2;
        4.不用进入库也可以查表内容
            语法
                select * from 库名.表名
            实例
                select * from dahai1.ta;

















'''
```

### 3.字段类型

```
'''
整型
    表示整数,通常id设置成整型 int
    存储范围(-2147483648,2147483647)
    强调：整型类型后面的宽度限制的根本不是存储宽度，限制的是显示宽度
    create table t5(id int(1));
    create table t6(id int(5));

    create table t7(id int zerofill);
    create table t8(id int(5) zerofill);
2. 浮点型:小数
    单精度和双精度
        数字的个数最大值为255,小数最大值为30
    单精度
        float(255,30)
    双精度
        double(255,30)
    准确精度(小数是最精确)
        decimal
        数字的个数最大值为65,小数最大值为30
    create table tt8(x float(255,30));
    create table tt9(x double(255,30));
    create table tt10(x decimal(65,30));

    insert into tt8 values(1.11111111111111111111111111111111111111);
    insert into tt9 values(1.11111111111111111111111111111111111111);
    insert into tt10 values(1.11111111111111111111111111111111111111);
3.日期类型
    year 1999
    date 1999-11-11
    time 08:30:00
    datetime/timestamp 1999-11-11 08:30:00

    create table student(
        id int,
        name varchar(16),
        a_year year,
        b_date date,
        class_time time,
        reg_time datetime
        );
    插入当前的时间
        insert into student values
        (1,'dahai',now(),now(),now(),now());
    自定义的数字时间
        insert into student values
        (1,'dahai',2000,20001111,083000,20001111083000);
    自定义的字符串数字时间
        insert into student values
        (1,'dahai','1999','2000-11-11','08:30:00','2000-11-11 08:30:00');
    datetime/timestamp
        在实际应用的很多场景中，MySQL的这两种日期类型都能够满足我们的需要，存储精度都为秒，
        但在某些情况下，会展现出他们各自的优劣。下面就来总结一下两种日期类型的区别。
    1.DATETIME的日期范围是1001——9999年，TIMESTAMP的时间范围是1970——2038年。

    2.DATETIME使用8字节的存储空间，TIMESTAMP的存储空间为4字节。因此，TIMESTAMP比DATETIME的空间利用率更高。

    3.DATETIME的默认值为null；TIMESTAMP的字段默认不为空（not null）,默认值为当前时间（CURRENT_TIMESTAMP）。
        create table time1(x timestamp);
        create table time2(x datetime);
4.字符类型
    注意: 宽度指限制字符的个数
    char：定长
        char(5)
    varchar 变长
        varchar(5)
    相同点: 宽度指的都是最打存储的字符个数,超过了都无法正常存储
    不同点
        char(5)
            'm'---》'm     ' 5个字符
        varchar(5)
            'm'----> 'm'   1个字符 （还有一个bytes是描述数据的）
char(5)
dahai|aa   |xxx  |f    |
varchar(5)
1个bytes+dahai|1个bytes+aa|1个bytes+xxx|1个bytes+f|
varchar(5)大部分用它 ,大部分情况下存储的数据都是小于约束的宽度
5.enum枚举是多选一，像python布尔类型,
    set集合是多选多 了解
    create table student1(id int,
    name varchar(20),
    sex enum('man','woman'),
    hobbies set('read','play','music'));
    插入数据
    insert into student1 values(1,'dahai','man','read,play');


''''''
整型
    表示整数,通常id设置成整型 int
    存储范围(-2147483648,2147483647)
    强调：整型类型后面的宽度限制的根本不是存储宽度，限制的是显示宽度
    create table t5(id int(1));
    create table t6(id int(5));

    create table t7(id int zerofill);
    create table t8(id int(5) zerofill);
2. 浮点型:小数
    单精度和双精度
        数字的个数最大值为255,小数最大值为30
    单精度
        float(255,30)
    双精度
        double(255,30)
    准确精度(小数是最精确)
        decimal
        数字的个数最大值为65,小数最大值为30
    create table tt8(x float(255,30));
    create table tt9(x double(255,30));
    create table tt10(x decimal(65,30));

    insert into tt8 values(1.11111111111111111111111111111111111111);
    insert into tt9 values(1.11111111111111111111111111111111111111);
    insert into tt10 values(1.11111111111111111111111111111111111111);
3.日期类型
    year 1999
    date 1999-11-11
    time 08:30:00
    datetime/timestamp 1999-11-11 08:30:00

    create table student(
        id int,
        name varchar(16),
        a_year year,
        b_date date,
        class_time time,
        reg_time datetime
        );
    插入当前的时间
        insert into student values
        (1,'dahai',now(),now(),now(),now());
    自定义的数字时间
        insert into student values
        (1,'dahai',2000,20001111,083000,20001111083000);
    自定义的字符串数字时间
        insert into student values
        (1,'dahai','1999','2000-11-11','08:30:00','2000-11-11 08:30:00');
    datetime/timestamp
        在实际应用的很多场景中，MySQL的这两种日期类型都能够满足我们的需要，存储精度都为秒，
        但在某些情况下，会展现出他们各自的优劣。下面就来总结一下两种日期类型的区别。
    1.DATETIME的日期范围是1001——9999年，TIMESTAMP的时间范围是1970——2038年。

    2.DATETIME使用8字节的存储空间，TIMESTAMP的存储空间为4字节。因此，TIMESTAMP比DATETIME的空间利用率更高。

    3.DATETIME的默认值为null；TIMESTAMP的字段默认不为空（not null）,默认值为当前时间（CURRENT_TIMESTAMP）。
        create table time1(x timestamp);
        create table time2(x datetime);
4.字符类型
    注意: 宽度指限制字符的个数
    char：定长
        char(5)
    varchar 变长
        varchar(5)
    相同点: 宽度指的都是最打存储的字符个数,超过了都无法正常存储
    不同点
        char(5)
            'm'---》'm     ' 5个字符
        varchar(5)
            'm'----> 'm'   1个字符 （还有一个bytes是描述数据的）
char(5)
dahai|aa   |xxx  |f    |
varchar(5)
1个bytes+dahai|1个bytes+aa|1个bytes+xxx|1个bytes+f|
varchar(5)大部分用它 ,大部分情况下存储的数据都是小于约束的宽度
5.enum枚举是多选一，像python布尔类型,
    set集合是多选多 了解
    create table student1(id int,
    name varchar(20),
    sex enum('man','woman'),
    hobbies set('read','play','music'));
    插入数据
    insert into student1 values(1,'dahai','man','read,play');


'''
```

### 作业

```
'''
1.建一张学生表 包含（id，name，age，sex，hobbies）
2.增加四条数据
3.查询表中sex为男的数据
4.删除id =3的数据，
5.将sex为女的，修改为男
'''
```