import wx
import UI

from Page import Page
from UI.ControlGroup import ControlGroup


class SoD(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Speed On Demand"

        self.State = {
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

            'NonSoDMode'         : 'CTRL-M',
            'JumpMode'           : "T",
            'SimpleSJCJ'         : 1,

            'RunMode'            : "C",
            'SSOnlyWhenMoving'   : 0,
            'SSSJModeEnable'     : 1,

            'FlyMode'            : "F",
            'GFlyMode'           : "G",

            'SelfTellOnChange'   : 1,

            'TPMode'             : 'SHIFT-LBUTTON',
            'TPCombo'            : 'SHIFT',
            'TPReset'            : 'CTRL-T',

            'TTPMode'            : 'SHIFT-CTRL-LBUTTON',
            'TTPCombo'           : 'SHIFT-CTRL',
            'TTPReset'           : 'SHIFT-CTRL-T',
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
            'Enable'             : None,
        }


        self.State['NovaMode'] = "T"
        self.State['NovaTray'] = "4"

        self.State['DwarfMode'] = "G"
        self.State['DwarfTray'] = "5"

        if (self.Profile.Pages['General'].State['Archetype'] == "Peacebringer"):
            self.State['NovaNova'] = "Bright Nova"
            self.State['DwarfDwarf'] = "White Dwarf"
            self.State['HumanFormShield'] = "Shining Shield"

        elif (self.Profile.Pages['General'].State['Archetype'] == "Warshade"):
            self.State['NovaNova'] = "Dark Nova"
            self.State['DwarfDwarf'] = "Black Dwarf"
            self.State['HumanFormShield'] = "Gravity Shield"

        self.State['HumanMode']    = "UNBOUND"
        self.State['HumanTray']    = "1"
        self.State['HumanHumanPBind'] = "nop"
        self.State['HumanNovaPBind']  = "nop"
        self.State['HumanDwarfPBind'] = "nop"

        #  Temp Travel Powers
        self.State['TempTray'] = "6"
        self.State['TempTraySwitch'] = "UNBOUND"
        self.State['TempMode'] = "UNBOUND"

    def FillTab(self):

        topSizer = wx.FlexGridSizer(0,2,10,10)

        topSizer.Add( wx.CheckBox( self, -1, "Enable Speed On Demand Binds" ), 0,
                wx.TOP|wx.LEFT, 10)
        topSizer.AddSpacer(1)

        leftColumn  = wx.BoxSizer(wx.VERTICAL)
        rightColumn = wx.BoxSizer(wx.VERTICAL)


        ##### MOVEMENT KEYS
        movementSizer = ControlGroup(self, 'Movement Keys')

        for dir in ("Up","Down","Forward","Back","Left","Right","TurnLeft","TurnRight"):
            movementSizer.AddLabeledControl(
                value = dir,
                ctltype = 'keybutton',
            )
        # TODO!  fill this picker with only the appropriate bits.
        # for i in (powers list):
        #   if (player has power): add_to_contents(i)
        movementSizer.AddLabeledControl(
            value = 'DefaultMode',
            ctltype = 'combo',
            contents = ('No SoD','Sprint','Super Speed','Jump','Fly'),
        )
        movementSizer.AddLabeledControl(
            value = 'MousechordSoD',
            ctltype = 'checkbox',
        )
        leftColumn.Add(movementSizer, 0, wx.EXPAND)


        ##### GENERAL SETTINGS
        generalSizer = ControlGroup(self, 'General Settings')

        generalSizer.AddLabeledControl(
            value = 'AutoMouseLook',
            ctltype = 'checkbox',
            tooltip = 'Automatically Mouselook when moving',
        )
        # TODO -- add "SprintPowers" to GameData
#        generalSizer.AddLabeledControl(
#            value = 'SprintPower',
#            ctltype = 'combo',
#            contents = GameData['SprintPowers'],
#        )

        # TODO -- decide what to do with this.
        # generalSizer.Add( wx.CheckBox(self, SPRINT_UNQUEUE, "Exec powexecunqueue"))

        for command in ("AutoRun","Follow","NonSoDMode"): # TODO - lost "Sprint-Only SoD Mode" b/c couldn't find the name in %$Labels
            generalSizer.AddLabeledControl(
                value = command,
                ctltype = 'keybutton',
            )
        generalSizer.AddLabeledControl(
            value = 'SprintSoD',
            ctltype = 'checkbox',
        )
        generalSizer.AddLabeledControl(
            value = 'ChangeCamera',
            ctltype = 'checkbox',
        )
        generalSizer.AddLabeledControl(
            value = 'CamdistBase',
            ctltype = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddLabeledControl(
            value = 'CamdistTravelling',
            ctltype = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddLabeledControl(
            value = 'ChangeDetail',
            ctltype = 'checkbox',
        )
        generalSizer.AddLabeledControl(
            value = 'DetailBase',
            ctltype = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddLabeledControl(
            value = 'DetailTravelling',
            ctltype = 'spinbox',
            contents = (1, 100),
        )
        generalSizer.AddLabeledControl(
            value = 'TPHideWindows',
            ctltype = 'checkbox',
        )
        generalSizer.AddLabeledControl(
            value = 'SelfTellOnChange',
            ctltype = 'checkbox',
        )
        leftColumn.Add(generalSizer, 0, wx.EXPAND)


        ##### SUPER SPEED
        superSpeedSizer = ControlGroup(self, 'Super Speed')
        superSpeedSizer.AddLabeledControl(
            value = 'RunMode',
            ctltype = 'keybutton',
        )
        superSpeedSizer.AddLabeledControl(
            value = 'SSOnlyWhenMoving',
            ctltype = 'checkbox',
        )
        superSpeedSizer.AddLabeledControl(
            value = 'SSSJModeEnable',
            ctltype = 'checkbox',
        )
        rightColumn.Add(superSpeedSizer, 0, wx.EXPAND)

        ##### SUPER JUMP
        superJumpSizer = ControlGroup(self, 'Super Jump')
        superJumpSizer.AddLabeledControl(
            value = 'JumpMode',
            ctltype = 'keybutton',
        )
        superJumpSizer.AddLabeledControl(
            value = 'SimpleSJCJ',
            ctltype = 'checkbox',
        )
        rightColumn.Add(superJumpSizer, 0, wx.EXPAND)


        ##### FLY
        flySizer = ControlGroup(self, 'Flight')

        flySizer.AddLabeledControl(
            value = 'FlyMode',
            ctltype = 'keybutton',
        )
        flySizer.AddLabeledControl(
            value = 'GFlyMode',
            ctltype = 'keybutton',
        )
        rightColumn.Add(flySizer, 0, wx.EXPAND)

        ##### TELEPORT
        teleportSizer = ControlGroup(self, 'Teleport')

        # if (at == peacebringer) "Dwarf Step"
        # if (at == warshade) "Shadow Step / Dwarf Step"

        teleportSizer.AddLabeledControl(
            value = "TPMode",
            ctltype = 'keybutton',
        )
        teleportSizer.AddLabeledControl(
            value = "TPCombo",
            ctltype = 'keybutton',
        )
        teleportSizer.AddLabeledControl(
            value = "TPReset",
            ctltype = 'keybutton',
        )

        # if (player has hover): {
        teleportSizer.AddLabeledControl(
            value = 'TPAutoHover',
            ctltype = 'checkbox',
        )
        #

        # if (player has team-tp) {
        teleportSizer.AddLabeledControl(
            value = "TTPMode",
            ctltype = 'keybutton',
        )
        teleportSizer.AddLabeledControl(
            value = "TTPCombo",
            ctltype = 'keybutton',
        )
        teleportSizer.AddLabeledControl(
            value = "TTPReset",
            ctltype = 'keybutton',
        )

        # if (player has group fly) {
        teleportSizer.AddLabeledControl(
            value = 'TTPAutoGFly',
            ctltype = 'checkbox',
        )
        #
        #
        # end team-tp
        rightColumn.Add(teleportSizer, 0, wx.EXPAND)

        ##### TEMP TRAVEL POWERS
        tempSizer = ControlGroup(self, 'Temp Travel Powers')
        # if (temp travel powers exist)?  Should this be "custom"?
        tempSizer.AddLabeledControl(
            value = 'TempMode',
            ctltype = 'keybutton',
        )
        tempSizer.AddLabeledControl(
            value = 'TempTray',
            ctltype = 'spinbox',
            contents = [1, 8],
        )
        rightColumn.Add(tempSizer, 0, wx.EXPAND)

        ##### KHELDIAN TRAVEL POWERS
        kheldianSizer = ControlGroup(self, 'Nova / Dwarf Travel Powers')

        kheldianSizer.AddLabeledControl(
            value = 'NovaMode',
            ctltype = 'keybutton',
        )
        kheldianSizer.AddLabeledControl(
            value = 'NovaTray',
            ctltype = 'spinbox',
            contents = [1, 8],
        )
        kheldianSizer.AddLabeledControl(
            value = 'DwarfMode',
            ctltype = 'keybutton',
        )
        kheldianSizer.AddLabeledControl(
            value = 'DwarfTray',
            ctltype = 'spinbox',
            contents = [1, 8],
        )

        # do we want a key to change directly to human form, instead of toggles?
        kheldianSizer.AddLabeledControl(
            value = 'HumanMode',
            ctltype = 'keybutton',
        )
        kheldianSizer.AddLabeledControl(
            value = 'HumanTray',
            ctltype = 'spinbox',
            contents = [1, 8],
        )

        rightColumn.Add(kheldianSizer, 0, wx.EXPAND)

        topSizer.Add(leftColumn)
        topSizer.Add(rightColumn)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizer(paddingSizer)


    def makeSoDFile(self, p):

        t = p['t']


        bl   = t['bl'].get(p['bl'], "")
        bla  = t['bl'].get(p['bla'], "")
        blf  = t['bl'].get(p['blf'], "")
        blbo = t['bl'].get(p['blbo'], "")
        blsd = t['bl'].get(p['blsd'], "")

        path   = t['path'].get(p['path'], "")
        pathr  = t['path'].get(p['pathr'], "")
        pathf  = t['path'].get(p['pathf'], "")
        pathbo = t['path'].get(p['pathbo'], "")
        pathsd = t['path'].get(p['pathsd'], "")

        mobile     = p.get('mobile', "")
        stationary = p.get('stationary', "")
        modestr    = p.get('modestr', "")
        flight     = p.get('flight', "")
        fix        = p.get('fix', "")
        turnoff    = p.get('turnoff', "")
        sssj       = p.get('sssj', "")

        # TODO -- this wants to beturnoff ||= mobile, stationary once we know what those are.  arrays?  hashes?
        #$turnoff ||= {mobile,stationary}

        if ((self.State['Default'] == modestr) and (t['totalkeys'] == 0)):

            curfile = profile.ResetFile
            sodDefaultResetKey(mobile,stationary)

            sodUpKey     (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
            sodDownKey   (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
            sodForwardKey(t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
            sodBackKey   (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
            sodLeftKey   (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
            sodRightKey  (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)

            if (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"r", curfile,{mobile,stationary})
            if (modestr == "Base")  : makeBaseModeKey  (profile,t,"r", curfile,turnoff,fix)
            if (modestr == "Fly")   : makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)
            if (modestr == "GFly")  : makeGFlyModeKey  (profile,t,"gf",curfile,turnoff,fix)
            if (modestr == "Run")   : makeSpeedModeKey (profile,t,"s", curfile,turnoff,fix)
            if (modestr == "Jump")  : makeJumpModeKey  (profile,t,"j", curfile,turnoff,path)
            if (modestr == "Temp")  : makeTempModeKey  (profile,t,"r", curfile,turnoff,path)
            if (modestr == "QFly")  : makeQFlyModeKey  (profile,t,"r", curfile,turnoff,modestr)

            sodAutoRunKey(t,bla,curfile,self.State,mobile,sssj)

            sodFollowKey(t,blf,curfile,self.State,mobile)

        if (flight and (flight == "Fly") and pathbo):
            #  blast off
            curfile = profile.GetBindFile(pathbo)
            sodResetKey(curfile,profile,path,actPower_toggle(None,1,stationary,mobile),'')

            sodUpKey     (t,blbo,curfile,self.State,mobile,stationary,flight,'','',"bo",sssj)
            sodDownKey   (t,blbo,curfile,self.State,mobile,stationary,flight,'','',"bo",sssj)
            sodForwardKey(t,blbo,curfile,self.State,mobile,stationary,flight,'','',"bo",sssj)
            sodBackKey   (t,blbo,curfile,self.State,mobile,stationary,flight,'','',"bo",sssj)
            sodLeftKey   (t,blbo,curfile,self.State,mobile,stationary,flight,'','',"bo",sssj)
            sodRightKey  (t,blbo,curfile,self.State,mobile,stationary,flight,'','',"bo",sssj)

            if (modestr == "Base") : makeBaseModeKey(profile,t,"r",curfile,turnoff,fix)

            t['ini'] = '-down$$'

            if (self.State['Default'] == "Fly"):

                if (self.State['NonSoD']):
                    t['FlyMode'] = t['NonSoDMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                if (self.State['Base']):
                    t['FlyMode'] = t['BaseMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                if (t['canss']):
                    t['FlyMode'] = t['RunMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                if (t['canjmp']):
                    t['FlyMode'] = t['JumpMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                if (self.State['Temp'] and self.State['TempEnable']):
                    t['FlyMode'] = t['TempMode']
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                else:
                    makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)

            t['ini'] = ''
            if (modestr == "GFly") : makeGFlyModeKey  (profile,t,"gbo",curfile,turnoff,fix)
            if (modestr == "Run")  : makeSpeedModeKey (profile,t,"s",  curfile,turnoff,fix)
            if (modestr == "Jump") : makeJumpModeKey  (profile,t,"j",  curfile,turnoff,path)

            sodAutoRunKey(t,bla,curfile,self.State,mobile,sssj)

            sodFollowKey(t,blf,curfile,self.State,mobile)

            # curfile = profile.GetBindFile(pathsd)

            sodResetKey(curfile,profile,path,actPower_toggle(None,1,stationary,mobile),'')

            sodUpKey     (t,blsd,curfile,self.State,mobile,stationary,flight,'','',"sd",sssj)
            sodDownKey   (t,blsd,curfile,self.State,mobile,stationary,flight,'','',"sd",sssj)
            sodForwardKey(t,blsd,curfile,self.State,mobile,stationary,flight,'','',"sd",sssj)
            sodBackKey   (t,blsd,curfile,self.State,mobile,stationary,flight,'','',"sd",sssj)
            sodLeftKey   (t,blsd,curfile,self.State,mobile,stationary,flight,'','',"sd",sssj)
            sodRightKey  (t,blsd,curfile,self.State,mobile,stationary,flight,'','',"sd",sssj)

            t['ini'] = '-down$$'
            if (modestr == "Base") : makeBaseModeKey(profile,t,"r",  curfile,turnoff,fix)
            if (modestr == "Fly")  : makeFlyModeKey( profile,t,"a",  curfile,turnoff,fix)
            if (modestr == "GFly") : makeGFlyModeKey(profile,t,"gbo",curfile,turnoff,fix)
            t['ini'] = ''
            if (modestr == "Jump") : makeJumpModeKey(profile,t,"j",  curfile,turnoff,path)

            sodAutoRunKey(t,bla,curfile,self.State,mobile,sssj)
            sodFollowKey(t,blf,curfile,self.State,mobile)

        curfile = profile.GetBindFile(path)

        sodResetKey(curfile,profile,path,actPower_toggle(None,1,stationary,mobile),'')

        sodUpKey     (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
        sodDownKey   (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
        sodForwardKey(t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
        sodBackKey   (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
        sodLeftKey   (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)
        sodRightKey  (t,bl,curfile,self.State,mobile,stationary,flight,'','','',sssj)

        if ((flight == "Fly") and pathbo):
            #  Base to set down
            if (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"r",curfile,{mobile,stationary},sodSetDownFix)
            if (modestr == "Base")  : makeBaseModeKey  (profile,t,"r",curfile,turnoff,sodSetDownFix)
            if (t['BaseMode']):
                curfile.SetBind(t['BaseMode'],"+down$$down 1" + actPower_name(None,1,mobile) + t['detailhi'] + t['runcamdist'] + t['blsd'])

            if (modestr == "Run")    : makeSpeedModeKey (profile,t,"s", curfile,turnoff,sodSetDownFix)
            if (modestr == "Fly")    : makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)
            if (modestr == "Jump")   : makeJumpModeKey  (profile,t,"j", curfile,turnoff,path)
            if (modestr == "Temp")   : makeTempModeKey  (profile,t,"r", curfile,turnoff,path)
            if (modestr == "QFly")   : makeQFlyModeKey  (profile,t,"r", curfile,turnoff,modestr)
        else:
            if (modestr == "NonSoD") : makeNonSoDModeKey(profile,t,"r", curfile,{mobile,stationary})
            if (modestr == "Base")   : makeBaseModeKey  (profile,t,"r", curfile,turnoff,fix)
            if (flight == "Jump"):
                if (modestr == "Fly"): makeFlyModeKey   (profile,t,"a", curfile,turnoff,fix,None,1)
            else:
                if (modestr == "Fly"): makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)


            if (modestr == "Run")   : makeSpeedModeKey  (profile,t,"s", curfile,turnoff,fix)
            if (modestr == "Jump")  : makeJumpModeKey   (profile,t,"j", curfile,turnoff,path)
            if (modestr == "Temp")  : makeTempModeKey   (profile,t,"r", curfile,turnoff,path)
            if (modestr == "QFly")  : makeQFlyModeKey   (profile,t,"r", curfile,turnoff,modestr)

        sodAutoRunKey(t,bla,curfile,self.State,mobile,sssj)

        sodFollowKey(t,blf,curfile,self.State,mobile)

    # AutoRun Binds
        curfile = profile.GetBindFile(pathr)

        sodResetKey(curfile,profile,path,actPower_toggle(None,1,stationary,mobile),'')

        sodUpKey     (t,bla,curfile,self.State,mobile,stationary,flight,1,'','',sssj)
        sodDownKey   (t,bla,curfile,self.State,mobile,stationary,flight,1,'','',sssj)
        sodForwardKey(t,bla,curfile,self.State,mobile,stationary,flight,bl, '','',sssj)
        sodBackKey   (t,bla,curfile,self.State,mobile,stationary,flight,bl, '','',sssj)
        sodLeftKey   (t,bla,curfile,self.State,mobile,stationary,flight,1,'','',sssj)
        sodRightKey  (t,bla,curfile,self.State,mobile,stationary,flight,1,'','',sssj)

        if ((flight == "Fly") and pathbo):
            if (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"ar",curfile,{mobile,stationary},sodSetDownFix)
            if (modestr == "Base")  : makeBaseModeKey  (profile,t,"gr",curfile,turnoff,sodSetDownFix)
            if (modestr == "Run")   : makeSpeedModeKey (profile,t,"as",curfile,turnoff,sodSetDownFix)
        else:
            if (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"ar",curfile,{mobile,stationary})
            if (modestr == "Base")  : makeBaseModeKey  (profile,t,"gr",curfile,turnoff,fix)
            if (modestr == "Run")   : makeSpeedModeKey (profile,t,"as",curfile,turnoff,fix)

        if (modestr == "Fly")       : makeFlyModeKey   (profile,t,"af",curfile,turnoff,fix)
        if (modestr == "Jump")      : makeJumpModeKey  (profile,t,"aj",curfile,turnoff,pathr)
        if (modestr == "Temp")      : makeTempModeKey  (profile,t,"ar",curfile,turnoff,path)
        if (modestr == "QFly")      : makeQFlyModeKey  (profile,t,"ar",curfile,turnoff,modestr)

        sodAutoRunOffKey(t,bl,curfile,self.State,mobile,stationary,flight)

        curfile.SetBind(self.State['Follow'],'nop')

        # FollowRun Binds
        curfile = profile.GetBindFile(pathf)

        sodResetKey(curfile,profile,path,actPower_toggle(None,1,stationary,mobile),'')

        sodUpKey     (t,blf,curfile,self.State,mobile,stationary,flight,'',bl,'',sssj)
        sodDownKey   (t,blf,curfile,self.State,mobile,stationary,flight,'',bl,'',sssj)
        sodForwardKey(t,blf,curfile,self.State,mobile,stationary,flight,'',bl,'',sssj)
        sodBackKey   (t,blf,curfile,self.State,mobile,stationary,flight,'',bl,'',sssj)
        sodLeftKey   (t,blf,curfile,self.State,mobile,stationary,flight,'',bl,'',sssj)
        sodRightKey  (t,blf,curfile,self.State,mobile,stationary,flight,'',bl,'',sssj)

        if ((flight == "Fly") and pathbo):
            if (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"fr",curfile,{mobile,stationary},sodSetDownFix)
            if (modestr == "Base")  : makeBaseModeKey  (profile,t,"fr",curfile,turnoff,sodSetDownFix)
            if (modestr == "Run")   : makeSpeedModeKey (profile,t,"fs",curfile,turnoff,sodSetDownFix)
        else:
            if (modestr == "NonSoD"): makeNonSoDModeKey(profile,t,"fr",curfile,{mobile,stationary})
            if (modestr == "Base")  : makeBaseModeKey  (profile,t,"fr",curfile,turnoff,fix)
            if (modestr == "Run")   : makeSpeedModeKey (profile,t,"fs",curfile,turnoff,fix)

        if (modestr == "Fly")       : makeFlyModeKey   (profile,t,"ff",curfile,turnoff,fix)
        if (modestr == "Jump")      : makeJumpModeKey  (profile,t,"fj",curfile,turnoff,pathf)
        if (modestr == "Temp")      : makeTempModeKey  (profile,t,"fr",curfile,turnoff,path)
        if (modestr == "QFly")      : makeQFlyModeKey  (profile,t,"fr",curfile,turnoff,modestr)

        curfile.SetBind(self.State['AutoRun'],'nop')

        sodFollowOffKey(t,bl,curfile,self.State,mobile,stationary,flight)



    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeNonSoDModeKey(self, p, t, bl, cur, toff, fix, fb):
        key = t['NonSoDMode']
        if (not key or (key == 'UNBOUND')): return

        if p['SoD']['Feedback']: feedback = (fb or '$$tname, Non-SoD Mode')
        else:                    feedback = ''

        if t['ini'] == None: t['ini'] = ''

        if (bl == "r"):
            bindload = t['bl']('n')
            if (fix):
                fix(p,t,key, makeNonSoDModeKey,"n",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, t['ini'] + actPower_toggle(None,1,None,toff) + t +dirs('UDFBLR') + t['detailhi'] + t['runcamdist'] + feedback + bindload)

        elif (bl == "ar"):
            bindload = t['bl']('an')
            if (fix):
                fix(p,t,key, makeNonSoDModeKey,"n",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, t['ini'] + actPower_toggle(None,1,None,toff) + t['detailhi'] + t['runcamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, makeNonSoDModeKey,"n",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, t['ini'] + actPower_toggle(None,1,None,toff) + t['detailhi'] + t['runcamdist'] + '$$up 0' + feedback + t['bl']('fn'))
        t['ini'] = ''

    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeTempModeKey(self, p, t, bl, cur, toff):
        key = t['TempMode']
        if (not key or (key == "UNBOUND")): return

        if p['SoD']['Feedback']: feedback = '$$tname, Temp Mode'
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''
        trayslot = "1 p['SoD']['TempTray']"

        if (bl == "r"):
            bindload = t['bl']('t')
            cur.SetBind(key, t['ini'] + actPower(None,1,trayslot,toff) + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)
        elif (bl == "ar"):
            bindload  = t['bl']('at')
            bindload2 = t['bl']('at','_t')
            tgl = p.GetBindFile(bindload2)
            cur.SetBind(key, t['in'] + actPower(None,1,trayslot,toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload2)
            tgl.SetBind(key, t['in'] + actPower(None,1,trayslot,toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload)
        else:
            cur.SetBind(key, t['ini'] + actPower(None,1,trayslot,toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + feedback + t['bl']('ft'))

        t['ini'] = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeQFlyModeKey(self, p, t, bl, cur, toff, modestr):
        key = t['QFlyMode']
        if (not key or key == "UNBOUND"): return

        if (modestr == "NonSoD"):
            cur.SetBind(key, "powexecname Quantum Flight")
            return

        if p['SoD']['Feedback']: feedback = '$$tname, QFlight Mode'
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''

        if (bl == "r"):
            bindload  = t['bl']('n')
            bindload2 = t['bl']('n'+'_q')
            tgl = p.GetBindFile(bindload2)

            if (modestr == 'Nova' or modestr == 'Dwarf'): tray = '$$gototray 1'
            else:                                         tray = ''

            cur.SetBind(key, t['ini'] + actPower(None,1,'Quantum Flight', toff) + tray + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload2)
            tgl.SetBind(key, t['ini'] + actPower(None,1,'Quantum Flight', toff) + tray + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t['bl']('an')
            bindload2 = t['bl']('an','_t')
            tgl = p.GetBindFile(bindload2)
            cur.SetBind(key, t['in'] + actPower(None,1,'Quantum Flight', toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload2)
            tgl.SetBind(key, t['in'] + actPower(None,1,'Quantum Flight', toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload)
        else:
            cur.SetBind(key, t['ini'] + actPower(None,1,'Quantum Flight', toff) + t['detaillo'] + t['flycamdist'] + '$$up 0' + feedback + t['bl']('fn'))

        t['ini'] = ''

    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeBaseModeKey(self, p, t, bl, cur, toff, fix, fb):
        key = t['BaseMode']
        if (not key or key == "UNBOUND"): return

        if p['SoD']['Feedback']: feedback = (fb or '$$tname, Sprint-SoD Mode')
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''

        if (bl == "r"):
            bindload  = t['bl']()

            if t['horizkeys']: sprint = t['sprint']
            else:              sprint = ''
            ton = actPower_toggle(1, 1, sprint, toff)

            if (fix):
                fix(p,t,key, makeBaseModeKey,"r",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, t['ini'] + ton + t.dirs('UDFBLR') + t['detailhi'] + t['runcamdist'] + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t['bl']('gr')

            if (fix):
                fix(p,t,key, makeBaseModeKey,"r",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, t['ini'] + actPower_toggle(1,1,t['sprint'],toff) + t['detailhi'] +  t['runcamdist'] + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, makeBaseModeKey,"r",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, t['ini'] + actPower_toggle(1,1,t['sprint'], toff) + t['detailhi'] + t['runcamdist'] + '$$up 0' + fb + t['bl']('fr'))

        t['ini'] = ''

    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeSpeedModeKey(self, p, t, bl, cur, toff, fix, fb):
        key = t['RunMode']

        if p['SoD']['Feedback']: feedback = (fb or '$$tname, Superspeed Mode')
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''

        if (t['canss']):
            if (bl == 's'):
                bindload = t['bl']('s')
                if (fix):
                    fix(p,t,key,makeSpeedModeKey,"s",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(key,t['ini'] + actPower_toggle(1,1,t['speed'],toff) + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

            elif (bl == "as"):
                bindload = t['bl']('as')
                if (fix):
                    fix(p,t,key,makeSpeedModeKey,"s",bl,cur,toff,"a",feedback)
                elif (not feedback):
                    cur.SetBind(key,t['ini'] + actPower_toggle(1,1,t['speed'],toff) + t.dirs('UDLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)
                else:
                    bindload  = t['bl']('as')
                    bindload2 = t['bl']('as','_s')
                    tgl = p.GetBindFile(bindload2)
                    cur.SetBind(key,t['ini'] + actPower_toggle(1,1,t['speed'],toff) + t.dirs('UDLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload2)
                    tgl.SetBind(key,t['ini'] + actPower_toggle(1,1,t['speed'],toff) + t.dirs('UDLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

            else:
                if (fix):
                    fix(p,t,key,makeSpeedModeKey,"s",bl,cur,toff,"f",feedback)
                else:
                    cur.SetBind(key, t['ini'] + actPower_toggle(1,1,t['speed'],toff) + '$$up 0' +  t['detaillo'] + t['flycamdist'] + feedback + t['bl']('fs'))




        t['ini'] = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeJumpModeKey(self, p, t, bl, cur, toff, fbl):
        key = t['JumpMode']
        if (t['canjmp'] and not p['SoD']['JumpSimple']):

            if p['SoD']['Feedback']: feedback = '$$tname, Superjump Mode'
            else:                    feedback = ''
            tgl = p.GetBindFile(fbl)

            if (bl == "j"):
                if (t['horizkeys'] + t['space'] > 0):
                    a = actPower(None,1,t['jump'],toff) + '$$up 1'
                else:
                    a = actPower(None,1,t['cjmp'],toff)

                bindload = t['bl']('j')
                tgl.SetBind(key, '-down' + a + t['detaillo'] + t['flycamdist'] + bindload)
                cur.SetBind(key, '+down' + feedback + BindFile.BLF(p, fbl))
            elif (bl == "aj"):
                bindload = t['bl']('aj')
                tgl.SetBind(key, '-down' + actPower(None,1,t['jump'],toff) + '$$up 1' + t['detaillo'] + t['flycamdist'] + t.dirs('DLR') + bindload)
                cur.SetBind(key, '+down' + feedback + BindFile.BLF(p, fbl))
            else:
                tgl.SetBind(key, '-down' + actPower(None,1,t['jump'],toff) + '$$up 1' + t['detaillo'] + t['flycamdist'] + t['bl']('fj'))
                cur.SetBind(key, '+down' + feedback + BindFile.BLF(p, fbl))


        t['ini'] = ''


    # TODO -- seems like these subs could get consolidated but stab one at that was feeble
    def makeFlyModeKey(self, p, t, bl, cur, toff, fix, fb, fb_on_a):
        key = t['FlyMode']
        if (not key or key == "UNBOUND"): return

        if p['SoD']['Feedback']: feedback = (fb or '$$tname, Flight Mode')
        else:                    feedback = ''

        if not t['ini']: t['ini'] = ''

        if (t['canhov'] + t['canfly'] > 0):
            if (bl == "bo"):
                bindload = t['bl']('bo')
                if (fix):
                    fix(p,t,key,makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(key,'+down$$' + actPower_toggle(1,1,t['flyx'],toff) + '$$up 1$$down 0' + t.dirs('FBLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

            elif (bl == "a"):
                if (not fb_on_a): feedback = ''
                bindload = t['bl']('a')

                if t['tkeys']: ton = t['flyx']
                else:          ton = t['hover']

                if (fix):
                    fix(p,t,key,makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(t['FlyMode'], t['ini'] + actPower_toggle(1,1, ton ,toff) + t.dirs('UDLR') + t['detaillo'] + t['flycamdist'] + feedback + bindload)

            elif (bl == "af"):
                bindload = t['bl']('af')
                if (fix):
                    fix(p,t,key,makeFlyModeKey,"f",bl,cur,toff,"a",feedback)
                else:
                    cur.SetBind(key, t['ini'] + actPower_toggle(1,1,t['flyx'],toff) + t['detaillo'] + t['flycamdist'] + t.dirs('DLR') + feedback + bindload)

            else:
                if (fix):
                    fix(p,t,key,makeFlyModeKey,"f",bl,cur,toff,"f",feedback)
                else:
                    cur.SetBind(key, t['ini'] + actPower_toggle(1,1,t['flyx'],toff) + t.dirs('UDFBLR') + t['detaillo'] + t['flycamdist'] + feedback + t['bl']('ff'))

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
                    cur.SetBind(key,t['ini'] + '$$up 1$$down 0' + actPower_toggle(None,1,t['gfly'],toff) + t.dirs('FBLR') + t['detaillo'] + t['flycamdist'] .bindload)

            elif (bl == "gaf"):
                bindload = t['bl']('gaf')
                if (fix):
                    fix(p,t,key,makeGFlyModeKey,"gf",bl,cur,toff,"a")
                else:
                    cur.SetBind(key,t['ini'] + t['detaillo'] + t['flycamdist'] + t.dirs('UDLR') + bindload)

            else:
                if (fix):
                    fix(p,t,key,makeGFlyModeKey,"gf",bl,cur,toff,"f")
                else:
                    if (bl == "gf"):
                        cur.SetBind(key,t['ini'] + actPower_toggle(1,1,t['gfly'],toff) + t['detaillo'] + t['flycamdist'] + t['bl']('gff'))
                    else:
                        cur.SetBind(key,t['ini'] + t['detaillo'] + t['flycamdist'] + t['bl']('gff'))




        t['ini'] = ''


    def iupMessage(self):
        print("ZOMG SOMEBODY IMPLEMENT A WARNING DIALOG!!!\n")

    def PopulateBindFiles(self):

        profile = self.Profile

        ResetFile = profile.ResetFile

        # ResetFile.SetBind(petselect['sel5'] + ' "petselect 5')
        if (self.State['Default'] == "NonSoD"):
            if (not self.State['NonSoD']):
                iupMessage("Notice","Enabling NonSoD mode, since it is set as your default mode.")
            self.State['NonSoD'] = 1

        if (self.State['Default'] == "Base" and not self.State['Base']):
            iupMessage("Notice","Enabling NonSoD mode and making it the default, since Sprint SoD, your previous Default mode, is not enabled.")
            self.State['NonSoD'] = 1
            self.State['Default'] = "NonSoD"

        if (self.State['Default'] == "Fly" and not (self.State['FlyHover'] or self.State['FlyFly'])):
            iupMessage("Notice","Enabling NonSoD mode and making it the default, since Flight SoD, your previous Default mode, is not enabled.")
            self.State['NonSoD'] = 1
            self.State['Default'] = "NonSoD"

        if (self.State['Default'] == "Jump" and not (self.State['JumpCJ'] or self.State['JumpSJ'])):
            iupMessage("Notice","Enabling NonSoD mode and making it the default, since Superjump SoD, your previous Default mode, is not enabled.")
            self.State['NonSoD'] = 1
            self.State['Default'] = "NonSoD"

        if (self.State['Default'] == "Run" and self.State['RunPrimaryNumber'] == 1):
            iupMessage("Notice","Enabling NonSoD mode and making it the default, since Superspeed SoD, your previous Default mode, is not enabled.")
            self.State['NonSoD'] = 1
            self.State['Default'] = "NonSoD"


        t = SoDTable({
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
        })

        if (self.State['JumpCJ'] and not self.State['JumpSJ']):
            t['cancj'] = 1
            t['cjmp'] = "Combat Jumping"
            t['jump'] = "Combat Jumping"

        if (not self.State['JumpCJ'] and self.State['JumpSJ']):
            t['canjmp'] = 1
            t['jump'] = "Super Jump"
            t['jumpifnocj'] = "Super Jump"

            t['cancj'] = 1
            t['canjmp'] = 1
            t['cjmp'] = "Combat Jumping"
            t['jump'] = "Super Jump"


        if (profile.Pages['General'].State['Archetype'] == "Peacebringer"):
            if (self.State['FlyHover']):
                t['canhov'] = 1
                t['canfly'] = 1
                t['hover'] = "Combat Flight"
                t['fly'] = "Energy Flight"
                t['flyx'] = "Energy Flight"
            else:
                t['canfly'] = 1
                t['hover'] = "Energy Flight"
                t['flyx'] = "Energy Flight"

        elif (not (profile.Pages['General'].State['Archetype'] == "Warshade")):
            if (self.State['FlyHover'] and not self.State['FlyFly']):
                t['canhov'] = 1
                t['hover'] = "Hover"
                t['flyx'] = "Hover"
                if (self.State['TPTPHover']): t['tphover'] = '$$powexectoggleon Hover'

            if (not self.State['FlyHover'] and self.State['FlyFly']):
                t['canfly'] = 1
                t['hover'] = "Fly"
                t['flyx'] = "Fly"

            if (self.State['FlyHover'] and self.State['FlyFly']):
                t['canhov'] = 1
                t['canfly'] = 1
                t['hover'] = "Hover"
                t['fly'] = "Fly"
                t['flyx'] = "Fly"
                if (self.State['TPTPHover']): t['tphover'] = '$$powexectoggleon Hover'


        if ((profile.Pages['General'].State['Archetype'] == "Peacebringer") and self.State['FlyQFly']):
            t['canqfly'] = 1

        if (self.State['FlyGFly']):
            t['cangfly'] = 1
            t['gfly'] = "Group Fly"
            if (self.State['TTPTPGFly']): t['ttpgfly'] = '$$powexectoggleon Group Fly'

        if (self.State['RunPrimaryNumber'] == 1):
            t['sprint'] = self.State['RunSecondary']
            t['speed']  = self.State['RunSecondary']
        else:
            t['sprint'] = self.State['RunSecondary']
            t['speed']  = self.State['RunPrimary']
            t['canss'] = 1

        if self.State['Unqueue'] : t['unqueue'] = '$$powexecunqueue'
        else:                      t['unqueue'] = ''
        if (self.State['AutoMouseLook']):
            t['mlon']  = '$$mouselook 1'
            t['mloff'] = '$$mouselook 0'

        if (self.State['RunUseCamdist']):
            t['runcamdist'] = '$$camdist ' + self.State['RunCamdist']

        if (self.State['FlyUseCamdist']):
            t['flycamdist'] = '$$camdist ' + self.State['FlyCamdist']

        if (self.State['Detail'] and self.State['DetailEnable']):
            t['detailhi'] = '$$visscale ' + self.State['DetailNormalAmt'] + '$$shadowvol 0$$ss 0'
            t['detaillo'] = '$$visscale ' + self.State['DetailMovingAmt'] + '$$shadowvol 0$$ss 0'


        if self.State['TPHideWindows']:
            windowhide = '$$windowhide health$$windowhide chat$$windowhide target$$windowhide tray'
            windowshow = '$$show health$$show chat$$show target$$show tray'
        else:
            windowhide = ''
            windowshow = ''

        # turn = "+zoomin$$-zoomin"  # a non functioning bind used only to activate the keydown/keyup functions of +commands
        t['turn'] = "+down";  # a non functioning bind used only to activate the keydown/keyup functions of +commands

        #  temporarily set self.State['Default'] to "NonSoD"
        # self.State['Default'] = "Base"
        #  set up the keys to be used.
        if (self.State['Default'] == "NonSoD") : t['NonSoDMode'] = self.State['NonSoDMode']
        if (self.State['Default'] == "Base")   : t['BaseMode'] = self.State['BaseMode']
        if (self.State['Default'] == "Fly")    : t['FlyMode'] = self.State['FlyMode']
        if (self.State['Default'] == "Jump")   : t['JumpMode'] = self.State['JumpMode']
        if (self.State['Default'] == "Run")    : t['RunMode'] = self.State['RunMode']
    #     if (self.State['Default'] == "GFly")  : t['GFlyMode'] = self.State['GFlyMode']
        t['TempMode'] = self.State['TempMode']
        t['QFlyMode'] = self.State['QFlyMode']

        for space in (0,1):
            t['space'] = space
            t['up'] = '$$up ' + space
            t['upx'] = '$$up ' + (1-space)

            for X in (0,1):
                t['X'] = X
                t['dow'] = '$$down ' + X
                t['dowx'] = '$$down ' + (1-X)

                for W in (0,1):
                    t['W'] = W
                    t['forw'] = '$$forward ' + W
                    t['forx'] = '$$forward ' + (1-W)

                    for S in (0,1):
                        t['S'] = S
                        t['bac'] = '$$backward ' + S
                        t['bacx'] = '$$backward ' + (1-S)

                        for A in (0,1):
                            t['A'] = A
                            t['lef'] = '$$left ' + A
                            t['lefx'] = '$$left ' + (1-A)

                            for D in (0,1):
                                t['D'] = D
                                t['rig'] = '$$right ' + D
                                t['rigx'] = '$$right ' + (1-D)

                                t['totalkeys'] = space+X+W+S+A+D;    # total number of keys down
                                t['horizkeys'] = W+S+A+D;    # total # of horizontal move keys.    So Sprint isn't turned on when jumping
                                t['vertkeys'] = space+X
                                t['jkeys'] = t['horizkeys']+t['space']

                                if (self.State['NonSoD'] or t['canqfly']):
                                    t[self.State['Default'] + "Mode"] = t['NonSoDMode']
                                    makeSoDFile({
                                        t : t,
                                        bl : 'n',
                                        bla : 'an',
                                        blf : 'fn',
                                        path : 'n',
                                        pathr : 'an',
                                        pathf : 'fn',
                                        mobile : '',
                                        stationary : '',
                                        modestr : "NonSoD",
                                    })
                                    t[self.State['Default'] + "Mode"] = None

                                if (self.State['Base']):
                                    t[self.State['Default'] + "Mode"] = t['BaseMode']
                                    makeSoDFile({
                                        t : t,
                                        bl : 'r',
                                        bla : 'gr',
                                        blf : 'fr',
                                        path : 'r',
                                        pathr : 'ar',
                                        pathf : 'fr',
                                        mobile : t['sprint'],
                                        stationary : '',
                                        modestr : "Base",
                                    })
                                    t[self.State['Default'] + "Mode"] = None

                                if (t['canss']):
                                    t[self.State['Default'] + "Mode"] = t['RunMode']
                                    if (self.State['SSSSSJModeEnable']): sssj = t['jump']
                                    if (self.State['SSMobileOnly']):
                                        makeSoDFile({
                                            t : t,
                                            bl : 's',
                                            bla : 'as',
                                            blf : 'fs',
                                            path : 's',
                                            pathr : 'as',
                                            pathf : 'fs',
                                            mobile : t['speed'],
                                            stationary : '',
                                            modestr : "Run",
                                            sssj : sssj,
                                        })
                                    else:
                                        makeSoDFile({
                                            t : t,
                                            bl : 's',
                                            bla : 'as',
                                            blf : 'fs',
                                            path : 's',
                                            pathr : 'as',
                                            pathf : 'fs',
                                            mobile : t['speed'],
                                            stationary : t['speed'],
                                            modestr : "Run",
                                            sssj : sssj,
                                        })

                                    t[self.State['Default'] + "Mode"] = None

                                if (t['canjmp']>0 and not (self.State['JumpSimple'])):
                                    t[self.State['Default'] + "Mode"] = t['JumpMode']
                                    if (t['jump'] == t['cjmp']): jturnoff = t['jumpifnocj']
                                    makeSoDFile({
                                        t : t,
                                        bl : 'j',
                                        bla : 'aj',
                                        blf : 'fj',
                                        path : 'j',
                                        pathr : 'aj',
                                        pathf : 'fj',
                                        mobile : t['jump'],
                                        stationary : t['cjmp'],
                                        modestr : "Jump",
                                        flight : "Jump",
                                        fix : sodJumpFix,
                                        turnoff : jturnoff,
                                    })
                                    t[self.State['Default'] + "Mode"] = None

                                if (t['canhov']+t['canfly']>0):
                                    t[self.State['Default'] + "Mode"] = t['FlyMode']
                                    makeSoDFile({
                                        t : t,
                                        bl : 'r',
                                        bla : 'af',
                                        blf : 'ff',
                                        path : 'r',
                                        pathr : 'af',
                                        pathf : 'ff',
                                        mobile : t['flyx'],
                                        stationary : t['hover'],
                                        modestr : "Fly",
                                        flight : "Fly",
                                        pathbo : 'bo',
                                        pathsd : 'sd',
                                        blbo : 'bo',
                                        blsd : 'sd',
                                    })
                                    t[self.State['Default'] + "Mode"] = None

                                if (t['canqfly']>0):
                                    t[self.State['Default'] + "Mode"] = t['QFlyMode']
                                    makeSoDFile({
                                        t : t,
                                        bl : 'q',
                                        bla : 'aq',
                                        blf : 'fq',
                                        path : 'q',
                                        pathr : 'aq',
                                        pathf : 'fq',
                                        mobile : "Quantum Flight",
                                        stationary : "Quantum Flight",
                                        modestr : "QFly",
                                        flight : "Fly",
                                    })
                                    t[self.State['Default'] + "Mode"] = None

                                if (t['cangfly']):
                                    t[self.State['Default'] + "Mode"] = t['GFlyMode']
                                    makeSoDFile({
                                        t : t,
                                        bl : 'a',
                                        bla : 'af',
                                        blf : 'ff',
                                        path : 'ga',
                                        pathr : 'gaf',
                                        pathf : 'gff',
                                        mobile : t['gfly'],
                                        stationary : t['gfly'],
                                        modestr : "GFly",
                                        flight : "GFly",
                                        pathbo : 'gbo',
                                        pathsd : 'gsd',
                                        blbo : 'gbo',
                                        blsd : 'gsd',
                                    })
                                    t[self.State['Default'] + "Mode"] = None

                                if (self.State['Temp'] and self.State['TempEnable']):
                                    trayslot = "1 " + self.State['TempTray']
                                    t[self.State['Default'] + "Mode"] = t['TempMode']
                                    makeSoDFile({
                                        t : t,
                                        bl : 't',
                                        bla : 'at',
                                        blf : 'ft',
                                        path : 't',
                                        pathr : 'at',
                                        pathf : 'ft',
                                        mobile : trayslot,
                                        stationary : trayslot,
                                        modestr : "Temp",
                                        flight : "Fly",
                                    })
                                    t[self.State['Default'] + "Mode"] = None


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

        if (self.State['TLeft']  and self.State['TLeft']  == "UNBOUND"):
            ResetFile.SetBind(self.State['TLeft'], "+turnleft")
        if (self.State['TRight'] and self.State['TRight'] == "UNBOUND"):
            ResetFile.SetBind(self.State['TRight'],"+turnright")

        if (self.State['Temp'] and self.State['TempEnable']):
            temptogglefile1 = profile.GetBindFile("temptoggle1.txt")
            temptogglefile2 = profile.GetBindFile("temptoggle2.txt")
            temptogglefile2.SetBind(self.State['TempTraySwitch'],'-down$$gototray 1'                     + BindFile.BLF(profile, 'temptoggle1.txt'))
            temptogglefile1.SetBind(self.State['TempTraySwitch'],'+down$$gototray ' + self.State['TempTray'] + BindFile.BLF(profile, 'temptoggle2.txt'))
            ResetFile.      SetBind(self.State['TempTraySwitch'],'+down$$gototray ' + self.State['TempTray'] + BindFile.BLF(profile, 'temptoggle2.txt'))


        if (profile.Pages['General'].State['Archetype'] == "Warshade"):
            dwarfTPPower  = "powexecname Black Dwarf Step"
            normalTPPower = "powexecname Shadow Step"
        elif (profile.Pages['General'].State['Archetype'] == "Peacebringer"):
            dwarfTPPower = "powexecname White Dwarf Step"
        else:
            normalTPPower = "powexecname Teleport"
            teamTPPower   = "powexecname Team Teleport"


        if (self.State['Human'] and self.State['HumanEnable']):
            humanBindKey = self.State['HumanMode']
            humanpbind = cbPBindToString(self.State['HumanHumanPBind'],profile)
            novapbind  = cbPBindToString(self.State['HumanNovaPBind'], profile)
            dwarfpbind = cbPBindToString(self.State['HumanDwarfPBind'],profile)

        if ((profile.Pages['General'].State['Archetype'] == "Peacebringer") or (profile.Pages['General'].State['Archetype'] == "Warshade")):
            if (humanBindKey):
                ResetFile.SetBind(humanBindKey,humanpbind)

        #  kheldian form support
        #  create the Nova and Dwarf form support files if enabled.
        Nova =  self.State['Nova']
        Dwarf = self.State['Dwarf']

        fullstop = '$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'

        if (Nova and Nova['Enable']):
            ResetFile.SetBind(Nova['Mode'], f"tname, Changing to {Nova['Nova']} Form{fullstop}{t['on']}{Nova['Nova']}$$gototray {Nova['Tray']}" + BindFile.BLF(profile, 'nova.txt'))

            novafile = profile.GetBindFile("nova.txt")

            if (Dwarf and Dwarf['Enable']):
                novafile.SetBind(Dwarf['Mode'],f"tname, Changing to {Dwarf['Dwarf']} Form{fullstop}{t['off']}{Nova['Nova']}{t['on']}{Dwarf['Dwarf']}$$gototray {Dwarf['Tray']}" + BindFile.BLF(profile, 'dwarf.txt'))

            if not humanBindKey:
                humanBindKey = Nova['Mode']

            if self.State['UseHumanFormPower']: humpower = '$$powexectoggleon ' + self.State['HumanFormShield']
            else:                               humpower = ''

            novafile.SetBind(humanBindKey,f"tname, Changing to Human Form, SoD Mode{fullstop}$$powexectoggleoff {Nova['Nova']} {humpower} $$gototray 1" + BindFile.BLF(profile, 'reset.txt'))

            if (humanBindKey == Nova['Mode']): humanBindKey = None

            if novapbind: novafile.SetBind(Nova['Mode'],novapbind)

            if t['canqfly']: makeQFlyModeKey(profile,t,"r",novafile,Nova['Nova'],"Nova")

            novafile.SetBind(self.State['Forward'],"+forward")
            novafile.SetBind(self.State['Left'],"+left")
            novafile.SetBind(self.State['Right'],"+right")
            novafile.SetBind(self.State['Back'],"+backward")
            novafile.SetBind(self.State['Up'],"+up")
            novafile.SetBind(self.State['Down'],"+down")
            novafile.SetBind(self.State['AutoRun'],"++forward")
            novafile.SetBind(self.State['FlyMode'],'nop')
            if (self.State['FlyMode'] != self.State['RunMode']):
                novafile.SetBind(self.State['RunMode'],'nop')
            if (self.State['MouseChord']):
                novafile.SetBind('mousechord "' + "+down$$+forward")

            if (self.State['TP'] and self.State['TPEnable']):
                novafile.SetBind(self.State['TPComboKey'],'nop')
                novafile.SetBind(self.State['TPBindKey'],'nop')
                novafile.SetBind(self.State['TPResetKey'],'nop')

            novafile.SetBind(self.State['Follow'],"follow")
            # novafile.SetBind(self.State['ToggleKey'],'tname, Changing to Human Form, Normal Mode$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0$$powexectoggleoff ' + Nova['Nova'] + '$$gototray 1' + BindFile.BLF(profile, 'reset.txt'))


        if (Dwarf and Dwarf['Enable']):
            ResetFile.SetBind(Dwarf['Mode'],f"tname, Changing to {Dwarf['Dwarf']} Form{fullstop}$$powexectoggleon {Dwarf['Dwarf']}$$gototray {Dwarf['Tray']}" + BindFile.BLF(profile, 'dwarf.txt'))
            dwrffile = profile.GetBindFile("dwarf.txt")
            if (Nova and Nova['Enable']):
                dwrffile.SetBind(Nova['Mode'],f"tname, Changing to {Nova['Nova']} Form{fullstop}$$powexectoggleoff {Dwarf['Dwarf']}$$powexectoggleon {Nova['Nova']}$$gototray {Nova['Tray']}" + BindFile.BLF(profile, 'nova.txt'))

            if not humanBindKey: humanBindKey = Dwarf['Mode']
            if self.State['UseHumanFormPower']: humpower = '$$powexectoggleon ' + self.State['HumanFormShield']
            else:                               humpower = ''

            dwrffile.SetBind(humanBindKey,f"t $name, Changing to Human Form, SoD Mode{fullstop}$$powexectoggleoff {Dwarf['Dwarf']}{humpower}$$gototray 1" + BindFile.BLF(profile, 'reset.txt'))

            if dwarfpbind: dwrffile.SetBind(Dwarf['Mode'],dwarfpbind)
            if t['canqfly']:
                makeQFlyModeKey(profile,t,"r",dwrffile,Dwarf['Dwarf'],"Dwarf")

            dwrffile.SetBind(self.State['Forward'],"+forward")
            dwrffile.SetBind(self.State['Left'],"+left")
            dwrffile.SetBind(self.State['Right'],"+right")
            dwrffile.SetBind(self.State['Back'],"+backward")
            dwrffile.SetBind(self.State['Up'],"+up")
            dwrffile.SetBind(self.State['Down'],"+down")
            dwrffile.SetBind(self.State['AutoRun'],"++forward")
            dwrffile.SetBind(self.State['FlyMode'],'nop')
            dwrffile.SetBind(self.State['Follow'],"follow")
            if (self.State['FlyMode'] != self.State['RunMode']):
                dwrffile.SetBind(self.State['RunMode'],'nop')
            if (self.State['MouseChord']):
                dwrffile.SetBind('mousechord "' + "+down$$+forward")

            if (self.State['TP'] and self.State['TPEnable']):
                dwrffile.SetBind(self.State['TPComboKey'],'+down$$' + dwarfTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'dtp','tp_on1.txt'))
                dwrffile.SetBind(self.State['TPBindKey'],'nop')
                dwrffile.SetBind(self.State['TPResetKey'],substr(t['detailhi'],2) + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'dtp','tp_off.txt'))
                #  Create tp_off file
                tp_off = profile.GetBindFile("dtp","tp_off.txt")
                tp_off.SetBind(self.State['TPComboKey'],'+down$$' + dwarfTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'dtp','tp_on1.txt'))
                tp_off.SetBind(self.State['TPBindKey'],'nop')

                tp_on1 = profile.GetBindFile("dtp","tp_on1.txt")
                tp_on1.SetBind(self.State['TPComboKey'],'-down$$powexecunqueue' + t['detailhi'] + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'dtp','tp_off.txt'))
                tp_on1.SetBind(self.State['TPBindKey'],'+down' + BindFile.BLF(profile, 'dtp','tp_on2.txt'))

                tp_on2 = profile.GetBindFile("dtp","tp_on2.txt")
                tp_on2.SetBind(self.State['TPBindKey'],'-down$$' + dwarfTPPower + BindFile.BLF(profile, 'dtp','tp_on1.txt'))

            dwrffile.SetBind(self.State['ToggleKey'],"t $name, Changing to Human Form, Normal Mode$fullstop\$\$powexectoggleoff Dwarf['Dwarf']\$\$gototray 1" + BindFile.BLF(profile, 'reset.txt'))


        if (self.State['JumpSimple']):
            if (self.State['JumpCJ'] and self.State['JumpSJ']):
                ResetFile.SetBind(self.State['JumpMode'],'powexecname Super Jump$$powexecname Combat Jumping')
            elif (self.State['JumpSJ']):
                ResetFile.SetBind(self.State['JumpMode'],'powexecname Super Jump')
            elif (self.State['JumpCJ']):
                ResetFile.SetBind(self.State['JumpMode'],'powexecname Combat Jumping')



        if (self.State['TP'] and self.State['TPEnable'] and not normalTPPower):
            ResetFile.SetBind(self.State['TPComboKey'],'nop')
            ResetFile.SetBind(self.State['TPBindKey'],'nop')
            ResetFile.SetBind(self.State['TPResetKey'],'nop')

        if (self.State['TP'] and self.State['TPEnable'] and not (profile.Pages['General'].State['Archetype'] == "Peacebringer") and normalTPPower):
            tphovermodeswitch = ''
            if (t['tphover'] == ''):
                tphovermodeswitch = re.sub('\d\d\d\d\d\d', '000000', t['bl']('r'))

            ResetFile.SetBind(self.State['TPComboKey'],'+down$$' + normalTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'tp','tp_on1.txt'))
            ResetFile.SetBind(self.State['TPBindKey'],'nop')
            ResetFile.SetBind(self.State['TPResetKey'],substr(t['detailhi'],2) + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'tp','tp_off.txt') + tphovermodeswitch)
            #  Create tp_off file
            tp_off = profile.GetBindFile("tp","tp_off.txt")
            tp_off.SetBind(self.State['TPComboKey'],'+down$$' + normalTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'tp','tp_on1.txt'))
            tp_off.SetBind(self.State['TPBindKey'],'nop')

            tp_on1 = profile.GetBindFile("tp","tp_on1.txt")
            zoomin = t['detailhi'] + t['runcamdist']
            if (t['tphover']): zoomin = ''
            tp_on1.SetBind(self.State['TPComboKey'],'-down$$powexecunqueue' + zoomin + windowshow + BindFile.BLF(profile, 'tp','tp_off.txt') + tphovermodeswitch)
            tp_on1.SetBind(self.State['TPBindKey'],'+down' + t['tphover'] + BindFile.BLF(profile, 'tp','tp_on2.txt'))

            tp_on2 = profile.GetBindFile("tp","tp_on2.txt")
            tp_on2.SetBind(self.State['TPBindKey'],'-down$$' + normalTPPower + BindFile.BLF(profile, 'tp','tp_on1.txt'))

        if (self.State['TTP'] and self.State['TTPEnable'] and not (profile.Pages['General'].State['Archetype'] == "Peacebringer") and teamTPPower) :
            tphovermodeswitch = ''
            ResetFile.SetBind(self.State['TTPComboKey'],'+down$$' + teamTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'ttp','ttp_on1.txt'))
            ResetFile.SetBind(self.State['TTPBindKey'],'nop')
            ResetFile.SetBind(self.State['TTPResetKey'],substr(t['detailhi'],2) + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'ttp','ttp_off') + tphovermodeswitch)
            #  Create tp_off file
            ttp_off = profile.GetBindFile("ttp","ttp_off.txt")
            ttp_off.SetBind(self.State['TTPComboKey'],'+down$$' + teamTPPower + t['detaillo'] + t['flycamdist'] + windowhide + BindFile.BLF(profile, 'ttp','ttp_on1.txt'))
            ttp_off.SetBind(self.State['TTPBindKey'],'nop')

            ttp_on1 = profile.GetBindFile("ttp","ttp_on1.txt")
            ttp_on1.SetBind(self.State['TTPComboKey'],'-down$$powexecunqueue' + t['detailhi'] + t['runcamdist'] + windowshow + BindFile.BLF(profile, 'ttp','ttp_off') + tphovermodeswitch)
            ttp_on1.SetBind(self.State['TTPBindKey'],'+down' + BindFile.BLF(profile, 'ttp','ttp_on2.txt'))

            ttp_on2 = profile.GetBindFile("ttp","ttp_on2.txt")
            ttp_on2.SetBind(self.State['TTPBindKey'],'-down$$' + teamTPPower + BindFile.BLF(profile, 'ttp','ttp_on1.txt'))



    def sodResetKey(self, curfile, p, path, turnoff, moddir):

        path = re.sub('\d\d\d\d\d\d', '000000', path)

        if (moddir == 'up')  : u = 1
        else:                   u = 0
        if (moddir == 'down'): d = 1
        else:                   d = 0
        curfile.SetBind(p.Pages['General']['Reset Key'],
                'up ' + u + '$$down ' + d + '$$forward 0$$backward 0$$left 0$$right 0' .
                turnoff + '$$tname, SoD Binds Reset' + BindFile.BaseReset(p) + BindFile.BLF(p, path)
        )


    def sodDefaultResetKey(self, mobile, stationary):
        return
        # TODO -- decide where to keep 'resetstring' and make this sub update it.
        #cbAddReset('up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'.actPower_name(None,1,stationary,mobile) + '$$tname, SoD Binds Reset')



    # TODO TODO TODO -- the s/\d\d\d\d\d\d/$newbits/ scheme in the following six subs is a vile evil (live veil ilve vlie) hack.
    def sodUpKey(self, t, bl, curfile, state, mobile, stationary, flight, autorun, followbl, bo, sssj):

        (upx,dow,forw,bac,lef,rig) = (t['upx'],t.D,t.F,t.B,t.L,t.R)

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
            Nonetoggleon


        if (t['totalkeys'] == 1 and t['space'] == 1):
           ml = t['mloff']
           if (not (stationary and (mobile == stationary))) : toggleoff = mobile
           toggleon = stationary
        else:
            Nonetoggleoff

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


        if (toggleon or toggleoff):
           toggle = actPower_name(None,1,toggleon,toggleoff,toggleoff2)


        newbits = t.KeyState({'toggle' : 'space'})
        bl = re.sub('\d\d\d\d\d\d', newbits, bl)

        if t['space'] == 1: ini = '-down'
        else:               ini = '+down'

        if (followbl):
            move = ''
            if (t['space'] != 1):
                bl = re.sub('\d\d\d\d\d\d', '000000', followbl)
                move = upx + dow + forw + bac + lef + rig

            curfile.SetBind(self.State['Up'],ini + move + bl)
        elif (notautorun):
            curfile.SetBind(self.State['Up'],ini + upx + dow + forw + bac + lef + rig + ml + toggle + bl)
        else:
            if (not sssj) : toggle = ''  #  returns the following line to the way it was before sssj
            curfile.SetBind(self.State['Up'],ini + upx + dow + '$$backward 0' + lef + rig + toggle + t['mlon'] + bl)



    def sodDownKey(self,t,bl,curfile,state,mobile,stationary,flight,autorun,followbl,bo,sssj):

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
                move = up + dowx + forw + bac + lef + rig

            curfile.SetBind(self.State['Down'],ini + move + bl)
        elif (notautorun):
            curfile.SetBind(self.State['Down'],ini + up + dowx + forw + bac + lef + rig + ml + toggle + bl)
        else:
            curfile.SetBind(self.State['Down'],ini + up + dowx + '$$backward 0' + lef + rig + t['mlon'] + bl)


    def sodForwardKey(self, t, bl, curfile, state, mobile, stationary, flught, autorunbl, followbl, bo, sssj):
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
                move = ini + up + dow + forx + bac + lef + rig

            curfile.SetBind(self.State['Forward'], move + bl)
            if (self.State['MouseChord']):
                if (t['W'] == 1) : move = ini + up + dow + forx + bac + rig + lef
                curfile.SetBind('mousechord', move + bl)

        elif (notautorunbl):
            curfile.SetBind(self.State['Forward'], ini + up + dow + forx + bac + lef + rig + ml + toggle + bl)
            if (self.State['MouseChord']):
                curfile.SetBind('mousechord', ini + up + dow + forx + bac + rig + lef + ml + toggle + bl)

        else:
            if (t['W'] == 1):
                bl = re.sub('\d\d\d\d\d\d', newbits, autorunbl)

            curfile.SetBind(self.State['Forward'], ini + up + dow + '$$forward 1$$backward 0' + lef + rig + t['mlon'] + bl)
            if (self.State['MouseChord']) :
                curfile.SetBind('mousechord', ini + up + dow + '$$forward 1$$backward 0' + rig + lef + t['mlon'] + bl)

    def sodBackKey(t,bl,curfile,state,mobile,stationary,flight,autorunbl,followbl,bo,sssj):
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
                move = ini + up + dow + forw + bacx + lef + rig

            curfile.SetBind(self.State['Back'], move + bl)
        elif (notautorunbl) :
            curfile.SetBind(self.State['Back'], ini + up + dow + forw + bacx + lef + rig + ml + toggle + bl)
        else:
            if (t['S'] == 1):
                move = '$$forward 1$$backward 0'
            else:
                move = '$$forward 0$$backward 1'
                bl = re.sub('\d\d\d\d\d\d', newbits, autorunbl)

            curfile.SetBind(self.State['Back'], ini + up + dow + move + lef + rig + t['mlon'] + bl)

    def sodLeftKey(t,bl,curfile,state,mobile,stationary,flight,autorun,followbl,bo,sssj):
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
                move = ini + up + dow + forw + bac + lefx + rig

            curfile.SetBind(self.State['Left'],move + bl)
        elif (notautorun) :
            curfile.SetBind(self.State['Left'],ini + up + dow + forw + bac + lefx + rig + ml + toggle + bl)
        else:
            curfile.SetBind(self.State['Left'],ini + up + dow + '$$backward 0' + lefx + rig + t['mlon'] + bl)

    def sodRightKey(t,bl,curfile,state,mobile,stationary,flight,autorun,followbl,bo,sssj):
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
                move = ini + up + dow + forw + bac + lef + rigx

            curfile.SetBind(self.State['Right'], move + bl)
        elif (notautorun) :
            curfile.SetBind(self.State['Right'], ini + up + dow + forw + bac + lef + rigx + ml + toggle + bl)
        else:
            curfile.SetBind(self.State['Right'], ini + up + dow + '$$forward 1$$backward 0' + lef + rigx + t['mlon'] + bl)


    def sodAutoRunKey(t,bl,curfile,state,mobile,sssj):
        if (sssj and t['space'] == 1) :
            curfile.SetBind(self.State['AutoRun'],'forward 1$$backward 0' + t.dirs('UDLR') + t['mlon'] + actPower_name(None,1,sssj,mobile) + bl)
        else:
            curfile.SetBind(self.State['AutoRun'],'forward 1$$backward 0' + t.dirs('UDLR') + t['mlon'] + actPower_name(None,1,mobile) + bl)

    def sodAutoRunOffKey(t,bl,curfile,state,mobile,stationary,flight,sssj):
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
        curfile.SetBind(self.State['AutoRun'], t.dirs('UDFBLR') + toggleon + bindload)


    def sodFollowKey(t,bl,curfile,state,mobile):
        curfile.SetBind(self.State['Follow'],'follow' + actPower_name(None,1,mobile) + bl + t.KeyState + '.txt')

    def sodFollowOffKey(t,bl,curfile,state,mobile,stationary,flight):
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

        curfile.SetBind(self.State['Follow'],"follow" + toggle + t.U + t['dow'] + t.F + t.B + t.L + t.R + bl + t.KeyState + '.txt')


    def bindisused(self):
        return self.State['Enable']


    def findconflicts(self):
        Utility.CheckConflict(self.State,"Up","Up Key")
        Utility.CheckConflict(self.State,"Down","Down Key")
        Utility.CheckConflict(self.State,"Forward","Forward Key")
        Utility.CheckConflict(self.State,"Back","Back Key")
        Utility.CheckConflict(self.State,"Left","Strafe Left Key")
        Utility.CheckConflict(self.State,"Right","Strafe Right Key")
        Utility.CheckConflict(self.State,"TLeft","Turn Left Key")
        Utility.CheckConflict(self.State,"TRight","Turn Right Key")
        Utility.CheckConflict(self.State,"AutoRun","AutoRun Key")
        Utility.CheckConflict(self.State,"Follow","Follow Key")

        if (self.State['NonSoD'])       : Utility.CheckConflict(self.State,"NonSoDMode","NonSoD Key")
        if (self.State['Base'])         : Utility.CheckConflict(self.State,"BaseMode","Sprint Mode Key")
        if (self.State['SSSS'])         : Utility.CheckConflict(self.State,"RunMode","Speed Mode Key")
        if (self.State['JumpCJ']
                or self.State['JumpSJ'] ): Utility.CheckConflict(self.State,"JumpMode","Jump Mode Key")
        if (self.State['FlyHover']
                or self.State['FlyFly'] ): Utility.CheckConflict(self.State,"FlyMode","Fly Mode Key")
        if (self.State['FlyQFly']
                and (profile.Pages['General'].State['Archetype'] == "Peacebringer")): Utility.CheckConflict(self.State,"QFlyMode","Q.Fly Mode Key")
        if (self.State['TP'] and self.State['TPEnable']):
            Utility.CheckConflict(self.State['TP'],"ComboKey","TP ComboKey")
            Utility.CheckConflict(self.State['TP'],"ResetKey","TP ResetKey")

            TPQuestion = "Teleport Bind"
            if (profile.Pages['General'].State['Archetype'] == "Peacebringer") :
               TPQuestion = "Dwarf Step Bind"
            elif (profile.Pages['General'].State['Archetype'] == "Warshade") :
               TPQuestion = "Shd/Dwf Step Bind"

            Utility.CheckConflict(self.State['TP'],"BindKey", TPQuestion)

            if (self.State['FlyGFly']): Utility.CheckConflict(self.State,"GFlyMode","Group Fly Key")
        if (self.State['TTP'] and self.State['TTPEnable']):
            Utility.CheckConflict(self.State['TTP'],"ComboKey","TTP ComboKey")
            Utility.CheckConflict(self.State['TTP'],"ResetKey","TTP ResetKey")
            Utility.CheckConflict(self.State['TTP'],"BindKey","Team TP Bind")

        if (self.State['Temp'] and self.State['TempEnable']):
            Utility.CheckConflict(self.State,"TempMode","Temp Mode Key")
            Utility.CheckConflict(self.State['Temp'],"TraySwitch","Tray Toggle Key")

        if ((profile.Pages['General'].State['Archetype'] == "Peacebringer") or (profile.Pages['General'].State['Archetype'] == "Warshade")) :
            if (self.State['Nova']  and self.State['NovaEnable']): Utility.CheckConflict(self.State['Nova'], "Mode","Nova Form Bind")
            if (self.State['Dwarf'] and self.State['DwarfEnable']): Utility.CheckConflict(self.State['Dwarf'],"Mode","Dwarf Form Bind")


    #  toggleon variation
    def actPower_toggle(self, start, unq, on, *rest):
        if (refon):
            #  deal with power slot stuff..
           traytest = on['trayslot']

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
        #         if ($v and ($v ne 'on') and notoffpower[$v]) {
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
        if (refon):
            #  deal with power slot stuff..
           traytest = on['trayslot']

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
    # # local actPower = actPower_toggle

    def sodJumpFix(self, profile,t,key,makeModeKey,suffix,bl,curfile,turnoff,autofollowmode,feedback):

        filename = t['path']("${autofollowmode}j",suffix)
        tglfile = profile.GetBindFile(filename)
        t['ini'] = '-down$$'
        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key,"+down" + feedback + actPower_name(None,1,t['cjmp']) + BindFile.BLF(profile,filename))


    def sodSetDownFix(self, profile,t,key,makeModeKey,suffix,bl,curfile,turnoff,autofollowmode,feedback):
        if autofollowmode:
            pathsuffix = "f"
        else:
            pathsuffix = "a"

        filename = t['path']("$autofollowmodepathsuffix",suffix)
        tglfile = profile.GetBindFile(filename)
        t['ini'] = '-down$$'
        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key,'+down' + feedback + BindFile.BLF(profile,filename))



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
        'TPAutoHover' : 'Automatically use Hover when Teleporting',

        'TTPMode'  : 'Team Teleport Bind',
        'TTPCombo' : 'Team Teleport Combo Key',
        'TTPReset' : 'Team Teleport Reset Key',
        'TTPAutoGFly' : 'Automatically use Group Fly when Team Teleporting',

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

class t():

    def KeyState(self, p):
        togglebit = p['toggle']

        for key in ('space','X','W','S','A','D'):
            if key == togglebit:
                ret = ret + nott[key]
            else:
                ret = ret + self[key]

        return ret


    # These next two subs are terrible.  This stuff should all be squirreled away in BindFile.

#    # This will return "$bindloadfilesilent C:\path\CODE\CODE1010101<suffix>.txt"
#    sub bl {
#        my self = shift
#        code = shift
#        suffix = shift || ''
#        p = self['profile']
#        return BindFile.BLF($p, uc($code), uc($code) + self.KeyState + suffix + '.txt')
#
#
#    # This will return "CODE\CODE1010101<suffix>.txt"
#    sub path {
#        my self = shift
#        code = shift
#        suffix = shift || ''
#        return File::Spec.catpath(None, uc($code), uc($code) + self.KeyState + suffix + '.txt')
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
