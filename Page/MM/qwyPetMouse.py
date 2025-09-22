import re
import wx
from Help import HelpButton
from Page.PopmenuEditor import GetValidGamePath, CheckAndCreateMenuPathForGamePath
import UI
from UI.ControlGroup import ControlGroup, cgButton
from Util.Paths import GetRootDirPath

import GameData

class qwyPetMouse(wx.Panel):
    def __init__(self, page, parent):
        super().__init__(parent)

        page.Init.update({
                'qpmMinions'    : 'SHIFT+NUMPAD4'          ,
                'qpmLts'        : 'SHIFT+NUMPAD5'          ,
                'qpmBoss'       : 'SHIFT+NUMPAD6'          ,
                'qpmAll'        : 'SHIFT+ADD'              ,
                'qpmNone'       : 'CTRL+ADD'               ,
                'qpmAttack'     : '2'                      ,
                'qpmPopmenu'    : '4'                      ,
                'qpmTargetGoto' : 'ALT+LBUTTON'            ,
                'qpmStay'       : 'ALT+RBUTTON'            ,
                'qpmFollow'     : 'RIGHTDOUBLECLICK'       ,
                'qpmDefensive'  : 'ALT+RIGHTDOUBLECLICK'   ,
                'qpmAggressive' : 'SHIFT+RIGHTDOUBLECLICK' ,
                'qpmPassive'    : 'CTRL+RIGHTDOUBLECLICK'  ,
        })

        self.Profile = page.Profile
        self.qwyPetMouseKeyButtons = {}

        qwyMouseSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(qwyMouseSizer)

        centeringSizer = wx.BoxSizer(wx.VERTICAL)

        popmenusizer = wx.BoxSizer(wx.HORIZONTAL)
        popmenusizer.Add(HelpButton(self, 'qwyPetMouse.html'), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)
        self.InstallPopmenu = cgButton(self, label = 'Install Popmenu (recommended)')
        self.InstallPopmenu.DefaultToolTip = 'This will install the optional popmenu to your Game Directory.  This is not required, but is highly recommended.'
        self.InstallPopmenu.Bind(wx.EVT_BUTTON, self.OnInstallPopmenu)
        popmenusizer.Add(self.InstallPopmenu, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 6)

        centeringSizer.Add(popmenusizer, 0)

        self.ButtonGrid = ControlGroup(self, page)

        for ctlname, ctllabel in [
            ['qpmMinions'    , 'Switch to Minions + Target Next'     ] ,
            ['qpmLts'        , 'Switch to Lieutenants + Target Next' ] ,
            ['qpmBoss'       , 'Switch to Boss + Target'             ] ,
            ['qpmAll'        , 'Select All'                          ] ,
            ['qpmNone'       , 'Select None'                         ] ,
            ['qpmAttack'     , 'Attack'                              ] ,
            ['qpmPopmenu'    , 'Open Popmenu'                        ] ,
            ['qpmTargetGoto' , 'Target Next Pet In Group + Go To'    ] ,
            ['qpmStay'       , 'Stay'                                ] ,
            ['qpmFollow'     , 'Follow'                              ] ,
            ['qpmDefensive'  , 'Defensive'                           ] ,
            ['qpmAggressive' , 'Aggressive'                          ] ,
            ['qpmPassive'    , 'Passive'                             ] ,
        ]:
            self.ButtonGrid.AddControl(ctlType = 'keybutton', ctlName = ctlname, label = ctllabel)
            self.qwyPetMouseKeyButtons[ctlname] = page.Ctrls[ctlname]

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
            self.InstallPopmenu.AddError('gamepath', 'Your Game Directory is not correctly set up for installing popmenus.  Please visit the Preferences dialog.')
            self.InstallPopmenu.Enable(False)

    def OnInstallPopmenu(self, _):
        try:
            profile = self.Profile
            menu = f'qwyPetMouse-{profile.ProfileBindsDir}.mnu'

            if wx.MessageBox(f'This will install the popmenu "{menu}" to your Game Directory.  Proceed?', 'Install Popmenu', wx.YES_NO) == wx.NO:
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
        except Exception as e:
            wx.LogError(f'Something broke while installing popmenu: {e}.  This is a bug.')

    def PopulateBindFiles(self):
        profile = self.Profile
        page    = profile.Mastermind
        primary = profile.Primary()
        pabb = GameData.MMPowerSets[primary]['abbrs']
        uniq = page.uniqueNames

        menu = profile.ProfileBindsDir

        ResetFile = profile.ResetFile()
        ResetFile.SetBind(page.GetState('qpmMinions')    , '' , page , [f'petselectname {uniq[0]}'    , profile.BLF('mmqpm' , 't1-1.txt')])
        ResetFile.SetBind(page.GetState('qpmLts')        , '' , page , [f'petselectname {uniq[3]}'    , profile.BLF('mmqpm' , 't2-1.txt')])
        ResetFile.SetBind(page.GetState('qpmBoss')       , '' , page , [f'petselectname {uniq[5]}'    , profile.BLF('mmqpm' , 't3.txt')])
        ResetFile.SetBind(page.GetState('qpmAll')        , '' , page , profile.BLF('mmqpm'             , 'all.txt'))
        ResetFile.SetBind(page.GetState('qpmNone')       , '' , page , profile.BLF('mmqpm'             , 'off.txt'))
        ResetFile.SetBind(page.GetState('qpmAttack')     , '' , page , 'nop')
        ResetFile.SetBind(page.GetState('qpmPopmenu')    , '' , page , f'popmenu qwyPetMouse-{menu}')
        ResetFile.SetBind(page.GetState('qpmTargetGoto') , '' , page , 'nop')
        ResetFile.SetBind(page.GetState('qpmStay')       , '' , page , 'nop')
        ResetFile.SetBind(page.GetState('qpmFollow')     , '' , page , 'nop')
        ResetFile.SetBind(page.GetState('qpmDefensive')  , '' , page , 'nop')
        ResetFile.SetBind(page.GetState('qpmAggressive') , '' , page , 'nop')
        ResetFile.SetBind(page.GetState('qpmPassive')    , '' , page , 'nop')

        OffFile = profile.GetBindFile('mmqpm', 'off.txt')
        OffFile.SetBind(page.GetState('qpmAttack')     , ''         , page , 'nop')
        OffFile.SetBind(page.GetState('qpmTargetGoto') , ''         , page , 'nop')
        OffFile.SetBind(page.GetState('qpmStay')       , ''         , page , 'nop')
        OffFile.SetBind(page.GetState('qpmFollow')     , ''         , page , 'nop')
        OffFile.SetBind(page.GetState('qpmDefensive')  , ''         , page , 'nop')
        OffFile.SetBind(page.GetState('qpmAggressive') , ''         , page , 'nop')
        OffFile.SetBind(page.GetState('qpmPassive')    , ''         , page , 'nop')

        AllFile = profile.GetBindFile('mmqpm', 'all.txt')
        AllFile.SetBind(page.GetState('qpmAttack')     , ''         , page , 'petcomall att')
        AllFile.SetBind(page.GetState('qpmTargetGoto') , ''         , page , 'petcomall fol')
        AllFile.SetBind(page.GetState('qpmStay')       , ''         , page , 'petcomall got')
        AllFile.SetBind(page.GetState('qpmFollow')     , ''         , page , 'petcomall sta')
        AllFile.SetBind(page.GetState('qpmDefensive')  , ''         , page , 'petcomall def')
        AllFile.SetBind(page.GetState('qpmAggressive') , ''         , page , 'petcomall agg')
        AllFile.SetBind(page.GetState('qpmPassive')    , ''         , page , 'petcomall pas')

        T11File = profile.GetBindFile('mmqpm', 't1-1.txt')
        T11File.SetBind(page.GetState('qpmAttack')     , '' , page , 'petcom att')
        T11File.SetBind(page.GetState('qpmTargetGoto') , '' , page , [f'petselectname {uniq[0]}' , 'petcom got'       , profile.BLF('mmqpm' , 't1-2.txt')])
        T11File.SetBind(page.GetState('qpmMinions')    , '' , page , [f'petselectname {uniq[0]}' , profile.BLF('mmqpm' , 't1-2.txt')])
        T11File.SetBind(page.GetState('qpmStay')       , '' , page , 'petcom sta')
        T11File.SetBind(page.GetState('qpmFollow')     , '' , page , 'petcom fol')
        T11File.SetBind(page.GetState('qpmDefensive')  , '' , page , 'petcom def')
        T11File.SetBind(page.GetState('qpmAggressive') , '' , page , 'petcom agg')
        T11File.SetBind(page.GetState('qpmPassive')    , '' , page , 'petcom pas')

        T12File = profile.GetBindFile('mmqpm', 't1-2.txt')
        T12File.SetBind(page.GetState('qpmAttack')     , '' , page , 'petcom att')
        T12File.SetBind(page.GetState('qpmTargetGoto') , '' , page , [f'petselectname {uniq[1]}' , 'petcom got'       , profile.BLF('mmqpm' , 't1-3.txt')])
        T12File.SetBind(page.GetState('qpmMinions')    , '' , page , [f'petselectname {uniq[1]}' , profile.BLF('mmqpm' , 't1-3.txt')])
        T12File.SetBind(page.GetState('qpmStay')       , '' , page , 'petcom sta')
        T12File.SetBind(page.GetState('qpmFollow')     , '' , page , 'petcom fol')
        T12File.SetBind(page.GetState('qpmDefensive')  , '' , page , 'petcom def')
        T12File.SetBind(page.GetState('qpmAggressive') , '' , page , 'petcom agg')
        T12File.SetBind(page.GetState('qpmPassive')    , '' , page , 'petcom pas')

        T13File = profile.GetBindFile('mmqpm', 't1-3.txt')
        T13File.SetBind(page.GetState('qpmAttack')     , '' , page , 'petcom att')
        T13File.SetBind(page.GetState('qpmTargetGoto') , '' , page , [f'petselectname {uniq[2]}' , 'petcom got'       , profile.BLF('mmqpm' , 't1-1.txt')])
        T13File.SetBind(page.GetState('qpmMinions')    , '' , page , [f'petselectname {uniq[2]}' , profile.BLF('mmqpm' , 't1-1.txt')])
        T13File.SetBind(page.GetState('qpmStay')       , '' , page , 'petcom sta')
        T13File.SetBind(page.GetState('qpmFollow')     , '' , page , 'petcom fol')
        T13File.SetBind(page.GetState('qpmDefensive')  , '' , page , 'petcom def')
        T13File.SetBind(page.GetState('qpmAggressive') , '' , page , 'petcom agg')
        T13File.SetBind(page.GetState('qpmPassive')    , '' , page , 'petcom pas')

        T21File = profile.GetBindFile('mmqpm', 't2-1.txt')
        T21File.SetBind(page.GetState('qpmAttack')     , '' , page , 'petcom att')
        T21File.SetBind(page.GetState('qpmTargetGoto') , '' , page , [f'petselectname {uniq[3]}' , 'petcom got'       , profile.BLF('mmqpm' , 't2-2.txt')])
        T21File.SetBind(page.GetState('qpmLts')        , '' , page , [f'petselectname {uniq[3]}' , profile.BLF('mmqpm' , 't2-2.txt')])
        T21File.SetBind(page.GetState('qpmStay')       , '' , page , 'petcom sta')
        T21File.SetBind(page.GetState('qpmFollow')     , '' , page , 'petcom fol')
        T21File.SetBind(page.GetState('qpmDefensive')  , '' , page , 'petcom def')
        T21File.SetBind(page.GetState('qpmAggressive') , '' , page , 'petcom agg')
        T21File.SetBind(page.GetState('qpmPassive')    , '' , page , 'petcom pas')

        T22File = profile.GetBindFile('mmqpm', 't2-2.txt')
        T22File.SetBind(page.GetState('qpmAttack')     , '' , page , 'petcom att')
        T22File.SetBind(page.GetState('qpmTargetGoto') , '' , page , [f'petselectname {uniq[4]}' , 'petcom got'       , profile.BLF('mmqpm' , 't2-1.txt')])
        T22File.SetBind(page.GetState('qpmLts')        , '' , page , [f'petselectname {uniq[4]}' , profile.BLF('mmqpm' , 't2-1.txt')])
        T22File.SetBind(page.GetState('qpmStay')       , '' , page , 'petcom sta')
        T22File.SetBind(page.GetState('qpmFollow')     , '' , page , 'petcom fol')
        T22File.SetBind(page.GetState('qpmDefensive')  , '' , page , 'petcom def')
        T22File.SetBind(page.GetState('qpmAggressive') , '' , page , 'petcom agg')
        T22File.SetBind(page.GetState('qpmPassive')    , '' , page , 'petcom pas')

        T3File = profile.GetBindFile('mmqpm', 't3.txt')
        T3File.SetBind(page.GetState('qpmAttack')     , '' , page , f'petcompow {pabb[2]} att')
        T3File.SetBind(page.GetState('qpmTargetGoto') , '' , page , f'petcompow {pabb[2]} got')
        T3File.SetBind(page.GetState('qpmStay')       , '' , page , f'petcompow {pabb[2]} sta')
        T3File.SetBind(page.GetState('qpmFollow')     , '' , page , f'petcompow {pabb[2]} fol')
        T3File.SetBind(page.GetState('qpmDefensive')  , '' , page , f'petcompow {pabb[2]} def')
        T3File.SetBind(page.GetState('qpmAggressive') , '' , page , f'petcompow {pabb[2]} agg')
        T3File.SetBind(page.GetState('qpmPassive')    , '' , page , f'petcompow {pabb[2]} pas')

    def MungeMenuText(self, menutext):
        menutext = re.sub(r'<<([A-Z_]+)(\d)?>>', self.MungeMenuTextLookup, menutext)
        return menutext

    def MungeMenuTextLookup(self, matchobj):
        primary = self.Profile.Primary()
        pnam = GameData.MMPowerSets[primary]['names']
        shortprimary = re.sub(r'\s+', '', primary)
        shortpowers = [
            re.sub(r'\s+', '', pnam[0]),
            re.sub(r'\s+', '', pnam[1]),
            re.sub(r'\s+', '', pnam[2]),
        ]
        n = int(matchobj.group(2) or 0)

        match matchobj.group(1):

            case 'RESET_BLF':
                return re.sub(r'\\', r'\\\\\\\\', self.Profile.ResetFile().BLF()) # yes we need eight slashes
            case 'MENUNAME':
                return self.Profile.ProfileBindsDir
            case 'ABB':
                return GameData.MMPowerSets[primary]['abbrs'][n]
            case 'POWER':
                return pnam[n]
            case 'ICON':
                return f'{shortprimary}_{shortpowers[n]}'
            case 'UNIQ':
                return self.Profile.Mastermind.uniqueNames[n]
            case 'NAME':
                return self.Profile.Mastermind.GetState(f'Pet{n+1}Name')

        wx.LogError(f'Encountered an unknown tag in source popmenu: <<{matchobj.group(0)}>>.  This is a bug in the source popmenu.')
        return matchobj.group(0)

UI.Labels.update({
    'qpmMinions'    : 'Switch to Minions + Target Next'     ,
    'qpmLts'        : 'Switch to Lieutenants + Target Next' ,
    'qpmBoss'       : 'Switch to Boss + Target'             ,
    'qpmAll'        : 'Select All'                          ,
    'qpmNone'       : 'Select None'                         ,
    'qpmAttack'     : 'Attack'                              ,
    'qpmPopmenu'    : 'Open Popmenu'                        ,
    'qpmTargetGoto' : 'Target Next Pet In Group + Go To'    ,
    'qpmStay'       : 'Stay'                                ,
    'qpmFollow'     : 'Follow'                              ,
    'qpmDefensive'  : 'Defensive'                           ,
    'qpmAggressive' : 'Aggressive'                          ,
    'qpmPassive'    : 'Passive'                             ,
})
