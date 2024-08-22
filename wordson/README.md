# 运行环境

pyhton

# 环境创建方法

> 建一个新环境，做好环境隔离，不然很有可能会污染你原来的环境，会出现以前跑通的代码，现在跑不通了

## 安装虚拟环境管理工具

> pip install -i [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple) virtualenvwrapper-win

> pip install -i [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple) virtualenvwrapper

## 环境管理相关命令

> mkvirtualenv env_name 创建虚拟环境

> workon env_name 激活虚拟环境

> deactivate 退出虚拟环境

> rmvirtualenv env_name 删除虚拟环境

### 配置国内下载镜像(如果人在国外就不用了)

> python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

> pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

### requirements.txt使用方法

> pip install -r requirements.txt

### requirements.txt创建方法

> pip freeze > requirements.txt
