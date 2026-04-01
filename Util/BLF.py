import wx

def BLF() -> str:
    return "bindloadfile" if wx.ConfigBase.Get().ReadBool('VerboseBLF') else 'bindloadfilesilent'
