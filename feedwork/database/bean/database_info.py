# -*- coding:utf-8 -*-
from feedwork.database.enum.conn_way import ConnWay
from feedwork.database.enum.database_type import DatabaseType


class Dbinfo(object):

    def __init__(self, ):
        self._name = None
        # 因为该类是封装dbinfo.conf文件内的参数，文件内配置的是字符串，所以以下两个变量统一用字符串
        self._way = ConnWay.NONE.value
        self._dbtype = DatabaseType.NONE.value
        self._host = None
        self._port = None
        self._dbname = None
        self._username = None
        self._password = None
        self._autocommit = False
        self._minPoolSize = None
        self._maxPoolSize = None
        self._properties = None

        self._set_session = None
        self._charset = None
        # 附加属性
        self._fetch_size = -1   # 不设置fetch_size
        self._max_rows = None
        self._fetch_direction = None
        self._query_timeout = None
        self._max_result_rows = None
        self._show_sql = False
        self._show_conn_time = False
        self._show_sql_time = False
        self._longtime_sql = -1     # 不打印执行时间长的sql

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def way(self):
        return self._way

    @way.setter
    def way(self, way):
        self._way = way

    @property
    def dbtype(self):
        return self._dbtype

    @dbtype.setter
    def dbtype(self, dbtype):
        self._dbtype = dbtype

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port: int):
        self._port = port

    @property
    def dbname(self):
        return self._dbname

    @dbname.setter
    def dbname(self, dbname):
        self._dbname = dbname

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def autocommit(self):
        return self._autocommit

    @autocommit.setter
    def autocommit(self, autocommit: bool):
        self._autocommit = autocommit

    @property
    def minPoolSize(self):
        return self._minPoolSize

    @minPoolSize.setter
    def minPoolSize(self, minPoolSize: int):
        self._minPoolSize = minPoolSize

    @property
    def maxPoolSize(self):
        return self._maxPoolSize

    @maxPoolSize.setter
    def maxPoolSize(self, maxPoolSize: int):
        self._maxPoolSize = maxPoolSize

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties: dict):
        self._properties = properties

    @property
    def set_session(self):
        return self._set_session

    @set_session.setter
    def set_session(self, set_session):
        self._set_session = set_session

    @property
    def charset(self):
        return self._charset

    @charset.setter
    def charset(self, charset):
        self._charset = charset

    @property
    def fetch_size(self):
        return self._fetch_size

    @fetch_size.setter
    def fetch_size(self, fetch_size: int):
        self._fetch_size = fetch_size

    @property
    def max_rows(self):
        return self._max_rows

    @max_rows.setter
    def max_rows(self, max_rows: int):
        self._max_rows = max_rows

    @property
    def fetch_direction(self):
        return self._fetch_direction

    @fetch_direction.setter
    def fetch_direction(self, fetch_direction):
        self._fetch_direction = fetch_direction

    @property
    def query_timeout(self):
        return self._query_timeout

    @query_timeout.setter
    def query_timeout(self, query_timeout: int):
        self._query_timeout = query_timeout

    @property
    def max_result_rows(self):
        return self._max_result_rows

    @max_result_rows.setter
    def max_result_rows(self, max_result_rows: int):
        self._max_result_rows = max_result_rows

    @property
    def show_sql(self):
        return self._show_sql

    @show_sql.setter
    def show_sql(self, show_sql: bool):
        self._show_sql = show_sql

    @property
    def show_conn_time(self):
        return self._show_conn_time

    @show_conn_time.setter
    def show_conn_time(self, show_conn_time: bool):
        self._show_conn_time = show_conn_time

    @property
    def show_sql_time(self):
        return self._show_sql_time

    @show_sql_time.setter
    def show_sql_time(self, show_sql_time: bool):
        self._show_sql_time = show_sql_time

    @property
    def longtime_sql(self):
        return self._longtime_sql

    @longtime_sql.setter
    def longtime_sql(self, longtime_sql: bool):
        self._longtime_sql = longtime_sql
