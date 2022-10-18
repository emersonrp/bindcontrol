import wx
import UI
import UI.EmotePicker
from UI.PowerPicker import PowerPicker
import GameData

class PowerBinderDialog(wx.Dialog):
    def __init__(self, parent, init = {}):
        wx.Dialog.__init__(self, parent, -1, "PowerBinder", style = wx.DEFAULT_DIALOG_STYLE)

        self.EditDialog = PowerBinderEditDialog(self)

        sizer = wx.BoxSizer(wx.VERTICAL);
        self.mainSizer = sizer

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        choiceSizer.Add(wx.StaticText(self, -1, "Add Step:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.bindChoice = wx.Choice(self, -1, choices = [cmd for cmd in commandClasses])
        self.bindChoice.Bind(wx.EVT_CHOICE, self.OnBindChoice)
        choiceSizer.Add(self.bindChoice, 1, wx.LEFT, 10)
        sizer.Add(choiceSizer, 1, wx.EXPAND|wx.BOTTOM, 10)

        rearrangeCtrl = wx.BoxSizer(wx.HORIZONTAL)

        self.RearrangeList = wx.RearrangeList(self, -1, size=(550,400))
        self.RearrangeList.Bind(wx.EVT_LISTBOX, self.OnListSelect)
        rearrangeCtrl.Add(self.RearrangeList, 1)

        rearrangeButtons = wx.BoxSizer(wx.VERTICAL)
        self.DelButton = wx.Button(self, -1, "Delete")
        self.DelButton.Bind(wx.EVT_BUTTON, self.OnRearrangeDelete)
        self.EditButton = wx.Button(self, -1, "Edit")
        self.EditButton.Bind(wx.EVT_BUTTON, self.OnRearrangeEdit)
        self.EditButton.Disable()
        upButton = wx.Button(self, -1, "\u25B2")
        upButton.Bind(wx.EVT_BUTTON, self.OnRearrangeUp)
        downButton = wx.Button(self, -1, "\u25BC")
        downButton.Bind(wx.EVT_BUTTON, self.OnRearrangeDown)
        rearrangeButtons.Add(upButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(downButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(self.EditButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(self.DelButton, 1, wx.BOTTOM, 10)
        rearrangeCtrl.Add(rearrangeButtons, 0, wx.LEFT, 10)

        sizer.Add(rearrangeCtrl, 0, wx.EXPAND|wx.TOP|wx.BOTTOM)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.BindStringDisplay = wx.TextCtrl(self, -1)
        self.BindStringDisplay.Disable()
        choiceSizer.Add(wx.StaticText(self, -1, "Bind String:"), 0,
                        wx.ALIGN_CENTER_VERTICAL)
        choiceSizer.Add(self.BindStringDisplay, 1, wx.LEFT, 10)

        sizer.Add(choiceSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 16)

        sizer.Add(self.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL|wx.HELP), 0, wx.EXPAND)

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL);
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10);

        # if we are loading from profile, ie, have "init", build the list from it
        if init: self.LoadFromData(init)

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.Fit()
        self.SetFocus()

    def LoadFromData(self, init):
        for type, data in init.items():
            commandClass = commandClasses[type]
            self.RearrangeList.Append(commandClass(data))

    def SaveToData(self):
        data = []
        index = 0
        for _ in self.RearrangeList.GetItems():
            # check whether we have an object already attached to this choice
            cmdObject = self.RearrangeList.GetClientData(index)
            commandClassName = commandRevClasses[type(cmdObject)]
            data.append({commandClassName: cmdObject.Serialize()})
            index = index + 1
        return data

    def OnRearrangeDelete(self, _):
        current = self.RearrangeList.GetSelection()
        if current == wx.NOT_FOUND: return

        self.RearrangeList.Delete(current)
        self.UpdateBindStringDisplay()

    def OnRearrangeUp(self, _):
        self.RearrangeList.MoveCurrentUp()
        self.UpdateBindStringDisplay()

    def OnRearrangeDown(self, _):
        self.RearrangeList.MoveCurrentDown()
        self.UpdateBindStringDisplay()

    def OnRearrangeEdit(self, _):
        index = self.RearrangeList.GetSelection()

        # check whether we have an object already attached to this choice
        cmdObject = None
        try:
            cmdObject = self.RearrangeList.GetClientData(index)
        except Exception:
            pass

        if cmdObject:
            self.ShowEditDialogFor(cmdObject)
        else:
            print("cmdObject was None")
        self.UpdateBindStringDisplay()

    # OnBindChoice creates a new step and adds it to the rearrangelist
    def OnBindChoice(self, evt):
        chosenSel  = self.bindChoice.GetSelection()
        chosenName = self.bindChoice.GetString(chosenSel)

        # make a new command object, attached to the parent dialog
        newCommand = commandClasses[chosenName]
        if newCommand:
            cmdObject = newCommand(self.EditDialog)
            self.bindChoice.SetClientData(chosenSel, cmdObject)

        # detach the command object and instead glue it to self.RearrangeList
        newCommand = self.bindChoice.DetachClientObject(chosenSel)
        newBindIndex = self.RearrangeList.Append(chosenName)
        self.RearrangeList.Select(newBindIndex)
        self.RearrangeList.SetClientData(newBindIndex, newCommand)

        # show the edit dialog if this command needs it
        if newCommand.UI:
            self.EditDialog.mainSizer.Insert(0, newCommand.UI, 1, wx.EXPAND|wx.ALL, 10)
            self.ShowEditDialogFor(newCommand)

        self.bindChoice.SetSelection(wx.NOT_FOUND)
        self.OnListSelect(evt)
        self.UpdateBindStringDisplay()

    def OnListSelect(self, _):
        selected = self.RearrangeList.GetSelection()

        selCommand = self.RearrangeList.GetClientData(selected)
        if selCommand.UI:
            self.EditButton.Enable()
        else:
            self.EditButton.Disable()

    def UpdateBindStringDisplay(self):
        self.BindStringDisplay.SetValue(self.MakeBindString())

    def MakeBindString(self):
        cmdBindStrings = []
        for index in range(self.RearrangeList.GetCount()):
            c = self.RearrangeList.GetClientData(index)
            if c: cmdBindStrings.append(c.MakeBindString(self))

        bindstring = ('$$'.join(cmdBindStrings))
        return bindstring

    def ShowEditDialogFor(self, command):
        self.EditDialog.mainSizer.Show(command.UI)

        self.EditDialog.Layout()
        self.EditDialog.Fit()

        chosenSel  = self.RearrangeList.GetSelection()
        chosenName = self.RearrangeList.GetString(chosenSel)

        self.EditDialog.SetTitle(f'Editing Step "{chosenName}"')
        self.EditDialog.ShowModal()

        self.EditDialog.mainSizer.Hide(command.UI)

class PowerBinderButton(wx.Button):
    def __init__(self, parent, tgtTxtCtrl, init = {}):
        wx.Button.__init__(self, parent, -1, label = "...")
        self.PowerBinderDialog = PowerBinderDialog(self.Parent, init)

        self.tgtTxtCtrl = tgtTxtCtrl
        self.Bind(wx.EVT_BUTTON, self.PowerBinderEventHandler)

    def PowerBinderEventHandler(self, _):
        dlg = self.PowerBinderDialog
        if (self.tgtTxtCtrl and dlg.ShowModal() == wx.ID_OK):
            bindString = dlg.MakeBindString()
            if bindString != self.tgtTxtCtrl.GetValue():
                self.tgtTxtCtrl.SetValue(bindString)
                wx.App.Get().Profile.SetModified()

class PowerBinderEditDialog(wx.Dialog):
    def __init__(self, parent, init = {}):
        wx.Dialog.__init__(self, parent, -1, "Edit Step",
           style = wx.DEFAULT_DIALOG_STYLE)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.SetMinSize([500, 150])

        self.mainSizer.Add(
            self.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL),
            0, wx.EXPAND|wx.ALL, 10)

        self.SetSizerAndFit(self.mainSizer)
        self.Layout()
        self.Fit()

########### Power Binder Command Objects
class PowerBindCmd():
    def __init__(self, dialog, init = {}):
        self.UI = self.BuildUI(dialog)
        if init: self.Deserialize(init)

    # Methods to override
    def BuildUI(self, _)        : return
    def MakeBindString(self, _) : return
    def Serialize(self)         : return
    def Deserialize(self, _) : return

####### Away From Keyboard
class AFKCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.AFKName = wx.TextCtrl(dialog, -1)
        self.AFKName.SetHint('Away From Keyboard Text')
        sizer.Add(self.AFKName, 1, wx.ALIGN_CENTER_VERTICAL)

        return sizer

    def MakeBindString(self, _):
        message = self.AFKName.GetValue()

        return f"afk {message}" if message else "afk"

####### Auto Power
class AutoPowerCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        autoPowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        autoPowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.autoPowerName = wx.TextCtrl(dialog, -1)
        autoPowerSizer.Add(self.autoPowerName, 1, wx.ALIGN_CENTER_VERTICAL)

        return autoPowerSizer

    def MakeBindString(self, _):
        return f"powexecauto {self.autoPowerName.GetValue()}"

####### Chat Command
class ChatCmd(PowerBindCmd):
    def __init__(self, dialog):
        self.chatChannelMap = { # before __init__
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
        PowerBindCmd.__init__(self,dialog)

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

    def MakeBindString(self, _):
        duration = self.chatCommandDuration.GetValue()

        choice = self.chatCommandChatSize
        index  = choice.GetSelection()
        size   = choice.GetString(index)

        duration = f"<duration {duration}>" if duration != 7 else ""
        size     = f"<size {size}>"         if size     != 1 else ""

        bdcolor = fgcolor = bgcolor = ''
        if self.chatCommandUseColorsCB.IsChecked():
            bdcolor = self.chatCommandBorderColor.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
            fgcolor = self.chatCommandBGColor    .GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
            bgcolor = self.chatCommandFGColor    .GetColour().GetAsString(wx.C2S_HTML_SYNTAX)

            bdcolor = f"<bordercolor {bdcolor}>"
            fgcolor = f"<color {fgcolor}>"
            bgcolor = f"<bgcolor {bgcolor}>"

        beginchat = "beginchat /" if self.chatCommandUseBeginchatCB.IsChecked() else ''
        text      = self.chatCommandMessage.GetValue()

        choice  = self.chatCommandChannel
        index   = choice.GetSelection()
        channel = choice.GetString(index)

        return f"{beginchat}{channel} {size}{duration}{bdcolor}{fgcolor}{bgcolor}{text}"

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

    def MakeBindString(self, _):
        useBeginchat = self.chatCommandGlobalUseBeginchatCB.IsChecked()
        channel      = self.chatCommandGlobalChannel.GetValue()
        message      = self.chatCommandGlobalMessage.GetValue()

        preface = "beginchat /" if useBeginchat else ""

        return f'{preface}send "{channel}" {message}'

#######Costume Change
class CostumeChangeCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        costumeChangeSizer = wx.BoxSizer(wx.HORIZONTAL)
        costumeChangeSizer.Add(wx.StaticText(dialog, -1, "Costume:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.costumeChangeCostume = wx.Choice(dialog, -1,
               choices = ["First", "Second", "Third", "Fourth", "Fifth"])
        self.costumeChangeCostume.SetSelection(0)
        costumeChangeSizer.Add(self.costumeChangeCostume, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        costumeChangeSizer.Add(wx.StaticText(dialog, -1, "CC Emote:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.costumeChangeEmote = wx.Choice(dialog, -1,
                choices = GameData.Emotes['costumechange'])
        self.costumeChangeEmote.Insert("- None -", 0)
        self.costumeChangeEmote.SetSelection(0)
        costumeChangeSizer.Add(self.costumeChangeEmote, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        return costumeChangeSizer

    def MakeBindString(self, _):
        costumeNumber = self.costumeChangeCostume.GetSelection() + 1
        costumeEmote  = self.costumeChangeEmote.GetSelection()

        if costumeEmote: # None, or 0 == "- None -"
            ccCmd = 'cce'
            emoteName = self.costumeChangeEmote.GetString(costumeEmote)
            emoteName = " CC" + emoteName.replace(" ","")
        else:
            ccCmd = 'cc'
            emoteName = ''

        return f"{ccCmd} {costumeNumber}{emoteName}"

####### Custom Bind
class CustomBindCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.customBindName = wx.TextCtrl(dialog, -1)
        self.customBindName.SetHint('Custom Bind Text')
        sizer.Add(self.customBindName, 1, wx.ALIGN_CENTER_VERTICAL)

        return sizer

    def MakeBindString(self, _):
        return self.customBindName.GetValue()

####### Emote
class EmoteCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        emoteSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.emoteText = wx.StaticText(dialog, -1, "Select Emote:")
        emoteSizer.Add(self.emoteText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)

        self.emoteName = wx.Button(dialog, -1, "...")
        self.emoteName.Bind(wx.EVT_BUTTON, UI.EmotePicker.OnEmotePicker)
        emoteSizer.Add(self.emoteName, 1, wx.ALIGN_CENTER_VERTICAL)

        return emoteSizer

    def MakeBindString(self, _):
        displayedEmoteName = self.emoteName.GetLabel()
        actualEmotePayload = UI.EmotePicker.EmotePicker.payloadMap[displayedEmoteName]

        return actualEmotePayload

####### Power Abort
class PowerAbortCmd(PowerBindCmd):
    def MakeBindString(self, _):
        return 'powexecabort'

####### Power Unqueue
class PowerUnqueueCmd(PowerBindCmd):
    def MakeBindString(self, _):
        return 'powexecunqueue'

####### SG Mode Toggle
class SGModeToggleCmd(PowerBindCmd):
    def MakeBindString(self, _):
        return 'sgmode'

####### Target Custom
class TargetCustomCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        targetCustomSizer = wx.GridBagSizer(5,5)
        targetCustomSizer.Add(wx.StaticText(dialog, -1, "Target Mode:"), (0,0),
                flag =wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.RIGHT)
        self.targetCustomModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        self.targetCustomModeChoice.SetSelection(0)
        targetCustomSizer.Add(self.targetCustomModeChoice, (0,1), flag=wx.EXPAND)
        self.targetCustomOptionalName = wx.TextCtrl(dialog, -1)
        self.targetCustomOptionalName.SetHint("Optional name to match")
        targetCustomSizer.Add(self.targetCustomOptionalName, (0,2), flag=wx.EXPAND)
        self.targetCustomCBEnemies = wx.CheckBox(dialog, -1, "Enemies")
        targetCustomSizer.Add(self.targetCustomCBEnemies, (1,0))
        self.targetCustomCBFriends = wx.CheckBox(dialog, -1, "Friends")
        targetCustomSizer.Add(self.targetCustomCBFriends, (1,1))
        self.targetCustomCBDefeated = wx.CheckBox(dialog, -1, "Defeated")
        targetCustomSizer.Add(self.targetCustomCBDefeated, (2,0))
        self.targetCustomCBAlive = wx.CheckBox(dialog, -1, "Alive")
        targetCustomSizer.Add(self.targetCustomCBAlive, (2,1))
        self.targetCustomCBMyPets = wx.CheckBox(dialog, -1, "My Pets")
        targetCustomSizer.Add(self.targetCustomCBMyPets, (3,0))
        self.targetCustomCBNotMyPets = wx.CheckBox(dialog, -1, "Not My Pets")
        targetCustomSizer.Add(self.targetCustomCBNotMyPets, (3,1))
        self.targetCustomCBBaseItems = wx.CheckBox(dialog, -1, "Base Items")
        targetCustomSizer.Add(self.targetCustomCBBaseItems, (4,0))
        self.targetCustomCBNotBaseItems = wx.CheckBox(dialog, -1, "Not Base Items")
        targetCustomSizer.Add(self.targetCustomCBNotBaseItems, (4,1))

        targetCustomSizer.AddGrowableCol(2)

        return targetCustomSizer

    def MakeBindString(self, _):
        choice = self.targetCustomModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)
        targetCommand = "targetcustom" + mode.lower()

        enemy    = " enemy"    if self.targetCustomCBEnemies.      IsChecked() else ""
        friend   = " friend"   if self.targetCustomCBFriends.      IsChecked() else ""
        defeated = " defeated" if self.targetCustomCBDefeated.     IsChecked() else ""
        alive    = " alive"    if self.targetCustomCBAlive.        IsChecked() else ""
        mypet    = " mypet"    if self.targetCustomCBMyPets.       IsChecked() else ""
        notmypet = " notmypet" if self.targetCustomCBNotMyPets.    IsChecked() else ""
        base     = " base"     if self.targetCustomCBBaseItems.    IsChecked() else ""
        notbase  = " notbase"  if self.targetCustomCBNotBaseItems. IsChecked() else ""

        name = self.targetCustomOptionalName.GetValue()

        return f"{targetCommand}{enemy}{friend}{defeated}{alive}{mypet}{notmypet}{base}{notbase} {name}"

####### Target Enemy
class TargetEnemyCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        targetEnemySizer = wx.BoxSizer(wx.HORIZONTAL)
        targetEnemySizer.Add(wx.StaticText(dialog, -1, "Target Enemy:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.targetEnemyModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        self.targetEnemyModeChoice.SetSelection(0)
        targetEnemySizer.Add(self.targetEnemyModeChoice, 0, wx.ALIGN_CENTER_VERTICAL)

        return targetEnemySizer

    def MakeBindString(self, _):
        choice = self.targetEnemyModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)
        return "targetenemy" + mode.lower()

####### Target Friend
class TargetFriendCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        targetFriendSizer = wx.BoxSizer(wx.HORIZONTAL)
        targetFriendSizer.Add(wx.StaticText(dialog, -1, "Target Friend:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.targetFriendModeChoice = wx.Choice(dialog, -1, choices = ['Near','Far','Next','Prev'])
        self.targetFriendModeChoice.SetSelection(0)
        targetFriendSizer.Add(self.targetFriendModeChoice, 0, wx.ALIGN_CENTER_VERTICAL)

        return targetFriendSizer

    def MakeBindString(self, _):
        choice = self.targetFriendModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)
        return "targetfriend" + mode.lower()

####### Team/Pet Select
class TeamPetSelectCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        teamPetSelectSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.teamPetSelectTeamRB = wx.RadioButton(dialog, -1, "Teammate", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL)
        teamPetSelectSizer.Add(self.teamPetSelectTeamRB, 0, wx.ALIGN_CENTER_VERTICAL)

        self.teamPetSelectPetRB  = wx.RadioButton(dialog, -1, "Pet/Henchman", style=wx.ALIGN_CENTER_VERTICAL)
        teamPetSelectSizer.Add(self.teamPetSelectPetRB, 0, wx.ALIGN_CENTER_VERTICAL)

        self.teamPetSelectNumber = wx.Choice(dialog, -1, choices=['1','2','3','4','5','6','7','8'],
                style=wx.ALIGN_CENTER_VERTICAL)
        self.teamPetSelectNumber.SetSelection(0)
        teamPetSelectSizer.Add(self.teamPetSelectNumber, 0, wx.ALIGN_CENTER_VERTICAL)

        return teamPetSelectSizer

    def MakeBindString(self, _):
        teamOrPet = 'team' if self.teamPetSelectTeamRB.GetValue() else 'pet'
        targetNumber = self.teamPetSelectNumber.GetSelection()+1

        return f"{teamOrPet}select {targetNumber}"

####### Unselect
class UnselectCmd(PowerBindCmd):
    def MakeBindString(self, _):
        return 'unselect'

####### Use Insp By Name
class UseInspByNameCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        useInspByNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspByNameSizer.Add(wx.StaticText(dialog, -1, "Inspiration:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.useInspByNameModeChoice = wx.Choice(dialog, -1, choices = self.GetAllInsps())
        self.useInspByNameModeChoice.SetSelection(0)
        useInspByNameSizer.Add(self.useInspByNameModeChoice, 1, wx.ALIGN_CENTER_VERTICAL)

        return useInspByNameSizer

    def MakeBindString(self, _):
        choice = self.useInspByNameModeChoice
        index  = choice.GetSelection()
        mode   = choice.GetString(index)
        return "inspexecname " + mode.lower()


    def GetAllInsps(self):
        Insplist = []
        for _, info in GameData.Inspirations.items():
            for insp in info['tiers']:
                Insplist.append(insp)
            Insplist.append("---")
        Insplist.pop(-1) # snip the terminal "---"

        return Insplist

####### Use Insp From Row / Column
class UseInspRowColCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        useInspRowColumnSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Row:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.useInspRowColumnRow = wx.Choice(dialog, -1, choices=['1','2','3','4'], style=wx.ALIGN_CENTER_VERTICAL)
        self.useInspRowColumnRow.SetSelection(0)
        useInspRowColumnSizer.Add(self.useInspRowColumnRow, 0, wx.ALIGN_CENTER_VERTICAL)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Column:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 4)
        self.useInspRowColumnCol = wx.Choice(dialog, -1, choices=['1','2','3','4','5'], style=wx.ALIGN_CENTER_VERTICAL)
        self.useInspRowColumnCol.SetSelection(0)
        useInspRowColumnSizer.Add(self.useInspRowColumnCol, 0, wx.ALIGN_CENTER_VERTICAL)

        return useInspRowColumnSizer

    def MakeBindString(self, _):
        row = self.useInspRowColumnRow.GetSelection()+1
        col = self.useInspRowColumnCol.GetSelection()+1

        return f"inspexectray {col} {row}"

####### Use Power
class UsePowerCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        outerSizer = wx.BoxSizer(wx.HORIZONTAL)

        usePowerSizer = wx.GridBagSizer(5,5)
        usePowerSizer.Add(wx.StaticText(dialog, -1, "Method:"), (0,0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.usePowerRBToggle = wx.RadioButton(dialog, -1, "Toggle", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL)
        usePowerSizer.Add(self.usePowerRBToggle, (0,1))
        self.usePowerRBOn = wx.RadioButton(dialog, -1, "On", style=wx.ALIGN_CENTER_VERTICAL)
        usePowerSizer.Add(self.usePowerRBOn, (0,2))
        self.usePowerRBOff = wx.RadioButton(dialog, -1, "Off", style=wx.ALIGN_CENTER_VERTICAL)
        usePowerSizer.Add(self.usePowerRBOff, (0,3))
        usePowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), (1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.usePowerName = PowerPicker(dialog)
        usePowerSizer.Add(self.usePowerName, (1,1), (1,3), flag=wx.EXPAND)
        usePowerSizer.AddGrowableCol(3)

        outerSizer.Add(usePowerSizer, 1, wx.ALIGN_CENTER_VERTICAL)

        return outerSizer

    def MakeBindString(self, _):
        if self.usePowerRBToggle.GetValue():
            method = "powexecname"
        elif self.usePowerRBOn.GetValue():
            method = "powexectoggleon"
        elif self.usePowerRBOff.GetValue():
            method = "powexectoggleoff"
        else:
            wx.LogError('PowerBindCmd "UsePowerCmd" got an impossible value for toggle/on/off')
            return ''

        return f"{method} {self.usePowerName.GetLabel()}"

####### Use Power From Tray
class UsePowerFromTrayCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        usePowerFromTraySizer = wx.BoxSizer(wx.HORIZONTAL)
        usePowerFromTraySizer.Add(wx.StaticText(dialog, -1, "Tray:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.usePowerFromTrayTray = wx.Choice(dialog, -1,
               choices = ['Main Tray', 'Alt Tray', 'Alt 2 Tray', 'Tray 1', 'Tray2', 'Tray 3',
                   'Tray 4', 'Tray 5', 'Tray 6', 'Tray 7', 'Tray 8', 'Tray 9', 'Tray 10'])
        self.usePowerFromTrayTray.SetSelection(0)
        usePowerFromTraySizer.Add(self.usePowerFromTrayTray, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        usePowerFromTraySizer.Add(wx.StaticText(dialog, -1, "Slot:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.usePowerFromTraySlot = wx.Choice(dialog, -1, choices=['1','2','3','4','5','6','7','8','9','10'])
        self.usePowerFromTraySlot.SetSelection(0)
        usePowerFromTraySizer.Add(self.usePowerFromTraySlot, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        return usePowerFromTraySizer

    def MakeBindString(self, _):
        choice = self.usePowerFromTrayTray
        tray = choice.GetSelection()

        choice = self.usePowerFromTraySlot
        slot   = choice.GetSelection()+1

        mode = "slot"
        mode2 = ''
        if tray > 3:
            mode = "tray"
            mode2 = f" {tray - 3}"
        elif tray == 3:
            mode = "alt2slot"
        elif tray == 2:
            mode = "altslot"

        return f"powexec{mode} {slot}{mode2}"

####### Window Toggle
class WindowToggleCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        windows = [ 'Actions', 'Badge', 'ChanSearch', 'Chat', 'Chat0', 'Chat1', 'Chat2', 'Chat3',
            'Chat4', 'Clue', 'Combatmonitor', 'Combatnumbers', 'Compass', 'Compose', 'Contact',
            'Costume', 'Email', 'Enhancements', 'Friend', 'Group', 'Help', 'Info', 'Inspirations',
            'Map', 'Mission', 'Nav', 'Options', 'Pet', 'Power', 'PowerList', 'Recipes', 'Salvage',
            'Search', 'Supergroup', 'Team', 'Target', 'Tray', ]
        windowToggleSizer = wx.BoxSizer(wx.HORIZONTAL)
        windowToggleSizer.Add(wx.StaticText(dialog, -1, "Window:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.windowToggleTray = wx.Choice(dialog, -1, choices = windows)
        self.windowToggleTray.SetSelection(0)
        windowToggleSizer.Add(self.windowToggleTray, 1, wx.ALIGN_CENTER_VERTICAL)

        return windowToggleSizer

    def MakeBindString(self, _):
        choice = self.windowToggleTray
        index  = choice.GetSelection()
        window = choice.GetString(index)
        return "windowtoggle " + window.lower()

# Must always add to this list when adding a new command class above
commandClasses = {
    'Auto Power'               : AutoPowerCmd,
    'Away From Keyboard'       : AFKCmd,
    'Chat Command'             : ChatCmd,
    'Chat Command (Global)'    : ChatGlobalCmd,
    'Costume Change'           : CostumeChangeCmd,
    'Custom Bind'              : CustomBindCmd,
    'Emote'                    : EmoteCmd,
    'Power Abort'              : PowerAbortCmd,
    'Power Unqueue'            : PowerUnqueueCmd,
    'SG Mode Toggle'           : SGModeToggleCmd,
    'Target Custom'            : TargetCustomCmd,
    'Target Enemy'             : TargetEnemyCmd,
    'Target Friend'            : TargetFriendCmd,
    'Team/Pet Select'          : TeamPetSelectCmd,
    'Unselect'                 : UnselectCmd,
    'Use Insp By Name'         : UseInspByNameCmd,
    'Use Insp From Row/Column' : UseInspRowColCmd,
    'Use Power'                : UsePowerCmd,
    'Use Power From Tray'      : UsePowerFromTrayCmd,
    'Window Toggle'            : WindowToggleCmd,
}
commandRevClasses = {v: k for k, v in commandClasses.items()}
