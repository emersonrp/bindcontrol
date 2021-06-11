from PowerBindCmd import PowerBindCmd
import wx


####### Chat Command Global
class ChatGlobalCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        chatCommandGlobalSizer = wx.GridBagSizer(5,5)

        self.chatCommandGlobalUseBeginchatCB = wx.CheckBox(dialog, -1, "Use beginchat")
        chatCommandGlobalSizer.Add(self.chatCommandGlobalUseBeginchatCB, (0,0), (1,2))

        self.chatCommandGlobalChannel = wx.TextCtrl(dialog, -1)
        self.chatCommandGlobalChannel.SetHint("Channel")
        chatCommandGlobalSizer.Add(self.chatCommandGlobalChannel, (1,0))

        self.chatCommandGlobalMessage = wx.TextCtrl(dialog, -1)
        self.chatCommandGlobalMessage.SetHint('Chat Command (Global) Message')
        chatCommandGlobalSizer.Add(self.chatCommandGlobalMessage, (1,1), flag=wx.EXPAND)

        chatCommandGlobalSizer.AddGrowableCol(1)

        return chatCommandGlobalSizer

    def MakeBindString(self, dialog):
        useBeginchat = self.chatCommandGlobalUseBeginchatCB.IsChecked()
        channel      = self.chatCommandGlobalChannel.GetValue()
        message      = self.chatCommandGlobalMessage.GetValue()

        preface = "beginchat /" if useBeginchat else ""

        return f'{preface}send "{channel}" {message}'
