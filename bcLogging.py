import wx

class bcLogging(wx.Log):
    def __init__(self, parent):
        super().__init__()
        self.InfoBar = wx.InfoBar(parent)
        self.InfoBar.SetShowHideEffects(wx.SHOW_EFFECT_SLIDE_TO_TOP, wx.SHOW_EFFECT_SLIDE_TO_BOTTOM)

        self.LogWindow = wx.LogWindow(parent, "Log Window", show = False, passToOld = False)
        self.LogWindow.GetFrame().SetSize(1000,300)

        self.LogInterposer = bcLogInterposer(self)

        self.SetLogLevel(wx.LOG_Message)

class bcLogInterposer(wx.LogInterposer):
    def __init__(self, logger):
        super().__init__()
        self.InfoBar = logger.InfoBar

    def DoLogTextAtLevel(self, level, msg):
        if level <= wx.LOG_Warning:
            iconflag = wx.ICON_ERROR if level == wx.LOG_Error else wx.ICON_WARNING
            self.InfoBar.ShowMessage(msg, iconflag)
