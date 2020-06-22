# -*- coding:utf-8 -*-
from feedwork.database.init_database_pool import default_dbname
from feedwork.database.bean.database_info import Dbinfo


class DatabaseConfig(object):

    def __init__(self):
        self._name = default_dbname
        self._desc = ''
        self._lazy_connect = False
        self._dbinfo = None
        self._conn = None
        self._id = None
        self._need_id = True  # noid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc

    @property
    def lazy_connect(self):
        return self._lazy_connect

    @lazy_connect.setter
    def lazy_connect(self, lazy_connect: bool):
        self._lazy_connect = lazy_connect

    @property
    def dbinfo(self):
        return self._dbinfo

    @dbinfo.setter
    def dbinfo(self, dbinfo: Dbinfo):
        self._dbinfo = dbinfo

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, conn):
        self._conn = conn

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def need_id(self):
        return self._need_id

    @need_id.setter
    def need_id(self, need_id: bool):
        self._need_id = need_id
