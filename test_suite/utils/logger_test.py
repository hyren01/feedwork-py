import os
import sys

import pytest
import datetime


def test_mylog():
    os.environ['HR_RUN_PROD'] = "y"
    os.environ['HR_LOG_FILE'] = "/tmp/logger-test.log"
    os.environ['HR_LOG_FILE_LEVEL'] = "ERROR"
    os.environ['HR_LOG_CONSOLE'] = "y"
    from feedwork.utils import logger

    logger.debug(f"调试 {datetime.datetime.now()}")
    logger.info(f"信息提示 {datetime.datetime.now()}")
    logger.warning(f"警告 =======  {datetime.datetime.now()}")
    logger.error(f"错误 !!!!!!  {datetime.datetime.now()}")


def test_loguru():
    os.environ['LOGURU_LEVEL'] = "INFO"
    from loguru import logger

    logger.debug(f"调试 {datetime.datetime.now()}")
    logger.info(f"信息提示 {datetime.datetime.now()}")
    logger.warning(f"警告 =======  {datetime.datetime.now()}")
    logger.error(f"错误 !!!!!!  {datetime.datetime.now()}")


test_mylog()
# @logger.catch
# def func(x, y, z):
#     return 1 / (x + y + z)


# func(1, -1, 0)

if __name__ == "__main__":
    pytest.main(["-q", os.path.basename(sys.argv[0])])
