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

        sizer = wx.BoxSizer(wx.VERTICAL);
        self.mainSizer = sizer

        self.bindChoice = wx.Choice(self, -1, choices = [cmd for cmd in commandClasses])
        self.bindChoice.Bind(wx.EVT_CHOICE, self.OnBindChoice)
        self.mainSizer.Add(self.bindChoice, 1, wx.EXPAND|wx.BOTTOM, 10)

        rearrangeCtrl = wx.BoxSizer(wx.HORIZONTAL)
        self.rearrangeList = wx.RearrangeList(self, -1, size=(550,400))
        self.rearrangeList.Bind(wx.EVT_LISTBOX, self.OnListSelect)
        rearrangeCtrl.Add(self.rearrangeList, 1)

        rearrangeButtons = wx.BoxSizer(wx.VERTICAL)
        delButton = wx.Button(self, -1, "Delete")
        delButton.Bind(wx.EVT_BUTTON, self.OnRearrangeDelete)
        editButton = wx.Button(self, -1, "Edit")
        editButton.Bind(wx.EVT_BUTTON, self.OnRearrangeEdit)
        upButton = wx.Button(self, -1, "Up")
        upButton.Bind(wx.EVT_BUTTON, self.OnRearrangeUp)
        downButton = wx.Button(self, -1, "Down")
        downButton.Bind(wx.EVT_BUTTON, self.OnRearrangeDown)
        rearrangeButtons.Add(delButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(editButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(upButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(downButton, 1, wx.BOTTOM, 10)
        rearrangeCtrl.Add(rearrangeButtons, 0, wx.LEFT, 10)

        sizer.Add(rearrangeCtrl, 0, wx.EXPAND|wx.TOP|wx.BOTTOM)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.BindStringDisplay = wx.StaticText(self, -1)
        choiceSizer.Add(wx.StaticText(self, -1, "Bind String:"), 0)
        choiceSizer.Add(self.BindStringDisplay, 1)

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
        current = self.rearrangeList.GetSelection()
        self.rearrangeList.Delete(current)
        self.UpdateBindStringDisplay()

    def OnRearrangeUp(self, evt):
        self.rearrangeList.MoveCurrentUp()
        self.UpdateBindStringDisplay()

    def OnRearrangeDown(self, evt):
        self.rearrangeList.MoveCurrentDown()
        self.UpdateBindStringDisplay()

    def OnRearrangeEdit(self, evt):
        return # TODO - this whole method
        index = self.bindChoice.GetSelection()

        # check whether we have an object already attached to this choice
        cmdObject = None
        try:
            cmdObject = self.bindChoice.GetClientData(index)
        except Exception:
            pass

        # if not, make and attach one
        if not cmdObject:
            chosenName = self.bindChoice.GetString(index)
            newCommandClass = commandClasses[chosenName]
            if newCommandClass:
                cmdObject = newCommandClass(self)
                self.bindChoice.SetClientData(index, cmdObject)

                # Shim the UI bits (if any) for the new command into the dialog,
                # just above the buttons, and then do the correct showing/hiding
                if cmdObject.UI:
                    self.mainSizer.Insert(self.mainSizer.GetItemCount()-1, cmdObject.UI, 0, wx.EXPAND)
                # else no extra UI, don't show

        # old or new, show it.
        self.ShowUIFor(cmdObject)
        self.Layout()
        self.Fit()

    def OnBindChoice(self, evt):
        # find the item we just poked "add" next to
        chosenSel  = self.bindChoice.GetSelection()
        chosenName = self.bindChoice.GetString(chosenSel)

        # check whether we have an object already attached to this choice
        cmdObject = None
        try:
            cmdObject = self.bindChoice.GetClientData(chosenSel)
        except Exception:
            pass

        # if not, make and attach one
        if not cmdObject:
            newCommand = commandClasses[chosenName]
            if newCommand:
                cmdObject = newCommand(self)
                self.bindChoice.SetClientData(chosenSel, cmdObject)
                if cmdObject.UI:
                    self.Freeze()
                    self.mainSizer.Insert(self.mainSizer.GetItemCount()-1, cmdObject.UI, 0, wx.EXPAND)
                    self.mainSizer.Hide(cmdObject.UI)
                    self.Thaw()


        # detach the command object from self.bindChoice, and instead glue it
        # to self.rearrangeList
        newCommand = self.bindChoice.DetachClientObject(chosenSel)
        newBindIndex = self.rearrangeList.Append(chosenName)
        self.rearrangeList.Select(newBindIndex)
        self.rearrangeList.SetClientData(newBindIndex, newCommand)

        # Reset the chooser to empty, leaving the UI in place, to make
        # it clear that the UI now points to the object above
        self.bindChoice.SetSelection(wx.NOT_FOUND)

        self.UpdateBindStringDisplay()

    def OnListSelect(self, evt):
        selected = self.rearrangeList.GetSelection()
        selCommand = self.rearrangeList.GetClientData(selected)

        self.ShowUIFor(selCommand)
        evt.Skip()

    def UpdateBindStringDisplay(self):
        self.BindStringDisplay.SetLabel(self.MakeBindString())

    def MakeBindString(self):
        # Quick'n'dirty glom together of the bindstrings, for debugging
        cmdBindStrings = []
        for index in range(self.rearrangeList.GetCount()):
            c = self.rearrangeList.GetClientData(index)
            if c: cmdBindStrings.append(c.MakeBindString(self)) # why "if c"?!?

        bindstring = ('$$'.join(cmdBindStrings))
        return bindstring

    def ShowUIFor(self, command):

        # unshow anything that's showing
        # NEW - from either rearrangeList or bindchoice
        for index in range(0,self.rearrangeList.GetCount()):
            try:
                c = self.rearrangeList.GetClientData(index)
                if c and c.UI: self.mainSizer.Hide(c.UI)
            except Exception:
                pass

        for choice in range(self.bindChoice.GetCount()):
            try:
                c = self.bindChoice.GetClientData(choice)
                if c and c.UI: self.mainSizer.Hide(c.UI)
            except Exception:
                pass

        # ... and show the one we want
        if command and command.UI: self.mainSizer.Show(command.UI)

        self.Layout()
        self.Fit()


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

