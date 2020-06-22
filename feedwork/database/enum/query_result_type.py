# -*- coding:utf-8 -*-
from enum import Enum, unique


# 如果不继承Enum，枚举值能被修改
class QueryResultType(Enum):
    JSON = 'json'
    DICT = 'dict'
    PANDAS = 'pandas'
    BEAN = 'bean'
    DB_NATURE = 'nature'
