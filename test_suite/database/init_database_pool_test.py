#!/usr/bin/env python
# -*- coding:utf-8 -*-
from feedwork.database.init_database_pool import database_pool
import pytest
import os
import sys
import json

database_name = "default"


def test_get_connection():
    # postgresql官方给出两种创建连接方式：
    # 1、conn = psycopg2.connect("dbname=test user=postgres password=secret")
    # 2、conn = psycopg2.connect(dbname="test", user="postgres", password="secret")
    conn = database_pool[database_name].connection()
    # 保证连接可用
    cursor = conn.cursor()
    cursor.execute("SELECT 1 AS num")
    result = cursor.fetchone()
    result = json.loads(json.dumps(result))
    conn.close()
    assert result[0] == 1


if __name__ == "__main__":
    pytest.main(["-q", os.path.basename(sys.argv[0])])
