# -*- coding:utf-8 -*-
from enum import Enum, unique


# 如果不继承Enum，枚举值能被修改
class DatabaseType(Enum):
    PGSQL = 'POSTGRESQL'
    MYSQL = 'MYSQL'
    ORACLE = 'ORACLE'
    TERADATA = ''
    HIVE = ''
    NONE = ''
