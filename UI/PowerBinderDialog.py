import wx
import string
import UI
import GameData

from Bind.PowerBindCmd import PowerBindCmd


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

        rearrangeCtrl = wx.RearrangeCtrl(self, -1, size=(500,300))
        sizer.Add(rearrangeCtrl, 1, wx.EXPAND)

        self.rearrangeList = rearrangeCtrl.GetList()
        self.rearrangeList.Bind(wx.EVT_LISTBOX, self.OnListSelect)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bindChoice = wx.Choice(self, -1, choices = [cmd for cmd in commandClasses])
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

        sizer.Add(self.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL|wx.HELP), 0, wx.EXPAND)

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL);
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10);

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.Fit()
        self.SetFocus()

    def OnBindChoice(self, evt):
        index = evt.EventObject.GetSelection()

        self.Layout()
        self.Fit()


    def OnAddBind(self, evt):
        chosenName = self.bindChoice.GetString(self.bindChoice.GetSelection())

        # Stick it into the list
        newBindIndex = self.rearrangeList.Append(chosenName)
        self.rearrangeList.Select(newBindIndex)

        # Make the bind object and glue it to the list entry
        newCommandClass = commandClasses[chosenName]
        if newCommandClass:
            newCommand = newCommandClass(self)
            self.rearrangeList.SetClientData(newBindIndex, newCommand)

            # Shim the UI bits for the new command into the dialog,
            # just above the buttons, and then do the correct showing/hiding
            self.mainSizer.Insert(self.mainSizer.GetItemCount()-1, newCommand.UI)
            self.ShowUIFor(newCommand)
        # else no extra UI, don't show

    def OnListSelect(self, evt):
        selected = self.rearrangeList.GetSelection()
        selCommand = self.rearrangeList.GetClientData(selected)

        self.ShowUIFor(selCommand)
        evt.Skip()


    def OnShowBindText(self, evt):
        pass

    def ShowUIFor(self, command):
        ilist = self.rearrangeList

        # unshow anything that's showing
        for index in range(0,ilist.GetCount()):
            c = ilist.GetClientData(index)
            if c.UI: self.mainSizer.Hide(c.UI)

        # ... and show the one we want
        if command.UI:
            self.mainSizer.Show(command.UI)

        self.Layout()
        self.Fit()



##############################
# Individual Commands' Classes
##############################


####### Auto Power
class AutoPowerCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        autoPowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        autoPowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        autoPowerName = wx.TextCtrl(dialog, -1)
        autoPowerSizer.Add(autoPowerName, 1, wx.ALIGN_CENTER_VERTICAL)

        return autoPowerSizer

    def Make(self, dialog):
        pass

####### Away From Keyboard
class AFKCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        AFKIndex = self.bindChoice.FindString("Away From Keyboard")
        AFKName = wx.TextCtrl(self, -1)
        AFKName.SetHint('Away From Keyboard Text')

        return AFKName

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

####### Chat Command Global
class ChatGlobalCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        chatCommandGlobalName = wx.TextCtrl(dialog, -1)
        chatCommandGlobalName.SetHint('Chat Command (Global) Text')

        return chatCommandGlobalName

#######Costume Change
class CostumeChangeCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        costumeChangeSizer = wx.BoxSizer(wx.HORIZONTAL)
        costumeChangeSizer.Add(wx.StaticText(dialog, -1, "Costume:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        costumeChangeCostume = wx.Choice(dialog, -1,
               choices = ["First", "Second", "Third", "Fourth", "Fifth"])
        costumeChangeCostume.SetSelection(0)
        costumeChangeSizer.Add(costumeChangeCostume, 1, wx.ALIGN_CENTER_VERTICAL)

        return costumeChangeSizer

####### Custom Bind
class CustomBindCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        customBindName = wx.TextCtrl(dialog, -1)
        customBindName.SetHint('Custom Bind Text')

        return customBindName

####### Emote
class EmoteCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        emoteSizer = wx.BoxSizer(wx.HORIZONTAL)
        emoteSizer.Add(wx.StaticText(dialog, -1, "Emote:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        # TODO - make this a wx.Choice with a list?  Yikes that's a big list.
        emoteName = wx.TextCtrl(dialog, -1)
        emoteSizer.Add(emoteName, 1, wx.ALIGN_CENTER_VERTICAL)

        return emoteSizer

####### Target Custom
class TargetCustomCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        targetCustomSizer = wx.FlexGridSizer(2,3,3)
        targetCustomSizer.Add(wx.StaticText(dialog, -1, "Target Mode:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT, 4)
        targetCustomModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        targetCustomModeChoice.SetSelection(0)
        targetCustomSizer.Add(targetCustomModeChoice)
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Enemies"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Friends"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Defeated"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Living"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target My Pets"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Not My Pets"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Base Items"))
        targetCustomSizer.Add(wx.CheckBox(dialog, -1, "Target Not Base Items"))

        return targetCustomSizer

####### Target Enemy
class TargetEnemyCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        targetEnemySizer = wx.BoxSizer(wx.HORIZONTAL)
        targetEnemySizer.Add(wx.StaticText(dialog, -1, "Target Enemy:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        targetEnemyModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        targetEnemyModeChoice.SetSelection(0)
        targetEnemySizer.Add(targetEnemyModeChoice)

        return targetEnemySizer

####### Target Friend
class TargetFriendCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        targetFriendSizer = wx.BoxSizer(wx.HORIZONTAL)
        targetFriendSizer.Add(wx.StaticText(dialog, -1, "Target Friend:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        targetFriendModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        targetFriendModeChoice.SetSelection(0)
        targetFriendSizer.Add(targetFriendModeChoice)

        return targetFriendSizer

####### Team/Pet Select
class TeamPetSelectCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        teamPetSelectSizer = wx.BoxSizer(wx.HORIZONTAL)
        teamPetSelectSizer.Add(wx.RadioButton(dialog, -1, "Teammate", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL))
        teamPetSelectSizer.Add(wx.RadioButton(dialog, -1, "Pet/Henchman", style=wx.ALIGN_CENTER_VERTICAL))
        teamPetSelectNumber = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS|wx.ALIGN_CENTER_VERTICAL)
        teamPetSelectNumber.SetRange(1, 7)
        teamPetSelectSizer.Add(teamPetSelectNumber)

        return teamPetSelectSizer

####### Use Insp By Name
class UseInspByNameCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        useInspByNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspByNameSizer.Add(wx.StaticText(dialog, -1, "Inspiration:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        useInspByNameModeChoice = wx.Choice(dialog, -1, choices = self.GetAllInsps())
        useInspByNameModeChoice.SetSelection(0)
        useInspByNameSizer.Add(useInspByNameModeChoice, 1)

        return useInspByNameSizer

    def GetAllInsps(self):
        Insplist = []
        for type, info in GameData.Inspirations.items():
            for insp in info['tiers']:
                Insplist.append(insp)

        return sorted(Insplist)

####### Use Insp From Row / Column
class UseInspRowColCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        useInspRowColumnSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Row:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        useInspRowColumnRow = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS|wx.ALIGN_CENTER_VERTICAL)
        useInspRowColumnRow.SetRange(1, 4)
        useInspRowColumnSizer.Add(useInspRowColumnRow, 1)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Column:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        useInspRowColumnCol = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS|wx.ALIGN_CENTER_VERTICAL)
        useInspRowColumnCol.SetRange(1, 5)
        useInspRowColumnSizer.Add(useInspRowColumnCol, 1)

        return useInspRowColumnSizer

####### Use Power
class UsePowerCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        usePowerSizer = wx.GridBagSizer(5,5)
        usePowerSizer.Add(wx.StaticText(dialog, -1, "Method:"), (0,0), flag=wx.ALIGN_CENTER_VERTICAL)
        usePowerSizer.Add(wx.RadioButton(dialog, -1, "Toggle", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL), (0,1))
        usePowerSizer.Add(wx.RadioButton(dialog, -1, "On", style=wx.ALIGN_CENTER_VERTICAL), (0,2))
        usePowerSizer.Add(wx.RadioButton(dialog, -1, "Off", style=wx.ALIGN_CENTER_VERTICAL), (0,3))
        usePowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), (1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        usePowerName = wx.TextCtrl(dialog, -1)
        usePowerName.SetHint('Power Name')
        usePowerSizer.Add(usePowerName, (1,1), (1,3), flag=wx.EXPAND)
        usePowerSizer.AddGrowableCol(3)

        return usePowerSizer

####### Use Power From Tray
class UsePowerFromTrayCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        usePowerFromTraySizer = wx.BoxSizer(wx.HORIZONTAL)
        usePowerFromTraySizer.Add(wx.StaticText(dialog, -1, "Tray:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        usePowerFromTrayTray = wx.Choice(dialog, -1,
               choices = ['Main Tray', 'Alt Tray', 'Alt 2 Tray', 'Tray 1', 'Tray2', 'Tray 3',
                   'Tray 4', 'Tray 5', 'Tray 6', 'Tray 7', 'Tray 8', 'Tray 9', 'Tray 10'])
        usePowerFromTrayTray.SetSelection(0)
        usePowerFromTraySizer.Add(usePowerFromTrayTray, 1, wx.ALIGN_CENTER_VERTICAL)
        usePowerFromTraySizer.Add(wx.StaticText(dialog, -1, "Slot:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        usePowerFromTraySlot = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS)
        usePowerFromTraySlot.SetRange(1, 10)
        usePowerFromTraySizer.Add(usePowerFromTraySlot, 1, wx.ALIGN_CENTER_VERTICAL)

        return usePowerFromTraySizer

####### Window Toggle
class WindowToggleCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        windowToggleSizer = wx.BoxSizer(wx.HORIZONTAL)
        windowToggleSizer.Add(wx.StaticText(dialog, -1, "Tray:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        windowToggleTray = wx.Choice(dialog, -1,
               choices = ['Powers', 'Manage', 'Chat', 'Tray', 'Target', 'Nav', 'Map', 'Menu', 'Pets'])
        windowToggleTray.SetSelection(0)
        windowToggleSizer.Add(windowToggleTray, 1, wx.ALIGN_CENTER_VERTICAL)

        return windowToggleSizer


commandClasses = {
    'Auto Power'               : AutoPowerCmd,
    'Away From Keyboard'       : AFKCmd,
    'Chat Command'             : ChatCmd,
    'Chat Command (Global)'    : ChatGlobalCmd,
    'Costume Change'           : CostumeChangeCmd,
    'Custom Bind'              : CustomBindCmd,
    'Emote'                    : EmoteCmd,
    'Power Abort'              : None,
    'Power Unqueue'            : None,
    'SG Mode Toggle'           : None,
    'Target Custom'            : TargetCustomCmd,
    'Target Enemy'             : TargetEnemyCmd,
    'Target Friend'            : TargetFriendCmd,
    'Team/Pet Select'          : TeamPetSelectCmd,
    'Unselect'                 : None,
    'Use Insp By Name'         : UseInspByNameCmd,
    'Use Insp From Row/Column' : UseInspRowColCmd,
    'Use Power'                : UsePowerCmd,
    'Use Power From Tray'      : UsePowerFromTrayCmd,
    'Window Toggle'            : WindowToggleCmd,
}


