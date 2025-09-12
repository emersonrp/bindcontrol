import wx
import wx.lib.agw.ultimatelistctrl as ulc
from Help import HelpButton

import GameData

class qwyNumpad(wx.Panel):
    def __init__(self, page, parent):
        super().__init__(parent)

        qwyNumpadSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(qwyNumpadSizer)

        centeringSizer = wx.BoxSizer(wx.VERTICAL)

        PetPickedSizer = wx.BoxSizer(wx.HORIZONTAL)

        PetPickedSizer.Add(HelpButton(self, 'qwyNumpad.html'), 0, wx.ALIGN_CENTER|wx.RIGHT, 10)

        PetPickedSizer.Add(wx.StaticText(self, label = 'Pet Selection:'), flag = wx.ALIGN_CENTER)
        self.PetPicker = wx.Choice(self, choices = ['All Pets', 'Pet Group', 'Individual Pet'])
        self.PetPicker.SetSelection(0)
        PetPickedSizer.Add(self.PetPicker, 0, wx.LEFT|wx.ALIGN_CENTER, 10)
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

    def GetKeyBinds(self):
        return [
            [ 'Select All'                       ,'NUMPAD0'       ,],
            [ 'Select Minions'                   ,'NUMPAD1'       ,],
            [ 'Select Lieutenants'               ,'NUMPAD2'       ,],
            [ 'Select Boss'                      ,'NUMPAD3'       ,],
            [ 'Selected Pets Defense'            ,'NUMPAD4'       ,],
            [ 'Selected Pets Aggressive'         ,'NUMPAD5'       ,],
            [ 'Selected Pets Passive'            ,'NUMPAD6'       ,],
            [ 'Selected Pets Stay'               ,'NUMPAD7'       ,],
            [ 'Selected Pets Attack'             ,'NUMPAD8'       ,],
            [ 'Selected Pets Go To'              ,'NUMPAD9'       ,],
            [ 'Selected Pets Say'                ,'DIVIDE'        ,],
            [ 'Selected Pets Follow'             ,'SUBTRACT'      ,],
            [ 'Upgrade Pets'                     ,'ADD'           ,],
            [ 'Heal Targeted Pet'                ,'NUMPADENTER'   ,],
            [ 'Select Next Pet In Group'         ,'DECIMAL'       ,],
            [ 'Dismiss Selected Pet'             ,'ALT+NUMPAD0'   ,],
            [ 'Select Minion 1'                  ,'ALT+NUMPAD1'   ,],
            [ 'Select Minion 2'                  ,'ALT+NUMPAD2'   ,],
            [ 'Select Minion 3'                  ,'ALT+NUMPAD3'   ,],
            [ 'Select Lieutenant 1'              ,'ALT+NUMPAD4'   ,],
            [ 'Select Lieutenant 2'              ,'ALT+NUMPAD5'   ,],
            [ 'Select Boss'                      ,'ALT+NUMPAD6'   ,],
            [ 'Selected Pets Defensive / Stay'   ,'ALT+NUMPAD7'   ,],
            [ 'Selected Pets Defensive / Attack' ,'ALT+NUMPAD8'   ,],
            [ 'Selected Pets Defensive / Go To'  ,'ALT+NUMPAD9'   ,],
            [ 'All Minions Say'                  ,'ALT+DIVIDE'    ,],
            [ 'Selected Pets Defensive / Follow' ,'ALT+SUBTRACT'  ,],
            [ 'Target Next Minion'               ,'ALT+DECIMAL'   ,],
            [ 'Dismiss Targeted Pet'             ,'SHIFT+NUMPAD0' ,],
            [ 'Summon Minions'                   ,'SHIFT+NUMPAD1' ,],
            [ 'Summon Lieutenants'               ,'SHIFT+NUMPAD2' ,],
            [ 'Summon Boss'                      ,'SHIFT+NUMPAD3' ,],
            [ 'Selected Pets Aggressive / Stay'  ,'SHIFT+NUMPAD7' ,],
            [ 'Selected Pets Aggressive / Attack','SHIFT+NUMPAD8' ,],
            [ 'Selected Pets Aggressive / Go To' ,'SHIFT+NUMPAD9' ,],
            [ 'All Lieutenants Say'              ,'SHIFT+DIVIDE'  ,],
            [ 'Selected Pets Aggressive / Follow','SHIFT+SUBTRACT',],
            [ 'Target Next Lieutenant'           ,'SHIFT+DECIMAL' ,],
            [ 'Dismiss All Pets'                 ,'CTRL+NUMPAD0'  ,],
            [ 'Dismiss Minions'                  ,'CTRL+NUMPAD1'  ,],
            [ 'Dismiss Lieutenants'              ,'CTRL+NUMPAD2'  ,],
            [ 'Dismiss Boss'                     ,'CTRL+NUMPAD3'  ,],
            [ 'Selected Pets Passive / Stay'     ,'CTRL+NUMPAD7'  ,],
            [ 'Selected Pets Passive / Attack'   ,'CTRL+NUMPAD8'  ,],
            [ 'Selected Pets Passive / Go To'    ,'CTRL+NUMPAD9'  ,],
            [ 'Boss Says'                        ,'CTRL+DIVIDE'   ,],
            [ 'Selected Pets Passive / Follow'   ,'CTRL+SUBTRACT' ,],
            [ 'Target Boss'                      ,'CTRL+DECIMAL'  ,],
        ]

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
        primary = profile.General.GetState('Primary')
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
        ['DIVIDE', 'All Pets Say', 'Minions Say', 'Lieutenants Say', 'Boss Says'],
        ['SUBTRACT', 'All Follow', 'All Def Follow', 'All Agg Follow', 'All Pas Follow'],
        ['NUMPAD9', 'All Goto', 'All Def Goto', 'All Agg Goto', 'All Pas Goto'],
        ['NUMPAD8', 'All Attack', 'All Def Attack', 'All Agg Attack', 'All Pas Attack'],
        ['NUMPAD7', 'All Stay', 'All Def Stay', 'All Agg Stay', 'All Pas Stay', ],
        ['NUMPAD6', 'All Passive', 'Select Boss', '', ''],
        ['NUMPAD5', 'All Aggressive', 'Select Lieutenant 2', '', ''],
        ['NUMPAD4', 'All Defense', 'Select Lieutenant 1', '', '', ],
        ['NUMPAD3', 'Select Boss', 'Select Minion 3', 'Summon Boss', 'Dismiss Boss'],
        ['NUMPAD2', 'Select Lieutenants', 'Select Minion 2', 'Summon Lieutenants', 'Dismiss Lieutenants'],
        ['NUMPAD1', 'Select Minions', 'Select Minion 1', 'Summon Minions', 'Dismiss Minions'],
        ['NUMPAD0', 'Select All', '', 'Dismiss Target', 'Dismiss All'],
        ['ADD', 'Perform Upgrades', '', '', ''],
        ['NUMPADENTER', 'Heal Targeted Pet', '', '', ''],
        ['DECIMAL', 'Target Next Pet', 'Target Next Minion',' Target Next Lieutenant', 'Target Boss'],
    ],
    [
        ['DIVIDE', 'Group Pets Say', 'Minions Say', 'Lieutenants Say', 'Boss Says'],
        ['SUBTRACT', 'Group Follow', 'Group Def Follow', 'Group Agg Follow', 'Group Pas Follow'],
        ['NUMPAD9', 'Group Goto', 'Group Def Goto', 'Group Agg Goto', 'Group Pas Goto'],
        ['NUMPAD8', 'Group Attack', 'Group Def Attack', 'Group Agg Attack', 'Group Pas Attack'],
        ['NUMPAD7', 'Group Stay', 'Group Def Stay', 'Group Agg Stay', 'Group Pas Stay', ],
        ['NUMPAD6', 'Group Passive', 'Select Boss', '', ''],
        ['NUMPAD5', 'Group Aggressive', 'Select Lieutenant 2', '', ''],
        ['NUMPAD4', 'Group Defense', 'Select Lieutenant 1', '', '', ],
        ['NUMPAD3', 'Select Boss', 'Select Minion 3', 'Summon Boss', 'Dismiss Boss'],
        ['NUMPAD2', 'Select Lieutenants', 'Select Minion 2', 'Summon Lieutenants', 'Dismiss Lieutenants'],
        ['NUMPAD1', 'Select Minions', 'Select Minion 1', 'Summon Minions', 'Dismiss Minions'],
        ['NUMPAD0', 'Select All', '', 'Dismiss Target', 'Dismiss All'],
        ['ADD', 'Perform Upgrades All', '', '', ''],
        ['NUMPADENTER', 'Heal Targeted Pet', '', '', ''],
        ['DECIMAL', 'Target Next Pet In Group', 'Target Next Minion',' Target Next Lieutenant', 'Target Boss'],
    ],
    [
        ['DIVIDE', 'Pet Says', 'Minions Say', 'Lieutenants Say', 'Boss Says'],
        ['SUBTRACT', 'Pet Follow', 'Pet Def Follow', 'Pet Agg Follow', 'Pet Pas Follow'],
        ['NUMPAD9', 'Pet Goto', 'Pet Def Goto', 'Pet Agg Goto', 'Pet Pas Goto'],
        ['NUMPAD8', 'Pet Attack', 'Pet Def Attack', 'Pet Agg Attack', 'Pet Pas Attack'],
        ['NUMPAD7', 'Pet Stay', 'Pet Def Stay', 'Pet Agg Stay', 'Pet Pas Stay', ],
        ['NUMPAD6', 'Pet Passive', 'Select Boss', '', ''],
        ['NUMPAD5', 'Pet Aggressive', 'Select Lieutenant 2', '', ''],
        ['NUMPAD4', 'Pet Defense', 'Select Lieutenant 1', '', '', ],
        ['NUMPAD3', 'Select Boss', 'Select Minion 3', 'Summon Boss', 'Dismiss Boss'],
        ['NUMPAD2', 'Select Lieutenants', 'Select Minion 2', 'Summon Lieutenants', 'Dismiss Lieutenants'],
        ['NUMPAD1', 'Select Minions', 'Select Minion 1', 'Summon Minions', 'Dismiss Minions'],
        ['NUMPAD0', 'Select All', 'Dismiss Selected', 'Dismiss Target', 'Dismiss All'],
        ['ADD', 'Perform Upgrades All', '', '', ''],
        ['NUMPADENTER', 'Heal Targeted Pet', '', '', ''],
        ['DECIMAL', 'Target Pet', 'Target Next Minion',' Target Next Lieutenant', 'Target Boss'],
    ],
]
