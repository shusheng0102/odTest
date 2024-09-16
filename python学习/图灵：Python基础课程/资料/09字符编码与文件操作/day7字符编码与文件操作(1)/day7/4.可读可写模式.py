# 可读可写:（了解）
# r+t

# w+t

# a+t

#  r + t
# 1 当文件不存时,会报错
# 2 当文件存在时,文件指针指向文件的开头
# 3 多了个末尾写
# with open('可读可写r+t模式.txt',mode='r+t',encoding='utf-8')as f:
#     print(f.readable())
#     print(f.writable())
#     msg = f.readline()
#     print(msg)
#     f.write('xxxxxxxxxxx')

# w+t
# 1 当文件不存时,新建一个空文档(无则创建)
# 2 当文件存在时,清空文件内容，文件指针跑到文件的开头（有则清空）
# 3 可以读
# with open('可读可写w+t模式.txt',mode='w+t',encoding='utf-8')as f:
#     print(f.readable())
#     print(f.writable())
#     f.write('aaaaaaaa\n')
#     f.write('bbbbbbbb\n')
#     # 指针移动seek（移动的字节数,开头开始0）
#     # 从开头开始移动0
#     f.seek(0,0)
#     print(f.readline())
#     #     还是在末尾写
#     f.write('cccccccc\n')

# a+t# 第二次打开时候也是在末尾写
# a 和 w的区别
# with open('可读可写a+t模式.txt',mode='a+t',encoding='utf-8')as f:
#     print(f.readable())
#     print(f.writable())
#     f.write('aaaaaaaa\n')
#     f.write('bbbbbbbb\n')
#     # 指针移动seek（移动的字节数,开头开始0）
#     # 从开头开始移动0
#     f.seek(0,0)
#     print(f.readline())
#     #     还是在末尾写
#     f.write('cccccccc\n')

# 图片和视频用不上
# r+b w+b a+b 规律和 r+t  w+t   a+t
# 乱掉 文件打不开