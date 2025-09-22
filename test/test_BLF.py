#!/usr/sbin/python
import wx
from BLF import BLF

def test_blf_silent(monkeypatch):
    _ = wx.App()

    assert BLF() is "bindloadfilesilent"

    config = wx.FileConfig()
    monkeypatch.setattr(config, 'ReadBool', lambda _: True)
    wx.ConfigBase.Set(config)

    assert BLF() is "bindloadfile"

    config.DeleteAll()
