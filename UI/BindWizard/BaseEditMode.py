import wx
import UI
from UI.BindWizard import WizardParent
from UI.CGControls import bcKeyButton, cgStaticText
from UI.KeySelectDialog import EVT_KEY_CHANGED
from UI.CGControls import cgCheckBox, cgbcKeyButton

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

        optsSizer = wx.StaticBoxSizer(wx.VERTICAL, dialog, label = 'Options')

        self.BEDisableMovement = cgCheckBox(optsSizer.GetStaticBox(), label = 'Default Movement Keys')
        self.BEDisableMovement.SetToolTip('Disable SoD etc and set movement keys to their default behavior')
        self.BEDisableMovement.CtlName = self.BindPane.MakeCtrlName('BEDisableMovement')
        self.BEDisableMovement.SetValue(wizdata.get('BEDisableMovement', False))
        optsSizer.Add(self.BEDisableMovement, 0, wx.EXPAND|wx.ALL, 5)

        self.BEDisableChat = cgCheckBox(optsSizer.GetStaticBox(), label = 'Disable Chat Keys')
        self.BEDisableChat.SetToolTip('Disable keys that will pop up the chat window')
        self.BEDisableChat.CtlName = self.BindPane.MakeCtrlName('BEDisableChat')
        self.BEDisableChat.SetValue(wizdata.get('BEDisableChat', False))
        optsSizer.Add(self.BEDisableChat, 0, wx.EXPAND|wx.ALL, 5)

        ### KEY SIZER
        keysSizer = wx.StaticBoxSizer(wx.VERTICAL, dialog, label = 'Options')

        keysGrid = wx.FlexGridSizer(4, 5, 5)
        for key in self.KeyInit:
            kblabel = wx.StaticText(keysSizer.GetStaticBox(), label = f"{self.AllCtrls[key]}:")
            keybutton = cgbcKeyButton(keysSizer.GetStaticBox(), init = {
                'CtlName'  : self.BindPane.MakeCtrlName(key),
                'CtlLabel' : kblabel,
                'ToolTip'  : UI.Labels[self.BindPane.MakeCtrlName(key)],
                'Key'      : wizdata.get(key) if key in wizdata else self.KeyInit.get(key, ''),
            })
            self.BindPane.SetCtrl(key, keybutton)
            keybutton.Bind(EVT_KEY_CHANGED, self.CheckForConflicts)
            keysGrid.Add(kblabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            keysGrid.Add(keybutton, 0, wx.EXPAND)
        keysSizer.Add(keysGrid, 0, wx.ALL, 10)

        mainSizer.Add(optsSizer, 0, wx.EXPAND|wx.ALL, 10)
        mainSizer.Add(keysSizer, 0, wx.EXPAND|wx.ALL, 10)

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
            if 'EnterEditMode' in conflicts:
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
            if ctrl := self.BindPane.GetCtrl(key):
                if conflicts := ctrl.CheckConflicts():
                    conflicts.append(key)
        if eem := self.BindPane.GetCtrl('EnterEditMode'):
            if eem.CheckConflicts():  conflicts.append('EnterEditMode')
        return conflicts

    def OnBindKeyChanged(self, evt = None):
        if evt: evt.Skip()
        self.CheckIfWellFormed()
        self.UpdateState()

    def CheckIfWellFormed(self, evt = None):
        if evt: evt.Skip()
        if self.BindPane.GetCtrl('EnterEditMode').GetValue():
            self.EnterEditMode.RemoveError('undef')
            return True
        else:
            self.EnterEditMode.AddError('undef', 'The keybind has not been selected')
            return False

    def UpdateState(self):
        newstate = { 'EnterEditMode' : self.BindPane.GetCtrl('EnterEditMode').GetValue() }
        for ctrlname in self.AllCtrls:
            newstate[ctrlname] = self.BindPane.GetCtrl(ctrlname).GetValue()
        self.State = { 'WizData' : newstate }

    def PopulateBindFiles(self):
        if not self.CheckIfWellFormed():  return
        resetfile = self.Profile.ResetFile()
        modefile  = self.Profile.GetBindFile('wiz', f"{self.BindPane.CustomID}-md.txt")

        resetfile.SetBind(self.BindPane.GetCtrl('EnterEditMode').MakeBind('editbase 1', modefile .BLF()))
        modefile .SetBind(self.BindPane.GetCtrl('EnterEditMode').MakeBind('keybindreset', 'editbase 0', resetfile.BLF()))

        if self.BindPane.GetCtrl('BEDisableMovement').GetValue():
            # go through movement keys, add their default values to modefile
            ...

        if self.BindPane.GetCtrl('BEDisableChat').GetValue():
            # go through chat keys, add them as 'nop' to modefile
            ...

        ### turn each keybutton into a bind in modefile
        if self.BindPane.GetCtrl('BEGridCycle').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BEGridCycle').MakeBind('gridsnapcycle'))

        if self.BindPane.GetCtrl('BEUndo').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BEUndo').MakeBind('baseundo'))

        if self.BindPane.GetCtrl('BEAngleCycle').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BEAngleCycle').MakeBind('anglesnapcycle'))

        if self.BindPane.GetCtrl('BERedo').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BERedo').MakeBind('baseredo'))

        if self.BindPane.GetCtrl('BEClipCycle').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BEClipCycle').MakeBind('roomclipcycle'))

        if self.BindPane.GetCtrl('BESelect').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BESelect').MakeBind('baseselect'))

        if self.BindPane.GetCtrl('BEAttachCycle').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BEAttachCycle').MakeBind('attach_cycle'))

        if self.BindPane.GetCtrl('BESelectNext').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BESelectNext').MakeBind('selectnext'))

        if self.BindPane.GetCtrl('BERotateCCW').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BERotateCCW').MakeBind('rotate 0'))

        if self.BindPane.GetCtrl('BESelectLast').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BESelectLast').MakeBind('selectlast'))

        if self.BindPane.GetCtrl('BERotateCW').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BERotateCW').MakeBind('rotate 1'))

        if self.BindPane.GetCtrl('BECenterCur').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BECenterCur').MakeBind('center'))

        if self.BindPane.GetCtrl('BESell').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BESell').MakeBind('sell'))

        if self.BindPane.GetCtrl('BECenterSel').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BECenterSel').MakeBind('centersel'))

        if self.BindPane.GetCtrl('BESeeEverything').GetValue():
            modefile.SetBind(self.BindPane.GetCtrl('BESeeEverything').MakeBind('seeeverything'))

        if self.BindPane.GetCtrl('BESetBaseLighting').GetValue():
            lighting0 = self.Profile.GetBindFile('wiz', f"{self.BindPane.CustomID}-l0.txt")
            lighting1 = self.Profile.GetBindFile('wiz', f"{self.BindPane.CustomID}-l1.txt")
            lighting2 = self.Profile.GetBindFile('wiz', f"{self.BindPane.CustomID}-l2.txt")

            modefile .SetBind(self.BindPane.GetCtrl('BESetBaseLighting').MakeBind('baselightingtype 1', lighting1.BLF()))
            lighting0.SetBind(self.BindPane.GetCtrl('BESetBaseLighting').MakeBind('baselightingtype 1', lighting1.BLF()))
            lighting1.SetBind(self.BindPane.GetCtrl('BESetBaseLighting').MakeBind('baselightingtype 2', lighting2.BLF()))
            lighting2.SetBind(self.BindPane.GetCtrl('BESetBaseLighting').MakeBind('baselightingtype 0', lighting0.BLF()))


    def AllBindFiles(self):
        cid = self.BindPane.CustomID
        files = [
            self.Profile.GetBindFile('wiz', f"{cid}-md.txt"),
            self.Profile.GetBindFile('wiz', f"{cid}-l0.txt"),
            self.Profile.GetBindFile('wiz', f"{cid}-l1.txt"),
            self.Profile.GetBindFile('wiz', f"{cid}-l2.txt"),
        ]
        return {
            'files' : files,
            'dirs'  : [],
        }
