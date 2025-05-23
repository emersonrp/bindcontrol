import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Chat Command
class ChatCmd(PowerBinderCommand):
    Name = "Chat Command"
    Menu = "Social"

    chatChannelMap = {
        'say' : 's',
        'group' : 'g',
        'broadcast': 'b',
        'local': 'l',
        'yell': 'y',
        'friends': 'f',
        'general': 'gen',
        'help': 'h',
        'looking for group': 'lfg',
        'request': 'req',
        'arena': 'ac',
        'supergroup': 'sg',
        'coalition': 'c',
        'tell $target,': 't $target,',
        'tell $name': 't $name',
    }

    def BuildUI(self, dialog):
        chatCommandSizer = wx.GridBagSizer(5, 5)
        self.chatCommandUseColorsCB = wx.CheckBox(dialog, -1, "Use Chat Bubble Colors")
        chatCommandSizer.Add(self.chatCommandUseColorsCB, (0,0), (1,6), flag=wx.ALIGN_CENTER_VERTICAL)
        # row 1
        self.chatCommandBorderColor = wx.ColourPickerCtrl(dialog, -1)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Border:"), (1,0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(self.chatCommandBorderColor, (1,1))
        self.chatCommandBGColor = wx.ColourPickerCtrl(dialog, -1)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Background:"), (1,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(self.chatCommandBGColor, (1,3))
        self.chatCommandFGColor = wx.ColourPickerCtrl(dialog, -1)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Text:"), (1,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(self.chatCommandFGColor, (1,5))
        # row 2
        self.chatCommandDuration = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS)
        self.chatCommandDuration.SetRange(1, 20)
        self.chatCommandDuration.SetValue(7)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Duration:"), (2,0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(self.chatCommandDuration, (2,1))
        self.chatCommandChatSize = wx.Choice(dialog, -1,
               choices = ['0.5', '0.6', '0.7', '0.8', '0.9', '1', '1.1', '1.2', '1.3', '1.4', '1.5'])
        self.chatCommandChatSize.SetSelection(5)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Size:"), (2,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(self.chatCommandChatSize, (2,3))
        self.chatCommandChannel = wx.Choice(dialog, -1, choices = [chan for chan in self.chatChannelMap])
        self.chatCommandChannel.SetSelection(0)
        chatCommandSizer.Add(wx.StaticText(dialog, -1, "Channel:"), (2,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(self.chatCommandChannel, (2,5))
        # row 3
        self.chatCommandUseBeginchatCB = wx.CheckBox(dialog, -1, "Use Beginchat")
        chatCommandSizer.Add(self.chatCommandUseBeginchatCB, (3,0), (1,2), flag=wx.ALIGN_CENTER_VERTICAL)
        self.chatCommandMessage = wx.TextCtrl(dialog, -1)
        self.chatCommandMessage.SetHint('Chat Command Text')
        chatCommandSizer.Add(self.chatCommandMessage, (3,2), (1,4), flag=wx.EXPAND)

        return chatCommandSizer

    def MakeBindString(self):
        duration = self.chatCommandDuration.GetValue()

        choice = self.chatCommandChatSize
        index  = choice.GetSelection()
        size   = choice.GetString(index)

        duration = f"<duration {duration}>" if duration != 7   else ""
        size     = f"<size {size}>"         if size     != "1" else ""

        bdcolor = fgcolor = bgcolor = ''
        if self.chatCommandUseColorsCB.IsChecked():
            bdcolor = self.chatCommandBorderColor.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
            fgcolor = self.chatCommandFGColor    .GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
            bgcolor = self.chatCommandBGColor    .GetColour().GetAsString(wx.C2S_HTML_SYNTAX)

            bdcolor = f"<bordercolor {bdcolor}>"
            fgcolor = f"<color {fgcolor}>"
            bgcolor = f"<bgcolor {bgcolor}>"

        beginchat = "beginchat /" if self.chatCommandUseBeginchatCB.IsChecked() else ''
        text      = self.chatCommandMessage.GetValue()

        choice  = self.chatCommandChannel
        index   = choice.GetSelection()
        channel = choice.GetString(index)

        return f"{beginchat}{channel} {size}{duration}{bdcolor}{fgcolor}{bgcolor}{text}"

    def Serialize(self):
        return {
            'usecolors' : self.chatCommandUseColorsCB.IsChecked(),
            'beginchat' : self.chatCommandUseBeginchatCB.IsChecked(),
            'channel'   : self.chatCommandChannel .GetSelection(),
            'size'      : self.chatCommandChatSize.GetSelection(),
            'duration'  : self.chatCommandDuration.GetValue(),
            'bdcolor'   : self.chatCommandBorderColor.GetColour().GetAsString(wx.C2S_HTML_SYNTAX),
            'fgcolor'   : self.chatCommandFGColor    .GetColour().GetAsString(wx.C2S_HTML_SYNTAX),
            'bgcolor'   : self.chatCommandBGColor    .GetColour().GetAsString(wx.C2S_HTML_SYNTAX),
            'text'      : self.chatCommandMessage.GetValue(),
        }

    def Deserialize(self, init):
        if init.get('usecolors', '') : self.chatCommandUseColorsCB   .SetValue(init['usecolors'])
        if init.get('beginchat', '') : self.chatCommandUseBeginchatCB.SetValue(init['beginchat'])
        if init.get('channel'  , '') : self.chatCommandChannel .SetSelection(init['channel'])
        if init.get('size'     , '') : self.chatCommandChatSize.SetSelection(init['size'])
        if init.get('duration' , '') : self.chatCommandDuration.SetValue(init['duration'])
        if init.get('bdcolor'  , '') : self.chatCommandBorderColor.SetColour(init['bdcolor'])
        if init.get('fgcolor'  , '') : self.chatCommandFGColor    .SetColour(init['fgcolor'])
        if init.get('bgcolor'  , '') : self.chatCommandBGColor    .SetColour(init['bgcolor'])
        if init.get('text'     , '') : self.chatCommandMessage.SetValue(init['text'])

