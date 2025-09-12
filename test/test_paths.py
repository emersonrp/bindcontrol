#!/usr/sbin/python
import sys, os
from pathlib import Path
from Util.Paths import GetRootDirPath
from unittest.mock import MagicMock

def test_getrootdirpath():

    path = Path(os.path.abspath(__file__)).parent.parent

    assert GetRootDirPath() == path

    setattr(sys, '_MEIPASS', '/tmp/testing')

    assert GetRootDirPath() == Path('/tmp/testing')
