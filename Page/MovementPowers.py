import re
import wx
from typing import Any, Literal, Final

from BLF import BLF
import GameData
from Icon import GetIcon
from Models.tObject import tObject
from Page import Page
import UI
from UI.ControlGroup import ControlGroup
from UI.CGControls import bcKeyButton, cgStaticText
from UI.KeySelectDialog import EVT_KEY_CHANGED
from UI.PowerPicker import PowerPicker

# "Constants"
ACTION_SOD : Final = 1
ACTION_PT  : Final = 2

class MovementPowers(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.TabTitle : str = "Movement / Speed on Demand"

        self.TempTravelPowerMenu : wx.Menu|None = None

        # A few things that are server-specific.  If we change servers, we reload the profile
        # so this is safe to do in __init__
        server : str = self.Profile.Server()
        self.togon   : str = "px_tgon" if server == "Rebirth" else "powexectoggleon"
        self.togoff  : str = "px_tgof" if server == "Rebirth" else "powexectoggleoff"
        self.unqueue : str = "px_uq"   if server == "Rebirth" else "powexecunqueue"

        self.Init: dict[str, Any] = {
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
            'PlayerTurn'      : False, # TODO this should toggle with "Keybind Profile" somehow
            'AutoMouseLook'   : False,

            'ChangeCamera'    : False,
            'CamdistBase'     : 15,
            'CamdistMove'     : 60,
            'ChangeDetail'    : False,
            'DetailBase'      : 100,
            'DetailMove'      : 50,
            'Feedback'        : False,

            'DefaultMode'     : "Sprint",
            'NonSoDMode'      : '',
            'MouseChord'      : True,

            'SprintKeyAction' : 'Speed on Demand',
            'SprintMode'      : '',
            'SprintPower'     : 'Sprint',

            'SpeedKeyAction'    : 'Speed on Demand',
            'SpeedPower'        : '',
            'SpeedMode'         : '',
            'SSSJModeEnable'    : False,
            'SpeedSpecialKey'   : '',
            'SpeedSpecialPower' : '', # hidden

            'JumpKeyAction'    : 'Speed on Demand',
            'JumpPower'        : '',
            'CJPower'          : 'Combat Jumping',
            'JumpMode'         : '',
            'JumpSpecialKey'   : '',
            'JumpSpecialPower' : '', # hidden

            'FlyKeyAction'    : 'Speed on Demand',
            'FlyPower'        : '',
            'HoverPower'      : 'Hover',
            'FlyMode'         : '',
            'GFlyMode'        : '',
            'FlySpecialKey'   : '',
            'FlySpecialPower' : '', # hidden

            'TPPower'         : '',
            'TPBindKey'       : '',
            'TPComboKey'      : 'LSHIFT',
            'TPExecuteKey'    : 'SHIFT+BUTTON1', # hidden rebirth magic

            'TTPBindKey'      : '',
            'TTPComboKey'     : 'LCTRL',
            'TTPExecuteKey'   : 'CTRL+BUTTON1', # hidden rebirth magic
            'TTPTPGFly'       : False,

            'TPHideWindows'   : True,
            'TPTPHover'       : False,

            'FlyGFly'         : '',

            'KhelFeedback'      : False,
            'UseHumanFormPower' : False,
            'HumanTray'         : "1",

            'NovaMode'        : "[",
            'NovaTray'        : "4",

            'DwarfMode'       : "]",
            'DwarfTray'       : "5",


            'TempEnable'      : False,
            'TempToggle'      : '',
        }

        if server == "Homecoming":
            UI.Labels.update({
                'TPBindKey'      : 'Teleport to Cursor Immediately',
                'TTPBindKey'     : 'Team Teleport to Cursor Immediately',
            })
        else:
            UI.Labels.update({
                'TPBindKey'      : 'Activate Teleport Power',
                'TTPBindKey'     : 'Activate Team Teleport Power',
            })

    def BuildPage(self) -> None:

        server = self.Profile.Server()

        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.leftColumn  = wx.BoxSizer(wx.VERTICAL)
        self.rightColumn = wx.BoxSizer(wx.VERTICAL)

        # hidden controls for keeping state
        self.hiddenSizer = ControlGroup(self, self, "Hidden Settings")
        self.hiddenSizer.AddControl(ctlName = 'FlySpecialPower', ctlType = 'text', )
        self.hiddenSizer.AddControl(ctlName = 'JumpSpecialPower', ctlType = 'text', )
        self.hiddenSizer.AddControl(ctlName = 'SpeedSpecialPower', ctlType = 'text', )
        self.leftColumn.Add(self.hiddenSizer)
        self.leftColumn.Hide(self.hiddenSizer)

        ##### MOVEMENT KEYS
        self.MovementSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label = "Movement Keys")
        staticbox = self.MovementSizer.GetStaticBox()
        innerSizer = wx.BoxSizer(wx.VERTICAL)
        self.MovementSizer.Add(innerSizer, 1, wx.ALL|wx.ALIGN_CENTER, 10)

        keySizer = wx.GridBagSizer(6, 3)
        tlLabel = cgStaticText(staticbox, label = 'Turn Left')
        fwLabel = cgStaticText(staticbox, label = 'Forward')
        trLabel = cgStaticText(staticbox, label = 'Turn Right')

        keySizer.Add(tlLabel, wx.GBPosition(0,0), wx.GBSpan(1,2), wx.ALIGN_CENTER)
        keySizer.Add(fwLabel, wx.GBPosition(0,2), wx.GBSpan(1,2), wx.ALIGN_CENTER)
        keySizer.Add(trLabel, wx.GBPosition(0,4), wx.GBSpan(1,2), wx.ALIGN_CENTER)

        tleftButton = bcKeyButton(staticbox)
        tleftButton.SetLabel(self.Init['TurnLeft'])
        self.Ctrls['TurnLeft'] = tleftButton
        tleftButton.CtlName = 'TurnLeft'
        tleftButton.CtlLabel = tlLabel
        tleftButton.Page = self
        tleftButton.Key = self.Init['TurnLeft']
        keySizer.Add(tleftButton, wx.GBPosition(1,0), wx.GBSpan(1,2))

        forwardButton = bcKeyButton(staticbox)
        self.Ctrls['Forward'] = forwardButton
        forwardButton.SetLabel(self.Init['Forward'])
        forwardButton.CtlName = 'Forward'
        forwardButton.CtlLabel = fwLabel
        forwardButton.Page = self
        forwardButton.Key = self.Init['Forward']
        keySizer.Add(forwardButton, wx.GBPosition(1,2), wx.GBSpan(1,2))

        trightButton = bcKeyButton(staticbox)
        self.Ctrls['TurnRight'] = trightButton
        trightButton.SetLabel(self.Init['TurnRight'])
        trightButton.CtlName = 'TurnRight'
        trightButton.CtlLabel = trLabel
        trightButton.Page = self
        trightButton.Key = self.Init['TurnRight']
        keySizer.Add(trightButton, wx.GBPosition(1,4), wx.GBSpan(1,2))

        leftLabel  = cgStaticText(staticbox, label = 'Left')
        backLabel  = cgStaticText(staticbox, label = 'Back')
        rightLabel = cgStaticText(staticbox, label = 'Right')

        leftButton = bcKeyButton(staticbox)
        self.Ctrls['Left'] = leftButton
        leftButton.SetLabel(self.Init['Left'])
        leftButton.CtlName = 'Left'
        leftButton.CtlLabel = leftLabel
        leftButton.Page = self
        leftButton.Key = self.Init['Left']
        keySizer.Add(leftButton, wx.GBPosition(2,0), wx.GBSpan(1,2))

        backButton = bcKeyButton(staticbox)
        backButton.SetLabel(self.Init['Back'])
        self.Ctrls['Back'] = backButton
        backButton.CtlName = 'Back'
        backButton.CtlLabel = backLabel
        backButton.Page = self
        backButton.Key = self.Init['Back']
        keySizer.Add(backButton, wx.GBPosition(2,2), wx.GBSpan(1,2))

        rightButton = bcKeyButton(staticbox)
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

        downLabel = cgStaticText(staticbox, label = 'Down')
        upLabel   = cgStaticText(staticbox, label = 'Up')

        keySizer.Add(downLabel, wx.GBPosition(4,0), wx.GBSpan(1,2), wx.ALIGN_CENTER|wx.TOP, 16)
        keySizer.Add(upLabel,   wx.GBPosition(4,2), wx.GBSpan(1,4), wx.ALIGN_CENTER|wx.TOP, 16)

        downButton = bcKeyButton(staticbox)
        self.Ctrls['Down'] = downButton
        downButton.SetLabel(self.Init['Down'])
        downButton.CtlName = 'Down'
        downButton.CtlLabel = downLabel
        downButton.Page = self
        downButton.Key = self.Init['Down']
        keySizer.Add(downButton, wx.GBPosition(5,0), wx.GBSpan(1,2), wx.EXPAND)

        upButton = bcKeyButton(staticbox)
        self.Ctrls['Up'] = upButton
        upButton.SetLabel(self.Init['Up'])
        upButton.CtlName = 'Up'
        upButton.CtlLabel = upLabel
        upButton.Page = self
        upButton.Key = self.Init['Up']
        keySizer.Add(upButton, wx.GBPosition(5,2), wx.GBSpan(1,4), wx.EXPAND)

        autoRunLabel = cgStaticText(staticbox, label = 'Autorun')
        followLabel  = cgStaticText(staticbox, label = 'Follow')

        keySizer.Add(autoRunLabel, wx.GBPosition(6,1), wx.GBSpan(1,2), wx.ALIGN_CENTER)
        keySizer.Add(followLabel,  wx.GBPosition(6,3), wx.GBSpan(1,2), wx.ALIGN_CENTER)

        autoRunButton = bcKeyButton(staticbox)
        self.Ctrls['AutoRun'] = autoRunButton
        autoRunButton.SetLabel(self.Init['AutoRun'])
        autoRunButton.CtlName = 'AutoRun'
        autoRunButton.CtlLabel = autoRunLabel
        autoRunButton.Page = self
        autoRunButton.Key = self.Init['AutoRun']
        keySizer.Add(autoRunButton, wx.GBPosition(7,1), wx.GBSpan(1,2), wx.EXPAND)

        followButton = bcKeyButton(staticbox)
        self.Ctrls['Follow'] = followButton
        followButton.SetLabel(self.Init['Follow'])
        followButton.CtlName = 'Follow'
        followButton.CtlLabel = followLabel
        followButton.Page = self
        followButton.Key = self.Init['Follow']
        keySizer.Add(followButton, wx.GBPosition(7,3), wx.GBSpan(1,2), wx.EXPAND)

        innerSizer.Add(keySizer, 0)

        self.leftColumn.Add(self.MovementSizer, 0, wx.EXPAND)

        ### DETAIL SETTINGS
        detailSizer = ControlGroup(self, self, 'Detail and Camera Settings')
        detailSizer.AddControl(ctlName = 'PlayerTurn', ctlType = 'checkbox',
            tooltip = 'Turn player to match camera when moving forward',)
        detailSizer.AddControl(ctlName = 'AutoMouseLook', ctlType = 'checkbox',
           tooltip = 'Automatically engage mouselook while movement keys are pressed',)
        detailSizer.AddControl(ctlName = 'ChangeCamera', ctlType = 'checkbox',
            tooltip = "Change the camera distance while moving")
        self.Ctrls['ChangeCamera'].Bind(wx.EVT_CHECKBOX, self.OnDetailsCameraChanged)
        detailSizer.AddControl(ctlName = 'CamdistBase', ctlType = 'spinbox', contents = (1, 100),
            tooltip = "Set the camera distance to use while stationary")
        detailSizer.AddControl(ctlName = 'CamdistMove', ctlType = 'spinbox', contents = (1, 100),
            tooltip = "Set the camera distance to use while moving")
        detailSizer.AddControl(ctlName = 'ChangeDetail', ctlType = 'checkbox',
            tooltip = "Change the game's detail level while moving")
        self.Ctrls['ChangeDetail'].Bind(wx.EVT_CHECKBOX, self.OnDetailsCameraChanged)
        detailSizer.AddControl(ctlName = 'DetailBase', ctlType = 'spinboxfractional', contents = (0, 1),
            tooltip = "Set the detail level to use while stationary")
        detailSizer.AddControl(ctlName = 'DetailMove', ctlType = 'spinboxfractional', contents = (0, 1),
            tooltip = "Set the detail level to use while moving")
        self.leftColumn.Add(detailSizer, 0, wx.EXPAND)

        ##### TEMP TRAVEL POWERS
        self.tempSizer = ControlGroup(self, self, 'Temp Travel Powers')
        self.tempSizer.AddControl(ctlName = 'TempEnable', ctlType = 'checkbox',
                                  tooltip = "Enable the Temp Travel Power toggle keybind")
        self.Ctrls['TempEnable'].Bind(wx.EVT_CHECKBOX, self.OnTempChanged)
        self.tempSizer.AddControl(ctlName = 'TempToggle', ctlType = 'keybutton',
                                  tooltip = "Select the key to use to toggle the chosen temp travel power")
        self.Ctrls['TempToggle'].Bind(EVT_KEY_CHANGED, self.OnTempChanged)
        self.TempTravelPowerLabel = wx.StaticText(self.tempSizer.GetStaticBox(), label = "Temp Travel Power:", style = wx.ALIGN_RIGHT)
        self.TempTravelPowerLabel.SetToolTip('Select the temporary travel power to toggle using the keybind')
        self.tempSizer.InnerSizer.Add(self.TempTravelPowerLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        temptravelPowerMenu = self.BuildTempTravelPowerMenu()
        temptravelPowerMenu.Bind(wx.EVT_MENU, self.OnTempTravelPowerPicked)
        self.TempTravelPowerPicker = PowerPicker(self.tempSizer.GetStaticBox(), menu = temptravelPowerMenu, size = wx.Size(230, 40))
        self.TempTravelPowerPicker.SetToolTip('Select the temporary travel power to toggle using the keybind')
        self.TempTravelPowerPicker.DefaultToolTip = 'Select the temporary travel power to toggle using the keybind'
        self.Ctrls['TempTravelPowerPicker'] = self.TempTravelPowerPicker
        self.tempSizer.InnerSizer.Add(self.TempTravelPowerPicker, 1, wx.EXPAND)
        self.leftColumn.Add(self.tempSizer, 0, wx.EXPAND)

        ##### KHELDIAN TRAVEL POWERS
        self.kheldianSizer = ControlGroup(self, self, 'Kheldian Forms / Powers')

        self.kheldianSizer.AddControl(ctlName = 'KhelFeedback', ctlType = 'checkbox',
            tooltip = "Perform a self-/tell when changing form indicating the new form",)
        self.kheldianSizer.AddControl(ctlName = 'UseHumanFormPower', ctlType = 'checkbox',
            tooltip = "Activate shield power when switching to human form",)
        self.kheldianSizer.AddControl(ctlName = 'HumanTray', ctlType = 'spinbox', contents = [1, 9],
            tooltip = "Select the powers tray to change to when in human form")
        self.kheldianSizer.AddControl(ctlName = 'NovaMode', ctlType = 'keybutton',
            tooltip = "Select the key to toggle between Nova and human form")
        self.Ctrls['NovaMode'].Bind(EVT_KEY_CHANGED, self.OnKheldianChanged)
        self.kheldianSizer.AddControl(ctlName = 'NovaTray', ctlType = 'spinbox', contents = [1, 9],
            tooltip = "Select the powers tray to change to when in Nova form")
        self.kheldianSizer.AddControl(ctlName = 'DwarfMode', ctlType = 'keybutton',
            tooltip = "Select the key to toggle between Dwarf and human form")
        self.Ctrls['DwarfMode'].Bind(EVT_KEY_CHANGED, self.OnKheldianChanged)
        self.kheldianSizer.AddControl(ctlName = 'DwarfTray', ctlType = 'spinbox', contents = [1, 9],
            tooltip = "Select the powers tray to change to when in Dwarf form")
        self.rightColumn.Add(self.kheldianSizer, 0, wx.EXPAND)

        ##### SPEED ON DEMAND SETTINGS
        SoDSizer = ControlGroup(self, self, 'Speed on Demand (SoD) Settings')

        SoDSizer.AddControl(ctlName = 'EnableSoD', ctlType = 'checkbox',
            helpfile = 'SpeedonDemand.html',
            tooltip = "Enable Speed on Demand behavior for the movement keys")
        self.Ctrls['EnableSoD'].Bind(wx.EVT_CHECKBOX, self.OnSpeedOnDemandChanged)
        SoDSizer.AddControl(ctlName = 'DefaultMode', ctlType = 'choice',
            contents = ('','Sprint','Speed','Jump','Fly'),
            helpfile = 'SpeedOnDemandModes.html',
            tooltip = "Select the Speed on Demand Mode the movement keys will use by default")
        self.Ctrls['DefaultMode'].Bind(wx.EVT_CHOICE, self.OnSpeedOnDemandChanged)
        SoDSizer.AddControl(ctlName = 'NonSoDMode', ctlType = 'keybutton',
            helpfile = 'SoDToggle.html',
            tooltip = "Select the key to toggle whether Speed on Demand is active")
        SoDSizer.AddControl(ctlName = 'MouseChord', ctlType = 'checkbox',
            tooltip = "Holding both mouse buttons will activate the current Speed on Demand Mode while moving forward")
        SoDSizer.AddControl(ctlName = 'Feedback', ctlType = 'checkbox',
            tooltip = "Announce changes in Speed on Demand Mode via self-/tell")

        self.rightColumn.Add(SoDSizer, 0, wx.EXPAND)

        ##### SPRINT SETTINGS
        SprintSizer = ControlGroup(self, self, 'Sprint Settings')

        SprintSizer.AddControl(ctlName = 'SprintKeyAction', ctlType = 'choice',
            contents = ('Speed on Demand', 'Power Toggle', 'None'),
            helpfile = 'SprintKeyAction.html',
            tooltip = 'Select what the Sprint Power Key will do')
        self.Ctrls['SprintKeyAction'].Bind(wx.EVT_CHOICE, self.OnSprintChanged)
        SprintSizer.AddControl(ctlName = 'SprintPower', ctlType = 'choice',
            contents = GameData.SprintPowers,
            helpfile = 'PreferredSprintPower.html',
            tooltip = "Select the sprint power to use with the keybinds in this section")
        self.Ctrls['SprintPower'].Bind(wx.EVT_CHOICE, self.OnSprintChanged)
        SprintSizer.AddControl(ctlName = 'SprintMode', ctlType = 'keybutton',)

        self.rightColumn.Add(SprintSizer, 0, wx.EXPAND)

        ##### SUPER SPEED
        self.superSpeedSizer = ControlGroup(self, self, 'Super Speed Settings')
        self.superSpeedSizer.AddControl(ctlName = 'SpeedKeyAction', ctlType = 'choice',
            contents = ('Speed on Demand', 'Power Toggle', 'None'),
            helpfile = 'SpeedKeyAction.html',
            tooltip = 'Select what the Speed Power Key will do')
        self.Ctrls['SpeedKeyAction'].Bind(wx.EVT_CHOICE, self.OnSpeedChanged)
        self.superSpeedSizer.AddControl(ctlName = "SpeedPower", ctlType = 'choice',
            contents = ['', 'Speed of Sound', 'Super Speed'],
            tooltip = "Select the super speed power to use with the keybinds in this section")
        self.Ctrls['SpeedPower'].Bind(wx.EVT_CHOICE, self.OnSpeedChanged)
        self.superSpeedSizer.AddControl(ctlName = 'SpeedMode', ctlType = 'keybutton',)
        self.superSpeedSizer.AddControl(ctlName = 'SpeedSpecialKey', ctlType = 'keybutton',)
        self.superSpeedSizer.AddControl(ctlName = 'SSSJModeEnable', ctlType = 'checkbox',
            helpfile = 'SuperSpeedSuperJumpMode.html',
            tooltip = 'Enable Super Speed / Super Jump Mode.')
        self.rightColumn.Add(self.superSpeedSizer, 0, wx.EXPAND)

        ##### SUPER JUMP
        self.superJumpSizer = ControlGroup(self, self, 'Jumping Settings')
        self.superJumpSizer.AddControl(ctlName = 'JumpKeyAction', ctlType = 'choice',
            contents = ('Speed on Demand', 'Power Toggle', 'None'),
            helpfile = 'JumpKeyAction.html',
            tooltip = 'Select what the Jump Power Key will do')
        self.Ctrls['JumpKeyAction'].Bind(wx.EVT_CHOICE, self.OnJumpChanged)
        self.superJumpSizer.AddControl(ctlName = "JumpPower", ctlType = 'choice',
            contents = ['', 'Mighty Leap', 'Super Jump',],
            tooltip = "Select the primary jump power to use with the keybinds in this section")
        self.Ctrls['JumpPower'].Bind(wx.EVT_CHOICE, self.OnJumpChanged)
        self.superJumpSizer.AddControl(ctlName = 'CJPower', ctlType = 'choice', contents = ['', 'Combat Jumping'],
            tooltip = "Select the defensive jump power to use with the keybinds in this section")
        self.superJumpSizer.AddControl(ctlName = 'JumpMode', ctlType = 'keybutton',)
        self.superJumpSizer.AddControl(ctlName = 'JumpSpecialKey', ctlType = 'keybutton',)
        self.rightColumn.Add(self.superJumpSizer, 0, wx.EXPAND)

        ##### FLY
        self.flySizer = ControlGroup(self, self, 'Flight Settings')
        self.flySizer.AddControl(ctlName = 'FlyKeyAction', ctlType = 'choice',
            contents = ('Speed on Demand', 'Power Toggle', 'None'),
            helpfile = 'FlyKeyAction.html',
            tooltip = 'Select what the Fly Power Key will do')
        self.Ctrls['FlyKeyAction'].Bind(wx.EVT_CHOICE, self.OnFlightChanged)
        self.flySizer.AddControl(ctlName = "FlyPower", ctlType = 'choice',
            contents = ['', 'Fly', 'Mystic Flight',],
            tooltip = "Select the primary flight power to use with the keybinds in this section")
        self.Ctrls['FlyPower'].Bind(wx.EVT_CHOICE, self.OnFlightChanged)
        self.flySizer.AddControl(ctlName = 'HoverPower', ctlType = 'choice', contents = ['', 'Hover', 'Combat Flight'],
            tooltip = "Select the defensive flight power to use with the keybinds in this section")
        self.Ctrls['HoverPower'].Bind(wx.EVT_CHOICE, self.OnFlightChanged)
        self.flySizer.AddControl(ctlName = 'FlyMode', ctlType = 'keybutton',)
        self.flySizer.AddControl(ctlName = 'FlySpecialKey', ctlType = 'keybutton',)
        self.flySizer.AddControl(ctlName = 'GFlyMode', ctlType = 'keybutton',
            tooltip = "Toggle Group Fly Speed on Demand Mode")
        self.rightColumn.Add(self.flySizer, 0, wx.EXPAND)

        ##### TELEPORT
        self.teleportSizer = ControlGroup(self, self, 'Teleport Settings')
        self.teleportSizer.AddControl(ctlName = "TPPower", ctlType = 'choice',
            contents = ['', 'Teleport', 'Jaunt', 'Shadow Step', 'White Dwarf Step', 'Black Dwarf Step'],
            tooltip = "Select the teleport power to use with the keybinds in this section")
        self.Ctrls['TPPower'].Bind(wx.EVT_CHOICE, self.OnTeleportChanged)
        if server == "Homecoming":
            tpTooltip = 'Immediately teleport to the cursor position without showing a target marker.'
            tpcTooltip = 'Show target marker on keypress;  teleport to marker on key release.'
        else:
            tpTooltip = 'Show target marker on keypress;  teleport to marker on key release.'
            tpcTooltip = 'Show target marker on keypress;  click to teleport.'
        self.teleportSizer.AddControl(ctlName = "TPBindKey", ctlType = 'keybutton', tooltip = tpTooltip)
        self.teleportSizer.AddControl(ctlName = "TPComboKey", ctlType = 'keybutton', tooltip = tpcTooltip)
        self.Ctrls['TPComboKey'].Bind(EVT_KEY_CHANGED, self.OnTPComboKey)
        self.teleportSizer.AddControl(ctlName = "TPExecuteKey", ctlType = 'keybutton')
        self.teleportSizer.AddControl(ctlName = 'TPTPHover', ctlType = 'checkbox',
            tooltip = "Activate the Hover power after teleporting")
        if server == "Homecoming":
            ttpTooltip = "Immediately Team Teleport to the cursor position without showing a target marker."
            ttpcTooltip = "Show target marker on keypress;  Team Teleport to marker on key release."
        else:
            ttpTooltip = "Show target marker on keypress;  Team Teleport to marker on key release."
            ttpcTooltip = "Show target marker on keypress;  click to team teleport."
        self.teleportSizer.AddControl(ctlName = "TTPBindKey", ctlType = 'keybutton', tooltip = ttpTooltip)
        self.teleportSizer.AddControl(ctlName = "TTPComboKey", ctlType = 'keybutton', tooltip = ttpcTooltip)
        self.Ctrls['TTPComboKey'].Bind(EVT_KEY_CHANGED, self.OnTTPComboKey)
        self.teleportSizer.AddControl(ctlName = "TTPExecuteKey", ctlType = 'keybutton')
        self.teleportSizer.AddControl(ctlName = 'TTPTPGFly', ctlType = 'checkbox',
            tooltip = "Activate the Group Fly power after Team Teleporting")
        self.teleportSizer.AddControl(ctlName = 'TPHideWindows', ctlType = 'checkbox',
            tooltip = 'Hide most UI elements while holding target marker key.', )
        self.rightColumn.Add(self.teleportSizer, 0, wx.EXPAND)

        topSizer.Add(self.leftColumn , 0, wx.ALL, 3)
        topSizer.Add(self.rightColumn, 0, wx.ALL, 3)

        self.MainSizer.Add(topSizer, flag = wx.ALL|wx.ALIGN_CENTER_HORIZONTAL)

    def ShowControlGroup(self, group, show = True) -> None:
        if self.rightColumn.GetItem(group):
            self.rightColumn.Show(group, show)
        elif self.leftColumn.GetItem(group):
            self.leftColumn.Show(group, show)
        else:
            wx.LogError(f"Tried to show/hide ControlGroup {group} which is in neither column.  This is a bug.")
            return
        group.EnableCtrls(show)

    def OnTPComboKey(self, evt = None) -> None:
        ComboKey = self.GetState('TPComboKey')
        self.Ctrls['TPExecuteKey'].SetLabel(ComboKey + "+BUTTON1")
        if evt: evt.Skip()

    def OnTTPComboKey(self, evt = None) -> None:
        ComboKey = self.GetState('TTPComboKey')
        self.Ctrls['TTPExecuteKey'].SetLabel(ComboKey + "+BUTTON1")
        if evt: evt.Skip()

    def OnDetailsCameraChanged(self, evt = None) -> None:
        c = self.Ctrls
        c['CamdistBase'].Enable(self.GetState('ChangeCamera'))
        c['CamdistMove'].Enable(self.GetState('ChangeCamera'))

        c['DetailBase'].Enable(self.GetState('ChangeDetail'))
        c['DetailMove'].Enable(self.GetState('ChangeDetail'))
        if evt: evt.Skip()

    def OnSpeedOnDemandChanged(self, evt = None) -> None:
        c = self.Ctrls
        sodmode = self.DefaultMode()
        c['NonSoDMode'].Show(bool(sodmode)) # Hide the "turn off SoD" key if "No SoD" is the default.
        for ctrl in ['DefaultMode', 'NonSoDMode', 'MouseChord', 'Feedback', ]:
            c[ctrl].Enable(self.SoDEnabled())
        for ctrl in ['SprintKeyAction', 'JumpKeyAction', 'FlyKeyAction', 'SpeedKeyAction', ]:
            c[ctrl].ShowEntryIf('Speed on Demand', self.SoDEnabled())
            # Reset these pickers to saved state in case we just reappeared their desired value.  Might be bad.
            c[ctrl].SetStringSelection(self.Profile.Data.get('MovementPowers', {}).get(ctrl, self.Init[ctrl] or ''))
        wx.CallAfter(self.OnSprintChanged)
        wx.CallAfter(self.OnJumpChanged)
        wx.CallAfter(self.OnSpeedChanged)
        wx.CallAfter(self.OnFlightChanged)
        wx.CallAfter(self.OnTeleportChanged)
        if evt: evt.Skip()

    def OnSprintChanged(self, evt = None):
        c = self.Ctrls
        c['DefaultMode'].ShowEntryIf('Sprint', self.GetKeyAction('Sprint') == ACTION_SOD)
        c['SprintMode'].Show(self.DefaultMode() != "Sprint")
        c['SprintMode'].Enable(bool(self.GetKeyAction('Sprint')))

        c['SprintKeyAction'].CtlLabel.SetLabel('Sprint Powers Mode:' if self.DefaultMode() == 'Sprint' else 'Sprint Key Action:')

        c['SprintMode'].SetToolTip({
            ACTION_SOD :  'Toggle Sprint Speed on Demand Mode',
            ACTION_PT  : f'Toggle {c['SprintPower'].GetStringSelection()} on and off',
        }.get(self.GetKeyAction('Sprint'), ''))

        self.Fit()
        self.Layout()
        if evt: evt.Skip()

    def OnSpeedChanged(self, evt = None) -> None:
        c = self.Ctrls
        if (self.Profile.HasPower('Speed', 'Super Speed') or self.Profile.HasPower('Experimentation', 'Speed of Sound')):
            c['DefaultMode'].ShowEntryIf('Speed', self.GetKeyAction('Speed') == ACTION_SOD)
            self.ShowControlGroup(self.superSpeedSizer)
            c['SpeedPower'].ShowEntryIf('Super Speed',    self.Profile.HasPower('Speed', 'Super Speed'))
            c['SpeedPower'].ShowEntryIf('Speed of Sound', self.Profile.HasPower('Experimentation', 'Speed of Sound'))
            c['SpeedPower'].Enable(bool(self.GetKeyAction('Speed')))
            c['SpeedMode'].Show(self.DefaultMode() != "Speed")
            c['SpeedMode'].Enable(bool(self.GetKeyAction('Speed')))
            c['SSSJModeEnable'].Show(self.rightColumn.IsShown(self.superJumpSizer))
            c['SSSJModeEnable'].Enable(self.SoDEnabled())


            c['SpeedKeyAction'].CtlLabel.SetLabel('Speed Powers Mode:' if self.DefaultMode() == 'Speed' else 'Speed Key Action:')

            c['SpeedMode'].SetToolTip({
                ACTION_SOD :  'Toggle Super Speed Speed on Demand Mode',
                ACTION_PT  : f'Toggle {c['SpeedPower'].GetStringSelection()} on and off',
            }.get(self.GetKeyAction('Speed'), ''))

            if (self.GetState('SpeedPower') == "Super Speed"):
                c['SpeedSpecialKey'].CtlLabel.SetLabel('Speed Phase:')
                c['SpeedSpecialPower'].SetValue('SpeedPhase')
                c['SpeedSpecialKey'].Show()
                c['SpeedSpecialKey'].SetToolTip('Select the key that will activate Speed Phase')
            else:
                c['SpeedSpecialKey'].Show(False)

            wx.CallAfter(self.OnTeleportChanged) # set up "Jaunt" as TP power if 'Speed of Sound'
        else:
            self.ShowControlGroup(self.superSpeedSizer, False)
            c['DefaultMode'].ShowEntryIf('Speed', False)

        self.Fit()
        self.Layout()
        if evt: evt.Skip()

    def OnJumpChanged(self, evt = None) -> None:
        c = self.Ctrls
        if (self.Profile.HasPower('Leaping', 'Super Jump') or self.Profile.HasPower('Force of Will', 'Mighty Leap')):
            c['DefaultMode'].ShowEntryIf('Jump', self.GetKeyAction('Jump') == ACTION_SOD)
            self.ShowControlGroup(self.superJumpSizer)
            c['JumpPower'].ShowEntryIf('Super Jump',  self.Profile.HasPower('Leaping', 'Super Jump'))
            c['JumpPower'].ShowEntryIf('Mighty Leap', self.Profile.HasPower('Force of Will', 'Mighty Leap'))
            c['JumpPower'].Enable(bool(self.GetKeyAction('Jump')))

            c['CJPower'].ShowEntryIf('Combat Jumping', self.Profile.HasPower('Leaping', 'Combat Jumping'))
            c['CJPower'].Show  (bool(self.GetKeyAction('Jump')) and c['CJPower'].GetCount() > 1)
            c['CJPower'].Enable(bool(self.GetKeyAction('Jump')) and c['CJPower'].GetCount() > 1)

            c['JumpKeyAction'].CtlLabel.SetLabel('Jump Powers Mode:' if self.DefaultMode() == 'Jump' else 'Jump Key Action:')

            c['JumpMode'].Show(self.DefaultMode() != "Jump")
            c['JumpMode'].Enable(bool(self.GetKeyAction('Jump')))
            c['SSSJModeEnable'].Show(bool(self.GetState('SpeedPower')))
            c['SSSJModeEnable'].Enable(self.SoDEnabled())

            c['JumpMode'].SetToolTip({
                ACTION_SOD : 'Toggle Jump Speed on Demand Mode',
                ACTION_PT : f'Toggle {c['JumpPower'].GetStringSelection()} on and off',
            }.get(self.GetKeyAction('Jump'), ''))

            if (self.GetState('JumpPower') == "Mighty Leap"):
                c['JumpSpecialKey'].CtlLabel.SetLabel('Takeoff:')
                c['JumpSpecialPower'].SetValue('Takeoff')
                c['JumpSpecialKey'].Show()
                c['JumpSpecialKey'].SetToolTip('Activate Takeoff')
            elif (self.GetState('JumpPower') == "Super Jump"):
                c['JumpSpecialKey'].CtlLabel.SetLabel('Double Jump:')
                c['JumpSpecialPower'].SetValue('Double_Jump')
                c['JumpSpecialKey'].Show()
                c['JumpSpecialKey'].SetToolTip('Activate Double Jump')
            else:
                c['JumpSpecialKey'].Show(False)
        else:
            self.ShowControlGroup(self.superJumpSizer, False)
            c['DefaultMode'].ShowEntryIf('Jump', False)

        self.Fit()
        self.Layout()
        if evt: evt.Skip()

    def OnFlightChanged(self, evt = None) -> None:
        c = self.Ctrls
        archetype = self.Profile.Archetype()
        flyusessod = self.GetKeyAction('Fly') == ACTION_SOD

        if (self.Profile.HasPower('Flight', 'Fly')
                    or self.Profile.HasPower('Sorcery', 'Mystic Flight')
                    or archetype == "Peacebringer"):
            c['DefaultMode'].ShowEntryIf('Fly', flyusessod)
            self.ShowControlGroup(self.flySizer)

            c['FlyPower'].ShowEntryIf("Fly",           self.Profile.HasPower("Flight", 'Fly'))
            c['FlyPower'].ShowEntryIf("Mystic Flight", self.Profile.HasPower("Sorcery", 'Mystic Flight'))
            c['FlyPower'].ShowEntryIf("Energy Flight", archetype == "Peacebringer")
            c['FlyPower'].Enable(bool(self.GetKeyAction('Fly')))

            c['FlyKeyAction'].CtlLabel.SetLabel('Fly Powers Mode:' if self.DefaultMode() == 'Fly' else 'Fly Key Action:')

            c['HoverPower'].ShowEntryIf('Hover',         self.Profile.HasPower('Flight', 'Hover'))
            c['HoverPower'].ShowEntryIf('Combat Flight', archetype == "Peacebringer")
            c['HoverPower'].Show  (bool(self.GetKeyAction('Fly')) and c['HoverPower'].GetCount() > 1)
            c['HoverPower'].Enable(bool(self.GetKeyAction('Fly')) and c['HoverPower'].GetCount() > 1)

            c['FlyMode'].Show(bool(self.GetState('FlyPower') or self.GetState('HoverPower')) and self.DefaultMode() != "Fly")
            c['FlyMode'].Enable(bool(self.GetKeyAction('Fly')))

            c['FlyMode'].SetToolTip({
                ACTION_SOD : 'Toggle Fly Speed on Demand Mode',
                ACTION_PT : f'Toggle {c['FlyPower'].GetStringSelection()} on and off',
            }.get(self.GetKeyAction('Fly'), ''))

            c['FlySpecialKey'].Show(False) # turn it off and then check to see if we want it
            if (self.GetState('FlyPower') == "Fly"):
                # "fly_boost" below because "afterburner" has overloaded meaning in-game and reacts
                # weirdly (ie, fires the wrong power) if Afterburner isn't on a visible button
                # https://github.com/emersonrp/bindcontrol/issues/80#issuecomment-2585719489
                c['FlySpecialPower'].SetValue('fly_boost')
                c['FlySpecialKey'].CtlLabel.SetLabel('Afterburner:')
                c['FlySpecialKey'].SetToolTip('Activate Afterburner')
                c['FlySpecialKey'].Show()

            # This next condition forces this to be Quantum Maneuvers for Peacebringers who
            # for some reason take Flight and want "Fly" as Primary but "Combat Flight" as
            # Defensive.  Almost certainly nobody does this.  Almost.
            if (archetype == "Peacebringer" and ((self.GetState('FlyPower') == 'Energy Flight') or self.GetState('HoverPower') == 'Combat Flight')):
                c['FlySpecialPower'].SetValue('Quantum Maneuvers')
                c['FlySpecialKey'].CtlLabel.SetLabel('Quantum Maneuvers:')
                c['FlySpecialKey'].SetToolTip('Activate Quantum Maneuvers')
                c['FlySpecialKey'].Show()

            c['GFlyMode'].Show(self.HasGFly())

            wx.CallAfter(self.OnTeleportChanged) # in case we did something with 'Hover' and need to update TPHover
        else:
            self.ShowControlGroup(self.flySizer, False)
            c['DefaultMode'].ShowEntryIf('Fly', False)

        self.Fit()
        self.Layout()
        if evt: evt.Skip()

    def OnTeleportChanged(self, evt = None) -> None:
        c = self.Ctrls
        if (self.HasTP()):
            self.ShowControlGroup(self.teleportSizer)
            c['TPPower'].ShowEntryIf('Teleport',         self.Profile.HasPower('Teleportation', 'Teleport'))
            c['TPPower'].ShowEntryIf('Translocation',    self.Profile.HasPower('Sorcery', 'Translocation'))
            c['TPPower'].ShowEntryIf('Jaunt',            self.GetState('SpeedPower') == "Speed of Sound")
            c['TPPower'].ShowEntryIf('Shadow Step',      self.Profile.Archetype() == "Warshade")
            c['TPPower'].ShowEntryIf('Black Dwarf Step', self.Profile.Archetype() == "Warshade")
            c['TPPower'].ShowEntryIf('White Dwarf Step', self.Profile.Archetype() == "Peacebringer")

            c['TPBindKey']    .Enable(bool(self.GetState('TPPower')))
            c['TPComboKey']   .Enable(bool(self.GetState('TPPower')))
            c['TPTPHover']    .Show(       c['HoverPower'].IsEnabled())
            c['TPTPHover']    .Enable(bool(c['HoverPower'].IsEnabled() and self.GetState('TPPower')))
            c['TPHideWindows'].Enable(bool(self.GetState('TPPower')))

            c['TTPBindKey'] .Show(self.HasTTP())
            c['TTPComboKey'].Show(self.HasTTP())
            c['TTPTPGFly']  .Show(self.HasTTP() and self.HasGFly())

            # The two 'execute' keys are always hidden as they are magical.
            # They are only for the complicated Rebirth Combo Teleport scheme and might
            # be able to be completely hidden behind "if server" logic eventually.
            c['TPExecuteKey'].Show(False)
            c['TTPExecuteKey'].Show(False)
        else:
            self.ShowControlGroup(self.teleportSizer, False)

        self.Fit()
        self.Layout()
        if evt: evt.Skip()

    def OnKheldianChanged(self, evt = None) -> None:
        c = self.Ctrls
        if (self.IsKheldian()):
            # show kheldian sizer, enable controls
            self.ShowControlGroup(self.kheldianSizer)

            c['UseHumanFormPower'].Show(  self.Profile.Server() != 'Homecoming')
            c['UseHumanFormPower'].Enable(self.Profile.Server() != 'Homecoming')

            c['NovaMode'].Enable()
            c['NovaTray'].Enable(bool(self.GetState('NovaMode')))
            c['DwarfMode'].Enable()
            c['DwarfTray'].Enable(bool(self.GetState('DwarfMode')))
        else:
            self.ShowControlGroup(self.kheldianSizer, False)
        if evt: evt.Skip()

    def OnTempChanged(self, evt = None) -> None:
        enabled = bool(self.GetState('TempEnable'))

        tt = self.Ctrls['TempToggle']
        tt.Enable(enabled)
        self.TempTravelPowerLabel.Enable(enabled)
        self.TempTravelPowerPicker.Enable(enabled)
        # this reaches down and touches up Profile.Data
        self.TempTravelPowerPicker.doOnMenuSelected()
        if enabled and not tt.GetLabel():
            tt.AddError('unset', 'No Temp Travel Power BindKey has been set.')
        else:
            tt.RemoveError('unset')

        if evt: evt.Skip()

    def OnTempTravelPowerPicked(self, evt) -> None:
        menu = evt.GetEventObject()
        menuitem = menu.FindItemById(evt.GetId())
        self.TempTravelPowerPicker.SetLabel (menuitem.GetItemLabel())
        self.TempTravelPowerPicker.SetBitmap(menuitem.GetBitmapBundle())
        setattr(self.TempTravelPowerPicker, 'IconFilename', getattr(menuitem, 'IconFilename'))
        evt.Skip()

    def BuildTempTravelPowerMenu(self) -> wx.Menu:
        menu = wx.Menu()
        for item in GameData.TempTravelPowers:
            if re.search(r'\|', item):
                item, iconname = re.split(r'\|', item)
            else:
                iconname = item
            menuitem = wx.MenuItem(id = wx.ID_ANY, text = item)

            if icon := GetIcon('Powers', 'Temp', iconname):
                menuitem.SetBitmap(icon)
                setattr(menuitem, 'IconFilename', icon.Filename)

            menu.Append(menuitem)
        return menu

    def SynchronizeUI(self, evt = None) -> None:
        self.OnDetailsCameraChanged()

        self.OnTempChanged()

        self.OnKheldianChanged()

        self.OnSpeedOnDemandChanged() # does all of the others

        self.Fit()

        self.Layout()

        if evt: evt.Skip()

    ##################
    ### Bindfile Stuff
    ##################

    def MakeSoDFile(self, params: dict) -> None:

        profile = self.Profile

        t      = params['t']
        suffix = params.get('suffix', '')

        bl        = t.bl      (      suffix)
        path      = t.path    (      suffix)
        gamepath  = t.gamepath(      suffix)
        bla       = t.bl      ('a' + suffix)
        patha     = t.path    ('a' + suffix)
        gamepatha = t.gamepath('a' + suffix)
        blf       = t.bl      ('f' + suffix)
        pathf     = t.path    ('f' + suffix)
        gamepathf = t.gamepath('f' + suffix)

        mobile     = params.get('mobile')
        stationary = params.get('stationary')
        modestr    = params.get('modestr')

        flight     = params.get('flight' , '')
        sssj       = params.get('sssj'   , '')
        usejumpfix = modestr == 'Jump'

        # I believe we're setting the default mode's key to the current
        # mode's key so that pressing the current mode's key while it's
        # already active will toggle us back to default mode
        setattr(t, self.DefaultMode() + 'ModeKey', params['key'])

        # if our current context is the Default Mode, and we're 000000,
        # write the keybinds to the reset file.
        if ((self.DefaultMode() == modestr) and (t.totalkeys == 0)):
            resetfile = profile.ResetFile()

            self.SoDUpKey     (t, bl , resetfile, mobile, stationary, flight, sssj = sssj)
            self.SoDDownKey   (t, bl , resetfile, mobile, stationary, flight)
            self.SoDForwardKey(t, bl , resetfile, mobile, stationary, flight, sssj = sssj)
            self.SoDBackKey   (t, bl , resetfile, mobile, stationary, flight, sssj = sssj)
            self.SoDLeftKey   (t, bl , resetfile, mobile, stationary, flight, sssj = sssj)
            self.SoDRightKey  (t, bl , resetfile, mobile, stationary, flight, sssj = sssj)
            self.SoDAutoRunKey(t, bla, resetfile, mobile, sssj)
            self.SoDFollowKey (t, blf, resetfile, mobile, stationary)

            if (modestr != "NonSoD")      : self.MakeNonSoDModeKey(t,"r", resetfile)
            if (modestr != "Sprint")      : self.MakeSprintModeKey(t,"r", resetfile,usejumpfix)
            if (modestr != "Fly")         : self.MakeFlyModeKey   (t,"f", resetfile,usejumpfix)
            if (modestr != "Super Speed") : self.MakeSpeedModeKey (t,"s", resetfile,usejumpfix, sssj = sssj)
            if (modestr != "Jump")        : self.MakeJumpModeKey  (t,"j", resetfile,path,gamepath)

            if (modestr != "GFly")        : self.MakeGFlyModeKey  (t,"gf",resetfile,usejumpfix)

        ### write the binds to the "current path/context + current key state" file
        curfile = profile.GetBindFile(f"{path}{t.KeyState()}.txt")

        self.SoDResetKey(curfile)

        self.SoDUpKey     (t,bl,curfile,mobile,stationary,flight,sssj = sssj)
        self.SoDDownKey   (t,bl,curfile,mobile,stationary,flight)
        self.SoDForwardKey(t,bl,curfile,mobile,stationary,flight,sssj = sssj)
        self.SoDBackKey   (t,bl,curfile,mobile,stationary,flight,sssj = sssj)
        self.SoDLeftKey   (t,bl,curfile,mobile,stationary,flight,sssj = sssj)
        self.SoDRightKey  (t,bl,curfile,mobile,stationary,flight,sssj = sssj)

        if (modestr != "NonSoD")      : self.MakeNonSoDModeKey(t,"r", curfile,)
        if (modestr != "Sprint")      : self.MakeSprintModeKey(t,"r", curfile,usejumpfix)
        # Not clear what's going on here;  maybe I messed it up.  Anyway, these two are
        # exactly the same except for feedback == True
        if (flight == "Jump"):
            if (modestr != "Fly")     : self.MakeFlyModeKey   (t,"f", curfile,usejumpfix,True)
        else:
            if (modestr != "Fly")     : self.MakeFlyModeKey   (t,"f", curfile,usejumpfix)
        if (modestr != "Super Speed") : self.MakeSpeedModeKey (t,"s", curfile,usejumpfix, sssj = sssj)
        if (modestr != "Jump")        : self.MakeJumpModeKey  (t,"j", curfile,path,gamepath)

        self.SoDAutoRunKey(t,bla,curfile,mobile,sssj)
        self.SoDFollowKey (t,blf,curfile,mobile,stationary)

        # Autorun Binds
        autorunfile = profile.GetBindFile(f"{patha}{t.KeyState()}.txt")

        self.SoDResetKey(autorunfile)

        self.SoDUpKey     (t,bla,autorunfile,mobile,stationary,flight,autorun=True, sssj = sssj)
        self.SoDDownKey   (t,bla,autorunfile,mobile,stationary,flight,autorun=True)
        self.SoDForwardKey(t,bla,autorunfile,mobile,stationary,flight,autorunbl=bl, sssj = sssj)
        self.SoDBackKey   (t,bla,autorunfile,mobile,stationary,flight,autorunbl=bl, sssj = sssj)
        self.SoDLeftKey   (t,bla,autorunfile,mobile,stationary,flight,autorun=True, sssj = sssj)
        self.SoDRightKey  (t,bla,autorunfile,mobile,stationary,flight,autorun=True, sssj = sssj)

        if (modestr != "NonSoD")      : self.MakeNonSoDModeKey(t,"ar",autorunfile)
        if (modestr != "Sprint")      : self.MakeSprintModeKey(t,"gr",autorunfile,usejumpfix)
        if (modestr != "Super Speed") : self.MakeSpeedModeKey (t,"as",autorunfile,usejumpfix, sssj = sssj)
        if (modestr != "Fly")         : self.MakeFlyModeKey   (t,"af",autorunfile,usejumpfix)
        if (modestr != "Jump")        : self.MakeJumpModeKey  (t,"aj",autorunfile,patha,gamepatha)

        self.SoDAutoRunOffKey(t,bl,autorunfile,mobile,stationary,flight)
        autorunfile.SetBind(self.Ctrls['Follow'].MakeBind('nop'))

        # Follow Binds
        followfile = profile.GetBindFile(f"{pathf}{t.KeyState()}.txt")

        self.SoDResetKey(followfile)

        self.SoDUpKey     (t,blf,followfile,mobile,stationary,flight,followbl = bl,sssj = sssj)
        self.SoDDownKey   (t,blf,followfile,mobile,stationary,flight,followbl = bl)
        self.SoDForwardKey(t,blf,followfile,mobile,stationary,flight,followbl = bl,sssj = sssj)
        self.SoDBackKey   (t,blf,followfile,mobile,stationary,flight,followbl = bl,sssj = sssj)
        self.SoDLeftKey   (t,blf,followfile,mobile,stationary,flight,followbl = bl,sssj = sssj)
        self.SoDRightKey  (t,blf,followfile,mobile,stationary,flight,followbl = bl,sssj = sssj)

        if (modestr != "NonSoD")      : self.MakeNonSoDModeKey(t,"fr",followfile)
        if (modestr != "Sprint")      : self.MakeSprintModeKey(t,"fr",followfile,usejumpfix)
        if (modestr != "Super Speed") : self.MakeSpeedModeKey (t,"fs",followfile,usejumpfix, sssj = sssj)
        if (modestr != "Fly")         : self.MakeFlyModeKey   (t,"ff",followfile,usejumpfix)
        if (modestr != "Jump")        : self.MakeJumpModeKey  (t,"fj",followfile,pathf,gamepathf)

        self.SoDFollowOffKey(t,bl,followfile,mobile,stationary,flight)
        followfile.SetBind(self.Ctrls['AutoRun'].MakeBind('nop'))

        setattr(t, self.DefaultMode() + 'ModeKey', None)

    def MakeNonSoDModeKey(self, t, bl, file, usejumpfix = False, skipfeedback = False) -> None:
        key = t.NonSoDModeKey
        name = UI.Labels['NonSoDMode']
        if not self.Ctrls['NonSoDMode'].IsEnabled(): return
        if not key: return

        togoff = self.OtherMovementPowers('n')

        if (not skipfeedback) and self.GetState('Feedback'): feedback = '$$t $name, Non-SoD Mode'
        else:                                      feedback = ''

        if (bl == "r"):
            bindload = t.BLF('n')
            if usejumpfix:
                self.SoDJumpFix(t,key, self.MakeNonSoDModeKey,"n",bl,file,feedback = feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(None,togoff) + t.dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload = t.BLF('an')
            if usejumpfix:
                self.SoDJumpFix(t,key, self.MakeNonSoDModeKey,"n",bl,file,"a",feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(None,togoff) + t.detailhi + t.runcamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if usejumpfix:
                self.SoDJumpFix(t,key, self.MakeNonSoDModeKey,"n",bl,file,"f",feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(None,togoff) + t.detailhi + t.runcamdist + '$$up 0' + feedback + t.BLF('fn'))
        t.ini = ''

    def MakeSprintModeKey(self, t, bl, file, usejumpfix = False, skipfeedback = False, doingtoggle = False) -> None:
        key = t.SprintModeKey
        name = UI.Labels['SprintMode']
        if not key: return

        if (not skipfeedback) and self.GetState('Feedback'): feedback = '$$t $name, Sprint-SoD Mode'
        else:                                      feedback = ''

        if istoggle := self.GetKeyAction('Sprint') == ACTION_PT:
            code   = 'n'
            togoff = self.AllSoDPowers() if doingtoggle else ''
        else: # is SoD
            code   = 'r'
            togoff = self.OtherMovementPowers('r')
        dotogglefix = istoggle and not doingtoggle

        if (bl == "r"):
            bindload  = t.BLF(code)

            if dotogglefix:
                self.SoDToggleFix(t, key, self.MakeSprintModeKey, code, bl, file, feedback = feedback)
            elif usejumpfix:
                self.SoDJumpFix  (t, key, self.MakeSprintModeKey, "r",  bl, file, feedback = feedback)
            else:
                if t.horizkeys: sprint = t.sprint
                else:           sprint = ''

                file.SetBind(key, name, self, t.ini + self.actPower_toggle(sprint, togoff, start = True) + t.dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t.BLF('a' + code)
            if dotogglefix:
                self.SoDToggleFix(t, key, self.MakeSprintModeKey, code, bl, file, "a", feedback)
            elif usejumpfix:
                self.SoDJumpFix(  t, key, self.MakeSprintModeKey, "r",  bl, file, "a", feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.sprint, togoff, start=True) + '$$up 0' + t.detailhi +  t.runcamdist + t.dirs('DLR') + feedback + bindload)

        else: # bl = 'fr'
            bindload = t.BLF('f' + code)
            if dotogglefix:
                self.SoDToggleFix(t, key, self.MakeSprintModeKey, code, bl, file, "f", feedback)
            elif usejumpfix:
                self.SoDJumpFix(  t, key, self.MakeSprintModeKey, "r",  bl, file, "f", feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.sprint, togoff, start=True) + '$$up 0' + t.detailhi + t.runcamdist + feedback + bindload)

        t.ini = ''

    def MakeSpeedModeKey(self, t, bl, file, usejumpfix = False, skipfeedback = False, doingtoggle = False, sssj = '') -> None:
        if not self.Ctrls['SpeedMode'].IsEnabled(): return

        key = t.SpeedModeKey
        name = UI.Labels['SpeedMode']

        # sssj mode forces us to differentiate between 'code' for X/X00000 and 'suffix' for 000000x.txt'
        if istoggle := self.GetKeyAction('Speed') == ACTION_PT:
            code   = 's' if sssj else 'n' # use sod-style movement keybinds if sssj to turn jumping on/off
            suffix = ''  if sssj else 'n'
            togoff = self.AllSoDPowers() if doingtoggle else ''
        else: # is SoD
            code   = 's'
            suffix = 's'
            togoff = self.OtherMovementPowers('s')
        dotogglefix = istoggle and not doingtoggle

        feedback = ''
        if (not skipfeedback) and self.GetState('Feedback'): feedback = '$$t $name, Superspeed Mode'

        if (self.GetState('SpeedPower')):
            if (bl == 's'):
                bindload  = t.BLF(code)
                if dotogglefix:
                    self.SoDToggleFix(t, key, self.MakeSpeedModeKey, suffix, bl, file, feedback, sssj = sssj)
                elif usejumpfix:
                    self.SoDJumpFix  (t, key, self.MakeSpeedModeKey, suffix, bl, file, feedback)
                else:
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(None, togoff, start=True) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "as"):
                bindload  = t.BLF('a' + code)
                if dotogglefix:
                    self.SoDToggleFix(t, key, self.MakeSpeedModeKey, suffix, bl, file, "a", feedback, sssj = sssj)
                elif usejumpfix:
                    self.SoDJumpFix  (t, key, self.MakeSpeedModeKey, suffix, bl, file, "a", feedback)
                else:
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(None, togoff, start=True) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload)

            else:  # bl == "fs"
                bindload  = t.BLF('f' + code)
                if dotogglefix:
                    self.SoDToggleFix(t, key, self.MakeSpeedModeKey, suffix, bl, file, "f", feedback, sssj = sssj)
                elif usejumpfix:
                    self.SoDJumpFix  (t, key, self.MakeSpeedModeKey, suffix, bl, file, "f", feedback)
                else:
                    bindload  = t.BLF('f' + code)
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(None, togoff, start=True) + '$$up 0' +  t.detaillo + t.flycamdist + feedback + bindload)

        t.ini = ''

    def MakeJumpModeKey(self, t, bl, file, fpath, fbl, doingtoggle = False) -> None:
        if not self.Ctrls['JumpMode'].IsEnabled(): return
        p = self.Profile
        key = t.JumpModeKey
        name = UI.Labels['JumpMode']

        if (t.canjmp and bool(self.GetKeyAction('Jump'))):

            if istoggle := (self.GetKeyAction('Jump') == ACTION_PT):
                togoff = self.actPower_toggle(None, self.AllSoDPowers()) if doingtoggle else ''
            else:
                togoff = self.actPower_toggle(None, self.OtherMovementPowers('j'))

            feedback = '$$t $name, Super Jump Mode' if self.GetState('Feedback') else ''

            # tglbl is the BLF() for the toggle file
            # tgl is the bindfile itself
            tglbl =       f"$${BLF()} {fbl}{t.KeyState()}j.txt"
            tgl   = p.GetBindFile(f"{fpath}{t.KeyState()}j.txt")

            if (bl == "j"):
                # if we're moving, turn on jump;  if stationary, turn on combat jumping
                if (t.horizkeys + t.space > 0):
                    a = self.actPower_name(None, {t.cjmp, t.jump}) + '$$up 1'
                else:
                    a = self.actPower_name(None, {t.jump, t.cjmp})

                tgl.SetBind(key, name, self, '-down' + a + togoff + t.detaillo + t.flycamdist + t.BLF('n' if istoggle else 'j'))
                file.SetBind(key, name, self, '+down' + feedback + tglbl)

            elif (bl == "aj"):
                ajbl = t.BLF('an' if istoggle else 'aj')
                tgl.SetBind(key, name, self, '-down' + self.actPower_name(t.jump) + togoff + '$$up 1' + t.detaillo + t.flycamdist + t.dirs('DLR') + ajbl)
                file.SetBind(key, name, self, '+down' + feedback + tglbl)

            else: # bl == fj
                fjbl = t.BLF('fn' if istoggle else 'fj')
                tgl.SetBind(key, name, self, '-down' + self.actPower_name(t.jump) + togoff + '$$up 1' + t.detaillo + t.flycamdist + fjbl)
                file.SetBind(key, name, self, '+down' + feedback + tglbl)

        t.ini = ''

    def MakeFlyModeKey(self, t, bl, file, usejumpfix = False, skipfeedback = False, fb_on_a = False, doingtoggle = False) -> None:
        if not self.Ctrls['FlyMode'].IsEnabled(): return
        key = t.FlyModeKey
        name = UI.Labels['FlyMode']

        if (not skipfeedback) and self.GetState('Feedback'): feedback = '$$t $name, Flight Mode'
        else:                                      feedback = ''

        if istoggle := (self.GetKeyAction('Fly') == ACTION_PT):
            code   = 'n'
            togoff = self.AllSoDPowers() if doingtoggle else ''
        else:
            code   = 'f'
            togoff = self.OtherMovementPowers('f')
        dotogglefix = istoggle and not doingtoggle

        if (t.canhov or t.canfly):
            if (bl == "f"):
                if (not fb_on_a): feedback = ''
                bindload = t.BLF(code)

                if t.totalkeys: ton = t.flyx
                else:           ton = t.hover

                if dotogglefix:
                    self.SoDToggleFix(t, key, self.MakeFlyModeKey, code, bl, file, feedback = feedback)
                elif usejumpfix:
                    self.SoDJumpFix(  t, key, self.MakeFlyModeKey, code, bl, file, feedback = feedback)
                else:
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(ton, togoff, start=True) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "af"):
                bindload = t.BLF(f'a{code}')
                if dotogglefix:
                    self.SoDToggleFix(t, key, self.MakeFlyModeKey, code, bl, file, "a", feedback)
                elif usejumpfix:
                    self.SoDJumpFix(  t, key, self.MakeFlyModeKey, code, bl, file, "a", feedback)
                else:
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.flyx, togoff, start=True) + t.dirs('DLR') + t.detaillo + t.flycamdist + feedback + bindload)

            else: # bl == "ff"
                bindload = t.BLF(f'f{code}')
                if dotogglefix:
                    self.SoDToggleFix(t, key, self.MakeFlyModeKey, code, bl, file, "f", feedback)
                elif usejumpfix:
                    self.SoDJumpFix(  t, key, self.MakeFlyModeKey, code, bl, file, "f", feedback)
                else:
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.flyx, togoff, start=True) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload)

        t.ini = ''

    # ###
    # TODO - need to test if this even works.  'mobile' and 'stationary' are both
    #        GFly, so it doesn't switch off when not moving, but... what's the point?
    # ###
    def MakeGFlyModeKey(self, t, bl, file, usejumpfix = False) -> None:
        key = t.GFlyModeKey
        name = UI.Labels['GFlyMode']
        if not self.Ctrls['GFlyMode'].IsEnabled(): return

        if self.GetState('GFlyMode'):
            if (bl == "gf"):
                bindload = t.BLF('gf')
                if usejumpfix:
                    self.SoDJumpFix(t,key,self.MakeGFlyModeKey,"gf",bl,file)
                else:
                    file.SetBind(key, name, self, t.ini + '$$up 1$$down 0' + self.actPower_toggle(t.gfly) + t.dirs('FBLR') + t.detaillo + t.flycamdist + bindload)

            elif (bl == "agf"):
                bindload = t.BLF('agf')
                if usejumpfix:
                    self.SoDJumpFix(t,key,self.MakeGFlyModeKey,"agf",bl,file,"a")
                else:
                    file.SetBind(key, name, self, t.ini + t.detaillo + t.flycamdist + t.dirs('UDLR') + bindload)

            else:
                if usejumpfix:
                    self.SoDJumpFix(t,key,self.MakeGFlyModeKey,"fgf",bl,file,"f")
                else:
                    if (bl == "fgf"):
                        file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.gfly,start=True) + t.detaillo + t.flycamdist + t.BLF('fgf'))
                    else:
                        file.SetBind(key, name, self, t.ini + t.detaillo + t.flycamdist + t.BLF('fgf'))

        t.ini = ''

    def PopulateBindFiles(self) -> bool:
        profile     = self.Profile
        resetfile   = profile.ResetFile()
        server      = profile.Server()
        archetype   = profile.Archetype()
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
            t.detailhi = f"$$visscale {self.GetState('DetailBase')}"
            t.detaillo = f"$$visscale {self.GetState('DetailMove')}"

        ## Combat Jumping / Super Jump
        if jpower := str(self.GetState('JumpPower')):
            t.canjmp = True
        if cpower := str(self.GetState('CJPower')):
            t.cancj = True

        if cpower and not jpower:
            t.cjmp = cpower
            t.jump = cpower
        elif jpower and not cpower:
            t.jump       = jpower
            t.jumpifnocj = jpower
        elif cpower and jpower:
            t.cjmp = cpower
            t.jump = jpower

        # Temp Travel Power Toggle
        if (self.GetState('TempEnable')):
            if temppower := self.TempTravelPowerPicker.HasPowerPicked():
                resetfile.SetBind(self.Ctrls['TempToggle'].MakeBind(f'powexecname {temppower}'))

        ## Flying / hover
        t.hover  = self.GetState('HoverPower')
        t.flyx   = self.GetState('FlyPower')
        t.canhov = bool(t.hover)
        t.canfly = bool(t.flyx)

        if archetype == "Peacebringer":
            t.canfly  = True
            t.canqfly = True

        if t.canhov and not t.canfly:   # hover, no fly
            t.flyx = t.hover
        elif not t.canhov and t.canfly: # fly, no hover
            t.hover = t.flyx
        elif t.canhov and t.canfly:     # hover and fly
            t.fly = t.flyx

        if t.canhov and self.GetState('TPTPHover'):
            t.tphover = f'$${self.togon} {t.hover}'

        if (self.HasGFly()):
            t.gfly = "Group Fly"
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
        if self.HasAnySoD() or self.GetState('AutoMouseLook'):
            self.DoSpeedOnDemandBinds(t)
        else:
            # bind normal movement keys if SoD not enabled or no mouselook
            if (self.GetState('Left')):
                resetfile.SetBind(self.Ctrls['Left'].MakeBind("+left"))
            if (self.GetState('Right')):
                resetfile.SetBind(self.Ctrls['Right'].MakeBind("+right"))
            if (self.GetState('Up')):
                resetfile.SetBind(self.Ctrls['Up'].MakeBind("+up"))
            if (self.GetState('Down')):
                resetfile.SetBind(self.Ctrls['Down'].MakeBind("+down"))
            if (self.GetState('Forward')):
                resetfile.SetBind(self.Ctrls['Forward'].MakeBind(["+forward", t.playerturn]))
            if (self.GetState('Back')):
                resetfile.SetBind(self.Ctrls['Back'].MakeBind("+backward"))
            if (self.GetState('Follow')):
                resetfile.SetBind(self.Ctrls['Follow'].MakeBind("+follow"))
            if (self.GetState('AutoRun')):
                resetfile.SetBind(self.Ctrls['AutoRun'].MakeBind("++autorun"))

        # Bind the turn keys in either case
        if (self.GetState('TurnLeft')):
            resetfile.SetBind(self.Ctrls['TurnLeft'].MakeBind("+turnleft"))
        if (self.GetState('TurnRight')):
            resetfile.SetBind(self.Ctrls['TurnRight'].MakeBind("+turnright"))

        # Make binds for the "stage 2" travel powers like Afterburner, if appropriate
        if self.Ctrls['FlySpecialKey'].IsEnabled():
            resetfile.SetBind(self.Ctrls['FlySpecialKey']  .MakeBind(f'powexecname {self.GetState("FlySpecialPower")}'))
        if self.Ctrls['SpeedSpecialKey'].IsEnabled():
            resetfile.SetBind(self.Ctrls['SpeedSpecialKey'].MakeBind(f'powexecname {self.GetState("SpeedSpecialPower")}'))
        if self.Ctrls['JumpSpecialKey'].IsEnabled():
            resetfile.SetBind(self.Ctrls['JumpSpecialKey'] .MakeBind(f'powexecname {self.GetState("JumpSpecialPower")}'))

        if self.IsKheldian(): self.DoKheldianBinds(t)

        ###### Basic travel power binds, not SoD
        # OK, first, let's do these trivial toggle binds if and only if we aren't doing SoD at all
        # The SoD case is handled inside make*ModeKey()
        #
        # TODO:  do we want "turn off other powers" added here?
        if not self.HasAnySoD():
            if self.GetKeyAction('Speed') == ACTION_PT:
                resetfile.SetBind(self.Ctrls["SpeedMode"].MakeBind(f'powexecname "{self.GetState("SpeedPower")}"'))

            if self.GetKeyAction('Jump') == ACTION_PT:
                jpower = self.GetState('JumpPower')
                cpower = self.GetState('CJPower')
                if jpower and cpower:
                    resetfile.SetBind(self.Ctrls['JumpMode'].MakeBind(f'powexecname "{jpower}"$$powexecname "{cpower}"'))
                elif jpower:
                    resetfile.SetBind(self.Ctrls['JumpMode'].MakeBind(f'powexecname "{jpower}"'))
                elif cpower:
                    resetfile.SetBind(self.Ctrls['JumpMode'].MakeBind(f'powexecname "{cpower}"'))

            if self.GetKeyAction('Fly') == ACTION_PT:
                fpower = self.GetState('FlyPower')
                hpower = self.GetState('HoverPower')
                if fpower and hpower:
                    resetfile.SetBind(self.Ctrls['FlyMode'].MakeBind(f'powexecname "{fpower}"$$powexecname "{hpower}"'))
                elif fpower:
                    resetfile.SetBind(self.Ctrls['FlyMode'].MakeBind(f'powexecname "{fpower}"'))
                elif hpower:
                    resetfile.SetBind(self.Ctrls['FlyMode'].MakeBind(f'powexecname "{hpower}"'))

        ###### Teleport Binds
        teamTPPower   = 'Team Teleport' if self.HasTTP() else ''
        normalTPPower = self.GetState('TPPower')

        # I'm not sure why we create these nop binds.  Are they necessary?
        if (self.HasTP() and not normalTPPower):
            resetfile.SetBind(self.Ctrls['TPBindKey'].MakeBind('nop'))
            resetfile.SetBind(self.Ctrls['TPComboKey'].MakeBind('nop'))
            if server == "Rebirth":
                resetfile.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('nop'))

        # personal tp binds
        if self.HasTP() and bool(normalTPPower):
            tphovermodeswitch = ''
            if t.tphover:
                tphovermodeswitch = t.bl('f') + "000000.txt"

            resetfile.SetBind(self.Ctrls['TPBindKey'].MakeBind(tpActivator + normalTPPower))
            tp_off = profile.GetBindFile("tp","tp_off.txt")
            tp_on1 = profile.GetBindFile("tp","tp_on1.txt")
            zoomin = '' if t.tphover else t.detailhi + t.runcamdist

            if server == 'Homecoming':
                resetfile.SetBind(self.Ctrls['TPComboKey'].MakeBind('+first$$-first$$powexecname ' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))

                tp_off.SetBind(self.Ctrls['TPComboKey'].MakeBind('+first$$-first$$powexecname ' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))

                tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeBind(f'+first$$-first$${self.unqueue}$$' + tpActivator + normalTPPower + zoomin + windowshow + profile.BLF('tp','tp_off.txt') + tphovermodeswitch))

            else: # server == Rebirth
                resetfile.SetBind(self.Ctrls['TPComboKey'].MakeBind('+ $$powexecname ' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))
                tp_off.SetBind(self.Ctrls['TPComboKey'].MakeBind('+ $$powexecname ' + normalTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('tp','tp_on1.txt')))
                tp_off.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('nop'))

                tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeBind(f'- $${self.unqueue}' + zoomin + windowshow + profile.BLF('tp','tp_off.txt') + tphovermodeswitch))
                tp_on1.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('+' + profile.BLF('tp','tp_on2.txt')))

                tp_on2 = profile.GetBindFile("tp","tp_on2.txt")
                tp_on2.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('-$$powexecname ' + normalTPPower + profile.BLF('tp','tp_on1.txt')))

        # team teleport binds
        if (self.HasTP() and self.HasTTP() and teamTPPower) :

            resetfile.SetBind(self.Ctrls['TTPBindKey'].MakeBind(tpActivator + teamTPPower))

            ttp_off = profile.GetBindFile("ttp","ttp_off.txt")
            ttp_on1 = profile.GetBindFile("ttp","ttp_on1.txt")

            if server == 'Homecoming':
                resetfile.SetBind(self.Ctrls['TTPComboKey'].MakeBind('+first$$-first$$powexecname ' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))

                ttp_off.SetBind(self.Ctrls['TTPComboKey'].MakeBind('+first$$-first$$powexecname ' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))

                ttp_on1.SetBind(self.Ctrls['TTPComboKey'].MakeBind(f'+first$$-first$${self.unqueue}$$' + tpActivator + teamTPPower + t.detailhi + t.runcamdist + windowshow + profile.BLF('ttp','ttp_off.txt')))

            else:
                resetfile.SetBind(self.Ctrls['TTPComboKey'].MakeBind('+ $$powexecname ' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))

                ttp_off.SetBind(self.Ctrls['TTPComboKey'].MakeBind('+ $$powexecname ' + teamTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('ttp','ttp_on1.txt')))
                ttp_off.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('nop'))

                ttp_on1.SetBind(self.Ctrls['TTPComboKey'].MakeBind(f'- $${self.unqueue}' + t.detailhi + t.runcamdist + windowshow + profile.BLF('ttp','ttp_off.txt')))
                ttp_on1.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('+' + profile.BLF('ttp','ttp_on2.txt')))

                ttp_on2 = profile.GetBindFile("ttp","ttp_on2.txt")
                ttp_on2.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('-$$powexecname ' + normalTPPower + profile.BLF('ttp','ttp_on1.txt')))

        return True

    ###### Kheldian power setup
    def DoKheldianBinds(self, t):
        profile   = self.Profile
        archetype = profile.Archetype()
        resetfile = profile.ResetFile()
        server    = profile.Server()
        humpower  = ''

        #  create the Nova and Dwarf form support files if enabled.
        if archetype == "Peacebringer":
            novaPower = "Bright Nova"
            dwarfPower = "White Dwarf"
            if server != 'Homecoming' and self.GetState('UseHumanFormPower'):
                humpower = f"$${self.togon} Shining Shield"
        else: # Warshade
            novaPower = "Dark Nova"
            dwarfPower = "Black Dwarf"
            if server != 'Homecoming' and self.GetState('UseHumanFormPower'):
                humpower = f"$${self.togon} Gravity Shield"

        fullstop = '$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'

        if self.GetState('NovaMode'):
            khelfeedback = f"t $name, Changing to {novaPower} Form" if self.GetState('KhelFeedback') else ''
            resetfile.SetBind(self.Ctrls['NovaMode'].MakeBind(f"{khelfeedback}{fullstop}{t.on}{novaPower}$$gototray {self.GetState('NovaTray')}" + profile.BLF('nova.txt')))

            novafile = profile.GetBindFile("nova.txt")

            if (bool(self.GetState('DwarfMode'))):
                khelfeedback = f"t $name, Changing to {dwarfPower} Form" if self.GetState('KhelFeedback') else ''
                novafile.SetBind(self.Ctrls['DwarfMode'].MakeBind(f"{khelfeedback}{fullstop}{t.off}{novaPower}{t.on}{dwarfPower}$$gototray {self.GetState('DwarfTray')}" + profile.BLF('dwarf.txt')))

            khelfeedback = "t $name, Changing to Human Form, SoD Mode" if self.GetState('KhelFeedback') else ''
            novafile.SetBind(self.Ctrls['NovaMode'].MakeBind(f"{khelfeedback}{fullstop}$${self.togoff} {novaPower}{humpower}$$gototray {self.GetState('HumanTray')}" + profile.BLF('reset.txt')))

            novafile.SetBind(self.Ctrls['Forward'].MakeBind(["+forward", t.playerturn]))
            novafile.SetBind(self.Ctrls['Left'].MakeBind("+left"))
            novafile.SetBind(self.Ctrls['Right'].MakeBind("+right"))
            novafile.SetBind(self.Ctrls['Back'].MakeBind("+backward"))
            novafile.SetBind(self.Ctrls['Up'].MakeBind("+up"))
            novafile.SetBind(self.Ctrls['Down'].MakeBind("+down"))
            novafile.SetBind(self.Ctrls['AutoRun'].MakeBind("++forward"))
            novafile.SetBind(self.Ctrls['FlyMode'].MakeBind('nop'))
            if (self.GetState('FlyMode') != self.GetState('SpeedMode')):
                novafile.SetBind(self.Ctrls['SpeedMode'].MakeBind('nop'))
            if (self.GetState('MouseChord')):
                novafile.SetBind('mousechord', 'Nova Form Mousechord', self.TabTitle, ['+down', '+forward', t.playerturn])

            # no teleport while nova
            novafile.SetBind(self.Ctrls['TPComboKey'].MakeBind('nop'))
            novafile.SetBind(self.Ctrls['TPBindKey'].MakeBind('nop'))
            if server == 'Rebirth':
                novafile.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('nop'))

            novafile.SetBind(self.Ctrls['Follow'].MakeBind("follow"))

        if self.GetState('DwarfMode'):
            khelfeedback = f"t $name, Changing to {dwarfPower} Form" if self.GetState('KhelFeedback') else ''
            resetfile.SetBind(self.Ctrls['DwarfMode'].MakeBind(f"{khelfeedback}{fullstop}$${self.togon} {dwarfPower}$$gototray {self.GetState('DwarfTray')}" + profile.BLF('dwarf.txt')))
            dwrffile = profile.GetBindFile("dwarf.txt")
            if (bool(self.GetState('NovaMode'))):
                khelfeedback = f"t $name, Changing to {novaPower} Form" if self.GetState('KhelFeedback') else ''
                dwrffile.SetBind(self.Ctrls['NovaMode'].MakeBind(f"{khelfeedback}{fullstop}$${self.togoff} {dwarfPower}$${self.togon} {novaPower}$$gototray {self.GetState('NovaTray')}" + profile.BLF('nova.txt')))

            khelfeedback = "t $name, Changing to Human Form, SoD Mode" if self.GetState('KhelFeedback') else ''
            dwrffile.SetBind(self.Ctrls['DwarfMode'].MakeBind(f"{khelfeedback}{fullstop}$${self.togoff} {dwarfPower}{humpower}$$gototray 1" + profile.BLF('reset.txt')))

            dwrffile.SetBind(self.Ctrls['Forward'].MakeBind(["+forward", t.playerturn]))
            dwrffile.SetBind(self.Ctrls['Left'].MakeBind("+left"))
            dwrffile.SetBind(self.Ctrls['Right'].MakeBind("+right"))
            dwrffile.SetBind(self.Ctrls['Back'].MakeBind("+backward"))
            dwrffile.SetBind(self.Ctrls['Up'].MakeBind("+up"))
            dwrffile.SetBind(self.Ctrls['Down'].MakeBind("+down"))
            dwrffile.SetBind(self.Ctrls['AutoRun'].MakeBind("++forward"))
            dwrffile.SetBind(self.Ctrls['FlyMode'].MakeBind('nop'))
            dwrffile.SetBind(self.Ctrls['Follow'].MakeBind("follow"))
            if (self.GetState('FlyMode') != self.GetState('SpeedMode')):
                dwrffile.SetBind(self.Ctrls['SpeedMode'].MakeBind('nop'))
            if (self.GetState('MouseChord')):
                dwrffile.SetBind('mousechord', "Dwarf Mode Mousechord", self.TabTitle, ['+down', '+forward', t.playerturn])

    def DoSpeedOnDemandBinds(self, t) -> None:
        # most of this is so that we return to Default SoD mode when we reset.
        profile   = self.Profile
        resetfile = profile.ResetFile()
        extrafile = profile.GetBindFile('extra.txt')
        config    = wx.ConfigBase.Get()
        default   = self.SoDModeInfo(self.DefaultMode())
        on_off    = self.actPower_toggle(default['sta'], self.AllSoDPowers())

        # We do this over two files so it doesn't get too long if there are
        # multiple SoD pools and on_off has like five powers in it.
        resetfile.SetBind(config.Read('ResetKey'), "Reset Key", self.TabTitle,
                    [
                        '+',
                        'unbindall' if config.ReadBool('FlushAllBinds') else '',
                        on_off,
                        extrafile.BLF(),
                    ])
        extrafile.SetBind(config.Read('ResetKey'), "Reset Key", self.TabTitle,
                    [
                        '+',
                        'up 0', 'down 0', 'forward 0', 'backward 0', 'left 0', 'right 0',
                        't $name, Binds Reset',
                        resetfile.BLF(),
                        t.BLF(default['code']),
                    ])


        #  if a given mode is not our default, get the key we use to enter that mode.
        #  this will (hopefully) only be used if/when we actually have that mode available.
        if (self.DefaultMode() != "NonSoD") : t.NonSoDModeKey = self.GetState('NonSoDMode')
        if (self.DefaultMode() != "Sprint") : t.SprintModeKey = self.GetState('SprintMode')
        if (self.DefaultMode() != "Fly")    : t.FlyModeKey    = self.GetState('FlyMode')
        if (self.DefaultMode() != "Jump")   : t.JumpModeKey   = self.GetState('JumpMode')
        if (self.DefaultMode() != "Speed")  : t.SpeedModeKey  = self.GetState('SpeedMode')
        if (self.DefaultMode() != "GFly")   : t.GFlyModeKey   = self.GetState('GFlyMode')

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
                                t.jkeys     = t.horizkeys+t.space

                                sssj = t.jump if self.GetState('SSSJModeEnable') else ''
                                ### NonSoD Mode
                                if self.HasAnySoD():
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'key'        : t.NonSoDModeKey,
                                        'suffix'     : 'n',
                                        'mobile'     : None,
                                        'stationary' : None,
                                        'modestr'    : "NonSoD",
                                        'sssj'       : sssj,
                                    })

                                ### Sprint Mode
                                if self.SoDEnabled() and self.GetState('SprintPower'):
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'key'        : t.SprintModeKey,
                                        'suffix'     : 'r',
                                        'mobile'     : t.sprint,
                                        'stationary' : None,
                                        'modestr'    : "Sprint",
                                        'sssj'       : sssj,
                                    })

                                ### Speed Mode
                                if self.GetKeyAction('Speed'):
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'key'        : t.SpeedModeKey,
                                        'suffix'     : 's',
                                        'mobile'     : t.speed,
                                        'stationary' : None, # I think we want no stationary power with SS anymore
                                        'modestr'    : "Super Speed",
                                        'sssj'       : sssj,
                                    })

                                ### Jump Mode
                                if self.GetKeyAction('Jump'):
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'key'        : t.JumpModeKey,
                                        'suffix'     : 'j',
                                        'mobile'     : t.jump,
                                        'stationary' : t.cjmp,
                                        'modestr'    : "Jump",
                                        'flight'     : "Jump",
                                        'sssj'       : sssj,
                                    })

                                ### Fly Mode
                                if self.GetKeyAction('Fly') and (t.canhov or t.canfly):
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'key'        : t.FlyModeKey,
                                        'suffix'     : 'f',
                                        'mobile'     : t.flyx,
                                        'stationary' : t.hover,
                                        'modestr'    : "Fly",
                                        'flight'     : t.fly,
                                        'sssj'       : sssj,
                                    })

                                ### GFly Mode
                                if t.GFlyModeKey:
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'key'        : t.GFlyModeKey,
                                        'suffix'     : 'gf',
                                        'mobile'     : t.gfly,
                                        'stationary' : t.gfly,
                                        'modestr'    : "GFly",
                                        'flight'     : "GFly",
                                        'sssj'       : sssj,
                                    })

        # clear the state of the tObject for further use
        t.space = 0
        t.X = 0
        t.W = 0
        t.S = 0
        t.A = 0
        t.D = 0

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

    # Reset now goes back to the Default Mode from wherever you are.
    def SoDResetKey(self, curfile):
        # extra.txt was set up back at the head of DoSpeedOnDemandBinds, and we rely on the
        # existing contents there to: turn off movement; feedback; reset.txt; default SoD
        extrafile = self.Profile.GetBindFile('extra.txt')
        default   = self.SoDModeInfo(self.DefaultMode())
        on_off    = self.actPower_toggle(default['sta'], self.AllSoDPowers())

        config = wx.ConfigBase.Get()

        curfile.SetBind(config.Read('ResetKey'), UI.Labels['ResetKey'], self,
            [
                '+',
                'unbindall' if config.ReadBool('FlushAllBinds') else '',
                on_off,
                extrafile.BLF(),
            ]
        )

    def SoDUpKey(self, t, bl, curfile, mobile, stationary, flight, autorun = False, followbl = '', sssj = None) -> None:

        (upx,dow,forw,bac,lef,rig) = (t.upx,t.dow,t.forw,t.bac,t.lef,t.rig)

        actkeys = t.totalkeys
        mouselook = ''

        if (not flight) and (not sssj):
            mobile = stationary = None

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

        newbits = t.KeyState(toggle = 'space')
        bl = f"{bl}{newbits}.txt"

        if t.space == 1: ini = '-down'
        else:            ini = '+down'

        if (followbl):
            move = ''
            if (t.space != 1):
                bl = f"{followbl}{newbits}.txt"
                move = f"{upx}{dow}{forw}{bac}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Up'].MakeBind(f"{ini}{move}{bl}"))
        elif (not autorun):
            curfile.SetBind(self.Ctrls['Up'].MakeBind(f"{ini}{upx}{dow}{forw}{bac}{lef}{rig}{mouselook}{toggle}{bl}"))
        else:
            if (not sssj) : toggle = ''  #  returns the following line to the way it was before sssj
            curfile.SetBind(self.Ctrls['Up'].MakeBind(f"{ini}{upx}{dow}$$backward 0{lef}{rig}{toggle}{t.mouselookon}{bl}"))

    def SoDDownKey(self, t, bl, curfile, mobile, stationary, flight, autorun = False, followbl = '') -> None:
        (up,dowx,forw,bac,lef,rig) = (t.up,t.dowx,t.forw,t.bac,t.lef,t.rig)

        actkeys = t.totalkeys
        mouselook      = ''

        if (not flight):
            mobile = stationary = None

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

        newbits = t.KeyState(toggle = 'X')
        bl = f"{bl}{newbits}.txt"

        if t.X == 1: ini = "-down"
        else:        ini = "+down"

        if (followbl):
            move = ''
            if (t.X != 1):
                bl = f"{followbl}{newbits}.txt"
                move = f"{up}{dowx}{forw}{bac}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Down'].MakeBind(f"{ini}{move}{bl}"))
        elif (not autorun):
            curfile.SetBind(self.Ctrls['Down'].MakeBind(f"{ini}{up}{dowx}{forw}{bac}{lef}{rig}{mouselook}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Down'].MakeBind(f"{ini}{up}{dowx}$$backward -1{lef}{rig}{t.mouselookon}{bl}"))

    def SoDForwardKey(self, t, bl, curfile,  mobile, stationary, flight, autorunbl = '', followbl = '', sssj = None) -> None:
        (up,dow,forx,bac,lef,rig) = (t.up,t.dow,t.forx,t.bac,t.lef,t.rig)
        name = UI.Labels['Forward']

        mouselook = ''

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

        newbits = t.KeyState(toggle = 'W')
        bl = f"{bl}{newbits}.txt"

        if t.W == 1: ini = "-down"
        else:        ini = "+down"

        if (followbl):
            if (t.W == 1):
                move = ini
            else:
                bl = f"{followbl}{newbits}.txt"
                move = f"{ini}{up}{dow}{forx}{bac}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Forward'].MakeBind(move + bl))
            if (self.GetState('MouseChord')):
                if (t.W != 1) : move = f"{ini}{up}{dow}{forx}{bac}{rig}{lef}{t.playerturn}"
                curfile.SetBind('mousechord', name, self, move + bl)

        elif (not autorunbl):
            curfile.SetBind(self.Ctrls['Forward'].MakeBind(f"{ini}{up}{dow}{forx}{bac}{lef}{rig}{mouselook}{toggle}{bl}"))
            if (self.GetState('MouseChord')):
                curfile.SetBind('mousechord', name, self, f"{ini}{up}{dow}{forx}{bac}{rig}{lef}{mouselook}{toggle}{t.playerturn}{bl}")

        else:
            if (t.W != 1):
                bl = f"{autorunbl}{newbits}.txt"

            curfile.SetBind(self.Ctrls['Forward'].MakeBind(f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{lef}{rig}{t.mouselookon}{bl}"))
            if (self.GetState('MouseChord')) :
                curfile.SetBind('mousechord', name, self, f"{ini}{up}{dow}{'$$forward 1$$backward 0'}{rig}{lef}{t.mouselookon}{t.playerturn}{bl}")

    def SoDBackKey(self, t, bl, curfile, mobile, stationary, flight, autorunbl = '', followbl = '', sssj = None) -> None:
        (up,dow,forw,bacx,lef,rig) = (t.up,t.dow,t.forw, t.bacx,t.lef,t.rig)

        mouselook = ''
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

        newbits = t.KeyState(toggle = 'S')
        bl = f"{bl}{newbits}.txt"

        if (t.S == 1) : ini = "-down"
        else:           ini = "+down"

        if (followbl):
            if (t.S == 1):
               move = ini
            else:
                bl = f"{followbl}{newbits}.txt"
                move = f"{ini}{up}{dow}{forw}{bacx}{lef}{rig}"

            curfile.SetBind(self.Ctrls['Back'].MakeBind(move + bl))
        elif (not autorunbl) :
            curfile.SetBind(self.Ctrls['Back'].MakeBind(f"{ini}{up}{dow}{forw}{bacx}{lef}{rig}{mouselook}{toggle}{bl}"))
        else:
            if (t.S == 1):
                move = '$$forward 1$$backward 0'
            else:
                move = '$$forward 0$$backward 1'
                bl = f"{autorunbl}{newbits}.txt"

            curfile.SetBind(self.Ctrls['Back'].MakeBind(f"{ini}{up}{dow}{move}{lef}{rig}{t.mouselookon}{bl}"))

    def SoDLeftKey(self, t, bl, curfile, mobile, stationary, flight, autorun = False, followbl = '', sssj = None) -> None:
        (up,dow,forw,bac,lefx,rig) = (t.up,t.dow,t.forw,t.bac, t.lefx,t.rig)

        mouselook = ''
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

        newbits = t.KeyState(toggle = 'A')
        bl = f"{bl}{newbits}.txt"

        if (t.A == 1): ini = '-down'
        else:          ini = '+down'

        if (followbl) :
            if (t.A == 1) :
               move = ini
            else:
                bl = f"{followbl}{newbits}.txt"
                move = f"{ini}{up}{dow}{forw}{bac}{lefx}{rig}"

            curfile.SetBind(self.Ctrls['Left'].MakeBind(move + bl))
        elif (not autorun) :
            curfile.SetBind(self.Ctrls['Left'].MakeBind(f"{ini}{up}{dow}{forw}{bac}{lefx}{rig}{mouselook}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Left'].MakeBind(f"{ini}{up}{dow}{'$$backward 0'}{lefx}{rig}{t.mouselookon}{bl}"))

    def SoDRightKey(self, t, bl, curfile, mobile, stationary, flight, autorun = False, followbl = '', sssj = None) -> None:
        (up,dow,forw,bac,lef,rigx) = (t.up,t.dow,t.forw,t.bac,t.lef, t.rigx)

        mouselook = ''
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

        newbits = t.KeyState(toggle = 'D')
        bl = f"{bl}{newbits}.txt"

        if (t.D == 1): ini = '-down'
        else:          ini = '+down'

        if (followbl) :
            if (t.D == 1):
                move = ini
            else:
                bl = f"{followbl}{newbits}.txt"
                move = f"{ini}{up}{dow}{forw}{bac}{lef}{rigx}"

            curfile.SetBind(self.Ctrls['Right'].MakeBind(move + bl))
        elif (not autorun) :
            curfile.SetBind(self.Ctrls['Right'].MakeBind(f"{ini}{up}{dow}{forw}{bac}{lef}{rigx}{mouselook}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Right'].MakeBind(f"{ini}{up}{dow}$$forward 1$$backward 0{lef}{rigx}{t.mouselookon}{bl}"))

    def SoDAutoRunKey(self, t, bl, curfile, mobile, sssj) -> None:
        bindload = bl + t.KeyState() + ".txt"
        if (sssj and t.space == 1) :
            curfile.SetBind(self.Ctrls['AutoRun'].MakeBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mouselookon + self.actPower_name(sssj,mobile) + bindload))
        else:
            curfile.SetBind(self.Ctrls['AutoRun'].MakeBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mouselookon + self.actPower_name(mobile) + bindload))

    def SoDAutoRunOffKey(self, t, bl, curfile, mobile, stationary, flight) -> None:
        toggleon = None
        if not flight:
            if (t.horizkeys > 0) : # if flying, check only horizontal keys
                toggleon = t.mouselookon + self.actPower_name(mobile)
            else:
                toggleon = t.mouselookoff + self.actPower_name(stationary,mobile)

        else:
            if (t.totalkeys > 0) : # otherwise check all keys
                toggleon = t.mouselookon + self.actPower_name(mobile)
            else:
                toggleon = t.mouselookoff + self.actPower_name(stationary,mobile)

        bindload = bl + t.KeyState() + '.txt'
        # "[2:]" on next line is to trim off the initial "$$" that dirs() provides
        curfile.SetBind(self.Ctrls['AutoRun'].MakeBind(t.dirs('UDFBLR')[2:] + toggleon + bindload))

    def SoDFollowKey(self, t, bl, curfile, mobile, stationary) -> None:
        curfile.SetBind(self.Ctrls['Follow'].MakeBind('follow' + self.actPower_toggle(mobile,stationary) + bl + t.KeyState() + '.txt'))

    def SoDFollowOffKey(self, t, bl, curfile, mobile, stationary, flight) -> None:
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

        curfile.SetBind(self.Ctrls['Follow'].MakeBind("follow" + toggle + t.up + t.dow + t.forw + t.bac + t.lef + t.rig + bl + t.KeyState() + '.txt'))

    #  toggleon variation
    def actPower_toggle(self, on, off:Any = '', start = False) -> str:
        s = ''

        offpower = set()

        if off and isinstance(off, (set,list)):
            for w in off:
                if (w and w != on and (w not in offpower)):
                    offpower.add(w)
                    s = s + f'$${self.togoff} {w}'

        elif off and (off != on):
                s = s + f'$${self.togoff} {off}'

        if on:
            s = s + f'$${self.togon} {on}'

        if start: s = s[2:]
        return s

    def actPower_name(self, on, *rest) -> str:
        s = ''
        for v in rest:
            if isinstance(v, str):
                if (v and v != on):
                    s = s + '$$powexecname ' + v

            elif isinstance(v, set):
                for w in v:
                    if (w and w != on):
                        s = s + '$$powexecname ' + w

        # Why are we doing this?  Let's not for now
        # if s:
        #     s = s + f'$${self.unqueue}'

        # why twice?  Does this guarantee that it gets activated, somehow?
        # Like, if it's already on, this turns it off, then turns it on?
        # And if it's off, it turns it on, and since that's activating one power, it stops?
        #
        # Yes, yes I think that's exactly why.  Why do we not just... powexectoggle_on here
        # instead?  Not sure if there's a reason one way or the other, leaving it for now.
        if on:
            s = s + '$$powexecname ' + on + '$$powexecname ' + on

        return s

    def SoDJumpFix(self, t, key, makeModeKey, suffix, bl, curfile, afmode = '', feedback = '') -> None:

        # This is the same file we were in with originally, in the calling sub,
        # except with 'j' tacked on the end.
        tglfile  = self.Profile.GetBindFile( t.bfpath(afmode + 'j', suffix) )

        # I think t.ini was unset before.  This makes the bind we're about to make
        # back in the original method into the "key up" for the "key down" we'll make below
        # It's going to be in the new file, which is loaded by the "key down" bind below,
        # and it, itself, when "key up," will load the intended BLF().  We've shimmed a
        # two-part press/release combo into the place of just a simple keypress bind.
        t.ini    = '+$$'

        # Also, I'm not 100% clear why we do this specifically with Jump Mode.  Why do we
        # need this press/release thing specifically here?  Bind length, with the feedback
        # tacked on the end?  Maybe?

        # make the "key up" bind back in the calling method.  We set skipfeedback = True
        # because we will be giving the feedback in the "key down" bind.
        makeModeKey(t, bl, tglfile, skipfeedback = True)
        # make the "key down" bind
        curfile.SetBind(key, "Jump Fix", self, "+" + feedback + self.actPower_name(t.cjmp) + t.BLF(f'{afmode}j', suffix))

    def SoDToggleFix(self, t, key, makeModeKey, suffix, bl, curfile, afmode = '', feedback = '', sssj = '') -> None:
        # if we are a toggle bind, *KeyAction == ACTION_PT, then
        # we want to make a press / release keybind pair.  On press:
        #   "+$$"
        #   * give feedback
        #   * toggle the toggle power
        #   * blf a second file
        # in the second file:
        #   * "+$$"
        #   * turn off SoD powers
        #   * BLF the N/N(keystate) file to turn off the movement keys' SoD stuff
        # So, now, on press we toggle the indicated power, and on release, we turn
        # off SoD (every time, whatever)
        t.ini = '+$$'

        if makeModeKey == self.MakeSprintModeKey:
            powercode = 'r'
            power = t.sprint
            tglfile = self.Profile.GetBindFile( t.bfpath(afmode + powercode, suffix) )
            makeModeKey(t, bl, tglfile, skipfeedback = True, doingtoggle = True)
        elif makeModeKey == self.MakeSpeedModeKey:
            powercode = 's'
            power = t.speed
            tglfile = self.Profile.GetBindFile( t.bfpath(afmode + powercode, suffix) )
            makeModeKey(t, bl, tglfile, skipfeedback = True, doingtoggle = True, sssj = sssj)
        elif makeModeKey == self.MakeJumpModeKey:
            powercode = 'j'
            power = {t.jump, t.cjmp}
            tglfile = self.Profile.GetBindFile( t.bfpath(afmode + powercode, suffix) )
            makeModeKey(t, bl, tglfile, t.path(afmode + powercode), t.bl(afmode + powercode), doingtoggle = True)
        elif makeModeKey == self.MakeFlyModeKey:
            powercode = 'f'
            power = {t.fly, t.hover}
            tglfile = self.Profile.GetBindFile( t.bfpath(afmode + powercode, suffix) )
            makeModeKey(t, bl, tglfile, skipfeedback = True, doingtoggle = True)
        else:
            raise Exception("Unknown callback in SoDToggleFix.  This is a bug.")

        curfile.SetBind(key, "Toggle Fix", self, "+" + feedback + self.actPower_name('', power) + t.BLF(f'{afmode}{powercode}', suffix))

    ### convenience methods
    def SoDEnabled(self) -> bool:
        return self.Ctrls['EnableSoD'].IsChecked()

    def DefaultMode(self) -> str:
        return self.Ctrls['DefaultMode'].GetStringSelection() or 'NonSoD'

    def HasGFly(self) -> bool:
        return self.Profile.HasPower('Flight', 'Group Fly')

    def HasTP(self):
        return (self.Profile.HasPower('Teleportation', 'Teleport')
                    or self.Profile.HasPower('Sorcery', 'Mystic Flight')
                    or self.GetState('SpeedPower') == 'Speed of Sound'
                    or self.IsKheldian()
                )

    def HasTTP(self) -> bool:
        return self.Profile.HasPower('Teleportation', 'Team Teleport')

    def HasAnySoD(self) -> bool:
        return (
            self.SoDEnabled() and (
                (self.Ctrls['JumpKeyAction'] .IsShown() and self.GetKeyAction('Jump')  == ACTION_SOD)
                    or
                (self.Ctrls['FlyKeyAction']  .IsShown() and self.GetKeyAction('Fly')   == ACTION_SOD)
                    or
                (self.Ctrls['SpeedKeyAction'].IsShown() and self.GetKeyAction('Speed') == ACTION_SOD)
            )
        )

    def IsKheldian(self) -> bool:
        return bool(self.Profile.Archetype() in ("Warshade", "Peacebringer"))

    # Get what state the KeyAction picker is in for a given *Mode key.
    def GetKeyAction(self, powertype: Literal['Jump', 'Fly', 'Speed', 'Sprint']) -> int:
        actionctrl = self.Ctrls[powertype + 'KeyAction']
        if not actionctrl.IsEnabled(): return 0
        return {
            'Speed on Demand' : ACTION_SOD,
            'Power Toggle'    : ACTION_PT,
        }.get(actionctrl.GetStringSelection(), 0)

    # used to do a "turn off all SoD" when toggling on a non-SoD power
    def AllSoDPowers(self) -> set:
        powers = set()
        if self.GetKeyAction('Jump') == ACTION_SOD:
            if jp := self.GetState('JumpPower'):   powers.add(jp)
            if cp := self.GetState('CJPower'):     powers.add(cp)
        if self.GetKeyAction('Fly') == ACTION_SOD:
            if fp := self.GetState('FlyPower'):    powers.add(fp)
            if hp := self.GetState('HoverPower'):  powers.add(hp)
        if self.GetKeyAction('Speed') == ACTION_SOD:
            if sp := self.GetState('SpeedPower'):  powers.add(sp)
        if self.GetKeyAction('Sprint') == ACTION_SOD:
            if rp := self.GetState('SprintPower'): powers.add(rp)
        return powers

    # powers that I own that are not in the current context.
    # For turning everyone else off when we turn something on
    def OtherMovementPowers(self, context: Literal['j', 'f', 's', 'n', 'r']) -> set:
        powers = set()
        # the "and self.*KeyAction" in this case means "and BC is managing this
        # movement power" but this means it won't shut off movement powers activated
        # manually via power trays or Simple Binds or something.  I think we're just
        # going to have to live with that.
        if context != 'j' and self.GetKeyAction('Jump'):
            if jp := self.GetState('JumpPower'):    powers.add(jp)
            if cp := self.GetState('CJPower'):      powers.add(cp)
        if context != 'f' and self.GetKeyAction('Fly'):
            if fp := self.GetState('FlyPower'):     powers.add(fp)
            if hp := self.GetState('HoverPower'):   powers.add(hp)
        if context != 's' and self.GetKeyAction('Speed'):
            if sp := self.GetState('SpeedPower'):   powers.add(sp)
        if context != 'r':
            if rp := self.GetState('SprintPower') : powers.add(rp)
        return powers

    # get blf etc info for given SoD Mode, typically Default but w/e
    def SoDModeInfo(self, Mode):
        c = self.Ctrls
        return {
            'Jump'        : {
                'code' : 'j',
                'sta'  : c['CJPower'].GetStringSelection(),
                'mob'  : c['JumpPower'].GetStringSelection(),
            },
            'Fly'         : {
                'code' : 'f',
                'sta'  : c['HoverPower'].GetStringSelection(),
                'mob'  : c['FlyPower'].GetStringSelection(),
            },
            'Sprint'      : {
                'code' : 'r',
                'sta'  : '',
                'mob'  : c['SprintPower'].GetStringSelection(),
            },
            'NonSoD'      : {
                'code' : 'n',
                'sta'  : '',
                'mob'  : '',
            },
            'Super Speed' : {
                'code' : 's',
                'sta'  : '',
                'mob'  : c['SpeedPower'].GetStringSelection(),
            },
        }[Mode or 'NonSoD']

    def AllBindFiles(self) -> dict[str, list]:
        files = [self.Profile.GetBindFile('extra.txt')]
        dirs  = [
                'R'  , 'F'   , 'J'  , 'S'  , 'N'  , 'GF',
                'AR' , 'AF'  , 'AJ' , 'AS' , 'AN' , 'AGF',
                'FR' , 'FF'  , 'FJ' , 'FS' , 'FN' , 'FGF',
                'BO' , 'GBO' ,
        ]
        for d in dirs:
            for sp in (0,1):
                for X in (0,1):
                    for W in (0,1):
                        for S in (0,1):
                            for A in (0,1):
                                for D in (0,1):
                                    for suffix in ['', 'f', 'j', 'a', 'n', 'r', 's', 'gf', '_t', '_s',]:
                                        files.append(
                                            self.Profile.GetBindFile(d,
                                                f'{d}{sp}{X}{W}{S}{A}{D}{suffix}.txt')
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

    'PlayerTurn'     : 'Turn to match camera',
    'AutoMouseLook'  : 'Mouselook when moving',
    'ChangeCamera'   : 'Change camera distance when moving',
    'CamdistBase'    : 'Base Camera Distance',
    'CamdistMove'    : 'Travelling Camera Distance',
    'ChangeDetail'   : 'Change graphics detail level when moving',
    'DetailBase'     : 'Base Detail Level',
    'DetailMove'     : 'Travelling Detail Level',

    'TempEnable'     : 'Enable Temp Travel Power Bind',
    'TempToggle'     : 'Toggle Temp Travel Power',

    'KhelFeedback'      : 'Give /tell Feedback When Changing Form',
    'UseHumanFormPower' : 'Activate Shield With Human Form',
    'HumanTray'         : 'Human Form Power Tray',
    'NovaMode'          : 'Toggle Nova Form',
    'NovaTray'          : 'Nova Form Power Tray',
    'DwarfMode'         : 'Toggle Dwarf Form',
    'DwarfTray'         : 'Dwarf Form Power Tray',

    'EnableSoD'      : 'Enable Speed on Demand Binds',
    'DefaultMode'    : 'Default Speed on Demand Mode',
    'NonSoDMode'     : 'Speed on Demand Toggle Key',
    'MouseChord'     : 'Mousechord is SoD Forward',
    'Feedback'       : 'Self-/tell when changing SoD mode',

    'SprintKeyAction' : "Sprint Key Action",
    'SprintPower'     : 'Preferred Sprint Power',
    'SprintMode'      : 'Sprint Key',

    'SpeedKeyAction'    : "Speed Key Action",
    'SpeedPower'        : "Primary Speed Power",
    'SpeedMode'         : 'Speed Key',
    'SSSJModeEnable'    : 'Enable Super Speed / Super Jump Mode',
    'SpeedSpecialKey'   : '',
    'SpeedSpecialPower' : '', # Hidden

    'JumpKeyAction'    : "Jump Key Action",
    'JumpPower'        : "Primary Jump Power",
    'CJPower'          : "Defensive Jump Power",
    'JumpMode'         : 'Jump Key',
    'JumpSpecialKey'   : '',
    'JumpSpecialPower' : '', # hidden

    'FlyKeyAction'    : "Fly Key Action",
    'FlyPower'        : "Primary Fly Power",
    'HoverPower'      : "Defensive Fly Power",
    'FlyMode'         : 'Fly Key',
    'FlySpecialKey'   : '',
    'FlySpecialPower' : '', # hidden
    'GFlyMode'        : 'Toggle Group Fly Mode',

    'TPPower'        : 'Teleport Power',
    'TPComboKey'     : 'Hold to Show Teleport Target Marker',
    'TPTPHover'      : 'Hover when Teleporting',
    'TTPComboKey'    : 'Hold to Show Team Teleport Target Marker',
    'TTPTPGFly'      : 'Group Fly when Team Teleporting',
    'TPHideWindows'  : 'Hide Windows when Holding Target Marker Key',
})
