import os
from types import MappingProxyType
import yaml

from feedwork.utils import logger
import feedwork.utils.FileHelper as fileu
import feedwork.utils.System as sysu


HRS_RESOURCES_ROOT = sysu.env("HRS_RESOURCES_ROOT", str)  # 所有资源根目录
logger.info(f"[load config] HRS_RESOURCES_ROOT={HRS_RESOURCES_ROOT}")
_HRS_FDCONFIG_ROOT = fileu.cat_path(HRS_RESOURCES_ROOT, "fdconfig", check_exist='dir')


def load_conf(filename: str):
    """
    读取 fdconfig 下的配置文件。
    :param filename: 配置文件名（不需要路径）
    :return: 配置文件内容的字典。如果配置文件不存在，返回空字典对象
    """
    conf_file = fileu.cat_path(_HRS_FDCONFIG_ROOT, filename)
    if not os.path.isfile(conf_file):
        logger.warning(f"config file [{conf_file}] not exist !")
        return MappingProxyType(dict())

    with open(conf_file, "r", encoding="utf8") as f:
        data = yaml.safe_load(f)
    return MappingProxyType(data)


# class AutowaredBeanByDict(dict):
#     __setattr__ = dict.__setitem__
#     __getattr__ = dict.__getitem__
#
#
# def dictToBean(dictObj):
#     if not isinstance(dictObj, dict):
#         return dictObj
#     inst = AutowaredBeanByDict()
#     for k, v in dictObj.items():
#         inst[k] = dictToBean(v)
#     return inst


# def load_conf(filename: str, *, return_type="bean"):
#     conf_file = os.path.join(_HRS_FDCONFIG_ROOT, filename)
#     if not os.path.isfile(conf_file):
#         raise RuntimeError(f"config file [{conf_file}] is not regular file !")
#     with open(conf_file, "r", encoding="utf8") as f:
#         data = yaml.safe_load(f)
#
#     if return_type == "bean":
#         return dictToBean(data)
#     elif return_type == "dict":
#         return data
#     else:
#         raise ValueError(f"Invalid return_type ! expected 'bean, dict' but '{return_type}'")


# if __name__ == "__main__":
#     # TODO 删掉 main！ 写到test_suite中去
#     dbinfo1 = load_conf("dbinfo.conf", return_type="bean")
#     assert type(dbinfo1) == AutowaredBeanByDict
#     dbinfo2 = load_conf("dbinfo.conf", return_type="dict")
#     assert type(dbinfo2) == dict
#
#     assert dbinfo1['global'].fetch_size == dbinfo2['global']['fetch_size']
#     print(type(dbinfo1))
#     print(dbinfo1['global'].fetch_size)
