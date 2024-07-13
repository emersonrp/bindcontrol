#!/usr/sbin/python
import wx
from BLF import BLF
from unittest.mock import MagicMock

def test_blf_silent():
    _ = wx.App()

    assert BLF() is "bindloadfilesilent"

    config = wx.FileConfig()
    config.ReadBool = MagicMock(return_value = True)
    wx.ConfigBase.Set(config)

    assert BLF() is "bindloadfile"

    config.DeleteAll()
