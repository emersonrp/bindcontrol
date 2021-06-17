import wx
import re
import UI
import Utility

from Page import Page
from UI.ControlGroup import ControlGroup


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
            'DefaultMode'        : '',
            'MousechordSoD'      : 1,
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
            'Unqueue'            : 1,
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

        self.Init['HumanMode']    = "UNBOUND"
        self.Init['HumanTray']    = "1"
        self.Init['HumanHumanPBind'] = "nop"
        self.Init['HumanNovaPBind']  = "nop"
        self.Init['HumanDwarfPBind'] = "nop"

        #  Temp Travel Powers
        self.Init['TempTray'] = "6"
        self.Init['TempTraySwitch'] = "UNBOUND"
        self.Init['TempMode'] = "UNBOUND"

    def BuildPage(self):

        topSizer = wx.FlexGridSizer(0,2,10,10)
        EnableSoD = wx.CheckBox( self, -1, "Enable Speed On Demand Binds",  )
        EnableSoD.SetValue(True)
        topSizer.Add( EnableSoD, 0, wx.TOP|wx.LEFT, 10)
        topSizer.AddSpacer(1)
        self.Controls['EnableSoD'] = EnableSoD
        EnableSoD.Bind(wx.EVT_CHECKBOX, self.OnEnableSoD)

        leftColumn  = wx.BoxSizer(wx.VERTICAL)
        rightColumn = wx.BoxSizer(wx.VERTICAL)


        ##### MOVEMENT KEYS
        movementSizer = ControlGroup(self, self, 'Movement Keys')

        for dir in ("Up","Down","Forward","Back","Left","Right","TurnLeft","TurnRight"):
            movementSizer.AddLabeledControl(
                ctlName = dir,
                ctlType = 'keybutton',
            )
        # TODO!  fill this picker with only the appropriate bits.
        # for i in (powers list):
        #   if (player has power): add_to_contents(i)
        movementSizer.AddLabeledControl(
            ctlName = 'DefaultMode',
            ctlType = 'combo',
            contents = ('No SoD','Sprint','Super Speed','Jump','Fly'),
        )
        movementSizer.AddLabeledControl(
            ctlName = 'MousechordSoD',
            ctlType = 'checkbox',
        )
        leftColumn.Add(movementSizer, 0, wx.EXPAND)


        ##### GENERAL SETTINGS
        generalSizer = ControlGroup(self, self, 'General Settings')

        generalSizer.AddLabeledControl(
            ctlName = 'AutoMouseLook',
            ctlType = 'checkbox',
            tooltip = 'Automatically Mouselook when moving',
        )
        # TODO -- add "SprintPowers" to GameData
#        generalSizer.AddLabeledControl(
#            ctlName = 'SprintPower',
#            ctlType = 'combo',
#            contents = GameData['SprintPowers'],
#        )

        # TODO -- decide what to do with this.
        # generalSizer.Add( wx.CheckBox(self, SPRINT_UNQUEUE, "Exec powexecunqueue"))

        for command in ("AutoRun","Follow","NonSoDMode"): # TODO - lost "Sprint-Only SoD Mode" b/c couldn't find the name in %$Labels
            generalSizer.AddLabeledControl(
                ctlName = command,
                ctlType = 'keybutton',
            )
        generalSizer.AddLabeledControl(
            ctlName = 'SprintSoD',
            ctlType = 'checkbox',
        )
        generalSizer.AddLabeledControl(
            ctlName = 'ChangeCamera',
            ctlType = 'checkbox',
        )
        generalSizer.AddLabeledControl(
            ctlName = 'CamdistBase',
            ctlType = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddLabeledControl(
            ctlName = 'CamdistTravelling',
            ctlType = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddLabeledControl(
            ctlName = 'ChangeDetail',
            ctlType = 'checkbox',
        )
        generalSizer.AddLabeledControl(
            ctlName = 'DetailBase',
            ctlType = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddLabeledControl(
            ctlName = 'DetailTravelling',
            ctlType = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddLabeledControl(
            ctlName = 'TPHideWindows',
            ctlType = 'checkbox',
        )
        generalSizer.AddLabeledControl(
            ctlName = 'SelfTellOnChange',
            ctlType = 'checkbox',
        )
        leftColumn.Add(generalSizer, 0, wx.EXPAND)


        ##### TEMP TRAVEL POWERS
        tempSizer = ControlGroup(self, self, 'Temp Travel Powers')
        # if (temp travel powers exist)?  Should this be "custom"?
        tempSizer.AddLabeledControl(
            ctlName = 'TempMode',
            ctlType = 'keybutton',
        )
        tempSizer.AddLabeledControl(
            ctlName = 'TempTray',
            ctlType = 'spinbox',
            contents = [1, 8],
        )
        leftColumn.Add(tempSizer, 0, wx.EXPAND)

        ##### SUPER SPEED
        superSpeedSizer = ControlGroup(self, self, 'Super Speed')
        superSpeedSizer.AddLabeledControl(
            ctlName = 'RunMode',
            ctlType = 'keybutton',
        )
        superSpeedSizer.AddLabeledControl(
            ctlName = 'SSOnlyWhenMoving',
            ctlType = 'checkbox',
        )
        superSpeedSizer.AddLabeledControl(
            ctlName = 'SSSJModeEnable',
            ctlType = 'checkbox',
        )
        rightColumn.Add(superSpeedSizer, 0, wx.EXPAND)

        ##### SUPER JUMP
        superJumpSizer = ControlGroup(self, self, 'Super Jump')
        superJumpSizer.AddLabeledControl(
            ctlName = 'JumpMode',
            ctlType = 'keybutton',
        )
        superJumpSizer.AddLabeledControl(
            ctlName = 'SimpleSJCJ',
            ctlType = 'checkbox',
        )
        rightColumn.Add(superJumpSizer, 0, wx.EXPAND)


        ##### FLY
        flySizer = ControlGroup(self, self, 'Flight')

        flySizer.AddLabeledControl(
            ctlName = 'FlyMode',
            ctlType = 'keybutton',
        )
        flySizer.AddLabeledControl(
            ctlName = 'GFlyMode',
            ctlType = 'keybutton',
        )
        rightColumn.Add(flySizer, 0, wx.EXPAND)

        ##### TELEPORT
        teleportSizer = ControlGroup(self, self, 'Teleport')

        # if (at == peacebringer) "Dwarf Step"
        # if (at == warshade) "Shadow Step / Dwarf Step"

        teleportSizer.AddLabeledControl(
            ctlName = "TPMode",
            ctlType = 'keybutton',
        )
        teleportSizer.AddLabeledControl(
            ctlName = "TPCombo",
            ctlType = 'keybutton',
        )
        teleportSizer.AddLabeledControl(
            ctlName = "TPReset",
            ctlType = 'keybutton',
        )

        # if (player has hover): {
        teleportSizer.AddLabeledControl(
            ctlName = 'TPAutoHover',
            ctlType = 'checkbox',
        )
        #

        # if (player has team-tp) {
        teleportSizer.AddLabeledControl(
            ctlName = "TTPMode",
            ctlType = 'keybutton',
        )
        teleportSizer.AddLabeledControl(
            ctlName = "TTPCombo",
            ctlType = 'keybutton',
        )
        teleportSizer.AddLabeledControl(
            ctlName = "TTPReset",
            ctlType = 'keybutton',
        )

        # if (player has group fly) {
        teleportSizer.AddLabeledControl(
            ctlName = 'TTPAutoGFly',
            ctlType = 'checkbox',
        )
        #
        #
        # end team-tp
        rightColumn.Add(teleportSizer, 0, wx.EXPAND)

        ##### KHELDIAN TRAVEL POWERS
        kheldianSizer = ControlGroup(self, self, 'Nova / Dwarf Travel Powers')

        kheldianSizer.AddLabeledControl(
            ctlName = 'NovaMode',
            ctlType = 'keybutton',
        )
        kheldianSizer.AddLabeledControl(
            ctlName = 'NovaTray',
            ctlType = 'spinbox',
            contents = [1, 8],
        )
        kheldianSizer.AddLabeledControl(
            ctlName = 'DwarfMode',
            ctlType = 'keybutton',
        )
        kheldianSizer.AddLabeledControl(
            ctlName = 'DwarfTray',
            ctlType = 'spinbox',
            contents = [1, 8],
        )

        # do we want a key to change directly to human form, instead of toggles?
        kheldianSizer.AddLabeledControl(
            ctlName = 'HumanMode',
            ctlType = 'keybutton',
        )
        kheldianSizer.AddLabeledControl(
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

    def OnEnableSoD(self, evt):
        for c,control in self.Controls.items():
            if c != 'EnableSoD':  # don't disable yourself kthx
                control.Enable(evt.EventObject.IsChecked())

    def makeSoDFile(self, p):

        profile = self.Profile

        t = p['t']
        t['D'] = t.get('D', '')
        t['L'] = t.get('L', '')
        t['R'] = t.get('R', '')
        t['F'] = t.get('F', '')
        t['B'] = t.get('B', '')

        bl   = t.get('bl', {}).get(p['bl'], "")
        bla  = t.get('bl', {}).get(p['bla'], "")
        blf  = t.get('bl', {}).get(p['blf'], "")
        blbo = t.get('bl', {}).get(p['blbo'], "")
        blsd = t.get('bl', {}).get(p['blsd'], "")

        path   = t.get('path', {}).get(p['path'], "")
        pathr  = t.get('path', {}).get(p['pathr'], "")
        pathf  = t.get('path', {}).get(p['pathf'], "")
        pathbo = t.get('path', {}).get(p['pathbo'], "")
        pathsd = t.get('path', {}).get(p['pathsd'], "")

        mobile     = p.get('mobile', "")
        stationary = p.get('stationary', "")
        modestr    = p.get('modestr', "")
        flight     = p.get('flight', "")
        fix        = p.get('fix', "")
        turnoff    = p.get('turnoff', "")
        sssj       = p.get('sssj', "")

        # TODO -- this wants to be turnoff ||= mobile, stationary once we know what those are.  arrays?  hashes?
        #$turnoff ||= {mobile,stationary}

        if ((self.GetState('Default') == modestr) and (t['totalkeys'] == 0)):

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
            curfile = profile.GetBindFile(pathbo)
            self.sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

            self.sodUpKey     (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodDownKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodForwardKey(t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodBackKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodLeftKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodRightKey  (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)

            if (modestr == "Base") : makeBaseModeKey(profile,t,"r",curfile,turnoff,fix)

            t['ini'] = '-down$$'

            if (self.GetState('Default') == "Fly"):

                if (self.GetState('NonSoD')):
                    t['FlyMode'] = t['NonSoDMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                elif (self.GetState('Base')):
                    t['FlyMode'] = t['BaseMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                elif (t['canss']):
                    t['FlyMode'] = t['RunMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                elif (t['canjmp']):
                    t['FlyMode'] = t['JumpMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                elif (self.GetState('Temp') and self.GetState('TempEnable')):
                    t['FlyMode'] = t['TempMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                else:
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)

            t['ini'] = ''
            if   (modestr == "GFly") : makeGFlyModeKey  (profile,t,"gbo",curfile,turnoff,fix)
            elif (modestr == "Run")  : makeSpeedModeKey (profile,t,"s",  curfile,turnoff,fix)
            elif (modestr == "Jump") : makeJumpModeKey  (profile,t,"j",  curfile,turnoff,path)

            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)

            self.sodFollowKey(t,blf,curfile,mobile)

            # curfile = profile.GetBindFile(pathsd)

            self.sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

            self.sodUpKey     (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodDownKey   (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodForwardKey(t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodBackKey   (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodLeftKey   (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
            self.sodRightKey  (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)

            t['ini'] = '-down$$'
            if   (modestr == "Base") : makeBaseModeKey(profile,t,"r",  curfile,turnoff,fix)
            elif (modestr == "Fly")  : makeFlyModeKey( profile,t,"a",  curfile,turnoff,fix)
            elif (modestr == "GFly") : makeGFlyModeKey(profile,t,"gbo",curfile,turnoff,fix)
            t['ini'] = ''
            if   (modestr == "Jump") : makeJumpModeKey(profile,t,"j",  curfile,turnoff,path)

            sodAutoRunKey(t,bla,curfile,mobile,sssj)
            sodFollowKey(t,blf,curfile,mobile)

        curfile = profile.GetBindFile(path)

        self.sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

        self.sodUpKey     (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodDownKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodForwardKey(t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodBackKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodLeftKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodRightKey  (t,bl,curfile,mobile,stationary,flight,'','','',sssj)

        if ((flight == "Fly") and pathbo):
            #  Base to set down
            if   (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"r",curfile,{mobile,stationary},sodSetDownFix)
            elif (modestr == "Base")  : makeBaseModeKey  (profile,t,"r",curfile,turnoff,sodSetDownFix)

            if (t['BaseMode']):
                curfile.SetBind(t['BaseMode'], "Base Mode", "Speed On Demand",
                                "+down$$down 1" + actPower_name(None,1,mobile) + t['detailhi'] + t['runcamdist'] + t['blsd'])

            if   (modestr == "Run")    : makeSpeedModeKey (profile,t,"s", curfile,turnoff,sodSetDownFix)
            elif (modestr == "Fly")    : makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)
            elif (modestr == "Jump")   : makeJumpModeKey  (profile,t,"j", curfile,turnoff,path)
            elif (modestr == "Temp")   : makeTempModeKey  (profile,t,"r", curfile,turnoff,path)
            elif (modestr == "QFly")   : makeQFlyModeKey  (profile,t,"r", curfile,turnoff,modestr)
        else:
            if   (modestr == "NonSoD") : makeNonSoDModeKey(profile,t,"r", curfile,{mobile,stationary})
            elif (modestr == "Base")   : makeBaseModeKey  (profile,t,"r", curfile,turnoff,fix)
            elif (flight == "Jump"):
                if (modestr == "Fly"): makeFlyModeKey   (profile,t,"a", curfile,turnoff,fix,None,1)
            else:
                if (modestr == "Fly"): makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)

            if   (modestr == "Run")   : makeSpeedModeKey  (profile,t,"s", curfile,turnoff,fix)
            elif (modestr == "Jump")  : makeJumpModeKey   (profile,t,"j", curfile,turnoff,path)
            elif (modestr == "Temp")  : makeTempModeKey   (profile,t,"r", curfile,turnoff,path)
            elif (modestr == "QFly")  : makeQFlyModeKey   (profile,t,"r", curfile,turnoff,modestr)

        sodAutoRunKey(t,bla,curfile,mobile,sssj)

        sodFollowKey(t,blf,curfile,mobile)

    # AutoRun Binds
        curfile = profile.GetBindFile(pathr)

        sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

        sodUpKey     (t,bla,curfile,mobile,stationary,flight,1,'','',sssj)
        sodDownKey   (t,bla,curfile,mobile,stationary,flight,1,'','',sssj)
        sodForwardKey(t,bla,curfile,mobile,stationary,flight,bl, '','',sssj)
        sodBackKey   (t,bla,curfile,mobile,stationary,flight,bl, '','',sssj)
        sodLeftKey   (t,bla,curfile,mobile,stationary,flight,1,'','',sssj)
        sodRightKey  (t,bla,curfile,mobile,stationary,flight,1,'','',sssj)

        if ((flight == "Fly") and pathbo):
            if   (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"ar",curfile,{mobile,stationary},sodSetDownFix)
            elif (modestr == "Base")  : makeBaseModeKey  (profile,t,"gr",curfile,turnoff,sodSetDownFix)
            elif (modestr == "Run")   : makeSpeedModeKey (profile,t,"as",curfile,turnoff,sodSetDownFix)
        else:
            if   (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"ar",curfile,{mobile,stationary})
            elif (modestr == "Base")  : makeBaseModeKey  (profile,t,"gr",curfile,turnoff,fix)
            elif (modestr == "Run")   : makeSpeedModeKey (profile,t,"as",curfile,turnoff,fix)

        if   (modestr == "Fly")       : makeFlyModeKey   (profile,t,"af",curfile,turnoff,fix)
        elif (modestr == "Jump")      : makeJumpModeKey  (profile,t,"aj",curfile,turnoff,pathr)
        elif (modestr == "Temp")      : makeTempModeKey  (profile,t,"ar",curfile,turnoff,path)
        elif (modestr == "QFly")      : makeQFlyModeKey  (profile,t,"ar",curfile,turnoff,modestr)

        sodAutoRunOffKey(t,bl,curfile,mobile,stationary,flight)

        curfile.SetBind(self.GetState('Follow'),'Follow','Speed On Demand','nop')

        # FollowRun Binds
        curfile = profile.GetBindFile(pathf)

        sodResetKey(curfile,profile,path,self.actPower_toggle(None,1,stationary,mobile),'')

        sodUpKey     (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        sodDownKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        sodForwardKey(t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        sodBackKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        sodLeftKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        sodRightKey  (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)

        if ((flight == "Fly") and pathbo):
            if   (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"fr",curfile,{mobile,stationary},sodSetDownFix)
            elif (modestr == "Base")  : makeBaseModeKey  (profile,t,"fr",curfile,turnoff,sodSetDownFix)
            elif (modestr == "Run")   : makeSpeedModeKey (profile,t,"fs",curfile,turnoff,sodSetDownFix)
        else:
            if   (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"fr",curfile,{mobile,stationary})
            elif (modestr == "Base")  : makeBaseModeKey  (profile,t,"fr",curfile,turnoff,fix)
            elif (modestr == "Run")   : makeSpeedModeKey (profile,t,"fs",curfile,turnoff,fix)

        if   (modestr == "Fly")       : makeFlyModeKey   (profile,t,"ff",curfile,turnoff,fix)
        elif (modestr == "Jump")      : makeJumpModeKey  (profile,t,"fj",curfile,turnoff,pathf)
        elif (modestr == "Temp")      : makeTempModeKey  (profile,t,"fr",curfile,turnoff,path)
        elif (modestr == "QFly")      : makeQFlyModeKey  (profile,t,"fr",curfile,turnoff,modestr)

        curfile.SetBind(self.GetState('AutoRun'),'Auto Run','Speed On Demand','nop')

        sodFollowOffKey(t,bl,curfile,mobile,stationary,flight)



    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeNonSoDModeKey(self, p, t, bl, cur, toff, fix, fb):
        key = t['NonSoDMode']
        if (not key or (key == 'UNBOUND')): return

        if p['SoD']['Feedback']: feedback = (fb or '$$t $name, Non-SoD Mode')
        else:                    feedback = ''

        if t['ini'] == None: t['ini'] = ''

        if (bl == "r"):
            bindload = t['bl']('n')
            if (fix):
                fix(p,t,key, makeNonSoDModeKey,"n",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, "Non-SoD Mode", "Speed On Demand",
                            t['ini'] + self.actPower_toggle(None,1,None,toff) + t +dirs('UDFBLR') + t['detailhi'] + t['runcamdist'] + feedback + bindload)

        elif (bl == "ar"):
            bindload = t['bl']('an')
            if (fix):
                fix(p,t,key, makeNonSoDModeKey,"n",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, "Non-SoD Mode", "Speed On Demand",
                            t['ini'] + self.actPower_toggle(None,1,None,toff) + t['detailhi'] + t['runcamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, makeNonSoDModeKey,"n",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, "Non-SoD Mode", "Speed On Demand",
                            t['ini'] + self.actPower_toggle(None,1,None,toff) + t['detailhi'] + t['runcamdist'] + '$$up 0' + feedback + t['bl']('fn'))
        t['ini'] = ''

    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeTempModeKey(self, p, t, bl, cur, toff):
        key = t['TempMode']
        if (not key or (key == "UNBOUND")): return

        if p['SoD']['Feedback']: feedback = '$$t $name, Temp Mode'
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''
        trayslot = "1 p['SoD']['TempTray']"

        if (bl == "r"):
            bindload = t['bl']('t')
            cur.SetBind(key, "Temp Mode", "Speed On Demand",
                        t['ini'] + actPower(None,1,trayslot,toff) + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)
        elif (bl == "ar"):
            bindload  = t['bl']('at')
            bindload2 = t['bl']('at','_t')
            tgl = p.GetBindFile(bindload2)
            cur.SetBind(key, "Temp Mode", "Speed On Demand",
                        t['in'] + actPower(None,1,trayslot,toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload2)
            tgl.SetBind(key, "Temp Mode", "Speed On Demand",
                        t['in'] + actPower(None,1,trayslot,toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload)
        else:
            cur.SetBind(key, "Temp Mode", "Speed On Demand",
                        t['ini'] + actPower(None,1,trayslot,toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + feedback + t['bl']('ft'))

        t['ini'] = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeQFlyModeKey(self, p, t, bl, cur, toff, modestr):
        key = t['QFlyMode']
        if (not key or key == "UNBOUND"): return

        if (modestr == "NonSoD"):
            cur.SetBind(key, "Quantum Flight", "Speed On Demand", "powexecname Quantum Flight")
            return

        if p['SoD']['Feedback']: feedback = '$$t $name, QFlight Mode'
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''

        if (bl == "r"):
            bindload  = t['bl']('n')
            bindload2 = t['bl']('n'+'_q')
            tgl = p.GetBindFile(bindload2)

            if (modestr == 'Nova' or modestr == 'Dwarf'): tray = '$$gototray 1'
            else:                                         tray = ''

            cur.SetBind(key, "Quantum Flight", "Speed On Demand",
                        t['ini'] + actPower(None,1,'Quantum Flight', toff) + tray + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload2)
            tgl.SetBind(key, "Quantum Flight", "Speed On Demand",
                        t['ini'] + actPower(None,1,'Quantum Flight', toff) + tray + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t['bl']('an')
            bindload2 = t['bl']('an','_t')
            tgl = p.GetBindFile(bindload2)
            cur.SetBind(key, "Quantum Flight", "Speed On Demand",
                        t['in'] + actPower(None,1,'Quantum Flight', toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload2)
            tgl.SetBind(key, "Quantum Flight", "Speed On Demand",
                        t['in'] + actPower(None,1,'Quantum Flight', toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload)
        else:
            cur.SetBind(key, "Quantum Flight", "Speed On Demand",
                        t['ini'] + actPower(None,1,'Quantum Flight', toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + feedback + t['bl']('fn'))

        t['ini'] = ''

    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeBaseModeKey(self, p, t, bl, cur, toff, fix, fb):
        key = t['BaseMode']
        if (not key or key == "UNBOUND"): return

        if p['SoD']['Feedback']: feedback = (fb or '$$t $name, Sprint-SoD Mode')
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''

        if (bl == "r"):
            bindload  = t['bl']()

            if t['horizkeys']: sprint = t['sprint']
            else:              sprint = ''
            ton = self.actPower_toggle(1, 1, sprint, toff)

            if (fix):
                fix(p,t,key, makeBaseModeKey,"r",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, "Base Mode", "Speed On Demand",
                            t['ini'] + ton + t.dirs('UDFBLR') + t['detailhi'] + t['runcamdist'] + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t['bl']('gr')

            if (fix):
                fix(p,t,key, makeBaseModeKey,"r",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, "Base Mode", "Speed On Demand",
                            t['ini'] + self.actPower_toggle(1,1,t['sprint'],toff) + t['detailhi'] +  t['runcamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, makeBaseModeKey,"r",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, "Base Mode", "Speed On Demand",
                            t['ini'] + self.actPower_toggle(1,1,t['sprint'], toff) + t['detailhi'] + t['runcamdist'] + '$$up 0' + fb + t['bl']('fr'))

        t['ini'] = ''

    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeSpeedModeKey(self, p, t, bl, cur, toff, fix, fb):
        key = t['RunMode']

        if p['SoD']['Feedback']: feedback = (fb or '$$t $name, Superspeed Mode')
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''

        if (t['canss']):
            if (bl == 's'):
                bindload = t['bl']('s')
                if (fix):
                    fix(p,t,key,makeSpeedModeKey,"s",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(key, "Speed Mode", "Speed On Demand",
                                t['ini'] + self.actPower_toggle(1,1,t['speed'],toff) + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

            elif (bl == "as"):
                bindload = t['bl']('as')
                if (fix):
                    fix(p,t,key,makeSpeedModeKey,"s",bl,cur,toff,"a",feedback)
                elif (not feedback):
                    cur.SetBind(key, "Speed Mode", "Speed On Demand",
                                t['ini'] + self.actPower_toggle(1,1,t['speed'],toff) + t.dirs('UDLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)
                else:
                    bindload  = t['bl']('as')
                    bindload2 = t['bl']('as','_s')
                    tgl = p.GetBindFile(bindload2)
                    cur.SetBind(key, "Speed Mode", "Speed On Demand",
                                t['ini'] + self.actPower_toggle(1,1,t['speed'],toff) + t.dirs('UDLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload2)
                    tgl.SetBind(key, "Speed Mode", "Speed On Demand",
                                t['ini'] + self.actPower_toggle(1,1,t['speed'],toff) + t.dirs('UDLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

            else:
                if (fix):
                    fix(p,t,key,makeSpeedModeKey,"s",bl,cur,toff,"f",feedback)
                else:
                    cur.SetBind(key, "Speed Mode", "Speed On Demand",
                                t['ini'] + self.actPower_toggle(1,1,t['speed'],toff) + '$$up 0' +  t['detaillo'] + t['flycamdist'] + feedback + t['bl']('fs'))




        t['ini'] = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeJumpModeKey(self, p, t, bl, cur, toff, fbl):
        key = t['JumpMode']
        if (t['canjmp'] and not p['SoD']['JumpSimple']):

            if p['SoD']['Feedback']: feedback = '$$t $name, Superjump Mode'
            else:                    feedback = ''
            tgl = p.GetBindFile(fbl)

            if (bl == "j"):
                if (t['horizkeys'] + t['space'] > 0):
                    a = actPower(None,1,t['jump'],toff) + '$$up 1'
                else:
                    a = actPower(None,1,t['cjmp'],toff)

                bindload = t['bl']('j')
                tgl.SetBind(key, "Jump Mode", "Speed On Demand", '-down' + a + t['detaillo'] + t['flycamdist'] + bindload)
                cur.SetBind(key, "Jump Mode", "Speed On Demand", '+down' + feedback + BindFile.BLF(p, fbl))
            elif (bl == "aj"):
                bindload = t['bl']('aj')
                tgl.SetBind(key, "Jump Mode", "Speed On Demand", '-down' + actPower(None,1,t['jump'],toff) + '$$up 1' + t['detaillo'] + t['flycamdist'] + t.dirs('DLR') + bindload)
                cur.SetBind(key, "Jump Mode", "Speed On Demand", '+down' + feedback + BindFile.BLF(p, fbl))
            else:
                tgl.SetBind(key, "Jump Mode", "Speed On Demand", '-down' + actPower(None,1,t['jump'],toff) + '$$up 1' + t['detaillo'] + t['flycamdist'] + t['bl']('fj'))
                cur.SetBind(key, "Jump Mode", "Speed On Demand", '+down' + feedback + BindFile.BLF(p, fbl))


        t['ini'] = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeFlyModeKey(self, p, t, bl, cur, toff, fix, fb, fb_on_a):
        key = t['FlyMode']
        if (not key or key == "UNBOUND"): return

        if p['SoD']['Feedback']: feedback = (fb or '$$t $name, Flight Mode')
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''

        if (t['canhov'] + t['canfly'] > 0):
            if (bl == "bo"):
                bindload = t['bl']('bo')
                if (fix):
                    fix(p,t,key,makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(key, "Fly Mode", "Speed On Demand", '+down$$' + self.actPower_toggle(1,1,t['flyx'],toff) + '$$up 1$$down 0' + t.dirs('FBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

            elif (bl == "a"):
                if (not fb_on_a): feedback = ''
                bindload = t['bl']('a')

                if t['tkeys']: ton = t['flyx']
                else:          ton = t['hover']

                if (fix):
                    fix(p,t,key,makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(t['FlyMode'],  "Fly Mode", "Speed On Demand", t['ini'] + self.actPower_toggle(1,1, ton ,toff) + t.dirs('UDLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

            elif (bl == "af"):
                bindload = t['bl']('af')
                if (fix):
                    fix(p,t,key,makeFlyModeKey,"f",bl,cur,toff,"a",feedback)
                else:
                    cur.SetBind(key,  "Fly Mode", "Speed On Demand", t['ini'] + self.actPower_toggle(1,1,t['flyx'],toff) + t['detaillo'] + t['flycamdist'] + t.dirs('DLR') + feedback + bindload)

            else:
                if (fix):
                    fix(p,t,key,makeFlyModeKey,"f",bl,cur,toff,"f",feedback)
                else:
                    cur.SetBind(key,  "Fly Mode", "Speed On Demand", t['ini'] + self.actPower_toggle(1,1,t['flyx'],toff) + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + t['bl']('ff'))

        t['ini'] = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeGFlyModeKey(self, p, t, bl, cur, toff, fix):
        key = t['GFlyMode']

        if not t['ini']: t['ini'] = ''

        if (t['cangfly'] > 0):
            if (bl == "gbo"):
                bindload = t['bl']('gbo')
                if (fix):
                    fix(p,t,key,makeGFlyModeKey,"gf",bl,cur,toff,'','')
                else:
                    cur.SetBind(key, "Group Fly Mode", "Speed On Demand", t['ini'] + '$$up 1$$down 0' + self.actPower_toggle(None,1,t['gfly'],toff) + t.dirs('FBLR') + t['detaillo'] + t['flycamdist'] .bindload)

            elif (bl == "gaf"):
                bindload = t['bl']('gaf')
                if (fix):
                    fix(p,t,key,makeGFlyModeKey,"gf",bl,cur,toff,"a")
                else:
                    cur.SetBind(key, "Group Fly Mode", "Speed On Demand", t['ini'] + t['detaillo'] + t['flycamdist'] + t.dirs('UDLR') + bindload)

            else:
                if (fix):
                    fix(p,t,key,makeGFlyModeKey,"gf",bl,cur,toff,"f")
                else:
                    if (bl == "gf"):
                        cur.SetBind(key, "Group Fly Mode", "Speed On Demand", t['ini'] + self.actPower_toggle(1,1,t['gfly'],toff) + t['detaillo'] + t['flycamdist'] + t['bl']('gff'))
                    else:
                        cur.SetBind(key, "Group Fly Mode", "Speed On Demand", t['ini'] + t['detaillo'] + t['flycamdist'] + t['bl']('gff'))




        t['ini'] = ''


    def PopulateBindFiles(self):


        ### TODO
        sssj = 0
        ### TODO

        profile = self.Profile

        ResetFile = profile.ResetFile()

        # ResetFile.SetBind(petselect['sel5'] + ' "petselect 5')
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


        t = tObject({
            'profile'    : profile,
            'sprint'     : '',
            'speed'      : '',
            'hover'      : '',
            'fly'        : '',
            'flyx'       : '',
            'jump'       : '',
            'cjmp'       : '',
            'canhov'     : 0,
            'canfly'     : 0,
            'canqfly'    : 0,
            'cangfly'    : 0,
            'cancj'      : 0,
            'canjmp'     : 0,
            'canss'      : 0,
            'tphover'    : '',
            'ttpgrpfly'  : '',
            'on'         : '$$powexectoggleon ',
            # 'on'       : '$$powexecname ',
            'off'        : '$$powexectoggleoff ',
            'mlon'       : '',
            'mloff'      : '',
            'runcamdist' : '',
            'flycamdist' : '',
            'detailhi'   : '',
            'detaillo'   : '',
            'RunMode'    : '',
        })

        if (self.GetState('JumpCJ') and not self.GetState('JumpSJ')):
            t['cancj'] = 1
            t['cjmp'] = "Combat Jumping"
            t['jump'] = "Combat Jumping"

        if (not self.GetState('JumpCJ') and self.GetState('JumpSJ')):
            t['canjmp'] = 1
            t['jump'] = "Super Jump"
            t['jumpifnocj'] = "Super Jump"

            t['cancj'] = 1
            t['canjmp'] = 1
            t['cjmp'] = "Combat Jumping"
            t['jump'] = "Super Jump"


        if (profile.General.GetState('Archetype') == "Peacebringer"):
            if (self.GetState('FlyHover')):
                t['canhov'] = 1
                t['canfly'] = 1
                t['hover'] = "Combat Flight"
                t['fly'] = "Energy Flight"
                t['flyx'] = "Energy Flight"
            else:
                t['canfly'] = 1
                t['hover'] = "Energy Flight"
                t['flyx'] = "Energy Flight"

        elif (not (profile.General.GetState('Archetype') == "Warshade")):
            if (self.GetState('FlyHover') and not self.GetState('FlyFly')):
                t['canhov'] = 1
                t['hover'] = "Hover"
                t['flyx'] = "Hover"
                if (self.GetState('TPTPHover')): t['tphover'] = '$$powexectoggleon Hover'

            if (not self.GetState('FlyHover') and self.GetState('FlyFly')):
                t['canfly'] = 1
                t['hover'] = "Fly"
                t['flyx'] = "Fly"

            if (self.GetState('FlyHover') and self.GetState('FlyFly')):
                t['canhov'] = 1
                t['canfly'] = 1
                t['hover'] = "Hover"
                t['fly'] = "Fly"
                t['flyx'] = "Fly"
                if (self.GetState('TPTPHover')): t['tphover'] = '$$powexectoggleon Hover'


        if ((profile.General.GetState('Archetype') == "Peacebringer") and self.GetState('FlyQFly')):
            t['canqfly'] = 1

        if (self.GetState('FlyGFly')):
            t['cangfly'] = 1
            t['gfly'] = "Group Fly"
            if (self.GetState('TTPTPGFly')): t['ttpgfly'] = '$$powexectoggleon Group Fly'

        if (self.GetState('RunPrimaryNumber') == 1):
            t['sprint'] = self.GetState('RunSecondary')
            t['speed']  = self.GetState('RunSecondary')
        else:
            t['sprint'] = self.GetState('RunSecondary')
            t['speed']  = self.GetState('RunPrimary')
            t['canss'] = 1

        if self.GetState('Unqueue') : t['unqueue'] = '$$powexecunqueue'
        else:                      t['unqueue'] = ''
        if (self.GetState('AutoMouseLook')):
            t['mlon']  = '$$mouselook 1'
            t['mloff'] = '$$mouselook 0'

        if (self.GetState('RunUseCamdist')):
            t['runcamdist'] = '$$camdist ' + self.GetState('RunCamdist')

        if (self.GetState('FlyUseCamdist')):
            t['flycamdist'] = '$$camdist ' + self.GetState('FlyCamdist')

        if (self.GetState('Detail') and self.GetState('DetailEnable')):
            t['detailhi'] = '$$visscale ' + self.GetState('DetailNormalAmt') + '$$shadowvol 0$$ss 0'
            t['detaillo'] = '$$visscale ' + self.GetState('DetailMovingAmt') + '$$shadowvol 0$$ss 0'


        if self.GetState('TPHideWindows'):
            windowhide = '$$windowhide health$$windowhide chat$$windowhide target$$windowhide tray'
            windowshow = '$$show health$$show chat$$show target$$show tray'
        else:
            windowhide = ''
            windowshow = ''

        # turn = "+zoomin$$-zoomin"  # a non functioning bind used only to activate the keydown/keyup functions of +commands
        t['turn'] = "+down";  # a non functioning bind used only to activate the keydown/keyup functions of +commands

        #  temporarily set self.GetState('Default') to "NonSoD"
        # self.SetState('Default', "Base")
        #  set up the keys to be used.
        if (self.GetState('Default') == "NonSoD") : t['NonSoDMode'] = self.GetState('NonSoDMode')
        if (self.GetState('Default') == "Base")   : t['BaseMode'] = self.GetState('BaseMode')
        if (self.GetState('Default') == "Fly")    : t['FlyMode'] = self.GetState('FlyMode')
        if (self.GetState('Default') == "Jump")   : t['JumpMode'] = self.GetState('JumpMode')
        if (self.GetState('Default') == "Run")    : t['RunMode'] = self.GetState('RunMode')
    #     if (self.GetState('Default') == "GFly")  : t['GFlyMode'] = self.GetState('GFlyMode')
        t['TempMode'] = self.GetState('TempMode')
        t['QFlyMode'] = self.GetState('QFlyMode')

        for space in (0,1):
            t['space'] = space
            t['up']  = f'$$up {space}'
            t['upx'] = f'$$up {1-space}'

            for X in (0,1):
                t['X'] = X
                t['dow']  = f'$$down {X}'
                t['dowx'] = f'$$down {1-X}'

                for W in (0,1):
                    t['W'] = W
                    t['forw'] = f'$$forward {W}'
                    t['forx'] = f'$$forward {1-W}'

                    for S in (0,1):
                        t['S'] = S
                        t['bac']  = f'$$backward {S}'
                        t['bacx'] = f'$$backward {1-S}'

                        for A in (0,1):
                            t['A'] = A
                            t['lef']  = f'$$left {A}'
                            t['lefx'] = f'$$left {1-A}'

                            for D in (0,1):
                                t['D'] = D
                                t['rig']  = '$$right {D}'
                                t['rigx'] = '$$right {1-D}'

                                t['totalkeys'] = space+X+W+S+A+D;    # total number of keys down
                                t['horizkeys'] = W+S+A+D;    # total # of horizontal move keys.    So Sprint isn't turned on when jumping
                                t['vertkeys'] = space+X
                                t['jkeys'] = t['horizkeys']+t['space']
                                if (self.GetState('NonSoD') or t['canqfly']):
                                    t[self.GetState('Default') + "Mode"] = t['NonSoDMode']
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 'n',
                                        'bla' : 'an',
                                        'blf' : 'fn',
                                        'path' : 'n',
                                        'pathr' : 'an',
                                        'pathf' : 'fn',
                                        'mobile' : '',
                                        'stationary' : '',
                                        'modestr' : "NonSoD",
                                    })
                                    t[self.GetState('Default') + "Mode"] = None

                                if (self.GetState('Base')):
                                    t[self.GetState('Default') + "Mode"] = t['BaseMode']
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 'r',
                                        'bla' : 'gr',
                                        'blf' : 'fr',
                                        'path' : 'r',
                                        'pathr' : 'ar',
                                        'pathf' : 'fr',
                                        'mobile' : t['sprint'],
                                        'stationary' : '',
                                        'modestr' : "Base",
                                    })
                                    t[self.GetState('Default') + "Mode"] = None

                                if (t['canss']):
                                    t[self.GetState('Default') + "Mode"] = t['RunMode']
                                    if (self.GetState('SSSSSJModeEnable')): sssj = t['jump']
                                    if (self.GetState('SSMobileOnly')):
                                        self.makeSoDFile({
                                            't' : t,
                                            'bl' : 's',
                                            'bla' : 'as',
                                            'blf' : 'fs',
                                            'path' : 's',
                                            'pathr' : 'as',
                                            'pathf' : 'fs',
                                            'mobile' : t['speed'],
                                            'stationary' : '',
                                            'modestr' : "Run",
                                            'sssj' : sssj,
                                        })
                                    else:
                                        self.makeSoDFile({
                                            't' : t,
                                            'bl' : 's',
                                            'bla' : 'as',
                                            'blbo' : None,
                                            'blf' : 'fs',
                                            'blsd' : None,
                                            'path' : 's',
                                            'pathbo': None,
                                            'pathr' : 'as',
                                            'pathsd': None,
                                            'pathf' : 'fs',
                                            'mobile' : t['speed'],
                                            'stationary' : t['speed'],
                                            'modestr' : "Run",
                                            'sssj' : sssj,
                                        })

                                    t[self.GetState('Default') + "Mode"] = None

                                if (t['canjmp']>0 and not (self.GetState('JumpSimple'))):
                                    t[self.GetState('Default') + "Mode"] = t['JumpMode']
                                    if (t['jump'] == t['cjmp']): jturnoff = t['jumpifnocj']
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 'j',
                                        'bla' : 'aj',
                                        'blf' : 'fj',
                                        'path' : 'j',
                                        'pathr' : 'aj',
                                        'pathf' : 'fj',
                                        'mobile' : t['jump'],
                                        'stationary' : t['cjmp'],
                                        'modestr' : "Jump",
                                        'flight' : "Jump",
                                        'fix' : sodJumpFix,
                                        'turnoff' : jturnoff,
                                    })
                                    t[self.GetState('Default') + "Mode"] = None

                                if (t['canhov']+t['canfly']>0):
                                    t[self.GetState('Default') + "Mode"] = t['FlyMode']
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 'r',
                                        'bla' : 'af',
                                        'blf' : 'ff',
                                        'path' : 'r',
                                        'pathr' : 'af',
                                        'pathf' : 'ff',
                                        'mobile' : t['flyx'],
                                        'stationary' : t['hover'],
                                        'modestr' : "Fly",
                                        'flight' : "Fly",
                                        'pathbo' : 'bo',
                                        'pathsd' : 'sd',
                                        'blbo' : 'bo',
                                        'blsd' : 'sd',
                                    })
                                    t[self.GetState('Default') + "Mode"] = None

                                if (t['canqfly']>0):
                                    t[self.GetState('Default') + "Mode"] = t['QFlyMode']
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 'q',
                                        'bla' : 'aq',
                                        'blf' : 'fq',
                                        'path' : 'q',
                                        'pathr' : 'aq',
                                        'pathf' : 'fq',
                                        'mobile' : "Quantum Flight",
                                        'stationary' : "Quantum Flight",
                                        'modestr' : "QFly",
                                        'flight' : "Fly",
                                    })
                                    t[self.GetState('Default') + "Mode"] = None

                                if (t['cangfly']):
                                    t[self.GetState('Default') + "Mode"] = t['GFlyMode']
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 'a',
                                        'bla' : 'af',
                                        'blf' : 'ff',
                                        'path' : 'ga',
                                        'pathr' : 'gaf',
                                        'pathf' : 'gff',
                                        'mobile' : t['gfly'],
                                        'stationary' : t['gfly'],
                                        'modestr' : "GFly",
                                        'flight' : "GFly",
                                        'pathbo' : 'gbo',
                                        'pathsd' : 'gsd',
                                        'blbo' : 'gbo',
                                        'blsd' : 'gsd',
                                    })
                                    t[self.GetState('Default') + "Mode"] = None

                                if (self.GetState('Temp') and self.GetState('TempEnable')):
                                    trayslot = "1 " + self.GetState('TempTray')
                                    t[self.GetState('Default') + "Mode"] = t['TempMode']
                                    self.makeSoDFile({
                                        't' : t,
                                        'bl' : 't',
                                        'bla' : 'at',
                                        'blf' : 'ft',
                                        'path' : 't',
                                        'pathr' : 'at',
                                        'pathf' : 'ft',
                                        'mobile' : trayslot,
                                        'stationary' : trayslot,
                                        'modestr' : "Temp",
                                        'flight' : "Fly",
                                    })
                                    t[self.GetState('Default') + "Mode"] = None


        t['space'] = t['X'] = t['W'] = t['S'] = t['A'] = t['D'] = 0

        t['up']   = '$$up '       +    t['space']
        t['upx']  = '$$up '       + (1-t['space'])
        t['dow']  = '$$down '     +    t['X']
        t['dowx'] = '$$down '     + (1-t['X'])
        t['forw'] = '$$forward '  +    t['W']
        t['forx'] = '$$forward '  + (1-t['W'])
        t['bac']  = '$$backward ' +    t['S']
        t['bacx'] = '$$backward ' + (1-t['S'])
        t['lef']  = '$$left '     +    t['A']
        t['lefx'] = '$$left '     + (1-t['A'])
        t['rig']  = '$$right '    +    t['D']
        t['rigx'] = '$$right '    + (1-t['D'])

        if (self.GetState('TLeft')  and self.GetState('TLeft')  == "UNBOUND"):
            ResetFile.SetBind(self.GetState('TLeft'), "Turn Left", "Speed On Demand", "+turnleft")
        if (self.GetState('TRight') and self.GetState('TRight') == "UNBOUND"):
            ResetFile.SetBind(self.GetState('TRight'), "Turn Right", "Speed On Demand", "+turnright")

        if (self.GetState('Temp') and self.GetState('TempEnable')):
            temptogglefile1 = profile.GetBindFile("temptoggle1.txt")
            temptogglefile2 = profile.GetBindFile("temptoggle2.txt")
            temptogglefile2.SetBind(self.GetState('TempTraySwitch'), "Toggle Temp", "Speed On Demand", '-down$$gototray 1'                         + BindFile.BLF(profile, 'temptoggle1.txt'))
            temptogglefile1.SetBind(self.GetState('TempTraySwitch'), "Toggle Temp", "Speed On Demand", '+down$$gototray ' + self.GetState('TempTray') + BindFile.BLF(profile, 'temptoggle2.txt'))
            ResetFile.      SetBind(self.GetState('TempTraySwitch'), "Toggle Temp", "Speed On Demand", '+down$$gototray ' + self.GetState('TempTray') + BindFile.BLF(profile, 'temptoggle2.txt'))


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
                ResetFile.SetBind(humanBindKey, "Human Mode", "Speed On Demand", humanpbind)

        #  kheldian form support
        #  create the Nova and Dwarf form support files if enabled.
        Nova  = self.GetState('Nova')
        Dwarf = self.GetState('Dwarf')

        fullstop = '$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'

        if (Nova and Nova['Enable']):
            ResetFile.SetBind(Nova['Mode'], "Nova Mode", "Speed On Demand",
                              f"t $name, Changing to {Nova['Nova']} Form{fullstop}{t['on']}{Nova['Nova']}$$gototray {Nova['Tray']}" + BindFile.BLF(profile, 'nova.txt'))

            novafile = profile.GetBindFile("nova.txt")

            if (Dwarf and Dwarf['Enable']):
                novafile.SetBind(Dwarf['Mode'], "Dwarf Mode", "Speed On Demand",
                                 f"t $name, Changing to {Dwarf['Dwarf']} Form{fullstop}{t['off']}{Nova['Nova']}{t['on']}{Dwarf['Dwarf']}$$gototray {Dwarf['Tray']}" + BindFile.BLF(profile, 'dwarf.txt'))

            if not humanBindKey:
                humanBindKey = Nova['Mode']

            if self.GetState('UseHumanFormPower'): humpower = '$$powexectoggleon ' + self.GetState('HumanFormShield')
            else:                               humpower = ''

            novafile.SetBind(humanBindKey, "Human Mode", "Speed On Demand",
                             f"t $name, Changing to Human Form, SoD Mode{fullstop}$$powexectoggleoff {Nova['Nova']} {humpower} $$gototray 1" + BindFile.BLF(profile, 'reset.txt'))

            if (humanBindKey == Nova['Mode']): humanBindKey = None

            if novapbind: novafile.SetBind(Nova['Mode'], "Nova Mode", "Speed On Demand", novapbind)

            if t['canqfly']: makeQFlyModeKey(profile,t,"r",novafile,Nova['Nova'],"Nova")

            novafile.SetBind(self.GetState('Forward'),"Forward", "Speed On Demand","+forward")
            novafile.SetBind(self.GetState('Left'), "Left", "Speed On Demand", "+left")
            novafile.SetBind(self.GetState('Right'), "Right", "Speed On Demand","+right")
            novafile.SetBind(self.GetState('Back'), "Back", "Speed On Demand", "+backward")
            novafile.SetBind(self.GetState('Up'), "Up", "Speed On Demand", "+up")
            novafile.SetBind(self.GetState('Down'), "Down", "Speed On Demand", "+down")
            novafile.SetBind(self.GetState('AutoRun'), "Auto Run", "Speed On Demand", "++forward")
            novafile.SetBind(self.GetState('FlyMode'),'nop')
            if (self.GetState('FlyMode') != self.GetState('RunMode')):
                novafile.SetBind(self.GetState('RunMode'), "Run Mode", "Speed On Demand", 'nop')
            if (self.GetState('MouseChord')):
                novafile.SetBind('mousechord', "Mouse Chord", "Speed On Demand", "+down$$+forward")

            if (self.GetState('TP') and self.GetState('TPEnable')):
                novafile.SetBind(self.GetState('TPComboKey'), "TP Combo Key", "Speed On Demand", 'nop')
                novafile.SetBind(self.GetState('TPBindKey'),  "TP Bind Key", "Speed On Demand", 'nop')
                novafile.SetBind(self.GetState('TPResetKey'), "TP Reset Key", "Speed On Demand", 'nop')

            novafile.SetBind(self.GetState('Follow'),"Follow", "Speed On Demand", "follow")
            # novafile.SetBind(self.GetState('ToggleKey'),'t $name, Changing to Human Form, Normal Mode$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0$$powexectoggleoff ' + Nova['Nova'] + '$$gototray 1' + BindFile.BLF(profile, 'reset.txt'))


        if (Dwarf and Dwarf['Enable']):
            ResetFile.SetBind(Dwarf['Mode'], "Dwarf Mode", "Speed On Demand",
                              f"t $name, Changing to {Dwarf['Dwarf']} Form{fullstop}$$powexectoggleon {Dwarf['Dwarf']}$$gototray {Dwarf['Tray']}" + BindFile.BLF(profile, 'dwarf.txt'))
            dwrffile = profile.GetBindFile("dwarf.txt")
            if (Nova and Nova['Enable']):
                dwrffile.SetBind(Nova['Mode'], "Nova Mode", "Speed On Demand",
                                 f"t $name, Changing to {Nova['Nova']} Form{fullstop}$$powexectoggleoff {Dwarf['Dwarf']}$$powexectoggleon {Nova['Nova']}$$gototray {Nova['Tray']}" + BindFile.BLF(profile, 'nova.txt'))

            if not humanBindKey: humanBindKey = Dwarf['Mode']
            if self.GetState('UseHumanFormPower'): humpower = '$$powexectoggleon ' + self.GetState('HumanFormShield')
            else:                               humpower = ''

            dwrffile.SetBind(humanBindKey, "Human Mode", "Speed On Demand",
                             f"t $name, Changing to Human Form, SoD Mode{fullstop}$$powexectoggleoff {Dwarf['Dwarf']}{humpower}$$gototray 1" + BindFile.BLF(profile, 'reset.txt'))

            if dwarfpbind: dwrffile.SetBind(Dwarf['Mode'], "Dwarf Mode", "Speed On Demand", dwarfpbind)
            if t['canqfly']:
                makeQFlyModeKey(profile,t,"r",dwrffile,Dwarf['Dwarf'],"Dwarf")

            dwrffile.SetBind(self.GetState('Forward'), "Forward", "Speed On Demand","+forward")
            dwrffile.SetBind(self.GetState('Left'), "Left", "Speed On Demand", "+left")
            dwrffile.SetBind(self.GetState('Right'), "Right", "Speed On Demand", "+right")
            dwrffile.SetBind(self.GetState('Back'), "Back", "Speed On Demand", "+backward")
            dwrffile.SetBind(self.GetState('Up'), "Up", "Speed On Demand", "+up")
            dwrffile.SetBind(self.GetState('Down'), "Down", "Speed On Demand", "+down")
            dwrffile.SetBind(self.GetState('AutoRun'), "Auto Run", "Speed On Demand","++forward")
            dwrffile.SetBind(self.GetState('FlyMode'), "Fly Mode", "Speed On Demand", 'nop')
            dwrffile.SetBind(self.GetState('Follow'), "Follow", "Speed On Demand", "follow")
            if (self.GetState('FlyMode') != self.GetState('RunMode')):
                dwrffile.SetBind(self.GetState('RunMode'), "Run Mode", "Speed On Demand", 'nop')
            if (self.GetState('MouseChord')):
                dwrffile.SetBind('mousechord', "Mouse Chord", "Speed On Demand", "+down$$+forward")

            if (self.GetState('TP') and self.GetState('TPEnable')):
                dwrffile.SetBind(self.GetState('TPComboKey'), "TP Combo", "Speed On Demand",
                                 '+down$$' + dwarfTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'dtp','tp_on1.txt'))
                dwrffile.SetBind(self.GetState('TPBindKey'), "TP Bind", "Speed On Demand", 'nop')
                dwrffile.SetBind(self.GetState('TPResetKey'), "TP Reset", "Speed On Demand",
                                 substr(t['detailhi'],2) + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'dtp','tp_off.txt'))
                #  Create tp_off file
                tp_off = profile.GetBindFile("dtp","tp_off.txt")
                tp_off.SetBind(self.GetState('TPComboKey'), "TP Combo", "Speed On Demand",
                               '+down$$' + dwarfTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'dtp','tp_on1.txt'))
                tp_off.SetBind(self.GetState('TPBindKey'), "TB Bind", "Speed On Demand", 'nop')

                tp_on1 = profile.GetBindFile("dtp","tp_on1.txt")
                tp_on1.SetBind(self.GetState('TPComboKey'), "TP Combo", "Speed On Demand",
                               '-down$$powexecunqueue' + t['detailhi'] + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'dtp','tp_off.txt'))
                tp_on1.SetBind(self.GetState('TPBindKey'), "TP Bind", "Speed On Demand",
                               '+down' + BindFile.BLF(profile, 'dtp','tp_on2.txt'))

                tp_on2 = profile.GetBindFile("dtp","tp_on2.txt")
                tp_on2.SetBind(self.GetState('TPBindKey'), "TP Bind", "Speed On Demand",
                               '-down$$' + dwarfTPPower + BindFile.BLF(profile, 'dtp','tp_on1.txt'))

            dwrffile.SetBind(self.GetState('ToggleKey'), "Toggle Key", "Speed On Demand",
                             "t $name, Changing to Human Form, Normal Mode$fullstop\$\$powexectoggleoff Dwarf['Dwarf']\$\$gototray 1" + BindFile.BLF(profile, 'reset.txt'))


        if (self.GetState('JumpSimple')):
            if (self.GetState('JumpCJ') and self.GetState('JumpSJ')):
                ResetFile.SetBind(self.GetState('JumpMode'), "Jump Mode", "Speed On Demand",'powexecname Super Jump$$powexecname Combat Jumping')
            elif (self.GetState('JumpSJ')):
                ResetFile.SetBind(self.GetState('JumpMode'), "Jump Mode", "Speed On Demand",'powexecname Super Jump')
            elif (self.GetState('JumpCJ')):
                ResetFile.SetBind(self.GetState('JumpMode'), "Jump Mode", "Speed On Demand",'powexecname Combat Jumping')



        if (self.GetState('TP') and self.GetState('TPEnable') and not normalTPPower):
            ResetFile.SetBind(self.GetState('TPComboKey'), "TP Combo", "Speed On Demand", 'nop')
            ResetFile.SetBind(self.GetState('TPBindKey'),  "TP Bind", "Speed On Demand", 'nop')
            ResetFile.SetBind(self.GetState('TPResetKey'), "TP Reset", "Speed On Demand", 'nop')

        if (self.GetState('TP') and self.GetState('TPEnable') and not (profile.General.GetState('Archetype') == "Peacebringer") and normalTPPower):
            tphovermodeswitch = ''
            if (t['tphover'] == ''):
                tphovermodeswitch = re.sub('\d\d\d\d\d\d', '000000', t['bl']('r'))

            ResetFile.SetBind(self.GetState('TPComboKey'), "TP Combo", "Speed On Demand", '+down$$' + normalTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'tp','tp_on1.txt'))
            ResetFile.SetBind(self.GetState('TPBindKey') , "TP Bind", "Speed On Demand", 'nop')
            ResetFile.SetBind(self.GetState('TPResetKey'), "TP Reset", "Speed On Demand", substr(t['detailhi'],2) + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'tp','tp_off.txt') + tphovermodeswitch)
            #  Create tp_off file
            tp_off = profile.GetBindFile("tp","tp_off.txt")
            tp_off.SetBind(self.GetState('TPComboKey'), "TP Combo", "Speed On Demand",
                           '+down$$' + normalTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'tp','tp_on1.txt'))
            tp_off.SetBind(self.GetState('TPBindKey'), "TP Bind", "Speed On Demand", 'nop')

            tp_on1 = profile.GetBindFile("tp","tp_on1.txt")
            zoomin = t['detailhi'] + t['runcamdist']
            if (t['tphover']): zoomin = ''
            tp_on1.SetBind(self.GetState('TPComboKey'), "TP Combo", "Speed On Demand", '-down$$powexecunqueue' + zoomin + windowshow + BindFile.BLF(profile, 'tp','tp_off.txt') + tphovermodeswitch)
            tp_on1.SetBind(self.GetState('TPBindKey'), "TP Bind", "Speed On Demand", '+down' + t['tphover'] + BindFile.BLF(profile, 'tp','tp_on2.txt'))

            tp_on2 = profile.GetBindFile("tp","tp_on2.txt")
            tp_on2.SetBind(self.GetState('TPBindKey'), "TP Bind", "Speed On Demand", '-down$$' + normalTPPower + BindFile.BLF(profile, 'tp','tp_on1.txt'))

        if (self.GetState('TTP') and self.GetState('TTPEnable') and not (profile.General.GetState('Archetype') == "Peacebringer") and teamTPPower) :
            tphovermodeswitch = ''
            ResetFile.SetBind(self.GetState('TTPComboKey'), "Team TP Combo", "Speed On Demand", '+down$$' + teamTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'ttp','ttp_on1.txt'))
            ResetFile.SetBind(self.GetState('TTPBindKey'),  "Team TP Bind", "Speed On Demand", 'nop')
            ResetFile.SetBind(self.GetState('TTPResetKey'), "Team TP Reset", "Speed On Demand", substr(t['detailhi'],2) + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'ttp','ttp_off') + tphovermodeswitch)
            #  Create tp_off file
            ttp_off = profile.GetBindFile("ttp","ttp_off.txt")
            ttp_off.SetBind(self.GetState('TTPComboKey'), "Team TP Combo", "Speed On Demand",
                            '+down$$' + teamTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'ttp','ttp_on1.txt'))
            ttp_off.SetBind(self.GetState('TTPBindKey'), "Team TP Bind", "Speed On Demand",'nop')

            ttp_on1 = profile.GetBindFile("ttp","ttp_on1.txt")
            ttp_on1.SetBind(self.GetState('TTPComboKey'), "Team TP Combo", "Speed On Demand",
                            '-down$$powexecunqueue' + t['detailhi'] + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'ttp','ttp_off') + tphovermodeswitch)
            ttp_on1.SetBind(self.GetState('TTPBindKey'), "Team TP Bind", "Speed On Demand",
                            '+down' + BindFile.BLF(profile, 'ttp','ttp_on2.txt'))

            ttp_on2 = profile.GetBindFile("ttp","ttp_on2.txt")
            ttp_on2.SetBind(self.GetState('TTPBindKey'), "Team TP Bind", "Speed On Demand",
                            '-down$$' + teamTPPower + BindFile.BLF(profile, 'ttp','ttp_on1.txt'))



    def sodResetKey(self, curfile, p, path, turnoff, moddir):

        path = re.sub('\d\d\d\d\d\d', '000000', path)

        if (moddir == 'up')  : u = 1
        else:                   u = 0
        if (moddir == 'down'): d = 1
        else:                   d = 0

        # TODO, BLF is on the Bindfile objects now.
        curfile.SetBind(p.General.GetState('ResetKey'), "SoD Reset", "Speed On Demand",
                f'up {u} $$down {d}$$forward 0$$backward 0$$left 0$$right 0' +
                str(turnoff) + '$$t $name, SoD Binds Reset' + curfile.BaseReset() + curfile.BLF() # <- that might not be right
        )


    def sodDefaultResetKey(self, mobile, stationary):
        return
        # TODO -- decide where to keep 'resetstring' and make this sub update it.
        #cbAddReset('up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'.actPower_name(None,1,stationary,mobile) + '$$t $name, SoD Binds Reset')



    # TODO TODO TODO -- the s/\d\d\d\d\d\d/$newbits/ scheme in the following six subs is a vile evil (live veil ilve vlie) hack.
    def sodUpKey(self, t, bl, curfile, mobile, stationary, flight, autorun, followbl, bo, sssj):

        (upx,dow,forw,bac,lef,rig) = (t['upx'],t['D'],t['F'],t['B'],t['L'],t['R'])

        actkeys = t['totalkeys']

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
           actkeys = t['jkeys']
           if (t['totalkeys'] == 1 and t['space'] == 1): upx = '$$up 0'
           else:                                         upx = '$$up 1'

           if (t['X'] == 1):                             upx = '$$up 0'


        toggleon = mobile
        if (actkeys == 0):
           ml = t['mlon']
           toggleon = mobile
           if (not (mobile and (mobile == stationary))) : toggleoff = stationary
        else:
            toggleon = ''


        if (t['totalkeys'] == 1 and t['space'] == 1):
           ml = t['mloff']
           if (not (stationary and (mobile == stationary))) : toggleoff = mobile
           toggleon = stationary
        else:
            toggleoff = ''

        if (sssj):
            if (t['space'] == 0): #  if we are hitting the space bar rather than releasing its..
               toggleon = sssj
               toggleoff = mobile
               if (stationary and stationary == mobile) : toggleoff2 = stationary
            elif (t['space'] == 1) : #  if we are releasing the space bar ..
               toggleoff = sssj
               if (t['horizkeys'] > 0 or autorun) : #  and we are moving laterally, or in autorun..
                   toggleon = mobile
               else: #  otherwise turn on the stationary power..
                   toggleon = stationary


        toggle = ''
        if (toggleon or toggleoff):
           toggle = self.actPower_name(None,1,toggleon,toggleoff,toggleoff2)


        newbits = t.KeyState({'toggle' : 'space'})
        bl = re.sub('\d\d\d\d\d\d', newbits, bl)

        if t['space'] == 1: ini = '-down'
        else:               ini = '+down'

        if (followbl):
            move = ''
            if (t['space'] != 1):
                bl = re.sub('\d\d\d\d\d\d', '000000', followbl)
                move = f"{upx}{dow}{forw}{bac}{lef}{rig}"

            curfile.SetBind(self.GetState('Up'), "Up", "Speed On Demand", f"{ini}{move}{bl}")
        elif (not autorun):
            curfile.SetBind(self.GetState('Up'), "Up", "Speed On Demand", f"{ini}{upx}{dow}{forw}{bac}{lef}{rig}{ml}{toggle}{bl}")
        else:
            if (not sssj) : toggle = ''  #  returns the following line to the way it was before sssj
            curfile.SetBind(self.GetState('Up'), "Up", "Speed On Demand", f"{ini}{upx}{dow}$$backward 0{lef}{rig}{toggle}{t['mlon']}{bl}")



    def sodDownKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo,sssj):

        actkeys = t['totalkeys']

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
            if (t['cancj']  == 1) : aj = t['cjmp']
            if (t['canjmp'] == 1) : aj = t['jump']
            actkeys = t['jkeys']
            if (t['X'] == 1 and t['totalkeys'] > 1) : up = '$$up 1'
            else:                                     up = '$$up 0'

        toggleon = mobile
        if (actkeys == 0):
           ml = t['mlon']
           toggleon = mobile
           if (not (mobile and mobile == stationary)): toggleoff = stationary
        else:
           toggleon = None


        if (t['totalkeys'] == 1 and t['X'] == 1):
           ml = t['mloff']
           if (not (stationary and mobile == stationary)): toggleoff = mobile
           toggleon = stationary
        else:
            toggleoff = None


        toggle = ''
        if (toggleon or toggleoff):
           toggle = actPower_name(None,1,toggleon,toggleoff)


        newbits =t.KeyState({'toggle' : 'X'})
        bl = re.sub('\d\d\d\d\d\d', newbits, bl)

        if t['X'] == 1: ini = "-down"
        else:           ini = "+down"

        if (followbl):
            move = ''
            if (t['X'] != 1):
                bl = re.sub('\d\d\d\d\d\d', newbits, followbl)
                move = f"{up}{dowx}{forw}{bac}{lef}{rig}"

            curfile.SetBind(self.GetState('Down'), "Down", "Speed On Demand", f"{ini}{move}{bl}")
        elif (not autorun):
            curfile.SetBind(self.GetState('Down'), "Down", "Speed On Demand", f"{ini}{up}{dowx}{forw}{bac}{lef}{rig}{ml}{toggle}{bl}")
        else:
            curfile.SetBind(self.GetState('Down'), "Down", "Speed On Demand", f"{ini}{up}{dowx}$$backward 0{lef}{rig}{t['mlon']}{bl}")


    def sodForwardKey(self, t, bl, curfile,  mobile, stationary, flught, autorunbl, followbl, bo, sssj):
        (up,dow,forx,bac,lef,rig) = (t.U,t.D,t['forx'],t.B,t.L,t.R)

        actkeys = t['totalkeys']
        if (bo == "bo") : up = '$$up 1'; dow = '$$down 0'
        if (bo == "sd") : up = '$$up 0'; dow = '$$down 1'

        if (mobile     == 'Group Fly'): mobile = None
        if (stationary == 'Group Fly'): stationary = None

        if (flight == "Jump"):
           dow = '$$down 0'
           actkeys = t['jkeys']
           if (
                (t['totalkeys'] == 1 and t['W'] == 1)
                    or
                (t['X'] == 1)
                ): up = '$$up 0'
           else : up = '$$up 1'


        toggleon = mobile
        if (t['totalkeys'] == 0) :
            ml = t['mlon']
            if (not (mobile and mobile == stationary)):
               toggleoff = stationary

        if (t['totalkeys'] == 1 and t['W'] == 1):
            ml = t['mloff']

        if flight: testKeys = t['totalkeys']
        else:      testKeys = t['horizkeys']
        if (testKeys == 1 and t['W'] == 1) :
            if (not (stationary and mobile == stationary)):
                toggleoff = mobile

            toggleon = stationary

        if (sssj and t['space'] == 1) : #  if (we are jumping with SS+SJ mode enabled)
           toggleon = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff):
           toggle = actPower_name(None,1,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'W'})
        bl = re.sub('\d\d\d\d\d\d', newbits, bl)

        if t['W'] == 1: ini = "-down"
        else:           ini = "+down"

        if (followbl):
            if (t['W'] == 1):
               move = ini
            else:
                bl = re.sub('\d\d\d\d\d\d', newbits, followbl)
                move = f"{ini}{up}{dow}{forx}{bac}{lef}{rig}"

            curfile.SetBind(self.GetState('Forward'), "Forward", "Speed On Demand", move + bl)
            if (self.GetState('MouseChord')):
                if (t['W'] == 1) : move = f"{ini}{up}{dow}{forx}{bac}{rig}{lef}"
                curfile.SetBind('mousechord', "Mouse Chord", "Speed On Demand",  move + bl)

        elif (not autorunbl):
            curfile.SetBind(self.GetState('Forward'), "Forward", "Speed On Demand", f"{ini}{up}{dow}{forx}{bac}{lef}{rig}{ml}{toggle}{bl}")
            if (self.GetState('MouseChord')):
                curfile.SetBind('mousechord', "Mouse Chord", "Speed On Demand", f"{ini}{up}{dow}{forx}{bac}{rig}{lef}{ml}{toggle}{bl}")

        else:
            if (t['W'] == 1):
                bl = re.sub('\d\d\d\d\d\d', newbits, autorunbl)

            curfile.SetBind(self.GetState('Forward'), "Forward", "Speed On Demand", f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{lef}{rig}{t['mlon']}{bl}")
            if (self.GetState('MouseChord')) :
                curfile.SetBind('mousechord', "Mouse Chord", "Speed On Demand", f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{rig}{lef}{t['mlon']}{bl}")

    def sodBackKey(t,bl,curfile,mobile,stationary,flight,autorunbl,followbl,bo,sssj):
        (up,dow,forw,bacx,lef,rig) = (t.U,t.D,t.F, t['bacx'],t.L,t.R)

        actkeys = t['totalkeys']
        if (bo == "bo") : up = '$$up 1';dow = '$$down 0'
        if (bo == "sd") : up = '$$up 0';dow = '$$down 1'

        if (mobile     == 'Group Fly'): mobile = None
        if (stationary == 'Group Fly'): stationary = None

        if (flight == "Jump"):
           dow = '$$down 0'
           actkeys = t['jkeys']
           if (t['totalkeys'] == 1 and t['S'] == 1) : up = '$$up 0'
           else:                                      up = '$$up 1'

           if (t['X'] == 1) : up = '$$up 0'


        toggleon = mobile
        if (t['totalkeys'] == 0):
           ml = t['mlon']
           toggleon = mobile
           if (not (mobile and mobile == stationary)):
               toggleoff = stationary

        if (t['totalkeys'] == 1 and t['S'] == 1):
            ml = t['mloff']

        if flight: testKeys = t['totalkeys']
        else:      testKeys = t['horizkeys']
        if (testKeys == 1 and t['S'] == 1):
            if (not (stationary and mobile == stationary)):
               toggleoff = mobile

            toggleon = stationary

        if (sssj and t['space'] == 1): #  if (we are jumping with SS+SJ mode enabled
            toggleon = sssj
            toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
           toggle = actPower_name(None,1,toggleon,toggleoff)

        newbits =t.KeyState({'toggle' : 'S'})
        bl = re.sub('\d\d\d\d\d\d', newbits, bl)

        if (t['S'] == 1) : ini = "-down"
        else:              ini = "+down"

        if (followbl):
            if (t['S'] == 1):
               move = ini
            else:
                bl = re.sub('\d\d\d\d\d\d', newbits, followbl)
                move = f"{ini}{up}{dow}{forw}{bacx}{lef}{rig}"

            curfile.SetBind(self.GetState('Back'), "Back", "Speed On Demand", move + bl)
        elif (not autorunbl) :
            curfile.SetBind(self.GetState('Back'), "Back", "Speed On Demand", f"{ini}{up}{dow}{forw}{bacx}{lef}{rig}{ml}{toggle}{bl}")
        else:
            if (t['S'] == 1):
                move = '$$forward 1$$backward 0'
            else:
                move = '$$forward 0$$backward 1'
                bl = re.sub('\d\d\d\d\d\d', newbits, autorunbl)

            curfile.SetBind(self.GetState('Back'), "Back", "Speed On Demand", f"{ini}{up}{dow}{move}{lef}{rig}{t['mlon']}{bl}")

    def sodLeftKey(t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo,sssj):
        (up,dow,forw,bac,lefx,rig) = (t.U,t.D,t.F,t.B, t['lefx'],t.R)

        actkeys = t['totalkeys']
        if (bo == "bo") : up = '$$up 1';dow = '$$down 0'
        if (bo == "sd") : up = '$$up 0';dow = '$$down 1'

        if (mobile     == 'Group Fly') : mobile = None
        if (stationary == 'Group Fly') : stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            actkeys = t['jkeys']
            if (t['totalkeys'] == 1 and t['A'] == 1) : up = '$$up 0'
            else:                                      up = '$$up 1'

            if (t['X'] == 1) : up = '$$up 0'

        toggleon = mobile
        if (t['totalkeys'] == 0):
            ml = t['mlon']
            toggleon = mobile
            if (not (mobile and mobile == stationary)) :
                toggleoff = stationary

        if (t['totalkeys'] == 1 and t['A'] == 1) :
            ml = t['mloff']

        if flight: testKeys = t['totalkeys']
        else:      testKeys = t['horizkeys']

        if (testKeys == 1 and t['A'] == 1) :
            if (not (stationary and mobile == stationary)):
               toggleoff = mobile

            toggleon = stationary

        if (sssj and t['space'] == 1) : #  if (we are jumping with SS+SJ mode enabled
           toggleon = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
           toggle = actPower_name(None,1,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'A'})
        bl = re.sub('\d\d\d\d\d\d', newbits, bl)

        if (t['A'] == 1): ini = '-down'
        else:             ini = '+down'

        if (followbl) :
            if (t['A'] == 1) :
               move = ini
            else:
                bl = re.sub('\d\d\d\d\d\d', newbits, followbl)
                move = f"{ini}{up}{dow}{forw}{bac}{lefx}{rig}"

            curfile.SetBind(self.GetState('Left'), "Left", "Speed On Demand", move + bl)
        elif (not autorun) :
            curfile.SetBind(self.GetState('Left'), "Left", "Speed On Demand", f"{ini}{up}{dow}{forw}{bac}{lefx}{rig}{ml}{toggle}{bl}")
        else:
            curfile.SetBind(self.GetState('Left'), "Left", "Speed On Demand", f"{ini}{up}{dow}{'$$backward 0'}{lefx}{rig}{t['mlon']}{bl}")

    def sodRightKey(t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo,sssj):
        (up,dow,forw,bac,lef,rigx) = (t.U,t.D,t.F,t.B,t.L, t['rigx'])

        actkeys = t['totalkeys']
        if (bo == "bo") :up = '$$up 1';dow = '$$down 0'
        if (bo == "sd") :up = '$$up 0';dow = '$$down 1'

        if (mobile     == 'Group Fly') : mobile = None
        if (stationary == 'Group Fly') : stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            actkeys = t['jkeys']
            if (t['totalkeys'] == 1 and t['D'] == 1) : up = '$$up 0'
            else:                                      up = '$$up 1'

            if (t['X'] == 1) : up = '$$up 0'

        toggleon = mobile
        if (t['totalkeys'] == 0):
           ml = t['mlon']
           toggleon = mobile
           if (not (mobile and mobile == stationary)) :
               toggleoff = stationary

        if (t['totalkeys'] == 1 and t['D'] == 1) :
           ml = t['mloff']

        if flight: testKeys = t['totalkeys']
        else :     testKeys = t['horizkeys']
        if (testKeys == 1 and t['D'] == 1) :
            if (not (stationary and mobile == stationary)):
               toggleoff = mobile

            toggleon = stationary

        if (sssj and t['space'] == 1) : #  if (we are jumping with SS+SJ mode enabled
           toggleon = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) : 
           toggle = actPower_name(None,1,toggleon,toggleoff)

        newbits =t.KeyState({'toggle' : 'D'})
        bl = re.sub('\d\d\d\d\d\d', newbits, bl)

        if (t['D'] == 1): ini = '-down'
        else:             ini = '+down'

        if (followbl) :
            if (t['D'] == 1):
                move = ini
            else:
                bl = re.sub('\d\d\d\d\d\d', newbits, followbl)
                move = f"{ini}{up}{dow}{forw}{bac}{lef}{rigx}"

            curfile.SetBind(self.GetState('Right'), "Right", "Speed On Demand", move + bl)
        elif (not autorun) :
            curfile.SetBind(self.GetState('Right'), "Right", "Speed On Demand", f"{ini}{up}{dow}{forw}{bac}{lef}{rigx}{ml}{toggle}{bl}")
        else:
            curfile.SetBind(self.GetState('Right'), "Right", "Speed On Demand", f"{ini}{up}{dow}$$forward 1$$backward 0{lef}{rigx}{t['mlon']}{bl}")


    def sodAutoRunKey(t,bl,curfile,mobile,sssj):
        if (sssj and t['space'] == 1) :
            curfile.SetBind(self.GetState('AutoRun'), "Auto Run", "Speed On Demand", 'forward 1$$backward 0' + t.dirs('UDLR') + t['mlon'] + actPower_name(None,1,sssj,mobile) + bl)
        else:
            curfile.SetBind(self.GetState('AutoRun'), "Auto Run", "Speed On Demand", 'forward 1$$backward 0' + t.dirs('UDLR') + t['mlon'] + actPower_name(None,1,mobile) + bl)

    def sodAutoRunOffKey(t,bl,curfile,mobile,stationary,flight,sssj):
        if (not flight and not sssj) :
            if (t['horizkeys'] > 0) :
               toggleon = t['mlon'] + actPower_name(None,1,mobile)
            else:
               toggleon = t['mloff'] + actPower_name(None,1,stationary,mobile)

        elif (sssj) :
            if (t['horizkeys'] > 0 or t['space'] == 1) :
               toggleon = t['mlon'] + actPower_name(None,1,mobile,toggleoff)
            else:
               toggleon = t['mloff'] + actPower_name(None,1,stationary,mobile,toggleoff)

        else:
            if (t['totalkeys'] > 0) :
               toggleon = t['mlon'] + actPower_name(None,1,mobile)
            else:
               toggleon = t['mloff'] + actPower_name(None,1,stationary,mobile)

        bindload = bl + t.KeyState + '.txt'
        curfile.SetBind(self.GetState('AutoRun'), "Auto Run", "Speed On Demand", t.dirs('UDFBLR') + toggleon + bindload)


    def sodFollowKey(t,bl,curfile,mobile):
        curfile.SetBind(self.GetState('Follow'), "Follow", "Speed On Demand", 'follow' + actPower_name(None,1,mobile) + bl + t.KeyState() + '.txt')

    def sodFollowOffKey(t,bl,curfile,mobile,stationary,flight):
        if (not flight):
            if (t['horizkeys'] == 0) :
                if (stationary == mobile) :
                   toggle = actPower_name(None,1,stationary,mobile)
                else:
                   toggle = actPower_name(None,1,stationary)

        else:
            if (t['totalkeys'] == 0) :
                if (stationary == mobile) :
                   toggle = actPower_name(None,1,stationary,mobile)
                else:
                   toggle = actPower_name(None,1,stationary)

        curfile.SetBind(self.GetState('Follow'), "Follow", "Speed On Demand", "follow" + toggle + t.U + t['dow'] + t.F + t.B + t.L + t.R + bl + t.KeyState() + '.txt')


    def bindisused(self):
        return self.GetState('Enable')


    def findconflicts(self):
        Utility.CheckConflict("Up","Up Key")
        Utility.CheckConflict("Down","Down Key")
        Utility.CheckConflict("Forward","Forward Key")
        Utility.CheckConflict("Back","Back Key")
        Utility.CheckConflict("Left","Strafe Left Key")
        Utility.CheckConflict("Right","Strafe Right Key")
        Utility.CheckConflict("TLeft","Turn Left Key")
        Utility.CheckConflict("TRight","Turn Right Key")
        Utility.CheckConflict("AutoRun","AutoRun Key")
        Utility.CheckConflict("Follow","Follow Key")

        if (self.GetState('NonSoD'))       : Utility.CheckConflict("NonSoDMode","NonSoD Key")
        if (self.GetState('Base'))         : Utility.CheckConflict("BaseMode","Sprint Mode Key")
        if (self.GetState('SSSS'))         : Utility.CheckConflict("RunMode","Speed Mode Key")
        if (self.GetState('JumpCJ')
                or self.GetState('JumpSJ') ): Utility.CheckConflict("JumpMode","Jump Mode Key")
        if (self.GetState('FlyHover')
                or self.GetState('FlyFly') ): Utility.CheckConflict("FlyMode","Fly Mode Key")
        if (self.GetState('FlyQFly')
                and (profile.General.GetState('Archetype') == "Peacebringer")): Utility.CheckConflict("QFlyMode","Q.Fly Mode Key")
        if (self.GetState('TP') and self.GetState('TPEnable')):
            Utility.CheckConflict(self.GetState('TP'),"ComboKey","TP ComboKey")
            Utility.CheckConflict(self.GetState('TP'),"ResetKey","TP ResetKey")

            TPQuestion = "Teleport Bind"
            if (profile.General.GetState('Archetype') == "Peacebringer") :
               TPQuestion = "Dwarf Step Bind"
            elif (profile.General.GetState('Archetype') == "Warshade") :
               TPQuestion = "Shd/Dwf Step Bind"

            Utility.CheckConflict(self.GetState('TP'),"BindKey", TPQuestion)

            if (self.GetState('FlyGFly')): Utility.CheckConflict("GFlyMode","Group Fly Key")
        if (self.GetState('TTP') and self.GetState('TTPEnable')):
            Utility.CheckConflict(self.GetState('TTP'),"ComboKey","TTP ComboKey")
            Utility.CheckConflict(self.GetState('TTP'),"ResetKey","TTP ResetKey")
            Utility.CheckConflict(self.GetState('TTP'),"BindKey","Team TP Bind")

        if (self.GetState('Temp') and self.GetState('TempEnable')):
            Utility.CheckConflict("TempMode","Temp Mode Key")
            Utility.CheckConflict(self.GetState('Temp'),"TraySwitch","Tray Toggle Key")

        if ((profile.General.GetState('Archetype') == "Peacebringer") or (profile.General.GetState('Archetype') == "Warshade")) :
            if (self.GetState('Nova')  and self.GetState('NovaEnable')): Utility.CheckConflict(self.GetState('Nova'), "Mode","Nova Form Bind")
            if (self.GetState('Dwarf') and self.GetState('DwarfEnable')): Utility.CheckConflict(self.GetState('Dwarf'),"Mode","Dwarf Form Bind")


    #  toggleon variation
    def actPower_toggle(self, start, unq, on, *rest):
        # if (refon):
            #  deal with power slot stuff..
           # traytest = on['trayslot']

        offpower = {}
        # # TODO this will simply not work yet
        # for v in rest:
        #     if (ref(v)):
        #         while (my ($j,w) = each %$v):
        #             if (w and w ne 'on' and not offpower[$w]):
        #                 if (refw):
        #                     if ($w['trayslot'] == traytest):
        #                        s = s + '$$powexectray ' + w['trayslot']
        #                        unq = 1

        #                 else:
        #                    offpower['w'] = 1
        #                    s .= '$$powexectoggleoff ' + w

        #         if ($v['trayslo'] andv['trayslot'] ==traytest) {
        #            s =s + '$$powexectray ' + v['trayslot']
        #            unq = 1

        #     else:
        #         if ($v and ($v ne 'on') and not offpower[$v]) {
        #            offpower[$v] = 1
        #            s .= '$$powexectoggleoff ' + v

        # if ($unq ands):
        #    s .= '$$powexecunqueue'

        # # if start then s = string.sub(s,3,string.len(s)) end
        # if ($on):
        #     if (refon):
        #         #  deal with power slot stuff..
        #        s .= '$$powexectray '.$on['trayslot'] + '$$powexectray ' + on['trayslot']
        #     else:
        #        s .= '$$powexectoggleon ' + on

        # return s


    #sub actPower { goto &actPower_name
    def actPower_name(self, start, unq, on,*rest):
        pass
        #if (ref on):
            #  deal with power slot stuff..
           #traytest = on['trayslot']

        # # TODO - reimplement this in Python re 'ref' etc
        # for v in rest:
        #     if (not ref(v)):
        #         if (v and v ne 'on'):
        #            s .= '$$powexecname ' + v

        #     else: #v is a ref
        #         while (my (None,w) = each %$v) {
        #             if ($w andw ne 'on'):
        #                 if (refw):
        #                     if ($w['trayslot'] ==traytest) {
        #                        s .= '$$powexectray ' + w['trayslot']

        #                 else:
        #                    s .= '$$powexecname ' + w



        #         if ($v['trayslot'] andv['trayslot'] ==traytest) {
        #            s .= '$$powexectray ' + v['trayslot']



        # if ($unq ands):
        #    s .= '$$powexecunqueue'


        # if ($on andon ne ''):
        #     if (refon):
        #         #  deal with power slot stuff..
        #        s .= '$$powexectray ' + on['trayslot'] + '$$powexectray ' + on['trayslot']
        #     else:
        #        s .= '$$powexecname ' + on + '$$powexecname ' + on


        # if ($start) {s = substrs, 2
        return s


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

        filename = t['path']("${autofollowmode}j",suffix)
        tglfile = profile.GetBindFile(filename)
        t['ini'] = '-down$$'
        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key, "Jump Fix", "Speed On Demand", "+down" + feedback + actPower_name(None,1,t['cjmp']) + BindFile.BLF(profile,filename))


    def sodSetDownFix(self, profile,t,key,makeModeKey,suffix,bl,curfile,turnoff,autofollowmode,feedback):
        if autofollowmode:
            pathsuffix = "f"
        else:
            pathsuffix = "a"

        filename = t['path']("$autofollowmodepathsuffix",suffix)
        tglfile = profile.GetBindFile(filename)
        t['ini'] = '-down$$'
        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key, "Set Down Fix", "Speed On Demand", '+down' + feedback + BindFile.BLF(profile,filename))



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
    # TODO - do we want to call out each possibility by name since it's a known list?
    def __init__(self, init):
        for key in init:
            self[key] = init[key]


    # return binary string of which keys are "on";
    # optionally flipping one of them first.
    # TODO:  not clear this belongs on a class, as opposed
    # to just a utility sub here or in Utility.
    def KeyState(self, p):
        togglebit = p['toggle']

        ret = ''
        for key in ('space','X','W','S','A','D'):
            if key == togglebit:
                ret = ret + str(not self[key])
            else:
                ret = ret + str(self[key])
        return ret


    # These next two subs are terrible.  This stuff should all be squirreled away in BindFile.

#    # This will return "$bindloadfilesilent C:\path\CODE\CODE1010101<suffix>.txt"
#    sub bl {
#        my self = shift
#        code = shift
#        suffix = shift || ''
#        p = self['profile']
#        return BindFile.BLF($p, uc($code), uc($code) + self.KeyState() + suffix + '.txt')
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
#    sub dirs {
#        my self = shift
#        ret
#        for (split '', shift) {
#           ret .= self[ { U = 'up', D = 'dow', F = 'forw', B = 'bac', L = 'lef', R = 'rig' ][$_]
#
#        returnret
#
#    sub U { shift()['up']
#    sub D { shift()['dow']
#    sub F { shift()['forw']
#    sub B { shift()['bac']
#    sub L { shift()['lef']
#    sub R { shift()['rig']
