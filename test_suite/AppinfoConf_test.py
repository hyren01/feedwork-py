"""
设置HRS_RESOURCES_ROOT为 fdconfig 的父目录才能执行本用例！
HRS_RESOURCES_ROOT=$PWD/resources pytest AppinfoConf_test.py
"""
import os
import sys
import time

import pytest

from feedwork.AppinfoConf import appinfo as prjInfo
from feedwork.AppinfoConf import ALGOR_MODULE_ROOT, ALGOR_PRETRAIN_ROOT
import feedwork.AppinfoConf as appconf


# 测试 ConfigHelper
def test_load():
    import feedwork.utils.ConfigHelper as confu
    null_appconf = confu.load_conf("notexist.conf")
    # assert isinstance(null_appconf, mappingproxy)
    assert len(null_appconf) == 0

    appinfos = confu.load_conf("appinfo.conf")
    # assert isinstance(appinfos, dict)
    with pytest.raises(Exception):
        appinfos['project_name'] = "test-fdcore"
    assert appinfos['project_name'] == "test fdcore"


def test_algor_value_byimport():
    import feedwork.utils.ConfigHelper as confu
    res_root = confu.HRS_RESOURCES_ROOT
    assert appconf.ALGOR_MODULE_ROOT == "mymodule"
    assert appconf.ALGOR_PRETRAIN_ROOT == "mypretrain"


def test_algor_value():
    import feedwork.utils.ConfigHelper as confu
    res_root = confu.HRS_RESOURCES_ROOT
    assert ALGOR_MODULE_ROOT == "mymodule"
    assert ALGOR_PRETRAIN_ROOT == "mypretrain"


def test_usable_byimport():
    with pytest.raises(Exception):
        appconf.appinfo['project_name'] = "test-fdcore"
    assert appconf.appinfo['project_name'] == "test fdcore"
    assert appconf.appinfo['version'] is None
    assert appconf.appinfo['global'] == "world"
    assert appconf.appinfo['nums'] == 10
    assert appconf.appinfo['money'] == -0.30
    assert appconf.appinfo['flag']      # == True
    assert not appconf.appinfo['show']  # == False

    assert appconf.appinfo['info']['fetch_size'] == 200
    assert appconf.appinfo['info']['max_result_rows'] == -1
    assert appconf.appinfo['info']['show_conn_time']  # == True

    assert appconf.appinfo['databases'][0]['name'] == "default"


def test_usable():
    with pytest.raises(Exception):
        prjInfo['project_name'] = "test-fdcore"
    assert prjInfo['project_name'] == "test fdcore"
    assert prjInfo['version'] is None
    assert prjInfo['global'] == "world"
    assert prjInfo['nums'] == 10
    assert prjInfo['money'] == -0.30
    assert prjInfo['flag']      # == True
    assert not prjInfo['show']  # == False

    assert prjInfo['info']['fetch_size'] == 200
    assert prjInfo['info']['max_result_rows'] == -1
    assert prjInfo['info']['show_conn_time']  # == True

    assert prjInfo['databases'][0]['name'] == "default"


def test_perf_byimport():
    start = time.time()
    for _ in range(10000):
        if appconf.appinfo['nums'] != 10:
            raise RuntimeError(f"appinfo.appinfo['nums']={prjInfo['nums']}")
        if appconf.appinfo['databases'][0]['name'] != "default":
            raise RuntimeError(f"appinfo.appinfo['databases'][0]['name']={prjInfo['databases'][0]['name']}")
    end = time.time()
    # 运行时间应该小于50毫秒
    # print("running time :", (end - start))
    assert (end - start) < 0.05


def test_perf():
    start = time.time()
    for _ in range(10000):
        if prjInfo['nums'] != 10:
            raise RuntimeError(f"prjInfo['nums']={prjInfo['nums']}")
        if prjInfo['databases'][0]['name'] != "default":
            raise RuntimeError(f"prjInfo['databases'][0]['name']={prjInfo['databases'][0]['name']}")
    end = time.time()
    # 运行时间应该小于50毫秒
    # print("running time :", (end - start))
    assert (end - start) < 0.05


if __name__ == "__main__":
    pytest.main(["-q", os.path.basename(sys.argv[0])])
