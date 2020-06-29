## database模块使用说明
如果使用配置文件连接数据库的方式：
- 设置环境变量： HRS_RESOURCES_ROOT
  * 指定所有资源文件在本机的存放根目录
  * 该目录下至少包括一个目录：fdconfig
- 创建conf文件： fdconfig/dbinfo.conf
  * 在这个文件中填写数据库连接信息。例如：

```yaml
# 每组配置使用 name 进行区别。在程序中，通过 name 获取不同的数据库连接
databases :
  -
    name       : default
    way        : POOL
    dbtype     : POSTGRESQL
    host       : 127.0.0.1
    port       : 5432
    dbname     : postgres
    username   : postgres
    password   : q1w2e3
    autocommit : no
    disable    : no
    minPoolSize: 10
    maxPoolSize: 10
    fetch_size : 200
    max_rows   : 1000
    fetch_direction : 1
    query_timeout   : 1000
    max_result_rows : -1        # 结果集最大允许多少条。-1为不受限制
    show_sql        : yes       # 在execute、query操作中显示sql
    show_conn_time  : no        # 是否显示数据连接的时间消耗
    show_sql_time   : yes       # 是否显示sql执行时间
    longtime_sql    : 10000     # 10秒。SQL执行时间超过这个值的，显示到日志中

```

##### 使用配置文件方式连接数据库：
```
from feedwork.database.database_wrapper import DatabaseWrapper
from feedwork.database.enum.query_result_type import QueryResultType


db = DatabaseWrapper()
try:
    db.execute("CREATE TABLE db_wrapper_test(id int null, name varchar(64) null)")
    # oracle的写法：db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(:1, :2)", (1, 'abc'))
    inser_num = db.execute("INSERT INTO db_wrapper_test(id, name) VALUES(%s, %s)", (1, 'abc'))
    update_num = db.execute("UPDATE db_wrapper_test SET name = %s WHERE id = %s", ('def', 1))
    delete_num = db.execute("DELETE FROM db_wrapper_test")
    df = db.query("SELECT * FROM db_wrapper_test WHERE id BETWEEN %s AND %s", (0, 4), QueryResultType.PANDAS)
    # 行数及列数
    assert df.shape[0] == 0
    assert df.shape[1] == 2
    # 对于pgsql来说，CREATE TABLE不在事务控制范围内；对于mysql来说，CREATE TABLE、DROP TABLE不在事务控制范围内
    # oracle语法不支持DROP TABLE IF EXISTS
    db.execute("DROP TABLE db_wrapper_test")
    db.commit()
except Exception as e:
    db.rollback()
    raise RuntimeError(e)
finally:
    db.close()
```
##### 使用编程方式连接数据库：
```
from feedwork.database.database_wrapper import DatabaseWrapper
from feedwork.database.enum.conn_way import ConnWay
from feedwork.database.enum.database_type import DatabaseType
from feedwork.database.bean.database_info import Dbinfo
from feedwork.database.bean.database_config import DatabaseConfig


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
    
db_config = __set_dbinfo()
db = DatabaseWrapper(dbconfig=db_config)
# 具体数据库操作同上
```
##### 在使用配置文件连接数据库情况下，在多数据库连接中指定连接进行数据库操作：
```
from feedwork.database.database_wrapper import DatabaseWrapper


# 指定配置文件中名字为mysql的数据库连接
db = DatabaseWrapper(name="mysql")
# 具体数据库操作不变
```
或者
```
from feedwork.database.database_wrapper import DatabaseWrapper
from feedwork.database.bean.database_config import DatabaseConfig


# 指定配置文件中名字为mysql的数据库连接
db_config = DatabaseConfig()
db_config.name = "mysql"
db_config.need_id = True
db_config.desc = "测试用"

db = DatabaseWrapper(dbconfig=db_config)
# 具体数据库操作不变
```
##### 使用自建的数据库连接：
```
from feedwork.database.database_wrapper import DatabaseWrapper
from feedwork.database.bean.database_config import DatabaseConfig
import pymysql


# 指定配置文件中名字为mysql的数据库连接
db_config = DatabaseConfig()
db_config.name = "mysql"
db_config.need_id = True
db_config.desc = "测试用"
db_config.conn = pymysql.connect(host="", port=3306, user="", passwd="", db="")

db = DatabaseWrapper(db_config)
# 具体数据库操作不变
```