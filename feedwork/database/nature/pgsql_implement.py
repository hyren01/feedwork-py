# -*- coding:utf-8 -*-
from feedwork.database.bean.database_info import Dbinfo
from feedwork.database.nature.database_interface import DatabaseInterface
import psycopg2
import psycopg2.extras


class PGSQLImplement(DatabaseInterface):

    def create_connection(self, db_host: str, db_port: int, db_name: str, username: str, password: str, dsn):
        conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=username, password=password,
                                cursor_factory=psycopg2.extras.RealDictCursor)
        return conn

    def transform_result(self, cursor, fetch_size):
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
            return origin_conn.autocommit
        origin_conn.autocommit = autocommit

    def is_closed(self, origin_conn):
        return False if origin_conn.closed == 0 else True

    def create_database_pool(self, creator, dbconf: Dbinfo):
        from DBUtils.PooledDB import PooledDB
        pool = PooledDB(
            creator=creator,  # 使用链接数据库的模块
            maxconnections=0,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=dbconf.minPoolSize,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建  启动时开启的空连接数量
            maxcached=dbconf.maxPoolSize,  # 链接池中最多闲置的链接，0和None不限制   连接池最大可用连接数量
            maxshared=0, # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[] if dbconf.set_session is None else dbconf.set_session,
            # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=0, # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
            host=dbconf.host,
            port=dbconf.port,
            user=dbconf.username,
            password=dbconf.password,
            database=dbconf.dbname)

        return pool
