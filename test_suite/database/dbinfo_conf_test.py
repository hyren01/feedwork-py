# -*- coding:utf-8 -*-
from feedwork.database.dbinfo_conf import dbinfo as database_info
import pytest
import os
import sys


def test_get():
    name = 'default'
    dbinfo = database_info.get(name)
    assert dbinfo.name == name
    assert dbinfo.way == 'POOL'
    assert dbinfo.autocommit is False
    assert dbinfo.minPoolSize == 10
    assert dbinfo.max_result_rows == -1


if __name__ == "__main__":
    pytest.main(["-q", os.path.basename(sys.argv[0])])
