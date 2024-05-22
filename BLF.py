import wx

def BLF():
    return "bindloadfile" if wx.ConfigBase.Get().ReadBool('VerboseBLF') else 'bindloadfilesilent'
