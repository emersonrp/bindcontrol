import wx
import os, sys
from pathlib import Path
from unittest.mock import Mock
from Util.Paths import ProfilePath, GetRootDirPath, CheckProfileForBindsDir, GetProfileFileForName, GetAllProfileBindsDirs

def test_CheckProfileForBindsDir(tmp_path):
    _, config = doSetup(tmp_path)

    # CheckProfileForBindsDir
    pdir = tmp_path / 'fubble'
    pdir.mkdir(exist_ok = True)
    file = pdir / 'bcprofileid.txt'
    file.write_text('Mister Fubble')
    assert CheckProfileForBindsDir(config, 'fubble') == 'Mister Fubble'
    file.unlink()
    pdir.rmdir()

    config.DeleteAll()

def test_GetProfileFileForName(tmp_path):
    _, config = doSetup(tmp_path)

    # GetProfileFileForName
    file = tmp_path / 'fubble.bcp'
    file.write_text('freebird')
    assert str(GetProfileFileForName(config, 'fubble')) == f'{tmp_path}/fubble.bcp'
    file.unlink()

    config.DeleteAll()

def test_GetAllProfileBindsDirs(tmp_path):
    _, config = doSetup(tmp_path)

    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.mkdir(exist_ok = True)

    assert sorted(GetAllProfileBindsDirs(config)) == sorted(['inky', 'pinky', 'blinky', 'clyde'])

    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.rmdir()

    config.DeleteAll()

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

