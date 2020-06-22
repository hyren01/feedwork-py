def isBlank(string: str):
    if string is None:
        return True
    assert isinstance(string, str)
    if string.strip() == '':
        return True

    return False


def isNotBlank(string: str):
    if string is None:
        return False
    assert isinstance(string, str)
    if len(string.strip()) > 0:
        return True
    else:
        return False

