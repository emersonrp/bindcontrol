import wx

def DarkMode():
    return wx.SystemSettings.GetAppearance().IsDark()

def ErrorColour() -> wx.Colour:
    return wx.Colour(100, 40, 40) if DarkMode() else wx.Colour(255, 200, 200)

def WarningColour() -> wx.Colour:
    return wx.Colour(100, 100, 40) if DarkMode() else wx.Colour(255, 255, 200)
