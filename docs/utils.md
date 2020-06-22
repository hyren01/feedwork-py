## 工具类说明

| 工具类  | 功能           | 详细说明                                |
| ---------- | ---------------- | ------------------------------------------- |
| logger     | 日志处理     | from feedwork.utils import logger <br> logger.debug("......") |
| Constant   | 定义程序中的常量 | import feedwork.utils.Constant as const <br> const.NAME = "fd" # 定义了一个常量 |
| DateHelper | 日期时间处理 | import feedwork.utils.DateHelper as dateu <br> dateu.sys_date()  # 得到系统当前日期 |
| FileHelper | 文件处理 | import feedwork.utils.FileHelper as fileu <br> fileu.cat_path("/", "path", "sub", "file.md")  # 代替os.join |
| StringHelper | 字符串处理 | 包括空串判断等工具函数 <br> import feedwork.utils.StringHelper as stru |
| System | 操作系统环境处理 | import feedwork.utils.System as sysu <br> PATH = sysu.env("PATH", str)  # 得到PATH环境变量 |
