#!/usr/bin/env python
# -*- coding:utf-8 -*-
from feedwork.database.database_wrapper import DatabaseWrapper
from feedwork.database.bean.database_info import Dbinfo
from feedwork.database.enum.conn_way import ConnWay
from feedwork.database.enum.database_type import DatabaseType
from feedwork.database.bean.database_config import DatabaseConfig
from feedwork.database.enum.query_result_type import QueryResultType
import pytest
import os
import sys


def __set_dbinfo(autocommit=False):
    # TODO 为了测试多个数据库，设置不同数据库的环境变量
    name = "test"
    db_info = Dbinfo()
    db_info.name = name
    db_info.way = ConnWay.DIRECTLY.value
    db_info.dbtype = DatabaseType.PGSQL.value
    db_info.host = "127.0.0.1"
    db_info.port = 5432
    db_info.dbname = "postgres"
    db_info.username = "postgres"
    db_info.password = "q1w2e3"
    db_info.autocommit = autocommit
    db_info.show_sql = True
    db_info.show_conn_time = True
    db_info.show_sql_time = True
    db_info.fetch_size = 200
    db_info.max_result_rows = -1
    db_info.longtime_sql = 10000
    db_info.query_timeout = 1000
    db_info.max_rows = 1000
    db_info.fetch_direction = 1

    db_config = DatabaseConfig()
    db_config.name = name
    db_config.need_id = True
    db_config.desc = "测试用"
    db_config.lazy_connect = False
    db_config.dbinfo = db_info

    return db_config


def test_execute_by_config_file():
    db = DatabaseWrapper()
    try:
        db.execute("CREATE TABLE db_wrapper_test(id int null, name varchar(64) null)")
        # oracle的写法：db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(:1, :2)", (1, 'abc'))
        inser_num = db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (1, 'abc'))
        assert inser_num == 1
        update_num = db.execute("UPDATE db_wrapper_test SET name = %s WHERE id = %s", ('def', 1))
        assert update_num == 1
        delete_num = db.execute("DELETE FROM db_wrapper_test")
        assert delete_num == 1
        # 对于pgsql来说，CREATE TABLE不在事务控制范围内；对于mysql来说，CREATE TABLE、DROP TABLE不在事务控制范围内
        # 所以下一行代码在测试pgsql时必须要提交，在测试mysql时可以放在finally中
        # oracle语法不支持DROP TABLE IF EXISTS
        db.execute("DROP TABLE db_wrapper_test")
        db.commit()
    except Exception as e:
        db.rollback()
        raise RuntimeError(e)
    finally:
        db.close()


def test_execute():
    db_config = __set_dbinfo(autocommit=True)
    db = DatabaseWrapper(db_config)
    try:
        db.execute("CREATE TABLE db_wrapper_test(id int null, name varchar(64) null)")
        inser_num = db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (1, 'abc'))
        assert inser_num == 1
        update_num = db.execute("UPDATE db_wrapper_test SET name = %s WHERE id = %s", ('def', 1))
        assert update_num == 1
        delete_num = db.execute("DELETE FROM db_wrapper_test")
        assert delete_num == 1
        # 因为设置了自动提交，所以不再手动调用commit()
    except Exception as e:
        raise RuntimeError(e)
    finally:
        db.execute("DROP TABLE db_wrapper_test")
        db.close()


def test_begin_transaction():
    db_config = __set_dbinfo(autocommit=True)
    db = DatabaseWrapper(db_config)
    try:
        db.execute("CREATE TABLE db_wrapper_test(id int null, name varchar(64) null)")
        db.begin_transaction()
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (1, 'abc'))
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (2, 'def'))
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (3, 'ghi'))
        # 先关闭一次，否则查询语句能查询出缓冲区里的数据
        db.close()
        db = DatabaseWrapper(db_config)
        df = db.query("SELECT * FROM db_wrapper_test WHERE id BETWEEN %s AND %s", (0, 4), QueryResultType.PANDAS)
        # 行数及列数
        assert df.shape[0] == 0
        assert df.shape[1] == 2
    except Exception as e:
        db.rollback()
        raise RuntimeError(e)
    finally:
        db.execute("DROP TABLE db_wrapper_test")
        db.close()


def test_commit():
    # TODO autocommit设置为False意味着该次连接开启事务，db.begin_transaction()存在的唯一价值是使用者能在自动提交的连接中开启事务，
    #  但是这里有个问题，若在自动提交的连接中开启了事务（即autocommit由True变为False），那么在commit中是否要关闭事务（即autocommit由False变为True）
    db_config = __set_dbinfo(autocommit=False)
    db = DatabaseWrapper(db_config)
    try:
        db.execute("CREATE TABLE db_wrapper_test(id int null, name varchar(64) null)")
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (1, 'abc'))
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (2, 'def'))
        db.commit()
        df = db.query("SELECT * FROM db_wrapper_test WHERE id BETWEEN %s AND %s", (0, 3), QueryResultType.PANDAS)
        # 行数及列数
        assert df.shape[0] == 2
        assert df.shape[1] == 2
    except Exception as e:
        db.rollback()
        raise RuntimeError(e)
    finally:
        # mysql的drop table不需要提交，pgsql需要
        db.execute("DROP TABLE db_wrapper_test")
        db.commit()
        db.close()


def test_close():
    db_config = __set_dbinfo()
    db = DatabaseWrapper(db_config)
    db.close()
    assert db.is_closed()


def test_rollback():
    db_config = __set_dbinfo(True)
    db = DatabaseWrapper(db_config)
    try:
        db.execute("CREATE TABLE db_wrapper_test(id int null, name varchar(64) null)")
        db.begin_transaction()
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (1, 'abc'))
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (2, 'def'))
        db.rollback()
        db.close()
        db = DatabaseWrapper(db_config)
        df = db.query("SELECT * FROM db_wrapper_test WHERE id BETWEEN %s AND %s", (0, 3), QueryResultType.PANDAS)
        # 行数及列数
        assert df.shape[0] == 0
        assert df.shape[1] == 2
        db.commit()
        df = db.query("SELECT * FROM db_wrapper_test WHERE id BETWEEN %s AND %s", (0, 3), QueryResultType.PANDAS)
        # 行数及列数
        assert df.shape[0] == 0
        assert df.shape[1] == 2
    except Exception as e:
        db.rollback()
        raise RuntimeError(e)
    finally:
        db.execute("DROP TABLE db_wrapper_test")
        db.commit()
        db.close()


def test_query():
    db_config = __set_dbinfo(autocommit=True)
    db = DatabaseWrapper(db_config)
    try:
        db.execute("CREATE TABLE db_wrapper_test(id int null, name varchar(64) null)")
        # ORACLE写法：db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(:1, :2)", (1, 'abc'))
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (1, 'abc'))
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (2, 'def'))
        db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (3, 'ghi'))
        df = db.query("SELECT * FROM db_wrapper_test WHERE id BETWEEN %s AND %s", (0, 4), QueryResultType.PANDAS)
        # 行数及列数
        assert df.shape[0] == 3
        assert df.shape[1] == 2
        json_result = db.query("SELECT * FROM db_wrapper_test WHERE id BETWEEN %s AND %s", (0, 4), QueryResultType.JSON)
        assert len(json_result) == 3
        assert len(json_result[0].keys()) == 2
        dict_result = db.query("SELECT * FROM db_wrapper_test WHERE id BETWEEN %s AND %s", (0, 4), QueryResultType.DICT)
        assert len(dict_result) == 3
        assert len(dict_result[0].keys()) == 2

        class DbWrapperTest(object):
            def __init__(self):
                self._id = None
                self._name = None

            @property
            def id(self):
                return self._id

            @id.setter
            def id(self, id):
                self._id = id

            @property
            def name(self):
                return self._name

            @name.setter
            def name(self, name):
                self._name = name

        bean_result = db.query("SELECT * FROM db_wrapper_test WHERE id BETWEEN %s AND %s", (0, 4), QueryResultType.BEAN,
                               DbWrapperTest)
        assert len(bean_result) == 3
        assert bean_result[0].id == 1
        # 因为设置了自动提交，所以不再手动调用commit()
    except Exception as e:
        raise RuntimeError(e)
    finally:
        db.execute("DROP TABLE db_wrapper_test")
        db.close()


if __name__ == "__main__":
    pytest.main(["-q", os.path.basename(sys.argv[0])])
