import BindControl
import pytest
import wx

from pathlib import Path
from Util.DefaultProfile import DefaultProfile

def test_create_main_no_config(config):
    _ = BindControl.Main(None)
    stdpaths = wx.StandardPaths.Get()

    assert config.Read('GameLang') == 'English'
    assert config.Read('ResetKey') == 'CTRL+R'
    assert config.ReadBool('UseSplitModKeys') is False
    assert config.ReadBool('FlushAllBinds')
    assert config.Read('ProfilePath') == str(Path(stdpaths.GetDocumentsDir()) / "bindcontrol")
    assert config.ReadBool('StartWithLastProfile')
    assert config.ReadBool('SaveSizeAndPosition')
    assert config.ReadBool('VerboseBLF') == False
    assert config.ReadBool('CrashOnBindError') == False
    assert config.ReadBool('ShowInspector') == False
    assert config.ReadBool('ShowDebugMessages') == False
    assert config.ReadInt('WinH') == 1000
    assert config.ReadInt('WinW') == 1000
    assert config.Read('DefaultProfile') == DefaultProfile

#####
@pytest.fixture(autouse = True)
def config():
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)

    yield config

    config.DeleteAll()
