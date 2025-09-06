import wx
import wx.lib.agw.ultimatelistctrl as ulc
from Help import HelpButton

import GameData

class qwyPetMouse(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qwyMouseSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(qwyMouseSizer)

        centeringSizer = wx.BoxSizer(wx.VERTICAL)

        self.ButtonGrid = ulc.UltimateListCtrl(self,
                    agwStyle = ulc.ULC_VRULES|ulc.ULC_HRULES|ulc.ULC_NO_HIGHLIGHT|ulc.ULC_REPORT)

        # column headers
        for i, name in enumerate(['Key', 'Minions', 'Lieutenants', 'Boss', 'All']):
            self.ButtonGrid.InsertColumn(i, name)

        for row in [
            ['2'                     , 'Attack'         , 'Attack'         , 'Attack'    , 'Attack']    ,
            ['ALT+LBUTTON'           , 'Target Next Pet', 'Target Next Pet', 'Go To'     , 'Go To']     ,
            [''                      , 'Go To'          , 'Go To'          , ''          , '']          ,
            ['ALT+RBUTTON'           , 'Stay'           , 'Stay'           , 'Stay'      , 'Stay']      ,
            ['RIGHTDOUBLECLICK'      , 'Follow'         , 'Follow'         , 'Follow'    , 'Follow']    ,
            ['ALT+RIGHTDOUBLECLICK'  , 'Defensive'      , 'Defensive'      , 'Defensive' , 'Defensive'] ,
            ['SHIFT+RIGHTDOUBLECLICK', 'Aggressive'     , 'Aggressive'     , 'Aggressive', 'Aggressive'],
            ['CTRL+RIGHTDOUBLECLICK' , 'Passive'        , 'Passive'        , 'Passive'   , 'Passive ']  ,
        ]:
            self.ButtonGrid.Append(row)

        for i in (0,1,2,3,4):
            self.ButtonGrid.SetColumnWidth(i, wx.LIST_AUTOSIZE)

        # This is awful
        rect = self.ButtonGrid.GetItemRect(0)
        height = rect.height * (self.ButtonGrid.GetItemCount()+2)
        width = rect.width
        self.ButtonGrid.SetMinSize((wx.Size(width, height)))
        self.ButtonGrid.SetAutoLayout(True)

        centeringSizer.Add(self.ButtonGrid, 1, wx.ALL, 15)

        qwyMouseSizer.Add(centeringSizer, 0, wx.ALIGN_CENTER)

        self.Fit()
        self.Layout()

    def GetKeyBinds(self):
        return [
            ['Select Minions'    , 'SHIFT+NUMPAD4'         ],
            ['Select Lieutenants', 'SHIFT+NUMPAD5'         ],
            ['Select Boss'       , 'SHIFT+NUMPAD6'         ],
            ['Select All'        , 'SHIFT+ADD'             ],
            ['Select None'       , 'CTRL+ADD'              ],
            ['Attack'            , '2'                     ],
            ['Open Popmenu'      , '4'                     ],
            ['Target Next Pet'   , 'ALT+LBUTTON'           ],
            ['Stay'              , 'ALT+RBUTTON'           ],
            ['Follow'            , 'RIGHTDOUBLECLICK'      ],
            ['Defensive'         , 'ALT+RIGHTDOUBLECLICK'  ],
            ['Aggressive'        , 'SHIFT+RIGHTDOUBLECLICK'],
            ['Passive'           , 'CTRL+RIGHTDOUBLECLICK' ],
        ]

    def PopulateBindFiles(self):
        profile = wx.App.Get().Main.Profile
        page    = profile.Mastermind
        primary = profile.GetState('Primary')
        pabb = GameData.MMPowerSets[primary]['abbrs']

        menu = MenuNames[primary]

        ResetFile = profile.ResetFile()
        ResetFile.SetBind('SHIFT+NUMPAD4', '', page, [f'targetcustomnext alive mypet {pabb[0]}', profile.BLF('mmqm', 't1.txt')])
        ResetFile.SetBind('SHIFT+NUMPAD5', '', page, [f'targetcustomnext alive mypet {pabb[3]}', profile.BLF('mmqm', 't2.txt')])
        ResetFile.SetBind('SHIFT+NUMPAD6', '', page, profile.BLF('mmqm', 't3.txt'))
        ResetFile.SetBind('SHIFT+ADD', '', page, profile.BLF('mmqm', 'all.txt'))
        ResetFile.SetBind('CTRL+ADD', '', page, profile.BLF('mmqm', 'off.txt'))
        ResetFile.SetBind('2', '', page, 'nop')
        ResetFile.SetBind('4', '', page, f'popmenu qwyPM-{menu}')
        ResetFile.SetBind('ALT+LBUTTON', '', page, 'nop')
        ResetFile.SetBind('ALT+RBUTTON', '', page, 'nop')
        ResetFile.SetBind('RIGHTDOUBLECLICK', '', page, 'nop')
        ResetFile.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'nop')
        ResetFile.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'nop')
        ResetFile.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'nop')

        OffFile = profile.GetBindFile('mmqm', 'off.txt')
        OffFile.SetBind('2', '', page, 'nop')
        OffFile.SetBind('ALT+LBUTTON', '', page, 'nop')
        OffFile.SetBind('ALT+RBUTTON', '', page, 'nop')
        OffFile.SetBind('RIGHTDOUBLECLICK', '', page, 'nop')
        OffFile.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'nop')
        OffFile.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'nop')
        OffFile.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'nop')

        AllFile = profile.GetBindFile('mmqm', 'all.txt')
        AllFile.SetBind('2', '', page, 'petcomall att')
        AllFile.SetBind('RIGHTDOUBLECLICK', '', page, 'petcomall fol')
        AllFile.SetBind('ALT+LBUTTON', '', page, 'petcomall got')
        AllFile.SetBind('ALT+RBUTTON', '', page, 'petcomall sta')
        AllFile.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'petcomall def')
        AllFile.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'petcomall agg')
        AllFile.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'petcomall pas')

        T1File = profile.GetBindFile('mmqm', 't1.txt')
        T1File.SetBind('2', '', page, 'petcom att')
        T1File.SetBind('ALT+LBUTTON', '', page, [f'targetcustomnext alive mypet {pabb[0]}', 'petcom got'])
        T1File.SetBind('ALT+RBUTTON', '', page, 'petcom sta')
        T1File.SetBind('RIGHTDOUBLECLICK', '', page, 'petcom fol')
        T1File.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'petcom def')
        T1File.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'petcom agg')
        T1File.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'petcom pas')

        T2File = profile.GetBindFile('mmqm', 't2.txt')
        T2File.SetBind('2', '', page, 'petcom att')
        T2File.SetBind('ALT+LBUTTON', '', page, [f'targetcustomnext alive mypet {pabb[3]}', 'petcom got'])
        T2File.SetBind('ALT+RBUTTON', '', page, 'petcom sta')
        T2File.SetBind('RIGHTDOUBLECLICK', '', page, 'petcom fol')
        T2File.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'petcom def')
        T2File.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'petcom agg')
        T2File.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'petcom pas')

        T3File = profile.GetBindFile('mmqm', 't3.txt')
        T3File.SetBind('2', '', page, f'petcompow {pabb[5]} att')
        T3File.SetBind('ALT+LBUTTON', '', page, f'petcompow {pabb[5]} got')
        T3File.SetBind('ALT+RBUTTON', '', page, f'petcompow {pabb[5]} sta')
        T3File.SetBind('RIGHTDOUBLECLICK', '', page, f'petcompow {pabb[5]} fol')
        T3File.SetBind('ALT+RIGHTDOUBLECLICK', '', page, f'petcompow {pabb[5]} def')
        T3File.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, f'petcompow {pabb[5]} agg')
        T3File.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, f'petcompow {pabb[5]} pas')

MenuNames = {
    "Beast Mastery"   : 'Beasts',
    "Demon Summoning" : 'Demons',
    "Mercenaries"     : 'Mercs',
    "Necromancy"      : 'Necro',
    "Ninjas"          : 'Ninjas',
    "Robotics"        : 'Bots',
    "Thugs"           : 'Thugs',
}
