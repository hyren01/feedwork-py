import time
import uuid


def guid():
    return uuid.uuid1().hex


def tiemstamp():
    return str(time.time()).replace('.', '')

