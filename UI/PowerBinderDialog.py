import wx
import string
import UI
import GameData

# This is awful
from PowerBindCmd import AFKCmd, AutoPowerCmd, ChatCmd, ChatGlobalCmd, CostumeChangeCmd, CustomBindCmd, EmoteCmd, \
                    PowerAbortCmd, PowerBindCmd, PowerUnqueueCmd, SGModeToggleCmd, TargetCustomCmd, TargetEnemyCmd, \
                    TargetFriendCmd, TeamPetSelectCmd, UnselectCmd, UseInspByNameCmd, UseInspRowColCmd, UsePowerCmd, \
                    UsePowerFromTrayCmd, WindowToggleCmd


class PowerBinderDialog(wx.Dialog):
    def __init__(self, parent):
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

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.Fit()
        self.SetFocus()

    def OnRearrangeDelete(self, evt):
        current = self.RearrangeList.GetSelection()
        if current == wx.NOT_FOUND: return

        self.RearrangeList.Delete(current)
        self.UpdateBindStringDisplay()

    def OnRearrangeUp(self, evt):
        self.RearrangeList.MoveCurrentUp()
        self.UpdateBindStringDisplay()

    def OnRearrangeDown(self, evt):
        self.RearrangeList.MoveCurrentDown()
        self.UpdateBindStringDisplay()

    def OnRearrangeEdit(self, evt):
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

    def OnListSelect(self, evt):
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

commandClasses = {
    'Auto Power'               : AutoPowerCmd.AutoPowerCmd,
    'Away From Keyboard'       : AFKCmd.AFKCmd,
    'Chat Command'             : ChatCmd.ChatCmd,
    'Chat Command (Global)'    : ChatGlobalCmd.ChatGlobalCmd,
    'Costume Change'           : CostumeChangeCmd.CostumeChangeCmd,
    'Custom Bind'              : CustomBindCmd.CustomBindCmd,
    'Emote'                    : EmoteCmd.EmoteCmd,
    'Power Abort'              : PowerAbortCmd.PowerAbortCmd,
    'Power Unqueue'            : PowerUnqueueCmd.PowerUnqueueCmd,
    'SG Mode Toggle'           : SGModeToggleCmd.SGModeToggleCmd,
    'Target Custom'            : TargetCustomCmd.TargetCustomCmd,
    'Target Enemy'             : TargetEnemyCmd.TargetEnemyCmd,
    'Target Friend'            : TargetFriendCmd.TargetFriendCmd,
    'Team/Pet Select'          : TeamPetSelectCmd.TeamPetSelectCmd,
    'Unselect'                 : UnselectCmd.UnselectCmd,
    'Use Insp By Name'         : UseInspByNameCmd.UseInspByNameCmd,
    'Use Insp From Row/Column' : UseInspRowColCmd.UseInspRowColCmd,
    'Use Power'                : UsePowerCmd.UsePowerCmd,
    'Use Power From Tray'      : UsePowerFromTrayCmd.UsePowerFromTrayCmd,
    'Window Toggle'            : WindowToggleCmd.WindowToggleCmd,
}

class PowerBinderButton(wx.Button):
    def __init__(self, parent, tgtTxtCtrl):
        wx.Button.__init__(self, parent, -1, label = "...")

        self.tgtTxtCtrl = tgtTxtCtrl
        self.Bind(wx.EVT_BUTTON, self.PowerBinderEventHandler)

    def PowerBinderEventHandler(self, evt):
        with PowerBinderDialog(self.Parent) as dlg:
            if (self.tgtTxtCtrl and dlg.ShowModal() == wx.ID_OK):
                bindString = dlg.MakeBindString()
                self.tgtTxtCtrl.SetValue(bindString)

class PowerBinderEditDialog(wx.Dialog):
    def __init__(self, parent):
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
