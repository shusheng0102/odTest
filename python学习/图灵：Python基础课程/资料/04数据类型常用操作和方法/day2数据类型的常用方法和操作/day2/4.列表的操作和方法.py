# 字符串，数字，布尔，复数 都是一个值
'''
# 列表类型：list
#作用：记录/存多个值，可以方便地取出来指定位置的值，比如人的多个爱好，一堆学生姓名
#定义：在[]内用逗号分隔开多个任意类型的值
'''
L = ['大海',1,1.2,[1.22,'小海']]
#     0     1  2   3
# print(L)
# # # 索引从0开始  相当于我们书的页码
# print(L[0])
# print(L[1])
# print(L[1])
# print(L[1])
# print(L[1])
# print(L[-1]) # 反向取
# print(L[3]) # 正向取
# print(L[3][1])
# xiaohai_list=L[3]
# print(xiaohai_list)
# print(xiaohai_list[1])
print(L)
print(id(L))
# 把原值改了
L[0]='红海'
print(L)
print(id(L))
# 2、切片(顾头不顾尾，步长)
# 查找列表当中的一段值 [起始值:终止值:步长]
# 和字符串提取字符一样,只不过字符串取的是字符，列表取的是一个数据类型/元素
# 但是字符串不能索引改值
# 默认步长为1
print(L[0:3])
print(L[0:3:1])
print(L[0:3:2])
# 3.len长度  列表元素的多少
print(len(L))
# 4.成员运算in和not in
print('红海' in L)
print('红海'not  in L)
# 查看列表某个元素的个数 count
print(L.count('红海'))
# 在列表中从左至右查找指定元素，找到了放回该值的下标/索引
print(L.index('红海'))
# print(L.index('海'))
#增

# append(元素) 往列表末尾追加一个元素
L.append('蓝海')
print(L)
# 规律列表的修改和增加都不需要重新复制，直接改变了原值，所以是可变类型
# 字符串，数字，布尔，复数 都是一个值，改变需要重新赋值，都是不可变类型
L.append('蓝海')
print(L)
# extend() 往列表当中添加多个元素 括号里放列表 也是末尾追加
L.extend(['绿海','紫海'])
# L.extend(['绿海','紫海'])
print(L)
# insert(索引，元素) 往指定索引位置前插入一个元素
L.insert(1,'黄海')
print(L)
# 删除

# del L[0]
# print(L)
# 指定删除
# L.remove('紫海')
# print(L)
# pop # 从列表里面拿走一个值
# # 按照索引删除值
# # 默认是删除最后一个
# L.pop()
# print(L)
# res=L.pop(0)
# # 返回值指定的索引元素
# print(res)
# print(L)
# 清空列表clear
# L.clear()
# print(L)
# 改
# L[0]='白海'
# print(L)
# 反序
# L.reverse()
# print(L)
# sort 排序 对数字
list_num = [1,3,2,5]
# 不写默认是正序
# reverse=True参数是倒序
list_num.sort(reverse=True)
print(list_num)
# reverse=False参数是正序
list_num.sort(reverse=False)
print(list_num)