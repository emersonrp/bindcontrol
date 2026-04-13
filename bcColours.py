import wx
import platform

# is there a saner way to do this?

# we're not gonna darkmode on Windows since Win11 is so broken in this respect
def DarkMode():
    return platform.system() != 'Windows' and wx.SystemSettings().GetAppearance().IsDark()

def ErrorColour() -> wx.Colour:
    return wx.Colour(86, 3, 25) if DarkMode() else wx.Colour(255, 200, 200)

def WarningColour() -> wx.Colour:
    return wx.Colour(125, 94, 0) if DarkMode() else wx.Colour(255, 255, 200)

def BlackColour() -> wx.Colour:
    return wx.WHITE if DarkMode() else wx.BLACK

def WhiteColour() -> wx.Colour:
    return wx.BLACK if DarkMode() else wx.WHITE
