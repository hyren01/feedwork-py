# -*- coding:utf-8 -*-
from abc import abstractmethod, ABCMeta
from feedwork.database.bean.database_info import Dbinfo


class DatabaseInterface(metaclass=ABCMeta):

    @abstractmethod
    def create_connection(self, db_host, db_port, db_name, username, password, dsn):
        """
        创建数据库连接，目前仅支持postgresql、mysql、oracle，否则抛出RuntimeError异常。

        :param db_host: str.数据库连接地址
        :param db_port: int.数据库连接端口
        :param db_name: str.数据库名/schema
        :param username: str.数据库用户名
        :param password: str.数据库密码
        :param dsn: str.可能用于oracle数据库
        :return object（各种数据库的Connection），数据库连接对象。
        """
        pass

    @abstractmethod
    def transform_result(self, cursor, fetch_size):
        pass

    @abstractmethod
    def get_or_set_autocommit(self, origin_conn, autocommit=None):
        """
        获取或者设置数据库连接的autocommit属性（用于事务处理），目前仅支持postgresql、mysql、oracle，否则抛出RuntimeError异常。
        当autocommit为False时，该函数设置当前connection的autocommit属性（开启事务）。

        :param origin_conn: object.各种数据库的原始Connection，不直接支持来源是数据库连接池的Connection。
        :param autocommit: bool.是否自动提交
        :return object（各种数据库的Connection），当autocommit为None时，该函数返回当前connection的autocommit属性。
        """
        pass

    @abstractmethod
    def is_closed(self, origin_conn):
        """
        获取数据库连接的closed属性（用于检测连接是否关闭），目前仅支持postgresql、mysql、oracle，否则抛出RuntimeError异常。

        :param origin_conn: object.各种数据库的原始Connection，不直接支持来源是数据库连接池的Connection。
        :return bool，数据库连接是否已经关闭。
        """
        pass

    @abstractmethod
    def create_database_pool(self, creator, dbconf: Dbinfo):
        pass
