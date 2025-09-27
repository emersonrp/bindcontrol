import wx
from UI.PowerBinderCommand import PowerBinderCommand

LFGSet_Numbers = {
    "Not Looking" : 0,
    "Any"         : 1,
    "Patrol"      : 2,
    "Missions"    : 4,
    "Task Force"  : 8,
    "Trial"       : 16,
    "Arena"       : 32,
    "No Invites"  : 128,
}

####### Window Save / Load
class LFGCmd(PowerBinderCommand):
    Name = "LFG Settings"
    Menu = "Social"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridBagSizer(2, 4)

        self.LFGSetRB = wx.RadioButton(dialog, wx.ID_ANY, label = "Looking for", style = wx.RB_GROUP)
        self.LFGSetRB.Bind(wx.EVT_RADIOBUTTON, self.SynchronizeUI)
        self.LFGSetRB.SetValue(True)
        sizer.Add(self.LFGSetRB, (0,0), (1,1), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.LFGSetChoice = wx.Choice(dialog, wx.ID_ANY, choices = list(LFGSet_Numbers.keys()))
        sizer.Add(self.LFGSetChoice, (0,1), (1,0), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.LFGSetChoice.SetSelection(0)

        self.LFGRemoveRB = wx.RadioButton(dialog, wx.ID_ANY, label = "Remove from LFG queue")
        self.LFGRemoveRB.Bind(wx.EVT_RADIOBUTTON, self.SynchronizeUI)
        sizer.Add(self.LFGRemoveRB, (1,0), (1,2), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.LFGToggleRB = wx.RadioButton(dialog, wx.ID_ANY, label = "Toggle LFG Status")
        self.LFGToggleRB.Bind(wx.EVT_RADIOBUTTON, self.SynchronizeUI)
        sizer.Add(self.LFGToggleRB, (2,0), (1,2), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.CommentCB = wx.CheckBox(dialog, wx.ID_ANY, label = "Set Search Comment")
        self.CommentCB.Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        sizer.Add(self.CommentCB, (3,0), (1,1), wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        self.Comment = wx.TextCtrl(dialog, wx.ID_ANY, )
        self.Comment.SetHint("Leave empty to clear comment")
        minsize = self.Comment.GetSizeFromText('Leave empty to clear comment')
        self.Comment.SetMinSize(minsize)
        # and let's make the choice picker thingie match
        self.LFGSetChoice.SetMinSize(minsize)
        sizer.Add(self.Comment, (3,1), (1,1), wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        CenteringSizer.Add(sizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        self.SynchronizeUI()
        return CenteringSizer

    def MakeBindString(self) -> str:
        lfgselection = ''
        if self.LFGSetRB.GetValue():
            command = "lfgset"
            lfgselection = f" {LFGSet_Numbers[self.LFGSetChoice.GetString(self.LFGSetChoice.GetSelection())]}"
        elif self.LFGToggleRB.GetValue():
            command = "lfgtoggle"
        else:
            command = "lfgremovefromqueue"

        comment = f"$$comment {self.Comment.GetValue()}" if self.CommentCB.IsChecked() else ''

        return f"{command}{lfgselection}{comment}"

    def Serialize(self) -> dict:
        if self.LFGSetRB.GetValue():
            lfgstate = 'lfgset'
        elif self.LFGToggleRB.GetValue():
            lfgstate = 'lfgtoggle'
        else:
            lfgstate = 'lfgremove'

        return {
                'lfgstate'   : lfgstate,
                'lfgvalue'   : self.LFGSetChoice.GetString(self.LFGSetChoice.GetSelection()),
                'usecomment' : self.CommentCB.IsChecked(),
                'comment'    : self.Comment.GetValue(),
        }

    def Deserialize(self, init) -> None:
        lfgstate = init.get('lfgstate', 'lfgset')
        if lfgstate == 'lfgset':
            self.LFGSetRB.SetValue(True)
        elif lfgstate == 'lfgtoggle':
            self.LFGToggleRB.SetValue(True)
        else:
            self.LFGRemoveRB.SetValue(True)

        self.LFGSetChoice.SetStringSelection(init.get('lfgvalue'))
        self.CommentCB.SetValue(init.get('usecomment', False))
        self.Comment.SetValue(init.get('comment', ''))

    def SynchronizeUI(self, evt = None) -> None:
        if evt: evt.Skip()

        self.LFGSetChoice.Enable(self.LFGSetRB.GetValue())
        self.Comment.Enable(self.CommentCB.IsChecked())

