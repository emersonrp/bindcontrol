import wx
import string
import UI
import GameData
import pprint
pp = pprint.PrettyPrinter(indent=1, width=132)

def PowerBinderEventHandler(evt):
    button = evt.EventObject

    with PowerBinderDialog(button.Parent) as dlg:

        if(dlg.ShowModal() == wx.ID_OK): pass

class PowerBinderDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "PowerBinder", style = wx.DEFAULT_DIALOG_STYLE)

        sizer = wx.BoxSizer(wx.VERTICAL);
        self.mainSizer = sizer

        self.rearrangeCtrl = wx.RearrangeCtrl(self, -1, size=(500,300))
        sizer.Add(self.rearrangeCtrl, 1, wx.EXPAND)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bindChoice = wx.Choice(self, -1, choices= [
            'Auto Power', 'Away From Keyboard', 'Chat Command',
            'Chat Command (Global)', 'Costume Change', 'Custom Bind',
            'Emote', 'Power Abort', 'Power Unqueue', 'SG Mode Toggle',
            'Target Custom', 'Target Enemy', 'Target Friend',
            'Team/Pet Select', 'Unselect', 'Use Insp By Name',
            'Use Insp From Row/Column', 'Use Power', 'Use Power From Tray',
            'Window Toggle',
        ])
        self.bindChoice.SetSelection(self.bindChoice.FindString("Use Power"))
        self.bindChoice.Bind(wx.EVT_CHOICE, self.OnBindChoice)
        choiceSizer.Add(self.bindChoice, 0, wx.ALIGN_CENTER_VERTICAL)

        addBindButton = wx.Button(self, -1, "Add")
        choiceSizer.Add(addBindButton, 0, wx.ALIGN_CENTER_VERTICAL)
        addBindButton.Bind(wx.EVT_BUTTON, self.OnAddBind)

        showBindTextButton = wx.Button(self, -1, "Show Bind Text")
        choiceSizer.Add(showBindTextButton, 0, wx.ALIGN_CENTER_VERTICAL)
        showBindTextButton.Bind(wx.EVT_BUTTON, self.OnShowBindText)

        sizer.Add(choiceSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 16)

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
        self.ExtraUI[autoPowerIndex] = { 'UI': autoPowerSizer }

        ####### Away From Keyboard
        AFKIndex = self.bindChoice.FindString("Away From Keyboard")
        AFKName = wx.TextCtrl(self, -1)
        AFKName.SetHint('Away From Keyboard Text')
        sizer.Add(AFKName, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(AFKName)
        self.ExtraUI[AFKIndex] = { 'UI': AFKName }

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
        chatCommandMessage.SetHint('Chat Command Text')
        chatCommandSizer.Add(chatCommandMessage, (3,2), (1,4), flag=wx.EXPAND)
        sizer.Add(chatCommandSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(chatCommandSizer)
        self.ExtraUI[chatCommandIndex] = { 'UI': chatCommandSizer }

        ####### Chat Command Global
        chatCommandGlobalIndex = self.bindChoice.FindString("Chat Command (Global)")
        chatCommandGlobalName = wx.TextCtrl(self, -1)
        chatCommandGlobalName.SetHint('Chat Command (Global) Text')
        sizer.Add(chatCommandGlobalName, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(chatCommandGlobalName)
        self.ExtraUI[chatCommandGlobalIndex] = { 'UI': chatCommandGlobalName }

        #######Costume Change
        costumeChangeIndex = self.bindChoice.FindString("Costume Change")
        costumeChangeSizer = wx.BoxSizer(wx.HORIZONTAL)
        costumeChangeSizer.Add(wx.StaticText(self, -1, "Costume:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        costumeChangeCostume = wx.Choice(self, -1,
               choices = ["First", "Second", "Third", "Fourth", "Fifth"])
        costumeChangeCostume.SetSelection(0)
        costumeChangeSizer.Add(costumeChangeCostume, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(costumeChangeSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(costumeChangeSizer)
        self.ExtraUI[costumeChangeIndex] = { 'UI': costumeChangeSizer }

        ####### Custom Bind
        customBindIndex = self.bindChoice.FindString("Custom Bind")
        customBindName = wx.TextCtrl(self, -1)
        customBindName.SetHint('Custom Bind Text')
        sizer.Add(customBindName, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(customBindName)
        self.ExtraUI[customBindIndex] = { 'UI': customBindName }

        ####### Emote
        emoteIndex = self.bindChoice.FindString("Emote")
        emoteSizer = wx.BoxSizer(wx.HORIZONTAL)
        emoteSizer.Add(wx.StaticText(self, -1, "Emote:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        # TODO - make this a wx.Choice with a list?  Yikes that's a big list.
        emoteName = wx.TextCtrl(self, -1)
        emoteSizer.Add(emoteName, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(emoteSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(emoteSizer)
        self.ExtraUI[emoteIndex] = { 'UI': emoteSizer }

        ####### Target Custom
        targetCustomIndex = self.bindChoice.FindString("Target Custom")
        targetCustomSizer = wx.FlexGridSizer(2,3,3)
        targetCustomSizer.Add(wx.StaticText(self, -1, "Target Mode:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 4)
        targetCustomModeChoice = wx.Choice(self, -1, choices = ['Near','Far','Next','Prev'])
        targetCustomModeChoice.SetSelection(0)
        targetCustomSizer.Add(targetCustomModeChoice)
        targetCustomSizer.Add(wx.CheckBox(self, -1, "Target Enemies"))
        targetCustomSizer.Add(wx.CheckBox(self, -1, "Target Friends"))
        targetCustomSizer.Add(wx.CheckBox(self, -1, "Target Defeated"))
        targetCustomSizer.Add(wx.CheckBox(self, -1, "Target Living"))
        targetCustomSizer.Add(wx.CheckBox(self, -1, "Target My Pets"))
        targetCustomSizer.Add(wx.CheckBox(self, -1, "Target Not My Pets"))
        targetCustomSizer.Add(wx.CheckBox(self, -1, "Target Base Items"))
        targetCustomSizer.Add(wx.CheckBox(self, -1, "Target Not Base Items"))
        sizer.Add(targetCustomSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(targetCustomSizer)
        self.ExtraUI[targetCustomIndex] = { 'UI': targetCustomSizer }

        ####### Target Enemy
        targetEnemyIndex = self.bindChoice.FindString("Target Enemy")
        targetEnemySizer = wx.BoxSizer(wx.HORIZONTAL)
        targetEnemySizer.Add(wx.StaticText(self, -1, "Target Enemy:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        targetEnemyModeChoice = wx.Choice(self, -1, choices = ['Near','Far','Next','Prev'])
        targetEnemyModeChoice.SetSelection(0)
        targetEnemySizer.Add(targetEnemyModeChoice)
        sizer.Add(targetEnemySizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(targetEnemySizer)
        self.ExtraUI[targetEnemyIndex] = { 'UI': targetEnemySizer }

        ####### Target Friend
        targetFriendIndex = self.bindChoice.FindString("Target Friend")
        targetFriendSizer = wx.BoxSizer(wx.HORIZONTAL)
        targetFriendSizer.Add(wx.StaticText(self, -1, "Target Friend:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        targetFriendModeChoice = wx.Choice(self, -1, choices = ['Near','Far','Next','Prev'])
        targetFriendModeChoice.SetSelection(0)
        targetFriendSizer.Add(targetFriendModeChoice)
        sizer.Add(targetFriendSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(targetFriendSizer)
        self.ExtraUI[targetFriendIndex] = { 'UI': targetFriendSizer }

        ####### Team/Pet Select
        teamPetSelectIndex = self.bindChoice.FindString("Team/Pet Select")
        teamPetSelectSizer = wx.BoxSizer(wx.HORIZONTAL)
        teamPetSelectSizer.Add(wx.RadioButton(self, -1, "Teammate", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL))
        teamPetSelectSizer.Add(wx.RadioButton(self, -1, "Pet/Henchman", style=wx.ALIGN_CENTER_VERTICAL))
        teamPetSelectNumber = wx.SpinCtrl(self, -1, style=wx.SP_ARROW_KEYS|wx.ALIGN_CENTER_VERTICAL)
        teamPetSelectNumber.SetRange(1, 7)
        teamPetSelectSizer.Add(teamPetSelectNumber)
        sizer.Add(teamPetSelectSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(teamPetSelectSizer)
        self.ExtraUI[teamPetSelectIndex] = { 'UI': teamPetSelectSizer }

        ####### Use Insp By Name
        useInspByNameIndex = self.bindChoice.FindString("Use Insp By Name")
        useInspByNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspByNameSizer.Add(wx.StaticText(self, -1, "Inspiration:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        useInspByNameModeChoice = wx.Choice(self, -1, choices = self.GetAllInsps())
        useInspByNameModeChoice.SetSelection(0)
        useInspByNameSizer.Add(useInspByNameModeChoice, 1)
        sizer.Add(useInspByNameSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(useInspByNameSizer)
        self.ExtraUI[useInspByNameIndex] = { 'UI': useInspByNameSizer }

        ####### Use Insp From Row / Column
        useInspRowColumnIndex = self.bindChoice.FindString("Use Insp From Row/Column")
        useInspRowColumnSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspRowColumnSizer.Add(wx.StaticText(self, -1, "Row:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        useInspRowColumnRow = wx.SpinCtrl(self, -1, style=wx.SP_ARROW_KEYS|wx.ALIGN_CENTER_VERTICAL)
        useInspRowColumnRow.SetRange(1, 4)
        useInspRowColumnSizer.Add(useInspRowColumnRow, 1)
        useInspRowColumnSizer.Add(wx.StaticText(self, -1, "Column:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        useInspRowColumnCol = wx.SpinCtrl(self, -1, style=wx.SP_ARROW_KEYS|wx.ALIGN_CENTER_VERTICAL)
        useInspRowColumnCol.SetRange(1, 5)
        useInspRowColumnSizer.Add(useInspRowColumnCol, 1)
        sizer.Add(useInspRowColumnSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(useInspRowColumnSizer)
        self.ExtraUI[useInspRowColumnIndex] = { 'UI': useInspRowColumnSizer }

        ####### Use Power
        usePowerIndex = self.bindChoice.FindString("Use Power")
        usePowerSizer = wx.GridBagSizer(5,5)
        usePowerSizer.Add(wx.StaticText(self, -1, "Method:"), (0,0), flag=wx.ALIGN_CENTER_VERTICAL)
        usePowerSizer.Add(wx.RadioButton(self, -1, "Toggle", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL), (0,1))
        usePowerSizer.Add(wx.RadioButton(self, -1, "On", style=wx.ALIGN_CENTER_VERTICAL), (0,2))
        usePowerSizer.Add(wx.RadioButton(self, -1, "Off", style=wx.ALIGN_CENTER_VERTICAL), (0,3))
        usePowerSizer.Add(wx.StaticText(self, -1, "Power:"), (1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        usePowerName = wx.TextCtrl(self, -1)
        usePowerName.SetHint('Power Name')
        usePowerSizer.Add(usePowerName, (1,1), (1,3), flag=wx.EXPAND)
        usePowerSizer.AddGrowableCol(3)
        sizer.Add(usePowerSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(usePowerSizer)
        self.ExtraUI[usePowerIndex] = { 'UI': usePowerSizer }

        ####### Use Power From Tray
        usePowerFromTrayIndex = self.bindChoice.FindString("Use Power From Tray")
        usePowerFromTraySizer = wx.BoxSizer(wx.HORIZONTAL)
        usePowerFromTraySizer.Add(wx.StaticText(self, -1, "Tray:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        usePowerFromTrayTray = wx.Choice(self, -1,
               choices = ['Main Tray', 'Alt Tray', 'Alt 2 Tray', 'Tray 1', 'Tray2', 'Tray 3',
                   'Tray 4', 'Tray 5', 'Tray 6', 'Tray 7', 'Tray 8', 'Tray 9', 'Tray 10'])
        usePowerFromTrayTray.SetSelection(0)
        usePowerFromTraySizer.Add(usePowerFromTrayTray, 1, wx.ALIGN_CENTER_VERTICAL)
        usePowerFromTraySizer.Add(wx.StaticText(self, -1, "Slot:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        usePowerFromTraySlot = wx.SpinCtrl(self, -1, style=wx.SP_ARROW_KEYS)
        usePowerFromTraySlot.SetRange(1, 10)
        usePowerFromTraySizer.Add(usePowerFromTraySlot, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(usePowerFromTraySizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(usePowerFromTraySizer)
        self.ExtraUI[usePowerFromTrayIndex] = { 'UI': usePowerFromTraySizer }

        ####### Window Toggle
        windowToggleIndex = self.bindChoice.FindString("Use Power From Tray")
        windowToggleSizer = wx.BoxSizer(wx.HORIZONTAL)
        windowToggleSizer.Add(wx.StaticText(self, -1, "Tray:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        windowToggleTray = wx.Choice(self, -1,
               choices = ['Powers', 'Manage', 'Chat', 'Tray', 'Target', 'Nav', 'Map', 'Menu', 'Pets'])
        windowToggleTray.SetSelection(0)
        windowToggleSizer.Add(windowToggleTray, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(windowToggleSizer, 0, wx.EXPAND|wx.TOP, 15)
        sizer.Hide(windowToggleSizer)
        self.ExtraUI[windowToggleIndex] = { 'UI': windowToggleSizer }

        sizer.Add(self.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL|wx.HELP), 0, wx.EXPAND|wx.TOP, 16)

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL);
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10);

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.Fit()
        self.SetFocus()

    def GetAllInsps(self):
        Insplist = []
        for type, info in GameData.Inspirations.items():
            for insp in info['tiers']:
                Insplist.append(insp)

        return sorted(Insplist)

    def OnBindChoice(self, evt):
        index = evt.EventObject.GetSelection()

        for i, extra in self.ExtraUI.items():
            self.mainSizer.Show(extra['UI'], i == index)

        self.Layout()
        self.Fit()


    def OnAddBind(self, evt):
        chosenName = self.bindChoice.GetString(self.bindChoice.GetSelection())

        self.rearrangeCtrl.GetList().Append(chosenName)

    def OnShowBindText(self, evt):
        pass


