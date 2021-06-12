import wx
import string
import UI
import GameData

from PowerBindCmd import AFKCmd, AutoPowerCmd, ChatCmd, ChatGlobalCmd, CostumeChangeCmd, CustomBindCmd, EmoteCmd, \
                    PowerAbortCmd, PowerBindCmd, PowerUnqueueCmd, SGModeToggleCmd, TargetCustomCmd, TargetEnemyCmd, \
                    TargetFriendCmd, TeamPetSelectCmd, UnselectCmd, UseInspByNameCmd, UseInspRowColCmd, UsePowerCmd, \
                    UsePowerFromTrayCmd, WindowToggleCmd


def PowerBinderEventHandler(evt):
    button = evt.EventObject
    print(button)

    with PowerBinderDialog(button.Parent) as dlg:

        if(dlg.ShowModal() == wx.ID_OK):
            bindString = dlg.MakeBindString()
            button.targetTextCtrl.SetValue(bindString)

class PowerBinderDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "PowerBinder", style = wx.DEFAULT_DIALOG_STYLE)

        sizer = wx.BoxSizer(wx.VERTICAL);
        self.mainSizer = sizer

        rearrangeCtrl = wx.RearrangeCtrl(self, -1, size=(550,400))
        sizer.Add(rearrangeCtrl, 1, wx.EXPAND)

        self.rearrangeList = rearrangeCtrl.GetList()
        self.rearrangeList.Bind(wx.EVT_LISTBOX, self.OnListSelect)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bindChoice = wx.Choice(self, -1, choices = [cmd for cmd in commandClasses])
        self.bindChoice.Bind(wx.EVT_CHOICE, self.OnBindChoice)
        choiceSizer.Add(self.bindChoice, 1, wx.ALIGN_CENTER_VERTICAL)

        addBindButton = wx.Button(self, -1, "Add")
        choiceSizer.Add(addBindButton, 0, wx.ALIGN_CENTER_VERTICAL)
        addBindButton.Bind(wx.EVT_BUTTON, self.OnAddBind)

        showBindStringButton = wx.Button(self, -1, "Show Bind String")
        choiceSizer.Add(showBindStringButton, 0, wx.ALIGN_CENTER_VERTICAL)
        showBindStringButton.Bind(wx.EVT_BUTTON, self.OnShowBindString)

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


    def OnAddBind(self, evt):
        # find the item we just poked "add" next to
        chosenSel  = self.bindChoice.GetSelection()
        chosenName = self.bindChoice.GetString(chosenSel)

        # detach the command object from self.bindChoice, and instead glue it
        # to self.rearrangeList
        newCommand = self.bindChoice.DetachClientObject(chosenSel)
        newBindIndex = self.rearrangeList.Append(chosenName)
        self.rearrangeList.Select(newBindIndex)
        self.rearrangeList.SetClientData(newBindIndex, newCommand)

        # hide its UI for now, and move the Choice Away
        self.ShowUIFor(None)
        self.bindChoice.SetSelection(wx.NOT_FOUND)

    def OnListSelect(self, evt):
        selected = self.rearrangeList.GetSelection()
        selCommand = self.rearrangeList.GetClientData(selected)

        self.ShowUIFor(selCommand)
        evt.Skip()

    def OnShowBindString(self, evt):
        bindstring = self.MakeBindString()

    def MakeBindString(self):
        # Quick'n'dirty glom together of the bindstrings, for debugging
        cmdBindStrings = []
        for index in range(self.rearrangeList.GetCount()):
            c = self.rearrangeList.GetClientData(index)
            if c: cmdBindStrings.append(c.MakeBindString(self)) # why "if c"?!?

        bindstring = ('$$'.join(cmdBindStrings))
        print(bindstring)
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
    def __init__(self, parent, targetTextCtrl):
        wx.Button.__init__(self, parent, -1, label = "...")

        print(self)
        self.targetTextCtrl = targetTextCtrl
        self.Bind(wx.EVT_BUTTON, PowerBinderEventHandler)
