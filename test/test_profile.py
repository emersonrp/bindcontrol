#!/usr/sbin/python
import wx
import Profile
from unittest.mock import MagicMock
from pathlib import Path

def test_CheckProfileForBindsDir(tmp_path):
    # setup
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    config.Read = MagicMock(return_value = str(tmp_path))

    # CheckProfileForBindsDir
    pdir = tmp_path / 'fubble'
    pdir.mkdir(exist_ok = True)
    file = pdir / 'bcprofileid.txt'
    file.write_text('Mister Fubble')
    assert Profile.CheckProfileForBindsDir('fubble') == 'Mister Fubble'
    file.unlink()
    pdir.rmdir()

def test_GetProfileFileForName(tmp_path):
    # setup
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    config.Read = MagicMock(return_value = str(tmp_path))

    # GetProfileFileForName
    file = tmp_path / 'fubble.bcp'
    file.write_text('freebird')
    assert str(Profile.GetProfileFileForName('fubble')) == f'{tmp_path}/fubble.bcp'
    file.unlink()

    config.DeleteAll()

def test_GetAllProfileBindsDirs(tmp_path):
    # setup
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    config.Read = MagicMock(return_value = str(tmp_path))
    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.mkdir(exist_ok = True)

    assert sorted(Profile.GetAllProfileBindsDirs()) == sorted(['inky', 'pinky', 'blinky', 'clyde'])

    for d in ['inky', 'pinky', 'blinky', 'clyde']:
        pdir = tmp_path / d
        pdir.rmdir()

    config.DeleteAll()

def test_ProfilePath(tmp_path):
    _ = wx.App()
    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    config.Read = MagicMock(return_value = str(tmp_path))

    assert Profile.ProfilePath() == tmp_path

    config.DeleteAll()
