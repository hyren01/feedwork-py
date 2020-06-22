## conf文件使用说明

- 设置环境变量： HRS_RESOURCES_ROOT
  * 指定所有资源文件在本机的存放根目录
  * 该目录下至少包括一个目录：fdconfig
- 创建conf文件： fdconfig/appinfo.conf
  * 在这个文件中填写需要设置的全局变量。例如：

```yaml
# 算法使用的配置参数
algor:
    module    : 自己的本地目录-训练模型的输出目录
    pretrain  : 自己的本地目录-bert等预训练模型的存放目录
```

- 代码中使用方式

```python
import feedwork.AppinfoConf as appconf

appconf.ALGOR_MODULE_ROOT      # 对应 algor.module
appconf.ALGOR_PRETRAIN_ROOT    # 对应 algor.pretrain
```
