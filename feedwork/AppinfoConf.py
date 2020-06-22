import os
import feedwork.utils.ConfigHelper as confu

appinfo = confu.load_conf("appinfo.conf")


def __algor_get(key: str):
    algor = appinfo.get('algor')
    if algor is None:
        return os.path.join(confu.HRS_RESOURCES_ROOT, key)
    if not isinstance(algor, dict):
        raise ValueError(f"'algor' must be dict !")
    return algor.get(key, os.path.join(confu.HRS_RESOURCES_ROOT, key))


# 自己训练出来的模型存放路径
ALGOR_MODULE_ROOT = __algor_get("module")
# bert 等预训练模型存放路径
ALGOR_PRETRAIN_ROOT = __algor_get("pretrain")
