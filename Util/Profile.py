import wx

def GetCurrentProfile():
    return wx.App.Get().Main.Profile
