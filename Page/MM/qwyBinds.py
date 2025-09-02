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
        pabb = GameData.MMPowerSets[primary]['abbrs']
        pnam = GameData.MMPowerSets[primary]['names']
        heal = GameData.MMPowerSets[primary]['heal']
        upgr = GameData.MMPowerSets[primary]['upgrade']
        uniq = page.uniqueNames

        # core binds, some get overridden via BLF.  Put them in the reset file
        ResetFile = profile.ResetFile()
        ResetFile.SetBind('NUMPAD0', '', page, profile.BLF('mmqn', 'pad.txt'))
        ResetFile.SetBind('NUMPAD1', '', page, profile.BLF('mmqn', 'min.txt'))
        ResetFile.SetBind('NUMPAD2', '', page, profile.BLF('mmqn', 'lt.txt'))
        ResetFile.SetBind('NUMPAD3', '', page, profile.BLF('mmqn', 'bos.txt'))
        ResetFile.SetBind('NUMPAD4', '', page, 'petcomall def')
        ResetFile.SetBind('NUMPAD5', '', page, 'petcomall agg')
        ResetFile.SetBind('NUMPAD6', '', page, 'petcomall pas')
        ResetFile.SetBind('NUMPAD7', '', page, 'petcomall sta')
        ResetFile.SetBind('NUMPAD8', '', page, 'petcomall att')
        ResetFile.SetBind('NUMPAD9', '', page, 'petcomall got')
        ResetFile.SetBind('DIVIDE', '', page, ['show chat', 'beginchat /petsayall '])
        ResetFile.SetBind('MULTIPLY', '', page, 'popmenu MMPad+')
        ResetFile.SetBind('SUBTRACT', '', page, 'petcomall fol')
        ResetFile.SetBind('ADD', '', page, ['+', 'targetcustomnext alive mypet', f'powexecauto {upgr[0]}', profile.BLF('mmqn', '2up.txt')])
        ResetFile.SetBind('NUMPADENTER', '', page, f'powexecname {heal}')
        ResetFile.SetBind('DECIMAL', '', page, 'targetcustomnext alive mypet')
        ResetFile.SetBind('ALT+NUMPAD0', '', page, 'nop')
        ResetFile.SetBind('ALT+NUMPAD1', '', page, profile.BLF('mmqn', 'min1.txt'))
        ResetFile.SetBind('ALT+NUMPAD2', '', page, profile.BLF('mmqn', 'min2.txt'))
        ResetFile.SetBind('ALT+NUMPAD3', '', page, profile.BLF('mmqn', 'min3.txt'))
        ResetFile.SetBind('ALT+NUMPAD4', '', page, profile.BLF('mmqn', 'lt1.txt'))
        ResetFile.SetBind('ALT+NUMPAD5', '', page, profile.BLF('mmqn', 'lt1.txt'))
        ResetFile.SetBind('ALT+NUMPAD6', '', page, profile.BLF('mmqn', 'boss.txt'))
        ResetFile.SetBind('ALT+NUMPAD7', '', page, 'petcomall def sta')
        ResetFile.SetBind('ALT+NUMPAD8', '', page, 'petcomall def att')
        ResetFile.SetBind('ALT+NUMPAD9', '', page, 'petcomall def got')
        ResetFile.SetBind('ALT+DIVIDE', '', page, ['show chat', f'beginchat /petsaypow {pabb[0]} '])
        ResetFile.SetBind('ALT+SUBTRACT', '', page, 'petcomall def fol')
        ResetFile.SetBind('ALT+MULTIPLY', '', page, 'customwindowtoggle MMPad+')
        ResetFile.SetBind('ALT+DECIMAL', '', page, f'targetcustomnext alive mypet {pabb[0]}')
        ResetFile.SetBind('SHIFT+NUMPAD0', '', page, 'petcom dis')
        # TODO:  "If Homecoming" else just powexecname?
        ResetFile.SetBind('SHIFT+NUMPAD1', '', page, f'powexeclocation back:2 {pnam[0]}')
        ResetFile.SetBind('SHIFT+NUMPAD2', '', page, f'powexeclocation back:2 {pnam[1]}')
        ResetFile.SetBind('SHIFT+NUMPAD3', '', page, f'powexeclocation back:2 {pnam[2]}')
        ResetFile.SetBind('SHIFT+NUMPAD7', '', page, 'petcomall agg sta')
        ResetFile.SetBind('SHIFT+NUMPAD8', '', page, 'petcomall agg att')
        ResetFile.SetBind('SHIFT+NUMPAD9', '', page, 'petcomall agg got')
        ResetFile.SetBind('SHIFT+DIVIDE', '', page, ['show chat', f'beginchat /petsaypow {pabb[0]} '])
        ResetFile.SetBind('SHIFT+SUBTRACT', '', page, 'petcomall agg fol')
        ResetFile.SetBind('SHIFT+DECIMAL', '', page, f'targetcustomnext alive mypet {pabb[1]}')
        ResetFile.SetBind('CTRL+NUMPAD0', '', page, 'petcomall dis')
        ResetFile.SetBind('CTRL+NUMPAD1', '', page, f'petcompow {pabb[0]} dis')
        ResetFile.SetBind('CTRL+NUMPAD2', '', page, f'petcompow {pabb[1]} dis')
        ResetFile.SetBind('CTRL+NUMPAD3', '', page, f'petcompow {pabb[2]} dis')
        ResetFile.SetBind('CTRL+NUMPAD7', '', page, 'petcomall pas sta')
        ResetFile.SetBind('CTRL+NUMPAD8', '', page, 'petcomall pas att')
        ResetFile.SetBind('CTRL+NUMPAD9', '', page, 'petcomall pas got')
        ResetFile.SetBind('CTRL+DIVIDE', '', page, ['show chat', f'beginchat /petsaypow {pabb[2]} '])
        ResetFile.SetBind('CTRL+SUBTRACT', '', page, 'petcomall pas fol')
        ResetFile.SetBind('CTRL+DECIMAL', '', page, f'petselectname {pabb[2]}')

        # Individual pet files:  min1, min2, min3, lt1, lt2, boss
        for i in range(6):
            fn = ['min1', 'min2', 'min3', 'lt1', 'lt2', 'boss'][i]
            PetFile = profile.GetBindFile('mmqn', f'{fn}.txt')
            PetFile.SetBind('NUMPAD4', '', page, f'petcomname {uniq[i]} def')
            PetFile.SetBind('NUMPAD5', '', page, f'petcomname {uniq[i]} agg')
            PetFile.SetBind('NUMPAD6', '', page, f'petcomname {uniq[i]} pas')
            PetFile.SetBind('NUMPAD7', '', page, f'petcomname {uniq[i]} sta')
            PetFile.SetBind('NUMPAD8', '', page, f'petcomname {uniq[i]} att')
            PetFile.SetBind('NUMPAD9', '', page, f'petcomname {uniq[i]} got')
            PetFile.SetBind('DIVIDE', '', page, ['show chat', f'beginchat /petsayname {uniq[i]} '])
            PetFile.SetBind('SUBTRACT', '', page, f'petcomname {uniq[i]} fol')
            PetFile.SetBind('DECIMAL', '', page, f'petselectname {uniq[i]}')
            PetFile.SetBind('ALT+NUMPAD0', '', page, f'petcom {uniq[i]} dis')
            PetFile.SetBind('ALT+NUMPAD7', '', page, f'petcomname {uniq[i]} def sta')
            PetFile.SetBind('ALT+NUMPAD8', '', page, f'petcomname {uniq[i]} def att')
            PetFile.SetBind('ALT+NUMPAD9', '', page, f'petcomname {uniq[i]} def got')
            PetFile.SetBind('ALT+SUBTRACT', '', page, f'petcomname {uniq[i]} def fol')
            PetFile.SetBind('SHIFT+NUMPAD7', '', page, f'petcomname {uniq[i]} agg sta')
            PetFile.SetBind('SHIFT+NUMPAD8', '', page, f'petcomname {uniq[i]} agg att')
            PetFile.SetBind('SHIFT+NUMPAD9', '', page, f'petcomname {uniq[i]} agg got')
            PetFile.SetBind('SHIFT+SUBTRACT', '', page, f'petcomname {uniq[i]} agg fol')
            PetFile.SetBind('CTRL+NUMPAD7', '', page, f'petcomname {uniq[i]} pas sta')
            PetFile.SetBind('CTRL+NUMPAD8', '', page, f'petcomname {uniq[i]} pas att')
            PetFile.SetBind('CTRL+NUMPAD9', '', page, f'petcomname {uniq[i]} pas got')
            PetFile.SetBind('CTRL+SUBTRACT', '', page, f'petcomname {uniq[i]} pas fol')

        for i, grp in enumerate(['mins', 'lts']):
            GrpFile = profile.GetBindFile('mmqn', f'{grp}.txt')
            GrpFile.SetBind('NUMPAD4', '', page, f'petcompow {pabb[i]} def')
            GrpFile.SetBind('NUMPAD5', '', page, f'petcompow {pabb[i]} agg')
            GrpFile.SetBind('NUMPAD6', '', page, f'petcompow {pabb[i]} pas')
            GrpFile.SetBind('NUMPAD7', '', page, f'petcompow {pabb[i]} sta')
            GrpFile.SetBind('NUMPAD8', '', page, f'petcompow {pabb[i]} att')
            GrpFile.SetBind('NUMPAD9', '', page, f'petcompow {pabb[i]} got')
            GrpFile.SetBind('DIVIDE', '', page, ['show chat', 'beginchat /petsaypow {pabb[i]} '])
            GrpFile.SetBind('SUBTRACT', '', page, f'petcompow {pabb[i]} fol')
            GrpFile.SetBind('DECIMAL', '', page, f'targetcustomnext alive mypet {pabb[i]}')
            GrpFile.SetBind('ALT+NUMPAD0', '', page, f'nop')
            GrpFile.SetBind('ALT+NUMPAD7', '', page, f'petcompow {pabb[i]} def sta')
            GrpFile.SetBind('ALT+NUMPAD8', '', page, f'petcompow {pabb[i]} def att')
            GrpFile.SetBind('ALT+NUMPAD9', '', page, f'petcompow {pabb[i]} def got')
            GrpFile.SetBind('ALT+SUBTRACT', '', page, f'petcompow {pabb[i]} def fol')
            GrpFile.SetBind('SHIFT+NUMPAD7', '', page, f'petcompow {pabb[i]} agg sta')
            GrpFile.SetBind('SHIFT+NUMPAD8', '', page, f'petcompow {pabb[i]} agg att')
            GrpFile.SetBind('SHIFT+NUMPAD9', '', page, f'petcompow {pabb[i]} agg got')
            GrpFile.SetBind('SHIFT+SUBTRACT', '', page, f'petcompow {pabb[i]} agg fol')
            GrpFile.SetBind('CTRL+NUMPAD7', '', page, f'petcompow {pabb[i]} pas sta')
            GrpFile.SetBind('CTRL+NUMPAD8', '', page, f'petcompow {pabb[i]} pas att')
            GrpFile.SetBind('CTRL+NUMPAD9', '', page, f'petcompow {pabb[i]} pas got')
            GrpFile.SetBind('CTRL+SUBTRACT', '', page, f'petcompow {pabb[i]} pas fol')

        Pet1UpFile = profile.GetBindFile('mmqn', '1up.txt')
        Pet1UpFile.SetBind('ADD', '', page, ['+', 'targetcustomnext alive mypet', f'powexecauto {upgr[0]}', profile.BLF('mmqn', '2up.txt')])

        Pet2UpFile = profile.GetBindFile('mmqn', '2up.txt')
        Pet2UpFile.SetBind('ADD', '', page, ['+', 'targetcustomnext alive mypet', f'powexecauto {upgr[1]}', profile.BLF('mmqn', '1up.txt')])

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
