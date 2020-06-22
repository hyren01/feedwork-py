#!/usr/bin/env python
# -*- coding:utf-8 -*-
from feedwork.utils import logger
import feedwork.utils.UuidHelper as uuidu
from feedwork.database.bean.database_config import DatabaseConfig
from feedwork.database.enum.conn_way import ConnWay
from feedwork.database.dbinfo_conf import dbinfo
from feedwork.database.enum.query_result_type import QueryResultType
from feedwork.database.enum.database_type import DatabaseType

import time
import json
import pandas as pd


class DatabaseWrapper(object):

    # PYTHON天然不支持多个构造器，导致JAVA中重载类构造函数的写法变更为PYTHON构造函数中默认参数的实现方式，在实际使用角度，
    # 此时若不传递builder参数，则认为使用默认的builder参数、dbinfo从配置文件中读取，因此原文中的内部类及构造器Builder无
    # 法按原设计来写，所以Builder类修改为DataBaseConfig类，该类作为属性类使用。
    def __init__(self, dbconfig: DatabaseConfig = DatabaseConfig()):

        # __NULL_FETCH_SIZE = -238949899  # 随便一个不会被用到的数字

        # 若DatabaseWrapper用于创建单次连接，则配置文件中的数据库信息不应该被设置为使用连接池，所以new一万次DatabaseWrapper不会构造一次连接池
        # 若DatabaseWrapper用于创建连接池，init_database_pool对象只会初始化一次连接池，所以不管该对象会new一万次还是放在全局变量使用都只会初始化一次连接池
        if dbconfig.dbinfo is None:
            self.dbinfo = dbinfo.get(dbconfig.name)
        else:
            self.dbinfo = dbconfig.dbinfo

        if self.dbinfo is None:
            raise RuntimeError(f"Can not get database conf info by name {dbconfig.name}")

        if dbconfig.need_id:   # 需要id
            self.id = uuidu.guid()
        else:
            self.id = ""

        self.desc = dbconfig.desc
        self.is_lazy_connect = dbconfig.lazy_connect
        self.conn = dbconfig.conn

        # 内部值
        # self.is_begin_transed = False
        self.is_commited = False
        # self.is_rollbacked = False
        # self.commit_count = 0

        # 用于管理数据库连接过程中的状态所使用的变量，主要用于兼容各个数据库及数据库连接对象。该变量存储不同数据库连接对象的引用。
        # 该对象其实是一个原始的数据库连接，它跟self.conn变量的区别是：self.conn变量有可能是数据库连接池所提供的连接，非原始连接
        self.__conn_origin = None

        if DatabaseType.PGSQL.value == self.dbinfo.dbtype:
            from feedwork.database.nature.pgsql_implement import PGSQLImplement as database_manager
        elif DatabaseType.MYSQL.value == self.dbinfo.dbtype:
            from feedwork.database.nature.mysql_implement import MYSQLImplement as database_manager
        elif DatabaseType.ORACLE.value == self.dbinfo.dbtype:
            from feedwork.database.nature.oracle_implement import ORACLEImplement as database_manager
        else:
            raise RuntimeError(f"Unsupported database type {self.dbinfo.dbtype}")
        self.database_manager = database_manager()

        if self.is_lazy_connect is False:
            self.__setup_connection()
            # if self.auto_commit is not True:
            #     self.begin_transaction()

    def begin_transaction(self):
        """
        开启数据库连接的事务。当数据库连接已经关闭时抛出RuntimeError异常。

        """
        # conn.closed不反映服务器关闭/切断的连接。它仅表示客户端使用connection.close()关闭的连接
        if self.is_closed():
            raise RuntimeError("The connection is closed before begin transaction!")
        if self.dbinfo.autocommit is False:
            logger.warning("Already begin transaction")
            return

        self.database_manager.get_or_set_autocommit(self.__conn_origin, False)

        self.is_commited = False
        # self.is_auto_commit = False
        # self.is_begin_transed = True

    @staticmethod
    def __transform_sql(sql):
        # python中的占位符都为%s，且不管是数值型还是字符型
        sql = str.replace(sql, '?', '%s')
        return sql

    def execute(self, sql: str, params: tuple = ()):
        """
        执行SQL的增加、删除、修改操作。

        :param sql: str.操作数据库的SQL语句，包含：INSERT INTO、DELETE、UPDATE。
        :param params: tuple.SQL语句的参数
        :return int.SQL执行后影响的行数。
        """
        # sql = DatabaseWrapper.__transform_sql(sql)
        if self.dbinfo.show_sql_time:
            start_time = time.time()
        self.cursor.execute(sql, params)
        if self.dbinfo.show_sql:
            logger.info(f"{self.id} execute sql: [{sql}]")
        if self.dbinfo.show_sql_time:
            sql_execute_time = time.time() - start_time
            if 0 < self.dbinfo.longtime_sql < sql_execute_time:
                logger.warning(f"{self.id} [LONGTIME SQL(EXECUTE)] elapse time {sql_execute_time}s, sql=[ {sql} ]")

        """Number of rows read from the backend in the last command."""
        return self.cursor.rowcount

    # TODO 提供queryResultSet 使用fetchone和yield
    def query(self, sql: str, params: tuple = (), result_type: QueryResultType = QueryResultType.PANDAS,
              wild_class=None):
        """
        执行SQL的查询操作。当传入的result_type参数不为PANDAS、DICT、JSON、BEAN、DB_NATURE时抛出RuntimeError异常。

        :param sql: str.查询数据库的SQL语句，包含：SELECT。
        :param params: tuple.SQL语句的参数
        :param result_type: QueryResultType.返回的结果集类型，默认为Pandas
        :param wild_class: object.当result_type参数为QueryResultType.BEAN时必须要传入的参数，表示要返回bean类
        :return object，根据result_type参数返回不同的对象。
        """
        if self.is_closed():
            raise RuntimeError("Status error, Connection is closed before query!")

        if result_type == QueryResultType.PANDAS:
            # return pd.read_sql_query(con=self.conn, sql=sql, params=params, chunksize=self.fetch_size)
            return pd.read_sql_query(con=self.conn, sql=sql, params=params)

        self.cursor.execute(sql, params)
        result = self.database_manager.transform_result(self.cursor, self.dbinfo.fetch_size)

        if result_type is None or result_type in [QueryResultType.JSON, QueryResultType.DICT]:
            return json.loads(json.dumps(result, ensure_ascii=False))
        elif result_type == QueryResultType.BEAN:
            if wild_class is None:
                raise RuntimeError("The parameter wild_class must be not none!")
            bean_list = DatabaseWrapper.__db_result_2_beans(wild_class, result)
            return bean_list
        elif result_type == QueryResultType.DB_NATURE:
            return result
        else:
            raise RuntimeError(f"Unsupported result type {result_type.value}")

    def commit(self):
        """
        提交事务，适用于已经开启事务的情况下使用。当数据库连接已经关闭时抛出RuntimeError异常。

        """
        if self.is_closed():
            raise RuntimeError("Status error, Connection is closed before commit!")
        if self.dbinfo.autocommit is False:
            self.conn.commit()
            self.is_commited = True
            # self.commit_count += 1
            if self.dbinfo.show_sql:
                logger.info(f"{self.id} Trans commit")
        else:
            logger.warning("")

    def close(self):
        """
        关闭数据库连接。当数据库连接没有构建或者已经关闭时抛出RuntimeError异常。
        该方法在开启事务且没有提交事务的情况下会自动执行回滚操作。

        """
        if self.is_closed():
            raise RuntimeError("Status error, Connection already closed!")
        # 意味着在开启事务状态下（默认开启）使用者必须手动提交事务
        # # FIXME 这个处理代码没有意义。代码中的多段事务就失效了。如果想有用，需要结合execute中设置的标志
        # if self.is_autocommit() is False and self.is_commited is False:
        #     logger.error(f"{self.id} Transaction has unhandled, auto rollback before close")
        #     self.conn.rollback()

        self.cursor.close()
        self.conn.close()
        logger.info(f"{self.id} close success")

    def rollback(self):
        """
        数据库操作回滚。当数据库连接没有构建或者已经关闭时抛出RuntimeError异常。
        该方法在该次连接为非自动提交时才会调用rollback()方法。

        """
        if self.is_closed():
            raise RuntimeError("Status error, Connection alredy closed!")
        if self.dbinfo.autocommit is False:
            self.conn.rollback()
            # self.is_rollbacked = True
            logger.info(f"{self.id} Transaction is rollback")
        else:
            logger.warning("The connection is autocommit, Please do not rollback")

    def is_closed(self):
        """
        获取当前连接是否是已经关闭的状态。当数据库连接没有构建时抛出RuntimeError异常。

        :return bool，连接是否已经关闭True/False
        """
        if self.conn is None:
            raise RuntimeError("Status error, No connect!")

        return self.database_manager.is_closed(self.__conn_origin)

    # 本方法非特殊情况，不应该被使用！！！
    def _is_autocommit(self):
        """
        获取当前连接是否自动提交的状态。当数据库连接没有构建时抛出RuntimeError异常。

        :return bool，连接是否自动提交True/False
        """
        if self.is_closed():
            raise RuntimeError("Status error, No connect!")

        return self.database_manager.get_or_set_autocommit(self.__conn_origin)

    # def make_connection(self):
    #     if self.is_lazy_connect:
    #         self.__setup_connection()

    def __setup_connection(self):
        """
        创建数据库连接。当数据库连接无法构建时抛出RuntimeError异常。

        """
        # 当连接不为空时，意味着使用者通过构造器构造了连接，导致重复调用该方法，所以此处直接返回，不抛出异常
        if self.conn is not None:
            logger.trace(f"{self.id} reuse  autocommit={self.conn.autocommit}")
            return
        dbinfo = self.dbinfo
        try:
            start_time = time.time()
            if ConnWay.DIRECTLY.value == dbinfo.way:
                dsn = dbinfo.host + ":" + str(dbinfo.port) + "/" + dbinfo.dbname
                self.conn = self.database_manager.create_connection(dbinfo.host, dbinfo.port, dbinfo.dbname,
                                                                    dbinfo.username, dbinfo.password, dsn)
                self.__conn_origin = self.conn
            elif ConnWay.POOL.value == dbinfo.way:
                from feedwork.database.init_database_pool import database_pool
                self.conn = database_pool[dbinfo.name].connection()
                # 连接池会对数据库连接进行封装，以下代码能拿到原始的数据库连接，从而能知道数据库连接的相关状态。该连接池没有提供状态查询接口
                # 因为存储的是对象引用，所以可以直接修改该变量，从而修改数据库连接对象
                self.__conn_origin = self.conn._con._con
            else:
                raise RuntimeError(f"{dbinfo.way} connection way is not support!")

            self.cursor = self.conn.cursor()

            logger.info(f"{self.id} new connection by {dbinfo.way} {self.desc} autocommit  -> {dbinfo.autocommit}")

            if dbinfo.show_conn_time:
                logger.info(f"{self.id} database connection spend {time.time() - start_time}s")

        except Exception as e:
            raise RuntimeError(f"{dbinfo.name} can not connect to database! {e}")

        if dbinfo.autocommit:
            self.database_manager.get_or_set_autocommit(self.__conn_origin, True)
        else:
            self.begin_transaction()

        logger.debug(f"{self.id} connection setup success")

    @staticmethod
    def __db_result_2_beans(bean_class, db_result):
        """
        查询数据库出的结果集转换为bean。

        :param bean_class.object，要创建的Bean类
        :param db_result.object，数据库结果集
        """
        list_result = []
        for row in db_result:
            sci = bean_class()
            for key in row:
                # bean中的key是小写，主要针对数据库返回的字段是大写的问题
                sci.__setattr__(key.lower(), row[key])
            list_result.append(sci)
        return list_result
