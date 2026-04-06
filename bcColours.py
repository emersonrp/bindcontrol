import wx

# is there a saner way to do this?

def DarkMode():
    return wx.SystemSettings.GetAppearance().IsDark()

def ErrorColour() -> wx.Colour:
    return wx.Colour(128, 0, 0) if DarkMode() else wx.Colour(255, 200, 200)

def WarningColour() -> wx.Colour:
    return wx.Colour(128, 128, 0) if DarkMode() else wx.Colour(255, 255, 200)

def BlackColour() -> wx.Colour:
    return wx.WHITE if DarkMode() else wx.BLACK

def WhiteColour() -> wx.Colour:
    return wx.BLACK if DarkMode() else wx.WHITE
