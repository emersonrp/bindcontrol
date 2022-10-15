import wx
import re
import GameData
import UI
from pathlib import Path, PureWindowsPath
from KeyBind import ControlKeyBind, FileKeyBind
from Page import Page
from UI.ControlGroup import ControlGroup, bcKeyButton

class SoD(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Speed On Demand"

        self.Init = {
            'EnableSoD'       : True,

            'Up'              : "SPACE",
            'Down'            : "X",
            'Forward'         : "W",
            'Back'            : "S",
            'Left'            : "A",
            'Right'           : "D",
            'TurnLeft'        : "Q",
            'TurnRight'       : "E",
            'AutoRun'         : "R",
            'Follow'          : "TILDE",
            'DefaultMode'     : "Sprint",
            'MouseChord'      : 0,
            'AutoMouseLook'   : 0,

            'SprintPower'     : 'Sprint',
            'SprintSoD'       : True,  # "Base" in citybinder
            'SprintMode'      : '',

            'ChangeCamera'    : False,
            'CamdistBase'     : 15,
            'CamdistMove'     : 60,
            'ChangeDetail'    : False,
            'DetailBase'      : 100,
            'DetailMove'      : 50,
            'Feedback'        : False,

            'NonSoDEnable'    : False,
            'NonSoDMode'      : 'CTRL+M',

            'HasSS'           : True,
            'RunMode'         : "C",
            'SSMobileOnly'    : False,
            'SSSJModeEnable'  : False,

            'HasSJ'           : False,
            'HasCJ'           : False,
            'JumpMode'        : "T",
            'SimpleSJCJ'      : False,

            'HasHover'        : False,
            'HasFly'          : False,
            'HasCF'           : False,
            'FlyMode'         : "F",
            'HasQF'           : False,
            'QFlyMode'        : "G",

            'HasTP'           : True,
            'TPBindKey'       : 'LSHIFT+LBUTTON',
            'TPComboKey'      : 'LSHIFT',
            'TPResetKey'      : 'LCTRL+T',

            'HasTTP'          : False,
            'TTPBindKey'      : 'LSHIFT+CTRL+LBUTTON',
            'TTPComboKey'     : 'LSHIFT+CTRL',
            'TTPResetKey'     : 'LSHIFT+CTRL+T',
            'TTPAutoGFly'     : True,

            'TPHideWindows'   : True,
            'TPTPHover'       : False,

            'FlyGFly'         : '',

            'UseNova'         : False,
            'NovaMode'        : "T",
            'NovaTray'        : "4",

            'UseDwarf'        : False,
            'DwarfMode'       : "G",
            'DwarfTray'       : "5",

            'HumanMode'       : "",
            'HumanTray'       : "1",
            'HumanHumanPBind' : "nop",
            'HumanNovaPBind'  : "nop",
            'HumanDwarfPBind' : "nop",

            'TempEnable'      : False,
            'TempTray'        : "6",
            'TempTraySwitch'  : "",
            'TempMode'        : "",
        }

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


    def BuildPage(self):

        topSizer = wx.FlexGridSizer(0,2,10,10)
        EnableSoD = wx.CheckBox( self, -1, "Enable Speed On Demand Binds",  )

        topSizer.Add(EnableSoD, 0, wx.TOP|wx.LEFT, 10)
        topSizer.AddSpacer(1)
        self.Ctrls['EnableSoD'] = EnableSoD
        EnableSoD.Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        EnableSoD.SetValue(self.Init['EnableSoD'])

        self.leftColumn  = wx.BoxSizer(wx.VERTICAL)
        self.rightColumn = wx.BoxSizer(wx.VERTICAL)


        ##### MOVEMENT KEYS
        movementSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label = "Movement Keys")
        staticbox = movementSizer.GetStaticBox()
        innerSizer = wx.BoxSizer(wx.HORIZONTAL)
        movementSizer.Add(innerSizer, 1, wx.ALL|wx.ALIGN_CENTER, 10)

        keySizer = wx.GridBagSizer(3, 3)
        innerSizer.Add(keySizer)
        tlLabel = wx.StaticText(staticbox, label = 'Turn Left')
        keySizer.Add(tlLabel, [0,0], flag = wx.ALIGN_CENTER)
        fwLabel = wx.StaticText(staticbox, label = 'Forward')
        keySizer.Add(fwLabel, [0,1], flag = wx.ALIGN_CENTER)
        trLabel = wx.StaticText(staticbox, label = 'Turn Right')
        keySizer.Add(trLabel, [0,2], flag = wx.ALIGN_CENTER)

        tleftButton = bcKeyButton(staticbox, -1, '')
        tleftButton.SetLabel(self.Init['TurnLeft'])
        self.Ctrls['TurnLeft'] = tleftButton
        tleftButton.CtlName = 'TurnLeft'
        tleftButton.CtlLabel = tlLabel
        tleftButton.Page = self
        tleftButton.Profile = self.Profile
        tleftButton.KeyBind = ControlKeyBind(self.Init['TurnLeft'], 'Turn Left', self.TabTitle)
        keySizer.Add(tleftButton, [1,0])

        forwardButton = bcKeyButton(staticbox, -1, '')
        self.Ctrls['Forward'] = forwardButton
        forwardButton.SetLabel(self.Init['Forward'])
        forwardButton.CtlName = 'Forward'
        forwardButton.CtlLabel = fwLabel
        forwardButton.Page = self
        forwardButton.Profile = self.Profile
        forwardButton.KeyBind = ControlKeyBind(self.Init['Forward'], 'Forward', self.TabTitle)
        keySizer.Add(forwardButton, [1,1])

        trightButton = bcKeyButton(staticbox, -1, '')
        self.Ctrls['TurnRight'] = trightButton
        trightButton.SetLabel(self.Init['TurnRight'])
        trightButton.CtlName = 'TurnRight'
        trightButton.CtlLabel = trLabel
        trightButton.Page = self
        trightButton.Profile = self.Profile
        trightButton.KeyBind = ControlKeyBind(self.Init['TurnRight'], 'TurnRight', self.TabTitle)
        keySizer.Add(trightButton, [1,2])

        leftLabel = wx.StaticText(staticbox, label = 'Left')
        backLabel = wx.StaticText(staticbox, label = 'Back')
        rightLabel = wx.StaticText(staticbox, label = 'Right')

        leftButton = bcKeyButton(staticbox, -1, '')
        self.Ctrls['Left'] = leftButton
        leftButton.SetLabel(self.Init['Left'])
        leftButton.CtlName = 'Left'
        leftButton.CtlLabel = leftLabel
        leftButton.Page = self
        leftButton.Profile = self.Profile
        leftButton.KeyBind = ControlKeyBind(self.Init['Left'], 'Left', self.TabTitle)
        keySizer.Add(leftButton, [2,0])

        backButton = bcKeyButton(staticbox, -1, '')
        backButton.SetLabel(self.Init['Back'])
        self.Ctrls['Back'] = backButton
        backButton.CtlName = 'Back'
        backButton.CtlLabel = backLabel
        backButton.Page = self
        backButton.Profile = self.Profile
        backButton.KeyBind = ControlKeyBind(self.Init['Back'], 'Back', self.TabTitle)
        keySizer.Add(backButton, [2,1])

        rightButton = bcKeyButton(staticbox, -1, '')
        self.Ctrls['Right'] = rightButton
        rightButton.SetLabel(self.Init['Right'])
        rightButton.CtlName = 'Right'
        rightButton.CtlLabel = rightLabel
        rightButton.Page = self
        rightButton.Profile = self.Profile
        rightButton.KeyBind = ControlKeyBind(self.Init['Right'], 'Right', self.TabTitle)
        keySizer.Add(rightButton, [2,2])

        keySizer.Add(leftLabel, [3,0], flag = wx.ALIGN_CENTER)
        keySizer.Add(backLabel, [3,1], flag = wx.ALIGN_CENTER)
        keySizer.Add(rightLabel, [3,2], flag = wx.ALIGN_CENTER)

        downLabel = wx.StaticText(staticbox, label = 'Down')
        upLabel   = wx.StaticText(staticbox, label = 'Up')

        downButton = bcKeyButton(staticbox, -1, '')
        self.Ctrls['Down'] = downButton
        downButton.SetLabel(self.Init['Down'])
        downButton.CtlName = 'Down'
        downButton.CtlLabel = downLabel
        downButton.Page = self
        downButton.Profile = self.Profile
        downButton.KeyBind = ControlKeyBind(self.Init['Down'], 'Down', self.TabTitle)
        keySizer.Add(downButton, [4,0], [1,1], wx.TOP, 10)

        upButton = bcKeyButton(staticbox, -1, '')
        self.Ctrls['Up'] = upButton
        upButton.SetLabel(self.Init['Up'])
        upButton.CtlName = 'Up'
        upButton.CtlLabel = upLabel
        upButton.Page = self
        upButton.Profile = self.Profile
        upButton.KeyBind = ControlKeyBind(self.Init['Up'], 'Up', self.TabTitle)
        keySizer.Add(upButton, [4,1], [1,2], wx.EXPAND|wx.TOP, 10)

        keySizer.Add(downLabel, [5,0], [1,1], flag = wx.ALIGN_CENTER)
        keySizer.Add(upLabel,   [5,1], [1,2], flag = wx.ALIGN_CENTER)

        #mcSizer = wx.FlexGridSizer(2,1,5,5)
        #mcSizer.AddGrowableCol(0)
        mcSizer = wx.BoxSizer(wx.HORIZONTAL)
        mcLabel = wx.StaticText(staticbox, -1, UI.Labels['MouseChord'] + ":")
        mcSizer.Add(mcLabel, 0, wx.LEFT|wx.RIGHT, 5)
        mcLabel.Bind(wx.EVT_LEFT_DOWN, self.onCBLabelClick)
        mousechord = wx.CheckBox(staticbox, -1)
        self.Ctrls['MouseChord'] = mousechord
        mousechord.SetValue(bool(self.Init['MouseChord']))
        mousechord.CtlName = 'MouseChord'
        mousechord.CtlLabel = mcLabel
        mcLabel.control = mousechord
        mousechord.Page = self
        mousechord.Profile = self.Profile
        mousechord.KeyBind = ControlKeyBind(self.Init['MouseChord'], 'MouseChord', self.TabTitle)
        mcSizer.Add(mousechord, 0, wx.RIGHT, 10)

        movementSizer.Add(mcSizer, 0, wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        self.leftColumn.Add(movementSizer, 0, wx.EXPAND)

        ##### GENERAL SETTINGS
        generalSizer = ControlGroup(self, self, 'General Settings')

        generalSizer.AddControl( ctlName = 'DefaultMode', ctlType = 'choice',
            contents = ('No SoD','Sprint','Super Speed','Jump','Fly'),)
        self.Ctrls['DefaultMode'].Bind(wx.EVT_CHOICE, self.SynchronizeUI)
        generalSizer.AddControl( ctlName = 'SprintPower', ctlType = 'choice',
            contents = GameData.SprintPowers,)
        generalSizer.AddControl( ctlName = 'AutoMouseLook', ctlType = 'checkbox',
            tooltip = 'Automatically Mouselook when moving',)
        generalSizer.AddControl( ctlName = 'AutoRun', ctlType = 'keybutton',)
        generalSizer.AddControl( ctlName = 'Follow', ctlType = 'keybutton',)
        generalSizer.AddControl( ctlName = 'NonSoDEnable', ctlType = 'checkbox',)
        self.Ctrls['NonSoDEnable'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        generalSizer.AddControl( ctlName = 'NonSoDMode', ctlType = 'keybutton',)
        generalSizer.AddControl( ctlName = 'SprintSoD', ctlType = 'checkbox',)
        self.Ctrls['SprintSoD'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        generalSizer.AddControl( ctlName = 'SprintMode', ctlType = 'keybutton',)

        self.leftColumn.Add(generalSizer, 0, wx.EXPAND)

        ### DETAIL SETTINGS
        detailSizer = ControlGroup(self, self, 'Detail Settings')
        detailSizer.AddControl( ctlName = 'ChangeCamera', ctlType = 'checkbox',)
        self.Ctrls['ChangeCamera'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        detailSizer.AddControl( ctlName = 'CamdistBase', ctlType = 'spinbox', contents = (1, 100),)
        detailSizer.AddControl( ctlName = 'CamdistMove', ctlType = 'spinbox', contents = (1, 100),)
        detailSizer.AddControl( ctlName = 'ChangeDetail', ctlType = 'checkbox',)
        self.Ctrls['ChangeDetail'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        detailSizer.AddControl( ctlName = 'DetailBase', ctlType = 'spinbox', contents = (1, 100),)
        detailSizer.AddControl( ctlName = 'DetailMove', ctlType = 'spinbox', contents = (1, 100),)
        detailSizer.AddControl( ctlName = 'TPHideWindows', ctlType = 'checkbox',)
        detailSizer.AddControl( ctlName = 'Feedback', ctlType = 'checkbox',)
        self.leftColumn.Add(detailSizer, 0, wx.EXPAND)


        ##### TEMP TRAVEL POWERS
        tempSizer = ControlGroup(self, self, 'Temp Travel Powers')
        # if (temp travel powers exist)?  Should this be "custom"?
        tempSizer.AddControl( ctlName = 'TempEnable', ctlType = 'checkbox',)
        self.Ctrls['TempEnable'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        tempSizer.AddControl( ctlName = 'TempMode', ctlType = 'keybutton',)
        tempSizer.AddControl( ctlName = 'TempTray', ctlType = 'spinbox', contents = [1, 8],)
        tempSizer.AddControl( ctlName = 'TempTraySwitch', ctlType = 'keybutton',)
        self.leftColumn.Add(tempSizer, 0, wx.EXPAND)

        ##### SUPER SPEED
        superSpeedSizer = ControlGroup(self, self, 'Super Speed')
        superSpeedSizer.AddControl( ctlName = 'HasSS', ctlType = "checkbox",)
        self.Ctrls['HasSS'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        superSpeedSizer.AddControl( ctlName = 'RunMode', ctlType = 'keybutton',)
        superSpeedSizer.AddControl( ctlName = 'SSMobileOnly', ctlType = 'checkbox',)
        superSpeedSizer.AddControl( ctlName = 'SSSJModeEnable', ctlType = 'checkbox',)
        self.rightColumn.Add(superSpeedSizer, 0, wx.EXPAND)

        ##### SUPER JUMP
        superJumpSizer = ControlGroup(self, self, 'Super Jump')
        superJumpSizer.AddControl( ctlName = 'HasSJ', ctlType = 'checkbox',)
        self.Ctrls['HasSJ'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        superJumpSizer.AddControl( ctlName = 'HasCJ', ctlType = 'checkbox',)
        self.Ctrls['HasCJ'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        superJumpSizer.AddControl( ctlName = 'SimpleSJCJ', ctlType = 'checkbox',)
        superJumpSizer.AddControl( ctlName = 'JumpMode', ctlType = 'keybutton',)
        self.rightColumn.Add(superJumpSizer, 0, wx.EXPAND)

        ##### FLY
        self.flySizer = ControlGroup(self, self, 'Flight')
        self.flySizer.AddControl( ctlName = 'HasHover', ctlType = 'checkbox',)
        self.Ctrls['HasHover'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        self.flySizer.AddControl( ctlName = 'HasFly', ctlType = 'checkbox',)
        self.Ctrls['HasFly'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        self.flySizer.AddControl( ctlName = 'HasCF', ctlType = 'checkbox',)
        self.Ctrls['HasCF'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        self.flySizer.AddControl( ctlName = 'FlyMode', ctlType = 'keybutton',)
        self.flySizer.AddControl( ctlName = 'HasQF', ctlType = 'checkbox',)
        self.Ctrls['HasQF'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        self.flySizer.AddControl( ctlName = 'QFlyMode', ctlType = 'keybutton',)
        #self.flySizer.AddControl( ctlName = 'GFlyMode', ctlType = 'keybutton',)
        self.rightColumn.Add(self.flySizer, 0, wx.EXPAND)

        ##### TELEPORT
        teleportSizer = ControlGroup(self, self, 'Teleport')

        # if (at == peacebringer) "Dwarf Step"
        # if (at == warshade) "Shadow Step / Dwarf Step"
        teleportSizer.AddControl( ctlName = 'HasTP', ctlType = 'checkbox',)
        self.Ctrls['HasTP'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        teleportSizer.AddControl( ctlName = "TPBindKey", ctlType = 'keybutton',)
        teleportSizer.AddControl( ctlName = "TPComboKey", ctlType = 'keybutton',)
        teleportSizer.AddControl( ctlName = "TPResetKey", ctlType = 'keybutton',)
        teleportSizer.AddControl( ctlName = 'TPTPHover', ctlType = 'checkbox',)
        self.rightColumn.Add(teleportSizer, 0, wx.EXPAND)

        # TODO - do we want these team versions in there?
        teamTeleportSizer = ControlGroup(self, self, 'Team Teleport')
        teamTeleportSizer.AddControl( ctlName = "HasTTP", ctlType = 'checkbox',)
        self.Ctrls['HasTTP'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        teamTeleportSizer.AddControl( ctlName = "TTPBindKey", ctlType = 'keybutton',)
        teamTeleportSizer.AddControl( ctlName = "TTPComboKey", ctlType = 'keybutton',)
        teamTeleportSizer.AddControl( ctlName = "TTPResetKey", ctlType = 'keybutton',)
        # if (player has group fly):
        # teleportSizer.AddControl( ctlName = 'TTPAutoGFly', ctlType = 'checkbox',)
        # end team-tp
        self.rightColumn.Add(teamTeleportSizer, 0, wx.EXPAND)

        ##### KHELDIAN TRAVEL POWERS
        self.kheldianSizer = ControlGroup(self, self, 'Nova / Dwarf Travel Powers')

        self.kheldianSizer.AddControl( ctlName = 'UseNova', ctlType = 'checkbox',)
        self.Ctrls['UseNova'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        self.kheldianSizer.AddControl( ctlName = 'NovaMode', ctlType = 'keybutton',)
        self.kheldianSizer.AddControl( ctlName = 'NovaTray', ctlType = 'spinbox', contents = [1, 8],)
        self.kheldianSizer.AddControl( ctlName = 'UseDwarf', ctlType = 'checkbox',)
        self.Ctrls['UseDwarf'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        self.kheldianSizer.AddControl( ctlName = 'DwarfMode', ctlType = 'keybutton',)
        self.kheldianSizer.AddControl( ctlName = 'DwarfTray', ctlType = 'spinbox', contents = [1, 8],)
        # do we want a key to change directly to human form, instead of toggles?
        self.kheldianSizer.AddControl( ctlName = 'HumanMode', ctlType = 'keybutton',)
        self.kheldianSizer.AddControl( ctlName = 'HumanTray', ctlType = 'spinbox', contents = [1, 8],)
        self.rightColumn.Add(self.kheldianSizer, 0, wx.EXPAND)

        topSizer.Add(self.leftColumn)
        topSizer.Add(self.rightColumn)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizerAndFit(paddingSizer)

        self.SynchronizeUI()

    def SynchronizeUI(self, _ = None):
        self.Freeze()

        try:
            c = self.Ctrls
            # start with turning everything on or off to match the global checkbox
            for cname,control in c.items():
                if cname != 'EnableSoD':  # don't disable yourself kthx
                    control.Enable(self.GetState('EnableSoD'))
                    if not isinstance(control.CtlLabel, str):
                        control.CtlLabel.Enable(self.GetState('EnableSoD'))

            # and if everything's off, we're done
            if not self.GetState('EnableSoD'): return

            c['NonSoDMode']         .Enable(self.GetState('NonSoDEnable'))
            c['NonSoDMode'].CtlLabel.Enable(self.GetState('NonSoDEnable'))

            c['SprintMode']         .Enable(self.GetState('SprintSoD') and self.GetState('DefaultMode') != "Sprint")
            c['SprintMode'].CtlLabel.Enable(self.GetState('SprintSoD') and self.GetState('DefaultMode') != "Sprint")

            c['CamdistBase']         .Enable(self.GetState('ChangeCamera'))
            c['CamdistBase'].CtlLabel.Enable(self.GetState('ChangeCamera'))
            c['CamdistMove']         .Enable(self.GetState('ChangeCamera'))
            c['CamdistMove'].CtlLabel.Enable(self.GetState('ChangeCamera'))

            c['DetailBase']         .Enable(self.GetState('ChangeDetail'))
            c['DetailBase'].CtlLabel.Enable(self.GetState('ChangeDetail'))
            c['DetailMove']         .Enable(self.GetState('ChangeDetail'))
            c['DetailMove'].CtlLabel.Enable(self.GetState('ChangeDetail'))

            c['TempMode']         .Enable(self.GetState('TempEnable'))
            c['TempMode'].CtlLabel.Enable(self.GetState('TempEnable'))
            c['TempTray']         .Enable(self.GetState('TempEnable'))
            c['TempTray'].CtlLabel.Enable(self.GetState('TempEnable'))
            c['TempTraySwitch']         .Enable(self.GetState('TempEnable'))
            c['TempTraySwitch'].CtlLabel.Enable(self.GetState('TempEnable'))

            c['RunMode']         .Enable(self.GetState('HasSS') and self.GetState('DefaultMode') != "Super Speed")
            c['RunMode'].CtlLabel.Enable(self.GetState('HasSS') and self.GetState('DefaultMode') != "Super Speed")
            c['SSMobileOnly']         .Enable(self.GetState('HasSS'))
            c['SSMobileOnly'].CtlLabel.Enable(self.GetState('HasSS'))
            c['SSSJModeEnable']         .Enable(self.GetState('HasSS') and self.GetState('HasSJ'))
            c['SSSJModeEnable'].CtlLabel.Enable(self.GetState('HasSS') and self.GetState('HasSJ'))

            # TODO - in citybinder, this is "if SJ or CJ" but shouldn't it be "SJ -and- CJ"?
            c['SimpleSJCJ']         .Enable(self.GetState('HasSJ') or self.GetState('HasCJ'))
            c['SimpleSJCJ'].CtlLabel.Enable(self.GetState('HasSJ') or self.GetState('HasCJ'))
            c['JumpMode']           .Enable((self.GetState('HasSJ') or self.GetState('HasCJ'))
                                          and self.GetState('DefaultMode') != "Jump")
            c['JumpMode'].CtlLabel.Enable((self.GetState('HasSJ') or self.GetState('HasCJ'))
                                          and self.GetState('DefaultMode') != "Jump")

            c['FlyMode']         .Enable((self.GetState('HasHover') or self.GetState('HasFly') or self.GetState('HasCF'))
                                          and self.GetState('DefaultMode') != "Fly")
            c['FlyMode'].CtlLabel.Enable((self.GetState('HasHover') or self.GetState('HasFly') or self.GetState('HasCF'))
                                          and self.GetState('DefaultMode') != "Fly")
            c['QFlyMode']         .Enable(self.GetState('HasQF'))
            c['QFlyMode'].CtlLabel.Enable(self.GetState('HasQF'))

            c['TPBindKey']         .Enable(self.GetState('HasTP'))
            c['TPBindKey'].CtlLabel.Enable(self.GetState('HasTP'))
            c['TPComboKey']         .Enable(self.GetState('HasTP'))
            c['TPComboKey'].CtlLabel.Enable(self.GetState('HasTP'))
            c['TPResetKey']         .Enable(self.GetState('HasTP'))
            c['TPResetKey'].CtlLabel.Enable(self.GetState('HasTP'))
            c['TPTPHover']         .Enable(self.GetState('HasTP') and self.GetState('HasHover'))
            c['TPTPHover'].CtlLabel.Enable(self.GetState('HasTP') and self.GetState('HasHover'))

            c['TTPBindKey']         .Enable(self.GetState('HasTTP'))
            c['TTPBindKey'].CtlLabel.Enable(self.GetState('HasTTP'))
            c['TTPComboKey']         .Enable(self.GetState('HasTTP'))
            c['TTPComboKey'].CtlLabel.Enable(self.GetState('HasTTP'))
            c['TTPResetKey']         .Enable(self.GetState('HasTTP'))
            c['TTPResetKey'].CtlLabel.Enable(self.GetState('HasTTP'))

            c['NovaMode']         .Enable(self.GetState('UseNova'))
            c['NovaMode'].CtlLabel.Enable(self.GetState('UseNova'))
            c['NovaTray']         .Enable(self.GetState('UseNova'))
            c['NovaTray'].CtlLabel.Enable(self.GetState('UseNova'))
            c['DwarfMode']         .Enable(self.GetState('UseDwarf'))
            c['DwarfMode'].CtlLabel.Enable(self.GetState('UseDwarf'))
            c['DwarfTray']         .Enable(self.GetState('UseDwarf'))
            c['DwarfTray'].CtlLabel.Enable(self.GetState('UseDwarf'))

            # show/hide kheldian-influenced controls depending on selected archetype;
            archetype = self.Profile.Archetype()
            kheldianOnlyControls = ['HasCF', 'HasQF', 'QFlyMode']
            nonkheldianOnlyControls = ['HasFly','HasHover','TPTPHover']

            kheldianGridSizer = self.kheldianSizer.GetChildren()[0].GetSizer()
            flyGridSizer      = self.flySizer.GetChildren()[0].GetSizer()
            if archetype == "Peacebringer" or archetype == "Warshade":
                # show kheldian sizer, enable controls
                for ctrl in kheldianGridSizer.GetChildren():
                    ctrl.GetWindow().Enable(True)
                self.rightColumn.Show(self.kheldianSizer)
                # if Warshade: hide flight sizer, disable controls
                for ctrl in flyGridSizer.GetChildren():
                    ctrl.GetWindow().Enable(archetype != "Warshade")
                self.rightColumn.Show(self.flySizer, archetype != "Warshade")

                # en/disable controls in other sizers
                for c in kheldianOnlyControls:
                    ctrl = self.Ctrls[c]
                    ctrl.GetContainingSizer().Show(ctrl)
                    ctrl.GetContainingSizer().Show(ctrl.CtlLabel)
                for c in nonkheldianOnlyControls:
                    ctrl = self.Ctrls[c]
                    ctrl.GetContainingSizer().Hide(ctrl)
                    ctrl.GetContainingSizer().Hide(ctrl.CtlLabel)
            else:
                # hide kheldiansizer, disable controls
                for ctrl in kheldianGridSizer.GetChildren():
                    ctrl.GetWindow().Enable(False)
                    self.rightColumn.Hide(self.kheldianSizer)

                # en/disable controls in other sizers
                for c in kheldianOnlyControls:
                    ctrl = self.Ctrls[c]
                    ctrl.GetContainingSizer().Hide(ctrl)
                    ctrl.GetContainingSizer().Hide(ctrl.CtlLabel)
                for c in nonkheldianOnlyControls:
                    ctrl = self.Ctrls[c]
                    ctrl.GetContainingSizer().Show(ctrl)
                    ctrl.GetContainingSizer().Show(ctrl.CtlLabel)

        except Exception as e:
            print(f"Something blowed up in SoD SynchronizeUI:  {e}")

        finally:
            self.Thaw()
            self.Layout()


    def makeSoDFile(self, p):

        profile = self.Profile

        t = p['t']

        bl   = p.get('bl'   , t.bl)
        bla  = p.get('bla'  , t.bla)
        blf  = p.get('blf'  , t.blf)
        blbo = p.get('blbo' , t.blbo)
        # blsd = p.get('blsd' , t.blsd) # used in commented-out code

        path      = p.get('path'     , t.path)
        gamepath  = p.get('gamepath' , t.gamepath)
        patha     = p.get('patha'    , t.patha)
        gamepatha = p.get('gamepatha'    , t.gamepatha)
        pathf     = p.get('pathf'    , t.pathf)
        gamepathf = p.get('gamepathf'    , t.gamepathf)
        pathbo    = p.get('pathbo'   , t.pathbo)
        # pathsd  = p.get('pathsd'   , t.pathsd) # used in commented-out code

        mobile     = p.get('mobile'     , None)
        stationary = p.get('stationary' , None)
        modestr    = p.get('modestr'    , "")
        flight     = p.get('flight'     , "")
        fix        = p.get('fix'        , "")
        turnoff    = p.get('turnoff'    , "")
        sssj       = p.get('sssj'       , "")

        # TODO TODO TODO -- here and seven other places, this list should be instead a set.
        # Keeping it as a list for now to match citybinder
        turnoff = turnoff or [ mobile, stationary ]

        if ((self.GetState('DefaultMode') == modestr) and (t.totalkeys == 0)):

            curfile = profile.ResetFile()

            self.sodUpKey     (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
            self.sodDownKey   (t,bl,curfile,mobile,stationary,flight,'','','')
            self.sodForwardKey(t,bl,curfile,mobile,stationary,flight,'','','',sssj)
            self.sodBackKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
            self.sodLeftKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
            self.sodRightKey  (t,bl,curfile,mobile,stationary,flight,'','','',sssj)

            if (modestr != "NonSoD")      : self.makeNonSoDModeKey(profile,t,"r", curfile,[ mobile,stationary ])
            if (modestr != "Sprint")      : self.makeSprintModeKey(profile,t,"r", curfile,turnoff,fix)
            if (modestr != "Fly")         : self.makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)
            # if (modestr != "GFly")        : self.makeGFlyModeKey  (profile,t,"gf",curfile,turnoff,fix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"s", curfile,turnoff,fix)
            if (modestr != "Jump")        : self.makeJumpModeKey  (profile,t,"j", curfile,turnoff,path, gamepath)
            if (modestr != "Temp")        : self.makeTempModeKey  (profile,t,"r", curfile,turnoff)
            if (modestr != "QFly")        : self.makeQFlyModeKey  (profile,t,"r", curfile,turnoff,modestr)

            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)

            self.sodFollowKey(t,blf,curfile,mobile)

        if (flight and (flight == "Fly") and pathbo):
            #  blast off
            curfile = profile.GetBindFile(pathbo + t.KeyState() + ".txt")
            self.sodResetKey(curfile,profile,gamepath,self.actPower_toggle(None,True,stationary,mobile),'')
            self.sodUpKey     (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodDownKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo")
            self.sodForwardKey(t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodBackKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodLeftKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodRightKey  (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)

            if (modestr == "Sprint") : self.makeSprintModeKey(profile,t,"r",curfile,turnoff,fix)

            t.ini = '-down$$'

            if (self.GetState('DefaultMode') == "Fly"):
                if (self.GetState('NonSoDEnable')):
                    t.FlyMode = t.NonSoDMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                if (self.GetState('SprintSoD')):
                    t.FlyMode = t.SprintMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                if (self.GetState('HasSS')):
                    t.FlyMode = t.RunMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                if (t.canjmp):
                    t.FlyMode = t.JumpMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
                if (self.GetState('TempEnable')):
                    t.FlyMode = t.TempMode
                    self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)
            else:
                self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)

            t.ini = ''
            # if (modestr != "GFly")        : self.makeGFlyModeKey (profile,t,"gbo",curfile,turnoff,fix)
            # if (modestr != "Super Speed") : self.makeSpeedModeKey(profile,t,"s",  curfile,turnoff,fix)
            # if (modestr != "Jump")        : self.makeJumpModeKey (profile,t,"j",  curfile,turnoff,path,gamepath)

            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)

            self.sodFollowKey(t,blf,curfile,mobile)

            # TODO this section is commented out in citybinder, why?
            # curfile = profile.GetBindFile(pathsd)
#
#            self.sodResetKey(curfile,profile,gamepath,self.actPower_toggle(None,True,stationary,mobile),'')
#
#            self.sodUpKey     (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
#            self.sodDownKey   (t,blsd,curfile,mobile,stationary,flight,'','',"sd")
#            self.sodForwardKey(t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
#            self.sodBackKey   (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
#            self.sodLeftKey   (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
#            self.sodRightKey  (t,blsd,curfile,mobile,stationary,flight,'','',"sd",sssj)
#
#            t.ini = '-down$$'
#            if (modestr != "Sprint") : self.makeSprintModeKey(profile,t,"r",  curfile,turnoff,fix)
#            if (modestr != "Fly")  : self.makeFlyModeKey( profile,t,"a",  curfile,turnoff,fix)
#            if (modestr != "GFly") : self.makeGFlyModeKey(profile,t,"gbo",curfile,turnoff,fix)
#            t.ini = ''
#            if (modestr != "Jump") : self.makeJumpModeKey(profile,t,"j",  curfile,turnoff,path,gamepath)
#
#            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)
#            self.sodFollowKey(t,blf,curfile,mobile)

        curfile = profile.GetBindFile(path + t.KeyState() + ".txt")

        self.sodResetKey(curfile,profile,gamepath,self.actPower_toggle(None,True,stationary,mobile),'')

        self.sodUpKey     (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodDownKey   (t,bl,curfile,mobile,stationary,flight,'','','')
        self.sodForwardKey(t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodBackKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodLeftKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodRightKey  (t,bl,curfile,mobile,stationary,flight,'','','',sssj)

        if ((flight == "Fly") and pathbo):
            #  Base to set down
            if (modestr != "NonSoD") : self.makeNonSoDModeKey(profile,t,"r",curfile,[ mobile,stationary ],self.sodSetDownFix)
            if (modestr != "Sprint") : self.makeSprintModeKey(profile,t,"r",curfile,turnoff,self.sodSetDownFix)

            #if (t.SprintMode):
                #curfile.SetBind(t.SprintMode, "+down$$down 1" + self.actPower_name(None,True,mobile) + t.detailhi + t.runcamdist + t.blsd)

            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"s", curfile,turnoff,self.sodSetDownFix)
            if (modestr != "Fly")         : self.makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)
            if (modestr != "Jump")        : self.makeJumpModeKey  (profile,t,"j", curfile,turnoff,path,gamepath)
            if (modestr != "Temp")        : self.makeTempModeKey  (profile,t,"r", curfile,turnoff)
            if (modestr != "QFly")        : self.makeQFlyModeKey  (profile,t,"r", curfile,turnoff,modestr)
        else:
            if (modestr != "NonSoD") : self.makeNonSoDModeKey(profile,t,"r", curfile,[ mobile,stationary ])
            if (modestr != "Sprint") : self.makeSprintModeKey(profile,t,"r", curfile,turnoff,fix)
            if (flight == "Jump"):
                if (modestr != "Fly"): self.makeFlyModeKey   (profile,t,"a", curfile,turnoff,fix,'',True)
            else:
                if (modestr != "Fly"): self.makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)

            if (modestr != "Super Speed")    : self.makeSpeedModeKey (profile,t,"s", curfile,turnoff,fix)
            if (modestr != "Jump")   : self.makeJumpModeKey  (profile,t,"j", curfile,turnoff,path,gamepath)
            if (modestr != "Temp")   : self.makeTempModeKey  (profile,t,"r", curfile,turnoff)
            if (modestr != "QFly")   : self.makeQFlyModeKey  (profile,t,"r", curfile,turnoff,modestr)

        self.sodAutoRunKey(t,bla,curfile,mobile,sssj)
        self.sodFollowKey(t,blf,curfile,mobile)

        # AutoRun Binds
        curfile = profile.GetBindFile(patha + t.KeyState() + ".txt")

        self.sodResetKey(curfile,profile,gamepath,self.actPower_toggle(None,True,stationary,mobile),'')

        self.sodUpKey     (t,bla,curfile,mobile,stationary,flight,1, '','',sssj)
        self.sodDownKey   (t,bla,curfile,mobile,stationary,flight,1, '','')
        self.sodForwardKey(t,bla,curfile,mobile,stationary,flight,bl,'','',sssj)
        self.sodBackKey   (t,bla,curfile,mobile,stationary,flight,bl,'','',sssj)
        self.sodLeftKey   (t,bla,curfile,mobile,stationary,flight,1, '','',sssj)
        self.sodRightKey  (t,bla,curfile,mobile,stationary,flight,1, '','',sssj)

        if ((flight == "Fly") and pathbo):
            if (modestr != "NonSoD")      : self.makeNonSoDModeKey(profile,t,"ar",curfile,[ mobile,stationary ],self.sodSetDownFix)
            if (modestr != "Sprint")      : self.makeSprintModeKey(profile,t,"gr",curfile,turnoff,self.sodSetDownFix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"as",curfile,turnoff,self.sodSetDownFix)
        else:
            if (modestr != "NonSoD")      : self.makeNonSoDModeKey(profile,t,"ar",curfile,[ mobile,stationary ])
            if (modestr != "Sprint")      : self.makeSprintModeKey(profile,t,"gr",curfile,turnoff,fix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"as",curfile,turnoff,fix)

        if (modestr != "Fly")       : self.makeFlyModeKey (profile,t,"af",curfile,turnoff,fix)
        if (modestr != "Jump")      : self.makeJumpModeKey(profile,t,"aj",curfile,turnoff,patha,gamepatha)
        if (modestr != "Temp")      : self.makeTempModeKey(profile,t,"ar",curfile,turnoff)
        if (modestr != "QFly")      : self.makeQFlyModeKey(profile,t,"ar",curfile,turnoff,modestr)

        self.sodAutoRunOffKey(t,bl,curfile,mobile,stationary,flight)

        curfile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind('nop'))

        # FollowRun Binds
        curfile = profile.GetBindFile(pathf + t.KeyState() + ".txt")

        self.sodResetKey(curfile,profile,gamepath,self.actPower_toggle(None,True,stationary,mobile),'')

        self.sodUpKey     (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodDownKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'')
        self.sodForwardKey(t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodBackKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodLeftKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodRightKey  (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)

        if ((flight == "Fly") and pathbo):
            if (modestr != "NonSoD"): self.makeNonSoDModeKey(profile,t,"fr",curfile,[ mobile,stationary ],self.sodSetDownFix)
            if (modestr != "Sprint"): self.makeSprintModeKey(profile,t,"fr",curfile,turnoff,self.sodSetDownFix)
            if (modestr != "Super Speed")   : self.makeSpeedModeKey (profile,t,"fs",curfile,turnoff,self.sodSetDownFix)
        else:
            if (modestr != "NonSoD"): self.makeNonSoDModeKey(profile,t,"fr",curfile,[ mobile,stationary ])
            if (modestr != "Sprint"): self.makeSprintModeKey(profile,t,"fr",curfile,turnoff,fix)
            if (modestr != "Super Speed")   : self.makeSpeedModeKey (profile,t,"fs",curfile,turnoff,fix)

        if (modestr != "Fly")       : self.makeFlyModeKey (profile,t,"ff",curfile,turnoff,fix)
        if (modestr != "Jump")      : self.makeJumpModeKey(profile,t,"fj",curfile,turnoff, pathf, gamepathf)
        if (modestr != "Temp")      : self.makeTempModeKey(profile,t,"fr",curfile,turnoff)
        if (modestr != "QFly")      : self.makeQFlyModeKey(profile,t,"fr",curfile,turnoff,modestr)

        curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind('nop'))

        self.sodFollowOffKey(t,bl,curfile,mobile,stationary,flight)

    def makeNonSoDModeKey(self, p, t, bl, cur, toff, fix = None, fb = ''):
        key = t.NonSoDMode
        if not key: return
        if not self.Ctrls['NonSoDMode'].IsEnabled(): return

        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Non-SoD Mode'
        else:                                      feedback = ''

        if (bl == "r"):
            bindload = t.BLF('n')
            if (fix):
                fix(p,t,key, self.makeNonSoDModeKey,"n",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(None,True,None,toff) + t.dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload = t.BLF('an')
            if (fix):
                fix(p,t,key, self.makeNonSoDModeKey,"n",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(None,True,None,toff) + t.detailhi + t.runcamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, self.makeNonSoDModeKey,"n",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(None,True,None,toff) + t.detailhi + t.runcamdist + '$$up 0' + feedback + t.BLF('fn'))
        t.ini = ''

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

    def makeQFlyModeKey(self, p, t, bl, cur, toff, modestr):
        key = t.QFlyMode
        if not key: return
        if not self.Ctrls['QFlyMode'].IsEnabled(): return

        if (modestr == "NonSoD"):
            cur.SetBind(key, "powexecname Quantum Flight")
            return

        if self.GetState('Feedback'): feedback = '$$t $name, QFlight Mode'
        else:                         feedback = ''

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

    def makeSprintModeKey(self, p, t, bl, cur, toff, fix, fb = ''):
        key = t.SprintMode
        if not key: return

        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Sprint-SoD Mode'
        else:                                      feedback = ''

        if (bl == "r"):
            bindload  = t.BLF('R')

            if t.horizkeys: sprint = t.sprint
            else:           sprint = ''
            ton = self.actPower_toggle(1, True, sprint, toff)

            if (fix):
                fix(p,t,key, self.makeSprintModeKey,"r",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, t.ini + ton + t.dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t.BLF('gr')

            if (fix):
                fix(p,t,key, self.makeSprintModeKey,"r",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(1,True,t.sprint,toff) + t.detailhi +  t.runcamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, self.makeSprintModeKey,"r",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, t.ini + self.actPower_toggle(1,True,t.sprint,toff) + t.detailhi + t.runcamdist + '$$up 0' + feedback + t.BLF('fr'))

        t.ini = ''

    def makeSpeedModeKey(self, p, t, bl, cur, toff, fix, fb = ''):
        key = t.RunMode
        bindload = feedback = ''

        if (not fb) and p.SoD.GetState('Feedback'): feedback = '$$t $name, Superspeed Mode'

        if (self.GetState('HasSS')):
            if (bl == 's'):
                bindload = f"{t.bls}{t.KeyState()}.txt"
                if (fix):
                    fix(p,t,key,self.makeSpeedModeKey,"s",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,True,t.speed,toff) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload))

            elif (bl == "as"):
                bindload = f"{t.blas}{t.KeyState()}.txt"
                if (fix):
                    fix(p,t,key,self.makeSpeedModeKey,"s",bl,cur,toff,"a",feedback)
                elif (not feedback):
                    cur.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,True,t.speed,toff) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload))
                else:
                    # TODO - what is the reasoning here for two files?  wtf _s.txt
                    bindload  = f"{t.pathas}{t.KeyState()}.txt"
                    bindload2 = f"{t.pathas}{t.KeyState()}_s.txt"
                    tgl = p.GetBindFile(bindload2)
                    cur.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,True,t.speed,toff) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload2))
                    tgl.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,True,t.speed,toff) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload))

            else:
                if (fix):
                    fix(p,t,key,self.makeSpeedModeKey,"s",bl,cur,toff,"f",feedback)
                else:
                    bindload = f"{t.blfs}{t.KeyState()}.txt"
                    cur.SetBind(FileKeyBind(key = key, contents = t.ini + self.actPower_toggle(1,True,t.speed,toff) + '$$up 0' +  t.detaillo + t.flycamdist + feedback + bindload))

        t.ini = ''

    def makeJumpModeKey(self, p, t, bl, cur, toff, fpath, fbl):
        key = t.JumpMode
        if (t.canjmp and not self.GetState('SimpleSJCJ')):

            if self.GetState('Feedback'): feedback = '$$t $name, Superjump Mode'
            else:                         feedback = ''

            tglbl = fbl   + t.KeyState() + "j.txt"
            tglfn = fpath + t.KeyState() + "j.txt"
            tgl = p.GetBindFile(tglfn)

            if (bl == "j"):
                if (t.horizkeys + t.space > 0):
                    a = self.actPower(None,1,t.jump,toff) + '$$up 1'
                else:
                    a = self.actPower(None,1,t.cjmp,toff)

                tgl.SetBind(key, '-down' + a + t.detaillo + t.flycamdist + t.blj + t.KeyState() + ".txt")
                cur.SetBind(key, '+down' + feedback + '$$bindloadfile ' + tglbl)
            elif (bl == "aj"):
                tgl.SetBind(key, '-down' + self.actPower(None,1,t.jump,toff) + '$$up 1' + t.detaillo + t.flycamdist + t.dirs('DLR') + t.blaj + t.KeyState() + ".txt")
                cur.SetBind(key, '+down' + feedback + '$$bindloadfile ' + tglbl)
            else:
                tgl.SetBind(key, '-down' + self.actPower(None,1,t.jump,toff) + '$$up 1' + t.detaillo + t.flycamdist + t.blfj + t.KeyState() + ".txt")
                cur.SetBind(key, '+down' + feedback + '$$bindloadfile ' + tglbl)

        t.ini = ''

    def makeFlyModeKey(self, p, t, bl, cur, toff, fix, fb = '', fb_on_a = False):
        key = t.FlyMode
        if not key: return

        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Flight Mode'
        else:                                      feedback = ''

        if (t.canhov or t.canfly):
            if (bl == "bo"):
                bindload = t.blbo + t.KeyState() + ".txt"
                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(key, '+down$$' + self.actPower_toggle(1,True,t.flyx,toff) + '$$up 1$$down 0' + t.dirs('FBLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "a"):
                if (not fb_on_a): feedback = ''
                bindload = t.bla + t.KeyState() + ".txt"

                if t.totalkeys: ton = t.flyx
                else:           ton = t.hover

                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(t.FlyMode,  t.ini + self.actPower_toggle(1,True,ton,toff) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "af"):
                bindload = t.blaf + t.KeyState() + ".txt"
                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,"a",feedback)
                else:
                    cur.SetBind(key,  t.ini + self.actPower_toggle(1,True,t.flyx,toff) + t.detaillo + t.flycamdist + t.dirs('DLR') + feedback + bindload)

            else:
                bindload = t.blff + t.KeyState() + ".txt"
                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,"f",feedback)
                else:
                    cur.SetBind(key,  t.ini + self.actPower_toggle(1,True,t.flyx,toff) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + t.blff + t.KeyState() + ".txt")

        t.ini = ''

    def makeGFlyModeKey(self, p, t, bl, cur, toff, fix):
        key = t.GFlyMode

        if (t.cangfly > 0):
            if (bl == "gbo"):
                bindload = t.BLF('gbo')
                if (fix):
                    fix(p,t,key,self.makeGFlyModeKey,"gf",bl,cur,toff,'','')
                else:
                    cur.SetBind(key, t.ini + '$$up 1$$down 0' + self.actPower_toggle(None,True,t.gfly,toff) + t.dirs('FBLR') + t.detaillo + t.flycamdist .bindload)

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
                        cur.SetBind(key, t.ini + self.actPower_toggle(1,True,t.gfly,toff) + t.detaillo + t.flycamdist + t.BLF('gff'))
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

        if (self.GetState('DefaultMode') == "NonSoD"):
            if (not self.GetState('NonSoDEnable')):
                wx.MessageBox("Enabling NonSoD mode, since it is set as your default mode.", "Mode Changed", wx.OK|wx.ICON_WARNING)
            self.SetState('NonSoDEnable', 1)

        elif (self.GetState('DefaultMode') == "Sprint" and not self.GetState('SprintSoD')):
            wx.MessageBox("Enabling NonSoD mode and making it the default, since Sprint SoD, your previous Default mode, is not enabled.", "Mode Changed", wx.OK|wx.ICON_WARNING)
            self.SetState('NonSoDEnable', 1)
            self.SetState('DefaultMode', "NonSoD")

        elif (self.GetState('DefaultMode') == "Fly" and not (self.GetState('HasHover') or self.GetState('HasFly'))):
            wx.MessageBox("Enabling NonSoD mode and making it the default, since you had selected Fly mode but your character has neither Hover nor Fly.", "Mode Changed", wx.OK|wx.ICON_WARNING)
            self.SetState('NonSoDEnable', 1)
            self.SetState('DefaultMode', "NonSoD")

        elif (self.GetState('DefaultMode') == "Jump" and not (self.GetState('HasCJ') or self.GetState('HasSJ'))):
            wx.MessageBox("Enabling NonSoD mode and making it the default, since you had selected Jump mode but your character has neither Combat Jumping nor Super Jump.", "Mode Changed", wx.OK|wx.ICON_WARNING)
            self.SetState('NonSoDEnable', 1)
            self.SetState('DefaultMode', "NonSoD")

        elif (self.GetState('DefaultMode') == "Super Speed" and not self.GetState('HasSS')):
            wx.MessageBox("Enabling NonSoD mode and making it the default, since you had selected Super Speed mode but your character doesn't have Super Speed", "Mode Changed", wx.OK|wx.ICON_WARNING)
            self.SetState('NonSoDEnable', 1)
            self.SetState('DefaultMode', "NonSoD")


        t = tObject(profile)

        ## Combat Jumping / Super Jump
        if (self.GetState('HasCJ') and not self.GetState('HasSJ')):
            t.cancj = 1
            t.cjmp  = "Combat Jumping"
            t.jump  = "Combat Jumping"

        elif (not self.GetState('HasCJ') and self.GetState('HasSJ')):
            t.canjmp     = 1
            t.jump       = "Super Jump"
            t.jumpifnocj = "Super Jump"

        elif self.GetState('HasCJ') and self.GetState('HasSJ'):
            t.cancj  = 1
            t.canjmp = 1
            t.cjmp   = "Combat Jumping"
            t.jump   = "Super Jump"

        ## Flying / hover
        if (profile.Archetype() == "Peacebringer"):
            if (self.GetState('HasHover')):
                t.canhov = 1
                t.canfly = 1
                t.hover  = "Combat Flight"
                t.fly    = "Energy Flight"
                t.flyx   = "Energy Flight"
            else:
                t.canfly = 1
                t.hover  = "Energy Flight"
                t.flyx   = "Energy Flight"

        elif (not (profile.Archetype() == "Warshade")):
            if (self.GetState('HasHover') and not self.GetState('HasFly')):
                t.canhov = 1
                t.hover  = "Hover"
                t.flyx   = "Hover"
                if (self.GetState('TPTPHover')): t.tphover = '$$powexectoggleon Hover'
            elif (not self.GetState('HasHover') and self.GetState('HasFly')):
                t.canfly = 1
                t.hover  = "Fly"
                t.flyx   = "Fly"
            elif (self.GetState('HasHover') and self.GetState('HasFly')):
                t.canhov = 1
                t.canfly = 1
                t.hover  = "Hover"
                t.fly    = "Fly"
                t.flyx   = "Fly"
                if (self.GetState('TPTPHover')): t.tphover = '$$powexectoggleon Hover'

        if ((profile.Archetype() == "Peacebringer") and self.GetState('FlyQFly')):
            t.canqfly = 1

        # if (self.GetState('FlyGFly')):
        #     t.cangfly = 1
        #     t.gfly    = "Group Fly"
        #     if (self.GetState('TTPTPGFly')): t.ttpgfly = '$$powexectoggleon Group Fly'

        if (self.GetState('HasSS')):
            t.sprint = self.GetState('SprintPower')
            t.speed  = 'Super Speed'
        else:
            t.sprint = self.GetState('SprintPower')
            t.speed  = self.GetState('SprintPower')

        if (self.GetState('AutoMouseLook')):
            t.mlon  = '$$mouselook 1'
            t.mloff = '$$mouselook 0'

        if (self.GetState('ChangeCamera')):
            t.runcamdist = f"$$camdist {self.GetState('CamdistBase')}"
            t.flycamdist = f"$$camdist {self.GetState('CamdistMove')}"

        if (self.GetState('ChangeDetail')):
            t.detailhi = f"$$visscale {self.GetState('DetailBase')}$$shadowvol 0$$ss 0"
            t.detaillo = f"$$visscale {self.GetState('DetailMove')}$$shadowvol 0$$ss 0"

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
        t.gamepatha = str(PureWindowsPath(t.gamebasepath) / 'F' / 'F')
        t.bla       = f"$$bindloadfile {t.gamepatha}"

        t.pathj     = str(Path(t.basepath) / 'J' / 'J')
        t.gamepathj = str(PureWindowsPath(t.gamebasepath) / 'J' / 'J')
        t.blj       = f"$$bindloadfile {t.gamepathj}"

        t.paths     = str(Path(t.basepath) / 'S' / 'S')
        t.gamepaths = str(PureWindowsPath(t.gamebasepath) / 'S' / 'S')
        t.bls       = f"$$bindloadfile {t.gamepaths}"

        #t.pathga     = str(Path(t.basepath) / 'GF' / 'GF') # air subfolder and base filename
        #t.gamepathga = str(PureWindowsPath(t.gamebasepath) / 'GF' / 'GF')
        #t.blga       = f"$$bindloadfile {t.gamepathga}"

        t.pathn     = str(Path(t.basepath) / 'N' / 'N') # ground subfolder and base filename.
        t.gamepathn = str(PureWindowsPath(t.gamebasepath) / 'N' / 'N')
        t.bln       = f"$$bindloadfile {t.gamepathn}"

        t.patht     = str(Path(t.basepath) / 'T' / 'T') # ground subfolder and base filename.
        t.gamepatht = str(PureWindowsPath(t.gamebasepath) / 'T' / 'T')
        t.blt       = f"$$bindloadfile {t.gamepatht}"

        t.pathq     = str(Path(t.basepath) / 'Q' / 'Q') # ground subfolder and base filename.
        t.gamepathq = str(PureWindowsPath(t.gamebasepath) / 'Q' / 'Q')
        t.blq       = f"$$bindloadfile {t.gamepathq}"

        t.pathgr     = str(Path(t.basepath) / 'AR' / 'AR')  # ground autorun subfolder and base filename
        t.gamepathgr = str(PureWindowsPath(t.gamebasepath) / 'AR' / 'AR')
        t.blgr       = f"$$bindloadfile {t.gamepathgr}"

        t.pathaf     = str(Path(t.basepath) / 'AF' / 'AF')  # air autorun subfolder and base filename
        t.gamepathaf = str(PureWindowsPath(t.gamebasepath) / 'AF' / 'AF')
        t.blaf       = f"$$bindloadfile {t.gamepathaf}"

        t.pathaj     = str(Path(t.basepath) / 'AJ' / 'AJ')
        t.gamepathaj = str(PureWindowsPath(t.gamebasepath) / 'AJ' / 'AJ')
        t.blaj       = f"$$bindloadfile {t.gamepathaj}"

        t.pathas     = str(Path(t.basepath) / 'AS' / 'AS')
        t.gamepathas = str(PureWindowsPath(t.gamebasepath) / 'AS' / 'AS')
        t.blas       = f"$$bindloadfile {t.gamepathas}"

        #t.pathgaf     = str(Path(t.basepath) / 'GAF' / 'GAF')  # air autorun subfolder and base filename
        #t.gamepathgaf = str(PureWindowsPath(t.gamebasepath) / 'GAF' / 'GAF')
        #t.blgaf       = f"$$bindloadfile {t.gamepathgaf}"

        t.pathan     = str(Path(t.basepath) / 'AN' / 'AN') # ground subfolder and base filename.
        t.gamepathan = str(PureWindowsPath(t.gamebasepath) / 'AN' / 'AN')
        t.blan       = f"$$bindloadfile {t.gamepathan}"

        t.pathat     = str(Path(t.basepath) / 'AT' / 'AT') # ground subfolder and base filename.
        t.gamepathat = str(PureWindowsPath(t.gamebasepath) / 'AT' / 'AT')
        t.blat       = f"$$bindloadfile {t.gamepathat}"

        t.pathaq     = str(Path(t.basepath) / 'AQ' / 'AQ') # ground subfolder and base filename.
        t.gamepathaq = str(PureWindowsPath(t.gamebasepath) / 'AQ' / 'AQ')
        t.blaq       = f"$$bindloadfile {t.gamepathaq}"

        t.pathfr     = str(Path(t.basepath) / 'FR' / 'FR')  # Follow Run subfolder and base filename
        t.gamepathfr = str(PureWindowsPath(t.gamebasepath) / 'FR' / 'FR')
        t.blfr       = f"$$bindloadfile {t.gamepathfr}"

        t.pathff     = str(Path(t.basepath) / 'FF' / 'FF')  # Follow Fly subfolder and base filename
        t.gamepathff = str(PureWindowsPath(t.gamebasepath) / 'FF' / 'FF')
        t.blff       = f"$$bindloadfile {t.gamepathff}"

        t.pathfj     = str(Path(t.basepath) / 'FJ' / 'FJ')
        t.gamepathfj = str(PureWindowsPath(t.gamebasepath) / 'FJ' / 'FJ')
        t.blfj       = f"$$bindloadfile {t.gamepathfj}"

        t.pathfs     = str(Path(t.basepath) / 'FS' / 'FS')
        t.gamepathfs = str(PureWindowsPath(t.gamebasepath) / 'FS' / 'FS')
        t.blfs       = f"$$bindloadfile {t.gamepathfs}"

        #t.pathgff     = str(Path(t.basepath) / 'GFF' / 'GFF')  # Follow Fly subfolder and base filename
        #t.gamepathgff = str(PureWindowsPath(t.gamebasepath) / 'GFF' / 'GFF')
        #t.blgff       = f"$$bindloadfile {t.gamepathgff}"

        t.pathfn     = str(Path(t.basepath) / 'FN' / 'FN') # ground subfolder and base filename.
        t.gamepathfn = str(PureWindowsPath(t.gamebasepath) / 'FN' / 'FN')
        t.blfn       = f"$$bindloadfile {t.gamepathfn}"

        t.pathft     = str(Path(t.basepath) / 'FT' / 'FT') # ground subfolder and base filename.
        t.gamepathft = str(PureWindowsPath(t.gamebasepath) / 'FT' / 'FT')
        t.blft       = f"$$bindloadfile {t.gamepathat}"

        t.pathfq     = str(Path(t.basepath) / 'FQ' / 'FQ') # ground subfolder and base filename.
        t.gamepathfq = str(PureWindowsPath(t.gamebasepath) / 'FQ' / 'FQ')
        t.blfq       = f"$$bindloadfile {t.gamepathfq}"

        t.pathbo     = str(Path(t.basepath) / 'BO' / 'BO')  # Blastoff Fly subfolder and base filename
        t.gamepathbo = str(PureWindowsPath(t.gamebasepath) / 'BO' / 'BO')
        t.blbo       = f"$$bindloadfile {t.gamepathbo}"

        t.pathsd     = str(Path(t.basepath) / 'SD' / 'SD')  #  SetDown Fly Subfolder and base filename
        t.gamepathsd = str(PureWindowsPath(t.gamebasepath) / 'SD' / 'SD')
        t.blsd       = f"$$bindloadfile {t.gamepathsd}"

        #t.pathgbo     = str(Path(t.basepath) / 'GBO' / 'GBO')  # Blastoff Fly subfolder and base filename
        #t.gamepathgbo = str(PureWindowsPath(t.gamebasepath) / 'GBO' / 'GBO')
        #t.blgbo       = f"$$bindloadfile {t.gamepathgbo}"

        #t.pathgsd     = str(Path(t.basepath) / 'GSD' / 'GSD')  #  SetDown Fly Subfolder and base filename
        #t.gamepathgsd = str(PureWindowsPath(t.gamebasepath) / 'GSD' / 'GSD')
        #t.blgsd       = f"$$bindloadfile {t.gamepathgsd}"

        #  set up the keys to be used.
        if (self.GetState('DefaultMode') != "NonSoD")      : t.NonSoDMode = self.GetState('NonSoDMode')
        if (self.GetState('DefaultMode') != "Sprint")      : t.SprintMode = self.GetState('SprintMode')
        if (self.GetState('DefaultMode') != "Fly")         : t.FlyMode    = self.GetState('FlyMode')
        if (self.GetState('DefaultMode') != "Jump")        : t.JumpMode   = self.GetState('JumpMode')
        if (self.GetState('DefaultMode') != "Super Speed") : t.RunMode    = self.GetState('RunMode')
    #    if (self.GetState('DefaultMode') != "GFly")        : t.GFlyMode   = self.GetState('GFlyMode')
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
                                t.horizkeys = W+S+A+D;    # total # of horizontal move keys. So Sprint isn't turned on when jumping
                                t.vertkeys  = space+X
                                t.jkeys     = t.horizkeys+t.space
                                if (self.GetState('NonSoDEnable') or t.canqfly):
                                    setattr(t, self.GetState('DefaultMode') + "Mode", t.NonSoDMode)
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : t.bln,
                                        'bla'        : t.blan,
                                        'blf'        : t.blfn,
                                        'path'       : t.pathn,
                                        'gamepath'   : t.gamepathn,
                                        'patha'      : t.pathan,
                                        'pathf'      : t.pathfn,
                                        'mobile'     : None,
                                        'stationary' : None,
                                        'modestr'    : "NonSoD",
                                    })
                                    setattr(t, self.GetState('DefaultMode') + "Mode", None)

                                if (self.GetState('SprintSoD')):
                                    setattr(t, self.GetState('DefaultMode') + "Mode", t.SprintMode)
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : t.bl,
                                        'bla'        : t.blgr,
                                        'blf'        : t.blfr,
                                        'path'       : t.path,
                                        'gamepath'   : t.gamepath,
                                        'patha'      : t.pathgr,
                                        'gamepatha'  : t.gamepathgr,
                                        'pathf'      : t.pathfr,
                                        'gamepathf'  : t.gamepathfr,
                                        'mobile'     : t.sprint,
                                        'stationary' : None,
                                        'modestr'    : "Sprint",
                                    })
                                    setattr(t, self.GetState('DefaultMode') + "Mode", None)

                                if (self.GetState('HasSS')):
                                    setattr(t, self.GetState('DefaultMode') + "Mode", t.RunMode)
                                    if (self.GetState('SSSJModeEnable')): sssj = t.jump
                                    st = None if self.GetState('SSMobileOnly') else t.speed
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : t.bls,
                                        'bla'        : t.blas,
                                        'blf'        : t.blfs,
                                        'path'       : t.paths,
                                        'gamepath'   : t.gamepaths,
                                        'patha'      : t.pathas,
                                        'gamepatha'  : t.gamepathas,
                                        'pathf'      : t.pathfs,
                                        'gamepathf'  : t.gamepathfs,
                                        'mobile'     : t.speed,
                                        'stationary' : st,
                                        'modestr'    : "Super Speed",
                                        'sssj'       : sssj,
                                    })
                                    setattr(t, self.GetState('DefaultMode') + "Mode", None)

                                if (t.canjmp and not (self.GetState('SimpleSJCJ'))):
                                    setattr(t, self.GetState('DefaultMode') + "Mode", t.JumpMode)
                                    jturnoff = ''
                                    if (t.jump != t.cjmp): jturnoff = t.jumpifnocj
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : t.blj,
                                        'bla'        : t.blaj,
                                        'blf'        : t.blfj,
                                        'path'       : t.pathj,
                                        'gamepath'   : t.gamepathj,
                                        'patha'      : t.pathaj,
                                        'pathf'      : t.pathfj,
                                        'mobile'     : t.jump,
                                        'stationary' : t.cjmp,
                                        'modestr'    : "Jump",
                                        'flight'     : "Jump",
                                        'fix'        : self.sodJumpFix,
                                        'turnoff'    : jturnoff,
                                    })
                                    setattr(t, self.GetState('DefaultMode') + "Mode", None)

                                if (t.canhov or t.canfly):
                                    setattr(t, self.GetState('DefaultMode') + "Mode", t.FlyMode)
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : t.bla,
                                        'bla'        : t.blaf,
                                        'blf'        : t.blff,
                                        'path'       : t.patha,
                                        'gamepath'   : t.gamepatha,
                                        'patha'      : t.pathaf,
                                        'gamepatha'  : t.gamepathaf,
                                        'pathf'      : t.pathff,
                                        'gamepathf'  : t.gamepathff,
                                        'mobile'     : t.flyx,
                                        'stationary' : t.hover,
                                        'modestr'    : "Fly",
                                        'flight'     : "Fly",
                                    })
                                    setattr(t, self.GetState('DefaultMode') + "Mode", None)

                               # if (t.canqfly):
                               #     setattr(t, self.GetState('DefaultMode') + "Mode", t.QFlyMode)
                               #     self.makeSoDFile({
                               #         't'          : t,
                               #         'bl'         : t.blq,
                               #         'bla'        : t.blaq,
                               #         'blf'        : t.blfq,
                               #         'path'       : t.pathq,
                               #         'gamepath'   : t.gamepathq,
                               #         'patha'      : t.pathaq,
                               #         'pathf'      : t.pathfq,
                               #         'mobile'     : "Quantum Flight",
                               #         'stationary' : "Quantum Flight",
                               #         'modestr'    : "QFly",
                               #         'flight'     : "Fly",
                               #     })
                               #     setattr(t, self.GetState('DefaultMode') + "Mode", None)

                                # if (t.cangfly):
                                #     setattr(t, self.GetState('DefaultMode') + "Mode", t.GFlyMode)
                                #     self.makeSoDFile({
                                #         't'          : t,
                                #         'bl'         : t.blga,
                                #         'bla'        : t.blgaf,
                                #         'blf'        : t.blgff,
                                #         'path'       : t.pathga,
                                #         'gamepath'   : t.gamepathga,
                                #         'patha'      : t.pathgaf,
                                #         'pathf'      : t.pathgff,
                                #         'mobile'     : t.gfly,
                                #         'stationary' : t.gfly,
                                #         'modestr'    : "GFly",
                                #         'flight'     : "GFly",
                                #         'pathbo'     : t.pathgbo,
                                #         'pathsd'     : t.pathgsd,
                                #         'blbo'       : t.blgbo,
                                #         'blsd'       : t.blgsd,
                                #     })
                                #     setattr(t, self.GetState('DefaultMode') + "Mode", None)

                                if (self.GetState('TempEnable')):
                                    trayslot = "1 " + self.GetState('TempTray')
                                    setattr(t, self.GetState('DefaultMode') + "Mode", t.TempMode)
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : t.blt,
                                        'bla'        : t.blat,
                                        'blf'        : t.blft,
                                        'path'       : t.patht,
                                        'gamepath'   : t.gamepatht,
                                        'patha'      : t.pathat,
                                        'pathf'      : t.pathft,
                                        'mobile'     : trayslot,
                                        'stationary' : trayslot,
                                        'modestr'    : "Temp",
                                        'flight'     : "Fly",
                                    })
                                    setattr(t, self.GetState('DefaultMode') + "Mode", None)


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

        if (self.GetState('TurnLeft')):
            ResetFile.SetBind(self.Ctrls['TurnLeft'].MakeFileKeyBind("+turnleft"))
        if (self.GetState('TurnRight')):
            ResetFile.SetBind(self.Ctrls['TurnRight'].MakeFileKeyBind("+turnright"))

        if (self.GetState('TempEnable')):
            temptogglefile1 = profile.GetBindFile("temptoggle1.txt")
            temptogglefile2 = profile.GetBindFile("temptoggle2.txt")
            temptogglefile2.SetBind(self.Ctrls['TempTraySwitch'].MakeFileKeyBind('-down$$gototray 1' + profile.BLF('temptoggle1.txt')))
            temptogglefile1.SetBind(self.Ctrls['TempTraySwitch'].MakeFileKeyBind('+down$$gototray ' + self.GetState('TempTray') + profile.BLF('temptoggle2.txt')))
            ResetFile.SetBind(self.Ctrls['TempTraySwitch'].MakeFileKeyBind('+down$$gototray ' + self.GetState('TempTray') + profile.BLF('temptoggle2.txt')))

        ###### Kheldian power setup
        #  create the Nova and Dwarf form support files if enabled.

        ### TODO TODO TODO - these are just in here to make pylint happy;  fix the actual problem
        Nova = Dwarf = {}

        if (profile.Archetype() == "Warshade"):
            dwarfTPPower  = "powexecname Black Dwarf Step"
            normalTPPower = "powexecname Shadow Step"
        elif (profile.Archetype() == "Peacebringer"):
            dwarfTPPower = "powexecname White Dwarf Step"
        else:
            normalTPPower = "powexecname Teleport"
            teamTPPower   = "powexecname Team Teleport"

        if (self.GetState('HumanMode')):
            humanBindKey = self.GetState('HumanMode')
            humanpbind   = self.GetState('HumanHumanPBind')
            novapbind    = self.GetState('HumanNovaPBind')
            dwarfpbind   = self.GetState('HumanDwarfPBind')

        if ((profile.Archetype() == "Peacebringer") or (profile.General.GetState('Archetype') == "Warshade")):
            if (humanBindKey):
                ResetFile.SetBind(humanBindKey, humanpbind)

        fullstop = '$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'

        if (self.GetState('UseNova')):
            ResetFile.SetBind(self.GetState('NovaMode'),
                f"t $name, Changing to {Nova['Nova']} Form{fullstop}{t.on}{Nova['Nova']}$$gototray {self.GetState('NovaTray')}" + profile.BLF('nova.txt'))

            novafile = profile.GetBindFile("nova.txt")

            if (self.GetState('UseDwarf')):
                novafile.SetBind(self.GetState('DwarfMode'), f"t $name, Changing to {Dwarf['Dwarf']} Form{fullstop}{t.off}{Nova['Nova']}{t.on}{Dwarf['Dwarf']}$$gototray {self.GetState('DwarfTray')}" + profile.BLF('dwarf.txt'))

            if not humanBindKey:
                humanBindKey = self.GetState('NovaMode')

            if self.GetState('UseHumanFormPower'): humpower = '$$powexectoggleon ' + self.GetState('HumanFormShield')
            else:                                  humpower = ''

            novafile.SetBind(humanBindKey, f"t $name, Changing to Human Form, SoD Mode{fullstop}$$powexectoggleoff {Nova['Nova']} {humpower} $$gototray 1" + profile.BLF('reset.txt'))

            if (humanBindKey == self.GetState('NovaMode')): humanBindKey = None

            if novapbind: novafile.SetBind(self.GetState('NovaMode'), novapbind)

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

            if (self.GetState('HasTP')):
                novafile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('nop'))
                novafile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind( 'nop'))
                novafile.SetBind(self.Ctrls['TPResetKey'].MakeFileKeyBind('nop'))

            novafile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind("follow"))
            # novafile.SetBind(self.Ctrls['ToggleKey'].MakeFileKeyBind('t $name, Changing to Human Form, Normal Mode$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0$$powexectoggleoff ' + Nova['Nova'] + '$$gototray 1' + profile.BLF('reset.txt')))


        if (self.GetState('UseDwarf')):
            ResetFile.SetBind(self.GetState('DwarfMode'), f"t $name, Changing to {Dwarf['Dwarf']} Form{fullstop}$$powexectoggleon {Dwarf['Dwarf']}$$gototray {self.GetState('DwarfTray')}" + profile.BLF('dwarf.txt'))
            dwrffile = profile.GetBindFile("dwarf.txt")
            if (self.GetState('UseNova')):
                dwrffile.SetBind(self.GetState('NovaMode'), f"t $name, Changing to {Nova['Nova']} Form{fullstop}$$powexectoggleoff {Dwarf['Dwarf']}$$powexectoggleon {Nova['Nova']}$$gototray {self.GetState('NovaTray')}" + profile.BLF('nova.txt'))

            if not humanBindKey: humanBindKey = self.GetState('DwarfMode')
            if self.GetState('UseHumanFormPower'): humpower = '$$powexectoggleon ' + self.GetState('HumanFormShield')
            else:                               humpower = ''

            dwrffile.SetBind(humanBindKey, f"t $name, Changing to Human Form, SoD Mode{fullstop}$$powexectoggleoff {Dwarf['Dwarf']}{humpower}$$gototray 1" + profile.BLF('reset.txt'))

            if dwarfpbind:
                dwrffile.SetBind(self.GetState('DwarfMode'), dwarfpbind)
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

            if (self.GetState('HasTP')):
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

            dwrffile.SetBind(self.Ctrls['ToggleKey'].MakeFileKeyBind(f"t $name, Changing to Human Form, Normal Mode$fullstop$$powexectoggleoff {Dwarf['Dwarf']}$$gototray 1" + profile.BLF('reset.txt')))
        ### End Kheldian-specific stuff

        if (self.GetState('SimpleSJCJ')):
            if (self.GetState('HasCJ') and self.GetState('HasSJ')):
                ResetFile.SetBind(self.Ctrls['JumpMode'].MakeFileKeyBind('powexecname Super Jump$$powexecname Combat Jumping'))
            elif (self.GetState('HasSJ')):
                ResetFile.SetBind(self.Ctrls['JumpMode'].MakeFileKeyBind('powexecname Super Jump'))
            elif (self.GetState('HasCJ')):
                ResetFile.SetBind(self.Ctrls['JumpMode'].MakeFileKeyBind('powexecname Combat Jumping'))

        if (self.GetState('HasTP') and not normalTPPower):
            ResetFile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('nop'))
            ResetFile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind( 'nop'))
            ResetFile.SetBind(self.Ctrls['TPResetKey'].MakeFileKeyBind('nop'))

        if (self.GetState('HasTP') and not (profile.Archetype() == "Peacebringer") and normalTPPower):
            tphovermodeswitch = ''
            if (t.tphover != ''):
                tphovermodeswitch = t.BLF('R') + "000000.txt"

            ResetFile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('nop'))
            ResetFile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+down$$' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))
            ResetFile.SetBind(self.Ctrls['TPResetKey'].MakeFileKeyBind(t.detailhi[2:] + t.runcamdist + windowshow + profile.BLF('tp','tp_off.txt') + tphovermodeswitch))
            #  Create tp_off file
            tp_off = profile.GetBindFile("tp","tp_off.txt")
            tp_off.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('nop'))
            tp_off.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+down$$' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))

            tp_on1 = profile.GetBindFile("tp","tp_on1.txt")
            zoomin = t.detailhi + t.runcamdist
            if (t.tphover): zoomin = ''
            tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('-down$$powexecunqueue' + zoomin + windowshow + profile.BLF('tp','tp_off.txt') + tphovermodeswitch))
            tp_on1.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('+down' + t.tphover + profile.BLF('tp','tp_on2.txt')))

            tp_on2 = profile.GetBindFile("tp","tp_on2.txt")
            tp_on2.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('-down$$' + normalTPPower + profile.BLF('tp','tp_on1.txt')))

        if (self.GetState('HasTTP') and not (profile.Archetype() == "Peacebringer") and teamTPPower) :
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

    def sodResetKey(self, curfile, p, gamepath, turnoff, moddir):

        u = int(moddir == 'up')
        d = int(moddir == 'down')

        curfile.SetBind(p.General.Ctrls['ResetKey'].MakeFileKeyBind(
                f'up {u}$$down {d}$$forward 0$$backward 0$$left 0$$right 0' +
                str(turnoff) +
                '$$t $name, SoD Binds Reset$$' + curfile.BaseReset() +
                f"$$bindloadfile {gamepath}000000.txt"
        ))

    def sodUpKey(self, t, bl, curfile, mobile, stationary, flight, autorun, followbl, bo, sssj):

        (upx,dow,forw,bac,lef,rig) = (t.upx,t.dow,t.forw,t.bac,t.lef,t.rig)

        actkeys = t.totalkeys
        ml = ''

        if (not flight) and (not sssj):
            mobile = stationary = None

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
           else:                                   upx = '$$up 1'

           if (t.X == 1):                          upx = '$$up 0'

        toggleon   = mobile
        toggleoff  = None
        toggleoff2 = None
        if (actkeys == 0):
           ml = t.mlon
           toggleon = mobile
           if (not mobile) and (mobile != stationary) : toggleoff = stationary
        else:
            toggleon = ''


        if (t.totalkeys == 1 and t.space == 1):
           ml = t.mloff
           if (stationary != '') and (mobile != stationary) : toggleoff = mobile
           toggleon = stationary
        else:
            toggleoff = None

        if (sssj):
            if (t.space == 0): #  if we are hitting the space bar rather than releasing its..
               toggleon = sssj
               toggleoff = mobile
               if (stationary != '' and stationary != mobile) : toggleoff2 = stationary
            elif (t.space == 1) : #  if we are releasing the space bar ..
               toggleoff = sssj
               if (t.horizkeys > 0 or autorun) : #  and we are moving laterally, or in autorun..
                   toggleon = mobile
               else: #  otherwise turn on the stationary power..
                   toggleon = stationary

        toggle = ''
        if (toggleon or toggleoff):
           toggle = self.actPower_name(None,True,toggleon,toggleoff,toggleoff2)

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

    def sodDownKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo):
        (up,dowx,forw,bac,lef,rig) = (t.up,t.dowx,t.forw,t.bac,t.lef,t.rig)

        actkeys = t.totalkeys
        ml      = ''

        if (not flight):
            mobile = stationary = None
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
            # commented out in citybinder
            # if (t.cancj  == 1) : aj = t.cjmp
            # if (t.canjmp == 1) : aj = t.jump
            actkeys = t.jkeys
            if (t.X == 1 and t.totalkeys > 1) : up = '$$up 1'
            else:                               up = '$$up 0'

        toggleon = mobile
        toggleoff = None
        if (actkeys == 0):
           ml = t.mlon
           toggleon = mobile
           if (not mobile) and (mobile != stationary): toggleoff = stationary
        else:
           toggleon = None

        if (t.totalkeys == 1 and t.X == 1):
           ml = t.mloff
           if (stationary != '') and (mobile != stationary): toggleoff = mobile
           toggleon = stationary
        else:
            toggleoff = None

        toggle = ''
        if (toggleon or toggleoff):
           toggle = self.actPower_name(None,True,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'X'})
        bl = f"{bl}{newbits}.txt"

        if t.X == 1: ini = "-down"
        else:        ini = "+down"

        if (followbl):
            move = ''
            if (t.X != 1):
                bl = f"{followbl}{newbits}.txt"
                move = f"{up}{dowx}{forw}{bac}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Down'].MakeFileKeyBind(f"{ini}{move}{bl}"))
        elif (not autorun):
            curfile.SetBind(self.Ctrls['Down'].MakeFileKeyBind(f"{ini}{up}{dowx}{forw}{bac}{lef}{rig}{ml}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Down'].MakeFileKeyBind(f"{ini}{up}{dowx}$$backward 0{lef}{rig}{t.mlon}{bl}"))

    def sodForwardKey(self, t, bl, curfile,  mobile, stationary, flight, autorunbl, followbl, bo, sssj):
        (up,dow,forx,bac,lef,rig) = (t.up,t.dow,t.forx,t.bac,t.lef,t.rig)

        # actkeys = t.totalkeys
        ml = ''
        if (bo == "bo") : up = '$$up 1'; dow = '$$down 0'
        if (bo == "sd") : up = '$$up 0'; dow = '$$down 1'

        if (mobile     == 'Group Fly'): mobile = None
        if (stationary == 'Group Fly'): stationary = None

        if (flight == "Jump"):
           dow = '$$down 0'
           # actkeys = t.jkeys
           if (
                (t.totalkeys == 1 and t.W == 1)
                    or
                (t.X == 1)
           ):     up = '$$up 0'
           else : up = '$$up 1'

        toggleon = mobile
        toggleoff = None
        if (t.totalkeys == 0) :
            ml = t.mlon
            if (not mobile) and (mobile != stationary):
               toggleoff = stationary

        if (t.totalkeys == 1 and t.W == 1):
            ml = t.mloff

        if flight: testKeys = t.totalkeys
        else:      testKeys = t.horizkeys
        if (testKeys == 1 and t.W == 1) :
            if (stationary != '') and (mobile != stationary):
                toggleoff = mobile
            toggleon = stationary

        if (sssj and t.space == 1) : #  if (we are jumping with SS+SJ mode enabled)
           toggleon = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff):
           toggle = self.actPower_name(None,True,toggleon,toggleoff)

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
                if (t.W != 1) : move = f"{ini}{up}{dow}{forx}{bac}{rig}{lef}"
                curfile.SetBind('mousechord',  move + bl)

        elif (not autorunbl):
            curfile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind(f"{ini}{up}{dow}{forx}{bac}{lef}{rig}{ml}{toggle}{bl}"))
            if (self.GetState('MouseChord')):
                curfile.SetBind('mousechord', f"{ini}{up}{dow}{forx}{bac}{rig}{lef}{ml}{toggle}{bl}")

        else:
            if (t.W != 1):
                bl = f"{autorunbl}{newbits}.txt"

            curfile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind(f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{lef}{rig}{t.mlon}{bl}"))
            if (self.GetState('MouseChord')) :
                curfile.SetBind('mousechord', f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{rig}{lef}{t.mlon}{bl}")

    def sodBackKey(self,t,bl,curfile,mobile,stationary,flight,autorunbl,followbl,bo,sssj):
        (up,dow,forw,bacx,lef,rig) = (t.up,t.dow,t.forw, t.bacx,t.lef,t.rig)

        # actkeys = t.totalkeys
        ml = ''
        if (bo == "bo") : up = '$$up 1';dow = '$$down 0'
        if (bo == "sd") : up = '$$up 0';dow = '$$down 1'

        if (mobile     == 'Group Fly'): mobile = None
        if (stationary == 'Group Fly'): stationary = None

        if (flight == "Jump"):
           dow = '$$down 0'
           # actkeys = t.jkeys
           if (t.totalkeys == 1 and t.S == 1) : up = '$$up 0'
           else:                                up = '$$up 1'

           if (t.X == 1) : up = '$$up 0'

        toggleon = mobile
        toggleoff = None
        if (t.totalkeys == 0):
           ml = t.mlon
           toggleon = mobile
           if (not mobile) and (mobile != stationary):
               toggleoff = stationary

        if (t.totalkeys == 1 and t.S == 1):
            ml = t.mloff

        if flight: testKeys = t.totalkeys
        else:      testKeys = t.horizkeys
        if (testKeys == 1 and t.S == 1):
            if (stationary != '') and (mobile != stationary):
               toggleoff = mobile

            toggleon = stationary

        if (sssj and t.space == 1): #  if (we are jumping with SS+SJ mode enabled
            toggleon = sssj
            toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
           toggle = self.actPower_name(None,True,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'S'})
        bl = f"{bl}{newbits}.txt"

        if (t.S == 1) : ini = "-down"
        else:           ini = "+down"

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

        # actkeys = t.totalkeys
        ml = ''
        if (bo == "bo") : up = '$$up 1';dow = '$$down 0'
        if (bo == "sd") : up = '$$up 0';dow = '$$down 1'

        if (mobile     == 'Group Fly') : mobile = None
        if (stationary == 'Group Fly') : stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            # actkeys = t.jkeys
            if (t.totalkeys == 1 and t.A == 1) : up = '$$up 0'
            else:                                up = '$$up 1'

            if (t.X == 1) : up = '$$up 0'

        toggleon = mobile
        toggleoff = None
        if (t.totalkeys == 0):
            ml = t.mlon
            toggleon = mobile
            if (not mobile) and (mobile != stationary) :
                toggleoff = stationary

        if (t.totalkeys == 1 and t.A == 1) :
            ml = t.mloff

        if flight: testKeys = t.totalkeys
        else:      testKeys = t.horizkeys

        if (testKeys == 1 and t.A == 1) :
            if (stationary != '') and (mobile != stationary):
               toggleoff = mobile
            toggleon = stationary

        if (sssj and t.space == 1) : #  if (we are jumping with SS+SJ mode enabled
           toggleon  = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
           toggle = self.actPower_name(None,True,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'A'})
        bl = f"{bl}{newbits}.txt"

        if (t.A == 1): ini = '-down'
        else:          ini = '+down'

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

        # actkeys = t.totalkeys
        ml = ''
        if (bo == "bo") :up = '$$up 1';dow = '$$down 0'
        if (bo == "sd") :up = '$$up 0';dow = '$$down 1'

        if (mobile     == 'Group Fly') : mobile = None
        if (stationary == 'Group Fly') : stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            # actkeys = t.jkeys
            if (t.totalkeys == 1 and t.D == 1) : up = '$$up 0'
            else:                                up = '$$up 1'

            if (t.X == 1) : up = '$$up 0'

        toggleon = mobile
        toggleoff = None
        if (t.totalkeys == 0):
           ml = t.mlon
           toggleon = mobile
           if (not mobile) and (mobile != stationary) :
               toggleoff = stationary

        if (t.totalkeys == 1 and t.D == 1) :
           ml = t.mloff

        if flight: testKeys = t.totalkeys
        else :     testKeys = t.horizkeys
        if (testKeys == 1 and t.D == 1) :
            if (stationary != '') and (mobile != stationary):
               toggleoff = mobile
            toggleon = stationary

        if (sssj and t.space == 1) : #  if (we are jumping with SS+SJ mode enabled
           toggleon = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
           toggle = self.actPower_name(None,True,toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'D'})
        bl = f"{bl}{newbits}.txt"

        if (t.D == 1): ini = '-down'
        else:          ini = '+down'

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
        bindload = bl + t.KeyState() + ".txt"
        if (sssj and t.space == 1) :
            curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mlon + self.actPower_name(None,True,sssj,mobile) + bindload))
        else:
            curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mlon + self.actPower_name(None,True,mobile) + bindload))

    # TODO sssj never gets passed in, in citybinder.  Is this right?
    def sodAutoRunOffKey(self, t,bl,curfile,mobile,stationary,flight,sssj = None):
        toggleon = toggleoff = None
        if sssj and t.space == 1:
            toggleoff = mobile
            mobile = sssj
        if (not flight) and (not sssj) :
            if (t.horizkeys > 0) :
                toggleon = t.mlon + self.actPower_name(None,True,mobile)
            else:
                toggleon = t.mloff + self.actPower_name(None,True,stationary,mobile)

        elif (sssj) :
            if (t.horizkeys > 0 or t.space == 1) :
                toggleon = t.mlon + self.actPower_name(None,True,mobile,toggleoff)
            else:
                toggleon = t.mloff + self.actPower_name(None,True,stationary,mobile,toggleoff)

        else:
            if (t.totalkeys > 0) :
                toggleon = t.mlon + self.actPower_name(None,True,mobile)
            else:
                toggleon = t.mloff + self.actPower_name(None,True,stationary,mobile)

        bindload = bl + t.KeyState() + '.txt'
        # "[2:]" on next line is to trim off the initial "$$" that dirs() provides
        curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind(t.dirs('UDFBLR')[2:] + toggleon + bindload))

    def sodFollowKey(self, t,bl,curfile,mobile):
        curfile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind('follow' + self.actPower_name(None,True,mobile) + bl + t.KeyState() + '.txt'))

    def sodFollowOffKey(self, t,bl,curfile,mobile,stationary,flight):
        toggle = ''
        if (not flight):
            if (t.horizkeys == 0) :
                if (stationary != mobile) :
                   toggle = self.actPower_name(None,True,stationary,mobile)
                else:
                   toggle = self.actPower_name(None,True,stationary)

        else:
            if (t.totalkeys == 0) :
                if (stationary != mobile) :
                   toggle = self.actPower_name(None,True,stationary,mobile)
                else:
                   toggle = self.actPower_name(None,True,stationary)

        curfile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind("follow" + toggle + t.up + t.dow + t.forw + t.bac + t.lef + t.rig + bl + t.KeyState() + '.txt'))

    #  toggleon variation
    def actPower_toggle(self, start, unq, on, *rest):
        s = traytest = ''

        # TODO Temp Travel Power stuff - might comment all this out
        if on and not isinstance(on, str):
            #  deal with power slot stuff..
            traytest = on['trayslot']

        unq = False  # we pass 'unq' in and ignore it to have the same signature as actPower_name
        offpower = set()

        w = None # TODO remove this when fixing 'v' vs 'w' below
        for v in rest:
            if v and not isinstance(v, str):
                for w in v:
                    if (w and w != on and not (w in offpower)):
                        if not isinstance(w, str):
                            if (w['trayslot'] != traytest):
                               s = s + '$$powexectray ' + w['trayslot']
                               unq = True
                        else:
                            offpower.add(w)
                            s = s + '$$powexectoggleoff ' + w

                # TODO This is part of Temp Travel Power which might go away
                # It currently breaks because v is a set not a dict.
                #
                # if (v['trayslot'] and v['trayslot'] != traytest):
                #    s = s + '$$powexectray ' + v['trayslot']
                #    unq = True

            else:
                # TODO -- the uncommented line is as in citybinder.  I think it's a bug
                # talking about w instead of v.  I am going with it for now while diffing
                #if (v != '' and (v != on) and not (v in offpower)):
                if (v != '' and (w != on) and not (v in offpower)):
                    offpower.add(v)
                    s = s + '$$powexectoggleoff ' + v

        if (unq and s):
            s = s + '$$powexecunqueue'

        if (on and on != ''):
            if not (isinstance(on, str)):
                #  deal with power slot stuff..
                s = s + '$$powexectray ' + on['trayslot'] + '$$powexectray ' + on['trayslot']
            else:
                s = s + '$$powexectoggleon ' + on

        # TODO this is commented out in citybinder, but seems to be needed here
        # It's a mystery.
        if start: s = s[2:]
        return s

    def actPower_name(self, start, unq, on, *rest):
        s = traytest = ''
        if isinstance(on, dict):
           #  deal with power slot stuff..
           traytest = on['trayslot']

        for v in rest:
            if isinstance(v, str):
                if (v != '' and v != on):
                    s = s + '$$powexecname ' + v

            elif isinstance(v, list):  # TODO change to set later
                for w in v:
                    if (w and w != on):
                        if isinstance(w, dict):
                            if (w['trayslot'] != traytest):
                                s = s + '$$powexectray ' + w['trayslot']
                        else:
                            s = s + '$$powexecname ' + w

                # TODO Temp Travel Power stuff -- maybe comment out later
                # if (v['trayslot'] and v['trayslot'] != traytest):
                #    s = s + '$$powexectray ' + v['trayslot']

        if (unq and s != ''):
            s = s + '$$powexecunqueue'

        if (on and on != ''):
            if isinstance(on, str):
                s = s + '$$powexecname ' + on + '$$powexecname ' + on
            else:
                #  deal with power slot stuff..
                s = s + '$$powexectray ' + on['trayslot'] + '$$powexectray ' + on['trayslot']

        if (start): s = s[2:]
        return s

    actPower = actPower_name
    # actPower = actPower_toggle

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

        filename = getattr(t,"path" + f"{autofollowmode}j") + t.KeyState() + suffix + '.txt'
        gamefilename = getattr(t,"gamepath" + f"{autofollowmode}j") + t.KeyState() + suffix + '.txt'
        tglfile  = profile.GetBindFile(filename)
        t.ini    = '-down$$'
        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key, "+down" + feedback + self.actPower_name(None,True,t.cjmp) + profile.BLF(gamefilename))

    def sodSetDownFix(self, profile,t,key,makeModeKey,suffix,bl,curfile,turnoff,autofollowmode,feedback):
        if autofollowmode:
            pathsuffix = "f"
        else:
            pathsuffix = "a"

        filename = getattr(t,'path' + f"{autofollowmode}{pathsuffix}") + t.KeyState() + suffix + ".txt"
        gamefilename = getattr(t,'gamepath' + f"{autofollowmode}{pathsuffix}") + t.KeyState() + suffix + ".txt"
        tglfile = profile.GetBindFile(filename)
        t.ini = '-down$$'

        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key, '+down' + feedback + profile.BLF(gamefilename))

    def bindBothResetFiles(self, key, contents):
        self.Profile.ResetFile.BindKey(key, contents)
        if key != self.Ctrls['ResetKey']:
            subresetpath = Path(self.Profile.BindsDir) / "subreset.txt"
            subresetfile = self.Profile.GetBindFile(subresetpath)
            subresetfile.BindKey(key, contents)

    def onCBLabelClick(self, evt):
        cblabel = evt.EventObject
        cblabel.control.SetValue(not cblabel.control.IsChecked())
        evt.Skip()

UI.Labels.update( {
    'Up'             : 'Up',
    'Down'           : 'Down',
    'Forward'        : 'Forward',
    'Back'           : 'Back',
    'Left'           : 'Strafe Left',
    'Right'          : 'Strafe Right',
    'TurnLeft'       : 'Turn Left',
    'TurnRight'      : 'Turn Right',
    'AutoRun'        : 'Auto Run',
    'Follow'         : 'Follow Target',

    'DefaultMode'    : 'Default SoD Mode',
    'MouseChord'     : 'Mousechord is SoD Forward',
    'AutoMouseLook'  : 'Mouselook when moving',

    'SprintPower'    : 'Power to use for Sprint',

    'ChangeCamera'   : 'Change camera distance when moving',
    'CamdistBase'    : 'Base Camera Distance',
    'CamdistMove'    : 'Travelling Camera Distance',

    'ChangeDetail'   : 'Change graphics detail level when moving',
    'DetailBase'     : 'Base Detail Level',
    'DetailMove'     : 'Travelling Detail Level',
    'TPHideWindows'  : 'Hide Windows when Teleporting',

    'HasSJ'          : 'Player has Super Jump',
    'HasCJ'          : 'Player has Combat Jumping',
    'NonSoDEnable'   : 'Enable Non-SoD Movement Mode',
    'NonSoDMode'     : 'Non-SoD Key',
    'SprintSoD'      : 'Enable Sprint SoD',
    'SprintMode'     : "Sprint Mode Key",

    'JumpMode'       : 'Toggle Jump Mode',
    'SimpleSJCJ'     : 'Simple Combat Jumping / Super Jump Toggle',

    'HasSS'          : 'Player has Super Speed',
    'RunMode'        : 'Toggle Super Speed Mode',
    'SSMobileOnly'   : 'SuperSpeed only when moving',
    'SSSJModeEnable' : 'Enable Super Speed / Super Jump Mode',

    'HasHover'       : "Player has Hover",
    'HasFly'         : "Player has Flight",
    'HasCF'          : 'Player has Combat Flying',
    'FlyMode'        : 'Toggle Fly Mode',
    'HasQF'          : 'Player has Quantum Flight',
    'QFlyMode'       : 'Toggle Quantum Fly Mode',

    'Feedback'       : 'Self-/tell when changing mode',

    'HasTP'          : 'Player has Teleport',
    'TPBindKey'      : 'Teleport Bind',
    'TPComboKey'     : 'Teleport Combo Key',
    'TPResetKey'     : 'Teleport Reset Key',
    'TPTPHover'      : 'Hover when Teleporting',

    'HasTTP'         : 'Player has Team Teleport',
    'TTPBindKey'     : 'Team Teleport Bind',
    'TTPComboKey'    : 'Team Teleport Combo Key',
    'TTPResetKey'    : 'Team Teleport Reset Key',
    'TTPAutoGFly'    : 'Group Fly when Team Teleporting',

    'TempEnable'     : 'Enable Temp Travel Mode',
    'TempMode'       : 'Toggle Temp Mode',
    'TempTray'       : 'Temporary Travel Power Tray',
    'TempTraySwitch' : "Tray Toggle Key",

    'UseNova'        : 'Use Nova Form Toggle',
    'NovaMode'       : 'Toggle Nova Form',
    'NovaTray'       : 'Nova Travel Power Tray',
    'UseDwarf'       : 'Use Dwarf Form Toggle',
    'DwarfMode'      : 'Toggle Dwarf Form',
    'DwarfTray'      : 'Dwarf Travel Power Tray',
    'HumanMode'      : 'Human Form',
    'HumanTray'      : 'Human Travel Power Tray',
})

class tObject(dict):
    def __init__(self, profile):
            self.profile    = profile
            self.ini        = ''
            self.sprint     = None
            self.speed      = None
            self.hover      = None
            self.fly        = None
            self.flyx       = None
            self.jump       = None
            self.cjmp       = ''
            self.canhov     = 0
            self.canfly     = 0
            self.canqfly    = 0
            self.cangfly    = 0
            self.cancj      = 0
            self.canjmp     = 0
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
            self.NonSoDMode = ''
            self.SprintMode = ''
            self.FlyMode    = ''
            self.JumpMode   = ''
            self.RunMode    = ''
            self.GFlyMode   = ''
            self.TempMode   = ''
            self.QFlyMode   = ''
            self.jumpifnocj = ''

            self.space :int = 0
            self.X :int     = 0
            self.W :int     = 0
            self.S :int     = 0
            self.A :int     = 0
            self.D :int     = 0
            self.up         = ''
            self.dow        = ''
            self.forw       = ''
            self.bac        = ''
            self.lef        = ''
            self.rig        = ''
            self.upx        = ''
            self.dowx       = ''
            self.forx       = ''
            self.bacx       = ''
            self.lefx       = ''
            self.rigx       = ''

            self.bl   = ''
            self.bla  = ''
            self.blaf = ''
            self.blaj = ''
            self.blan = ''
            self.blaq = ''
            self.blas = ''
            self.blat = ''
            self.blbo = ''
            self.blf  = ''
            self.blff = ''
            self.blfn = ''
            self.blfj = ''
            self.blfq = ''
            self.blfs = ''
            self.blft = ''
            self.blfr = ''
            self.blgr = ''
            self.blj  = ''
            self.bln  = ''
            self.blq  = ''
            self.bls  = ''
            self.blsd = ''
            self.blt  = ''

            self.path   = ''
            self.patha  = ''
            self.pathaf = ''
            self.pathaj = ''
            self.pathan = ''
            self.pathaq = ''
            self.pathas = ''
            self.pathat = ''
            self.pathbo = ''
            self.pathf  = ''
            self.pathff = ''
            self.pathfn = ''
            self.pathfj = ''
            self.pathfq = ''
            self.pathfs = ''
            self.pathft = ''
            self.pathfr = ''
            self.pathgr = ''
            self.pathj  = ''
            self.pathn  = ''
            self.pathq  = ''
            self.paths  = ''
            self.pathsd = ''
            self.patht  = ''

            self.gamepath   = ''
            self.gamepatha  = ''
            self.gamepathaf = ''
            self.gamepathaj = ''
            self.gamepathan = ''
            self.gamepathaq = ''
            self.gamepathas = ''
            self.gamepathat = ''
            self.gamepathbo = ''
            self.gamepathf  = ''
            self.gamepathff = ''
            self.gamepathfn = ''
            self.gamepathfj = ''
            self.gamepathfq = ''
            self.gamepathfs = ''
            self.gamepathft = ''
            self.gamepathfr = ''
            self.gamepathgr = ''
            self.gamepathj  = ''
            self.gamepathn  = ''
            self.gamepathq  = ''
            self.gamepaths  = ''
            self.gamepathsd = ''
            self.gamepatht  = ''

            self.basepath     = ''
            self.gamebasepath = ''

            self.path         = ''
            self.gamepath     = ''

            self.vertkeys  :int = 0
            self.horizkeys :int = 0
            self.jkeys     :int = 0
            self.totalkeys :int = 0


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
           ret += getattr(self, dirdict[dir])

        return ret

    # This will return "$bindloadfilesilent C:\path\CODE\CODE101010<suffix>.txt"
    def BLF(self, code, suffix = ''):
        return self.profile.BLF(code.upper(), code.upper() + self.KeyState() + suffix + '.txt')
