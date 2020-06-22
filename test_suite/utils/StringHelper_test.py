import os
import sys
import time

import pytest

import feedwork.utils.StringHelper as stru


def test_isBlank():
    assert stru.isBlank(None)
    assert stru.isBlank("")
    assert stru.isBlank(" ")
    assert stru.isBlank("\t \r\n \r \n")
    assert not stru.isBlank("a")
    with pytest.raises(AssertionError):
        stru.isBlank(1)


def test_isNotBlank():
    assert not stru.isNotBlank(None)
    assert not stru.isNotBlank("")
    assert not stru.isNotBlank(" ")
    assert not stru.isNotBlank("\t \r\n \r \n")
    assert stru.isNotBlank("a")
    with pytest.raises(AssertionError):
        stru.isNotBlank(1)


if __name__ == "__main__":
    pytest.main(["-q", os.path.basename(sys.argv[0])])
