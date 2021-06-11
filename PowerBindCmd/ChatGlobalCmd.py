from PowerBindCmd import PowerBindCmd
import wx


####### Chat Command Global
class ChatGlobalCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        chatCommandGlobalName = wx.TextCtrl(dialog, -1)
        chatCommandGlobalName.SetHint('Chat Command (Global) Text')

        return chatCommandGlobalName

