import wx
from BLF import BLF

def test_blf_silent(monkeypatch):
    _ = wx.App()

    assert BLF() == "bindloadfilesilent"

    config = wx.FileConfig()
    monkeypatch.setattr(config, 'ReadBool', lambda _: True)
    wx.ConfigBase.Set(config)

    assert BLF() == "bindloadfile"

    config.DeleteAll()
