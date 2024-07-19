# *****
# 修改文件的方式一:
# 1 将文件内容由硬盘全部读入内存
# 2 在内存中完成修改
# 3 将内存中修改后的结果覆盖写回硬盘
# with open('文件修改.txt',mode='rt',encoding='utf-8')as f:
#     all_data=f.read()
#     print(all_data)
# # # 读出来的数据已经存到all_data变量里面的了
# with open('文件修改.txt',mode='wt',encoding='utf-8')as f1:
#     f1.write(all_data.replace('红黄蓝','大海'))

# 修改文件的方式二:
# 1 以读的方式打开源文件,以写的方式打开一个临时文件
# 2 从源文件中每读一样内容修改完毕后写入临时文件,直到源文件读取完毕
# 3 删掉源文件,将临时文件重命名为源文件名
# import os
# with open('文件修改二.txt',mode='rt',encoding='utf-8')as read_f\
#     ,open('临时文件.txt',mode='wt',encoding='utf-8')as write_f:
#     for line in read_f:
#         print(line)
#         write_f.write(line.replace('大海','夏洛'))
#
# # 文件修改二删除
# os.remove('文件修改二.txt')
# # # 临时文件.txt 改成 文件修改二
# os.rename('临时文件.txt','文件修改二.txt')


# 方式一:
# 优点: 在文件修改的过程中硬盘上始终一份数据
# 缺点: 占用内存过多,不适用于大文件


# 方式二:
# 优点: 同一时刻在内存中只存在源文件的一行内容,不会过多地占用内存
# 缺点: 在文件修改的过程中会出现源文件与临时文件共存,硬盘上同一时刻会有两份数据,即在修改的过程中会过多的占用硬盘,
