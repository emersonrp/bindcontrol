#!/usr/sbin/python
import wx
from BLF import BLF

def test_blf_silent():
    tmpapp = wx.App()

    assert BLF() is "bindloadfilesilent"

    config = wx.FileConfig()
    wx.ConfigBase.Set(config)
    config.WriteBool('VerboseBLF', True)

    assert BLF() is "bindloadfile"

    config.DeleteAll()
