import sys
import wx
import wx.lib.agw.ultimatelistctrl as ulc
from Help import HelpButton
from Page.PopmenuEditor import GetValidGamePath
from UI.ControlGroup import cgButton
from Util.Paths import GetRootDirPath

import GameData

class qwyPetMouse(wx.Panel):
    def __init__(self, page, parent):
        super().__init__(parent)

        self.Profile = page.Profile

        qwyMouseSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(qwyMouseSizer)

        centeringSizer = wx.BoxSizer(wx.VERTICAL)

        popmenusizer = wx.BoxSizer(wx.HORIZONTAL)
        self.InstallPopmenu = cgButton(self, label = 'Install Popmenu (recommended)')
        self.InstallPopmenu.Bind(wx.EVT_BUTTON, self.OnInstallPopmenu)
        popmenusizer.Add(self.InstallPopmenu, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        popmenusizer.Add(HelpButton(self, 'qwyPetMouse.html'), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        centeringSizer.Add(popmenusizer, 0)

        self.ButtonGrid = ulc.UltimateListCtrl(self,
                    agwStyle = ulc.ULC_VRULES|ulc.ULC_HRULES|ulc.ULC_NO_HIGHLIGHT|ulc.ULC_REPORT)

        # column headers
        for i, name in enumerate(['Key', 'Function']):
            self.ButtonGrid.InsertColumn(i, name)

        for row in [
            ['SHIFT+NUMPAD4'          , 'Select + Target Next Minion'     ],
            ['SHIFT+NUMPAD5'          , 'Select + Target Next Lieutenant' ],
            ['SHIFT+NUMPAD6'          , 'Select Boss'                     ],
            ['SHIFT+ADD'              , 'Select All'                      ],
            ['CTRL+ADD'               , 'Select None'                     ],
            ['2'                      , 'Attack'                          ],
            ['4'                      , 'Open Popmenu'                    ],
            ['ALT+LBUTTON'            , 'Target Next Pet In Group + Go To'],
            ['ALT+RBUTTON'            , 'Stay'                            ],
            ['RIGHTDOUBLECLICK'       , 'Follow'                          ],
            ['ALT+RIGHTDOUBLECLICK'   , 'Defensive'                       ],
            ['SHIFT+RIGHTDOUBLECLICK' , 'Aggressive'                      ],
            ['CTRL+RIGHTDOUBLECLICK'  , 'Passive'                         ],
        ]:
            self.ButtonGrid.Append(row)

        self.ButtonGrid.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.ButtonGrid.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        # This is awful
        rect = self.ButtonGrid.GetItemRect(0)
        height = rect.height * (self.ButtonGrid.GetItemCount()+2)
        width = rect.width
        self.ButtonGrid.SetMinSize((wx.Size(width, height)))
        self.ButtonGrid.SetAutoLayout(True)

        centeringSizer.Add(self.ButtonGrid, 1)

        qwyMouseSizer.Add(centeringSizer, 0, wx.ALIGN_CENTER|wx.ALL, 15)

        self.CheckPopmenuPath()
        self.Fit()
        self.Layout()

    def CheckPopmenuPath(self):
        if GetValidGamePath(self.Profile.Server):
            self.InstallPopmenu.RemoveError('gamepath')
            self.InstallPopmenu.Enable()
        else:
            self.InstallPopmenu.AddError('gamepath', 'Your gamepath is not correctly set up for installing popmenus.  Please visit the Preferences dialog.')
            self.InstallPopmenu.Enable(False)

    def OnInstallPopmenu(self, _):
        profile = self.Profile
        primary = profile.GetState('Primary')
        menu = MenuNames[primary]

        if wx.MessageBox(f'This will install the popmenu "qwyPM-{menu}.mnu" to your game directory.  Proceed?', 'Install Popmenu', wx.YES_NO) == wx.ID_NO:
            return

        file_path = GetRootDirPath() / 'popmenus' / f'qwyPM-{menu}.mnu'

        # GET CORRECT DIRECTORY FROM POPMENU EDITOR

        # if file exists, warn
        if file_path.exists():
            if wx.MessageBox(f'The popmenu "qwyPM-{menu}.mnu" already exists in the game directory.  Overwrite?', 'Popemnu Exists', wx.YES_NO) == wx.ID_NO:
                return




        # otherwise, copy it from /popmenus/ to GameDir/texts/etc/etc/etc/

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
        profile = self.Profile
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
