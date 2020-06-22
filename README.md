## python 项目的公共包

- [配置文件](docs/config.md)
- [工具类](docs/utils.md)
- [数据库处理](docs/database.md)

## 安装
### 开发环境的安装方式
```shell
python3 -m pip install -U git+http://139.9.126.19:38111/FdcoreHyren/feedwork-py.git
```

### 部署发布的安装方式

1. 构建模块：python3 setup.py build。完成后会多出来一个build目录
2. 生成发布压缩包：python3 setup.py sdist。完成后会在dist目录下生成一个gz压缩文件
3. 把该gz文件上传需安装的主机，解压文件并进入解压目录，执行：python3 setup.py install

## 源码测试
1. 安装pytest： python3 -m pip install pytest
2. 运行测试用例
  * 命令行方式： pytest xxx.py（不指定文件则运行所有测试用例）
  * PyCharm方式： File -> setting -> Python Integrated Tools - Default test runner 的下拉框中选 pytest
