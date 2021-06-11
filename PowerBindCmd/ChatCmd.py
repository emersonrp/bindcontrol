from PowerBindCmd import PowerBindCmd
import wx


####### Chat Command
class ChatCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        chatCommandSizer = wx.GridBagSizer(5, 5)
        chatCommandUseColorsCB = wx.CheckBox(dialog, -1, "Use Chat Bubble Colors")
        chatCommandSizer.Add(chatCommandUseColorsCB, (0,0), (1,6), flag=wx.ALIGN_CENTER_VERTICAL)
        # row 1
        chatCommandBorderColor = wx.ColourPickerCtrl(dialog, -1)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Border:"), (1,0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandBorderColor, (1,1))
        chatCommandBGColor = wx.ColourPickerCtrl(dialog, -1)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Background:"), (1,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandBGColor, (1,3))
        chatCommandFGColor = wx.ColourPickerCtrl(dialog, -1)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Text:"), (1,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandFGColor, (1,5))
        # row 2
        chatCommandDuration = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS)
        chatCommandDuration.SetRange(1, 20)
        chatCommandDuration.SetValue(7)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Duration:"), (2,0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandDuration, (2,1))
        chatCommandChatSize = wx.Choice(dialog, -1,
               choices = ['0.5', '0.6', '0.7', '0.8', '0.9', '1', '1.1', '1.2', '1.3', '1.4', '1.5'])
        chatCommandChatSize.SetSelection(5)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Size:"), (2,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandChatSize, (2,3))
        chatCommandChannel = wx.Choice(dialog, -1,
               choices = ['say', 'group', 'broadcast', 'local', 'yell', 'friends', 'general',
                        'request', 'arena', 'supergroup', 'coalition', 'tell $target,', 'tell $name,'])
        chatCommandChannel.SetSelection(0)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Channel:"), (2,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandChannel, (2,5))
        # row 3
        chatCommandUseColorsCB = wx.CheckBox(dialog, -1, "Use Beginchat")
        chatCommandSizer.Add(chatCommandUseColorsCB, (3,0), (1,2), flag=wx.ALIGN_CENTER_VERTICAL)
        chatCommandMessage = wx.TextCtrl(dialog, -1)
        chatCommandMessage.SetHint('Chat Command Text')
        chatCommandSizer.Add(chatCommandMessage, (3,2), (1,4), flag=wx.EXPAND)

        return chatCommandSizer

