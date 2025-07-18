import re
import wx
import GameData
import UI
from pathlib import Path, PureWindowsPath
from typing import Dict, Any
from BLF import BLF
from Page import Page
from Icon import GetIcon
from UI.ControlGroup import ControlGroup, bcKeyButton
from UI.KeySelectDialog import EVT_KEY_CHANGED
from UI.PowerPicker import PowerPicker

class MovementPowers(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Movement / Speed on Demand"

        self.TempTravelPowerMenu = None

        # A few things that are server-specific.  If we change servers, we reload the profile
        # so this is safe to do in __init__
        server = self.Profile.Server
        self.togon   = "powexectoggleon"  if server == "Homecoming" else "px_tgon"
        self.togoff  = "powexectoggleoff" if server == "Homecoming" else "px_tgof"
        self.unqueue = "powexecunqueue"   if server == "Homecoming" else "px_uq"

        self.Init: Dict[str, Any] = {
            'EnableSoD'       : False,

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
            'PlayerTurn'      : 0, # TODO this should toggle with "Keybind Profile" somehow
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
            'NonSoDMode'      : '',

            'SpeedPower'        : '',
            'SpeedMode'         : "C",
            'SSMobileOnly'      : False,
            'SSSJModeEnable'    : False,
            'SpeedSpecialKey'   : "",
            'SpeedSpecialPower' : "",

            'JumpPower'        : '',
            'HasCJ'            : False,
            'JumpMode'         : "T",
            'SimpleSJCJ'       : False,
            'JumpSpecialKey'   : "",
            'JumpSpecialPower' : "",

            'FlyPower'        : '',
            'HoverPower'      : '', # hidden
            'HasHover'        : False,
            'HasGFly'         : False,
            'HasQF'           : False, # hidden
            'FlyMode'         : "F",
            'GFlyMode'        : "",
            'FlySpecialKey'   : "",
            'FlySpecialPower' : "", # hidden

            'TPPower'         : '',
            'TPBindKey'       : '',
            'TPComboKey'      : 'LSHIFT',
            'TPExecuteKey'    : 'LSHIFT+BUTTON1',

            'HasTTP'          : False,
            'TTPBindKey'      : '',
            'TTPComboKey'     : 'LCTRL',
            'TTPExecuteKey'   : 'LCTRL+BUTTON1',
            'TTPTPGFly'       : False,

            'TPHideWindows'   : True,
            'TPTPHover'       : False,

            'FlyGFly'         : '',

            'HumanTray'       : "1",

            'UseNova'         : False,
            'NovaMode'        : "[",
            'NovaTray'        : "4",

            'UseDwarf'        : False,
            'DwarfMode'       : "]",
            'DwarfTray'       : "5",


            'TempEnable'      : False,
            'TempToggle'      : "",
        }

        if self.Profile.Server == "Homecoming":
            UI.Labels.update({
                'TPBindKey'      : 'Teleport to Cursor Immediately',
                'TTPBindKey'     : 'Team Teleport to Cursor Immediately',
            })
        else:
            UI.Labels.update({
                'TPBindKey'      : 'Activate Teleport Power',
                'TTPBindKey'     : 'Activate Team Teleport Power',
            })

    def BuildPage(self):

        server = self.Profile.Server

        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.leftColumn  = wx.BoxSizer(wx.VERTICAL)
        self.rightColumn = wx.BoxSizer(wx.VERTICAL)

        # hidden controls for keeping state
        self.hiddenSizer = ControlGroup(self, self, "Hidden Settings")
        self.hiddenSizer.AddControl( ctlName = 'HoverPower', ctlType = 'text')
        self.hiddenSizer.AddControl( ctlName = 'HasQF', ctlType = 'checkbox',)
        self.hiddenSizer.AddControl( ctlName = 'FlySpecialPower', ctlType = 'text', )
        self.hiddenSizer.AddControl( ctlName = 'JumpSpecialPower', ctlType = 'text', )
        self.hiddenSizer.AddControl( ctlName = 'SpeedSpecialPower', ctlType = 'text', )
        self.leftColumn.Add(self.hiddenSizer)
        self.leftColumn.Hide(self.hiddenSizer)

        ##### MOVEMENT KEYS
        movementSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label = "Movement Keys")
        staticbox = movementSizer.GetStaticBox()
        innerSizer = wx.BoxSizer(wx.VERTICAL)
        movementSizer.Add(innerSizer, 1, wx.ALL|wx.ALIGN_CENTER, 10)

        keySizer = wx.GridBagSizer(6, 3)
        tlLabel = wx.StaticText(staticbox, label = 'Turn Left')
        fwLabel = wx.StaticText(staticbox, label = 'Forward')
        trLabel = wx.StaticText(staticbox, label = 'Turn Right')

        keySizer.Add(tlLabel, wx.GBPosition(0,0), wx.GBSpan(1,2), wx.ALIGN_CENTER)
        keySizer.Add(fwLabel, wx.GBPosition(0,2), wx.GBSpan(1,2), wx.ALIGN_CENTER)
        keySizer.Add(trLabel, wx.GBPosition(0,4), wx.GBSpan(1,2), wx.ALIGN_CENTER)

        tleftButton = bcKeyButton(staticbox, -1, )
        tleftButton.SetLabel(self.Init['TurnLeft'])
        self.Ctrls['TurnLeft'] = tleftButton
        tleftButton.CtlName = 'TurnLeft'
        tleftButton.CtlLabel = tlLabel
        tleftButton.Page = self
        tleftButton.Key = self.Init['TurnLeft']
        keySizer.Add(tleftButton, wx.GBPosition(1,0), wx.GBSpan(1,2))

        forwardButton = bcKeyButton(staticbox, -1, )
        self.Ctrls['Forward'] = forwardButton
        forwardButton.SetLabel(self.Init['Forward'])
        forwardButton.CtlName = 'Forward'
        forwardButton.CtlLabel = fwLabel
        forwardButton.Page = self
        forwardButton.Key = self.Init['Forward']
        keySizer.Add(forwardButton, wx.GBPosition(1,2), wx.GBSpan(1,2))

        trightButton = bcKeyButton(staticbox, -1, )
        self.Ctrls['TurnRight'] = trightButton
        trightButton.SetLabel(self.Init['TurnRight'])
        trightButton.CtlName = 'TurnRight'
        trightButton.CtlLabel = trLabel
        trightButton.Page = self
        trightButton.Key = self.Init['TurnRight']
        keySizer.Add(trightButton, wx.GBPosition(1,4), wx.GBSpan(1,2))

        leftLabel = wx.StaticText(staticbox, label = 'Left')
        backLabel = wx.StaticText(staticbox, label = 'Back')
        rightLabel = wx.StaticText(staticbox, label = 'Right')

        leftButton = bcKeyButton(staticbox, -1, )
        self.Ctrls['Left'] = leftButton
        leftButton.SetLabel(self.Init['Left'])
        leftButton.CtlName = 'Left'
        leftButton.CtlLabel = leftLabel
        leftButton.Page = self
        leftButton.Key = self.Init['Left']
        keySizer.Add(leftButton, wx.GBPosition(2,0), wx.GBSpan(1,2))

        backButton = bcKeyButton(staticbox, -1, )
        backButton.SetLabel(self.Init['Back'])
        self.Ctrls['Back'] = backButton
        backButton.CtlName = 'Back'
        backButton.CtlLabel = backLabel
        backButton.Page = self
        backButton.Key = self.Init['Back']
        keySizer.Add(backButton, wx.GBPosition(2,2), wx.GBSpan(1,2))

        rightButton = bcKeyButton(staticbox, -1, )
        self.Ctrls['Right'] = rightButton
        rightButton.SetLabel(self.Init['Right'])
        rightButton.CtlName = 'Right'
        rightButton.CtlLabel = rightLabel
        rightButton.Page = self
        rightButton.Key = self.Init['Right']
        keySizer.Add(rightButton, wx.GBPosition(2,4), wx.GBSpan(1,2))

        keySizer.Add(leftLabel,  wx.GBPosition(3,0), wx.GBSpan(1,2), wx.ALIGN_CENTER)
        keySizer.Add(backLabel,  wx.GBPosition(3,2), wx.GBSpan(1,2), wx.ALIGN_CENTER)
        keySizer.Add(rightLabel, wx.GBPosition(3,4), wx.GBSpan(1,2), wx.ALIGN_CENTER)

        downLabel = wx.StaticText(staticbox, label = 'Down')
        upLabel   = wx.StaticText(staticbox, label = 'Up')

        keySizer.Add(downLabel, wx.GBPosition(4,0), wx.GBSpan(1,2), wx.ALIGN_CENTER|wx.TOP, 16)
        keySizer.Add(upLabel,   wx.GBPosition(4,2), wx.GBSpan(1,4), wx.ALIGN_CENTER|wx.TOP, 16)

        downButton = bcKeyButton(staticbox, -1, )
        self.Ctrls['Down'] = downButton
        downButton.SetLabel(self.Init['Down'])
        downButton.CtlName = 'Down'
        downButton.CtlLabel = downLabel
        downButton.Page = self
        downButton.Key = self.Init['Down']
        keySizer.Add(downButton, wx.GBPosition(5,0), wx.GBSpan(1,2), wx.EXPAND)

        upButton = bcKeyButton(staticbox, -1, )
        self.Ctrls['Up'] = upButton
        upButton.SetLabel(self.Init['Up'])
        upButton.CtlName = 'Up'
        upButton.CtlLabel = upLabel
        upButton.Page = self
        upButton.Key = self.Init['Up']
        keySizer.Add(upButton, wx.GBPosition(5,2), wx.GBSpan(1,4), wx.EXPAND)

        autoRunLabel = wx.StaticText(staticbox, label = 'Autorun')
        followLabel  = wx.StaticText(staticbox, label = 'Follow')

        keySizer.Add(autoRunLabel, wx.GBPosition(6,1), wx.GBSpan(1,2), wx.ALIGN_CENTER)
        keySizer.Add(followLabel,  wx.GBPosition(6,3), wx.GBSpan(1,2), wx.ALIGN_CENTER)

        autoRunButton = bcKeyButton(staticbox, -1, )
        self.Ctrls['AutoRun'] = autoRunButton
        autoRunButton.SetLabel(self.Init['AutoRun'])
        autoRunButton.CtlName = 'AutoRun'
        autoRunButton.CtlLabel = autoRunLabel
        autoRunButton.Page = self
        autoRunButton.Key = self.Init['AutoRun']
        keySizer.Add(autoRunButton, wx.GBPosition(7,1), wx.GBSpan(1,2), wx.EXPAND)

        followButton = bcKeyButton(staticbox, -1, )
        self.Ctrls['Follow'] = followButton
        followButton.SetLabel(self.Init['Follow'])
        followButton.CtlName = 'Follow'
        followButton.CtlLabel = followLabel
        followButton.Page = self
        followButton.Key = self.Init['Follow']
        keySizer.Add(followButton, wx.GBPosition(7,3), wx.GBSpan(1,2), wx.EXPAND)

        innerSizer.Add(keySizer, 0)

        self.leftColumn.Add(movementSizer, 0, wx.EXPAND)

        ### DETAIL SETTINGS
        detailSizer = ControlGroup(self, self, 'Detail and Camera Settings')
        detailSizer.AddControl( ctlName = 'PlayerTurn', ctlType = 'checkbox',
            tooltip = 'Turn player to match camera when moving forward',)
        detailSizer.AddControl( ctlName = 'AutoMouseLook', ctlType = 'checkbox',
           tooltip = 'Automatically engage mouselook while movement keys are pressed',)
        detailSizer.AddControl( ctlName = 'ChangeCamera', ctlType = 'checkbox',
            tooltip = "Change the camera distance while moving")
        self.Ctrls['ChangeCamera'].Bind(wx.EVT_CHECKBOX, self.OnDetailsCameraChanged)
        detailSizer.AddControl( ctlName = 'CamdistBase', ctlType = 'spinbox', contents = (1, 100),
            tooltip = "Set the camera distance to use while stationary")
        detailSizer.AddControl( ctlName = 'CamdistMove', ctlType = 'spinbox', contents = (1, 100),
            tooltip = "Set the camera distance to use while moving")
        detailSizer.AddControl( ctlName = 'ChangeDetail', ctlType = 'checkbox',
            tooltip = "Change the game's detail level while moving")
        self.Ctrls['ChangeDetail'].Bind(wx.EVT_CHECKBOX, self.OnDetailsCameraChanged)
        detailSizer.AddControl( ctlName = 'DetailBase', ctlType = 'spinboxfractional', contents = (0, 1),
            tooltip = "Set the detail level to use while stationary")
        detailSizer.AddControl( ctlName = 'DetailMove', ctlType = 'spinboxfractional', contents = (0, 1),
            tooltip = "Set the detail level to use while moving")
        self.leftColumn.Add(detailSizer, 0, wx.EXPAND)

        ##### KHELDIAN TRAVEL POWERS
        self.kheldianSizer = ControlGroup(self, self, 'Kheldian Forms / Powers')

        self.kheldianSizer.AddControl( ctlName = 'HumanTray', ctlType = 'spinbox', contents = [1, 8],
            tooltip = "Select the powers tray to change to when in human form")
        self.kheldianSizer.AddControl( ctlName = 'UseNova', ctlType = 'checkbox',
            tooltip = "Use a key to toggle between Nova and human form")
        self.Ctrls['UseNova'].Bind(wx.EVT_CHECKBOX, self.OnKheldianChanged)
        self.kheldianSizer.AddControl( ctlName = 'NovaMode', ctlType = 'keybutton',
            tooltip = "Select the key to toggle between Nova and human form")
        self.kheldianSizer.AddControl( ctlName = 'NovaTray', ctlType = 'spinbox', contents = [1, 8],
            tooltip = "Select the powers tray to change to when in Nova form")
        self.kheldianSizer.AddControl( ctlName = 'UseDwarf', ctlType = 'checkbox',
            tooltip = "Use a key to toggle between Dwarf and human form")
        self.Ctrls['UseDwarf'].Bind(wx.EVT_CHECKBOX, self.OnKheldianChanged)
        self.kheldianSizer.AddControl( ctlName = 'DwarfMode', ctlType = 'keybutton',
            tooltip = "Select the key to toggle between Dwarf and human form")
        self.kheldianSizer.AddControl( ctlName = 'DwarfTray', ctlType = 'spinbox', contents = [1, 8],
            tooltip = "Select the powers tray to change to when in Dwarf form")
        self.leftColumn.Add(self.kheldianSizer, 0, wx.EXPAND)

        ##### SPEED ON DEMAND SETTINGS
        SoDSizer = ControlGroup(self, self, 'Speed on Demand Settings')

        SoDSizer.AddControl( ctlName = 'EnableSoD', ctlType = 'checkbox',
            tooltip = "Enable Speed on Demand behavior for the movement keys")
        self.Ctrls['EnableSoD'].Bind(wx.EVT_CHECKBOX, self.OnSpeedOnDemandChanged)
        SoDSizer.AddControl( ctlName = 'DefaultMode', ctlType = 'choice',
            contents = ('No SoD','Sprint','Speed','Jump','Fly'),
            tooltip = "Select the Speed on Demand mode the movement keys will use by default")
        self.Ctrls['DefaultMode'].Bind(wx.EVT_CHOICE, self.OnSpeedOnDemandChanged)
        SoDSizer.AddControl( ctlName = 'SprintPower', ctlType = 'choice',
            contents = GameData.SprintPowers,
            tooltip = "Select the power to use for Sprint Speed on Demand")
        SoDSizer.AddControl( ctlName = 'NonSoDEnable', ctlType = 'checkbox',
            tooltip = "Use a key to toggle whether Speed on Demand is active")
        self.Ctrls['NonSoDEnable'].Bind(wx.EVT_CHECKBOX, self.OnSpeedOnDemandChanged)
        SoDSizer.AddControl( ctlName = 'NonSoDMode', ctlType = 'keybutton',
            tooltip = "Select the key to toggle Speed on Demand")
        SoDSizer.AddControl( ctlName = 'SprintSoD', ctlType = 'checkbox',)
        self.Ctrls['SprintSoD'].Bind(wx.EVT_CHECKBOX, self.OnSpeedOnDemandChanged)
        SoDSizer.AddControl( ctlName = 'SprintMode', ctlType = 'keybutton',)
        SoDSizer.AddControl( ctlName = 'MouseChord', ctlType = 'checkbox',)
        SoDSizer.AddControl( ctlName = 'Feedback', ctlType = 'checkbox',
            tooltip = "Announce changes in Speed on Demand modes via self-/tell")

        self.rightColumn.Add(SoDSizer, 0, wx.EXPAND)

        ##### TEMP TRAVEL POWERS
        self.tempSizer = ControlGroup(self, self, 'Temp Travel Powers')
        self.tempSizer.AddControl( ctlName = 'TempEnable', ctlType = 'checkbox',
                                  tooltip = "Enable the Temp Travel Power toggle keybind")
        self.Ctrls['TempEnable'].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        self.tempSizer.AddControl( ctlName = 'TempToggle', ctlType = 'keybutton',
                                  tooltip = "Select the key to use to toggle the chosen temp travel power")
        self.Ctrls['TempToggle'].Bind(EVT_KEY_CHANGED, self.OnTempChanged)
        self.TempTravelPowerLabel = wx.StaticText(self.tempSizer.GetStaticBox(), wx.ID_ANY, "Temp Travel Power:", style = wx.ALIGN_RIGHT)
        self.TempTravelPowerLabel.SetToolTip('Select the temporary travel power to toggle using the keybind')
        self.tempSizer.InnerSizer.Add(self.TempTravelPowerLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)

        temptravelPowerMenu = self.BuildTempTravelPowerMenu()
        temptravelPowerMenu.Bind(wx.EVT_MENU, self.OnTempTravelPowerPicked)

        self.TempTravelPowerPicker = PowerPicker(self.tempSizer.GetStaticBox(), menu = temptravelPowerMenu, size = wx.Size(230, 40))
        self.TempTravelPowerPicker.SetToolTip('Select the temporary travel power to toggle using the keybind')
        self.TempTravelPowerPicker.DefaultToolTip = 'Select the temporary travel power to toggle using the keybind'
        self.Ctrls['TempTravelPowerPicker'] = self.TempTravelPowerPicker
        self.tempSizer.InnerSizer.Add(self.TempTravelPowerPicker, 1, wx.EXPAND)

        self.tempSizer.Layout()
        self.leftColumn.Add(self.tempSizer, 0, wx.EXPAND)

        ##### SUPER SPEED
        self.superSpeedSizer = ControlGroup(self, self, 'Speed')
        self.superSpeedSizer.AddControl(ctlName = "SpeedPower", ctlType = 'choice', contents = [''],
            tooltip = "Select the super speed power to use with the keybinds in this section")
        self.Ctrls['SpeedPower'].Bind(wx.EVT_CHOICE, self.OnSpeedChanged)
        self.superSpeedSizer.AddControl( ctlName = 'SpeedMode', ctlType = 'keybutton',
            tooltip = "Enter Speed on Demand Super Speed Mode")
        self.superSpeedSizer.AddControl( ctlName = 'SpeedSpecialKey', ctlType = 'keybutton',)
        self.superSpeedSizer.AddControl( ctlName = 'SSMobileOnly', ctlType = 'checkbox',
            tooltip = "Activate speed power only when moving;  deactivate when stationary")
        self.superSpeedSizer.AddControl( ctlName = 'SSSJModeEnable', ctlType = 'checkbox',
            tooltip = "Enable Super Speed + Super Jump mode.  Check the Manual for details")
        self.rightColumn.Add(self.superSpeedSizer, 0, wx.EXPAND)

        ##### SUPER JUMP
        self.superJumpSizer = ControlGroup(self, self, 'Jumping')
        self.superJumpSizer.AddControl(ctlName = "JumpPower", ctlType = 'choice', contents = [''],
            tooltip = "Select the jump power to use with the keybinds in this section")
        self.Ctrls['JumpPower'].Bind(wx.EVT_CHOICE, self.OnJumpChanged)
        self.superJumpSizer.AddControl( ctlName = 'HasCJ', ctlType = 'checkbox',
            tooltip = "Should the binds use Combat Jumping as a defense / stationary power?")
        self.Ctrls['HasCJ'].Bind(wx.EVT_CHECKBOX, self.OnJumpChanged)
        self.superJumpSizer.AddControl( ctlName = 'SimpleSJCJ', ctlType = 'checkbox',
            tooltip = "Use the Jump Mode key as a simple Super Jump / Combat Jumping toggle.  This will toggle on and off either power if it is the only one available")
        self.Ctrls['SimpleSJCJ'].Bind(wx.EVT_CHECKBOX, self.OnJumpChanged)
        self.superJumpSizer.AddControl( ctlName = 'JumpMode', ctlType = 'keybutton',
            tooltip = "Enter Speed on Demand Jump Mode")
        self.superJumpSizer.AddControl( ctlName = 'JumpSpecialKey', ctlType = 'keybutton',)
        self.rightColumn.Add(self.superJumpSizer, 0, wx.EXPAND)

        ##### FLY
        self.flySizer = ControlGroup(self, self, 'Flight')
        self.flySizer.AddControl(ctlName = "FlyPower", ctlType = 'choice', contents = [''],
            tooltip = "Select the flight power to use with the keybinds in this section")
        self.Ctrls['FlyPower'].Bind(wx.EVT_CHOICE, self.OnFlightChanged)
        self.flySizer.AddControl( ctlName = 'HasHover', ctlType = 'checkbox',)
        self.Ctrls['HasHover'].Bind(wx.EVT_CHECKBOX, self.OnFlightChanged)
        self.flySizer.AddControl( ctlName = 'FlyMode', ctlType = 'keybutton',
            tooltip = "Enter Speed on Demand Fly Mode")
        self.flySizer.AddControl( ctlName = 'FlySpecialKey', ctlType = 'keybutton',)
        self.flySizer.AddControl( ctlName = 'HasGFly', ctlType = 'checkbox',
            tooltip = "Enable Group Fly-related keybinds")
        self.Ctrls['HasGFly'].Bind(wx.EVT_CHECKBOX, self.OnFlightChanged)
        self.flySizer.AddControl( ctlName = 'GFlyMode', ctlType = 'keybutton',
            tooltip = "Enter Group Fly Speed on Demand Mode")
        self.rightColumn.Add(self.flySizer, 0, wx.EXPAND)

        ##### TELEPORT
        self.teleportSizer = ControlGroup(self, self, 'Teleport')
        self.teleportSizer.AddControl(ctlName = "TPPower", ctlType = 'choice', contents = [''],
            tooltip = "Select the teleport power to use with the keybinds in this section")
        self.Ctrls['TPPower'].Bind(wx.EVT_CHOICE, self.OnTeleportChanged)
        if server == "Homecoming":
            tpTooltip = 'Immediately teleport to the cursor position without showing a target marker.'
            tpcTooltip = 'Show target marker on keypress;  teleport to marker on key release.'
        else:
            tpTooltip = 'Initiate teleport power, showing target marker.'
            tpcTooltip = 'Show target marker on keypress;  click to teleport.'
        self.teleportSizer.AddControl( ctlName = "TPBindKey", ctlType = 'keybutton', tooltip = tpTooltip)
        self.teleportSizer.AddControl( ctlName = "TPComboKey", ctlType = 'keybutton', tooltip = tpcTooltip)
        self.Ctrls['TPComboKey'].Bind(EVT_KEY_CHANGED, self.OnTPComboKey)
        self.teleportSizer.AddControl( ctlName = "TPExecuteKey", ctlType = 'keybutton')
        self.teleportSizer.AddControl( ctlName = 'TPTPHover', ctlType = 'checkbox',
            tooltip = "Activate the Hover power after teleporting")
        self.teleportSizer.AddControl( ctlName = "HasTTP", ctlType = 'checkbox',
            tooltip = "Enable Team Teleport-related keybinds")
        self.Ctrls['HasTTP'].Bind(wx.EVT_CHECKBOX, self.OnTeleportChanged)
        if server == "Homecoming":
            ttpTooltip = "Immediately Team Teleport to the cursor position without showing a target marker."
            ttpcTooltip = "Show target marker on keypress;  Team Teleport to marker on key release."
        else:
            ttpTooltip = "Initiate Team Teleport, showing target marker."
            ttpcTooltip = "Show target marker on keypress;  click to team teleport."
        self.teleportSizer.AddControl( ctlName = "TTPBindKey", ctlType = 'keybutton', tooltip = ttpTooltip)
        self.teleportSizer.AddControl( ctlName = "TTPComboKey", ctlType = 'keybutton', tooltip = ttpcTooltip)
        self.Ctrls['TTPComboKey'].Bind(EVT_KEY_CHANGED, self.OnTTPComboKey)
        self.teleportSizer.AddControl( ctlName = "TTPExecuteKey", ctlType = 'keybutton')
        self.teleportSizer.AddControl( ctlName = 'TTPTPGFly', ctlType = 'checkbox',
            tooltip = "Activate the Group Fly power after Team Teleporting")
        self.teleportSizer.AddControl( ctlName = 'TPHideWindows', ctlType = 'checkbox',
            tooltip = 'Hide most UI elements while holding target marker key.', )
        self.rightColumn.Add(self.teleportSizer, 0, wx.EXPAND)

        topSizer.Add(self.leftColumn, 0, wx.ALL, 3)
        topSizer.Add(self.rightColumn, 0, wx.ALL, 3)

        self.MainSizer.Add(topSizer, flag = wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, border = 16)

    # If we have two items, blank plus one power, pre-set it to the one power
    def PrePickLonePower(self, control):
        if not isinstance(control, wx.Choice): return
        if control.GetCount() == 2: control.SetSelection(1)

    def ShowControlGroup(self, group, show = True):
        if self.rightColumn.GetItem(group):
            self.rightColumn.Show(group, show)
        elif self.leftColumn.GetItem(group):
            self.leftColumn.Show(group, show)
        else:
            wx.LogError(f"Tried to show/hide {group} which is in neither column.  This is a bug.")
        for ctrl in group.GetChildren():
            win = ctrl.GetWindow()
            if win: win.Enable(show)

    def OnTPComboKey(self, evt = None):
        ComboKey = self.GetState('TPComboKey')
        self.Ctrls['TPExecuteKey'].SetLabel(ComboKey + "+BUTTON1")
        if evt: evt.Skip()

    def OnTTPComboKey(self, evt = None):
        ComboKey = self.GetState('TTPComboKey')
        self.Ctrls['TTPExecuteKey'].SetLabel(ComboKey + "+BUTTON1")
        if evt: evt.Skip()

    def OnDetailsCameraChanged(self, evt = None):
        c = self.Ctrls
        c['CamdistBase'].Enable(self.GetState('ChangeCamera'))
        c['CamdistMove'].Enable(self.GetState('ChangeCamera'))

        c['DetailBase'].Enable(self.GetState('ChangeDetail'))
        c['DetailMove'].Enable(self.GetState('ChangeDetail'))
        if evt: evt.Skip()

    def OnSpeedOnDemandChanged(self, evt = None):
        c = self.Ctrls
        for ctrl in ['DefaultMode', 'SprintPower', 'NonSoDEnable', 'SprintSoD', 'MouseChord', 'Feedback']:
            c[ctrl].Enable(self.GetState('EnableSoD'))
        c['NonSoDMode'].Enable(self.GetState('EnableSoD') and self.GetState('NonSoDEnable'))
        c['SprintMode'].Enable(self.GetState('EnableSoD') and self.GetState('SprintSoD') and self.DefaultMode() != "Sprint")
        if evt: evt.Skip()

    def OnFlightChanged(self, evt = None):
        c = self.Ctrls
        archetype = self.Profile.Archetype()

        if (self.Profile.HasPowerPool('Flight')
                    or self.Profile.HasPowerPool('Sorcery')
                    or archetype == "Peacebringer"):
            self.ShowControlGroup(self.flySizer)
            c['FlyPower'].ShowEntryIf("Fly",           self.Profile.HasPowerPool("Flight"))
            c['FlyPower'].ShowEntryIf("Mystic Flight", self.Profile.HasPowerPool("Sorcery"))
            c['FlyPower'].ShowEntryIf("Energy Flight", archetype == "Peacebringer")
            self.PrePickLonePower(c['FlyPower'])

            c['FlyMode'].Enable(bool(self.GetState('FlyPower') or self.GetState('HoverPower'))
                                          and self.DefaultMode() != "Fly")
            c['HasHover'].Show(self.Profile.HasPowerPool('Flight') or archetype == "Peacebringer")
            if archetype == 'Peacebringer':
                c['HasHover'].CtlLabel.SetLabel('Has Combat Flight:')
                c['HasHover'].SetToolTip('Use Combat Flight as a defense / stationary power -- if your Peacebringer is below level 10, leave this unchecked')
                c['HoverPower'].SetValue('Combat Flight')
            else:
                c['HasHover'].CtlLabel.SetLabel('Has Hover:')
                c['HasHover'].SetToolTip('Use Hover as a defense / stationary power')
                c['HoverPower'].SetValue('Hover')

            try: # try/except here because we Freeze to prevent flicker and what if it breaks?
                self.Freeze()
                c['FlySpecialKey'].Show(False)
                if (self.GetState('FlyPower') == "Fly"):
                    c['FlySpecialKey'].CtlLabel.SetLabel('Afterburner:')
                    c['FlySpecialPower'].SetValue('fly_boost') # "afterburner" has overloaded meaning.
                    c['FlySpecialKey'].Show()

                if (archetype == "Peacebringer" and ((self.GetState('FlyPower') == 'Energy Flight') or self.GetState('HasHover'))):
                    c['FlySpecialKey'].CtlLabel.SetLabel('Quantum Maneuvers:')
                    c['FlySpecialPower'].SetValue('Quantum Maneuvers')
                    c['FlySpecialKey'].Show()
            except Exception:
                pass
            finally:
                self.Thaw()

            c['HasGFly'].Enable(self.Profile.HasPowerPool('Flight'))
            c['GFlyMode'].Enable(self.hasGFly())
        else:
            self.ShowControlGroup(self.flySizer, False)
        if evt: evt.Skip()

    def OnJumpChanged(self, evt = None):
        c = self.Ctrls
        if (self.Profile.HasPowerPool('Leaping') or self.Profile.HasPowerPool('Force of Will')):
            self.ShowControlGroup(self.superJumpSizer)
            c['JumpPower'].ShowEntryIf('Mighty Leap', self.Profile.HasPowerPool('Force of Will'))
            c['JumpPower'].ShowEntryIf('Super Jump',  self.Profile.HasPowerPool('Leaping'))
            self.PrePickLonePower(c['JumpPower'])

            c['JumpMode']  .Enable(bool(
                    self.DefaultMode() != "Jump"
                        and
                    (self.GetState('JumpPower') or self.GetState('HasCJ') or self.GetState('SimpleSJCJ'))
                ))
            c['HasCJ'].Enable(self.Profile.HasPowerPool('Leaping'))
            c['SimpleSJCJ'].Enable(bool(self.GetState('JumpPower') or self.GetState('HasCJ')))
            c['SSSJModeEnable'].Show(bool(self.GetState('SpeedPower') and self.rightColumn.IsShown(self.superJumpSizer)))

            if (self.GetState('JumpPower') == "Mighty Leap"):
                c['JumpSpecialKey'].CtlLabel.SetLabel('Takeoff:')
                c['JumpSpecialPower'].SetValue('Takeoff')
                c['JumpSpecialKey'].Show()
            elif (self.GetState('JumpPower') == "Super Jump"):
                c['JumpSpecialKey'].CtlLabel.SetLabel('Double Jump:')
                c['JumpSpecialPower'].SetValue('Double_Jump')
                c['JumpSpecialKey'].Show()
            else:
                c['JumpSpecialKey'].Show(False)
        else:
            self.ShowControlGroup(self.superJumpSizer, False)
        if evt: evt.Skip()

    def OnSpeedChanged(self, evt = None):
        c = self.Ctrls
        if (self.Profile.HasPowerPool('Speed') or self.Profile.HasPowerPool('Experimentation')):
            self.ShowControlGroup(self.superSpeedSizer)
            c['SpeedPower'].ShowEntryIf('Speed of Sound', self.Profile.HasPowerPool('Experimentation'))
            c['SpeedPower'].ShowEntryIf('Super Speed',    self.Profile.HasPowerPool('Speed'))
            self.PrePickLonePower(c['SpeedPower'])
            c['SpeedMode'].Enable(bool(self.GetState('SpeedPower')) and self.DefaultMode() != "Speed")
            c['SSMobileOnly'].Enable(bool(self.GetState('SpeedPower')))
            c['SSSJModeEnable'].Show(bool(self.GetState('SpeedPower') and self.rightColumn.IsShown(self.superJumpSizer)))

            if (self.GetState('SpeedPower') == "Super Speed"):
                c['SpeedSpecialKey'].CtlLabel.SetLabel('Speed Phase:')
                c['SpeedSpecialPower'].SetValue('SpeedPhase')
                c['SpeedSpecialKey'].Show()
            else:
                c['SpeedSpecialKey'].Show(False)
        else:
            self.ShowControlGroup(self.superSpeedSizer, False)
        if evt: evt.Skip()

    def OnTeleportChanged(self, evt = None):
        c = self.Ctrls
        archetype = self.Profile.Archetype()

        if (self.Profile.HasPowerPool('Teleportation')
                    or self.Profile.HasPowerPool('Sorcery')
                    or self.Profile.HasPowerPool('Experimentation')
                    or archetype == "Warshade"):
            self.ShowControlGroup(self.teleportSizer)
            c['TPPower'].ShowEntryIf('Teleport',      self.Profile.HasPowerPool('Teleportation'))
            c['TPPower'].ShowEntryIf('Translocation', self.Profile.HasPowerPool('Sorcery'))
            c['TPPower'].ShowEntryIf('Jaunt',         self.Profile.HasPowerPool('Experimentation')
                                                        and self.GetState('SpeedPower') == "Speed of Sound")
            c['TPPower'].ShowEntryIf('Shadow Step',   archetype == "Warshade")
            self.PrePickLonePower(c['TPPower'])
            c['TPBindKey'].Enable(self.GetState('TPPower') != '')
            c['TPComboKey'].Enable(self.GetState('TPPower') != '')
            c['TPTPHover'].Show((self.GetState('TPPower') != '') and self.hasHover())
            c['HasTTP']     .Show(self.Profile.HasPowerPool('Teleportation'))
            c['TTPBindKey'] .Show(c['HasTTP'].IsShown() and self.GetState('HasTTP'))
            c['TTPComboKey'].Show(c['HasTTP'].IsShown() and self.GetState('HasTTP'))
            c['TTPTPGFly']  .Show(c['HasTTP'].IsShown() and self.GetState('HasTTP') and self.hasGFly())

            # The two 'execute' keys are always hidden as they are magical.
            # They are only for the complicated Rebirth Combo Teleport scheme and might
            # be able to be completely hidden behind "if server" logic eventually.
            c['TPExecuteKey'].Show(False)
            c['TTPExecuteKey'].Show(False)
        else:
            self.ShowControlGroup(self.teleportSizer, False)
        if evt: evt.Skip()

    def OnKheldianChanged(self, evt = None):
        c = self.Ctrls
        if (self.isKheldian()):
            # show kheldian sizer, enable controls
            self.ShowControlGroup(self.kheldianSizer)

            c['NovaMode'].Enable(self.GetState('UseNova'))
            c['NovaTray'].Enable(self.GetState('UseNova'))
            c['DwarfMode'].Enable(self.GetState('UseDwarf'))
            c['DwarfTray'].Enable(self.GetState('UseDwarf'))
        else:
            self.ShowControlGroup(self.kheldianSizer, False)
        if evt: evt.Skip()

    def OnTempChanged(self, evt = None):
        tt = self.Ctrls['TempToggle']
        enabled = bool(self.GetState('TempEnable'))

        tt.Enable(enabled)
        self.TempTravelPowerLabel.Enable(enabled)
        self.TempTravelPowerPicker.Enable(enabled)
        self.TempTravelPowerPicker.OnMenuSelection()
        if enabled and not tt.GetLabel():
            tt.AddError('unset', 'No Temp Travel Power BindKey has been set.')
        else:
            tt.RemoveError('unset')

        if evt: evt.Skip()

    def OnTempTravelPowerPicked(self, evt):
        menu = evt.GetEventObject()
        menuitem = menu.FindItemById(evt.GetId())
        label = menuitem.GetItemLabel()
        bitmap = menuitem.GetBitmapBundle()
        self.TempTravelPowerPicker.SetLabel(label)
        self.TempTravelPowerPicker.SetBitmap(bitmap)
        setattr(self.TempTravelPowerPicker, 'IconFilename', getattr(menuitem, 'IconFilename'))

    def BuildTempTravelPowerMenu(self):
        menu = wx.Menu()
        for item in GameData.TempTravelPowers:
            if re.search(r'\|', item):
                item, iconname = re.split(r'\|', item)
            else:
                iconname = item
            menuitem = wx.MenuItem(id = wx.ID_ANY, text = item)
            icon = GetIcon('Powers', 'Temp', iconname)
            if icon:
                menuitem.SetBitmap(icon)
                setattr(menuitem, 'IconFilename', icon.Filename)
            menu.Append(menuitem)
        return menu

    def SynchronizeUI(self, evt = None):
        self.Freeze()

        try:
            self.OnDetailsCameraChanged()

            self.OnKheldianChanged()

            self.OnSpeedOnDemandChanged()

            self.OnFlightChanged()

            self.OnJumpChanged()

            self.OnSpeedChanged()

            self.OnTeleportChanged()

            self.OnTempChanged()

        except Exception as e:
            print(f"Something blowed up in SoD SynchronizeUI:  {e}")
            raise e

        finally:
            self.Layout()
            self.Thaw()
            if evt: evt.Skip()

    def makeSoDFile(self, p):

        profile = self.Profile

        t = p['t']

        bl   = p.get('bl'   , t.bl)
        bla  = p.get('bla'  , t.bla)
        blf  = p.get('blf'  , t.blf)
        blbo = p.get('blbo' , t.blbo)

        path      = p.get('path'      , t.path)
        gamepath  = p.get('gamepath'  , t.gamepath)
        patha     = p.get('patha'     , t.patha)
        gamepatha = p.get('gamepatha' , t.gamepatha)
        pathf     = p.get('pathf'     , t.pathf)
        gamepathf = p.get('gamepathf' , t.gamepathf)
        pathbo    = p.get('pathbo'    , t.pathbo)

        mobile     = p.get('mobile'     , None)
        stationary = p.get('stationary' , None)
        modestr    = p.get('modestr'    , "")
        flight     = p.get('flight'     , "")
        fix        = p.get('fix'        , "")
        turnoff    = p.get('turnoff'    , [ mobile, stationary ])
        sssj       = p.get('sssj'       , "")

        if ((self.DefaultMode() == modestr) and (t.totalkeys == 0)):

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
            if (modestr != "GFly")        : self.makeGFlyModeKey  (profile,t,"gf",curfile,turnoff,fix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"s", curfile,turnoff,fix)
            if (modestr != "Jump")        : self.makeJumpModeKey  (profile,t,"j", curfile,turnoff,path, gamepath)

            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)

            self.sodFollowKey(t,blf,curfile,mobile,stationary)

        if (flight and (flight == self.GetState('FlyPower')) and pathbo):
            #  blast off
            curfile = profile.GetBindFile(f"{pathbo}{t.KeyState()}.txt")
            self.sodResetKey(curfile,gamepath,self.actPower_toggle(stationary,mobile,True))
            self.sodUpKey     (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodDownKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo")
            self.sodForwardKey(t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodBackKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodLeftKey   (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)
            self.sodRightKey  (t,blbo,curfile,mobile,stationary,flight,'','',"bo",sssj)

            if (modestr == "Sprint") : self.makeSprintModeKey(profile,t,"r",curfile,turnoff,fix)

            t.ini = '-down$$'

            if (self.DefaultMode() == "Fly") :
                if (self.GetState('NonSoDEnable'))     : t.FlyMode = t.NonSoDMode
                if (self.GetState('SprintSoD'))        : t.FlyMode = t.SprintMode
                if (self.GetState('SpeedPower'))       : t.FlyMode = t.SpeedMode
                if (t.canjmp)                          : t.FlyMode = t.JumpMode
            self.makeFlyModeKey(profile,t,"a",curfile,turnoff,fix)

            t.ini = ''
            if (modestr != "GFly")        : self.makeGFlyModeKey (profile,t,"gbo",curfile,turnoff,fix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey(profile,t,"s",  curfile,turnoff,fix)
            if (modestr != "Jump")        : self.makeJumpModeKey (profile,t,"j",  curfile,turnoff,path,gamepath)

            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)

            self.sodFollowKey(t,blf,curfile,mobile,stationary)

        curfile = profile.GetBindFile(f"{path}{t.KeyState()}.txt")

        self.sodResetKey(curfile,gamepath,self.actPower_toggle(stationary,mobile,True))

        self.sodUpKey     (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodDownKey   (t,bl,curfile,mobile,stationary,flight,'','','')
        self.sodForwardKey(t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodBackKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodLeftKey   (t,bl,curfile,mobile,stationary,flight,'','','',sssj)
        self.sodRightKey  (t,bl,curfile,mobile,stationary,flight,'','','',sssj)

        if ((flight == "Fly" or flight == "Mystic Flight") and pathbo):
            #  Base to set down
            if (modestr != "NonSoD") : self.makeNonSoDModeKey(profile,t,"r",curfile,[ mobile,stationary ],self.sodSetDownFix)
            if (modestr != "Sprint") : self.makeSprintModeKey(profile,t,"r",curfile,turnoff,self.sodSetDownFix)

            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"s", curfile,turnoff,self.sodSetDownFix)
            if (modestr != "Fly")         : self.makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)
            if (modestr != "Jump")        : self.makeJumpModeKey  (profile,t,"j", curfile,turnoff,path,gamepath)
        else:
            if (modestr != "NonSoD")      : self.makeNonSoDModeKey(profile,t,"r", curfile,[ mobile,stationary ])
            if (modestr != "Sprint")      : self.makeSprintModeKey(profile,t,"r", curfile,turnoff,fix)
            if (flight == "Jump"):
                if (modestr != "Fly")     : self.makeFlyModeKey   (profile,t,"a", curfile,turnoff,fix,'',True)
            else:
                if (modestr != "Fly")     : self.makeFlyModeKey   (profile,t,"bo",curfile,turnoff,fix)

            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"s", curfile,turnoff,fix)
            if (modestr != "Jump")        : self.makeJumpModeKey  (profile,t,"j", curfile,turnoff,path,gamepath)

        self.sodAutoRunKey(t,bla,curfile,mobile,sssj)
        self.sodFollowKey(t,blf,curfile,mobile,stationary)

        # AutoRun Binds
        curfile = profile.GetBindFile(f"{patha}{t.KeyState()}.txt")

        self.sodResetKey(curfile,gamepath,self.actPower_toggle(stationary,mobile,True))

        self.sodUpKey     (t,bla,curfile,mobile,stationary,flight,1, '','',sssj)
        self.sodDownKey   (t,bla,curfile,mobile,stationary,flight,1, '','')
        self.sodForwardKey(t,bla,curfile,mobile,stationary,flight,bl,'','',sssj)
        self.sodBackKey   (t,bla,curfile,mobile,stationary,flight,bl,'','',sssj)
        self.sodLeftKey   (t,bla,curfile,mobile,stationary,flight,1, '','',sssj)
        self.sodRightKey  (t,bla,curfile,mobile,stationary,flight,1, '','',sssj)

        if ((flight == "Fly" or flight == "Mystic Flight") and pathbo):
            if (modestr != "NonSoD")      : self.makeNonSoDModeKey(profile,t,"ar",curfile,[ mobile,stationary ],self.sodSetDownFix)
            if (modestr != "Sprint")      : self.makeSprintModeKey(profile,t,"gr",curfile,turnoff,self.sodSetDownFix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"as",curfile,turnoff,self.sodSetDownFix)
        else:
            if (modestr != "NonSoD")      : self.makeNonSoDModeKey(profile,t,"ar",curfile,[ mobile,stationary ])
            if (modestr != "Sprint")      : self.makeSprintModeKey(profile,t,"gr",curfile,turnoff,fix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"as",curfile,turnoff,fix)

        if (modestr != "Fly")       : self.makeFlyModeKey (profile,t,"af",curfile,turnoff,fix)
        if (modestr != "Jump")      : self.makeJumpModeKey(profile,t,"aj",curfile,turnoff,patha,gamepatha)

        self.sodAutoRunOffKey(t,bl,curfile,mobile,stationary,flight)

        curfile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind('nop'))

        # FollowRun Binds
        curfile = profile.GetBindFile(f"{pathf}{t.KeyState()}.txt")

        self.sodResetKey(curfile,gamepath,self.actPower_toggle(stationary,mobile,True))

        self.sodUpKey     (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodDownKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'')
        self.sodForwardKey(t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodBackKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodLeftKey   (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)
        self.sodRightKey  (t,blf,curfile,mobile,stationary,flight,'',bl,'',sssj)

        if ((flight == "Fly" or flight == "Mystic Flight") and pathbo):
            if (modestr != "NonSoD")      : self.makeNonSoDModeKey(profile,t,"fr",curfile,[ mobile,stationary ],self.sodSetDownFix)
            if (modestr != "Sprint")      : self.makeSprintModeKey(profile,t,"fr",curfile,turnoff,self.sodSetDownFix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"fs",curfile,turnoff,self.sodSetDownFix)
        else:
            if (modestr != "NonSoD")      : self.makeNonSoDModeKey(profile,t,"fr",curfile,[ mobile,stationary ])
            if (modestr != "Sprint")      : self.makeSprintModeKey(profile,t,"fr",curfile,turnoff,fix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey (profile,t,"fs",curfile,turnoff,fix)

        if (modestr != "Fly")       : self.makeFlyModeKey (profile,t,"ff",curfile,turnoff,fix)
        if (modestr != "Jump")      : self.makeJumpModeKey(profile,t,"fj",curfile,turnoff, pathf, gamepathf)

        curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind('nop'))

        self.sodFollowOffKey(t,bl,curfile,mobile,stationary,flight)

    def makeNonSoDModeKey(self, p, t, bl, cur, toff, fix = None, fb = ''):
        key = t.NonSoDMode
        name = UI.Labels['NonSoDMode']
        if not self.Ctrls['NonSoDMode'].IsEnabled(): return
        if not key: return

        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Non-SoD Mode'
        else:                                      feedback = ''

        if (bl == "r"):
            bindload = t.BLF('n')
            if (fix):
                fix(p,t,key, self.makeNonSoDModeKey,"n",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, name, self, t.ini + self.actPower_toggle(None,toff) + t.dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload = t.BLF('an')
            if (fix):
                fix(p,t,key, self.makeNonSoDModeKey,"n",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, name, self, t.ini + self.actPower_toggle(None,toff) + t.detailhi + t.runcamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, self.makeNonSoDModeKey,"n",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, name, self, t.ini + self.actPower_toggle(None,toff) + t.detailhi + t.runcamdist + '$$up 0' + feedback + t.BLF('fn'))
        t.ini = ''

    def makeSprintModeKey(self, p, t, bl, cur, toff, fix, fb = ''):
        key = t.SprintMode
        name = UI.Labels['SprintMode']
        if not key: return

        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Sprint-SoD Mode'
        else:                                      feedback = ''

        if (bl == "r"):
            bindload  = t.BLF('R')

            if t.horizkeys: sprint = t.sprint
            else:           sprint = ''
            ton = self.actPower_toggle(sprint, toff, start = True)

            if (fix):
                fix(p,t,key, self.makeSprintModeKey,"r",bl,cur,toff,'',feedback)
            else:
                cur.SetBind(key, name, self, t.ini + ton + t.dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t.BLF('gr')

            if (fix):
                fix(p,t,key, self.makeSprintModeKey,"r",bl,cur,toff,"a",feedback)
            else:
                cur.SetBind(key, name, self, t.ini + self.actPower_toggle(t.sprint,toff,start=True) + t.detailhi +  t.runcamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if (fix):
                fix(p,t,key, self.makeSprintModeKey,"r",bl,cur,toff,"f",feedback)
            else:
                cur.SetBind(key, name, self, t.ini + self.actPower_toggle(t.sprint,toff,start=True) + t.detailhi + t.runcamdist + '$$up 0' + feedback + t.BLF('fr'))

        t.ini = ''

    def makeSpeedModeKey(self, p, t, bl, cur, toff, fix, fb = ''):
        key = t.SpeedMode
        name = UI.Labels['SpeedMode']
        if not self.Ctrls['SpeedMode'].IsEnabled(): return
        bindload = feedback = ''

        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Superspeed Mode'

        if (self.GetState('SpeedPower')):
            if (bl == 's'):
                bindload = f"{t.bls}{t.KeyState()}.txt"
                if (fix):
                    fix(p,t,key,self.makeSpeedModeKey,"s",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(key, name, self, t.ini + self.actPower_toggle(t.speed,toff,start=True) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "as"):
                bindload = f"{t.blas}{t.KeyState()}.txt"
                if (fix):
                    fix(p,t,key,self.makeSpeedModeKey,"s",bl,cur,toff,"a",feedback)
                elif (not feedback):
                    cur.SetBind(key, name, self, t.ini + self.actPower_toggle(t.speed,toff,start=True) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload)
                else:
                    bindload  = f"{t.blas}{t.KeyState()}.txt"
                    bindload2 = f"{t.blas}{t.KeyState()}_s.txt"
                    tgl = p.GetBindFile(f"{t.pathas}{t.KeyState()}_s.txt")
                    cur.SetBind(key, name, self, "+ $$" + t.ini + self.actPower_toggle(t.speed,toff,start=True) + t.dirs('UDLR') + t.detaillo + t.flycamdist + bindload2)
                    tgl.SetBind(key, name, self, "- $$" + feedback + bindload)

            else:
                if (fix):
                    fix(p,t,key,self.makeSpeedModeKey,"s",bl,cur,toff,"f",feedback)
                else:
                    bindload = f"{t.blfs}{t.KeyState()}.txt"
                    cur.SetBind(key, name, self, t.ini + self.actPower_toggle(t.speed,toff,start=True) + '$$up 0' +  t.detaillo + t.flycamdist + feedback + bindload)

        t.ini = ''

    def makeJumpModeKey(self, p, t, bl, cur, toff, fpath, fbl):
        key = t.JumpMode
        name = UI.Labels['JumpMode']
        if not self.Ctrls['JumpMode'].IsEnabled(): return
        if (t.canjmp and not self.GetState('SimpleSJCJ')):

            if self.GetState('Feedback'): feedback = '$$t $name, Superjump Mode'
            else:                         feedback = ''

            tglbl =   f"{fbl}{t.KeyState()}j.txt"
            tglfn = f"{fpath}{t.KeyState()}j.txt"
            tgl = p.GetBindFile(tglfn)

            if (bl == "j"):
                if (t.horizkeys + t.space > 0):
                    a = self.actPower_name(t.jump,toff) + '$$up 1'
                else:
                    a = self.actPower_name(t.cjmp,toff)

                tgl.SetBind(key, name, self, '-down' + a + t.detaillo + t.flycamdist + t.blj + t.KeyState() + ".txt")
                cur.SetBind(key, name, self, '+down' + feedback + f'$${BLF()} ' + tglbl)
            elif (bl == "aj"):
                tgl.SetBind(key, name, self, '-down' + self.actPower_name(t.jump,toff) + '$$up 1' + t.detaillo + t.flycamdist + t.dirs('DLR') + t.blaj + t.KeyState() + ".txt")
                cur.SetBind(key, name, self, '+down' + feedback + f'$${BLF()} ' + tglbl)
            else:
                tgl.SetBind(key, name, self, '-down' + self.actPower_name(t.jump,toff) + '$$up 1' + t.detaillo + t.flycamdist + t.blfj + t.KeyState() + ".txt")
                cur.SetBind(key, name, self, '+down' + feedback + f'$${BLF()} ' + tglbl)

        t.ini = ''

    def makeFlyModeKey(self, p, t, bl, cur, toff, fix, fb = '', fb_on_a = False):
        key = t.FlyMode
        name = UI.Labels['FlyMode']
        if not self.Ctrls['FlyMode'].IsEnabled(): return
        if not key: return

        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Flight Mode'
        else:                                      feedback = ''

        if (t.canhov or t.canfly):
            if (bl == "bo"):
                bindload = t.blbo + t.KeyState() + ".txt"
                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(key, name, self, '+down$$' + self.actPower_toggle(t.flyx,toff,start=True) + '$$up 1$$down 0' + t.dirs('FBLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "a"):
                if (not fb_on_a): feedback = ''
                bindload = t.bla + t.KeyState() + ".txt"

                if t.totalkeys: ton = t.flyx
                else:           ton = t.hover

                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,'',feedback)
                else:
                    cur.SetBind(t.FlyMode, name, self, t.ini + self.actPower_toggle(ton,toff,start=True) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "af"):
                bindload = t.blaf + t.KeyState() + ".txt"
                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,"a",feedback)
                else:
                    cur.SetBind(key, name, self, t.ini + self.actPower_toggle(t.flyx,toff,start=True) + t.detaillo + t.flycamdist + t.dirs('DLR') + feedback + bindload)

            else:
                bindload = t.blff + t.KeyState() + ".txt"
                if (fix):
                    fix(p,t,key,self.makeFlyModeKey,"f",bl,cur,toff,"f",feedback)
                else:
                    cur.SetBind(key, name, self, t.ini + self.actPower_toggle(t.flyx,toff,start=True) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + t.blff + t.KeyState() + ".txt")

        t.ini = ''

    def makeGFlyModeKey(self, p, t, bl, cur, toff, fix):
        key = t.GFlyMode
        name = UI.Labels['GFlyMode']
        if not self.Ctrls['GFlyMode'].IsEnabled(): return

        if t.cangfly:
            if (bl == "gbo"):
                bindload = t.BLF('gbo')
                if (fix):
                    fix(p,t,key,self.makeGFlyModeKey,"gf",bl,cur,toff,'','')
                else:
                    cur.SetBind(key, name, self, t.ini + '$$up 1$$down 0' + self.actPower_toggle(t.gfly,toff) + t.dirs('FBLR') + t.detaillo + t.flycamdist + bindload)

            elif (bl == "gaf"):
                bindload = t.BLF('gaf')
                if (fix):
                    fix(p,t,key,self.makeGFlyModeKey,"gf",bl,cur,toff,"a")
                else:
                    cur.SetBind(key, name, self, t.ini + t.detaillo + t.flycamdist + t.dirs('UDLR') + bindload)

            else:
                if (fix):
                    fix(p,t,key,self.makeGFlyModeKey,"gf",bl,cur,toff,"f")
                else:
                    if (bl == "gf"):
                        cur.SetBind(key, name, self, t.ini + self.actPower_toggle(t.gfly,toff,start=True) + t.detaillo + t.flycamdist + t.BLF('gff'))
                    else:
                        cur.SetBind(key, name, self, t.ini + t.detaillo + t.flycamdist + t.BLF('gff'))

        t.ini = ''

    def PopulateBindFiles(self):
        profile   = self.Profile
        ResetFile = profile.ResetFile()
        server = self.Profile.Server
        tpActivator = "powexeclocation cursor " if server == 'Homecoming' else "powexecname "

        # set up the "t" object that drives approximately everything
        t = tObject(profile)

        if (self.GetState('PlayerTurn')):
            t.playerturn = 'playerturn'

        if (self.GetState('AutoMouseLook')):
            t.mouselookon  = '$$mouselook 1'
            t.mouselookoff = '$$mouselook 0'

        if (self.GetState('ChangeCamera')):
            t.runcamdist = f"$$camdist {self.GetState('CamdistBase')}"
            t.flycamdist = f"$$camdist {self.GetState('CamdistMove')}"

        if (self.GetState('ChangeDetail')):
            t.detailhi = f"$$visscale {self.GetState('DetailBase')}$$shadowvol 0$$ss 0"
            t.detaillo = f"$$visscale {self.GetState('DetailMove')}$$shadowvol 0$$ss 0"

        ## Combat Jumping / Super Jump
        if (self.GetState('HasCJ') and not self.GetState('JumpPower')):
            t.cancj = True
            t.cjmp  = "Combat Jumping"
            t.jump  = "Combat Jumping"

        elif (not self.GetState('HasCJ') and self.GetState('JumpPower')):
            t.canjmp     = True
            t.jump       = self.GetState('JumpPower')
            t.jumpifnocj = self.GetState('JumpPower')

        elif self.GetState('HasCJ') and self.GetState('JumpPower'):
            t.cancj  = True
            t.canjmp = True
            t.cjmp   = "Combat Jumping"
            t.jump   = self.GetState('JumpPower')

        # Temp Travel Power Toggle
        if (self.GetState('TempEnable')):
            if temppower := self.TempTravelPowerPicker.HasPowerPicked():
                ResetFile.SetBind(self.Ctrls['TempToggle'].MakeFileKeyBind(f'powexecname {temppower}'))

        ## Flying / hover
        t.hover  = self.GetState('HoverPower')
        t.flyx   = self.GetState('FlyPower')

        if (profile.Archetype() == "Peacebringer"):
            t.canfly = True

        # hover, no fly
        if (self.hasHover() and not self.GetState('FlyPower')):
            t.canhov = True
            t.flyx   = self.GetState('HoverPower')
            if (self.GetState('TPTPHover')): t.tphover = f'$${self.togon} {self.GetState("HoverPower")}'
        # fly, no hover
        elif (not self.hasHover() and bool(self.GetState('FlyPower'))):
            t.canfly = True
            t.hover  = self.GetState('FlyPower')
        # hover and fly
        elif (self.hasHover() and self.GetState('FlyPower')):
            t.canhov = True
            t.canfly = True
            t.fly    = self.GetState('FlyPower')
            if (self.GetState('TPTPHover')): t.tphover = f'$${self.togon} {self.GetState("HoverPower")}'

        if ((profile.Archetype() == "Peacebringer") and self.GetState('FlyQFly')):
            t.canqfly = True

        if (self.GetState('HasGFly')):
            t.cangfly = True
            t.gfly    = "Group Fly"
            if (self.GetState('TTPTPGFly')): t.ttpgfly = f'$${self.togon} Group Fly'

        if (self.GetState('SpeedPower')):
            t.sprint = self.GetState('SprintPower')
            t.speed  = self.GetState('SpeedPower')
        else:
            t.sprint = self.GetState('SprintPower')
            t.speed  = self.GetState('SprintPower')

        if self.GetState('TPHideWindows'):
            windowhide = '$$windowhide health$$windowhide chat$$windowhide target$$windowhide tray$$windowhide nav'
            windowshow = '$$show health$$show chat$$show target$$show tray$$show nav'
        else:
            windowhide = ''
            windowshow = ''

        ###
        ### Here's where we go into the giant SoD tangle, conditionally
        ###
        if self.GetState('EnableSoD') or self.GetState('AutoMouseLook'):
            self.doSpeedOnDemandBinds(t)
        else:
            # bind normal movement keys if SoD not enabled or no mouselook

            if (self.GetState('Left')):
                ResetFile.SetBind(self.Ctrls['Left'].MakeFileKeyBind(["+left"]))
            if (self.GetState('Right')):
                ResetFile.SetBind(self.Ctrls['Right'].MakeFileKeyBind(["+right"]))
            if (self.GetState('Up')):
                ResetFile.SetBind(self.Ctrls['Up'].MakeFileKeyBind(["+up"]))
            if (self.GetState('Down')):
                ResetFile.SetBind(self.Ctrls['Down'].MakeFileKeyBind(["+down"]))
            if (self.GetState('Forward')):
                turn = 'playerturn' if self.GetState('PlayerTurn') else ''
                ResetFile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind(["+forward", turn]))
            if (self.GetState('Back')):
                ResetFile.SetBind(self.Ctrls['Back'].MakeFileKeyBind(["+backward"]))
            if (self.GetState('Follow')):
                ResetFile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind(["+follow"]))
            if (self.GetState('AutoRun')):
                ResetFile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind(["++autorun"]))

        # Bind the turn keys in either case
        if (self.GetState('TurnLeft')):
            ResetFile.SetBind(self.Ctrls['TurnLeft'].MakeFileKeyBind("+turnleft"))
        if (self.GetState('TurnRight')):
            ResetFile.SetBind(self.Ctrls['TurnRight'].MakeFileKeyBind("+turnright"))


        # Make binds for the "stage 2" travel powers like Afterburner, if appropriate
        if self.Ctrls['FlySpecialKey'].IsEnabled():
            ResetFile.SetBind(self.Ctrls['FlySpecialKey'].MakeFileKeyBind(f'powexecname {self.GetState("FlySpecialPower")}'))
        if self.Ctrls['SpeedSpecialKey'].IsEnabled():
            ResetFile.SetBind(self.Ctrls['SpeedSpecialKey'].MakeFileKeyBind(f'powexecname {self.GetState("SpeedSpecialPower")}'))
        if self.Ctrls['JumpSpecialKey'].IsEnabled():
            ResetFile.SetBind(self.Ctrls['JumpSpecialKey'].MakeFileKeyBind(f'powexecname {self.GetState("JumpSpecialPower")}'))

        ###### Kheldian power setup
        #  create the Nova and Dwarf form support files if enabled.
        archetype = profile.Archetype()

        Nova = Dwarf = HumanFormShield = ''
        if (archetype == "Peacebringer"):
            Nova = "Bright Nova"
            Dwarf = "White Dwarf"
            HumanFormShield = "Shining Shield"

        elif (archetype == "Warshade"):
            Nova = "Dark Nova"
            Dwarf = "Black Dwarf"
            HumanFormShield = "Gravity Shield"

        dwarfTPPower = normalTPPower = teamTPPower = ''

        if (archetype == "Warshade"):
            dwarfTPPower  = "Black Dwarf Step"
            normalTPPower = "Shadow Step"
        elif (archetype == "Peacebringer"):
            dwarfTPPower = "White Dwarf Step"
        else:
            normalTPPower = self.GetState('TPPower')
            teamTPPower   = "Team Teleport"

        fullstop = '$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'

        if (self.isKheldian() and self.GetState('UseNova')):
            ResetFile.SetBind(self.Ctrls['NovaMode'].MakeFileKeyBind(f"t $name, Changing to {Nova} Form{fullstop}{t.on}{Nova}$$gototray {self.GetState('NovaTray')}" + profile.BLF('nova.txt')))

            novafile = profile.GetBindFile("nova.txt")

            if (self.GetState('UseDwarf')):
                novafile.SetBind(self.Ctrls['DwarfMode'].MakeFileKeyBind(f"t $name, Changing to {Dwarf} Form{fullstop}{t.off}{Nova}{t.on}{Dwarf}$$gototray {self.GetState('DwarfTray')}" + profile.BLF('dwarf.txt')))

            humpower = ''
            # TODO this control went missing
            #if self.GetState('UseHumanFormPower'): humpower = f'$${self.togon} ' + HumanFormShield
            #else:                                  humpower = ''
            novafile.SetBind(self.Ctrls['NovaMode'].MakeFileKeyBind(f"t $name, Changing to Human Form, SoD Mode{fullstop}$${self.togoff} {Nova}{humpower}$$gototray 1" + profile.BLF('reset.txt')))

            novafile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind("+forward"))
            novafile.SetBind(self.Ctrls['Left'].MakeFileKeyBind("+left"))
            novafile.SetBind(self.Ctrls['Right'].MakeFileKeyBind("+right"))
            novafile.SetBind(self.Ctrls['Back'].MakeFileKeyBind("+backward"))
            novafile.SetBind(self.Ctrls['Up'].MakeFileKeyBind("+up"))
            novafile.SetBind(self.Ctrls['Down'].MakeFileKeyBind("+down"))
            novafile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind("++forward"))
            novafile.SetBind(self.Ctrls['FlyMode'].MakeFileKeyBind('nop'))
            if (self.GetState('FlyMode') != self.GetState('SpeedMode')):
                novafile.SetBind(self.Ctrls['SpeedMode'].MakeFileKeyBind('nop'))
            if (self.GetState('MouseChord')):
                novafile.SetBind('mousechord', 'Nova Form Mousechord', self, ['+down', '+forward', t.playerturn])

            # no teleport while nova
            novafile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('nop'))
            novafile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('nop'))
            if server == 'Rebirth':
                novafile.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('nop'))

            novafile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind("follow"))

        if (self.isKheldian() and self.GetState('UseDwarf')):
            ResetFile.SetBind(self.Ctrls['DwarfMode'].MakeFileKeyBind(f"t $name, Changing to {Dwarf} Form{fullstop}$${self.togon} {Dwarf}$$gototray {self.GetState('DwarfTray')}" + profile.BLF('dwarf.txt')))
            dwrffile = profile.GetBindFile("dwarf.txt")
            if (self.GetState('UseNova')):
                dwrffile.SetBind(self.Ctrls['NovaMode'].MakeFileKeyBind(f"t $name, Changing to {Nova} Form{fullstop}$${self.togoff} {Dwarf}$${self.togon} {Nova}$$gototray {self.GetState('NovaTray')}" + profile.BLF('nova.txt')))

            humpower = ''
            # TODO this control went missing
            #if self.GetState('UseHumanFormPower'): humpower = f'$${self.togon} ' + HumanFormShield
            #else:                                  humpower = ''
            dwrffile.SetBind(self.Ctrls['DwarfMode'].MakeFileKeyBind(f"t $name, Changing to Human Form, SoD Mode{fullstop}$${self.togoff} {Dwarf}{humpower}$$gototray 1" + profile.BLF('reset.txt')))

            dwrffile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind("+forward"))
            dwrffile.SetBind(self.Ctrls['Left'].MakeFileKeyBind("+left"))
            dwrffile.SetBind(self.Ctrls['Right'].MakeFileKeyBind("+right"))
            dwrffile.SetBind(self.Ctrls['Back'].MakeFileKeyBind("+backward"))
            dwrffile.SetBind(self.Ctrls['Up'].MakeFileKeyBind("+up"))
            dwrffile.SetBind(self.Ctrls['Down'].MakeFileKeyBind("+down"))
            dwrffile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind("++forward"))
            dwrffile.SetBind(self.Ctrls['FlyMode'].MakeFileKeyBind('nop'))
            dwrffile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind("follow"))
            if (self.GetState('FlyMode') != self.GetState('SpeedMode')):
                dwrffile.SetBind(self.Ctrls['SpeedMode'].MakeFileKeyBind('nop'))
            if (self.GetState('MouseChord')):
                dwrffile.SetBind('mousechord', "Dwarf Mode Mousechord", self, ['+down', '+forward', t.playerturn])

            # TODO:  this should get DRY'ed up with the normal teleport logic below
            if dwarfTPPower:
                tphovermodeswitch = ''
                if (t.tphover != ''):
                    tphovermodeswitch = t.bla + "000000.txt"

                dwrffile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind(tpActivator + dwarfTPPower))

                tp_off = profile.GetBindFile("dtp","tp_off.txt")
                tp_on1 = profile.GetBindFile("dtp","tp_on1.txt")
                zoomin = '' if t.tphover else t.detailhi + t.runcamdist

                dwrffile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+first$$-first$$powexecname ' + dwarfTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('dtp','tp_on1.txt')))
                if server == 'Homecoming':
                    tp_off.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+first$$-first$$powexecname ' + dwarfTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('dtp','tp_on1.txt')))

                    tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind(f'+first$$-first$${self.unqueue}$$powexeclocation cursor' + dwarfTPPower + zoomin + windowshow + profile.BLF('dtp','tp_off.txt') + tphovermodeswitch))

                else:  # server == Rebirth
                    tp_off.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+ $$powexecname ' + dwarfTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('dtp','tp_on1.txt')))
                    tp_off.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('nop'))

                    tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind(f'- {self.unqueue}' + zoomin + windowshow + profile.BLF('dtp','tp_off.txt') + tphovermodeswitch))
                    tp_on1.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('+ ' + profile.BLF('dtp','tp_on2.txt')))

                    tp_on2 = profile.GetBindFile("dtp","tp_on2.txt")
                    tp_on2.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('- $$powexecname ' + dwarfTPPower + profile.BLF('dtp','tp_on1.txt')))
        ###
        ###### End Kheldian power setup

        if (self.GetState('SimpleSJCJ')):
            jpower = self.GetState('JumpPower')
            if (self.GetState('HasCJ') and jpower):
                ResetFile.SetBind(self.Ctrls['JumpMode'].MakeFileKeyBind(f'powexecname {jpower}$$powexecname Combat Jumping'))
            elif (self.GetState('JumpPower')):
                ResetFile.SetBind(self.Ctrls['JumpMode'].MakeFileKeyBind(f'powexecname {jpower}'))
            elif (self.GetState('HasCJ')):
                ResetFile.SetBind(self.Ctrls['JumpMode'].MakeFileKeyBind(f'powexecname Combat Jumping'))

        # TODO - this is making 'nop' binds even when teleport is completely disabled.
        # That's not right but I'm not in a space to track it down and fix it yet.
        if (not normalTPPower):
            ResetFile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind('nop'))
            ResetFile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('nop'))
            if server == "Rebirth":
                ResetFile.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('nop'))

        # Normal non-peacebringer teleport binds
        if (normalTPPower and not (archetype == "Peacebringer")):
            tphovermodeswitch = ''
            if (t.tphover != ''):
                tphovermodeswitch = t.bla + "000000.txt"

            ResetFile.SetBind(self.Ctrls['TPBindKey'].MakeFileKeyBind(tpActivator + normalTPPower))
            tp_off = profile.GetBindFile("tp","tp_off.txt")
            tp_on1 = profile.GetBindFile("tp","tp_on1.txt")
            zoomin = '' if t.tphover else t.detailhi + t.runcamdist

            if server == 'Homecoming':
                ResetFile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+first$$-first$$powexecname ' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))

                tp_off.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+first$$-first$$powexecname ' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))

                tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind(f'+first$$-first$${self.unqueue}$$' + tpActivator + normalTPPower + zoomin + windowshow + profile.BLF('tp','tp_off.txt') + tphovermodeswitch))

            else: # server == Rebirth
                ResetFile.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+ $$powexecname ' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))
                tp_off.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind('+ $$powexecname ' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))
                tp_off.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('nop'))

                tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeFileKeyBind(f'- $${self.unqueue}' + zoomin + windowshow + profile.BLF('tp','tp_off.txt') + tphovermodeswitch))
                tp_on1.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('+' + profile.BLF('tp','tp_on2.txt')))

                tp_on2 = profile.GetBindFile("tp","tp_on2.txt")
                tp_on2.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('-$$powexecname ' + normalTPPower + profile.BLF('tp','tp_on1.txt')))

        # normal non-peacebringer team teleport binds
        if (self.GetState('HasTTP') and not (archetype == "Peacebringer") and teamTPPower) :

            ResetFile.SetBind(self.Ctrls['TTPBindKey'].MakeFileKeyBind(tpActivator + teamTPPower))

            ttp_off = profile.GetBindFile("ttp","ttp_off.txt")
            ttp_on1 = profile.GetBindFile("ttp","ttp_on1.txt")

            if server == 'Homecoming':
                ResetFile.SetBind(self.Ctrls['TTPComboKey'].MakeFileKeyBind('+first$$-first$$powexecname ' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))

                ttp_off.SetBind(self.Ctrls['TTPComboKey'].MakeFileKeyBind('+first$$-first$$powexecname ' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))

                ttp_on1.SetBind(self.Ctrls['TTPComboKey'].MakeFileKeyBind(f'+first$$-first$${self.unqueue}$$' + tpActivator + teamTPPower + t.detailhi + t.runcamdist + windowshow + profile.BLF('ttp','ttp_off.txt')))

            else:
                ResetFile.SetBind(self.Ctrls['TTPComboKey'].MakeFileKeyBind('+ $$powexecname ' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))

                ttp_off.SetBind(self.Ctrls['TTPComboKey'].MakeFileKeyBind('+ $$powexecname ' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))
                ttp_off.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('nop'))

                ttp_on1.SetBind(self.Ctrls['TTPComboKey'].MakeFileKeyBind(f'- $${self.unqueue}' + t.detailhi + t.runcamdist + windowshow + profile.BLF('ttp','ttp_off.txt')))
                ttp_on1.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('+' + profile.BLF('ttp','ttp_on2.txt')))

                ttp_on2 = profile.GetBindFile("ttp","ttp_on2.txt")
                ttp_on2.SetBind(self.Ctrls['TPExecuteKey'].MakeFileKeyBind('-$$powexecname ' + normalTPPower + profile.BLF('ttp','ttp_on1.txt')))

        return True

    def doSpeedOnDemandBinds(self, t):
        profile   = self.Profile
        ResetFile = profile.ResetFile()
        config    = wx.ConfigBase.Get()

        keybindreset = 'keybind_reset' if config.ReadBool('FlushAllBinds') else ''
        ResetFile.SetBind(config.Read('ResetKey'), "Reset Key", self,
                    [
                        keybindreset,
                        ResetFile.BLF(),
                        'up 0', 'down 0', 'forward 0', 'backward 0', 'left 0', 'right 0',
                        'powexecname Sprint',
                        self.unqueue,
                        't $name, Binds Reset',
                    ])

        # TODO - Disabling, for now, this set of warning dialogs, on the possibly-mistaken notion that
        # I can get the UI to be clearer about this so that these intrusive popups aren't needed.

        #if (self.DefaultMode() == "NonSoD"):
        #    if (not self.GetState('NonSoDEnable')):
        #        wx.MessageBox("Enabling NonSoD mode, since it is set as your default mode.", "Mode Changed", wx.OK|wx.ICON_WARNING)
        #    self.SetState('NonSoDEnable', 1)

        #elif (self.DefaultMode() == "Sprint" and not self.GetState('SprintSoD')):
        #    wx.MessageBox("Enabling NonSoD mode and making it the default, since Sprint SoD, your previous Default mode, is not enabled.", "Mode Changed", wx.OK|wx.ICON_WARNING)
        #    self.SetState('NonSoDEnable', 1)
        #    self.SetState('DefaultMode', "NonSoD")

        #elif (self.DefaultMode() == "Fly" and not (self.GetState('HasHover') or self.GetState('FlyPower'))):
        #    wx.MessageBox("Enabling NonSoD mode and making it the default, since you had selected Fly mode but your character has neither Hover nor a Fly power.", "Mode Changed", wx.OK|wx.ICON_WARNING)
        #    self.SetState('NonSoDEnable', 1)
        #    self.SetState('DefaultMode', "NonSoD")

        #elif (self.DefaultMode() == "Jump" and not (self.GetState('HasCJ') or self.GetState('JumpPower'))):
        #    wx.MessageBox("Enabling NonSoD mode and making it the default, since you had selected Jump mode but your character has neither Combat Jumping nor a Super Jump power.", "Mode Changed", wx.OK|wx.ICON_WARNING)
        #    self.SetState('NonSoDEnable', 1)
        #    self.SetState('DefaultMode', "NonSoD")

        #elif (self.DefaultMode() == "Speed" and not self.GetState('SpeedPower')):
        #    wx.MessageBox("Enabling NonSoD mode and making it the default, since you had selected Super Speed mode but your character doesn't have Super Speed", "Mode Changed", wx.OK|wx.ICON_WARNING)
        #    self.SetState('NonSoDEnable', 1)
        #    self.SetState('DefaultMode', "NonSoD")

        t.basepath     = profile.BindsDir()
        t.gamebasepath = profile.GameBindsDir()

        t.path     = t.basepath     / 'R' / 'R' # run
        t.gamepath = t.gamebasepath / 'R' / 'R'
        t.bl       = f"$${BLF()} {t.gamepath}"

        t.patha     = t.basepath     / 'F' / 'F' # fly
        t.gamepatha = t.gamebasepath / 'F' / 'F'
        t.bla       = f"$${BLF()} {t.gamepatha}"

        t.pathj     = t.basepath     / 'J' / 'J' # jump
        t.gamepathj = t.gamebasepath / 'J' / 'J'
        t.blj       = f"$${BLF()} {t.gamepathj}"

        t.paths     = t.basepath     / 'S' / 'S' # speed
        t.gamepaths = t.gamebasepath / 'S' / 'S'
        t.bls       = f"$${BLF()} {t.gamepaths}"

        #t.pathga     = t.basepath     / 'GF' / 'GF' # group fly
        #t.gamepathga = t.gamebasepath / 'GF' / 'GF'
        #t.blga       = f"$${BLF()} {t.gamepathga}"

        t.pathn     = t.basepath     / 'N' / 'N' # normal / non-sod
        t.gamepathn = t.gamebasepath / 'N' / 'N'
        t.bln       = f"$${BLF()} {t.gamepathn}"

        t.pathgr     = t.basepath     / 'AR' / 'AR'  # autorun ground
        t.gamepathgr = t.gamebasepath / 'AR' / 'AR'
        t.blgr       = f"$${BLF()} {t.gamepathgr}"

        t.pathaf     = t.basepath     / 'AF' / 'AF'  # autorun flight
        t.gamepathaf = t.gamebasepath / 'AF' / 'AF'
        t.blaf       = f"$${BLF()} {t.gamepathaf}"

        t.pathaj     = t.basepath     / 'AJ' / 'AJ'  # autorun jump
        t.gamepathaj = t.gamebasepath / 'AJ' / 'AJ'
        t.blaj       = f"$${BLF()} {t.gamepathaj}"

        t.pathas     = t.basepath     / 'AS' / 'AS'  # autorun speed
        t.gamepathas = t.gamebasepath / 'AS' / 'AS'
        t.blas       = f"$${BLF()} {t.gamepathas}"

        #t.pathgaf     = t.basepath     / 'GAF' / 'GAF'  # autorun group fly
        #t.gamepathgaf = t.gamebasepath / 'GAF' / 'GAF'
        #t.blgaf       = f"$${BLF()} {t.gamepathgaf}"

        t.pathan     = t.basepath     / 'AN' / 'AN' # autorun normal / non-sod
        t.gamepathan = t.gamebasepath / 'AN' / 'AN'
        t.blan       = f"$${BLF()} {t.gamepathan}"

        t.pathfr     = t.basepath     / 'FR' / 'FR'  # Follow Run
        t.gamepathfr = t.gamebasepath / 'FR' / 'FR'
        t.blfr       = f"$${BLF()} {t.gamepathfr}"

        t.pathff     = t.basepath     / 'FF' / 'FF'  # Follow Fly
        t.gamepathff = t.gamebasepath / 'FF' / 'FF'
        t.blff       = f"$${BLF()} {t.gamepathff}"

        t.pathfj     = t.basepath     / 'FJ' / 'FJ'  # Follow Jump
        t.gamepathfj = t.gamebasepath / 'FJ' / 'FJ'
        t.blfj       = f"$${BLF()} {t.gamepathfj}"

        t.pathfs     = t.basepath     / 'FS' / 'FS'  # Follow Speed
        t.gamepathfs = t.gamebasepath / 'FS' / 'FS'
        t.blfs       = f"$${BLF()} {t.gamepathfs}"

        #t.pathgff     = t.basepath     / 'GFF' / 'GFF'  # Follow Group Fly
        #t.gamepathgff = t.gamebasepath / 'GFF' / 'GFF'
        #t.blgff       = f"$${BLF()} {t.gamepathgff}"

        t.pathfn     = t.basepath     / 'FN' / 'FN' # Follow normal / non-sod
        t.gamepathfn = t.gamebasepath / 'FN' / 'FN'
        t.blfn       = f"$${BLF()} {t.gamepathfn}"

        t.pathbo     = t.basepath     / 'BO' / 'BO'  # Blastoff Fly
        t.gamepathbo = t.gamebasepath / 'BO' / 'BO'
        t.blbo       = f"$${BLF()} {t.gamepathbo}"

        t.pathgbo     = t.basepath     / 'GBO' / 'GBO'  # Blastoff Group Fly
        t.gamepathgbo = t.gamebasepath / 'GBO' / 'GBO'
        t.blgbo       = f"$${BLF()} {t.gamepathgbo}"

        #  if a given mode is not our default, get the key we use to enter that mode.
        #  this will (hopefully) only be used if/when we actually have that mode available.
        if (self.DefaultMode() != "NonSoD") : t.NonSoDMode = self.GetState('NonSoDMode')
        if (self.DefaultMode() != "Sprint") : t.SprintMode = self.GetState('SprintMode')
        if (self.DefaultMode() != "Fly")    : t.FlyMode    = self.GetState('FlyMode')
        if (self.DefaultMode() != "Jump")   : t.JumpMode   = self.GetState('JumpMode')
        if (self.DefaultMode() != "Speed")  : t.SpeedMode  = self.GetState('SpeedMode')
        if (self.DefaultMode() != "GFly")   : t.GFlyMode   = self.GetState('GFlyMode')

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

                                t.totalkeys = space+X+W+S+A+D # total number of keys down
                                t.horizkeys = W+S+A+D # total # of horizontal move keys. So Sprint isn't turned on when jumping
                                t.vertkeys  = space+X
                                t.jkeys     = t.horizkeys+t.space
                                if (self.GetState('NonSoDEnable') or t.canqfly or t.mouselookon):
                                    setattr(t, self.DefaultMode() + "Mode", t.NonSoDMode)
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : t.bln,
                                        'bla'        : t.blan,
                                        'blf'        : t.blfn,
                                        'path'       : t.pathn,
                                        'gamepath'   : t.gamepathn,
                                        'patha'      : t.pathan,
                                        'gamepatha'  : t.gamepathan,
                                        'pathf'      : t.pathfn,
                                        'gamepathf'  : t.gamepathfn,
                                        'mobile'     : None,
                                        'stationary' : None,
                                        'modestr'    : "NonSoD",
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                if (self.GetState('EnableSoD') and self.GetState('SprintSoD')):
                                    setattr(t, self.DefaultMode() + "Mode", t.SprintMode)
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
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                if (self.GetState('EnableSoD') and self.GetState('SpeedPower')):
                                    sssj = None
                                    setattr(t, self.DefaultMode() + "Mode", t.SpeedMode)
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
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                if (self.GetState('EnableSoD') and t.canjmp and not (self.GetState('SimpleSJCJ'))):
                                    setattr(t, self.DefaultMode() + "Mode", t.JumpMode)
                                    jturnoff = None
                                    if (t.jump != t.cjmp): jturnoff = {t.jumpifnocj}
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : t.blj,
                                        'bla'        : t.blaj,
                                        'blf'        : t.blfj,
                                        'path'       : t.pathj,
                                        'gamepath'   : t.gamepathj,
                                        'patha'      : t.pathaj,
                                        'gamepatha'  : t.gamepathaj,
                                        'pathf'      : t.pathfj,
                                        'gamepathf'  : t.gamepathfj,
                                        'mobile'     : t.jump,
                                        'stationary' : t.cjmp,
                                        'modestr'    : "Jump",
                                        'flight'     : "Jump",
                                        'fix'        : self.sodJumpFix,
                                        'turnoff'    : jturnoff,
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                if (self.GetState('EnableSoD') and t.canhov or t.canfly):
                                    setattr(t, self.DefaultMode() + "Mode", t.FlyMode)
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
                                        # TODO: added "or t.flyx" here to fix BO/* not being written if hover
                                        # is not available.  This might not be the right solution
                                        'flight'     : t.fly or t.flyx,
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                if (self.GetState('EnableSoD') and t.cangfly):
                                    setattr(t, self.DefaultMode() + "Mode", t.GFlyMode)
                                    self.makeSoDFile({
                                        't'          : t,
                                        'bl'         : t.blga,
                                        'bla'        : t.blgaf,
                                        'blf'        : t.blgff,
                                        'path'       : t.pathga,
                                        'gamepath'   : t.gamepathga,
                                        'patha'      : t.pathgaf,
                                        'pathf'      : t.pathgff,
                                        'mobile'     : t.gfly,
                                        'stationary' : t.gfly,
                                        'modestr'    : "GFly",
                                        'flight'     : "GFly",
                                        'pathbo'     : t.pathgbo,
                                        'blbo'       : t.blgbo,
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

        t.space = t.X = t.W = t.S = t.A = t.D = 0

        t.up   = '$$up 0'
        t.upx  = '$$up 1'
        t.dow  = '$$down 0'
        t.dowx = '$$down 1'
        t.forw = '$$forward 0'
        t.forx = '$$forward 1'
        t.bac  = '$$backward 0'
        t.bacx = '$$backward 1'
        t.lef  = '$$left 0'
        t.lefx = '$$left 1'
        t.rig  = '$$right 0'
        t.rigx = '$$right 1'

    def sodResetKey(self, curfile, gamepath, turnoff):

        config = wx.ConfigBase.Get()

        keybindreset = 'keybind_reset' if config.ReadBool('FlushAllBinds') else ''
        curfile.SetBind(config.Read('ResetKey'), UI.Labels['ResetKey'], self,
            [
                keybindreset,
                'up 0', 'down 0', 'forward 0', 'backward 0', 'left 0', 'right 0',
                str(turnoff),
                't $name, Binds Reset',
                curfile.BaseReset(),
                f"{BLF()} {gamepath}000000.txt"
            ]
        )

    def sodUpKey(self, t, bl, curfile, mobile, stationary, flight, autorun, followbl, bo, sssj):

        (upx,dow,forw,bac,lef,rig) = (t.upx,t.dow,t.forw,t.bac,t.lef,t.rig)

        actkeys = t.totalkeys
        mouselook = ''

        if (not flight) and (not sssj):
            mobile = stationary = None

        if (bo == "bo") :
            upx = '$$up 1'
            dow = '$$down 0'

        if     mobile == "GroupFly": mobile     = None
        if stationary == "GroupFly": stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            actkeys = t.jkeys
            if (t.totalkeys == 1 and t.space == 1): upx = '$$up 0'
            else:                                   upx = '$$up 1'

            if (t.X == 1):                          upx = '$$up 0'

        toggleon   = None
        toggleoff  = None
        toggleoff2 = None
        if (actkeys == 0):
            # pressing just the up key
            mouselook = t.mouselookon
            toggleon = mobile
            if (mobile != stationary): toggleoff = stationary

        if (actkeys == 1 and t.space == 1):
            # releasing the up key, which was the only one held down
            mouselook = t.mouselookoff
            toggleon = stationary
            if (mobile != stationary) : toggleoff = mobile

        if (sssj):
            if (t.space == 0): #  if we are hitting the space bar rather than releasing its..
                toggleon = sssj
                toggleoff = mobile
                if (stationary) and (stationary != mobile) : toggleoff2 = stationary
            elif (t.space == 1) : #  if we are releasing the space bar ..
                toggleoff = sssj
                if (t.horizkeys > 0 or autorun) : #  and we are moving laterally, or in autorun..
                    toggleon = mobile
                else: #  otherwise turn on the stationary power..
                    toggleon = stationary

        toggle = ''
        if (toggleon or toggleoff):
            toggle = self.actPower_toggle(toggleon,[toggleoff,toggleoff2])

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
            curfile.SetBind(self.Ctrls['Up'].MakeFileKeyBind(f"{ini}{upx}{dow}{forw}{bac}{lef}{rig}{mouselook}{toggle}{bl}"))
        else:
            if (not sssj) : toggle = ''  #  returns the following line to the way it was before sssj
            curfile.SetBind(self.Ctrls['Up'].MakeFileKeyBind(f"{ini}{upx}{dow}$$backward 0{lef}{rig}{toggle}{t.mouselookon}{bl}"))

    def sodDownKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo):
        (up,dowx,forw,bac,lef,rig) = (t.up,t.dowx,t.forw,t.bac,t.lef,t.rig)

        actkeys = t.totalkeys
        mouselook      = ''

        if (not flight):
            mobile = stationary = None
        if (bo == 'bo'):
            up = '$$up 1'
            dowx = '$$down 0'

        if (mobile     and mobile     == 'Group Fly'): mobile = None
        if (stationary and stationary == 'Group Fly'): stationary = None

        if (flight == 'Jump'):
            dowx = '$$down 0'
            actkeys = t.jkeys
            if (t.X == 1 and t.totalkeys > 1) : up = '$$up 1'
            else:                               up = '$$up 0'

        toggleon = mobile
        toggleoff = None
        if (actkeys == 0):
            mouselook = t.mouselookon
            toggleon = mobile
            if (mobile != stationary): toggleoff = stationary

        if (t.totalkeys == 1 and t.X == 1):
            mouselook = t.mouselookoff
            if (mobile != stationary): toggleoff = mobile
            toggleon = stationary

        toggle = ''
        if (toggleon or toggleoff):
            toggle = self.actPower_toggle(toggleon,toggleoff)

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
            curfile.SetBind(self.Ctrls['Down'].MakeFileKeyBind(f"{ini}{up}{dowx}{forw}{bac}{lef}{rig}{mouselook}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Down'].MakeFileKeyBind(f"{ini}{up}{dowx}$$backward -1{lef}{rig}{t.mouselookon}{bl}"))

    def sodForwardKey(self, t, bl, curfile,  mobile, stationary, flight, autorunbl, followbl, bo, sssj):
        (up,dow,forx,bac,lef,rig) = (t.up,t.dow,t.forx,t.bac,t.lef,t.rig)
        name = UI.Labels['Forward']

        mouselook = ''
        if (bo == "bo") : up = '$$up 1'; dow = '$$down 0'

        if (mobile     == 'Group Fly'): mobile = None
        if (stationary == 'Group Fly'): stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            if (
                 (t.totalkeys == 1 and t.W == 1)
                     or
                 (t.X == 1)
            ):     up = '$$up 0'
            else : up = '$$up 1'

        toggleon = mobile
        toggleoff = stationary
        if (t.totalkeys == 0) :
            mouselook = t.mouselookon
            if (not mobile) and (mobile != '') and (mobile != stationary):
                toggleoff = stationary

        if (t.totalkeys == 1 and t.W == 1):
            mouselook = t.mouselookoff

        if flight: testKeys = t.totalkeys
        else:      testKeys = t.horizkeys

        if (testKeys == 1 and t.W == 1):
            toggleoff = mobile
            toggleon = stationary

        if (sssj and t.space == 1):
           toggleon = sssj
           toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff):
            toggle = self.actPower_toggle(toggleon,toggleoff)

        newbits = t.KeyState({'toggle' : 'W'})
        bl = f"{bl}{newbits}.txt"

        if t.W == 1: ini = "-down"
        else:        ini = "+down"

        if (followbl):
            if (t.W == 1):
                move = ini
            else:
                bl = f"{followbl}{newbits}.txt"
                move = f"{ini}{up}{dow}{forx}{bac}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind(move + bl))
            if (self.GetState('MouseChord')):
                if (t.W != 1) : move = f"{ini}{up}{dow}{forx}{bac}{rig}{lef}{t.playerturn}"
                curfile.SetBind('mousechord', name, self, move + bl)

        elif (not autorunbl):
            curfile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind(f"{ini}{up}{dow}{forx}{bac}{lef}{rig}{mouselook}{toggle}{bl}"))
            if (self.GetState('MouseChord')):
                curfile.SetBind('mousechord', name, self, f"{ini}{up}{dow}{forx}{bac}{rig}{lef}{mouselook}{toggle}{t.playerturn}{bl}")

        else:
            if (t.W != 1):
                bl = f"{autorunbl}{newbits}.txt"

            curfile.SetBind(self.Ctrls['Forward'].MakeFileKeyBind(f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{lef}{rig}{t.mouselookon}{bl}"))
            if (self.GetState('MouseChord')) :
                curfile.SetBind('mousechord', name, self, f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{rig}{lef}{t.mouselookon}{t.playerturn}{bl}")

    def sodBackKey(self,t,bl,curfile,mobile,stationary,flight,autorunbl,followbl,bo,sssj):
        (up,dow,forw,bacx,lef,rig) = (t.up,t.dow,t.forw, t.bacx,t.lef,t.rig)

        mouselook = ''
        if (bo == "bo") : up = '$$up 1';dow = '$$down 0'

        if (mobile     == 'Group Fly'): mobile = None
        if (stationary == 'Group Fly'): stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            if (t.totalkeys == 1 and t.S == 1) : up = '$$up 0'
            else:                                up = '$$up 1'

            if (t.X == 1) : up = '$$up 0'

        toggleon = mobile
        toggleoff = stationary
        if (t.totalkeys == 0):
            mouselook = t.mouselookon
            toggleon = mobile
            if (not mobile) and (mobile != '') and (mobile != stationary):
                toggleoff = stationary

        if (t.totalkeys == 1 and t.S == 1):
            mouselook = t.mouselookoff

        if flight: testKeys = t.totalkeys
        else:      testKeys = t.horizkeys

        if (testKeys == 1 and t.S == 1):
            toggleoff = mobile
            toggleon = stationary

        if (sssj and t.space == 1): #  if we are jumping with SS+SJ mode enabled
            toggleon = sssj
            toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
            toggle = self.actPower_toggle(toggleon,toggleoff)

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
            curfile.SetBind(self.Ctrls['Back'].MakeFileKeyBind(f"{ini}{up}{dow}{forw}{bacx}{lef}{rig}{mouselook}{toggle}{bl}"))
        else:
            if (t.S == 1):
                move = '$$forward 1$$backward 0'
            else:
                move = '$$forward 0$$backward 1'
                bl = f"{autorunbl}{newbits}.txt"

            curfile.SetBind(self.Ctrls['Back'].MakeFileKeyBind(f"{ini}{up}{dow}{move}{lef}{rig}{t.mouselookon}{bl}"))

    def sodLeftKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo,sssj):
        (up,dow,forw,bac,lefx,rig) = (t.up,t.dow,t.forw,t.bac, t.lefx,t.rig)

        mouselook = ''
        if (bo == "bo") : up = '$$up 1';dow = '$$down 0'

        if (mobile     == 'Group Fly') : mobile = None
        if (stationary == 'Group Fly') : stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            if (t.totalkeys == 1 and t.A == 1) : up = '$$up 0'
            else:                                up = '$$up 1'

            if (t.X == 1) : up = '$$up 0'

        toggleon = mobile
        toggleoff = stationary
        if (t.totalkeys == 0):
            mouselook = t.mouselookon
            toggleon = mobile
            if (not mobile) and (mobile != '') and (mobile != stationary) :
                toggleoff = stationary

        if (t.totalkeys == 1 and t.A == 1) :
            mouselook = t.mouselookoff

        if flight: testKeys = t.totalkeys
        else:      testKeys = t.horizkeys

        if (testKeys == 1 and t.A == 1) :
            toggleoff = mobile
            toggleon = stationary

        if (sssj and t.space == 1) : #  if we are jumping with SS+SJ mode enabled
            toggleon  = sssj
            toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
            toggle = self.actPower_toggle(toggleon,toggleoff)

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
            curfile.SetBind(self.Ctrls['Left'].MakeFileKeyBind(f"{ini}{up}{dow}{forw}{bac}{lefx}{rig}{mouselook}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Left'].MakeFileKeyBind(f"{ini}{up}{dow}{'$$backward 0'}{lefx}{rig}{t.mouselookon}{bl}"))

    def sodRightKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,bo,sssj):
        (up,dow,forw,bac,lef,rigx) = (t.up,t.dow,t.forw,t.bac,t.lef, t.rigx)

        mouselook = ''
        if (bo == "bo") :up = '$$up 1';dow = '$$down 0'

        if (mobile     == 'Group Fly') : mobile = None
        if (stationary == 'Group Fly') : stationary = None

        if (flight == "Jump"):
            dow = '$$down 0'
            if (t.totalkeys == 1 and t.D == 1) : up = '$$up 0'
            else:                                up = '$$up 1'

            if (t.X == 1) : up = '$$up 0'

        toggleon = mobile
        toggleoff = stationary
        if (t.totalkeys == 0):
            mouselook = t.mouselookon
            toggleon = mobile
            if (not mobile) and (mobile != '') and (mobile != stationary) :
                toggleoff = stationary

        if (t.totalkeys == 1 and t.D == 1) :
            mouselook = t.mouselookoff

        if flight: testKeys = t.totalkeys
        else :     testKeys = t.horizkeys

        if (testKeys == 1 and t.D == 1) :
            toggleoff = mobile
            toggleon = stationary

        if (sssj and t.space == 1) : #  if we are jumping with SS+SJ mode enabled
            toggleon = sssj
            toggleoff = mobile

        toggle = ''
        if (toggleon or toggleoff) :
            toggle = self.actPower_toggle(toggleon,toggleoff)

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
            curfile.SetBind(self.Ctrls['Right'].MakeFileKeyBind(f"{ini}{up}{dow}{forw}{bac}{lef}{rigx}{mouselook}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Right'].MakeFileKeyBind(f"{ini}{up}{dow}$$forward 1$$backward 0{lef}{rigx}{t.mouselookon}{bl}"))

    def sodAutoRunKey(self,t,bl,curfile,mobile,sssj):
        bindload = bl + t.KeyState() + ".txt"
        if (sssj and t.space == 1) :
            curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mouselookon + self.actPower_name(sssj,mobile) + bindload))
        else:
            curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mouselookon + self.actPower_name(mobile) + bindload))

    # TODO sssj never gets passed in, in citybinder.  Is this right?
    def sodAutoRunOffKey(self, t,bl,curfile,mobile,stationary,flight,sssj = None):
        toggleon = toggleoff = None
        if sssj and t.space == 1:
            toggleoff = mobile
            mobile = sssj
        if (not flight) and (not sssj) :
            if (t.horizkeys > 0) :
                toggleon = t.mouselookon + self.actPower_name(mobile)
            else:
                toggleon = t.mouselookoff + self.actPower_name(stationary,mobile)

        elif (sssj) :
            if (t.horizkeys > 0 or t.space == 1) :
                toggleon = t.mouselookon + self.actPower_name(mobile,toggleoff)
            else:
                toggleon = t.mouselookoff + self.actPower_name(stationary,mobile,toggleoff)

        else:
            if (t.totalkeys > 0) :
                toggleon = t.mouselookon + self.actPower_name(mobile)
            else:
                toggleon = t.mouselookoff + self.actPower_name(stationary,mobile)

        bindload = bl + t.KeyState() + '.txt'
        # "[2:]" on next line is to trim off the initial "$$" that dirs() provides
        curfile.SetBind(self.Ctrls['AutoRun'].MakeFileKeyBind(t.dirs('UDFBLR')[2:] + toggleon + bindload))

    def sodFollowKey(self, t,bl,curfile,mobile,stationary):
        curfile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind('follow' + self.actPower_toggle(mobile,stationary) + bl + t.KeyState() + '.txt'))

    def sodFollowOffKey(self, t,bl,curfile,mobile,stationary,flight):
        toggle = ''
        if (not flight):
            if (t.horizkeys == 0) :
                if (stationary != mobile) :
                   toggle = self.actPower_toggle(stationary,mobile)
                else:
                   toggle = self.actPower_name(stationary)

        else:
            if (t.totalkeys == 0) :
                if (stationary != mobile) :
                   toggle = self.actPower_toggle(stationary,mobile)
                else:
                   toggle = self.actPower_name(stationary)

        curfile.SetBind(self.Ctrls['Follow'].MakeFileKeyBind("follow" + toggle + t.up + t.dow + t.forw + t.bac + t.lef + t.rig + bl + t.KeyState() + '.txt'))

    #  toggleon variation
    def actPower_toggle(self, on, off, start = False):
        s = ''

        offpower = set()

        if off and not isinstance(off, str):
            for w in off:
                if (w and w != on and not (w in offpower)):
                    offpower.add(w)
                    s = s + f'$${self.togoff} {w}'

        else:
            if (off and off != '' and (off != on) and not (off in offpower)):
                offpower.add(off)
                s = s + f'$${self.togoff} {off}'

        if (on and on != ''):
            s = s + f'$${self.togon} {on}'

        if start: s = s[2:]
        return s

    def actPower_name(self, on, *rest):
        s = ''
        for v in rest:
            if isinstance(v, str):
                if (v != '' and v != on):
                    s = s + '$$powexecname ' + v

            elif isinstance(v, set):
                for w in v:
                    if (w and w != on):
                        s = s + '$$powexecname ' + w

        if (s != ''):
            s = s + f'$${self.unqueue}'

        if (on and on != ''):
            s = s + '$$powexecname ' + on + '$$powexecname ' + on

        return s

    def sodJumpFix(self, profile,t,key,makeModeKey,suffix,bl,curfile,turnoff,autofollowmode,feedback):

        filename     = str(getattr(t,"path"     + f"{autofollowmode}j")) + t.KeyState() + suffix + '.txt'
        gamefilename = str(getattr(t,"gamepath" + f"{autofollowmode}j")) + t.KeyState() + suffix + '.txt'
        tglfile      = profile.GetBindFile(filename)
        t.ini        = '-down$$'
        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key, "Jump Fix", self, "+down" + feedback + self.actPower_name(t.cjmp) + profile.BLF(gamefilename))

    def sodSetDownFix(self, profile,t,key,makeModeKey,suffix,bl,curfile,turnoff,autofollowmode,feedback):
        if autofollowmode:
            pathsuffix = "f"
        else:
            pathsuffix = "a"

        filename     = str(getattr(t,'path'     + f"{autofollowmode}{pathsuffix}")) + t.KeyState() + suffix + ".txt"
        gamefilename = str(getattr(t,'gamepath' + f"{autofollowmode}{pathsuffix}")) + t.KeyState() + suffix + ".txt"
        tglfile      = profile.GetBindFile(filename)
        t.ini        = '-down$$'

        makeModeKey(profile,t,bl,tglfile,turnoff,None,1)
        curfile.SetBind(key, "SetDown Fix", self, '+down' + feedback + profile.BLF(gamefilename))


    ### convenience methods
    def DefaultMode(self):
        return self.GetState('DefaultMode') if self.GetState('EnableSoD') else 'NonSoD'

    def hasHover(self):
        return bool(
            (self.Profile.HasPowerPool('Flight') or self.Profile.Archetype() == "Peacebringer")
            and self.GetState('HasHover')
        )

    def hasGFly(self):
        return bool(self.Profile.HasPowerPool('Flight') and self.GetState('HasGFly'))

    def isKheldian(self):
        return bool(self.Profile.Archetype() == "Warshade" or self.Profile.Archetype() == "Peacebringer")

    def AllBindFiles(self):
        files = []
        dirs  = [
                'R'  , 'F'   , 'J'  , 'S'  , 'N'  ,
                'AR' , 'AF'  , 'AJ' , 'AS' , 'AN' ,
                'FR' , 'FF'  , 'FJ' , 'FS' , 'FN' ,
                'BO' , 'GBO' ,
        ]
        for dir in dirs:
            for sp in (0,1):
                for X in (0,1):
                    for W in (0,1):
                        for S in (0,1):
                            for A in (0,1):
                                for D in (0,1):
                                    for suffix in ['', 'f', 'j', 'a', 'n', 'r', 's', 'gf', '_t', '_s',]:
                                        files.append(
                                            self.Profile.GetBindFile(dir,
                                                f'{dir}{sp}{X}{W}{S}{A}{D}{suffix}.txt')
                                            )

        files.append(self.Profile.GetBindFile('nova.txt'))
        files.append(self.Profile.GetBindFile('dwarf.txt'))

        dirs.append('dtp')
        files.append(self.Profile.GetBindFile('dtp', 'tp_on.txt')) # historical
        files.append(self.Profile.GetBindFile('dtp', 'tp_on1.txt'))
        files.append(self.Profile.GetBindFile('dtp', 'tp_on2.txt'))
        files.append(self.Profile.GetBindFile('dtp', 'tp_off.txt'))

        dirs.append('tp')
        files.append(self.Profile.GetBindFile('tp', 'tp_on.txt')) # historical
        files.append(self.Profile.GetBindFile('tp', 'tp_on1.txt'))
        files.append(self.Profile.GetBindFile('tp', 'tp_on2.txt'))
        files.append(self.Profile.GetBindFile('tp', 'tp_off.txt'))

        dirs.append('ttp')
        files.append(self.Profile.GetBindFile('ttp', 'ttp_on.txt')) # historical
        files.append(self.Profile.GetBindFile('ttp', 'ttp_on1.txt'))
        files.append(self.Profile.GetBindFile('ttp', 'ttp_on2.txt'))
        files.append(self.Profile.GetBindFile('ttp', 'ttp_off.txt'))

        return {
            'files' : files,
            'dirs'  : dirs,
        }

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

    'EnableSoD'      : 'Enable Speed on Demand Binds',
    'DefaultMode'    : 'Default Speed on Demand Mode',
    'SprintPower'    : 'Power to use for Sprint',
    'NonSoDEnable'   : 'Enable Speed-on-Demand Toggle',
    'NonSoDMode'     : 'Speed on Demand Toggle',
    'SprintSoD'      : 'Enable Sprint Speed on Demand',
    'SprintMode'     : "Sprint Mode",
    'MouseChord'     : 'Mousechord is SoD Forward',
    'Feedback'       : 'Self-/tell when changing SoD mode',

    'PlayerTurn'     : 'Turn to match camera',
    'AutoMouseLook'  : 'Mouselook when moving',
    'ChangeCamera'   : 'Change camera distance when moving',
    'CamdistBase'    : 'Base Camera Distance',
    'CamdistMove'    : 'Travelling Camera Distance',
    'ChangeDetail'   : 'Change graphics detail level when moving',
    'DetailBase'     : 'Base Detail Level',
    'DetailMove'     : 'Travelling Detail Level',

    'JumpPower'        : "Primary Jump Power",
    'HasCJ'            : 'Has Combat Jumping',
    'JumpMode'         : 'Toggle Jump Mode',
    'SimpleSJCJ'       : 'Simple Combat Jumping / Super Jump Toggle',
    'JumpSpecialKey'   : '',
    'JumpSpecialPower' : '', # hidden

    'SpeedPower'        : "Primary Speed Power",
    'SpeedMode'         : 'Toggle Super Speed Mode',
    'SSMobileOnly'      : 'SuperSpeed only when moving',
    'SSSJModeEnable'    : 'Enable Super Speed / Super Jump Mode',
    'SpeedSpecialKey'   : '',
    'SpeedSpecialPower' : '', # Hidden

    'FlyPower'        : "Primary Flight Power",
    'HasHover'        : "Has Hover",
    'HasGFly'         : 'Has Group Fly',
    'FlyMode'         : 'Toggle Fly Mode',
    'FlySpecialKey'   : 'Afterburner',
    'FlySpecialPower' : '', # hidden
    'GFlyMode'        : 'Toggle Group Fly Mode',

    'TPPower'        : 'Teleport Power',
    'TPComboKey'     : 'Hold to Show Teleport Target Marker',
    'TPTPHover'      : 'Hover when Teleporting',
    'HasTTP'         : 'Has Team Teleport',
    'TTPComboKey'    : 'Hold to Show Team Teleport Target Marker',
    'TTPTPGFly'      : 'Group Fly when Team Teleporting',
    'TPHideWindows'  : 'Hide Windows when Holding Target Marker Key',

    'TempEnable'     : 'Enable Temp Travel Power Bind',
    'TempToggle'     : 'Toggle Temp Travel Power',

    'HumanTray'      : 'Human Form Power Tray',
    'UseNova'        : 'Use Nova Form Toggle',
    'NovaMode'       : 'Toggle Nova Form',
    'NovaTray'       : 'Nova Form Power Tray',
    'UseDwarf'       : 'Use Dwarf Form Toggle',
    'DwarfMode'      : 'Toggle Dwarf Form',
    'DwarfTray'      : 'Dwarf Form Power Tray',
})

class tObject(dict):
    def __init__(self, profile):
        from Profile import Profile
        self.togon   = "powexectoggleon"  if profile.Server == "Homecoming" else "px_tgon"
        self.togoff  = "powexectoggleoff" if profile.Server == "Homecoming" else "px_tgof"

        self.profile      :Profile = profile
        self.ini          :str = ''
        self.sprint       :str = ''
        self.speed        :str = ''
        self.hover        :str = ''
        self.fly          :str = ''
        self.gfly         :str = ''
        self.flyx         :str = ''
        self.jump         :str = ''
        self.cjmp         :str = ''
        self.canhov       :bool = False
        self.canfly       :bool = False
        self.canqfly      :bool = False
        self.cangfly      :bool = False
        self.cancj        :bool = False
        self.canjmp       :bool = False
        self.tphover      :str = ''
        self.ttpgfly      :str = ''
        self.on           :str = f'$${self.togon} '
        self.off          :str = f'$${self.togoff} '
        self.playerturn   :str = ''
        self.mouselookon  :str = ''
        self.mouselookoff :str = ''
        self.runcamdist   :str = ''
        self.flycamdist   :str = ''
        self.detailhi     :str = ''
        self.detaillo     :str = ''
        self.NonSoDMode   :str = ''
        self.SprintMode   :str = ''
        self.FlyMode      :str = ''
        self.JumpMode     :str = ''
        self.SpeedMode    :str = ''
        self.GFlyMode     :str = ''
        self.jumpifnocj   :str = ''

        self.space:int = 0
        self.X    :int = 0
        self.W    :int = 0
        self.S    :int = 0
        self.A    :int = 0
        self.D    :int = 0
        self.up   :str = ''
        self.dow  :str = ''
        self.forw :str = ''
        self.bac  :str = ''
        self.lef  :str = ''
        self.rig  :str = ''
        self.upx  :str = ''
        self.dowx :str = ''
        self.forx :str = ''
        self.bacx :str = ''
        self.lefx :str = ''
        self.rigx :str = ''

        self.bl    :str = ''
        self.bla   :str = ''
        self.blaf  :str = ''
        self.blaj  :str = ''
        self.blan  :str = ''
        self.blas  :str = ''
        self.blat  :str = ''
        self.blbo  :str = ''
        self.blf   :str = ''
        self.blff  :str = ''
        self.blfn  :str = ''
        self.blfj  :str = ''
        self.blfs  :str = ''
        self.blft  :str = ''
        self.blfr  :str = ''
        self.blgr  :str = ''
        self.blga  :str = ''
        self.blgaf :str = ''
        self.blgbo :str = ''
        self.blgff :str = ''
        self.blj   :str = ''
        self.bln   :str = ''
        self.bls   :str = ''
        self.blt   :str = ''

        self.path    :Path = Path()
        self.patha   :Path = Path()
        self.pathaf  :Path = Path()
        self.pathaj  :Path = Path()
        self.pathan  :Path = Path()
        self.pathas  :Path = Path()
        self.pathat  :Path = Path()
        self.pathbo  :Path = Path()
        self.pathf   :Path = Path()
        self.pathff  :Path = Path()
        self.pathfn  :Path = Path()
        self.pathfj  :Path = Path()
        self.pathfs  :Path = Path()
        self.pathft  :Path = Path()
        self.pathfr  :Path = Path()
        self.pathga  :Path = Path()
        self.pathgaf :Path = Path()
        self.pathgbo :Path = Path()
        self.pathgff :Path = Path()
        self.pathgr  :Path = Path()
        self.pathj   :Path = Path()
        self.pathn   :Path = Path()
        self.paths   :Path = Path()
        self.patht   :Path = Path()

        self.gamepath   :PureWindowsPath = PureWindowsPath()
        self.gamepatha  :PureWindowsPath = PureWindowsPath()
        self.gamepathaf :PureWindowsPath = PureWindowsPath()
        self.gamepathaj :PureWindowsPath = PureWindowsPath()
        self.gamepathan :PureWindowsPath = PureWindowsPath()
        self.gamepathas :PureWindowsPath = PureWindowsPath()
        self.gamepathat :PureWindowsPath = PureWindowsPath()
        self.gamepathbo :PureWindowsPath = PureWindowsPath()
        self.gamepathf  :PureWindowsPath = PureWindowsPath()
        self.gamepathff :PureWindowsPath = PureWindowsPath()
        self.gamepathfn :PureWindowsPath = PureWindowsPath()
        self.gamepathfj :PureWindowsPath = PureWindowsPath()
        self.gamepathfs :PureWindowsPath = PureWindowsPath()
        self.gamepathft :PureWindowsPath = PureWindowsPath()
        self.gamepathfr :PureWindowsPath = PureWindowsPath()
        self.gamepathga :PureWindowsPath = PureWindowsPath()
        self.gamepathgbo:PureWindowsPath = PureWindowsPath()
        self.gamepathgr :PureWindowsPath = PureWindowsPath()
        self.gamepathj  :PureWindowsPath = PureWindowsPath()
        self.gamepathn  :PureWindowsPath = PureWindowsPath()
        self.gamepaths  :PureWindowsPath = PureWindowsPath()
        self.gamepatht  :PureWindowsPath = PureWindowsPath()

        self.basepath     :Path = Path()
        self.gamebasepath :PureWindowsPath = PureWindowsPath()

        self.vertkeys  :int = 0
        self.horizkeys :int = 0
        self.jkeys     :int = 0
        self.totalkeys :int = 0


    # return binary "011010" string of which keys are "on";
    # optionally flipping one of them first.
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

    # This will return "${BLF()} C:\path\CODE\CODE101010<suffix>.txt"
    def BLF(self, code, suffix = ''):
        return self.profile.BLF(code.upper(), code.upper() + self.KeyState() + suffix + '.txt')
