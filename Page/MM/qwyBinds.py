import wx
import wx.lib.agw.ultimatelistctrl as ulc

class qwyBinds(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qwyNumpadSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(qwyNumpadSizer)

        ButtonGrid = ulc.UltimateListCtrl(self,
                    agwStyle = ulc.ULC_VRULES|ulc.ULC_HRULES|ulc.ULC_NO_HIGHLIGHT|ulc.ULC_REPORT)

        # OK, let's make this thing happen

        # column headers
        for i, name in enumerate(['Key', 'No Chord', 'ALT+', 'SHIFT+', 'CTRL+']):
            ButtonGrid.InsertColumn(i, name)

        for row in [
            ['NUMLOCK', '-', '-', '-', '-'],
            ['DIVIDE', 'all pet say', 'all minions say', 'all lieutenants say', 'boss says'],
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
            ['DECIMAL', 'target next pet all', 'target next minion',' target next lieutenant', 'target boss'],
        ]: ButtonGrid.Append(row)

        for i in (0,1,2,3,4):
            ButtonGrid.SetColumnWidth(i, wx.LIST_AUTOSIZE)

        # This is awful
        rect = ButtonGrid.GetItemRect(0)
        height = rect.height * (ButtonGrid.GetItemCount()+2)
        width = rect.width
        ButtonGrid.SetMinSize((wx.Size(width, height)))
        ButtonGrid.SetAutoLayout(True)

        qwyNumpadSizer.Add(ButtonGrid, 0, wx.ALIGN_CENTER|wx.ALL, 25)

        self.Fit()
        self.Layout()
