# 字符串，数字，布尔，复数 都是一个值
'''
# 列表类型：list
#作用：记录/存多个值，可以方便地取出来指定位置的值，比如人的多个爱好，一堆学生姓名
#定义：在[]内用逗号分隔开多个任意类型的值
'''
L = ['大海',1,1.2,[1.22,'小海']]
#     0     1  2   3
print(L)
# # 索引从0开始  相当于我们书的页码
print(L[0])
print(L[1])
print(L[1])
print(L[1])
print(L[1])
print(L[-1]) # 反向取
print(L[3]) # 正向取
print(L[3][1])
xiaohai_list=L[3]
print(xiaohai_list)
print(xiaohai_list[1])
L[0]='红海'
print(L)