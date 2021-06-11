import wx
import string
import UI
import GameData

from PowerBindCmd import AFKCmd, AutoPowerCmd, ChatCmd, ChatGlobalCmd, CostumeChangeCmd, CustomBindCmd, EmoteCmd, \
                    PowerBindCmd, TargetCustomCmd, TargetEnemyCmd, TargetFriendCmd, TeamPetSelectCmd, \
                    UseInspByNameCmd, UseInspRowColCmd, UsePowerCmd, UsePowerFromTrayCmd, WindowToggleCmd


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

        rearrangeCtrl = wx.RearrangeCtrl(self, -1, size=(550,400))
        sizer.Add(rearrangeCtrl, 1, wx.EXPAND)

        self.rearrangeList = rearrangeCtrl.GetList()
        self.rearrangeList.Bind(wx.EVT_LISTBOX, self.OnListSelect)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bindChoice = wx.Choice(self, -1, choices = [cmd for cmd in commandClasses])
        self.bindChoice.SetSelection(self.bindChoice.FindString("Use Power"))
        self.bindChoice.Bind(wx.EVT_CHOICE, self.OnBindChoice)
        choiceSizer.Add(self.bindChoice, 1, wx.ALIGN_CENTER_VERTICAL)

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

        self.ShowUIFor(None)

        self.Layout()
        self.Fit()


    def OnAddBind(self, evt):
        chosenName = self.bindChoice.GetString(self.bindChoice.GetSelection())

        # Stick it into the list
        newBindIndex = self.rearrangeList.Append(chosenName)
        self.rearrangeList.Select(newBindIndex)

        # Make the command object and glue it to the list entry
        newCommandClass = commandClasses[chosenName]
        if newCommandClass:
            newCommand = newCommandClass(self)
            self.rearrangeList.SetClientData(newBindIndex, newCommand)

            # Shim the UI bits for the new command into the dialog,
            # just above the buttons, and then do the correct showing/hiding
            self.mainSizer.Insert(self.mainSizer.GetItemCount()-1, newCommand.UI, 0, wx.EXPAND)
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
            if c and c.UI: self.mainSizer.Hide(c.UI)

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
    'Power Abort'              : None,
    'Power Unqueue'            : None,
    'SG Mode Toggle'           : None,
    'Target Custom'            : TargetCustomCmd.TargetCustomCmd,
    'Target Enemy'             : TargetEnemyCmd.TargetEnemyCmd,
    'Target Friend'            : TargetFriendCmd.TargetFriendCmd,
    'Team/Pet Select'          : TeamPetSelectCmd.TeamPetSelectCmd,
    'Unselect'                 : None,
    'Use Insp By Name'         : UseInspByNameCmd.UseInspByNameCmd,
    'Use Insp From Row/Column' : UseInspRowColCmd.UseInspRowColCmd,
    'Use Power'                : UsePowerCmd.UsePowerCmd,
    'Use Power From Tray'      : UsePowerFromTrayCmd.UsePowerFromTrayCmd,
    'Window Toggle'            : WindowToggleCmd.WindowToggleCmd,
}


