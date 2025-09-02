import wx
import wx.lib.agw.ultimatelistctrl as ulc

import GameData

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

        # set it up with the longest possible strings before doing SetColumnWidth
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

    def PopulateBindFiles(self):
        # This is going to be complicated and tangly - there are like 14 files with many entries.
        profile = wx.App.Get().Main.Profile
        page    = profile.Mastermind
        primary = profile.GetState('Primary')
        pset = GameData.MMPowerSets[primary]

        # Pad.txt - central file, overriden by other via BLF
        PadFile = profile.GetBindFile('mmq', 'pad.txt')
        PadFile.SetBind('NUMPAD0', '', page, profile.BLF('mmq', 'pad.txt'))
        PadFile.SetBind('NUMPAD1', '', page, profile.BLF('mmq', 'min.txt'))
        PadFile.SetBind('NUMPAD2', '', page, profile.BLF('mmq', 'lt.txt'))
        PadFile.SetBind('NUMPAD3', '', page, profile.BLF('mmq', 'bos.txt'))
        PadFile.SetBind('NUMPAD4', '', page, 'petcomall def')
        PadFile.SetBind('NUMPAD5', '', page, 'petcomall agg')
        PadFile.SetBind('NUMPAD6', '', page, 'petcomall pas')
        PadFile.SetBind('NUMPAD7', '', page, 'petcomall sta')
        PadFile.SetBind('NUMPAD8', '', page, 'petcomall att')
        PadFile.SetBind('NUMPAD9', '', page, 'petcomall got')
        PadFile.SetBind('DIVIDE', '', page, ['show chat', 'beginchat /petsayall '])
        PadFile.SetBind('MULTIPLY', '', page, 'popmenu MMPad+')
        PadFile.SetBind('SUBTRACT', '', page, 'petcomall fol')
        PadFile.SetBind('ADD', '', page, ['+', 'targetcustomnext alive mypet', 'powexecauto upgrade robot', profile.BLF('mmq', '2up.txt')])
        PadFile.SetBind('NUMPADENTER', '', page, 'powexecname repair')
        PadFile.SetBind('DECIMAL', '', page, 'targetcustomnext alive mypet')
        PadFile.SetBind('ALT+NUMPAD0', '', page, 'nop')
        PadFile.SetBind('ALT+NUMPAD1', '', page, profile.BLF('mmq', 'min1.txt'))
        PadFile.SetBind('ALT+NUMPAD2', '', page, profile.BLF('mmq', 'min2.txt'))
        PadFile.SetBind('ALT+NUMPAD3', '', page, profile.BLF('mmq', 'min3.txt'))
        PadFile.SetBind('ALT+NUMPAD4', '', page, profile.BLF('mmq', 'lt1.txt'))
        PadFile.SetBind('ALT+NUMPAD5', '', page, profile.BLF('mmq', 'lt1.txt'))
        PadFile.SetBind('ALT+NUMPAD6', '', page, profile.BLF('mmq', 'boss.txt'))
        PadFile.SetBind('ALT+NUMPAD7', '', page, 'petcomall def sta')
        PadFile.SetBind('ALT+NUMPAD8', '', page, 'petcomall def att')
        PadFile.SetBind('ALT+NUMPAD9', '', page, 'petcomall def got')
        PadFile.SetBind('ALT+DIVIDE', '', page, ['show chat', f'beginchat /petsaypow {pset['min']} '])
        PadFile.SetBind('ALT+SUBTRACT', '', page, 'petcomall def fol')
        PadFile.SetBind('ALT+MULTIPLY', '', page, 'customwindowtoggle MMPad+')
        PadFile.SetBind('ALT+DECIMAL', '', page, f'targetcustomnext alive mypet {pset['min']}')
        PadFile.SetBind('SHIFT+NUMPAD0', '', page, 'petcom dis')
        # TODO TODO TODO get the full power names somehow
        PadFile.SetBind('SHIFT+NUMPAD1', '', page, 'powexeclocation back:2 Battle Drones')
        PadFile.SetBind('SHIFT+NUMPAD2', '', page, 'powexeclocation back:2 Protector Bots')
        PadFile.SetBind('SHIFT+NUMPAD3', '', page, 'powexeclocation back:2 Assault Bot')
        PadFile.SetBind('SHIFT+NUMPAD7', '', page, 'petcomall agg sta')
        PadFile.SetBind('SHIFT+NUMPAD8', '', page, 'petcomall agg att')
        PadFile.SetBind('SHIFT+NUMPAD9', '', page, 'petcomall agg got')
        PadFile.SetBind('SHIFT+DIVIDE', '', page, ['show chat', f'beginchat /petsaypow {pset['min']} '])
        PadFile.SetBind('SHIFT+SUBTRACT', '', page, 'petcomall agg fol')
        PadFile.SetBind('SHIFT+DECIMAL', '', page, f'targetcustomnext alive mypet {pset['lts']}')
        PadFile.SetBind('CTRL+NUMPAD0', '', page, 'petcomall dis')
        PadFile.SetBind('CTRL+NUMPAD1', '', page, f'petcompow {pset['min']} dis')
        PadFile.SetBind('CTRL+NUMPAD2', '', page, f'petcompow {pset['lts']} dis')
        PadFile.SetBind('CTRL+NUMPAD3', '', page, f'petcompow {pset['bos']} dis')
        PadFile.SetBind('CTRL+NUMPAD7', '', page, 'petcomall pas sta')
        PadFile.SetBind('CTRL+NUMPAD8', '', page, 'petcomall pas att')
        PadFile.SetBind('CTRL+NUMPAD9', '', page, 'petcomall pas got')
        PadFile.SetBind('CTRL+DIVIDE', '', page, ['show chat', f'beginchat /petsaypow {pset['bos']} '])
        PadFile.SetBind('CTRL+SUBTRACT', '', page, 'petcomall pas fol')
        PadFile.SetBind('CTRL+DECIMAL', '', page, f'petselectname {pset['bos']}')


GridContents = [
    [
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
        ['ADD', 'roll upgrades all', '', '', ''],
        ['NUMPADENTER', 'pet heal targeted', '', '', ''],
        ['DECIMAL', 'target pet', 'target next minion',' target next lieutenant', 'target boss'],
    ],
]
