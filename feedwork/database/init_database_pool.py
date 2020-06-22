# -*- coding:utf-8 -*-
from feedwork.database.enum.database_type import DatabaseType
from types import MappingProxyType
from feedwork.database.enum.conn_way import ConnWay
from feedwork.database.dbinfo_conf import dbinfo as database_info


default_dbname = "default"

__database_pool_tmp = {}
for name, dbinfo_tmp in database_info.items():
    if DatabaseType.PGSQL.value == dbinfo_tmp.dbtype:
        import psycopg2 as creator
        from feedwork.database.nature.pgsql_implement import PGSQLImplement
        database_implement = PGSQLImplement()
    elif DatabaseType.MYSQL.value == dbinfo_tmp.dbtype:
        import pymysql as creator
        from feedwork.database.nature.mysql_implement import MYSQLImplement
        database_implement = MYSQLImplement()
    elif DatabaseType.ORACLE.value == dbinfo_tmp.dbtype:
        import cx_Oracle as creator
        from feedwork.database.nature.oracle_implement import ORACLEImplement
        database_implement = ORACLEImplement()
    else:
        raise RuntimeError(f"Can not supported database type: {dbinfo_tmp.dbtype}")

    if dbinfo_tmp.way == ConnWay.POOL.value:
        __database_pool_tmp[name] = database_implement.create_database_pool(creator, dbinfo_tmp)

# python官方使用代理模式，代理使用字典，并且拦截了字典的修改请求，以此来实现字典的不可修改能力
database_pool = MappingProxyType(__database_pool_tmp)
