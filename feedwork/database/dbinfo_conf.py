# -*- coding:utf-8 -*-
from feedwork.utils.ConfigHelper import load_conf
from types import MappingProxyType
from feedwork.database.bean.database_info import Dbinfo


def __dict_2_beans(bean_class, dict_obj: dict):
    """
    字典转换为bean。

    :param bean_class.object，要创建的Bean类
    :param dict_obj.dict，字典类型（json.loads后也是dict）
    """
    sci = bean_class()
    if not dict_obj:
        return sci
    for key in dict_obj:
        sci.__setattr__(key, dict_obj[key])

    return sci


def __transform_dbinfo(dbinfos):
    database_infos_tmp = {}
    for dbinfo_init in dbinfos:
        if 'name' not in dbinfo_init:
            raise KeyError(f"The key [name] not in dbinfo!")
        database_infos_tmp[dbinfo_init['name']] = __dict_2_beans(Dbinfo, dbinfo_init)
    return MappingProxyType(database_infos_tmp)


# 从yaml文件中读出配置信息
dbinfo = __transform_dbinfo(load_conf("dbinfo.conf")['databases'])
