# -*- coding:utf-8 -*-
from feedwork.database.bean.database_info import Dbinfo
from feedwork.database.nature.database_interface import DatabaseInterface
import cx_Oracle


class ORACLEImplement(DatabaseInterface):

    def create_connection(self, db_host: str, db_port: int, db_name: str, username: str, password: str, dsn):
        conn = cx_Oracle.connect(username, password, dsn, encoding='UTF-8')
        return conn

    def transform_result(self, cursor, fetch_size):
        cursor.rowfactory = ORACLEImplement.__make_dictfactory(cursor)
        result = []
        if fetch_size is not None and fetch_size > 0:
            result_tmp = cursor.fetchmany(fetch_size)
            while result_tmp is not None and len(result_tmp) > 0:
                result_tmp = list(result_tmp)
                result = result.__add__(result_tmp)
                result_tmp = cursor.fetchmany(fetch_size)
        else:
            result = cursor.fetchall()

        return result

    def get_or_set_autocommit(self, origin_conn, autocommit=None):
        if autocommit is None:
            return False if origin_conn.autocommit == 0 else True
        origin_conn.autocommit = 1 if autocommit else 0

    def is_closed(self, origin_conn):
        # 这里有问题，原始的oralce连接中没有closed属性
        return type(origin_conn.stmtcachesize) is not int

    def create_database_pool(self, creator, dbconf: Dbinfo):
        from DBUtils.PooledDB import PooledDB
        dsn = dbconf.host + ":" + str(dbconf.port) + "/" + dbconf.dbname
        pool = PooledDB(
            creator=creator,
            maxconnections=0,
            mincached=dbconf.minPoolSize,
            maxcached=dbconf.maxPoolSize,
            maxshared=0,
            blocking=True,
            maxusage=None,
            setsession=[] if dbconf.set_session is None else dbconf.set_session,
            ping=0,
            dsn=dsn,
            user=dbconf.username,
            password=dbconf.password)

        return pool

    @staticmethod
    def __make_dictfactory(cursor):
        column_names = [d[0] for d in cursor.description]

        def create_row(*args):
            return dict(zip(column_names, args))
        return create_row
