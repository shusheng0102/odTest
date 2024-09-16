# day20.表的完整性

# 1.表达完整性约束

```
'''
一、创建表的完整语法
#语法：
create table 库名.表名(
    字段名1 类型[(宽度) 约束条件],
    字段名2 类型[(宽度) 约束条件],
    字段名3 类型[(宽度) 约束条件]
);
约束条件：是在数据类型之外对字段附加的额外的限制
#注意：
1、最后一个字段之后不能加逗号
2. 在同一张表中，字段名是不能相同
3. 宽度和约束条件可选,字段名和类型是必须的
常用约束
    not null 非空
    default 默认值
    auto_increment 必须要加一个键 自增长 可以不用进行插入了
    primary key 主键 非空且唯一
实例
    create table t1(
        id int primary key auto_increment,
        name varchar(16) not null,
        sex enum('male','female') not null default 'male'
        );

    插入只用插入name
    insert into t1(name) values('dahai'),('xialuo'),('xishi');
auto_increment(自己设置初始值)
    实例
        create table tb51(
        id int primary key auto_increment,
        name varchar(20) not null
        )auto_increment = 100;
    insert into tb51(name) values('dahai'),('xialuo'),('xishi');

        delete from tb51;
    约束重置
        truncate tb51;
唯一约束
unique key
    实例
        创建方式一
            create table t2(x int unique);
        创建方式二
            create table t3(
            x int,
            unique key(x)
            );
联合唯一（二者加起来是唯一）
    create table service(
        ip varchar(15),
        port int,
        unique key(ip,port)
        );
    insert into service values
    ('1.1.1.1',3306);
primary key(非空唯一)
站在约束角度看primary key=not null unique
以后但凡建表，必须注意：
# 主键id
1、必须有且只有一个主键
2、通常是id字段被设置为主键
create table t5(
    id int primary key auto_increment
    );
    insert into t5 values();
联合主键（二者加起来是非空且唯一）
    create table t6(
    x varchar(15),
    y int,
    primary key(x,y)
    );
    insert into t6 values
    ('1.1.1.1',3306);

'''
```

# 2.外键多对一

```
'''
外键
foreign key 限制关联表某一个字段的值必是来自于被关联表的一个字段
# foreign key注意：
# 1、被关联的字段必须是一个key，通常是id字段
# 2、创建表时：必须先建立被关联的表，才能建立关联表
    create table dep(
        id int primary key auto_increment,
        dep_name varchar(20),
        dep_info varchar(20)
        );
    语法
        constraint 外键名字      也可以不写
        foreign key(当前表需要关联的id,直接自己设置的名字) references 被关联的表名(被关联表的id)
        create table emp(
        id int primary key auto_increment,
        name varchar(15),
        age int,
        dep_id int,
        constraint fk_emp_dep
        foreign key(dep_id) references dep(id)
        );
    不写创建外键名
        create table emp(
        id int primary key auto_increment,
        name varchar(15),
        age int,
        dep_id int,
        foreign key(dep_id) references dep(id)
        );
    删除必须先删除关联的表
        drop table emp;
        drop table dep;
    删除外键（一般不用删除，外键的建立是考虑好了的）
        语法
            alter table 表名 drop foreign key 外键名字;
        实例
            alter table emp drop foreign key emp_ibfk_1;
    # 1,2
    # 3、插入记录时：必须先往被关联的表插入记录，才能往关联表中插入记录
        insert into dep(dep_name,dep_info) values
        ('python','python_course'),
        ('music','music_course'),
        ('java','java_course');

        插入关联表
        insert into emp(name,age,dep_id) values
        ('dahai',18,1),
        ('xishi',19,2),
        ('zuge',23,3),
        ('xialuo',24,1),
        ('zhouyu',21,3);
    删除时：应该先删除关联表emp中的记录，再删除被关联表对应的记录
    要删除部门表里面的一个id需要先把它被关联的字段删除
    delete from emp where dep_id = 2;
    删除
    delete from dep where id =2;
    改被关联表(改不了)
    update dep set id = 200 where id = 3;
    创建关联表可以更新同步和删除同步
        删除
        delete from dep where id =2;
        改被关联表(改不了)
        update dep set id = 200 where id = 3;
更新和删除同步，员工表设置成更新删除同步 on update cascade on delete cascade
        create table emp(
        id int primary key auto_increment,
        name varchar(15),
        age int,
        dep_id int,
        foreign key(dep_id) references dep(id)
        on update cascade on delete cascade
        );
查询
    select * from emp,dep;
    select * from emp,dep where emp.dep_id = dep.id;
    select * from emp,dep where emp.dep_id = dep.id order by emp.id asc;
    select * from emp,dep where emp.dep_id = dep.id order by emp.id desc;


'''
```

# 3.多对多

```
'''
多对多
    author2book 多对一     author
    author2book 多对一     book
    author      多对多     book
    create table author(
        id int primary key auto_increment,
        name varchar(16),
        age int
        );
    create table book(
        id int primary key auto_increment,
        bname varchar(16),
        price int
        );
    # 非主键可以混用
    create table author2book(
        id int primary key auto_increment,
        author_id int,
        book_id int,
        unique key(author_id,book_id),
        foreign key(author_id) references author(id)
        on update cascade on delete cascade,
        foreign key(book_id) references book(id)
        on update cascade on delete cascade
        );
    插入数据
        insert into author(name,age) values
        ('dahai',22),
        ('xialuo',23),
        ('guan',18),
        ('xishi',19),
        ('jiujiu',20);

        insert into book(bname,price) values
        ('玉女真经',5),
        ('九阳神功',3),
        ('太极拳',4),
        ('如来神掌',2),
        ('玉女剑法',6);

        insert into author2book(author_id,book_id) values
        (1,2),
        (1,3),
        (2,3),
        (2,4),
        (3,2),
        (3,3),
        (3,4),
        (4,3),
        (5,2);
查
    select * from author,book,author2book;
    select * from author,book,author2book;
    select author.id,name,age,bname,price from author,book,author2book where author.id =author2book.author_id and book.id = author2book.book_id;

    select author.id,name,age,bname,price from author,book,author2book where author.id =author2book.author_id and book.id = author2book.book_id and author.name ='dahai';

'''
```

# 4.一对一

```
'''
一对一
    学生表中的学生 对应的详细信息
    create table student(
        id int primary key,
        name varchar(10)
        );
    create table stu_detail(
        s_id int primary key,
        age int,
        sex char(5),
        foreign key(s_id) references student(id)
        on update cascade
        on delete cascade
        );
    插入数据
        insert into student values
        (1,'dahai'),
        (2,'xialuo'),
        (3,'xishi');
        insert into stu_detail values
        (1,18,'man'),
        (2,18,'man'),
        (3,18,'woman');
    select * from student,stu_detail;
    select * from student,stu_detail where student.id = stu_detail.s_id;

'''
```

# 作业

```
'''
建立选课的4张表:
(学院表，学生表，课程表，选课表(中间表)) , 并每张表插入4条数据。
学院表与学生表是一对多的关系
学生表与课程表是多对多的关系
'''
```

