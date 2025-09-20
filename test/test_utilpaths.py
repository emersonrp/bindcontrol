import wx
import os, sys
from pathlib import Path
from unittest.mock import Mock
from Util.Paths import ProfilePath, GetRootDirPath

def test_ProfilePath(tmp_path):
    _, config = doSetup(tmp_path)

    assert ProfilePath(config) == tmp_path

    config.DeleteAll()

def test_GetRootDirPath(tmp_path):
    assert GetRootDirPath() == Path(os.path.abspath(__file__)).parent.parent
    setattr(sys, '_MEIPASS', tmp_path)
    assert GetRootDirPath() == Path(tmp_path)

#########
def doSetup(tmp_path):
    app = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    config.Read = Mock(return_value = str(tmp_path))

    return app, config

