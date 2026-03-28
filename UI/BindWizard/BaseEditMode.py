import wx
import UI
from UI.BindWizard import WizardParent
from UI.ControlGroup import ControlGroup
from UI.CGControls import bcKeyButton, cgStaticText
from UI.KeySelectDialog import EVT_KEY_CHANGED

class BaseEditMode(WizardParent):
    WizardName  = 'Base Edit Mode'
    WizToolTip  = 'Switch to and from a set of controls optimized for base editing'
    WizHelpFile = 'BaseEditMode.html'
    IconPath    = ('UI', 'BaseEditMode')

    def __init__(self, parent, init):
        super().__init__(parent, init)

        # we use this also to serialize, below
        self.AllCtrls = {
            'EnterEditMode'     : 'Toggle Base Edit Mode',
            'BEDisableMovement' : 'Default Movement Keys',
            'BEDisableChat'     : 'Disable Chat Keys',
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
            'BESetBaseLighting' : 'Rotate Through Base Lighting Options',
        }
        for k,v in self.AllCtrls.items():
            UI.Labels[self.BindPane.MakeCtrlName(k)] = v

        # we use this as a list, below, to initialize and later to conflict-check these.
        # Order matters here for layout.
        self.KeyInit = {
            'BEGridCycle'       : 'F1',
            'BEUndo'            : 'CTRL+Z',
            'BEAngleCycle'      : 'F2',
            'BERedo'            : 'CTRL+Y',
            'BEClipCycle'       : 'F3',
            'BESelect'          : '',
            'BEAttachCycle'     : 'F5',
            'BESelectNext'      : 'TAB',
            'BERotateCCW'       : '',
            'BESelectLast'      : 'SHIFT+TAB',
            'BERotateCW'        : '',
            'BECenterCur'       : '',
            'BESell'            : '',
            'BECenterSel'       : '',
            'BESeeEverything'   : '',
            'BESetBaseLighting' : ''
        }
        for k,v in self.KeyInit.items():
            self.Profile.CustomBinds.Init[self.BindPane.MakeCtrlName(k)] = v

        self.Dialog() # do this early to run Profile.CheckAllConflicts

    def BuildUI(self, dialog, init : dict|None = None) -> wx.Sizer:
        wizdata = {}
        if init: wizdata = init.get('WizData', {})

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        optsSizer = ControlGroup(dialog, self.Profile.CustomBinds, label = 'Options')

        self.BEDisableMovement = optsSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = self.BindPane.MakeCtrlName('BEDisableMovement'),
            tooltip = 'Disable SoD etc and set movement keys to their default behavior',
        )

        self.BEDisableChat = optsSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = self.BindPane.MakeCtrlName('BEDisableChat'),
            tooltip = 'Disable keys that will pop up the chat window',
        )

        ### KEY SIZER
        keysSizer = ControlGroup(dialog, self.Profile.CustomBinds, label = 'Keybinds', width = 4)

        for key in self.KeyInit:
            keybutton = keysSizer.AddControl(
                ctlType = 'keybutton',
                ctlName = self.BindPane.MakeCtrlName(key),
                tooltip = UI.Labels[self.BindPane.MakeCtrlName(key)],
            )
            keybutton.Bind(EVT_KEY_CHANGED, self.CheckForConflicts)
            setattr(self, key, keybutton)

        for ctrlname in wizdata:
            if hasattr(self, ctrlname): # just in case, 'cause kaboom
                getattr(self, ctrlname).SetValue(wizdata[ctrlname])

        mainSizer.Add(optsSizer, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(keysSizer, 0, wx.EXPAND|wx.ALL, 5)

        self.Profile.CheckAllConflicts()

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
        for cmd in ('BEDisableMovement', 'BEDisableChat', ):
            ctpanel = wx.Panel(cmdPanel)
            ctsizer = wx.BoxSizer(wx.HORIZONTAL)
            ctpanel.SetSizer(ctsizer)
            cmdtext = cgStaticText(ctpanel, label = UI.Labels[self.BindPane.MakeCtrlName(cmd)], style = wx.ALIGN_CENTER)
            cmdtext.SetBackgroundColour(wx.Colour(220, 220, 220))
            if self.State.get('WizData', {}).get(cmd, False):
                cmdtext.SetLabel("✓ " + UI.Labels[self.BindPane.MakeCtrlName(cmd)])
            else:
                cmdtext.SetForegroundColour(wx.Colour(160, 160, 160))
            ctsizer.Add(cmdtext, 1, wx.EXPAND|wx.ALL, 5)
            cmdSizer.Add(ctpanel, 1, wx.EXPAND)

            ctpanel.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
            cmdtext.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)

        if conflicts := self.CheckForConflicts():
            conflicts.remove('EnterEditMode')
            conflicts = [f"\n\t\u2022 {UI.Labels[self.BindPane.MakeCtrlName(c)]}" for c in conflicts]
            ctpanel = wx.Panel(cmdPanel)
            ctsizer = wx.BoxSizer(wx.HORIZONTAL)
            ctpanel.SetSizer(ctsizer)
            cmdtext = cgStaticText(ctpanel, label = f"Error: {len(conflicts)} key conflicts", style = wx.ALIGN_CENTER)
            cmdtext.SetBackgroundColour(wx.Colour(255, 200, 200))
            cmdtext.SetToolTip("The following keys have conflicts:" + "".join(conflicts))
            ctsizer.Add(cmdtext, 1, wx.EXPAND|wx.ALL, 5)
            cmdSizer.Add(ctpanel, 1, wx.EXPAND)

            ctpanel.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
            cmdtext.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)

        panelSizer.Add(cmdPanel, 1, wx.ALIGN_CENTER|wx.ALL, 15)
        cmdPanel.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)

        bkText = cgStaticText(panel, label = 'Bind Key:')
        panelSizer.Add(bkText, 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 5)
        bkText.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)

        self.EnterEditMode = bcKeyButton(panel, init = {
            'CtlName' : bindpane.MakeCtrlName('EnterEditMode'),
            'Page'    : bindpane.Page,
            'Key'     : self.State.get('WizData', {}).get('EnterEditMode', ''),
        })
        panelSizer.Add(self.EnterEditMode, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        bindpane.SetCtrl('EnterEditMode', self.EnterEditMode)
        self.EnterEditMode.Bind(EVT_KEY_CHANGED, self.OnBindKeyChanged)
        UI.Labels[self.EnterEditMode] = 'Enter Edit Mode'

        panel.SetSizer(panelSizer)

        self.CheckForConflicts()
        self.CheckIfWellFormed()

        return panel

    def CheckForConflicts(self, evt = None):
        if evt: evt.Skip()
        conflicts = []
        for key in self.KeyInit:
            if getattr(self, key).CheckConflicts():
                conflicts.append(key)
        if hasattr(self, 'EnterEditMode'):
            if self.EnterEditMode.CheckConflicts():  conflicts.append('EnterEditMode')
        return conflicts

    def OnBindKeyChanged(self, evt = None):
        if evt: evt.Skip()
        self.CheckIfWellFormed()
        self.UpdateState()

    def CheckIfWellFormed(self, evt = None):
        if evt: evt.Skip()
        if self.EnterEditMode.GetValue():
            self.EnterEditMode.RemoveError('undef')
            return True
        else:
            self.EnterEditMode.AddError('undef', 'The keybind has not been selected')
            return False

    def UpdateState(self):
        newstate = { 'EnterEditMode' : self.EnterEditMode.GetValue() }
        for ctrlname in self.AllCtrls:
            newstate[ctrlname] = getattr(self, ctrlname).GetValue()
        self.State = { 'WizData' : newstate }

    def PopulateBindFiles(self):
        if not self.CheckIfWellFormed():  return
        resetfile = self.Profile.ResetFile()
        modefile  = self.Profile.GetBindFile('wiz', f"{self.BindPane.CustomID}-md.txt")

        resetfile.SetBind(self.EnterEditMode.MakeBind(modefile.BLF()))
        modefile .SetBind(self.EnterEditMode.MakeBind(resetfile.BLF()))

    def AllBindFiles(self):
        return {
            'files' : [],
            'dirs'  : [],
        }
