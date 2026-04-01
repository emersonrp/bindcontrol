import wx

Labels: dict[str, str] = {
    'ResetKey': 'Binds Reset Key',
}

def COHFont(pointsize:int = 12) -> wx.Font:
    return wx.Font(wx.FontInfo(pointsize).FaceName('Montreal-DemiBold'))
