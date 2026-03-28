import wx
import UI
from UI.BindWizard import WizardParent
from UI.ControlGroup import ControlGroup
from UI.CGControls import bcKeyButton, cgStaticText

class BaseEditMode(WizardParent):
    WizardName  = 'Base Edit Mode'
    WizToolTip  = 'Switch to and from a set of controls optimized for base editing'
    WizHelpFile = 'BaseEditMode.html'
    IconPath    = ('UI', 'BaseEditMode')

    def __init__(self, parent, init):
        super().__init__(parent, init)

        # All of this is so we can use ControlGroup.  Maybe that's a false economy.
        for k,v in {
            'BEDisableMovement' : 'Default Movement Keys',
            'BEDisableChat'     : 'Disable Chat Keys',
            'BEExitEditMode'    : 'Exit Edit Mode',
            'BEGridCycle'       : 'Cycle Placement Grid Sizes',
            'BEAngleCycle'      : 'Cycle Rotation Snap Angle',
            'BEClipCycle'       : 'Toggle Wall Clipping',
            'BEAttachCycle'     : 'Cycle Object Attachment',
            'BEUndo'            : 'Undo last Action',
            'BERedo'            : 'Redo last Undo / Repeat Action',
            'BESelect'          : 'Select Base Item Under Cursor',
            'BESelectNext'      : 'Select Next Base Item',
            'BESelectLast'      : 'Select Previous Base Item',
            'BESell'            : 'Delete Selected / Targeted Item',
            'BECenterCur'       : 'Center View At Cursor Location',
            'BECenterSel'       : 'Center View On Selected Base Item',
            'BERotateCCW'       : 'Rotate Selected Object 90° CCW',
            'BERotateCW'        : 'Rotate Selected Object 90° CW',
            'BESeeEverything'   : 'Toggle seeing hidden markers',
        }.items():
            UI.Labels[self.BindPane.MakeCtrlName(k)] = v

        for k,v in {
            'BEExitEditMode'  : '',
            'BEGridCycle'     : 'F1',
            'BEAngleCycle'    : 'F2',
            'BEClipCycle'     : 'F3',
            'BEAttachCycle'   : 'F5',
            'BEUndo'          : 'CTRL+Z',
            'BERedo'          : 'CTRL+Y',
            'BESelect'        : '',
            'BESelectNext'    : 'TAB',
            'BESelectLast'    : 'SHIFT+TAB',
            'BESell'          : '',
            'BECenterCur'     : '',
            'BECenterSel'     : '',
            'BERotateCCW'     : '',
            'BERotateCW'      : '',
            'BESeeEverything' : '',
        }.items():
            self.Profile.CustomBinds.Init[self.BindPane.MakeCtrlName(k)] = v

    def BuildUI(self, dialog, init : dict|None = None) -> wx.Sizer:
        wizdata = {}
        if init: wizdata = init.get('WizData', {})

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        optsSizer = ControlGroup(dialog, self.Profile.CustomBinds, label = 'Options')

        self.BEDisableMovement = optsSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = self.BindPane.MakeCtrlName('BEDisableMovement'),
            tooltip = 'Disable SoD etc, returning movement keys to their defaults',
        )
        self.BindPane.SetCtrl('BEDisableMovement', self.BEDisableMovement)
        self.BEDisableMovement.SetValue(bool(wizdata.get('BEDisableMovement'))) # pyright: ignore

        self.BEDisableChat = optsSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = self.BindPane.MakeCtrlName('BEDisableChat'),
            tooltip = 'Disable keys that will pop up the chat window',
        )
        self.BindPane.SetCtrl('BEDisableChat', self.BEDisableChat)
        self.BEDisableChat.SetValue(bool(wizdata.get('BEDisableChat'))) # pyright: ignore

        ### KEY SIZER
        keysSizer = ControlGroup(dialog, self.Profile.CustomBinds, label = 'Keybinds', width = 4)

        self.BEExitEditMode = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BEExitEditMode'),
            tooltip = 'Exit Base Edit mode and return to normal keybinds',
        )
        self.BindPane.SetCtrl('BEExitEditMode', self.BEExitEditMode)

        self.BEGridCycle = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BEGridCycle'),
            tooltip = 'Cycle through object placement grid sizes',
        )
        self.BindPane.SetCtrl('BEGridCycle', self.BEGridCycle)

        self.BEUndo = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BEUndo'),
            tooltip = 'Undo last action',
        )
        self.BindPane.SetCtrl('BEUndo', self.BEUndo)

        self.BEAngleCycle = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BEAngleCycle'),
            tooltip = 'Cycle through snap-drag rotation angle settings',
        )
        self.BindPane.SetCtrl('BEAngleCycle', self.BEAngleCycle)

        self.BERedo = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BERedo'),
            tooltip = 'Redo last undo / repeat action',
        )
        self.BindPane.SetCtrl('BERedo', self.BERedo)

        self.BEClipCycle = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BEClipCycle'),
            tooltip = 'Toggle wall clipping',
        )
        self.BindPane.SetCtrl('BEClipCycle', self.BEClipCycle)

        self.BESelect = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BESelect'),
            tooltip = 'Select base item under cursor',
        )
        self.BindPane.SetCtrl('BESelect', self.BESelect)

        self.BEAttachCycle = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BEAttachCycle'),
            tooltip = 'Cycle through object placement attachment (floor, wall, ceiling, surface)',
        )
        self.BindPane.SetCtrl('BEAttachCycle', self.BEAttachCycle)

        self.BESelectNext = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BESelectNext'),
            tooltip = 'Select next base item',
        )
        self.BindPane.SetCtrl('BESelectNext', self.BESelectNext)

        self.BERotateCCW = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BERotateCCW'),
            tooltip = 'Rotate selected item 90° CCW',
        )
        self.BindPane.SetCtrl('BERotateCCW', self.BERotateCCW)

        self.BESelectLast = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BESelectLast'),
            tooltip = 'Select previous base item',
        )
        self.BindPane.SetCtrl('BESelectLast', self.BESelectLast)

        self.BERotateCW = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BERotateCW'),
            tooltip = 'Rotate selected item 90° CW',
        )
        self.BindPane.SetCtrl('BERotateCW', self.BERotateCW)

        self.BECenterCur = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BECenterCur'),
            tooltip = 'Center view on cursor',
        )
        self.BindPane.SetCtrl('BECenterCur', self.BECenterCur)

        self.BESell = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BESell'),
            tooltip = 'Delete currently selected / targeted item',
        )
        self.BindPane.SetCtrl('BESell', self.BESell)

        self.BECenterSel = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BECenterSel'),
            tooltip = 'Center view on selected base item',
        )
        self.BindPane.SetCtrl('BECenterSel', self.BECenterSel)

        self.BESeeEverything = keysSizer.AddControl(
            ctlType = 'keybutton',
            ctlName = self.BindPane.MakeCtrlName('BESeeEverything'),
            tooltip = 'Toggle seeing hidden items',
        )
        self.BindPane.SetCtrl('BESeeEverything', self.BESeeEverything)


        mainSizer.Add(optsSizer, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(keysSizer, 0, wx.EXPAND|wx.ALL, 5)

        return mainSizer

    def Serialize(self):
        return self.State.get('WizData', {})

    def PaneContents(self):
        bindpane = self.BindPane
        panel = wx.Panel(bindpane.GetPane())
        panel.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)

        cmdSizer = wx.GridSizer(2, 4, 5, 5)
        cmdPanel = wx.Panel(panel)
        cmdPanel.SetSizer(cmdSizer)
        cmdPanel.SetToolTip(self.BindString())
        for cmd in ('BEDisableMovement', ):
            ctpanel = wx.Panel(cmdPanel)
            ctsizer = wx.BoxSizer(wx.HORIZONTAL)
            ctpanel.SetSizer(ctsizer)
            cmdtext = cgStaticText(ctpanel, label = UI.Labels[self.BindPane.MakeCtrlName(cmd)], style = wx.ALIGN_CENTER)
            if self.State.get('WizData', {}).get(cmd):
                cmdtext.SetLabel("✓ " + UI.Labels[cmd])
            else:
                cmdtext.SetForegroundColour(wx.Colour(160, 160, 160))
            ctsizer.Add(cmdtext, 1, wx.EXPAND|wx.ALL, 5)
            cmdSizer.Add(ctpanel, 1, wx.EXPAND)

            ctpanel.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
            cmdtext.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)

        panelSizer.Add(cmdPanel, 1, wx.ALIGN_CENTER|wx.ALL, 15)
        cmdPanel.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)

        # BindStringDisplay = cgStaticText(panel, label = self.BindString())
        # panelSizer.Add(BindStringDisplay, 1, wx.ALIGN_CENTER|wx.ALL, 10)
        # BindStringDisplay.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)

        bkText = cgStaticText(panel, label = 'Bind Key:')
        panelSizer.Add(bkText, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5)
        bkText.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)

        EnterEditModeKeyName = bindpane.MakeCtrlName('EnterEditMode')
        self.EnterEditModeKey = bcKeyButton(panel, init = {
            'CtlName' : EnterEditModeKeyName,
            'Page'    : bindpane.Page,
        })
        panelSizer.Add(self.EnterEditModeKey, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        bindpane.SetCtrl('EditMode', self.EnterEditModeKey)
        UI.Labels[self.EnterEditModeKey] = 'Enter Edit Mode'

        panel.SetSizer(panelSizer)

        return panel

    def UpdateState(self):
        self.State = { 'WizData' : {
            'BEDisableMovement'    : self.BEDisableMovement   .GetValue(), # pyright: ignore
        } }

    def PopulateBindFiles(self):
        self.Profile.ResetFile().SetBind(self.EnterEditModeKey.Key, 'Escape Configurator', self.Profile.CustomBinds, self.BindString())

    def BindString(self) -> str:
        commands = []
        #wizdata = self.State.get('WizData', {})

        return '$$'.join(commands)

    def AllBindFiles(self):
        return {
            'files' : [],
            'dirs'  : [],
        }
