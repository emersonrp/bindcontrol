import wx
import string
import UI

def PowerBinderEventHandler(evt):
    button = evt.EventObject

    with PowerBinderDialog(button.Parent) as dlg:

        if(dlg.ShowModal() == wx.ID_OK): pass

class PowerBinderDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "PowerBinder", style = wx.DEFAULT_DIALOG_STYLE)

        sizer = wx.BoxSizer(wx.VERTICAL);

        self.rearrangeCtrl = wx.RearrangeCtrl(self, -1, size=(350,300))
        sizer.Add(self.rearrangeCtrl, 1, wx.EXPAND)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bindChoice = wx.Choice(self, -1, choices= [
            'Auto Power', 'Away From Keyboard', 'Chat Command',
            'Chat Command (Global)', 'Costume Change', 'Custom Bind',
            'Emote', 'Power Abort', 'Power Unqueue', 'SG Mode Toggle',
            'Target Custom', 'Target Enemy', 'Target Friend',
            'Team/Pet Select', 'Unselect', 'Use Insp by Name',
            'Use Insp From Row / Custom', 'Use Power', 'Use Power From Tray',
            'Window Toggle',
        ])
        self.bindChoice.SetSelection(self.bindChoice.FindString("Use Power"))
        choiceSizer.Add(self.bindChoice, 0, wx.ALIGN_CENTER_VERTICAL)
        addButton = wx.Button(self, -1, "Add")
        choiceSizer.Add(addButton, 0, wx.ALIGN_CENTER_VERTICAL)
        addButton.Bind(wx.EVT_BUTTON, self.AddSomething)


        sizer.Add(choiceSizer, 0, wx.EXPAND|wx.TOP, 16)

        ###
        # UI Chunks for various choices
        # We make and Add() all of these but keep them hidden
        # until the wx.Choice is on the right item

        self.ExtraUI = {}

        ####### Auto Power
        autoPowerIndex = self.bindChoice.FindString("Auto Power")
        autoPowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        autoPowerSizer.Add(wx.StaticText(self, -1, "Power:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        autoPowerName = wx.TextCtrl(self, -1)
        autoPowerSizer.Add(autoPowerName, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(autoPowerSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(autoPowerSizer)
        self.ExtraUI[autoPowerIndex] = { UI: autoPowerSizer }

        ####### Chat Command
        chatCommandIndex = self.bindChoice.FindString("Chat Command")
        chatCommandSizer = wx.GridBagSizer(5, 5)
        chatCommandUseColorsCB = wx.CheckBox(self, -1, "Use Chat Bubble Colors")
        chatCommandSizer.Add(chatCommandUseColorsCB, (0,0), (1,6), flag=wx.ALIGN_CENTER_VERTICAL)
        # row 1
        chatCommandBorderColor = wx.ColourPickerCtrl(self, -1)
        chatCommandSizer.Add(wx.StaticText(self, -1, "Border:"), (1,0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandBorderColor, (1,1))
        chatCommandBGColor = wx.ColourPickerCtrl(self, -1)
        chatCommandSizer.Add(wx.StaticText(self, -1, "Background:"), (1,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandBGColor, (1,3))
        chatCommandFGColor = wx.ColourPickerCtrl(self, -1)
        chatCommandSizer.Add(wx.StaticText(self, -1, "Text:"), (1,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandFGColor, (1,5))
        # row 2
        chatCommandDuration = wx.SpinCtrl(self, -1, style=wx.SP_ARROW_KEYS)
        chatCommandDuration.SetRange(1, 20)
        chatCommandDuration.SetValue(7)
        chatCommandSizer.Add(wx.StaticText(self, -1, "Duration:"), (2,0), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandDuration, (2,1))
        chatCommandChatSize = wx.Choice(self, -1,
               choices = ['0.5', '0.6', '0.7', '0.8', '0.9', '1', '1.1', '1.2', '1.3', '1.4', '1.5'])
        chatCommandChatSize.SetSelection(5)
        chatCommandSizer.Add(wx.StaticText(self, -1, "Size:"), (2,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandChatSize, (2,3))
        chatCommandChannel = wx.Choice(self, -1,
               choices = ['say', 'group', 'broadcast', 'local', 'yell', 'friends', 'general',
                        'request', 'arena', 'supergroup', 'coalition', 'tell $target,', 'tell $name,'])
        chatCommandChannel.SetSelection(0)
        chatCommandSizer.Add(wx.StaticText(self, -1, "Channel:"), (2,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        chatCommandSizer.Add(chatCommandChannel, (2,5))
        # row 3
        chatCommandUseColorsCB = wx.CheckBox(self, -1, "Use Beginchat")
        chatCommandSizer.Add(chatCommandUseColorsCB, (3,0), (1,2), flag=wx.ALIGN_CENTER_VERTICAL)
        chatCommandMessage = wx.TextCtrl(self, -1)
        chatCommandMessage.SetHint('Message')
        chatCommandSizer.Add(chatCommandMessage, (3,2), (1,4), flag=wx.EXPAND)
        sizer.Add(chatCommandSizer, 0, wx.EXPAND|wx.TOP, 15)
        # sizer.Hide(chatCommandSizer)
        self.ExtraUI[chatCommandIndex] = { UI: chatCommandSizer }

        ####### Chat Command Global
        chatCommandGlobalIndex = self.bindChoice.FindString("Chat Command")
        chatCommandGlobalName = wx.TextCtrl(self, -1)
        sizer.Add(chatCommandGlobalName, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(chatCommandGlobalName)
        self.ExtraUI[chatCommandGlobalIndex] = { UI: chatCommandGlobalName }

        #######Costume Change
        costumeChangeIndex = self.bindChoice.FindString("CostumeChange")
        costumeChangeSizer = wx.BoxSizer(wx.HORIZONTAL)
        costumeChangeSizer.Add(wx.StaticText(self, -1, "Costume:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        costumeChangeCostume = wx.Choice(self, -1,
               choices = ["First", "Second", "Third", "Fourth", "Fifth"])
        costumeChangeCostume.SetSelection(0)
        costumeChangeSizer.Add(costumeChangeCostume, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(costumeChangeSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(costumeChangeSizer)
        self.ExtraUI[costumeChangeIndex] = { UI: costumeChangeSizer }








        sizer.Add(self.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL|wx.HELP), 0)

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL);
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10);

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.SetFocus()




    def AddSomething(self, evt):
        chosenName = self.bindChoice.GetString(self.bindChoice.GetSelection())

        self.rearrangeCtrl.GetList().Append(chosenName)


