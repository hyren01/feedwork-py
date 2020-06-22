import os
from os.path import dirname, normcase


def isfile(file: str) -> bool:
    return os.path.isfile(file)


def isdir(file: str) -> bool:
    return os.path.isdir(file)


def cat_path(base, *paths, **kwargs) -> str:
    """
    连接多个路径到base,返回规范化的绝对路径名。
    默认不检查文件/目录是否真实存在。
    如果需要同时做检查，最后一个参数输入check_exist='file' or 'dir'。例如：
        cat_path("/", "usr", "local", check_exist='dir')
        cat_path("/", "etc", "passwd", check_exist='file')
    """
    final_path = os.path.abspath(os.path.join(base, *paths))
    base_path = os.path.abspath(base)
    # 确保final_path以base_path开始
    # 在不区分大小写的操作系统（如Windows）上使用normcase以确保不会初始判断失误
    # 此外，以下条件之一必须为 true：
    # 1. 下一个字符是路径分隔符（以防止安全连接（“/dir”，“/../d”）等条件）
    # 2. final_path必须与base_path相同
    # 3. base_path必须是最根路径（表示“/”或c:\\”）
    if (not normcase(final_path).startswith(normcase(base_path + os.path.sep)) and
            normcase(final_path) != normcase(base_path) and
            dirname(normcase(base_path)) != normcase(base_path)):
        raise RuntimeError(
            f'The joined path ({final_path}) is located outside of the base path component ({base_path})')
    if kwargs:
        check_exist = kwargs.get('check_exist')
        if check_exist == 'dir':
            if not os.path.isdir(final_path):
                raise RuntimeError(f"({final_path}) is not regular dir !")
        elif check_exist == 'file':
            if not os.path.isfile(final_path):
                raise RuntimeError(f"({final_path}) is not regular file !")
    return final_path


def linecount(file) -> int:
    """
    得到文件的行数
    :param file: 文件全路经名或文件对象
    :return: 文件行数
    """

    def _linecount(fileObj) -> int:
        count = 0
        for _ in fileObj:
            count += 1
        return count

    # for count, line in enumerate(open(file_path)): pass
    if type(file) is str:
        with open(file, 'r') as f:
            return _linecount(f)
    else:
        return _linecount(file)


def size(filepath, readable=False):
    """
    得到文件大小
    :param filepath: 文件全路径
    :param readable: 是否返回带有计数单位的可读结果
    :return: 文件大小。数字，或带有KB/MB单位的文件大小
    """
    fstat = os.stat(filepath)
    fsize = fstat.st_size
    if readable:
        sizeMB = 1024 * 1024
        if fsize < sizeMB:
            return f"{fsize / 1024:.2f} KB"
        else:
            return f"{fsize / sizeMB:.2f} MB"
    else:
        return fsize


def readForString(file) -> str:
    if not isfile(file):
        return None
    with open(file, "r") as f:
        content = f.read()
    return content


def write(file, content, append=False) -> bool:
    """
    覆盖或追加写入文件
    :param file: 文件全路径或文件对象
    :param content: 写入的文本
    :param append: 是否为追加模式。如果file参数是文件对象，会忽略本参数
    :return: None
    """
    if type(file) is str:
        if not isfile(file):
            return False
        mode = 'a' if append else 'w'
        with open(file, mode) as f:
            f.write(content)
    else:
        file.write(content)
    return True
