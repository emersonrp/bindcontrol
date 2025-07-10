import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Window Save / Load
class HideUnhideCmd(PowerBinderCommand):
    Name = "Hide / Unhide"
    Menu = "Social"

    def BuildUI(self, dialog):
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        hidePicker = wx.BoxSizer(wx.VERTICAL)
        self.HideShowDialog = wx.RadioButton(dialog, wx.ID_ANY, "Show Hide Dialog")
        self.HideShowDialog.Bind(wx.EVT_RADIOBUTTON, self.SynchronizeUI)
        self.HideSet        = wx.RadioButton(dialog, wx.ID_ANY, "Hide from...")
        self.HideSet       .Bind(wx.EVT_RADIOBUTTON, self.SynchronizeUI)
        self.Unhide         = wx.RadioButton(dialog, wx.ID_ANY, "Unhide from...")
        self.Unhide        .Bind(wx.EVT_RADIOBUTTON, self.SynchronizeUI)
        hidePicker.Add(self.HideShowDialog, 1, wx.EXPAND|wx.ALL, 5)
        hidePicker.Add(self.HideSet       , 1, wx.EXPAND|wx.ALL, 5)
        hidePicker.Add(self.Unhide        , 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(hidePicker, 0, wx.EXPAND|wx.ALL, 5)

        hideFromGrid = wx.GridSizer(2, 5, 5)
        self.HSearches   = wx.CheckBox(dialog, wx.ID_ANY, "Searches")
        self.HSupergroup = wx.CheckBox(dialog, wx.ID_ANY, "Supergroup")
        self.HFriends    = wx.CheckBox(dialog, wx.ID_ANY, "Friends")
        self.HGFriends   = wx.CheckBox(dialog, wx.ID_ANY, "Global Friends")
        self.HGChannels  = wx.CheckBox(dialog, wx.ID_ANY, "Global Channels")
        self.HTells      = wx.CheckBox(dialog, wx.ID_ANY, "Tells")
        self.HInvites    = wx.CheckBox(dialog, wx.ID_ANY, "Invites")
        hideFromGrid.Add(self.HSearches, 0, wx.EXPAND)
        hideFromGrid.Add(self.HGChannels, 0, wx.EXPAND)
        hideFromGrid.Add(self.HSupergroup, 0, wx.EXPAND)
        hideFromGrid.Add(self.HTells, 0, wx.EXPAND)
        hideFromGrid.Add(self.HFriends, 0, wx.EXPAND)
        hideFromGrid.Add(self.HInvites, 0, wx.EXPAND)
        hideFromGrid.Add(self.HGFriends, 0, wx.EXPAND)
        sizer.Add(hideFromGrid, 0, wx.EXPAND|wx.ALL, 5)

        self.SynchronizeUI()

        CenteringSizer.Add(sizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        return CenteringSizer

    def MakeBindString(self):
        if self.HideShowDialog.GetValue() == True:
            return "hide"
        elif self.HideSet.GetValue() == True:
            hidevalue = 0
            if self.HSearches  .IsChecked(): hidevalue += 1
            if self.HSupergroup.IsChecked(): hidevalue += 2
            if self.HFriends   .IsChecked(): hidevalue += 4
            if self.HGFriends  .IsChecked(): hidevalue += 8
            if self.HGChannels .IsChecked(): hidevalue += 16
            if self.HTells     .IsChecked(): hidevalue += 32
            if self.HInvites   .IsChecked(): hidevalue += 64
            return f"hideset {hidevalue}"
        else: # unhide doesn't have an unhideset version, sigh...
            commands = []
            if self.HSearches  .IsChecked(): commands.append('unhidesearch')
            if self.HSupergroup.IsChecked(): commands.append('unhidesg')
            if self.HFriends   .IsChecked(): commands.append('unhidefriends')
            if self.HGFriends  .IsChecked(): commands.append('unhidegfriends')
            if self.HGChannels .IsChecked(): commands.append('unhidegchannels')
            if self.HTells     .IsChecked(): commands.append('unhidetell')
            if self.HInvites   .IsChecked(): commands.append('unhideinvite')
            if len(commands) == 7: # checked all
                return "unhideall"
            else:
                return '$$'.join(commands)

    def Serialize(self):
        if self.HideShowDialog.GetValue() == True:
            hidepicker = 'dialog'
        elif self.HideSet.GetValue() == True:
            hidepicker = 'hide'
        else:
            hidepicker = 'unhide'

        return {
            'hidepicker' : hidepicker,
            'searches'   : self.HSearches.IsChecked(),
            'supergroup' : self.HSupergroup.IsChecked(),
            'friends'    : self.HFriends.IsChecked(),
            'gfriends'   : self.HGFriends.IsChecked(),
            'gchannels'  : self.HGChannels.IsChecked(),
            'tells'      : self.HTells.IsChecked(),
            'invites'    : self.HInvites.IsChecked(),
        }

    def Deserialize(self, init):
        hidepicker = init.get('hidepicker', 'dialog')
        if hidepicker == 'dialog':
            self.HideShowDialog.SetValue(True)
        elif hidepicker == 'hide':
            self.HideSet.SetValue(True)
        else:
            self.Unhide.SetValue(True)

        self.HSearches  .SetValue(init.get('searches', False))
        self.HSupergroup.SetValue(init.get('supergroup', False))
        self.HFriends   .SetValue(init.get('friends', False))
        self.HGFriends  .SetValue(init.get('gfriends', False))
        self.HGChannels .SetValue(init.get('gchannels', False))
        self.HTells     .SetValue(init.get('tells', False))
        self.HInvites   .SetValue(init.get('invites', False))

        self.SynchronizeUI()

    def SynchronizeUI(self, evt = None):
        if evt: evt.Skip()
        # if we have NOY chosen "Show Dialog" then enable the checkboxes
        self.HSearches  .Enable(self.HideShowDialog.GetValue() != True)
        self.HSupergroup.Enable(self.HideShowDialog.GetValue() != True)
        self.HFriends   .Enable(self.HideShowDialog.GetValue() != True)
        self.HGFriends  .Enable(self.HideShowDialog.GetValue() != True)
        self.HGChannels .Enable(self.HideShowDialog.GetValue() != True)
        self.HTells     .Enable(self.HideShowDialog.GetValue() != True)
        self.HInvites   .Enable(self.HideShowDialog.GetValue() != True)

