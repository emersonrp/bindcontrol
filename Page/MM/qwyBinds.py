import wx
import wx.lib.agw.ultimatelistctrl as ulc

class qwyBinds(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qwyNumpadSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(qwyNumpadSizer)

        centeringSizer = wx.BoxSizer(wx.VERTICAL)

        PetPickedSizer = wx.BoxSizer(wx.HORIZONTAL)
        PetPickedSizer.Add(wx.StaticText(self, label = 'Pet Selection:'), flag = wx.ALIGN_CENTER)
        self.PetPicker = wx.Choice(self, choices = ['All Pets', 'Pet Group', 'Individual Pet'])
        self.PetPicker.SetSelection(0)
        PetPickedSizer.Add(self.PetPicker, 0, wx.LEFT|wx.ALIGN_CENTER, 6)
        self.PetPicker.Bind(wx.EVT_CHOICE, self.OnPetPicked)

        centeringSizer.Add(PetPickedSizer, 0, wx.TOP|wx.BOTTOM, 10)

        self.ButtonGrid = ulc.UltimateListCtrl(self,
                    agwStyle = ulc.ULC_VRULES|ulc.ULC_HRULES|ulc.ULC_NO_HIGHLIGHT|ulc.ULC_REPORT)

        # column headers
        for i, name in enumerate(['Key', 'No Chord', 'ALT+', 'SHIFT+', 'CTRL+']):
            self.ButtonGrid.InsertColumn(i, name)

        # set it up with the longest strings before doing SetColumnWidth
        for row in GridContents[1]:
            self.ButtonGrid.Append(row)


        for i in (0,1,2,3,4):
            self.ButtonGrid.SetColumnWidth(i, wx.LIST_AUTOSIZE)

        self.OnPetPicked()

        # This is awful
        rect = self.ButtonGrid.GetItemRect(0)
        height = rect.height * (self.ButtonGrid.GetItemCount()+2)
        width = rect.width
        self.ButtonGrid.SetMinSize((wx.Size(width, height)))
        self.ButtonGrid.SetAutoLayout(True)

        centeringSizer.Add(self.ButtonGrid, 1)

        qwyNumpadSizer.Add(centeringSizer, 0, wx.ALIGN_CENTER)

        self.Fit()
        self.Layout()

    def OnPetPicked(self, evt = None):
        contents = GridContents[self.PetPicker.GetSelection()]

        self.ButtonGrid.DeleteAllItems()

        for row in contents:
            self.ButtonGrid.Append(row)

        if evt: evt.Skip()

GridContents = [
    [
        ['NUMLOCK', '-', '-', '-', '-'],
        ['DIVIDE', 'all pets say', 'minions say', 'lieutenants say', 'boss says'],
        ['MULTIPLY', 'open popmenu', 'toggle custom window', '', ''],
        ['SUBTRACT', 'all follow', 'all def follow', 'all agg follow', 'all pas follow'],
        ['NUMPAD9', 'all goto', 'all def goto', 'all agg goto', 'all pas goto'],
        ['NUMPAD8', 'all attack', 'all def attack', 'all agg attack', 'all pas attack'],
        ['NUMPAD7', 'all stay', 'all def stay', 'all agg stay', 'all pas stay', ],
        ['NUMPAD6', 'all passive', 'select boss', '', ''],
        ['NUMPAD5', 'all aggressive', 'select lieutenant 2', '', ''],
        ['NUMPAD4', 'all defense', 'select lieutenant 1', '', '', ],
        ['NUMPAD3', 'select boss', 'select minion 3', 'summon boss', 'dismiss boss'],
        ['NUMPAD2', 'select lieutenants', 'select minion 2', 'summon lieutenants', 'dismiss lieutenants'],
        ['NUMPAD1', 'select minions', 'select minion 1', 'summon minions', 'dismiss minions'],
        ['NUMPAD0', 'select all', '', 'dismiss target', 'dismiss all'],
        ['ADD', 'roll upgrades', '', '', ''],
        ['NUMPADENTER', 'pet heal targeted', '', '', ''],
        ['DECIMAL', 'target next pet', 'target next minion',' target next lieutenant', 'target boss'],
    ],
    [
        ['NUMLOCK', '-', '-', '-', '-'],
        ['DIVIDE', 'group pets say', 'minions say', 'lieutenants say', 'boss says'],
        ['MULTIPLY', 'open MMPad + popmenu', 'toggle MMPad + custom window', '', ''],
        ['SUBTRACT', 'group follow', 'group def follow', 'group agg follow', 'group pas follow'],
        ['NUMPAD9', 'group goto', 'group def goto', 'group agg goto', 'group pas goto'],
        ['NUMPAD8', 'group attack', 'group def attack', 'group agg attack', 'group pas attack'],
        ['NUMPAD7', 'group stay', 'group def stay', 'group agg stay', 'group pas stay', ],
        ['NUMPAD6', 'group passive', 'select boss', '', ''],
        ['NUMPAD5', 'group aggressive', 'select lieutenant 2', '', ''],
        ['NUMPAD4', 'group defense', 'select lieutenant 1', '', '', ],
        ['NUMPAD3', 'select boss', 'select minion 3', 'summon boss', 'dismiss boss'],
        ['NUMPAD2', 'select lieutenants', 'select minion 2', 'summon lieutenants', 'dismiss lieutenants'],
        ['NUMPAD1', 'select minions', 'select minion 1', 'summon minions', 'dismiss minions'],
        ['NUMPAD0', 'select all', '', 'dismiss target', 'dismiss all'],
        ['ADD', 'roll upgrades all', '', '', ''],
        ['NUMPADENTER', 'pet heal targeted', '', '', ''],
        ['DECIMAL', 'target next pet in group', 'target next minion',' target next lieutenant', 'target boss'],
    ],
    [
        ['NUMLOCK', '-', '-', '-', '-'],
        ['DIVIDE', 'pet says', 'minions say', 'lieutenants say', 'boss says'],
        ['MULTIPLY', 'open popmenu', 'toggle custom window', '', ''],
        ['SUBTRACT', 'pet follow', 'pet def follow', 'pet agg follow', 'pet pas follow'],
        ['NUMPAD9', 'pet goto', 'pet def goto', 'pet agg goto', 'pet pas goto'],
        ['NUMPAD8', 'pet attack', 'pet def attack', 'pet agg attack', 'pet pas attack'],
        ['NUMPAD7', 'pet stay', 'pet def stay', 'pet agg stay', 'pet pas stay', ],
        ['NUMPAD6', 'pet passive', 'select boss', '', ''],
        ['NUMPAD5', 'pet aggressive', 'select lieutenant 2', '', ''],
        ['NUMPAD4', 'pet defense', 'select lieutenant 1', '', '', ],
        ['NUMPAD3', 'select boss', 'select minion 3', 'summon boss', 'dismiss boss'],
        ['NUMPAD2', 'select lieutenants', 'select minion 2', 'summon lieutenants', 'dismiss lieutenants'],
        ['NUMPAD1', 'select minions', 'select minion 1', 'summon minions', 'dismiss minions'],
        ['NUMPAD0', 'select all', 'dismiss selected', 'dismiss target', 'dismiss all'],
        ['ADD', 'roll upgrades', '', '', ''],
        ['NUMPADENTER', 'pet heal targeted', '', '', ''],
        ['DECIMAL', 'target pet', 'target next minion',' target next lieutenant', 'target boss'],
    ],
]

