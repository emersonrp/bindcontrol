import wx
import re
import GameData
import UI
import Utility
from pathlib import Path, PureWindowsPath

from Page import Page
from UI.ControlGroup import ControlGroup
from BindFile import BindFile
from KeyBind.FileKeyBind import FileKeyBind


class SoD(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Speed On Demand"

        self.Init = {
            'Up'                 : "SPACE",
            'Down'               : "X",
            'Forward'            : "W",
            'Back'               : "S",
            'Left'               : "A",
            'Right'              : "D",
            'TurnLeft'           : "Q",
            'TurnRight'          : "E",
            'AutoRun'            : "R",
            'Follow'             : "TILDE",
            'DefaultMode'        : "Sprint",
            'MousechordSoD'      : 0,
            'AutoMouseLook'      : 0,

            'SprintPower'        : 'Sprint',
            'SprintSoD'          : True,

            'ChangeCamera'       : 1,
            'CamdistBase'        : 15,
            'CamdistTravelling'  : 60,

            'ChangeDetail'       : 1,
            'DetailBase'         : 100,
            'DetailTravelling'   : 50,

            'NonSoDMode'         : 'CTRL+M',
            'JumpMode'           : "T",
            'SimpleSJCJ'         : 1,

            'RunMode'            : "C",
            'SSOnlyWhenMoving'   : 0,
            'SSSJModeEnable'     : 1,

            'FlyMode'            : "F",
            'GFlyMode'           : "G",

            'SelfTellOnChange'   : 1,

            'TPMode'             : 'SHIFT+LBUTTON',
            'TPCombo'            : 'SHIFT',
            'TPReset'            : 'CTRL+T',

            'TTPMode'            : 'SHIFT+CTRL+LBUTTON',
            'TTPCombo'           : 'SHIFT+CTRL',
            'TTPReset'           : 'SHIFT+CTRL+T',
            'TTPAutoGFly'        : True,

            'TPHideWindows'      : False,
            'TPAutoHover'        : True,

            'RunPrimary'         : "Super Speed",
            'RunPrimaryNumber'   : 2,
            'RunSecondary'       : "Sprint",
            'RunSecondaryNumber' : 1,
            'FlyHover'           : 1,
            'FlyFly'             : '',
            'FlyGFly'            : '',
            'EnableSoD'          : True,
        }

        self.Init['NovaMode'] = "T"
        self.Init['NovaTray'] = "4"

        self.Init['DwarfMode'] = "G"
        self.Init['DwarfTray'] = "5"

        # TODO we aren't ever a kheldian during init so this doesn't do anything
        # I think this is the only place we have this logic yet, though.
        if (self.Profile.General.Init['Archetype'] == "Peacebringer"):
            self.Init['NovaNova'] = "Bright Nova"
            self.Init['DwarfDwarf'] = "White Dwarf"
            self.Init['HumanFormShield'] = "Shining Shield"

        elif (self.Profile.General.Init['Archetype'] == "Warshade"):
            self.Init['NovaNova'] = "Dark Nova"
            self.Init['DwarfDwarf'] = "Black Dwarf"
            self.Init['HumanFormShield'] = "Gravity Shield"

        self.Init['HumanMode']    = ""
        self.Init['HumanTray']    = "1"
        self.Init['HumanHumanPBind'] = "nop"
        self.Init['HumanNovaPBind']  = "nop"
        self.Init['HumanDwarfPBind'] = "nop"

        #  Temp Travel Powers
        self.Init['TempTray'] = "6"
        self.Init['TempTraySwitch'] = ""
        self.Init['TempMode'] = ""

    def BuildPage(self):

        topSizer = wx.FlexGridSizer(0,2,10,10)
        EnableSoD = wx.CheckBox( self, -1, "Enable Speed On Demand Binds",  )

        topSizer.Add( EnableSoD, 0, wx.TOP|wx.LEFT, 10)
        topSizer.AddSpacer(1)
        self.Ctrls['EnableSoD'] = EnableSoD
        EnableSoD.Bind(wx.EVT_CHECKBOX, self.OnEnableSoD)

        leftColumn  = wx.BoxSizer(wx.VERTICAL)
        rightColumn = wx.BoxSizer(wx.VERTICAL)


        ##### MOVEMENT KEYS
        movementSizer = ControlGroup(self, self, 'Movement Keys')

        for dir in ("Up","Down","Forward","Back","Left","Right","TurnLeft","TurnRight"):
            movementSizer.AddControl(
                ctlName = dir,
                ctlType = 'keybutton',
            )
        movementSizer.AddControl(
            ctlName = 'MousechordSoD',
            ctlType = 'checkbox',
        )
        leftColumn.Add(movementSizer, 0, wx.EXPAND)


        ##### GENERAL SETTINGS
        generalSizer = ControlGroup(self, self, 'General Settings')

        # TODO!  fill this picker with only the appropriate bits.
        # for i in (powers list):
        #   if (player has power): add_to_contents(i)
        generalSizer.AddControl(
            ctlName = 'DefaultMode',
            ctlType = 'combo',
            contents = ('No SoD','Sprint','Super Speed','Jump','Fly'),
        )
        generalSizer.AddControl(
            ctlName = 'SprintPower',
            ctlType = 'combo',
            contents = GameData.SprintPowers,
        )
        generalSizer.AddControl(
            ctlName = 'AutoMouseLook',
            ctlType = 'checkbox',
            tooltip = 'Automatically Mouselook when moving',
        )

        for command in ("AutoRun","Follow","NonSoDMode"): # TODO - lost "Sprint-Only SoD Mode" b/c couldn't find the name in %$Labels
            generalSizer.AddControl(
                ctlName = command,
                ctlType = 'keybutton',
            )
        generalSizer.AddControl(
            ctlName = 'SprintSoD',
            ctlType = 'checkbox',
        )
        generalSizer.AddControl(
            ctlName = 'ChangeCamera',
            ctlType = 'checkbox',
        )
        generalSizer.AddControl(
            ctlName = 'CamdistBase',
            ctlType = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddControl(
            ctlName = 'CamdistTravelling',
            ctlType = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddControl(
            ctlName = 'ChangeDetail',
            ctlType = 'checkbox',
        )
        generalSizer.AddControl(
            ctlName = 'DetailBase',
            ctlType = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddControl(
            ctlName = 'DetailTravelling',
            ctlType = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddControl(
            ctlName = 'TPHideWindows',
            ctlType = 'checkbox',
        )
        generalSizer.AddControl(
            ctlName = 'SelfTellOnChange',
            ctlType = 'checkbox',
        )
        leftColumn.Add(generalSizer, 0, wx.EXPAND)


        ##### TEMP TRAVEL POWERS
        tempSizer = ControlGroup(self, self, 'Temp Travel Powers')
        # if (temp travel powers exist)?  Should this be "custom"?
        tempSizer.AddControl(
            ctlName = 'TempMode',
            ctlType = 'keybutton',
        )
        tempSizer.AddControl(
            ctlName = 'TempTray',
            ctlType = 'spinbox',
            contents = [1, 8],
        )
        leftColumn.Add(tempSizer, 0, wx.EXPAND)

        ##### SUPER SPEED
        superSpeedSizer = ControlGroup(self, self, 'Super Speed')
        superSpeedSizer.AddControl(
            ctlName = 'RunMode',
            ctlType = 'keybutton',
        )
        superSpeedSizer.AddControl(
            ctlName = 'SSOnlyWhenMoving',
            ctlType = 'checkbox',
        )
        superSpeedSizer.AddControl(
            ctlName = 'SSSJModeEnable',
            ctlType = 'checkbox',
        )
        rightColumn.Add(superSpeedSizer, 0, wx.EXPAND)

        ##### SUPER JUMP
        superJumpSizer = ControlGroup(self, self, 'Super Jump')
        superJumpSizer.AddControl(
            ctlName = 'JumpMode',
            ctlType = 'keybutton',
        )
        superJumpSizer.AddControl(
            ctlName = 'SimpleSJCJ',
            ctlType = 'checkbox',
        )
        rightColumn.Add(superJumpSizer, 0, wx.EXPAND)


        ##### FLY
        flySizer = ControlGroup(self, self, 'Flight')

        flySizer.AddControl(
            ctlName = 'FlyMode',
            ctlType = 'keybutton',
        )
        flySizer.AddControl(
            ctlName = 'GFlyMode',
            ctlType = 'keybutton',
        )
        rightColumn.Add(flySizer, 0, wx.EXPAND)

        ##### TELEPORT
        teleportSizer = ControlGroup(self, self, 'Teleport')

        # if (at == peacebringer) "Dwarf Step"
        # if (at == warshade) "Shadow Step / Dwarf Step"

        teleportSizer.AddControl(
            ctlName = "TPMode",
            ctlType = 'keybutton',
        )
        teleportSizer.AddControl(
            ctlName = "TPCombo",
            ctlType = 'keybutton',
        )
        teleportSizer.AddControl(
            ctlName = "TPReset",
            ctlType = 'keybutton',
        )

        # if (player has hover): {
        teleportSizer.AddControl(
            ctlName = 'TPAutoHover',
            ctlType = 'checkbox',
        )
        #

        # if (player has team-tp) {
        teleportSizer.AddControl(
            ctlName = "TTPMode",
            ctlType = 'keybutton',
        )
        teleportSizer.AddControl(
            ctlName = "TTPCombo",
            ctlType = 'keybutton',
        )
        teleportSizer.AddControl(
            ctlName = "TTPReset",
            ctlType = 'keybutton',
        )

        # if (player has group fly) {
        teleportSizer.AddControl(
            ctlName = 'TTPAutoGFly',
            ctlType = 'checkbox',
        )
        #
        #
        # end team-tp
        rightColumn.Add(teleportSizer, 0, wx.EXPAND)

        ##### KHELDIAN TRAVEL POWERS
        kheldianSizer = ControlGroup(self, self, 'Nova / Dwarf Travel Powers')

        kheldianSizer.AddControl(
            ctlName = 'NovaMode',
            ctlType = 'keybutton',
        )
        kheldianSizer.AddControl(
            ctlName = 'NovaTray',
            ctlType = 'spinbox',
            contents = [1, 8],
        )
        kheldianSizer.AddControl(
            ctlName = 'DwarfMode',
            ctlType = 'keybutton',
        )
        kheldianSizer.AddControl(
            ctlName = 'DwarfTray',
            ctlType = 'spinbox',
            contents = [1, 8],
        )

        # do we want a key to change directly to human form, instead of toggles?
        kheldianSizer.AddControl(
            ctlName = 'HumanMode',
            ctlType = 'keybutton',
        )
        kheldianSizer.AddControl(
            ctlName = 'HumanTray',
            ctlType = 'spinbox',
            contents = [1, 8],
        )

        rightColumn.Add(kheldianSizer, 0, wx.EXPAND)

        topSizer.Add(leftColumn)
        topSizer.Add(rightColumn)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizerAndFit(paddingSizer)

        self.SynchronizeUI()


    def SynchronizeUI(self):
        self.OnEnableSoD()

    def OnEnableSoD(self, evt = None):
        for c,control in self.Ctrls.items():
            if c != 'EnableSoD':  # don't disable yourself kthx
                control         .Enable(self.GetState('EnableSoD'))
                control.ctlLabel.Enable(self.GetState('EnableSoD'))

    def makeSoDFile(self, p):

        profile = self.Profile

        t = p['t']

        bl   = t.bl   or p.get('bl'   , "")
        bla  = t.bla  or p.get('bla'  , "")
        blf  = t.blf  or p.get('blf'  , "")
        blbo = t.blbo or p.get('blbo' , "")
        blsd = t.blsd or p.get('blsd' , "")

        path   = t.path   or p.get('path'   , "")
        patha  = t.patha  or p.get('patha'  , "")
        pathf  = t.pathf  or p.get('pathf'  , "")
        pathbo = t.pathbo or p.get('pathbo' , "")
        pathsd = t.pathsd or p.get('pathsd' , "")

        mobile     = p.get('mobile'     , "")
        stationary = p.get('stationary' , "")
        modestr    = p.get('modestr'    , "")
        flight     = p.get('flight'     , "")
        fix        = p.get('fix'        , "")
        turnoff    = p.get('turnoff'    , "")
        sssj       = p.get('sssj'       , "")

        # TODO -- this wants to be turnoff ||= mobile, stationary once we know what those are.  arrays?  hashes?
        #$turnoff ||= {mobile,stationary}

        if ((self.GetState('Default') == modestr) and (t.totalkeys == 0)):

            curfile = profile.ResetFile()
            self.sodDefaultResetKey(mobile,stationary)

            self.sodUpKey     (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
            self.sodDownKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
            self.sodForwardKey(t,bl,curfile,mobile,stationary,flight,'','','',sssj)
            self.sodBackKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
            self.sodLeftKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
            self.sodRightKey  (t,bl,curfile,mobile,stationary,flight,'','','',sssj)

            if   (modestr == "NonSoD"): self.makeNonSoDModeKey(profile,t,"r", curfile,{mobile,stationary})
            elif (modestr == "Base")  : self.makeBaseModeKey  (profile,t,"r", curfile,turnoff,fix)
            elif (modestr == "Fly")   : self.makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)
            elif (modestr == "GFly")  : self.makeGFlyModeKey  (profile,t,"gf",curfile,turnoff,fix)
            elif (modestr == "Run")   : self.makeSpeedModeKey (profile,t,"s", curfile,turnoff,fix)
            elif (modestr == "Jump")  : self.makeJumpModeKey  (profile,t,"j", curfile,turnoff,path)
            elif (modestr == "Temp")  : self.makeTempModeKey  (profile,t,"r", curfile,turnoff,path)
            elif (modestr == "QFly")  : self.makeQFlyModeKey  (profile,t,"r", curfile,turnoff,modestr)

            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)

            self.sodFollowKey(t,blf,curfile,mobile)

        if (flight and (flight == "Fly") and pathbo):
            #  blast off
            curfile = profile.GetBindFile(pathbo + t.KeyState() + ".txt")
            self.sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

            self.sodUpKey     (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodDownKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodForwardKey(t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodBackKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodLeftKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodRightKey  (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)

            if (modestr == "Base") : self.makeBaseModeKey(profile,t,"r",curfile,turnoff,fix)

            t.ini = '-down$$'

            if (self.GetState('Default') == "Fly"):

                if (self.GetState('NonSoD')):
                    t.FlyMode = t.NonSoDMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                elif (self.GetState('Base')):
                    t.FlyMode = t.BaseMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                elif (t.canss):
                    t.FlyMode = t.RunMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                elif (t.canjmp):
                    t.FlyMode = t.JumpMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                elif (self.GetState('Temp') and self.GetState('TempEnable')):
                    t.FlyMode = t.TempMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                else:
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)

            t.ini = ''
            # if   (modestr == "GFly") : self.makeGFlyModeKey (profile,t,"gbo",curfile,turnoff,fix)
            # elif (modestr == "Run")  : self.makeSpeedModeKey(profile,t,"s",  curfile,turnoff,fix)
            # elif (modestr == "Jump") : self.makeJumpModeKey (profile,t,"j",  curfile,turnoff,path)

            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)

            self.sodFollowKey(t,blf,curfile,mobile)

            # TODO this is commented out in citybinder, why?
            # curfile = profile.GetBindFile(pathsd)

            self.sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

            self.sodUpKey     (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodDownKey   (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodForwardKey(t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodBackKey   (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodLeftKey   (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodRightKey  (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)

            t.ini = '-down$$'
            if   (modestr == "Base") : self.makeBaseModeKey(profile,t,"r",  curfile,turnoff,fix)
            elif (modestr == "Fly")  : self.makeFlyModeKey( profile,t,"a",  curfile,turnoff,fix)
            elif (modestr == "GFly") : self.makeGFlyModeKey(profile,t,"gbo",curfile,turnoff,fix)
            t.ini = ''
            if   (modestr == "Jump") : self.makeJumpModeKey(profile,t,"j",  curfile,turnoff,path)

            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)
            self.sodFollowKey(t,blf,curfile,mobile)

        ### TODO recently added Keystate and .txt to this.  Is this right?
        curfile = profile.GetBindFile(path + t.KeyState() + ".txt")

        self.sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

        self.sodUpKey     (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodDownKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodForwardKey(t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodBackKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodLeftKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodRightKey  (t,bl,curfile,mobile,stationary,flight,'','','',sssj)

        if ((flight == "Fly") and pathbo):
            #  Base to set down
            if   (modestr == "NonSoD"): self.makeNonSoDModeKey(profile,t,"r",curfile,{mobile,stationary},self.sodSetDownFix())
            elif (modestr == "Base")  : self.makeBaseModeKey  (profile,t,"r",curfile,turnoff,self.sodSetDownFix())

            if (t.BaseMode):
                curfile.SetBind(t.BaseMode, "+down$$down 1" + self.actPower_name(None,1,mobile) + t.detailhi + t.runcamdist + t.blsd)

            if   (modestr == "Run")    : self.makeSpeedModeKey (profile,t,"s", curfile,turnoff,self.sodSetDownFix())
            elif (modestr == "Fly")    : self.makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)
            elif (modestr == "Jump")   : self.makeJumpModeKey  (profile,t,"j", curfile,turnoff,path)
            elif (modestr == "Temp")   : self.makeTempModeKey  (profile,t,"r", curfile,turnoff,path)
            elif (modestr == "QFly")   : self.makeQFlyModeKey  (profile,t,"r", curfile,turnoff,modestr)
        else:
            if   (modestr == "NonSoD") : self.makeNonSoDModeKey(profile,t,"r", curfile,{mobile,stationary})
            elif (modestr == "Base")   : self.makeBaseModeKey  (profile,t,"r", curfile,turnoff,fix)
            elif (flight == "Jump"):
                if (modestr == "Fly"): self.makeFlyModeKey   (profile,t,"a", curfile,turnoff,fix,None,1)
            else:
                if (modestr == "Fly"): self.makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)

            if   (modestr == "Run")   : self.makeSpeedModeKey  (profile,t,"s", curfile,turnoff,fix)
            elif (modestr == "Jump")  : self.makeJumpModeKey   (profile,t,"j", curfile,turnoff,path)
            elif (modestr == "Temp")  : self.makeTempModeKey   (profile,t,"r", curfile,turnoff,path)
            elif (modestr == "QFly")  : self.makeQFlyModeKey   (profile,t,"r", curfile,turnoff,modestr)

        self.sodAutoRunKey(t,bla,curfile,mobile,sssj)
        self.sodFollowKey(t,blf,curfile,mobile)

        # AutoRun Binds
        curfile = profile.GetBindFile(patha + t.KeyState() + ".txt")

        self.sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

        self.sodUpKey     (t,bla,curfile,mobile,stationary,flight,1,'','',sssj)
        self.sodDownKey   (t,bla,curfile,mobile,stationary,flight,1,'','',sssj)
        self.sodForwardKey(t,bla,curfile,mobile,stationary,flight,bl, '','',sssj)
        self.sodBackKey   (t,bla,curfile,mobile,stationary,flight,bl, '','',sssj)
        self.sodLeftKey   (t,bla,curfile,mobile,stationary,flight,1,'','',sssj)
        self.sodRightKey  (t,bla,curfile,mobile,stationary,flight,1,'','',sssj)

        if ((flight == "Fly") and pathbo):
            if   (modestr == "NonSoD"): self.makeNonSoDModeKey(profile,t,"ar",curfile,{mobile,stationary},self.sodSetDownFix())
            elif (modestr == "Base")  : self.makeBaseModeKey  (profile,t,"gr",curfile,turnoff,self.sodSetDownFix())
            elif (modestr == "Run")   : self.makeSpeedModeKey (profile,t,"as",curfile,turnoff,self.sodSetDownFix())
        else:
            if   (modestr == "NonSoD"): self.makeNonSoDModeKey(profile,t,"ar",curfile,{mobile,stationary})
            elif (modestr == "Base")  : self.makeBaseModeKey  (profile,t,"gr",curfile,turnoff,fix)
            elif (modestr == "Run")   : self.makeSpeedModeKey (profile,t,"as",curfile,turnoff,fix)

        if   (modestr == "Fly")       : self.makeFlyModeKey   (profile,t,"af",curfile,turnoff,fix)
        elif (modestr == "Jump")      : self.makeJumpModeKey  (profile,t,"aj",curfile,turnoff,patha)
        elif (modestr == "Temp")      : self.makeTempModeKey  (profile,t,"ar",curfile,turnoff,path)
        elif (modestr == "QFly")      : self.makeQFlyModeKey  (profile,t,"ar",curfile,turnoff,modestr)

        self.sodAutoRunOffKey(t,bl,curfile,mobile,stationary,flight,sssj)

        curfile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind('nop'))

        # FollowRun Binds
        curfile = profile.GetBindFile(pathf + t.KeyState() + ".txt")

        self.sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

        self.sodUpKey     (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodDownKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodForwardKey(t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodBackKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodLeftKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodRightKey  (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)

        if ((flight == "Fly") and pathbo):
            if   (modestr == "NonSoD"): self.makeNonSoDModeKey(profile,t,"fr",curfile,{mobile,stationary},self.sodSetDownFix())
            elif (modestr == "Base")  : self.makeBaseModeKey  (profile,t,"fr",curfile,turnoff,self.sodSetDownFix())
            elif (modestr == "Run")   : self.makeSpeedModeKey (profile,t,"fs",curfile,turnoff,self.sodSetDownFix())
        else:
            if   (modestr == "NonSoD"): self.makeNonSoDModeKey(profile,t,"fr",curfile,{mobile,stationary})
            elif (modestr == "Base")  : self.makeBaseModeKey  (profile,t,"fr",curfile,turnoff,fix)
            elif (modestr == "Run")   : self.makeSpeedModeKey (profile,t,"fs",curfile,turnoff,fix)

        if   (modestr == "Fly")       : self.makeFlyModeKey   (profile,t,"ff",curfile,turnoff,fix)
        elif (modestr == "Jump")      : self.makeJumpModeKey  (profile,t,"fj",curfile,turnoff,pathf)
        elif (modestr == "Temp")      : self.makeTempModeKey  (profile,t,"fr",curfile,turnoff,path)
        elif (modestr == "QFly")      : self.makeQFlyModeKey  (profile,t,"fr",curfile,turnoff,modestr)

        curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind('nop'))

        self.sodFollowOffKey(t,bl,curfile,mobile,stationary,flight)



    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeNonSoDModeKey(self, p, t, bl, cur, toff, fix, fb):
        key = t.NonSoDMode
        if not key: return

        if self.GetState('Feedback'): feedback = (fb or '$$t $name, Non-SoD Mode')
        else:                         feedback = ''

        if t.ini == None: t.ini = ''

        if (bl == "r"):
            bindload = t.BLF('n')
            if (fix):
                fix(p,t,key, self.makeNonSoDModeKey,"n",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(None,1,None,toff) + t + dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload = t.BLF('an')
            if (fix):
                fix(p,t,key, self.makeNonSoDModeKey,"n",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(None,1,None,toff) + t.detailhi + t.runcamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, self.makeNonSoDModeKey,"n",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(None,1,None,toff) + t.detailhi + t.runcamdist + '$$up 0' + feedback + t.BLF('fn'))
        t.ini = ''

    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeTempModeKey(self, p, t, bl, cur, toff):
        key = t.TempMode
        if not key: return

        if self.GetState('Feedback'): feedback = '$$t $name, Temp Mode'
        else:                         feedback = ''

        trayslot = f"1 {self.GetState('TempTray')}"

        if (bl == "r"):
            bindload = t.BLF('t')
            cur.SetBind(key, t.ini + self.actPower(None,1,trayslot,toff) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload)
        elif (bl == "ar"):
            bindload  = t.BLF('at')
            bindload2 = t.BLF('at','_t')
            tgl = p.GetBindFile(bindload2)
            cur.SetBind(key, t.ini + self.actPower(None,1,trayslot,toff) + t.detaillo + t.flycamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload2)
            tgl.SetBind(key, t.ini + self.actPower(None,1,trayslot,toff) + t.detaillo + t.flycamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)
        else:
            cur.SetBind(key, t.ini + self.actPower(None,1,trayslot,toff) + t.detaillo + t.flycamdist + '$$up 0' + feedback + t.BLF('ft'))

        t.ini = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeQFlyModeKey(self, p, t, bl, cur, toff, modestr):
        key = t.QFlyMode
        if not key: return

        if (modestr == "NonSoD"):
            cur.SetBind(key, "powexecname Quantum Flight")
            return

        if self.GetState('Feedback'): feedback = '$$t $name, QFlight Mode'
        else:                         feedback = ''

        if not t.ini: t.ini = ''

        if (bl == "r"):
            bindload  = t.BLF('n')
            bindload2 = t.BLF('n'+'_q')
            tgl = p.GetBindFile(bindload2)

            if (modestr == 'Nova' or modestr == 'Dwarf'): tray = '$$gototray 1'
            else:                                         tray = ''

            cur.SetBind(key, t.ini + self.actPower(None,1,'Quantum Flight', toff) + tray + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload2)
            tgl.SetBind(key, t.ini + self.actPower(None,1,'Quantum Flight', toff) + tray + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t.BLF('an')
            bindload2 = t.BLF('an','_t')
            tgl = p.GetBindFile(bindload2)
            cur.SetBind(key, t.ini + self.actPower(None,1,'Quantum Flight', toff) + t.detaillo + t.flycamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload2)
            tgl.SetBind(key, t.ini + self.actPower(None,1,'Quantum Flight', toff) + t.detaillo + t.flycamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)
        else:
            cur.SetBind(key, t.ini + self.actPower(None,1,'Quantum Flight', toff) + t.detaillo + t.flycamdist + '$$up 0' + feedback + t.BLF('fn'))

        t.ini = ''

    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeBaseModeKey(self, p, t, bl, cur, toff, fix, fb):
        key = t.BaseMode
        if not key: return

        if self.GetState('Feedback'): feedback = (fb or '$$t $name, Sprint-SoD Mode')
        else:                         feedback = ''

        if not t.ini: t.ini = ''

        if (bl == "r"):
            bindload  = t.BLF()

            if t.horizkeys: sprint = t.sprint
            else:              sprint = ''
            ton = self.actPower_toggle(1, 1, sprint, toff)

            if (fix):
                fix(p,t,key, self.makeBaseModeKey,"r",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, t.ini + ton + t.dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t.BLF('gr')

            if (fix):
                fix(p,t,key, self.makeBaseModeKey,"r",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(1,1,t.sprint,toff) + t.detailhi +  t.runcamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, self.makeBaseModeKey,"r",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(1,1,t.sprint, toff) + t.detailhi + t.runcamdist + '$$up 0' + fb + t.BLF('fr'))

        t.ini = ''

    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeSpeedModeKey(self, p, t, bl, cur, toff, fix, fb = ''):
        key = t.RunMode

        bindload = feedback = ''

        if p.SoD.GetState('Feedback'): feedback = (fb or '$$t $name, Superspeed Mode')

        if not t.get('ini', ''): t.ini = ''

        if (t.canss):
            if (bl == 's'):
                bindload = f"{t.bls}{t.space}{t.X}{t.W}{t.S}{t.A}{t.D}.txt"
                if (fix):
                    fix(p,t,key,self.makeSpeedModeKey,"s",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,1,t.speed,toff) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload))

            elif (bl == "as"):
                bindload = f"{t.blas}{t.space}{t.X}{t.W}{t.S}{t.A}{t.D}.txt"
                if (fix):
                    fix(p,t,key,self.makeSpeedModeKey,"s",bl,cur,toff,"a",feedback)
                elif (not feedback):
                    cur.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,1,t.speed,toff) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload))
                else:
                    bindload  = f"{t.pathas}{t.space}{t.X}{t.W}{t.S}{t.A}{t.D}.txt"
                    bindload2 = f"{t.pathas}{t.space}{t.X}{t.W}{t.S}{t.A}{t.D}_s.txt"
                    tgl = p.GetBindFile(bindload2)
                    cur.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,1,t.speed,toff) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload2))
                    tgl.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,1,t.speed,toff) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload))

            else:
                if (fix):
                    fix(p,t,key,self.makeSpeedModeKey,"s",bl,cur,toff,"f",feedback)
                else:
                    cur.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,1,t.speed,toff) + '$$up 0' +  t.detaillo + t.flycamdist + feedback + t.blfs))

        t.ini = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeJumpModeKey(self, p, t, bl, cur, toff, fbl):
        key = t.JumpMode
        if (t.canjmp and not self.GetState('JumpSimple')):

            if self.GetState('Feedback'): feedback = '$$t $name, Superjump Mode'
            else:                         feedback = ''
            tgl = p.GetBindFile(fbl)

            if (bl == "j"):
                if (t.horizkeys + t.space > 0):
                    a = self.actPower(None,1,t.jump,toff) + '$$up 1'
                else:
                    a = self.actPower(None,1,t.cjmp,toff)

                bindload = t.BLF('j')
                tgl.SetBind(key, '-down' + a + t.detaillo + t.flycamdist + bindload)
                cur.SetBind(key, '+down' + feedback + p.BLF(fbl))
            elif (bl == "aj"):
                bindload = t.BLF('aj')
                tgl.SetBind(key, '-down' + self.actPower(None,1,t.jump,toff) + '$$up 1' + t.detaillo + t.flycamdist + t.dirs('DLR') + bindload)
                cur.SetBind(key, '+down' + feedback + p.BLF(fbl))
            else:
                tgl.SetBind(key, '-down' + self.actPower(None,1,t.jump,toff) + '$$up 1' + t.detaillo + t.flycamdist + t.BLF('fj'))
                cur.SetBind(key, '+down' + feedback + p.BLF(fbl))


        t.ini = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeFlyModeKey(self, p, t, bl, cur, toff, fix, fb, fb_on_a):
        key = t.FlyMode
        if not key: return

        if self.GetState('Feedback'): feedback = (fb or '$$t $name, Flight Mode')
        else:                         feedback = ''

        if not t.ini: t.ini = ''

        if (t.canhov + t.canfly > 0):
            if (bl == "bo"):
                bindload = t.BLF('bo')
                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(key, '+down$$' + self.actPower_toggle(1,1,t.flyx,toff) + '$$up 1$$down 0' + t.dirs('FBLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "a"):
                if (not fb_on_a): feedback = ''
                bindload = t.BLF('a')

                if t.tkeys: ton = t.flyx
                else:          ton = t.hover

                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(t.FlyMode,  t.ini + self.actPower_toggle(1,1, ton ,toff) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "af"):
                bindload = t.BLF('af')
                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,"a",feedback)
                else:
                    cur.SetBind(key,  t.ini + self.actPower_toggle(1,1,t.flyx,toff) + t.detaillo + t.flycamdist + t.dirs('DLR') + feedback + bindload)

            else:
                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,"f",feedback)
                else:
                    cur.SetBind(key,  t.ini + self.actPower_toggle(1,1,t.flyx,toff) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + t.BLF('ff'))

        t.ini = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeGFlyModeKey(self, p, t, bl, cur, toff, fix):
        key = t.GFlyMode

        if not t.ini: t.ini = ''

        if (t.cangfly > 0):
            if (bl == "gbo"):
                bindload = t.BLF('gbo')
                if (fix):
                    fix(p,t,key,self.makeGFlyModeKey,"gf",bl,cur,toff,'','')
                else:
                    cur.SetBind(key, t.ini + '$$up 1$$down 0' + self.actPower_toggle(None,1,t.gfly,toff) + t.dirs('FBLR') + t.detaillo + t.flycamdist .bindload)

            elif (bl == "gaf"):
                bindload = t.BLF('gaf')
                if (fix):
                    fix(p,t,key,self.makeGFlyModeKey,"gf",bl,cur,toff,"a")
                else:
                    cur.SetBind(key, t.ini + t.detaillo + t.flycamdist + t.dirs('UDLR') + bindload)

            else:
                if (fix):
                    fix(p,t,key,self.makeGFlyModeKey,"gf",bl,cur,toff,"f")
                else:
                    if (bl == "gf"):
                        cur.SetBind(key, t.ini + self.actPower_toggle(1,1,t.gfly,toff) + t.detaillo + t.flycamdist + t.BLF('gff'))
                    else:
                        cur.SetBind(key, t.ini + t.detaillo + t.flycamdist + t.BLF('gff'))

        t.ini = ''


    def PopulateBindFiles(self):

        if not self.GetState('EnableSoD'): return

        ### TODO
        sssj = 0
        ### TODO

        profile = self.Profile

        ResetFile = profile.ResetFile()

        # ResetFile.SetBind(petselect.sel5 + ' "petselect 5')
        if (self.GetState('Default') == "NonSoD"):
            if (not self.GetState('NonSoD')):
                wx.Error("Notice","Enabling NonSoD mode, since it is set as your default mode.")
            self.SetState('NonSoD', 1)

        if (self.GetState('Default') == "Base" and not self.GetState('Base')):
            wx.Error("Notice","Enabling NonSoD mode and making it the default, since Sprint SoD, your previous Default mode, is not enabled.")
            self.SetState('NonSoD', 1)
            self.SetState('Default', "NonSoD")

        if (self.GetState('Default') == "Fly" and not (self.GetState('FlyHover') or self.GetState('FlyFly'))):
            wx.Error("Notice","Enabling NonSoD mode and making it the default, since Flight SoD, your previous Default mode, is not enabled.")
            self.SetState('NonSoD', 1)
            self.SetState('Default', "NonSoD")

        if (self.GetState('Default') == "Jump" and not (self.GetState('JumpCJ') or self.GetState('JumpSJ'))):
            wx.Error("Notice","Enabling NonSoD mode and making it the default, since Superjump SoD, your previous Default mode, is not enabled.")
            self.SetState('NonSoD', 1)
            self.SetState('Default', "NonSoD")

        if (self.GetState('Default') == "Run" and self.GetState('RunPrimaryNumber') == 1):
            wx.Error("Notice","Enabling NonSoD mode and making it the default, since Superspeed SoD, your previous Default mode, is not enabled.")
            self.SetState('NonSoD', 1)
            self.SetState('Default', "NonSoD")


        t = tObject(profile)

        ## Combat Jumping / Super Jump
        if (self.GetState('JumpCJ') and not self.GetState('JumpSJ')):
            t.cancj = 1
            t.cjmp = "Combat Jumping"
            t.jump = "Combat Jumping"

        elif (not self.GetState('JumpCJ') and self.GetState('JumpSJ')):
            t.canjmp = 1
            t.jump = "Super Jump"
            t.jumpifnocj = "Super Jump"

        else:
            t.cancj = 1
            t.canjmp = 1
            t.cjmp = "Combat Jumping"
            t.jump = "Super Jump"

        ## Flying / hover
        if (profile.General.GetState('Archetype') == "Peacebringer"):
            if (self.GetState('FlyHover')):
                t.canhov = 1
                t.canfly = 1
                t.hover = "Combat Flight"
                t.fly = "Energy Flight"
                t.flyx = "Energy Flight"
            else:
                t.canfly = 1
                t.hover = "Energy Flight"
                t.flyx = "Energy Flight"

        elif (not (profile.General.GetState('Archetype') == "Warshade")):
            if (self.GetState('FlyHover') and not self.GetState('FlyFly')):
                t.canhov = 1
                t.hover = "Hover"
                t.flyx = "Hover"
                if (self.GetState('TPTPHover')): t.tphover = '$$powexectoggleon Hover'
            elif (not self.GetState('FlyHover') and self.GetState('FlyFly')):
                t.canfly = 1
                t.hover = "Fly"
                t.flyx = "Fly"
            elif (self.GetState('FlyHover') and self.GetState('FlyFly')):
                t.canhov = 1
                t.canfly = 1
                t.hover = "Hover"
                t.fly = "Fly"
                t.flyx = "Fly"
                if (self.GetState('TPTPHover')): t.tphover = '$$powexectoggleon Hover'

        if ((profile.General.GetState('Archetype') == "Peacebringer") and self.GetState('FlyQFly')):
            t.canqfly = 1

        # if (self.GetState('FlyGFly')):
        #     t.cangfly = 1
        #     t.gfly = "Group Fly"
        #     if (self.GetState('TTPTPGFly')): t.ttpgfly = '$$powexectoggleon Group Fly'

        if (self.GetState('RunPrimaryNumber') == 1):
            t.sprint = self.GetState('RunSecondary')
            t.speed  = self.GetState('RunSecondary')
        else:
            t.sprint = self.GetState('RunSecondary')
            t.speed  = self.GetState('RunPrimary')
            t.canss = 1

        if (self.GetState('AutoMouseLook')):
            t.mlon  = '$$mouselook 1'
            t.mloff = '$$mouselook 0'

        if (self.GetState('RunUseCamdist')):
            t.runcamdist = '$$camdist ' + self.GetState('RunCamdist')

        if (self.GetState('FlyUseCamdist')):
            t.flycamdist = '$$camdist ' + self.GetState('FlyCamdist')

        if (self.GetState('Detail') and self.GetState('DetailEnable')):
            t.detailhi = '$$visscale ' + self.GetState('DetailNormalAmt') + '$$shadowvol 0$$ss 0'
            t.detaillo = '$$visscale ' + self.GetState('DetailMovingAmt') + '$$shadowvol 0$$ss 0'

        if self.GetState('TPHideWindows'):
            windowhide = '$$windowhide health$$windowhide chat$$windowhide target$$windowhide tray'
            windowshow = '$$show health$$show chat$$show target$$show tray'
        else:
            windowhide = ''
            windowshow = ''


        t.basepath     = profile.BindsDir()
        t.gamebasepath = profile.GameBindsDir()

        t.path     = str(Path(t.basepath) / 'R' / 'R')
        t.gamepath = str(PureWindowsPath(t.gamebasepath) / 'R' / 'R')
        t.bl       = f"$$bindloadfile {t.gamepath}"

        t.patha     = str(Path(t.basepath) / 'F' / 'F') # air subfolder and base filename
        t.gamepatha = str(PureWindowsPath(t.basepath) / 'F' / 'F') # air subfolder and base filename
        t.bla       = f"$$bindloadfile {t.gamepatha}"

        t.pathj     = str(Path(t.basepath) / 'J' / 'J')
        t.gamepathj = str(PureWindowsPath(t.basepath) / 'J' / 'J')
        t.blj       = f"$$bindloadfile {t.gamepathj}"

        t.paths     = str(Path(t.basepath) / 'S' / 'S')
        t.gamepaths = str(PureWindowsPath(t.basepath) / 'S' / 'S')
        t.bls       = f"$$bindloadfile {t.gamepaths}"

        #t.pathga     = str(Path(t.basepath) / 'GF' / 'GF') # air subfolder and base filename
        #t.gamepathga = str(PureWindowsPath(t.basepath) / 'GF' / 'GF') # air subfolder and base filename
        #t.blga       = f"$$bindloadfile {t.gamepathga}"

        t.pathn     = str(Path(t.basepath) / 'N' / 'N') # ground subfolder and base filename.
        t.gamepathn = str(PureWindowsPath(t.basepath) / 'N' / 'N') # ground subfolder and base filename.
        t.bln       = f"$$bindloadfile {t.gamepathn}"

        t.patht     = str(Path(t.basepath) / 'T' / 'T') # ground subfolder and base filename.
        t.gamepatht = str(PureWindowsPath(t.basepath) / 'T' / 'T') # ground subfolder and base filename.
        t.blt       = f"$$bindloadfile {t.gamepatht}"

        t.pathq     = str(Path(t.basepath) / 'Q' / 'Q') # ground subfolder and base filename.
        t.gamepathq = str(PureWindowsPath(t.basepath) / 'Q' / 'Q') # ground subfolder and base filename.
        t.blq       = f"$$bindloadfile {t.gamepathq}"

        t.pathgr     = str(Path(t.basepath) / 'AR' / 'AR')  # ground autorun subfolder and base filename
        t.gamepathgr = str(PureWindowsPath(t.basepath) / 'AR' / 'AR')  # ground autorun subfolder and base filename
        t.blgr       = f"$$bindloadfile {t.gamepathgr}"

        t.pathaf     = str(Path(t.basepath) / 'AF' / 'AF')  # air autorun subfolder and base filename
        t.gamepathaf = str(PureWindowsPath(t.basepath) / 'AF' / 'AF')  # air autorun subfolder and base filename
        t.blaf       = f"$$bindloadfile {t.gamepathaf}"

        t.pathaj     = str(Path(t.basepath) / 'AJ' / 'AJ')
        t.gamepathaj = str(PureWindowsPath(t.basepath) / 'AJ' / 'AJ')
        t.blaj       = f"$$bindloadfile {t.gamepathaj}"

        t.pathas     = str(Path(t.basepath) / 'AS' / 'AS')
        t.gamepathas = str(PureWindowsPath(t.basepath) / 'AS' / 'AS')
        t.blas       = f"$$bindloadfile {t.gamepathas}"

        #t.pathgaf     = str(Path(t.basepath) / 'GAF' / 'GAF')  # air autorun subfolder and base filename
        #t.gamepathgaf = str(PureWindowsPath(t.basepath) / 'GAF' / 'GAF')  # air autorun subfolder and base filename
        #t.blgaf       = f"$$bindloadfile {t.gamepathgaf}"

        t.pathan     = str(Path(t.basepath) / 'AN' / 'AN') # ground subfolder and base filename.
        t.gamepathan = str(PureWindowsPath(t.basepath) / 'AN' / 'AN') # ground subfolder and base filename.
        t.blan       = f"$$bindloadfile {t.gamepathan}"

        t.pathat     = str(Path(t.basepath) / 'AT' / 'AT') # ground subfolder and base filename.
        t.gamepathat = str(PureWindowsPath(t.basepath) / 'AT' / 'AT') # ground subfolder and base filename.
        t.blat       = f"$$bindloadfile {t.gamepathat}"

        t.pathaq     = str(Path(t.basepath) / 'AQ' / 'AQ') # ground subfolder and base filename.
        t.gamepathaq = str(PureWindowsPath(t.basepath) / 'AQ' / 'AQ') # ground subfolder and base filename.
        t.blaq       = f"$$bindloadfile {t.gamepathaq}"

        t.pathfr     = str(Path(t.basepath) / 'FR' / 'FR')  # Follow Run subfolder and base filename
        t.gamepathfr = str(PureWindowsPath(t.basepath) / 'FR' / 'FR')  # Follow Run subfolder and base filename
        t.blfr       = f"$$bindloadfile {t.gamepathfr}"

        t.pathff     = str(Path(t.basepath) / 'FF' / 'FF')  # Follow Fly subfolder and base filename
        t.gamepathff = str(PureWindowsPath(t.basepath) / 'FF' / 'FF')  # Follow Fly subfolder and base filename
        t.blff       = f"$$bindloadfile {t.gamepathff}"

        t.pathfj     = str(Path(t.basepath) / 'FJ' / 'FJ')
        t.gamepathfj = str(PureWindowsPath(t.basepath) / 'FJ' / 'FJ')
        t.blfj       = f"$$bindloadfile {t.gamepathfj}"

        t.pathfs     = str(Path(t.basepath) / 'FS' / 'FS')
        t.gamepathfs = str(PureWindowsPath(t.basepath) / 'FS' / 'FS')
        t.blfs       = f"$$bindloadfile {t.gamepathfs}"

        #t.pathgff     = str(Path(t.basepath) / 'GFF' / 'GFF')  # Follow Fly subfolder and base filename
        #t.gamepathgff = str(PureWindowsPath(t.basepath) / 'GFF' / 'GFF')  # Follow Fly subfolder and base filename
        #t.blgff       = f"$$bindloadfile {t.gamepathgff}"

        t.pathfn     = str(Path(t.basepath) / 'FN' / 'FN') # ground subfolder and base filename.
        t.gamepathfn = str(PureWindowsPath(t.basepath) / 'FN' / 'FN') # ground subfolder and base filename.
        t.blfn       = f"$$bindloadfile {t.gamepathfn}"

        t.pathft     = str(Path(t.basepath) / 'FT' / 'FT') # ground subfolder and base filename.
        t.gamepathft = str(PureWindowsPath(t.basepath) / 'FT' / 'FT') # ground subfolder and base filename.
        t.blft       = f"$$bindloadfile {t.gamepathat}"

        t.pathfq     = str(Path(t.basepath) / 'FQ' / 'FQ') # ground subfolder and base filename.
        t.gamepathfq = str(PureWindowsPath(t.basepath) / 'FQ' / 'FQ') # ground subfolder and base filename.
        t.blfq       = f"$$bindloadfile {t.gamepathfq}"

        t.pathbo     = str(Path(t.basepath) / 'BO' / 'BO')  # Blastoff Fly subfolder and base filename
        t.gamepathbo = str(PureWindowsPath(t.basepath) / 'BO' / 'BO')  # Blastoff Fly subfolder and base filename
        t.blbo       = f"$$bindloadfile {t.gamepathbo}"

        t.pathsd     = str(Path(t.basepath) / 'SD' / 'SD')  #  SetDown Fly Subfolder and base filename
        t.gamepathsd = str(PureWindowsPath(t.basepath) / 'SD' / 'SD')  #  SetDown Fly Subfolder and base filename
        t.blsd       = f"$$bindloadfile {t.gamepathsd}"

        #t.pathgbo     = str(Path(t.basepath) / 'GBO' / 'GBO')  # Blastoff Fly subfolder and base filename
        #t.gamepathgbo = str(PureWindowsPath(t.basepath) / 'GBO' / 'GBO')  # Blastoff Fly subfolder and base filename
        #t.blgbo       = f"$$bindloadfile {t.gamepathgbo}"

        #t.pathgsd     = str(Path(t.basepath) / 'GSD' / 'GSD')  #  SetDown Fly Subfolder and base filename
        #t.gamepathgsd = str(PureWindowsPath(t.basepath) / 'GSD' / 'GSD')  #  SetDown Fly Subfolder and base filename
        #t.blgsd       = f"$$bindloadfile {t.gamepathgsd}"

        #  temporarily set self.GetState('Default') to "NonSoD"
        # self.SetState('Default', "Base")
        #  set up the keys to be used.
        if (self.GetState('Default') == "NonSoD") : t.NonSoDMode = self.GetState('NonSoDMode')
        if (self.GetState('Default') == "Base")   : t.BaseMode   = self.GetState('BaseMode')
        if (self.GetState('Default') == "Fly")    : t.FlyMode    = self.GetState('FlyMode')
        if (self.GetState('Default') == "Jump")   : t.JumpMode   = self.GetState('JumpMode')
        if (self.GetState('Default') == "Run")    : t.RunMode    = self.GetState('RunMode')
    #    if (self.GetState('Default') == "GFly")   : t.GFlyMode   = self.GetState('GFlyMode')
        t.TempMode = self.GetState('TempMode')
        t.QFlyMode = self.GetState('QFlyMode')

        for space in (0,1):
            t.space = space
            t.up  = f'$$up {space}'
            t.upx = f'$$up {1-space}'

            for X in (0,1):
                t.X = X
                t.dow  = f'$$down {X}'
                t.dowx = f'$$down {1-X}'

                for W in (0,1):
                    t.W = W
                    t.forw = f'$$forward {W}'
                    t.forx = f'$$forward {1-W}'

                    for S in (0,1):
                        t.S = S
                        t.bac  = f'$$backward {S}'
                        t.bacx = f'$$backward {1-S}'

                        for A in (0,1):
                            t.A = A
                            t.lef  = f'$$left {A}'
                            t.lefx = f'$$left {1-A}'

                            for D in (0,1):
                                t.D = D
                                t.rig  = f'$$right {D}'
                                t.rigx = f'$$right {1-D}'

                                t.totalkeys = space+X+W+S+A+D;    # total number of keys down
                                t.horizkeys = W+S+A+D;    # total # of horizontal move keys.    So Sprint isn't turned on when jumping
                                t.vertkeys  = space+X
                                t.jkeys     = t.horizkeys+t.space
                                if (self.GetState('NonSoD') or t.canqfly):
                                    setattr(t, self.GetState('Default') + "Mode", t.NonSoDMode)
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 'n',
                                        'bla' : 'an',
                                        'blf' : 'fn',
                                        'path' : 'n',
                                        'patha' : 'an',
                                        'pathf' : 'fn',
                                        'mobile' : '',
                                        'stationary' : '',
                                        'modestr' : "NonSoD",
                                    })
                                    setattr(t, self.GetState('Default') + "Mode", None)

                                if (self.GetState('Base')):
                                    setattr(t, self.GetState('Default') + "Mode", t.BaseMode)
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : 'r',
                                        'bla'        : 'gr',
                                        'blf'        : 'fr',
                                        'path'       : 'r',
                                        'patha'      : 'ar',
                                        'pathf'      : 'fr',
                                        'mobile'     : t.sprint,
                                        'stationary' : '',
                                        'modestr'    : "Base",
                                    })
                                    setattr(t, self.GetState('Default') + "Mode", None)

                                if (t.canss):
                                    setattr(t, self.GetState('Default') + "Mode", t.RunMode)
                                    if (self.GetState('SSSSSJModeEnable')): sssj = t.jump
                                    if (self.GetState('SSMobileOnly')):
                                        self.makeSoDFile({
                                            't'          : t,
                                            'bl'         : 's',
                                            'bla'        : 'as',
                                            'blf'        : 'fs',
                                            'path'       : 's',
                                            'patha'      : 'as',
                                            'pathf'      : 'fs',
                                            'mobile'     : t.speed,
                                            'stationary' : '',
                                            'modestr'    : "Run",
                                            'sssj'       : sssj,
                                        })
                                    else:
                                        self.makeSoDFile({
                                            't'          : t,
                                            'bl'         : 's',
                                            'bla'        : 'as',
                                            'blf'        : 'fs',
                                            'path'       : 's',
                                            'patha'      : 'as',
                                            'pathf'      : 'fs',
                                            'mobile'     : t.speed,
                                            'stationary' : t.speed,
                                            'modestr'    : "Run",
                                            'sssj'       : sssj,
                                        })

                                    setattr(t, self.GetState('Default') + "Mode", None)

                                if (t.canjmp>0 and not (self.GetState('JumpSimple'))):
                                    jturnoff = ''
                                    setattr(t, self.GetState('Default') + "Mode", t.JumpMode)
                                    if (t.jump == t.cjmp):
                                        jturnoff = t.jumpifnocj
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : 'j',
                                        'bla'        : 'aj',
                                        'blf'        : 'fj',
                                        'path'       : 'j',
                                        'patha'      : 'aj',
                                        'pathf'      : 'fj',
                                        'mobile'     : t.jump,
                                        'stationary' : t.cjmp,
                                        'modestr'    : "Jump",
                                        'flight'     : "Jump",
                                        'fix'        : self.sodJumpFix,
                                        'turnoff'    : jturnoff,
                                    })
                                    setattr(t, self.GetState('Default') + "Mode", None)

                                if (t.canhov+t.canfly>0):
                                    setattr(t, self.GetState('Default') + "Mode", t.FlyMode)
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 'r',
                                        'bla' : 'af',
                                        'blf' : 'ff',
                                        'path' : 'r',
                                        'patha' : 'af',
                                        'pathf' : 'ff',
                                        'mobile' : t.flyx,
                                        'stationary' : t.hover,
                                        'modestr' : "Fly",
                                        'flight' : "Fly",
                                        'pathbo' : 'bo',
                                        'pathsd' : 'sd',
                                        'blbo' : 'bo',
                                        'blsd' : 'sd',
                                    })
                                    setattr(t, self.GetState('Default') + "Mode", None)

                                if (t.canqfly>0):
                                    setattr(t, self.GetState('Default') + "Mode", t.QFlyMode)
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 'q',
                                        'bla' : 'aq',
                                        'blf' : 'fq',
                                        'path' : 'q',
                                        'patha' : 'aq',
                                        'pathf' : 'fq',
                                        'mobile' : "Quantum Flight",
                                        'stationary' : "Quantum Flight",
                                        'modestr' : "QFly",
                                        'flight' : "Fly",
                                    })
                                    setattr(t, self.GetState('Default') + "Mode", None)

                                # if (t.cangfly):
                                #     setattr(t, self.GetState('Default') + "Mode", t.GFlyMode)
                                #     self.makeSoDFile({
                                #         't' : t,
                                #         'bl' : 'a',
                                #         'bla' : 'af',
                                #         'blf' : 'ff',
                                #         'path' : 'ga',
                                #         'patha' : 'gaf',
                                #         'pathf' : 'gff',
                                #         'mobile' : t.gfly,
                                #         'stationary' : t.gfly,
                                #         'modestr' : "GFly",
                                #         'flight' : "GFly",
                                #         'pathbo' : 'gbo',
                                #         'pathsd' : 'gsd',
                                #         'blbo' : 'gbo',
                                #         'blsd' : 'gsd',
                                #     })
                                #     setattr(t, self.GetState('Default') + "Mode", None)

                                if (self.GetState('Temp') and self.GetState('TempEnable')):
                                    trayslot = "1 " + self.GetState('TempTray')
                                    setattr(t, self.GetState('Default') + "Mode", t.TempMode)
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 't',
                                        'bla' : 'at',
                                        'blf' : 'ft',
                                        'path' : 't',
                                        'patha' : 'at',
                                        'pathf' : 'ft',
                                        'mobile' : trayslot,
                                        'stationary' : trayslot,
                                        'modestr' : "Temp",
                                        'flight' : "Fly",
                                    })
                                    setattr(t, self.GetState('Default') + "Mode", None)


        t.space = t.X = t.W = t.S = t.A = t.D = 0

        t.up   = '$$up '       + str(   t.space)
        t.upx  = '$$up '       + str((1-t.space))
        t.dow  = '$$down '     + str(   t.X)
        t.dowx = '$$down '     + str((1-t.X))
        t.forw = '$$forward '  + str(   t.W)
        t.forx = '$$forward '  + str((1-t.W))
        t.bac  = '$$backward ' + str(   t.S)
        t.bacx = '$$backward ' + str((1-t.S))
        t.lef  = '$$left '     + str(   t.A)
        t.lefx = '$$left '     + str((1-t.A))
        t.rig  = '$$right '    + str(   t.D)
        t.rigx = '$$right '    + str((1-t.D))

        if (self.GetState('TLeft')):
            ResetFile.SetBind(self.Ctrls['TLeft'].MakeFileKeyBind("+turnleft"))
        if (self.GetState('TRight')):
            ResetFile.SetBind(self.Ctrls['TRight'].MakeFileKeyBind("+turnright"))

        if (self.GetState('Temp') and self.GetState('TempEnable')):
            temptogglefile1 = profile.GetBindFile("temptoggle1.txt")
            temptogglefile2 = profile.GetBindFile("temptoggle2.txt")
            temptogglefile2.SetBind(self.Ctrls['TempTraySwitch'].MakeFileKeyBind('-down$$gototray 1' + profile.BLF('temptoggle1.txt')))
            temptogglefile1.SetBind(self.Ctrls['TempTraySwitch'].MakeFileKeyBind('+down$$gototray ' + self.GetState('TempTray') + profile.BLF('temptoggle2.txt')))
            ResetFile.SetBind(self.Ctrls['TempTraySwitch'].MakeFileKeyBind('+down$$gototray ' + self.GetState('TempTray') + profile.BLF('temptoggle2.txt')))


        if (profile.General.GetState('Archetype') == "Warshade"):
            dwarfTPPower  = "powexecname Black Dwarf Step"
            normalTPPower = "powexecname Shadow Step"
        elif (profile.General.GetState('Archetype') == "Peacebringer"):
            dwarfTPPower = "powexecname White Dwarf Step"
        else:
            normalTPPower = "powexecname Teleport"
            teamTPPower   = "powexecname Team Teleport"

        if (self.GetState('Human') and self.GetState('HumanEnable')):
            humanBindKey = self.GetState('HumanMode')
            humanpbind = cbPBindToString(self.GetState('HumanHumanPBind'),profile)
            novapbind  = cbPBindToString(self.GetState('HumanNovaPBind'), profile)
            dwarfpbind = cbPBindToString(self.GetState('HumanDwarfPBind'),profile)

        if ((profile.General.GetState('Archetype') == "Peacebringer") or (profile.General.GetState('Archetype') == "Warshade")):
            if (humanBindKey):
                ResetFile.SetBind(humanBindKey, humanpbind)

        #  kheldian form support
        #  create the Nova and Dwarf form support files if enabled.
        Nova  = self.GetState('Nova')
        Dwarf = self.GetState('Dwarf')

        fullstop = '$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'

        if (Nova and Nova['Enable']):
            ResetFile.SetBind(Nova['Mode'], f"t $name, Changing to {Nova['Nova']} Form{fullstop}{t.on}{Nova['Nova']}$$gototray {Nova['Tray']}" + profile.BLF('nova.txt'))

            novafile = profile.GetBindFile("nova.txt")

            if (Dwarf and Dwarf['Enable']):
                novafile.SetBind(Dwarf['Mode'], f"t $name, Changing to {Dwarf['Dwarf']} Form{fullstop}{t.off}{Nova['Nova']}{t.on}{Dwarf['Dwarf']}$$gototray {Dwarf['Tray']}" + profile.BLF('dwarf.txt'))

            if not humanBindKey:
                humanBindKey = Nova['Mode']

            if self.GetState('UseHumanFormPower'): humpower = '$$powexectoggleon ' + self.GetState('HumanFormShield')
            else:                               humpower = ''

            novafile.SetBind(humanBindKey, f"t $name, Changing to Human Form, SoD Mode{fullstop}$$powexectoggleoff {Nova['Nova']} {humpower} $$gototray 1" + profile.BLF('reset.txt'))

            if (humanBindKey == Nova['Mode']): humanBindKey = None

            if novapbind: novafile.SetBind(Nova['Mode'], novapbind)

            if t.canqfly: self.makeQFlyModeKey(profile,t,"r",novafile,Nova['Nova'],"Nova")

            novafile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind("+forward"))
            novafile.SetBind(self.Ctrls['Left'].MakeFileKeyBind("+left"))
            novafile.SetBind(self.Ctrls['Right'].MakeFileKeyBind("+right"))
            novafile.SetBind(self.Ctrls['Back'].MakeFileKeyBind("+backward"))
            novafile.SetBind(self.Ctrls['Up'].MakeFileKeyBind("+up"))
            novafile.SetBind(self.Ctrls['Down'].MakeFileKeyBind("+down"))
            novafile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind("++forward"))
            novafile.SetBind(self.Ctrls['FlyMode'].MakeFileKeyBind('nop'))
            if (self.GetState('FlyMode') != self.GetState('RunMode')):
                novafile.SetBind(self.Ctrls['RunMode'].MakeFileKeyBind('nop'))
            if (self.GetState('MouseChord')):
                novafile.SetBind('mousechord', "+down$$+forward")

            if (self.GetState('TP') and self.GetState('TPEnable')):
                novafile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('nop'))
                novafile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind( 'nop'))
                novafile.SetBind(self.Ctrls['TPResetKey'].MakeFileKeyBind('nop'))

            novafile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind("follow"))
            # novafile.SetBind(self.Ctrls['ToggleKey'].MakeFileKeyBind('t $name, Changing to Human Form, Normal Mode$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0$$powexectoggleoff ' + Nova['Nova'] + '$$gototray 1' + profile.BLF('reset.txt')))


        if (Dwarf and Dwarf['Enable']):
            ResetFile.SetBind(Dwarf['Mode'], f"t $name, Changing to {Dwarf['Dwarf']} Form{fullstop}$$powexectoggleon {Dwarf['Dwarf']}$$gototray {Dwarf['Tray']}" + profile.BLF('dwarf.txt'))
            dwrffile = profile.GetBindFile("dwarf.txt")
            if (Nova and Nova['Enable']):
                dwrffile.SetBind(Nova['Mode'], f"t $name, Changing to {Nova['Nova']} Form{fullstop}$$powexectoggleoff {Dwarf['Dwarf']}$$powexectoggleon {Nova['Nova']}$$gototray {Nova['Tray']}" + profile.BLF('nova.txt'))

            if not humanBindKey: humanBindKey = Dwarf['Mode']
            if self.GetState('UseHumanFormPower'): humpower = '$$powexectoggleon ' + self.GetState('HumanFormShield')
            else:                               humpower = ''

            dwrffile.SetBind(humanBindKey, f"t $name, Changing to Human Form, SoD Mode{fullstop}$$powexectoggleoff {Dwarf['Dwarf']}{humpower}$$gototray 1" + profile.BLF('reset.txt'))

            if dwarfpbind:
                dwrffile.SetBind(Dwarf['Mode'], dwarfpbind)
            if t.canqfly:
                self.makeQFlyModeKey(profile,t,"r",dwrffile,Dwarf['Dwarf'],"Dwarf")

            dwrffile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind("+forward"))
            dwrffile.SetBind(self.Ctrls['Left'].MakeFileKeyBind("+left"))
            dwrffile.SetBind(self.Ctrls['Right'].MakeFileKeyBind("+right"))
            dwrffile.SetBind(self.Ctrls['Back'].MakeFileKeyBind("+backward"))
            dwrffile.SetBind(self.Ctrls['Up'].MakeFileKeyBind("+up"))
            dwrffile.SetBind(self.Ctrls['Down'].MakeFileKeyBind("+down"))
            dwrffile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind("++forward"))
            dwrffile.SetBind(self.Ctrls['FlyMode'].MakeFileKeyBind('nop'))
            dwrffile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind("follow"))
            if (self.GetState('FlyMode') != self.GetState('RunMode')):
                dwrffile.SetBind(self.Ctrls['RunMode'].MakeFileKeyBind('nop'))
            if (self.GetState('MouseChord')):
                dwrffile.SetBind('mousechord', "+down$$+forward")

            if (self.GetState('TP') and self.GetState('TPEnable')):
                dwrffile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+down$$' + dwarfTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('dtp','tp_on1.txt')))
                dwrffile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('nop'))
                dwrffile.SetBind(self.Ctrls['TPResetKey'].MakeFileKeyBind(t.detailhi[2:] + t.runcamdist + windowshow + profile.BLF('dtp','tp_off.txt')))
                tp_off = profile.GetBindFile("dtp","tp_off.txt")
                tp_off.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+down$$' + dwarfTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('dtp','tp_on1.txt')))
                tp_off.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('nop') )
                tp_on1 = profile.GetBindFile("dtp","tp_on1.txt")
                tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('-down$$powexecunqueue' + t.detailhi + t.runcamdist + windowshow + profile.BLF('dtp','tp_off.txt')))
                tp_on1.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('+down' + profile.BLF('dtp','tp_on2.txt')))

                tp_on2 = profile.GetBindFile("dtp","tp_on2.txt")
                tp_on2.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('-down$$' + dwarfTPPower + profile.BLF('dtp','tp_on1.txt')))

            dwrffile.SetBind(self.Ctrls['ToggleKey'].MakeFileKeyBind("t $name, Changing to Human Form, Normal Mode$fullstop\$\$powexectoggleoff Dwarf['Dwarf']\$\$gototray 1" + profile.BLF('reset.txt')))

        if (self.GetState('JumpSimple')):
            if (self.GetState('JumpCJ') and self.GetState('JumpSJ')):
                ResetFile.SetBind(self.Ctrls['JumpMode'].MakeFileKeyBind('powexecname Super Jump$$powexecname Combat Jumping'))
            elif (self.GetState('JumpSJ')):
                ResetFile.SetBind(self.Ctrls['JumpMode'].MakeFileKeyBind('powexecname Super Jump'))
            elif (self.GetState('JumpCJ')):
                ResetFile.SetBind(self.Ctrls['JumpMode'].MakeFileKeyBind('powexecname Combat Jumping'))

        if (self.GetState('TP') and self.GetState('TPEnable') and not normalTPPower):
            ResetFile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('nop'))
            ResetFile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind( 'nop'))
            ResetFile.SetBind(self.Ctrls['TPResetKey'].MakeFileKeyBind('nop'))

        if (self.GetState('TP') and self.GetState('TPEnable') and not (profile.General.GetState('Archetype') == "Peacebringer") and normalTPPower):
            tphovermodeswitch = ''
            if (t.tphover == ''):
                tphovermodeswitch = t.BLF('R') + "000000.txt"

            ResetFile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+down$$' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))
            ResetFile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('nop'))
            ResetFile.SetBind(self.Ctrls['TPResetKey'].MakeFileKeyBind(t.detailhi[2:] + t.runcamdist + windowshow + profile.BLF('tp','tp_off.txt') + tphovermodeswitch))
            #  Create tp_off file
            tp_off = profile.GetBindFile("tp","tp_off.txt")
            tp_off.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+down$$' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))
            tp_off.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('nop'))

            tp_on1 = profile.GetBindFile("tp","tp_on1.txt")
            zoomin = t.detailhi + t.runcamdist
            if (t.tphover): zoomin = ''
            tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('-down$$powexecunqueue' + zoomin + windowshow + profile.BLF('tp','tp_off.txt') + tphovermodeswitch))
            tp_on1.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('+down' + t.tphover + profile.BLF('tp','tp_on2.txt')))

            tp_on2 = profile.GetBindFile("tp","tp_on2.txt")
            tp_on2.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('-down$$' + normalTPPower + profile.BLF('tp','tp_on1.txt')))

        if (self.GetState('TTP') and self.GetState('TTPEnable') and not (profile.General.GetState('Archetype') == "Peacebringer") and teamTPPower) :
            tphovermodeswitch = ''
            ResetFile.SetBind(self.Ctrls['TTPComboKey'].MakeFileKeyBind('+down$$' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))
            ResetFile.SetBind(self.Ctrls['TTPBindKey'].MakeFileKeyBind( 'nop'))
            ResetFile.SetBind(self.Ctrls['TTPResetKey'].MakeFileKeyBind(t.detailhi[2:] + t.runcamdist + windowshow + profile.BLF('ttp','ttp_off') + tphovermodeswitch))
            #  Create tp_off file
            ttp_off = profile.GetBindFile("ttp","ttp_off.txt")
            ttp_off.SetBind(self.Ctrls['TTPComboKey'].MakeFileKeyBind('+down$$' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))
            ttp_off.SetBind(self.Ctrls['TTPBindKey'].MakeFileKeyBind('nop'))

            ttp_on1 = profile.GetBindFile("ttp","ttp_on1.txt")
            ttp_on1.SetBind(self.Ctrls['TTPComboKey'].MakeFileKeyBind('-down$$powexecunqueue' + t.detailhi + t.runcamdist + windowshow + profile.BLF('ttp','ttp_off') + tphovermodeswitch))
            ttp_on1.SetBind(self.Ctrls['TTPBindKey'].MakeFileKeyBind('+down' + profile.BLF('ttp','ttp_on2.txt')))

            ttp_on2 = profile.GetBindFile("ttp","ttp_on2.txt")
            ttp_on2.SetBind(self.Ctrls['TTPBindKey'].MakeFileKeyBind( '-down$$' + teamTPPower + profile.BLF('ttp','ttp_on1.txt')))



    def sodResetKey(self, curfile, p, path, turnoff, moddir):

        if (moddir == 'up')  : u = 1
        else:                  u = 0
        if (moddir == 'down'): d = 1
        else:                  d = 0

        curfile.SetBind(p.General.Ctrls['ResetKey'].MakeFileKeyBind(
                f'up {u}$$down {d}$$forward 0$$backward 0$$left 0$$right 0' +
                str(turnoff) +
                '$$t $name, SoD Binds Reset' + curfile.BaseReset() +
                f"$$bindloadfile{path}000000.txt"
        ))


    def sodDefaultResetKey(self, mobile, stationary):
        return
        # TODO -- decide where to keep 'resetstring' and make this sub update it.
        cbAddReset('up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'.actPower_name(None,1,stationary,mobile) + '$$t $name, SoD Binds Reset')


    def sodUpKey(self, t, bl, curfile, mobile, stationary, flight, autorun, followbl, bo, sssj):

        (upx,dow,forw,bac,lef,rig) = (t.upx,t.dow,t.forw,t.bac,t.lef,t.rig)

        actkeys = t.totalkeys
        ml = ''

        if (not flight and not sssj):
            mobile = None
            stationary = None

        if (bo == "bo") :
            upx = '$$up 1'
            dow = '$$down 0'
        if (bo == "sd") :
            upx = '$$up 0'
            dow = '$$down 1'

        if     mobile == "GroupFly": mobile     = None
        if stationary == "GroupFly": stationary = None

        if (flight == "Jump"):
           dow = '$$down 0'
           actkeys = t.jkeys
           if (t.totalkeys == 1 and t.space == 1): upx = '$$up 0'
           else:                                         upx = '$$up 1'

           if (t.X == 1):                             upx = '$$up 0'


        toggleon = mobile
        toggleoff2 = ''
        if (actkeys == 0):
           ml = t.mlon
           toggleon = mobile
           if (not (mobile and (mobile == stationary))) : toggleoff = stationary
        else:
            toggleon = ''


        if (t.totalkeys == 1 and t.space == 1):
           ml = t.mloff
           if (not (stationary and (mobile == stationary))) : toggleoff = mobile
           toggleon = stationary
        else:
            toggleoff = ''

        if (sssj):
            if (t.space == 0): #  if we are hitting the space bar rather than releasing its..
               toggleon = sssj
               toggleoff = mobile
               if (stationary and stationary == mobile) : toggleoff2 = stationary
            elif (t.space == 1) : #  if we are releasing the space bar ..
               toggleoff = sssj
               if (t.horizkeys > 0 or autorun) : #  and we are moving laterally, or in autorun..
                   toggleon = mobile
               else: #  otherwise turn on the stationary power..
                   toggleon = stationary

        toggle = ''
        if (toggleon or toggleoff):
           toggle = self.actPower_name(None,1,toggleon,toggleoff,toggleoff2)

        newbits = t.KeyState({'toggle' : 'space'})
        bl = f"{bl}{newbits}.txt"

        if t.space == 1: ini = '-down'
        else:            ini = '+down'

        if (followbl):
            move = ''
            if (t.space != 1):
                bl = f"{followbl}{newbits}.txt"
                move = f"{upx}{dow}{forw}{bac}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Up'].MakeFileKeyBind(f"{ini}{move}{bl}"))
        elif (not autorun):
            curfile.SetBind(self.Ctrls['Up'].MakeFileKeyBind(f"{ini}{upx}{dow}{forw}{bac}{lef}{rig}{ml}{toggle}{bl}"))
        else:
            if (not sssj) : toggle = ''  #  returns the following line to the way it was before sssj
            curfile.SetBind(self.Ctrls['Up'].MakeFileKeyBind(f"{ini}{upx}{dow}$$backward 0{lef}{rig}{toggle}{t.mlon}{bl}"))

    def sodDownKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo,sssj):
        (up,dowx,forw,bac,lef,rig) = (t.up,t.dowx,t.forw,t.bac,t.lef,t.rig)

        actkeys = t.totalkeys
        ml = ''

        up = dowx = forw = bac = lef = rig = ''
        if (not flight):
            mobile = None
            stationary = None
        if (bo == 'bo'):
            up = '$$up 1'
            dowx = '$$down 0'
        if (bo == 'sd'):
            up = '$$up 0'
            dowx = '$$down 1'

        if (mobile     and mobile     == 'Group Fly'): mobile = None
        if (stationary and stationary == 'Group Fly'): stationary = None

        if (flight == 'Jump'):
            dowx = '$$down 0'
            if (t.cancj  == 1) : aj = t.cjmp
            if (t.canjmp == 1) : aj = t.jump
            actkeys = t.jkeys
            if (t.X == 1 and t.totalkeys > 1) : up = '$$up 1'
            else:                                     up = '$$up 0'

        toggleon = mobile
        if (actkeys == 0):
           ml = t.mlon
           toggleon = mobile
           if (not (mobile and mobile == stationary)): toggleoff = stationary
        else:
           toggleon = None

        if (t.totalkeys == 1 and t.X == 1):
           ml = t.mloff
           if (not (stationary and mobile == stationary)): toggleoff = mobile
           toggleon = stationary
        else:
            toggleoff = None

        toggle = ''
        if (toggleon or toggleoff):
           toggle = self.actPower_name(None,1,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'X'})
        bl = f"{bl}{t.space}{1-t.X}{t.W}{t.S}{t.A}{t.D}.txt"

        if t.X == 1: ini = "-down"
        else:           ini = "+down"

        if (followbl):
            move = ''
            if (t.X != 1):
                bl = f"{followbl}{t.space}{t.W}{t.S}{t.A}{t.D}.txt"
                move = f"{up}{dowx}{forw}{bac}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Down'].MakeFileKeyBind(f"{ini}{move}{bl}"))
        elif (not autorun):
            curfile.SetBind(self.Ctrls['Down'].MakeFileKeyBind(f"{ini}{up}{dowx}{forw}{bac}{lef}{rig}{ml}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Down'].MakeFileKeyBind(f"{ini}{up}{dowx}$$backward 0{lef}{rig}{t.mlon}{bl}"))

    def sodForwardKey(self, t, bl, curfile,  mobile, stationary, flight, autorunbl, followbl, bo, sssj):
        (up,dow,forx,bac,lef,rig) = (t.up,t.dow,t.forx,t.bac,t.lef,t.rig)

        actkeys = t.totalkeys
        ml = toggleoff = ''
        if (bo == "bo") : up = '$$up 1'; dow = '$$down 0'
        if (bo == "sd") : up = '$$up 0'; dow = '$$down 1'

        if (mobile     == 'Group Fly'): mobile = None
        if (stationary == 'Group Fly'): stationary = None

        if (flight == "Jump"):
           dow = '$$down 0'
           actkeys = t.jkeys
           if (
                (t.totalkeys == 1 and t.W == 1)
                    or
                (t.X == 1)
                ): up = '$$up 0'
           else : up = '$$up 1'

        toggleon = mobile
        if (t.totalkeys == 0) :
            ml = t.mlon
            if (not (mobile and mobile == stationary)):
               toggleoff = stationary

        if (t.totalkeys == 1 and t.W == 1):
            ml = t.mloff

        if flight: testKeys = t.totalkeys
        else:      testKeys = t.horizkeys
        if (testKeys == 1 and t.W == 1) :
            if (not (stationary and mobile == stationary)):
                toggleoff = mobile

            toggleon = stationary

        if (sssj and t.space == 1) : #  if (we are jumping with SS+SJ mode enabled)
           toggleon = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff):
           toggle = self.actPower_name(None,1,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'W'})
        bl = f"{bl}{newbits}.txt"

        if t.W == 1: ini = "-down"
        else:           ini = "+down"

        if (followbl):
            if (t.W == 1):
               move = ini
            else:
                bl = f"{followbl}{newbits}.txt"
                move = f"{ini}{up}{dow}{forx}{bac}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind(move + bl))
            if (self.GetState('MouseChord')):
                if (t.W == 1) : move = f"{ini}{up}{dow}{forx}{bac}{rig}{lef}"
                curfile.SetBind('mousechord',  move + bl)

        elif (not autorunbl):
            curfile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind(f"{ini}{up}{dow}{forx}{bac}{lef}{rig}{ml}{toggle}{bl}"))
            if (self.GetState('MouseChord')):
                curfile.SetBind('mousechord', f"{ini}{up}{dow}{forx}{bac}{rig}{lef}{ml}{toggle}{bl}")

        else:
            if (t.W == 1):
                bl = f"{autorunbl}{newbits}.txt"

            curfile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind(f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{lef}{rig}{t.mlon}{bl}"))
            if (self.GetState('MouseChord')) :
                curfile.SetBind('mousechord', f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{rig}{lef}{t.mlon}{bl}")

    def sodBackKey(self,t,bl,curfile,mobile,stationary,flight,autorunbl,followbl,bo,sssj):
        (up,dow,forw,bacx,lef,rig) = (t.up,t.dow,t.forw, t.bacx,t.lef,t.rig)

        actkeys = t.totalkeys
        ml = toggleoff = ''
        if (bo == "bo") : up = '$$up 1';dow = '$$down 0'
        if (bo == "sd") : up = '$$up 0';dow = '$$down 1'

        if (mobile     == 'Group Fly'): mobile = None
        if (stationary == 'Group Fly'): stationary = None

        if (flight == "Jump"):
           dow = '$$down 0'
           actkeys = t.jkeys
           if (t.totalkeys == 1 and t.S == 1) : up = '$$up 0'
           else:                                      up = '$$up 1'

           if (t.X == 1) : up = '$$up 0'

        toggleon = mobile
        if (t.totalkeys == 0):
           ml = t.mlon
           toggleon = mobile
           if (not (mobile and mobile == stationary)):
               toggleoff = stationary

        if (t.totalkeys == 1 and t.S == 1):
            ml = t.mloff

        if flight: testKeys = t.totalkeys
        else:      testKeys = t.horizkeys
        if (testKeys == 1 and t.S == 1):
            if (not (stationary and mobile == stationary)):
               toggleoff = mobile

            toggleon = stationary

        if (sssj and t.space == 1): #  if (we are jumping with SS+SJ mode enabled
            toggleon = sssj
            toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
           toggle = self.actPower_name(None,1,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'S'})
        bl = f"{bl}{newbits}.txt"

        if (t.S == 1) : ini = "-down"
        else:              ini = "+down"

        if (followbl):
            if (t.S == 1):
               move = ini
            else:
                bl = f"{followbl}{newbits}.txt"
                move = f"{ini}{up}{dow}{forw}{bacx}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Back'].MakeFileKeyBind(move + bl))
        elif (not autorunbl) :
            curfile.SetBind(self.Ctrls['Back'].MakeFileKeyBind(f"{ini}{up}{dow}{forw}{bacx}{lef}{rig}{ml}{toggle}{bl}"))
        else:
            if (t.S == 1):
                move = '$$forward 1$$backward 0'
            else:
                move = '$$forward 0$$backward 1'
                bl = f"{autorunbl}{newbits}.txt"

            curfile.SetBind(self.Ctrls['Back'].MakeFileKeyBind(f"{ini}{up}{dow}{move}{lef}{rig}{t.mlon}{bl}"))

    def sodLeftKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo,sssj):
        (up,dow,forw,bac,lefx,rig) = (t.up,t.dow,t.forw,t.bac, t.lefx,t.rig)

        actkeys = t.totalkeys
        ml = toggleoff = ''
        if (bo == "bo") : up = '$$up 1';dow = '$$down 0'
        if (bo == "sd") : up = '$$up 0';dow = '$$down 1'

        if (mobile     == 'Group Fly') : mobile = None
        if (stationary == 'Group Fly') : stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            actkeys = t.jkeys
            if (t.totalkeys == 1 and t.A == 1) : up = '$$up 0'
            else:                                      up = '$$up 1'

            if (t.X == 1) : up = '$$up 0'

        toggleon = mobile
        if (t.totalkeys == 0):
            ml = t.mlon
            toggleon = mobile
            if (not (mobile and mobile == stationary)) :
                toggleoff = stationary

        if (t.totalkeys == 1 and t.A == 1) :
            ml = t.mloff

        if flight: testKeys = t.totalkeys
        else:      testKeys = t.horizkeys

        if (testKeys == 1 and t.A == 1) :
            if (not (stationary and mobile == stationary)):
               toggleoff = mobile

            toggleon = stationary

        if (sssj and t.space == 1) : #  if (we are jumping with SS+SJ mode enabled
           toggleon = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
           toggle = self.actPower_name(None,1,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'A'})
        bl = f"{bl}{newbits}.txt"

        if (t.A == 1): ini = '-down'
        else:             ini = '+down'

        if (followbl) :
            if (t.A == 1) :
               move = ini
            else:
                bl = f"{followbl}{newbits}.txt"
                move = f"{ini}{up}{dow}{forw}{bac}{lefx}{rig}"

            curfile.SetBind(self.Ctrls['Left'].MakeFileKeyBind(move + bl))
        elif (not autorun) :
            curfile.SetBind(self.Ctrls['Left'].MakeFileKeyBind(f"{ini}{up}{dow}{forw}{bac}{lefx}{rig}{ml}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Left'].MakeFileKeyBind(f"{ini}{up}{dow}{'$$backward 0'}{lefx}{rig}{t.mlon}{bl}"))

    def sodRightKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo,sssj):
        (up,dow,forw,bac,lef,rigx) = (t.up,t.dow,t.forw,t.bac,t.lef, t.rigx)

        actkeys = t.totalkeys
        ml = toggleoff = ''
        if (bo == "bo") :up = '$$up 1';dow = '$$down 0'
        if (bo == "sd") :up = '$$up 0';dow = '$$down 1'

        if (mobile     == 'Group Fly') : mobile = None
        if (stationary == 'Group Fly') : stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            actkeys = t.jkeys
            if (t.totalkeys == 1 and t.D == 1) : up = '$$up 0'
            else:                                      up = '$$up 1'

            if (t.X == 1) : up = '$$up 0'

        toggleon = mobile
        if (t.totalkeys == 0):
           ml = t.mlon
           toggleon = mobile
           if (not (mobile and mobile == stationary)) :
               toggleoff = stationary

        if (t.totalkeys == 1 and t.D == 1) :
           ml = t.mloff

        if flight: testKeys = t.totalkeys
        else :     testKeys = t.horizkeys
        if (testKeys == 1 and t.D == 1) :
            if (not (stationary and mobile == stationary)):
               toggleoff = mobile

            toggleon = stationary

        if (sssj and t.space == 1) : #  if (we are jumping with SS+SJ mode enabled
           toggleon = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) : 
           toggle = self.actPower_name(None,1,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'D'})
        bl = f"{bl}{newbits}.txt"

        if (t.D == 1): ini = '-down'
        else:             ini = '+down'

        if (followbl) :
            if (t.D == 1):
                move = ini
            else:
                bl = f"{followbl}{newbits}.txt"
                move = f"{ini}{up}{dow}{forw}{bac}{lef}{rigx}"

            curfile.SetBind(self.Ctrls['Right'].MakeFileKeyBind(move + bl))
        elif (not autorun) :
            curfile.SetBind(self.Ctrls['Right'].MakeFileKeyBind(f"{ini}{up}{dow}{forw}{bac}{lef}{rigx}{ml}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Right'].MakeFileKeyBind(f"{ini}{up}{dow}$$forward 1$$backward 0{lef}{rigx}{t.mlon}{bl}"))


    def sodAutoRunKey(self,t,bl,curfile,mobile,sssj):
        if (sssj and t.space == 1) :
            curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mlon + self.actPower_name(None,1,sssj,mobile) + bl))
        else:
            curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mlon + self.actPower_name(None,1,mobile) + bl))

    def sodAutoRunOffKey(self, t,bl,curfile,mobile,stationary,flight,sssj):
        if (not flight and not sssj) :
            if (t.horizkeys > 0) :
               toggleon = t.mlon + self.actPower_name(None,1,mobile)
            else:
               toggleon = t.mloff + self.actPower_name(None,1,stationary,mobile)

        elif (sssj) :
            if (t.horizkeys > 0 or t.space == 1) :
               toggleon = t.mlon + self.actPower_name(None,1,mobile,toggleoff)
            else:
               toggleon = t.mloff + self.actPower_name(None,1,stationary,mobile,toggleoff)

        else:
            if (t.totalkeys > 0) :
               toggleon = t.mlon + self.actPower_name(None,1,mobile)
            else:
               toggleon = t.mloff + self.actPower_name(None,1,stationary,mobile)

        bindload = bl + t.KeyState() + '.txt'
        curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind(t.dirs('UDFBLR') + toggleon + bindload))


    def sodFollowKey(self, t,bl,curfile,mobile):
        curfile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind('follow' + self.actPower_name(None,1,mobile) + bl + t.KeyState() + '.txt'))

    def sodFollowOffKey(self, t,bl,curfile,mobile,stationary,flight):
        toggle = ''
        if (not flight):
            if (t.horizkeys == 0) :
                if (stationary == mobile) :
                   toggle = self.actPower_name(None,1,stationary,mobile)
                else:
                   toggle = self.actPower_name(None,1,stationary)

        else:
            if (t.totalkeys == 0) :
                if (stationary == mobile) :
                   toggle = self.actPower_name(None,1,stationary,mobile)
                else:
                   toggle = self.actPower_name(None,1,stationary)

        curfile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind("follow" + toggle + t.up + t.dow + t.forw + t.bac + t.lef + t.rig + bl + t.KeyState() + '.txt'))


    def bindisused(self):
        return self.GetState('Enable')


#    def findconflicts(self):
#        Utility.CheckConflict("Up","Up Key")
#        Utility.CheckConflict("Down","Down Key")
#        Utility.CheckConflict("Forward","Forward Key")
#        Utility.CheckConflict("Back","Back Key")
#        Utility.CheckConflict("Left","Strafe Left Key")
#        Utility.CheckConflict("Right","Strafe Right Key")
#        Utility.CheckConflict("TLeft","Turn Left Key")
#        Utility.CheckConflict("TRight","Turn Right Key")
#        Utility.CheckConflict("AutoRun","AutoRun Key")
#        Utility.CheckConflict("Follow","Follow Key")
#
#        if (self.GetState('NonSoD'))       : Utility.CheckConflict("NonSoDMode","NonSoD Key")
#        if (self.GetState('Base'))         : Utility.CheckConflict("BaseMode","Sprint Mode Key")
#        if (self.GetState('SSSS'))         : Utility.CheckConflict("RunMode","Speed Mode Key")
#        if (self.GetState('JumpCJ')
#                or self.GetState('JumpSJ') ): Utility.CheckConflict("JumpMode","Jump Mode Key")
#        if (self.GetState('FlyHover')
#                or self.GetState('FlyFly') ): Utility.CheckConflict("FlyMode","Fly Mode Key")
#        if (self.GetState('FlyQFly')
#                and (profile.General.GetState('Archetype') == "Peacebringer")): Utility.CheckConflict("QFlyMode","Q.Fly Mode Key")
#        if (self.GetState('TP') and self.GetState('TPEnable')):
#            Utility.CheckConflict(self.GetState('TP'),"ComboKey","TP ComboKey")
#            Utility.CheckConflict(self.GetState('TP'),"ResetKey","TP ResetKey")
#
#            TPQuestion = "Teleport Bind"
#            if (profile.General.GetState('Archetype') == "Peacebringer") :
#               TPQuestion = "Dwarf Step Bind"
#            elif (profile.General.GetState('Archetype') == "Warshade") :
#               TPQuestion = "Shd/Dwf Step Bind"
#
#            Utility.CheckConflict(self.GetState('TP'),"BindKey", TPQuestion)
#
#            if (self.GetState('FlyGFly')): Utility.CheckConflict("GFlyMode","Group Fly Key")
#        if (self.GetState('TTP') and self.GetState('TTPEnable')):
#            Utility.CheckConflict(self.GetState('TTP'),"ComboKey","TTP ComboKey")
#            Utility.CheckConflict(self.GetState('TTP'),"ResetKey","TTP ResetKey")
#            Utility.CheckConflict(self.GetState('TTP'),"BindKey","Team TP Bind")
#
#        if (self.GetState('Temp') and self.GetState('TempEnable')):
#            Utility.CheckConflict("TempMode","Temp Mode Key")
#            Utility.CheckConflict(self.GetState('Temp'),"TraySwitch","Tray Toggle Key")
#
#        if ((self.Profile.General.GetState('Archetype') == "Peacebringer") or (self.Profile.General.GetState('Archetype') == "Warshade")) :
#            if (self.GetState('Nova')  and self.GetState('NovaEnable')): Utility.CheckConflict(self.GetState('Nova'), "Mode","Nova Form Bind")
#            if (self.GetState('Dwarf') and self.GetState('DwarfEnable')): Utility.CheckConflict(self.GetState('Dwarf'),"Mode","Dwarf Form Bind")


    #  toggleon variation
    def actPower_toggle(self, start, unq, on, *rest):
        s = ''
        if not isinstance(on, str):
            #  deal with power slot stuff..
          traytest = on['trayslot']

        offpower = {}

        for v in rest:
            if v and not isinstance(v, str):
                for j, w in v.items():
                    if (w and w != 'on' and not offpower[w]):
                        if not isinstance(w, str):
                            if (w['trayslot'] == traytest):
                               s = s + '$$powexectray ' + w['trayslot']
                               unq = 1

                        else:
                           offpower['w'] = 1
                           s = s + '$$powexectoggleoff ' + w

                if (v['trayslot'] and v['trayslot'] == traytest):
                   s = s + '$$powexectray ' + v['trayslot']
                   unq = 1

            else:
                if (v and (v != 'on') and not offpower.get(v, None)):
                   offpower[v] = 1
                   s = s + '$$powexectoggleoff ' + v

        if (unq and s):
           s = s + '$$powexecunqueue'

        # if start then s = string.sub(s,3,string.len(s)) end
        if (on):
            if not (isinstance(on, str)):
                #  deal with power slot stuff..
               s = s + '$$powexectray '.on['trayslot'] + '$$powexectray ' + on['trayslot']
            else:
               s = s + '$$powexectoggleon ' + on

        return s


    def actPower_name(self, start, unq, on,*rest):
        s = ''
        if not isinstance(on, str):
           #  deal with power slot stuff..
           traytest = on['trayslot']

        for v in rest:
            if isinstance(v, str):
                if (v and v != 'on'):
                   s = s + '$$powexecname ' + v

            elif v: #v is a dict
                for _,w in v.items():
                    if (w and w != 'on'):
                        if isinstance(w, str):
                           s = s + '$$powexecname ' + w
                        else:
                           if (w['trayslot'] == traytest):
                               s = s + '$$powexectray ' + w['trayslot']


                if (v['trayslot'] and v['trayslot'] == traytest):
                   s = s + '$$powexectray ' + v['trayslot']

        if (unq and s):
           s = s + '$$powexecunqueue'

        if (on):
            if isinstance(s, str):
               s = s + '$$powexecname ' + on + '$$powexecname ' + on
            else:
                #  deal with power slot stuff..
               s = s + '$$powexectray ' + on['trayslot'] + '$$powexectray ' + on['trayslot']

        if (start): s = s[:2]
        return s

    actPower = actPower_name
    #actPower = actPower_toggle


    # TODO - this isn't used anywhere, is it useful?
    #  updated hybrid binds can reduce the space used in SoD Bindfiles by more than 40KB per SoD mode generated
    # sub actPower_hybrid {
    #     my ($start,$unq,$on,@rest) = @_
    #     my ($s,traytest) = ('','')
    #     if (refon) {traytest =on['trayslot']

    #     for v (@rest) {
    #         if (!refv):
    #             if ($v == 'on') {s .= '$$powexecname ' + v
    #          else:
    #             while (my (None,w) = each %$v) {
    #                 if ($w andw ne 'on'):
    #                     if (refw):
    #                         if ($w['trayslot'] ==traytest) {
    #                            s .= '$$powexectray ' + w['trayslot']

    #                      else:
    #                        s .= '$$powexecname ' + w



    #             if ($v['trayslot'] ==traytest) {
    #                s .= '$$powexectray ' + v['trayslot']



    #     if ($unq ands) {s .= '$$powexecunqueue'

    #     if ($on):
    #         if (refon):
    #             #  deal with power slot stuff..
    #            s .= '$$powexectray ' + on['trayslot'] + '$$powexectray ' + on['trayslot']
    #          else:
    #            s .= '$$powexectoggleon ' + on


    #     if ($start) {s = substrs, 2
    #     returns


    # local actPower = actPower_name
    # # local actPower = self.actPower_toggle

    def sodJumpFix(self, profile,t,key,makeModeKey,suffix,bl,curfile,turnoff,autofollowmode,feedback):

        filename = t.path(f"{autofollowmode}j",suffix)
        tglfile = profile.GetBindFile(filename)
        t.ini = '-down$$'
        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key, "+down" + feedback + self.actPower_name(None,1,t.cjmp) + profile.BLF(filename))


    def sodSetDownFix(self, profile,t,key,makeModeKey,suffix,bl,curfile,turnoff,autofollowmode,feedback):
        if autofollowmode:
            pathsuffix = "f"
        else:
            pathsuffix = "a"

        filename = t.path(f"{autofollowmode}{pathsuffix}",suffix)
        tglfile = profile.GetBindFile(filename)
        t.ini = '-down$$'
        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key, '+down' + feedback + profile.BLF(filename))



    UI.Labels.update( {
        'Up' : 'Up',
        'Down' : 'Down',
        'Forward' : 'Forward',
        'Back' : 'Back',
        'Left' : 'Strafe Left',
        'Right' : 'Strafe Right',
        'TurnLeft' : 'Turn Left',
        'TurnRight' : 'Turn Right',
        'AutoRun' : 'Auto Run',
        'Follow' : 'Follow Target',

        'DefaultMode' : 'Default SoD Mode',
        'MousechordSoD' : 'Mousechord is SoD Forward',
        'AutoMouselook' : 'Automatically Mouselook when moving',

        'SprintPower' : 'Power to use for Sprint',

        'ChangeCamera' : 'Change camera distance when moving',
        'CamdistBase' : 'Base Camera Distance',
        'CamdistTravelling' : 'Travelling Camera Distance',

        'ChangeDetail' : 'Change graphics detail level when moving',
        'DetailBase' : 'Base Detail Level',
        'DetailTravelling' : 'Travelling Detail Level',

        'NonSoDMode' : 'Non-SoD Mode',
        'JumpMode' : 'Toggle Jump Mode',
        'SimpleSJCJ' : 'Simple Combat Jumping / Super Jump Toggle',

        'RunMode' : 'Toggle Super Speed Mode',
        'SSOnlyWhenMoving' : 'SuperSpeed only when moving',
        'SSSJModeEnable' : 'Enable Super Speed / Super Jump Mode',

        'FlyMode' : 'Toggle Fly Mode',
        'GFlyMode' : 'Toggle Group Fly Mode',

        'SelfTellOnChange' : 'Self-/tell when changing mode',

        'TPMode'  : 'Teleport Bind',
        'TPCombo' : 'Teleport Combo Key',
        'TPReset' : 'Teleport Reset Key',
        'TPHideWindows' : 'Hide Windows when Teleporting',
        'TPAutoHover' : 'Hover when Teleporting',

        'TTPMode'  : 'Team Teleport Bind',
        'TTPCombo' : 'Team Teleport Combo Key',
        'TTPReset' : 'Team Teleport Reset Key',
        'TTPAutoGFly' : 'Group Fly when Team Teleporting',

        'TempMode' : 'Toggle Temp Mode',
        'TempTray' : 'Temporary Travel Power Tray',

        'NovaMode' : 'Toggle Nova Form',
        'NovaTray' : 'Nova Travel Power Tray',
        'DwarfMode' : 'Toggle Dwarf Form',
        'DwarfTray' : 'Dwarf Travel Power Tray',
        'HumanMode' : 'Human Form',
        'HumanTray' : 'Human Travel Power Tray',

        'SprintSoD' : 'Enable Sprint SoD',
    })

class tObject(dict):
    def __init__(self, profile):
            self.profile    = profile
            self.sprint     = ''
            self.speed      = ''
            self.hover      = ''
            self.fly        = ''
            self.flyx       = ''
            self.jump       = ''
            self.cjmp       = ''
            self.canhov     = 0
            self.canfly     = 0
            self.canqfly    = 0
            self.cangfly    = 0
            self.cancj      = 0
            self.canjmp     = 0
            self.canss      = 0
            self.tphover    = ''
            self.ttpgrpfly  = ''
            self.on         = '$$powexectoggleon '
            # self.on       = '$$powexecname '
            self.off        = '$$powexectoggleoff '
            self.mlon       = ''
            self.mloff      = ''
            self.runcamdist = ''
            self.flycamdist = ''
            self.detailhi   = ''
            self.detaillo   = ''
            self.RunMode    = ''
            self.JumpMode   = ''

            self.space      = 0
            self.X          = 0
            self.W          = 0
            self.S          = 0
            self.A          = 0
            self.D          = 0
            self.up         = ''
            self.dow        = ''
            self.forw       = ''
            self.bac        = ''
            self.lef        = ''
            self.rig        = ''

            self.bl   = ''
            self.bla  = ''
            self.blf  = ''
            self.blbo = ''
            self.blsd = ''

            self.path       = ''
            self.gamepath   = ''
            self.patha      = ''
            self.gamepatha  = ''
            self.pathf      = ''
            self.gamepathf  = ''
            self.pathbo     = ''
            self.gamepathbo = ''
            self.pathsd     = ''
            self.gamepathsd = ''

    # return binary "011010" string of which keys are "on";
    # optionally flipping one of them first.
    # TODO:  not clear this belongs on a class as opposed
    # to just a utility sub here or in Utility.
    def KeyState(self, p = {}):
        togglebit = p.get('toggle', '')

        ret = ''
        for key in ('space','X','W','S','A','D'):
            retthing = int(getattr(self, key))
            if key == togglebit:
                ret = ret + str(1 - retthing)
            else:
                ret = ret + str(retthing)
        return ret

    def dirs(self, dirs):
        dirdict = { 'U': 'up', "D": 'dow', "F": 'forw', "B": 'bac', "L": 'lef', "R": 'rig' }
        ret = ''
        for dir in list(dirs):
           #ret += self[ dirdict[dir] ]
           ret += getattr(self, dirdict[dir])

        return ret


    # These next two subs are terrible.  This stuff should all be squirreled away in BindFile.

    # This will return "$bindloadfilesilent C:\path\CODE\CODE1010101<suffix>.txt"
    def BLF(self, code, suffix = ''):
        return self.profile.BLF(code.upper(), code.upper() + self.KeyState() + suffix + '.txt')
#
#
#    # This will return "CODE\CODE1010101<suffix>.txt"
#    sub path {
#        my self = shift
#        code = shift
#        suffix = shift || ''
#        return File::Spec.catpath(None, uc($code), uc($code) + self.KeyState() + suffix + '.txt')
#
#

