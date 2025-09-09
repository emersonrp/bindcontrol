import re
import wx
import wx.lib.agw.ultimatelistctrl as ulc
from Help import HelpButton
from Page.PopmenuEditor import GetValidGamePath, CheckAndCreateMenuPathForGamePath
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
        menu = f'qwyPetMouse-{profile.ProfileBindsDir}.mnu'

        if wx.MessageBox(f'This will install the popmenu "{menu}" to your game directory.  Proceed?', 'Install Popmenu', wx.YES_NO) == wx.NO:
            return

        filepath = GetRootDirPath() / 'popmenus' / 'qwyPetMouse.mnu'
        if not filepath.exists():
            wx.LogError(f'Cannot find source popmenu in the BindControl install directory.  This is a bug.')
            return

        # This method side-effects checking, verifying, and creating the menupath
        menupath = CheckAndCreateMenuPathForGamePath(GetValidGamePath(self.Profile.Server))
        if not menupath: return

        # read the text from the source file and make all necessary substitutions
        menutext = self.MungeMenuText(filepath.read_text())

        # import the menu file from popmenus/* using the PopmenuEditor.
        # doImportMenu throws its own errors.
        self.Profile.PopmenuEditor.doImportMenu(menupath, text = menutext, allow_overwrite = True)

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
        primary = profile.Primary()
        pabb = GameData.MMPowerSets[primary]['abbrs']
        uniq = page.uniqueNames

        menu = profile.ProfileBindsDir

        ResetFile = profile.ResetFile()
        ResetFile.SetBind('SHIFT+NUMPAD4', '', page, [f'petselectname {uniq[0]}', profile.BLF('mmqm', 't1-1.txt')])
        ResetFile.SetBind('SHIFT+NUMPAD5', '', page, [f'petselectname {uniq[3]}', profile.BLF('mmqm', 't2-1.txt')])
        ResetFile.SetBind('SHIFT+NUMPAD6', '', page, [f'petselectname {uniq[5]}', profile.BLF('mmqm', 't3.txt')])
        ResetFile.SetBind('SHIFT+ADD', '', page, profile.BLF('mmqm', 'all.txt'))
        ResetFile.SetBind('CTRL+ADD', '', page, profile.BLF('mmqm', 'off.txt'))
        ResetFile.SetBind('2', '', page, 'nop')
        ResetFile.SetBind('4', '', page, f'popmenu qwyPetMouse-{menu}')
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

        T11File = profile.GetBindFile('mmqm', 't1-1.txt')
        T11File.SetBind('2', '', page, 'petcom att')
        T11File.SetBind('ALT+LBUTTON', '', page, [f'petselectname {uniq[0]}', 'petcom got', profile.BLF('mmqm', 't1-2.txt')])
        T11File.SetBind('SHIFT+4', '', page, [f'petselectname {uniq[0]}', profile.BLF('mmqm', 't1-2.txt')])
        T11File.SetBind('ALT+RBUTTON', '', page, 'petcom sta')
        T11File.SetBind('RIGHTDOUBLECLICK', '', page, 'petcom fol')
        T11File.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'petcom def')
        T11File.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'petcom agg')
        T11File.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'petcom pas')

        T12File = profile.GetBindFile('mmqm', 't1-2.txt')
        T12File.SetBind('2', '', page, 'petcom att')
        T12File.SetBind('ALT+LBUTTON', '', page, [f'petselectname {uniq[1]}', 'petcom got', profile.BLF('mmqm', 't1-3.txt')])
        T12File.SetBind('SHIFT+4', '', page, [f'petselectname {uniq[1]}', profile.BLF('mmqm', 't1-3.txt')])
        T12File.SetBind('ALT+RBUTTON', '', page, 'petcom sta')
        T12File.SetBind('RIGHTDOUBLECLICK', '', page, 'petcom fol')
        T12File.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'petcom def')
        T12File.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'petcom agg')
        T12File.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'petcom pas')

        T13File = profile.GetBindFile('mmqm', 't1-3.txt')
        T13File.SetBind('2', '', page, 'petcom att')
        T13File.SetBind('ALT+LBUTTON', '', page, [f'petselectname {uniq[2]}', 'petcom got', profile.BLF('mmqm', 't1-1.txt')])
        T13File.SetBind('SHIFT+4', '', page, [f'petselectname {uniq[2]}', profile.BLF('mmqm', 't1-1.txt')])
        T13File.SetBind('ALT+RBUTTON', '', page, 'petcom sta')
        T13File.SetBind('RIGHTDOUBLECLICK', '', page, 'petcom fol')
        T13File.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'petcom def')
        T13File.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'petcom agg')
        T13File.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'petcom pas')

        T21File = profile.GetBindFile('mmqm', 't2-1.txt')
        T21File.SetBind('2', '', page, 'petcom att')
        T21File.SetBind('ALT+LBUTTON', '', page, [f'petselectname {uniq[3]}', 'petcom got', profile.BLF('mmqm', 't2-2.txt')])
        T21File.SetBind('SHIFT+5', '', page, [f'petselectname {uniq[3]}', profile.BLF('mmqm', 't2-2.txt')])
        T21File.SetBind('ALT+RBUTTON', '', page, 'petcom sta')
        T21File.SetBind('RIGHTDOUBLECLICK', '', page, 'petcom fol')
        T21File.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'petcom def')
        T21File.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'petcom agg')
        T21File.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'petcom pas')

        T22File = profile.GetBindFile('mmqm', 't2-2.txt')
        T22File.SetBind('2', '', page, 'petcom att')
        T22File.SetBind('ALT+LBUTTON', '', page, [f'petselectname {uniq[4]}', 'petcom got', profile.BLF('mmqm', 't2-1.txt')])
        T22File.SetBind('SHIFT+5', '', page, [f'petselectname {uniq[4]}', profile.BLF('mmqm', 't2-1.txt')])
        T22File.SetBind('ALT+RBUTTON', '', page, 'petcom sta')
        T22File.SetBind('RIGHTDOUBLECLICK', '', page, 'petcom fol')
        T22File.SetBind('ALT+RIGHTDOUBLECLICK', '', page, 'petcom def')
        T22File.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, 'petcom agg')
        T22File.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, 'petcom pas')

        T3File = profile.GetBindFile('mmqm', 't3.txt')
        T3File.SetBind('2', '', page, f'petcompow {pabb[2]} att')
        T3File.SetBind('ALT+LBUTTON', '', page, f'petcompow {pabb[2]} got')
        T3File.SetBind('ALT+RBUTTON', '', page, f'petcompow {pabb[2]} sta')
        T3File.SetBind('RIGHTDOUBLECLICK', '', page, f'petcompow {pabb[2]} fol')
        T3File.SetBind('ALT+RIGHTDOUBLECLICK', '', page, f'petcompow {pabb[2]} def')
        T3File.SetBind('SHIFT+RIGHTDOUBLECLICK', '', page, f'petcompow {pabb[2]} agg')
        T3File.SetBind('CTRL+RIGHTDOUBLECLICK', '', page, f'petcompow {pabb[2]} pas')

    def MungeMenuText(self, menutext):
        primary = self.Profile.Primary()
        pabb = GameData.MMPowerSets[primary]['abbrs']
        pnam = GameData.MMPowerSets[primary]['names']
        uniq = self.Profile.Mastermind.uniqueNames
        shortprim = re.sub(r'\s+', '', primary)
        shortpow0 = re.sub(r'\s+', '', pnam[0])
        shortpow1 = re.sub(r'\s+', '', pnam[1])
        shortpow2 = re.sub(r'\s+', '', pnam[2])
        reset_blf = re.sub(r'\\', r'\\\\\\\\', self.Profile.ResetFile().BLF()) # yes we need eight slashes

        menutext = re.sub(r'<<RESET_BLF>>', reset_blf, menutext)
        menutext = re.sub(r'<<MENUNAME>>', self.Profile.ProfileBindsDir, menutext)
        menutext = re.sub(r'<<ABB0>>', pabb[0], menutext)
        menutext = re.sub(r'<<ABB1>>', pabb[1], menutext)
        menutext = re.sub(r'<<ABB2>>', pabb[2], menutext)
        menutext = re.sub(r'<<POWER0>>', pnam[0], menutext)
        menutext = re.sub(r'<<POWER1>>', pnam[1], menutext)
        menutext = re.sub(r'<<POWER2>>', pnam[2], menutext)
        menutext = re.sub(r'<<ICON0>>', f'{shortprim}_{shortpow0}', menutext)
        menutext = re.sub(r'<<ICON1>>', f'{shortprim}_{shortpow1}', menutext)
        menutext = re.sub(r'<<ICON2>>', f'{shortprim}_{shortpow2}', menutext)
        menutext = re.sub(r'<<UNIQ0>>', uniq[0], menutext)
        menutext = re.sub(r'<<UNIQ1>>', uniq[1], menutext)
        menutext = re.sub(r'<<UNIQ2>>', uniq[2], menutext)
        menutext = re.sub(r'<<UNIQ3>>', uniq[3], menutext)
        menutext = re.sub(r'<<UNIQ4>>', uniq[4], menutext)
        menutext = re.sub(r'<<UNIQ5>>', uniq[5], menutext)
        menutext = re.sub(r'<<NAME0>>', self.Profile.Mastermind.GetState('Pet1Name'), menutext)
        menutext = re.sub(r'<<NAME1>>', self.Profile.Mastermind.GetState('Pet2Name'), menutext)
        menutext = re.sub(r'<<NAME2>>', self.Profile.Mastermind.GetState('Pet3Name'), menutext)
        menutext = re.sub(r'<<NAME3>>', self.Profile.Mastermind.GetState('Pet4Name'), menutext)
        menutext = re.sub(r'<<NAME4>>', self.Profile.Mastermind.GetState('Pet5Name'), menutext)
        menutext = re.sub(r'<<NAME5>>', self.Profile.Mastermind.GetState('Pet6Name'), menutext)

        return menutext
