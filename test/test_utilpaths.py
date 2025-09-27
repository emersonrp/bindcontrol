import wx
import os
import sys
from pathlib import Path
import pytest
from Util.Paths import ProfilePath, GetRootDirPath, CheckProfileForBindsDir, GetProfileFileForName, GetAllProfileBindsDirs

def test_CheckProfileForBindsDir(config, tmp_path):
    # CheckProfileForBindsDir
    pdir = tmp_path / 'fubble'
    pdir.mkdir(exist_ok = True)
    file = pdir / 'bcprofileid.txt'
    file.write_text('Mister Fubble')
    assert CheckProfileForBindsDir(config, 'fubble') == 'Mister Fubble'
    file.unlink()
    pdir.rmdir()

def test_GetProfileFileForName(config, tmp_path):
    # GetProfileFileForName
    file = tmp_path / 'fubble.bcp'
    file.write_text('freebird')
    assert str(GetProfileFileForName(config, 'fubble')) == f'{tmp_path}/fubble.bcp'
    file.unlink()

def test_GetAllProfileBindsDirs(config, tmp_path):
    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.mkdir(exist_ok = True)

    assert sorted(GetAllProfileBindsDirs(config)) == sorted(['inky', 'pinky', 'blinky', 'clyde'])

    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.rmdir()

def test_ProfilePath(config, tmp_path):
    assert ProfilePath(config) == tmp_path

def test_GetRootDirPath(monkeypatch, tmp_path):
    assert GetRootDirPath() == Path(os.path.abspath(__file__)).parent.parent
    # TODO - if we use MEIPASS at any other point in the test suite
    # we need to have undone this somehow.  monkeypatch doesn't work.
    setattr(sys, '_MEIPASS', tmp_path)
    assert GetRootDirPath() == Path(tmp_path)

#########
@pytest.fixture(autouse = True)
def config(tmp_path, monkeypatch):
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    monkeypatch.setattr(config, 'Read', lambda _: str(tmp_path))

    yield config

    config.DeleteAll()
