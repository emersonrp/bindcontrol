import re
import wx
from typing import Any

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

class MovementPowers(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.TabTitle : str = "Movement / Speed on Demand"

        self.TempTravelPowerMenu : wx.Menu|None = None

        # A few things that are server-specific.  If we change servers, we reload the profile
        # so this is safe to do in __init__
        server = self.Profile.Server()
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
            'DefaultMode'     : "Sprint",
            'MouseChord'      : False,
            'PlayerTurn'      : False, # TODO this should toggle with "Keybind Profile" somehow
            'AutoMouseLook'   : False,

            'SprintMode'      : '',
            'SprintPower'     : 'Sprint',

            'ChangeCamera'    : False,
            'CamdistBase'     : 15,
            'CamdistMove'     : 60,
            'ChangeDetail'    : False,
            'DetailBase'      : 100,
            'DetailMove'      : 50,
            'Feedback'        : False,

            'NonSoDMode'      : '',

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
            tooltip = "Select the Speed on Demand mode the movement keys will use by default")
        self.Ctrls['DefaultMode'].Bind(wx.EVT_CHOICE, self.OnSpeedOnDemandChanged)
        SoDSizer.AddControl(ctlName = 'NonSoDMode', ctlType = 'keybutton',
            helpfile = 'SoDToggle.html',
            tooltip = "Select the key to toggle whether Speed on Demand is active")
        SoDSizer.AddControl(ctlName = 'SprintMode', ctlType = 'keybutton',
            helpfile = 'SprintSoDToggle.html',
            tooltip = "Select the key to toggle Sprint Speed on Demand Mode")
        SoDSizer.AddControl(ctlName = 'SprintPower', ctlType = 'choice',
            contents = GameData.SprintPowers,
            helpfile = 'PreferredSprintPower.html',
            tooltip = "Select the power to use for Sprint Speed on Demand")
        SoDSizer.AddControl(ctlName = 'MouseChord', ctlType = 'checkbox',
            tooltip = "Holding both mouse buttons will go forward using the current Speed on Demand Mode")
        SoDSizer.AddControl(ctlName = 'Feedback', ctlType = 'checkbox',
            tooltip = "Announce changes in Speed on Demand modes via self-/tell")

        self.rightColumn.Add(SoDSizer, 0, wx.EXPAND)

        ##### SUPER SPEED
        self.superSpeedSizer = ControlGroup(self, self, 'Super Speed Powers Settings')
        self.superSpeedSizer.AddControl(ctlName = 'SpeedKeyAction', ctlType = 'choice',
            contents = ('Speed on Demand', 'Power Toggle', 'None'),
            helpfile = 'SpeedKeyAction.html',
            tooltip = 'Select what the Speed Power Key will do')
        self.Ctrls['SpeedKeyAction'].Bind(wx.EVT_CHOICE, self.OnSpeedChanged)
        self.superSpeedSizer.AddControl(ctlName = "SpeedPower", ctlType = 'choice', contents = [''],
            tooltip = "Select the super speed power to use with the keybinds in this section")
        self.Ctrls['SpeedPower'].Bind(wx.EVT_CHOICE, self.OnSpeedChanged)
        self.superSpeedSizer.AddControl(ctlName = 'SpeedMode', ctlType = 'keybutton',)
        self.superSpeedSizer.AddControl(ctlName = 'SpeedSpecialKey', ctlType = 'keybutton',)
        self.superSpeedSizer.AddControl(ctlName = 'SSSJModeEnable', ctlType = 'checkbox',
            tooltip = "Enable Super Speed + Super Jump Mode.")
        self.rightColumn.Add(self.superSpeedSizer, 0, wx.EXPAND)

        ##### SUPER JUMP
        self.superJumpSizer = ControlGroup(self, self, 'Jumping Powers Settings')
        self.superJumpSizer.AddControl(ctlName = 'JumpKeyAction', ctlType = 'choice',
            contents = ('Speed on Demand', 'Power Toggle', 'None'),
            helpfile = 'JumpKeyAction.html',
            tooltip = 'Select what the Jump Power Key will do')
        self.Ctrls['JumpKeyAction'].Bind(wx.EVT_CHOICE, self.OnJumpChanged)
        self.superJumpSizer.AddControl(ctlName = "JumpPower", ctlType = 'choice', contents = [''],
            tooltip = "Select the jump power to use with the keybinds in this section")
        self.Ctrls['JumpPower'].Bind(wx.EVT_CHOICE, self.OnJumpChanged)
        self.superJumpSizer.AddControl(ctlName = 'CJPower', ctlType = 'choice', contents = ['', 'Combat Jumping'],
            tooltip = "Select the jump power that will be activated by Speed on Demand when you are not moving")
        self.superJumpSizer.AddControl(ctlName = 'JumpMode', ctlType = 'keybutton',)
        self.superJumpSizer.AddControl(ctlName = 'JumpSpecialKey', ctlType = 'keybutton',)
        self.rightColumn.Add(self.superJumpSizer, 0, wx.EXPAND)

        ##### FLY
        self.flySizer = ControlGroup(self, self, 'Flight Powers Settings')
        self.flySizer.AddControl(ctlName = 'FlyKeyAction', ctlType = 'choice',
            contents = ('Speed on Demand', 'Power Toggle', 'None'),
            helpfile = 'FlyKeyAction.html',
            tooltip = 'Select what the Fly Power Key will do')
        self.Ctrls['FlyKeyAction'].Bind(wx.EVT_CHOICE, self.OnFlightChanged)
        self.flySizer.AddControl(ctlName = "FlyPower", ctlType = 'choice', contents = [''],
            tooltip = "Select the flight power to use with the keybinds in this section")
        self.flySizer.AddControl(ctlName = 'HoverPower', ctlType = 'choice', contents = ['', 'Hover', 'Combat Flight'],
            tooltip = "Select the flight power that will be activated by Speed on Demand when you are not moving")
        self.Ctrls['FlyPower'].Bind(wx.EVT_CHOICE, self.OnFlightChanged)
        self.flySizer.AddControl(ctlName = 'FlyMode', ctlType = 'keybutton',)
        self.flySizer.AddControl(ctlName = 'FlySpecialKey', ctlType = 'keybutton',)
        self.flySizer.AddControl(ctlName = 'GFlyMode', ctlType = 'keybutton',
            tooltip = "Toggle Group Fly Speed on Demand Mode")
        self.rightColumn.Add(self.flySizer, 0, wx.EXPAND)

        ##### TELEPORT
        self.teleportSizer = ControlGroup(self, self, 'Teleport Powers Settings')
        self.teleportSizer.AddControl(ctlName = "TPPower", ctlType = 'choice', contents = [''],
            tooltip = "Select the teleport power to use with the keybinds in this section")
        self.Ctrls['TPPower'].Bind(wx.EVT_CHOICE, self.OnTeleportChanged)
        if server == "Homecoming":
            tpTooltip = 'Immediately teleport to the cursor position without showing a target marker.'
            tpcTooltip = 'Show target marker on keypress;  teleport to marker on key release.'
        else:
            # TODO - is this "show marker on press, teleport on release?"  Clarify if so.
            tpTooltip = 'Initiate teleport power, showing target marker.'
            # ...because otherwise this one is the same thing.
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
            ttpTooltip = "Initiate Team Teleport, showing target marker."
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

        topSizer.Add(self.leftColumn, 0, wx.ALL, 3)
        topSizer.Add(self.rightColumn, 0, wx.ALL, 3)

        self.MainSizer.Add(topSizer, flag = wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, border = 16)

    # If we have two items, blank plus one power, pre-set it to the one power
    def PrePickLonePower(self, control) -> None:
        if not isinstance(control, wx.Choice): return
        if control.GetCount() == 2: control.SetSelection(1)

    def ShowControlGroup(self, group, show = True) -> None:
        if self.rightColumn.GetItem(group):
            self.rightColumn.Show(group, show)
        elif self.leftColumn.GetItem(group):
            self.leftColumn.Show(group, show)
        else:
            wx.LogError(f"Tried to show/hide ControlGroup {group} which is in neither column.  This is a bug.")
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
        sodmode = self.GetState('DefaultMode')
        c['NonSoDMode'].Show(bool(sodmode))
        c['SprintMode'].Show(sodmode != 'Sprint')
        for ctrl in ['DefaultMode', 'NonSoDMode', 'SprintPower', 'SprintMode', 'MouseChord', 'Feedback', ]:
            c[ctrl].Enable(self.SoDEnabled())
        for ctrl in ['JumpKeyAction', 'FlyKeyAction', 'SpeedKeyAction', ]:
            c[ctrl].ShowEntryIf('Speed on Demand', self.SoDEnabled())
            # Reset these pickers to saved state in case we just reappeared their desired value.  Might be bad.
            c[ctrl].SetStringSelection(self.Profile.Data.get('MovementPowers', {}).get(ctrl, ''))
        self.OnJumpChanged()
        self.OnSpeedChanged()
        self.OnFlightChanged()
        if evt: evt.Skip()

    def OnSpeedChanged(self, evt = None) -> None:
        c = self.Ctrls
        sodenabled = self.SoDEnabled()
        if (self.Profile.HasPower('Speed', 'Super Speed') or self.Profile.HasPower('Experimentation', 'Speed of Sound')):
            c['DefaultMode'].ShowEntryIf('Speed', self.SpeedKeyAction() == 'SoD')
            self.ShowControlGroup(self.superSpeedSizer)
            c['SpeedPower'].ShowEntryIf('Super Speed',    self.Profile.HasPower('Speed', 'Super Speed'))
            c['SpeedPower'].ShowEntryIf('Speed of Sound', self.Profile.HasPower('Experimentation', 'Speed of Sound'))
            self.PrePickLonePower(c['SpeedPower'])
            c['SpeedPower'].Enable(bool(self.SpeedKeyAction()))
            c['SpeedMode'].Show(self.DefaultMode() != "Speed")
            c['SpeedMode'].Enable(bool(self.SpeedKeyAction()))
            c['SSSJModeEnable'].Show(self.rightColumn.IsShown(self.superJumpSizer))
            c['SSSJModeEnable'].Enable(sodenabled)

            c['SpeedMode'].SetToolTip({
                'SoD' : 'Toggle Super Speed Speed on Demand Mode',
                'PT' : f'Toggle {c['SpeedPower'].GetStringSelection()} on and off',
            }.get(self.SpeedKeyAction(), ''))

            if (self.GetState('SpeedPower') == "Super Speed"):
                c['SpeedSpecialKey'].CtlLabel.SetLabel('Speed Phase:')
                c['SpeedSpecialPower'].SetValue('SpeedPhase')
                c['SpeedSpecialKey'].Show()
                c['SpeedSpecialKey'].SetToolTip('Activate Speed Phase')
            else:
                c['SpeedSpecialKey'].Show(False)
        else:
            self.ShowControlGroup(self.superSpeedSizer, False)
            c['DefaultMode'].ShowEntryIf('Speed', False)

        if evt: evt.Skip()

    def OnJumpChanged(self, evt = None) -> None:
        c = self.Ctrls
        if (self.Profile.HasPower('Leaping', 'Super Jump') or self.Profile.HasPower('Force of Will', 'Mighty Leap')):
            c['DefaultMode'].ShowEntryIf('Jump', self.JumpKeyAction() == 'SoD')
            self.ShowControlGroup(self.superJumpSizer)
            c['JumpPower'].ShowEntryIf('Super Jump',  self.Profile.HasPower('Leaping', 'Super Jump'))
            c['JumpPower'].ShowEntryIf('Mighty Leap', self.Profile.HasPower('Force of Will', 'Mighty Leap'))
            c['JumpPower'].Enable(bool(self.JumpKeyAction()))
            self.PrePickLonePower(c['JumpPower'])

            c['CJPower'].ShowEntryIf('Combat Jumping', self.Profile.HasPower('Leaping', 'Combat Jumping'))
            c['CJPower'].Show  (bool(self.JumpKeyAction()) and c['CJPower'].GetCount() > 1)
            c['CJPower'].Enable(bool(self.JumpKeyAction()) and c['CJPower'].GetCount() > 1)

            c['JumpMode'].Show(self.DefaultMode() != "Jump")
            c['JumpMode'].Enable(bool(self.JumpKeyAction()))
            c['SSSJModeEnable'].Show(bool(self.GetState('SpeedPower')))
            c['SSSJModeEnable'].Enable(self.SoDEnabled())

            c['JumpMode'].SetToolTip({
                'SoD' : 'Toggle Jump Speed on Demand Mode',
                'PT' : f'Toggle {c['JumpPower'].GetStringSelection()} on and off',
            }.get(self.JumpKeyAction(), ''))

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
            c['DefaultMode'].ShowEntryIf('Fly', False)

        if evt: evt.Skip()

    def OnFlightChanged(self, evt = None) -> None:
        c = self.Ctrls
        archetype = self.Profile.Archetype()
        flyusessod = self.FlyKeyAction() == 'SoD'

        if (self.Profile.HasPower('Flight', 'Fly')
                    or self.Profile.HasPower('Sorcery', 'Mystic Flight')
                    or archetype == "Peacebringer"):
            c['DefaultMode'].ShowEntryIf('Fly', flyusessod)
            self.ShowControlGroup(self.flySizer)

            c['FlyPower'].ShowEntryIf("Fly",           self.Profile.HasPower("Flight", 'Fly'))
            c['FlyPower'].ShowEntryIf("Mystic Flight", self.Profile.HasPower("Sorcery", 'Mystic Flight'))
            c['FlyPower'].ShowEntryIf("Energy Flight", archetype == "Peacebringer")
            self.PrePickLonePower(c['FlyPower'])
            c['FlyPower'].Enable(bool(self.FlyKeyAction()))

            c['HoverPower'].ShowEntryIf('Hover',         self.Profile.HasPower('Flight', 'Hover'))
            c['HoverPower'].ShowEntryIf('Combat Flight', archetype == "Peacebringer")
            c['HoverPower'].Show  (bool(self.FlyKeyAction()) and c['HoverPower'].GetCount() > 1)
            c['HoverPower'].Enable(bool(self.FlyKeyAction()) and c['HoverPower'].GetCount() > 1)

            c['FlyMode'].Show((self.GetState('FlyPower') or self.GetState('HoverPower')) and self.DefaultMode() != "Fly")
            c['FlyMode'].Enable(bool(self.FlyKeyAction()))

            c['FlyMode'].SetToolTip({
                'SoD' : 'Toggle Fly Speed on Demand Mode',
                'PT' : f'Toggle {c['FlyPower'].GetStringSelection()} on and off',
            }.get(self.FlyKeyAction(), ''))

            if (self.GetState('FlyPower') == "Fly"):
                # "fly_boost" below because "afterburner" has overloaded meaning in-game and reacts
                # weirdly (ie, fires the wrong power) if Afterburner isn't on a visible button
                # https://github.com/emersonrp/bindcontrol/issues/80#issuecomment-2585719489
                c['FlySpecialPower'].SetValue('fly_boost')
                c['FlySpecialKey'].CtlLabel.SetLabel('Afterburner:')
                c['FlySpecialKey'].SetToolTip('Activate Afterburner')

            if (archetype == "Peacebringer" and ((self.GetState('FlyPower') == 'Energy Flight') or bool(self.GetState('HoverPower')))):
                c['FlySpecialPower'].SetValue('Quantum Maneuvers')
                c['FlySpecialKey'].CtlLabel.SetLabel('Quantum Maneuvers:')
                c['FlySpecialKey'].SetToolTip('Activate Quantum Maneuvers')

            c['GFlyMode'].Show(self.HasGFly())
        else:
            self.ShowControlGroup(self.flySizer, False)
            c['DefaultMode'].ShowEntryIf('Fly', False)

        if evt: evt.Skip()

    def OnTeleportChanged(self, evt = None) -> None:
        c = self.Ctrls
        if (self.HasTPPowers()):
            self.ShowControlGroup(self.teleportSizer)
            c['TPPower'].ShowEntryIf('Teleport',      self.Profile.HasPower('Teleportation', 'Teleport'))
            c['TPPower'].ShowEntryIf('Translocation', self.Profile.HasPower('Sorcery', 'Translocation'))
            c['TPPower'].ShowEntryIf('Jaunt',         self.Profile.HasPower('Experimentation', 'Jaunt')
                                                        and self.GetState('SpeedPower') == "Speed of Sound")
            c['TPPower'].ShowEntryIf('Shadow Step',   self.Profile.Archetype() == "Warshade")
            self.PrePickLonePower(c['TPPower'])
            c['TPBindKey']  .Enable(bool(self.GetState('TPPower')))
            c['TPComboKey'] .Enable(bool(self.GetState('TPPower')))
            c['TPTPHover']  .Show(  bool(self.GetState('TPPower')) and bool(self.GetState('HoverPower')))
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
        if evt: evt.Skip()

    def OnKheldianChanged(self, evt = None) -> None:
        c = self.Ctrls
        if (self.IsKheldian()):
            # show kheldian sizer, enable controls
            self.ShowControlGroup(self.kheldianSizer)

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

        self.OnSpeedOnDemandChanged()

        self.OnSpeedChanged()

        self.OnJumpChanged()

        self.OnFlightChanged()

        self.OnTeleportChanged()

        self.Fit()

        self.Layout()

        if evt: evt.Skip()

    def MakeSoDFile(self, params: dict) -> None:

        profile = self.Profile

        t      = params['t']
        suffix = params.get('suffix', '')

        bl        = getattr(t, 'bl'        + suffix)
        bla       = getattr(t, 'bla'       + suffix)
        blf       = getattr(t, 'blf'       + suffix)
        path      = getattr(t, 'path'      + suffix)
        gamepath  = getattr(t, 'gamepath'  + suffix)
        patha     = getattr(t, 'patha'     + suffix)
        gamepatha = getattr(t, 'gamepatha' + suffix)
        pathf     = getattr(t, 'pathf'     + suffix)
        gamepathf = getattr(t, 'gamepathf' + suffix)

        mobile     = params.get('mobile')
        stationary = params.get('stationary')
        modestr    = params.get('modestr'    , '')
        flight     = params.get('flight'     , '')
        jumpfix    = params.get('jumpfix'    , False)
        turnoff    = params.get('turnoff'    , [ mobile, stationary ])
        sssj       = params.get('sssj'       , '')

        # if our current context is the Default Mode, and we're 000000,
        # write the keybinds to the reset file.
        if ((self.DefaultMode() == modestr) and (t.totalkeys == 0)):
            curfile = profile.ResetFile()

            self.sodUpKey     (t,bl,curfile,mobile,stationary,flight,'','',sssj)
            self.sodDownKey   (t,bl,curfile,mobile,stationary,flight,'','')
            self.sodForwardKey(t,bl,curfile,mobile,stationary,flight,'','',sssj)
            self.sodBackKey   (t,bl,curfile,mobile,stationary,flight,'','',sssj)
            self.sodLeftKey   (t,bl,curfile,mobile,stationary,flight,'','',sssj)
            self.sodRightKey  (t,bl,curfile,mobile,stationary,flight,'','',sssj)
            self.sodAutoRunKey(t,bla,curfile,mobile,sssj)
            self.sodFollowKey (t,blf,curfile,mobile,stationary)

            if (modestr != "NonSoD")      : self.makeNonSoDModeKey(t,"r", curfile,[ mobile,stationary ], False)
            if (modestr != "Sprint")      : self.makeSprintModeKey(t,"r", curfile,turnoff              ,jumpfix)
            if (modestr != "Fly")         : self.makeFlyModeKey   (t,"ff",curfile,turnoff              ,jumpfix)
            if (modestr != "Super Speed") : self.makeSpeedModeKey (t,"s", curfile,turnoff              ,jumpfix)
            if (modestr != "Jump")        : self.makeJumpModeKey  (t,"j", curfile,turnoff,path, gamepath)

            if (modestr != "GFly")        : self.makeGFlyModeKey  (t,"gf",curfile,turnoff              ,jumpfix)

        ### write the binds to the "current path/context + current key state" file
        curfile = profile.GetBindFile(f"{path}{t.KeyState()}.txt")

        self.sodResetKey(curfile,gamepath,self.actPower_toggle(stationary,mobile,True))

        self.sodUpKey     (t,bl,curfile,mobile,stationary,flight,'','',sssj)
        self.sodDownKey   (t,bl,curfile,mobile,stationary,flight,'','')
        self.sodForwardKey(t,bl,curfile,mobile,stationary,flight,'','',sssj)
        self.sodBackKey   (t,bl,curfile,mobile,stationary,flight,'','',sssj)
        self.sodLeftKey   (t,bl,curfile,mobile,stationary,flight,'','',sssj)
        self.sodRightKey  (t,bl,curfile,mobile,stationary,flight,'','',sssj)

        if (modestr != "NonSoD")      : self.makeNonSoDModeKey(t,"r", curfile,[ mobile,stationary ], False)
        if (modestr != "Sprint")      : self.makeSprintModeKey(t,"r", curfile,turnoff              ,jumpfix)
        if (flight == "Jump"):
            if (modestr != "Fly")     : self.makeFlyModeKey   (t,"a", curfile,turnoff              ,jumpfix,True)
        else:
            if (modestr != "Fly")     : self.makeFlyModeKey   (t,"ff",curfile,turnoff              ,jumpfix)
        if (modestr != "Super Speed") : self.makeSpeedModeKey (t,"s", curfile,turnoff              ,jumpfix)
        if (modestr != "Jump")        : self.makeJumpModeKey  (t,"j", curfile,turnoff,path,gamepath)

        self.sodAutoRunKey(t,bla,curfile,mobile,sssj)
        self.sodFollowKey(t,blf,curfile,mobile,stationary)

        # AutoRun Binds
        curfile = profile.GetBindFile(f"{patha}{t.KeyState()}.txt")

        self.sodResetKey(curfile,gamepath,self.actPower_toggle(stationary,mobile,True))

        self.sodUpKey     (t,bla,curfile,mobile,stationary,flight,1, '',sssj)
        self.sodDownKey   (t,bla,curfile,mobile,stationary,flight,1, '')
        self.sodForwardKey(t,bla,curfile,mobile,stationary,flight,bl,'',sssj)
        self.sodBackKey   (t,bla,curfile,mobile,stationary,flight,bl,'',sssj)
        self.sodLeftKey   (t,bla,curfile,mobile,stationary,flight,1, '',sssj)
        self.sodRightKey  (t,bla,curfile,mobile,stationary,flight,1, '',sssj)

        if (modestr != "NonSoD")      : self.makeNonSoDModeKey(t,"ar",curfile,[ mobile,stationary ], False)
        if (modestr != "Sprint")      : self.makeSprintModeKey(t,"gr",curfile,turnoff              ,jumpfix)
        if (modestr != "Super Speed") : self.makeSpeedModeKey (t,"as",curfile,turnoff              ,jumpfix)
        if (modestr != "Fly")         : self.makeFlyModeKey   (t,"af",curfile,turnoff              ,jumpfix)
        if (modestr != "Jump")        : self.makeJumpModeKey  (t,"aj",curfile,turnoff,patha,gamepatha)

        self.sodAutoRunOffKey(t,bl,curfile,mobile,stationary,flight)

        curfile.SetBind(self.Ctrls['Follow'].MakeBind('nop'))

        # FollowRun Binds
        curfile = profile.GetBindFile(f"{pathf}{t.KeyState()}.txt")

        self.sodResetKey(curfile,gamepath,self.actPower_toggle(stationary,mobile,True))

        self.sodUpKey     (t,blf,curfile,mobile,stationary,flight,'',bl,sssj)
        self.sodDownKey   (t,blf,curfile,mobile,stationary,flight,'',bl)
        self.sodForwardKey(t,blf,curfile,mobile,stationary,flight,'',bl,sssj)
        self.sodBackKey   (t,blf,curfile,mobile,stationary,flight,'',bl,sssj)
        self.sodLeftKey   (t,blf,curfile,mobile,stationary,flight,'',bl,sssj)
        self.sodRightKey  (t,blf,curfile,mobile,stationary,flight,'',bl,sssj)

        if (modestr != "NonSoD")      : self.makeNonSoDModeKey(t,"fr",curfile,[ mobile,stationary ], False)
        if (modestr != "Sprint")      : self.makeSprintModeKey(t,"fr",curfile,turnoff              ,jumpfix)
        if (modestr != "Super Speed") : self.makeSpeedModeKey (t,"fs",curfile,turnoff              ,jumpfix)
        if (modestr != "Fly")         : self.makeFlyModeKey   (t,"ff",curfile,turnoff              ,jumpfix)
        if (modestr != "Jump")        : self.makeJumpModeKey  (t,"fj",curfile,turnoff, pathf, gamepathf)

        curfile.SetBind(self.Ctrls['AutoRun'].MakeBind('nop'))

        self.sodFollowOffKey(t,bl,curfile,mobile,stationary,flight)

    def makeNonSoDModeKey(self, t, bl, file, toff, jumpfix, fb = '') -> None:
        key = t.NonSoDMode
        name = UI.Labels['NonSoDMode']
        if not self.Ctrls['NonSoDMode'].IsEnabled(): return
        if not key: return

        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Non-SoD Mode'
        else:                                      feedback = ''

        if (bl == "r"):
            bindload = t.BLF('n')
            if jumpfix:
                self.sodJumpFix(t,key, self.makeNonSoDModeKey,"n",bl,file,toff,'',feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(None,toff) + t.dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload = t.BLF('an')
            if jumpfix:
                self.sodJumpFix(t,key, self.makeNonSoDModeKey,"n",bl,file,toff,"a",feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(None,toff) + t.detailhi + t.runcamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if jumpfix:
                self.sodJumpFix(t,key, self.makeNonSoDModeKey,"n",bl,file,toff,"f",feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(None,toff) + t.detailhi + t.runcamdist + '$$up 0' + feedback + t.BLF('fn'))
        t.ini = ''

    def makeSprintModeKey(self, t, bl, file, toff, jumpfix, fb = '') -> None:
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

            if jumpfix:
                self.sodJumpFix(t,key, self.makeSprintModeKey,"r",bl,file,toff,'',feedback)
            else:
                file.SetBind(key, name, self, t.ini + ton + t.dirs('UDFBLR') + t.detailhi + t.runcamdist + feedback + bindload)

        elif (bl == "ar"):
            bindload  = t.BLF('gr')

            if jumpfix:
                self.sodJumpFix(t,key, self.makeSprintModeKey,"r",bl,file,toff,"a",feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.sprint,toff,start=True) + t.detailhi +  t.runcamdist + '$$up 0' + t.dirs('DLR') + feedback + bindload)

        else:
            if jumpfix:
                self.sodJumpFix(t,key, self.makeSprintModeKey,"r",bl,file,toff,"f",feedback)
            else:
                file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.sprint,toff,start=True) + t.detailhi + t.runcamdist + '$$up 0' + feedback + t.BLF('fr'))

        t.ini = ''

    def makeSpeedModeKey(self, t, bl, file, toff, jumpfix, fb = '') -> None:
        p = self.Profile
        key = t.SpeedMode
        name = UI.Labels['SpeedMode']
        if not self.Ctrls['SpeedMode'].IsEnabled(): return
        bindload = ''
        istoggle = self.SpeedKeyAction() == 'PT'

        feedback = ''
        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Superspeed Mode'

        if (self.GetState('SpeedPower')):
            if (bl == 's'):
                bindload = t.BLF('n') if istoggle else f"{t.bls}{t.KeyState()}.txt" # use non-sod if we're doing a simple toggle
                if jumpfix:
                    self.sodJumpFix(t,key,self.makeSpeedModeKey,"s",bl,file,toff,'',feedback)
                else:
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.speed,toff,start=True) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "as"):
                bindload = t.BLF('an') if istoggle else f"{t.blas}{t.KeyState()}.txt" # use non-sod if we're doing a simple toggle
                if jumpfix:
                    self.sodJumpFix(t,key,self.makeSpeedModeKey,"s",bl,file,toff,"a",feedback)
                elif (not feedback):
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.speed,toff,start=True) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload)
                else:
                    bindload  = f"{t.blas}{t.KeyState()}.txt"
                    bindload2 = f"{t.blas}{t.KeyState()}_s.txt"
                    tgl = p.GetBindFile(f"{t.pathas}{t.KeyState()}_s.txt")
                    file.SetBind(key, name, self, "+ $$" + t.ini + self.actPower_toggle(t.speed,toff,start=True) + t.dirs('UDLR') + t.detaillo + t.flycamdist + bindload2)
                    tgl.SetBind(key, name, self, "- $$" + feedback + bindload)

            else:  # bl == "fs"
                if jumpfix:
                    self.sodJumpFix(t,key,self.makeSpeedModeKey,"s",bl,file,toff,"f",feedback)
                else:
                    bindload = t.BLF('fn') if istoggle else f"{t.blfs}{t.KeyState()}.txt" # use non-sod if we're doing a simple toggle
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.speed,toff,start=True) + '$$up 0' +  t.detaillo + t.flycamdist + feedback + bindload)

        t.ini = ''

    def makeJumpModeKey(self, t, bl, file, toff, fpath, fbl) -> None:
        p = self.Profile
        key = t.JumpMode
        name = UI.Labels['JumpMode']
        if not self.Ctrls['JumpMode'].IsEnabled(): return
        if (t.canjmp and bool(self.JumpKeyAction())):
            istoggle = self.JumpKeyAction() == 'PT'

            feedback = '$$t $name, Super Jump Mode' if self.GetState('Feedback') else ''

            tglbl = t.BLF('n') if istoggle else f"$${BLF()} {fbl}{t.KeyState()}j.txt" # use non-sod if we're doing a simple toggle
            tgl   = p.GetBindFile(f"{fpath}{t.KeyState()}j.txt")

            if (bl == "j"):
                if (t.horizkeys + t.space > 0):
                    a = self.actPower_name(t.jump,toff) + '$$up 1'
                else:
                    a = self.actPower_name(t.cjmp,toff)

                tgl.SetBind(key, name, self, '-down' + a + t.detaillo + t.flycamdist + t.blj + t.KeyState() + ".txt")
                file.SetBind(key, name, self, '+down' + feedback + tglbl)
            elif (bl == "aj"):
                ajbl = t.blan if istoggle else t.blaj # use non-sod if we're doing a simple toggle
                tgl.SetBind(key, name, self, '-down' + self.actPower_name(t.jump,toff) + '$$up 1' + t.detaillo + t.flycamdist + t.dirs('DLR') + ajbl + t.KeyState() + ".txt")
                file.SetBind(key, name, self, '+down' + feedback + tglbl)
            else:
                fjbl = t.blfn if istoggle else t.blfj # use non-sod if we're doing a simple toggle
                tgl.SetBind(key, name, self, '-down' + self.actPower_name(t.jump,toff) + '$$up 1' + t.detaillo + t.flycamdist + fjbl + t.KeyState() + ".txt")
                file.SetBind(key, name, self, '+down' + feedback + tglbl)

        t.ini = ''

    def makeFlyModeKey(self, t, bl, file, toff, jumpfix, fb = False, fb_on_a = False) -> None:
        key = t.FlyMode
        name = UI.Labels['FlyMode']
        if not self.Ctrls['FlyMode'].IsEnabled(): return
        if not key: return

        if (not fb) and self.GetState('Feedback'): feedback = '$$t $name, Flight Mode'
        else:                                      feedback = ''

        istoggle = self.FlyKeyAction() == 'PT'

        if (t.canhov or t.canfly):
            if (bl == "a"):
                if (not fb_on_a): feedback = ''
                bindload = t.BLF('n') if istoggle else t.bla + t.KeyState() + ".txt" # use non-sod if we're doing a simple toggle

                if t.totalkeys: ton = t.flyx
                else:           ton = t.hover

                if jumpfix:
                    self.sodJumpFix(t,key,self.makeFlyModeKey,"f",bl,file,toff,'',feedback)
                else:
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(ton,toff,start=True) + t.dirs('UDLR') + t.detaillo + t.flycamdist + feedback + bindload)

            elif (bl == "af"):
                bindload = t.BLF('an') if istoggle else t.blaf + t.KeyState() + ".txt" # use non-sod if we're doing a simple toggle
                if jumpfix:
                    self.sodJumpFix(t,key,self.makeFlyModeKey,"f",bl,file,toff,"a",feedback)
                else:
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.flyx,toff,start=True) + t.detaillo + t.flycamdist + t.dirs('DLR') + feedback + bindload)

            else: # bl == "ff"
                bindload = t.BLF('fn') if istoggle else t.blff + t.KeyState() + ".txt" # use non-sod if we're doing a simple toggle
                if jumpfix:
                    self.sodJumpFix(t,key,self.makeFlyModeKey,"f",bl,file,toff,"f",feedback)
                else:
                    file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.flyx,toff,start=True) + t.dirs('UDFBLR') + t.detaillo + t.flycamdist + feedback + bindload)

        t.ini = ''

    def makeGFlyModeKey(self, t, bl, file, toff, jumpfix) -> None:
        key = t.GFlyMode
        name = UI.Labels['GFlyMode']
        if not self.Ctrls['GFlyMode'].IsEnabled(): return

        if t.cangfly:
            if (bl == "gbo"):
                bindload = t.BLF('gbo')
                if jumpfix:
                    self.sodJumpFix(t,key,self.makeGFlyModeKey,"gf",bl,file,toff,'','')
                else:
                    file.SetBind(key, name, self, t.ini + '$$up 1$$down 0' + self.actPower_toggle(t.gfly,toff) + t.dirs('FBLR') + t.detaillo + t.flycamdist + bindload)

            elif (bl == "gaf"):
                bindload = t.BLF('gaf')
                if jumpfix:
                    self.sodJumpFix(t,key,self.makeGFlyModeKey,"gf",bl,file,toff,"a")
                else:
                    file.SetBind(key, name, self, t.ini + t.detaillo + t.flycamdist + t.dirs('UDLR') + bindload)

            else:
                if jumpfix:
                    self.sodJumpFix(t,key,self.makeGFlyModeKey,"gf",bl,file,toff,"f")
                else:
                    if (bl == "gf"):
                        file.SetBind(key, name, self, t.ini + self.actPower_toggle(t.gfly,toff,start=True) + t.detaillo + t.flycamdist + t.BLF('gff'))
                    else:
                        file.SetBind(key, name, self, t.ini + t.detaillo + t.flycamdist + t.BLF('gff'))

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
        if (cpower and not jpower):
            t.cjmp  = cpower
            t.jump  = cpower
        elif jpower and not cpower:
            t.jump       = jpower
            t.jumpifnocj = jpower
        elif cpower and jpower:
            t.cjmp   = cpower
            t.jump   = jpower

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
                turn = 'playerturn' if self.GetState('PlayerTurn') else ''
                resetfile.SetBind(self.Ctrls['Forward'].MakeBind(["+forward", turn]))
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

        if self.IsKheldian(): self.DoKheldianBinds(t, tpActivator, windowhide, windowshow)

        ###### Basic travel power binds, not SoD
        # OK, first, let's do these trivial toggle binds if and only if we aren't doing SoD at all
        # The SoD case is handled inside make*ModeKey()
        if not self.HasAnySoD():
            if self.SpeedKeyAction() == "PT":
                spower = self.GetState("SpeedPower")
                resetfile.SetBind(self.Ctrls["FlyMode"].MakeBind(f'powexecname "{spower}"'))

            if self.JumpKeyAction() == 'PT':
                jpower = self.GetState('JumpPower')
                cpower = self.GetState('CJPower')
                if jpower and cpower:
                    resetfile.SetBind(self.Ctrls['JumpMode'].MakeBind(f'powexecname "{jpower}"$$powexecname "{cpower}"'))
                elif jpower:
                    resetfile.SetBind(self.Ctrls['JumpMode'].MakeBind(f'powexecname "{jpower}"'))
                elif cpower:
                    resetfile.SetBind(self.Ctrls['JumpMode'].MakeBind(f'powexecname "{cpower}"'))

            if self.FlyKeyAction() == 'PT':
                fpower = self.GetState('FlyPower')
                hpower = self.GetState('HoverPower')
                if fpower and hpower:
                    resetfile.SetBind(self.Ctrls['FlyMode'].MakeBind(f'powexecname "{fpower}"$$powexecname "{hpower}"'))
                elif fpower:
                    resetfile.SetBind(self.Ctrls['FlyMode'].MakeBind(f'powexecname "{fpower}"'))
                elif hpower:
                    resetfile.SetBind(self.Ctrls['FlyMode'].MakeBind(f'powexecname "{hpower}"'))

        ###### Teleport Binds
        teamTPPower = 'Team Teleport' if self.HasTTP() else ''
        normalTPPower = 'Shadow Step' if archetype == 'Warshade' else self.GetState('TPPower')

        # I'm not sure why we create these nop binds.  Are they necessary?
        if (self.HasTPPowers() and not normalTPPower):
            resetfile.SetBind(self.Ctrls['TPBindKey'].MakeBind('nop'))
            resetfile.SetBind(self.Ctrls['TPComboKey'].MakeBind('nop'))
            if server == "Rebirth":
                resetfile.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('nop'))

        # We did kheldian tp binds inside DoKheldianBinds()
        if (self.HasTPPowers() and normalTPPower and (archetype != "Peacebringer")):
            tphovermodeswitch = ''
            if t.tphover:
                tphovermodeswitch = getattr(t, 'blf') + "000000.txt"

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

        # normal non-peacebringer team teleport binds
        if (self.HasTPPowers() and self.HasTTP() and (archetype != "Peacebringer") and teamTPPower) :

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
    def DoKheldianBinds(self, t, tpActivator, windowhide, windowshow):
        profile   = self.Profile
        archetype = profile.Archetype()
        resetfile = profile.ResetFile()
        server    = profile.Server()

        #  create the Nova and Dwarf form support files if enabled.
        if archetype == "Peacebringer":
            novaPower = "Bright Nova"
            dwarfPower = "White Dwarf"
            humanFormShield = "Shining Shield"
            dwarfTPPower = "White Dwarf Step"
        else: # Warshade
            novaPower = "Dark Nova"
            dwarfPower = "Black Dwarf"
            humanFormShield = "Gravity Shield"
            dwarfTPPower = "Black Dwarf Step"

        fullstop = '$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'

        if self.GetState('NovaMode'):
            khelfeedback = f"t $name, Changing to {novaPower} Form" if self.GetState('KhelFeedback') else ''
            resetfile.SetBind(self.Ctrls['NovaMode'].MakeBind(f"{khelfeedback}{fullstop}{t.on}{novaPower}$$gototray {self.GetState('NovaTray')}" + profile.BLF('nova.txt')))

            novafile = profile.GetBindFile("nova.txt")

            if (bool(self.GetState('DwarfMode'))):
                khelfeedback = f"t $name, Changing to {dwarfPower} Form" if self.GetState('KhelFeedback') else ''
                novafile.SetBind(self.Ctrls['DwarfMode'].MakeBind(f"{khelfeedback}{fullstop}{t.off}{novaPower}{t.on}{dwarfPower}$$gototray {self.GetState('DwarfTray')}" + profile.BLF('dwarf.txt')))

            humpower = f'$${self.togon} {humanFormShield}' if self.GetState('UseHumanFormPower') else ''

            khelfeedback = "t $name, Changing to Human Form, SoD Mode" if self.GetState('KhelFeedback') else ''
            novafile.SetBind(self.Ctrls['NovaMode'].MakeBind(f"{khelfeedback}{fullstop}$${self.togoff} {novaPower}{humpower}$$gototray {self.GetState('HumanTray')}" + profile.BLF('reset.txt')))

            novafile.SetBind(self.Ctrls['Forward'].MakeBind("+forward"))
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

        if self.GetState('UseDwarf'):
            khelfeedback = f"t $name, Changing to {dwarfPower} Form" if self.GetState('KhelFeedback') else ''
            resetfile.SetBind(self.Ctrls['DwarfMode'].MakeBind(f"{khelfeedback}{fullstop}$${self.togon} {dwarfPower}$$gototray {self.GetState('DwarfTray')}" + profile.BLF('dwarf.txt')))
            dwrffile = profile.GetBindFile("dwarf.txt")
            if (bool(self.GetState('NovaMode'))):
                khelfeedback = f"t $name, Changing to {novaPower} Form" if self.GetState('KhelFeedback') else ''
                dwrffile.SetBind(self.Ctrls['NovaMode'].MakeBind(f"{khelfeedback}{fullstop}$${self.togoff} {dwarfPower}$${self.togon} {novaPower}$$gototray {self.GetState('NovaTray')}" + profile.BLF('nova.txt')))

            humpower = f'$${self.togon} {humanFormShield}' if self.GetState('UseHumanFormPower') else ''

            khelfeedback = "t $name, Changing to Human Form, SoD Mode" if self.GetState('KhelFeedback') else ''
            dwrffile.SetBind(self.Ctrls['DwarfMode'].MakeBind(f"{khelfeedback}{fullstop}$${self.togoff} {dwarfPower}{humpower}$$gototray 1" + profile.BLF('reset.txt')))

            dwrffile.SetBind(self.Ctrls['Forward'].MakeBind("+forward"))
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

            # TODO:  this should get DRY'ed up with the normal teleport logic
            if dwarfTPPower:
                tphovermodeswitch = ''
                if t.tphover:
                    tphovermodeswitch = t.bla + "000000.txt"

                dwrffile.SetBind(self.Ctrls['TPBindKey'].MakeBind(tpActivator + dwarfTPPower))

                tp_off = profile.GetBindFile("dtp","tp_off.txt")
                tp_on1 = profile.GetBindFile("dtp","tp_on1.txt")
                zoomin = '' if t.tphover else t.detailhi + t.runcamdist

                dwrffile.SetBind(self.Ctrls['TPComboKey'].MakeBind('+first$$-first$$powexecname ' + dwarfTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('dtp','tp_on1.txt')))
                if server == 'Homecoming':
                    tp_off.SetBind(self.Ctrls['TPComboKey'].MakeBind('+first$$-first$$powexecname ' + dwarfTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('dtp','tp_on1.txt')))

                    tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeBind(f'+first$$-first$${self.unqueue}$$powexeclocation cursor' + dwarfTPPower + zoomin + windowshow + profile.BLF('dtp','tp_off.txt') + tphovermodeswitch))

                else:  # server == Rebirth
                    tp_off.SetBind(self.Ctrls['TPComboKey'].MakeBind('+ $$powexecname ' + dwarfTPPower + t.detaillo + t.flycamdist + windowhide + profile.BLF('dtp','tp_on1.txt')))
                    tp_off.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('nop'))

                    tp_on1.SetBind(self.Ctrls['TPComboKey'].MakeBind(f'- {self.unqueue}' + zoomin + windowshow + profile.BLF('dtp','tp_off.txt') + tphovermodeswitch))
                    tp_on1.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('+ ' + profile.BLF('dtp','tp_on2.txt')))

                    tp_on2 = profile.GetBindFile("dtp","tp_on2.txt")
                    tp_on2.SetBind(self.Ctrls['TPExecuteKey'].MakeBind('- $$powexecname ' + dwarfTPPower + profile.BLF('dtp','tp_on1.txt')))

    def DoSpeedOnDemandBinds(self, t) -> None:
        profile   = self.Profile
        resetfile = profile.ResetFile()
        config    = wx.ConfigBase.Get()

        keybindreset = 'keybind_reset' if config.ReadBool('FlushAllBinds') else ''
        resetfile.SetBind(config.Read('ResetKey'), "Reset Key", self.TabTitle,
                    [
                        keybindreset,
                        resetfile.BLF(),
                        'up 0', 'down 0', 'forward 0', 'backward 0', 'left 0', 'right 0',
                        'powexecname Sprint',
                        self.unqueue,
                        't $name, Binds Reset',
                    ])

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

                                ### NonSoD Mode
                                if self.HasAnySoD():
                                    setattr(t, self.DefaultMode() + "Mode", t.NonSoDMode) # why do we need this?
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'suffix'     : 'n',
                                        'mobile'     : None,
                                        'stationary' : None,
                                        'modestr'    : "NonSoD",
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                ### Sprint Mode
                                if self.SoDEnabled() and self.GetState('SprintPower'):
                                    setattr(t, self.DefaultMode() + "Mode", t.SprintMode) # why do we need this?
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'suffix'     : 'r',
                                        'mobile'     : t.sprint,
                                        'stationary' : None,
                                        'modestr'    : "Sprint",
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                ### Speed Mode
                                if self.SpeedKeyAction():
                                    setattr(t, self.DefaultMode() + "Mode", t.SpeedMode) # why do we need this?
                                    sssj = t.jump if self.GetState('SSSJModeEnable') else None
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'suffix'     : 's',
                                        'mobile'     : t.speed,
                                        'stationary' : None, # I think we want no stationary power with SS anymore
                                        'modestr'    : "Super Speed",
                                        'sssj'       : sssj,
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                ### Jump Mode
                                if self.JumpKeyAction():
                                    setattr(t, self.DefaultMode() + "Mode", t.JumpMode) # why do we need this?
                                    jturnoff = None if (t.jump == t.cjmp) else {t.jumpifnocj}
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'suffix'     : 'j',
                                        'mobile'     : t.jump,
                                        'stationary' : t.cjmp,
                                        'modestr'    : "Jump",
                                        'flight'     : "Jump",
                                        'jumpfix'    : True,
                                        'turnoff'    : jturnoff,
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                ### Fly Mode
                                if self.FlyKeyAction() and (t.canhov or t.canfly):
                                    setattr(t, self.DefaultMode() + "Mode", t.FlyMode) # why do we need this?
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'suffix'     : 'f',
                                        'mobile'     : t.flyx,
                                        'stationary' : t.hover,
                                        'modestr'    : "Fly",
                                        'flight'     : t.fly,
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

                                ### GFly Mode
                                if t.cangfly:
                                    setattr(t, self.DefaultMode() + "Mode", t.GFlyMode) # why do we need this?
                                    self.MakeSoDFile({
                                        't'          : t,
                                        'suffix'     : 'gf',
                                        'mobile'     : t.gfly,
                                        'stationary' : t.gfly,
                                        'modestr'    : "GFly",
                                        'flight'     : "GFly",
                                    })
                                    setattr(t, self.DefaultMode() + "Mode", None)

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

    def sodResetKey(self, curfile, gamepath, turnoff) -> None:

        config = wx.ConfigBase.Get()

        keybindreset = 'keybind_reset' if config.ReadBool('FlushAllBinds') else ''
        curfile.SetBind(config.Read('ResetKey'), UI.Labels['ResetKey'], self,
            [
                keybindreset,
                'up 0', 'down 0', 'forward 0', 'backward 0', 'left 0', 'right 0',
                str(turnoff),
                't $name, Binds Reset',
                self.Profile.ResetFile().BLF(),
                f"{BLF()} {gamepath}000000.txt"
            ]
        )

    def sodUpKey(self, t, bl, curfile, mobile, stationary, flight, autorun, followbl, sssj) -> None:

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

        newbits = t.KeyState({'toggle' : 'space'})
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

    def sodDownKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl) -> None:
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

        newbits = t.KeyState({'toggle' : 'X'})
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

    def sodForwardKey(self, t, bl, curfile,  mobile, stationary, flight, autorunbl, followbl, sssj) -> None:
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

    def sodBackKey(self,t,bl,curfile,mobile,stationary,flight,autorunbl,followbl,sssj) -> None:
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

    def sodLeftKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,sssj) -> None:
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

            curfile.SetBind(self.Ctrls['Left'].MakeBind(move + bl))
        elif (not autorun) :
            curfile.SetBind(self.Ctrls['Left'].MakeBind(f"{ini}{up}{dow}{forw}{bac}{lefx}{rig}{mouselook}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Left'].MakeBind(f"{ini}{up}{dow}{'$$backward 0'}{lefx}{rig}{t.mouselookon}{bl}"))

    def sodRightKey(self,t,bl,curfile,mobile,stationary,flight,autorun,followbl,sssj) -> None:
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

            curfile.SetBind(self.Ctrls['Right'].MakeBind(move + bl))
        elif (not autorun) :
            curfile.SetBind(self.Ctrls['Right'].MakeBind(f"{ini}{up}{dow}{forw}{bac}{lef}{rigx}{mouselook}{toggle}{bl}"))
        else:
            curfile.SetBind(self.Ctrls['Right'].MakeBind(f"{ini}{up}{dow}$$forward 1$$backward 0{lef}{rigx}{t.mouselookon}{bl}"))

    def sodAutoRunKey(self,t,bl,curfile,mobile,sssj) -> None:
        bindload = bl + t.KeyState() + ".txt"
        if (sssj and t.space == 1) :
            curfile.SetBind(self.Ctrls['AutoRun'].MakeBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mouselookon + self.actPower_name(sssj,mobile) + bindload))
        else:
            curfile.SetBind(self.Ctrls['AutoRun'].MakeBind('forward 1$$backward 0' + t.dirs('UDLR') + t.mouselookon + self.actPower_name(mobile) + bindload))

    # TODO sssj never gets passed in, in citybinder.  Is this right?
    def sodAutoRunOffKey(self, t,bl,curfile,mobile,stationary,flight,sssj = None) -> None:
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
        curfile.SetBind(self.Ctrls['AutoRun'].MakeBind(t.dirs('UDFBLR')[2:] + toggleon + bindload))

    def sodFollowKey(self, t,bl,curfile,mobile,stationary) -> None:
        curfile.SetBind(self.Ctrls['Follow'].MakeBind('follow' + self.actPower_toggle(mobile,stationary) + bl + t.KeyState() + '.txt'))

    def sodFollowOffKey(self, t,bl,curfile,mobile,stationary,flight) -> None:
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
    def actPower_toggle(self, on, off, start = False) -> str:
        s = ''

        offpower = set()

        if off and not isinstance(off, str):
            for w in off:
                if (w and w != on and (w not in offpower)):
                    offpower.add(w)
                    s = s + f'$${self.togoff} {w}'

        else:
            if (off and (off != on) and (off not in offpower)):
                offpower.add(off)
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

        if s:
            s = s + f'$${self.unqueue}'

        if on:
            s = s + '$$powexecname ' + on + '$$powexecname ' + on

        return s

    # This seems to be used when making keys for jump mode, triggered inside various make*ModeKey subs to do its
    # thing instead of the normal SetBind() in there.  It also takes in 'makeModeKey' which is always a reference
    # back to the calling method, and it calls that with different parameters, so it seems to make two binds, one
    # here and one inside the "callback" which isn't really one.  This -seems- to be in order to convert what
    # might otherwise be a simple powexec bind into a two-file toggle one, but why?
    #
    # The reason and thinking for all of this is still not clear to me after fifteen years.  RP 2025
    def sodJumpFix(self, t,key,makeModeKey,suffix,bl,curfile,turnoff,autofollowmode,feedback = '') -> None:
        profile = self.Profile

        filename     = str(getattr(t,"path"     + f"{autofollowmode}j")) + t.KeyState() + suffix + '.txt'
        gamefilename = str(getattr(t,"gamepath" + f"{autofollowmode}j")) + t.KeyState() + suffix + '.txt'
        tglfile      = profile.GetBindFile(filename)
        t.ini        = '-down$$'
        makeModeKey(t,bl,tglfile,turnoff,None,1)
        # TODO TODO TODO do we need to do anything in here for when we're making simple toggle binds?  Probably.
        curfile.SetBind(key, "Jump Fix", self, "+down" + feedback + self.actPower_name(t.cjmp) + profile.BLF(gamefilename))

    ### convenience methods
    def SoDEnabled(self) -> bool:
        return self.Ctrls['EnableSoD'].IsChecked()

    def DefaultMode(self) -> str:
        return self.Ctrls['DefaultMode'].GetStringSelection()

    def HasGFly(self) -> bool:
        return self.Profile.HasPower('Flight', 'Group Fly')

    def HasTPPowers(self):
        return (self.Profile.HasPower('Teleportation', 'Teleport')
                    or self.Profile.HasPower('Sorcery', 'Translocation')
                    or self.Profile.HasPower('Experimentation', 'Jaunt')
                    or self.Profile.Archetype() == "Warshade"
                )

    def HasTTP(self) -> bool:
        return self.Profile.HasPower('Teleportation', 'Team Teleport')

    def HasAnySoD(self) -> bool:
        return (
            self.SoDEnabled() and (
                (self.Ctrls['JumpKeyAction'] .IsShown() and self.JumpKeyAction()  == 'SoD')
                    or
                (self.Ctrls['FlyKeyAction']  .IsShown() and self.FlyKeyAction()   == 'SoD')
                    or
                (self.Ctrls['SpeedKeyAction'].IsShown() and self.SpeedKeyAction() == 'SoD')
            )
        )

    def IsKheldian(self) -> bool:
        return bool(self.Profile.Archetype() in ("Warshade", "Peacebringer"))

    # Let's DRY these next three up somehow
    def JumpKeyAction(self):
        return {
            'Speed on Demand' : 'SoD',
            'Power Toggle'    : 'PT',
        }.get(self.Ctrls['JumpKeyAction'].GetStringSelection(), '')

    def FlyKeyAction(self):
        return {
            'Speed on Demand' : 'SoD',
            'Power Toggle'    : 'PT',
        }.get(self.Ctrls['FlyKeyAction'].GetStringSelection(), '')

    def SpeedKeyAction(self):
        return {
            'Speed on Demand' : 'SoD',
            'Power Toggle'    : 'PT',
        }.get(self.Ctrls['SpeedKeyAction'].GetStringSelection(), '')

    def AllBindFiles(self) -> dict[str, list]:
        files = []
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
    'SprintPower'    : 'Preferred Sprint Power',
    'SprintMode'     : "Switch to Sprint SoD Mode",
    'MouseChord'     : 'Mousechord is SoD Forward',
    'Feedback'       : 'Self-/tell when changing SoD mode',

    'SpeedKeyAction'    : "Speed Power Key Action",
    'SpeedPower'        : "Primary Speed Power",
    'SpeedMode'         : 'Speed Power Key',
    'SSSJModeEnable'    : 'Enable Super Speed / Super Jump Mode',
    'SpeedSpecialKey'   : '',
    'SpeedSpecialPower' : '', # Hidden

    'JumpKeyAction'    : "Jump Power Key Action",
    'JumpPower'        : "Primary Jump Power",
    'CJPower'          : "Defensive Jump Power",
    'JumpMode'         : 'Jump Power Key',
    'JumpSpecialKey'   : '',
    'JumpSpecialPower' : '', # hidden

    'FlyKeyAction'    : "Fly Power Key Action",
    'FlyPower'        : "Primary Fly Power",
    'HoverPower'      : "Defensive Fly Power",
    'FlyMode'         : 'Fly Power Key',
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
