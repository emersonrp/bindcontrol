import wx
import UI
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.PowerBinderDialog import PowerBinderButton
from UI.ControlGroup import cgTextCtrl

### CustomBind subclasses for the individual bind types

class SimpleBindPane(CustomBindPaneParent):
    def __init__(self, page, init = {}):
        CustomBindPaneParent.__init__(self, page, init)

        self.Description = "Simple Bind"

        self.PowerBinderBtn = None

    def Serialize(self):
        data = {
            'Type'     : 'SimpleBind',
            'Title'    : self.Title,
            'Contents' : self.Ctrls[self.MakeCtlName('BindContents')].GetValue(),
            'Key'      : self.Ctrls[self.MakeCtlName('BindKey')].Key,
        }
        if self.PowerBinderBtn:
            if self.PowerBinderBtn.PowerBinderDialog():
                data['PowerBinderDlg'] = self.PowerBinderBtn.PowerBinderDialog().SaveToData()
            else:
                wx.LogWarning(f'Unable to save PowerBinder data for Simple Bind "{self.Title}"')
        return data

    def BuildBindUI(self, page):
        pane = self.GetPane()
        setattr(pane, 'Page', page)

        BindSizer = wx.BoxSizer(wx.HORIZONTAL)

        BindContentsCtrl = cgTextCtrl(pane, -1, self.Init.get('Contents', ''), style = wx.TE_READONLY)
        BindContentsCtrl.SetForegroundColour(wx.Colour(128,128,128))
        BindContentsCtrl.SetHint('Use the PowerBinder button to the right to define this keybind')
        self.Ctrls[self.MakeCtlName('BindContents')] = BindContentsCtrl

        powerbinderdata = self.Init.get('PowerBinderDlg', {})

        BindSizer.Add(wx.StaticText(pane, -1, "Bind Contents:"), 0, wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(BindContentsCtrl,                          1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        pbb = PowerBinderButton(pane, BindContentsCtrl, powerbinderdata)
        BindSizer.Add(pbb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.PowerBinderBtn = pbb

        BindKeyCtrl = bcKeyButton(pane, -1, {
            'CtlName' : self.MakeCtlName("BindKey"),
            'Page'    : page,
            'Key'     : self.Init.get('Key', ''),
        })
        BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.onKeyChanged)

        BindContentsCtrl.Bind(wx.EVT_TEXT, self.onContentsChanged)
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(BindKeyCtrl,                          0, wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[BindKeyCtrl.CtlName] = BindKeyCtrl
        UI.Labels[BindKeyCtrl.CtlName] = f'Simple Bind "{self.Title}"'

        # gotta wait to bind this until pbb is defined/etc
        BindContentsCtrl.Bind(wx.EVT_LEFT_DOWN, pbb.OnClickPBB)

        BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(BindSizer, 1, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)
        self.checkIfWellFormed()


    def onContentsChanged(self, _):
        self.Profile.SetModified()
        self.checkIfWellFormed()

    def onKeyChanged(self, _):
        self.Profile.SetModified()
        self.checkIfWellFormed()
        if self.Profile:
            self.Profile.CheckAllConflicts()

    def AllBindFiles(self): return {}

    def checkIfWellFormed(self):
        isWellFormed = True

        bc = self.Ctrls[self.MakeCtlName('BindContents')]
        bc.SetToolTip('')

        if self.PowerBinderBtn:
            if bc.GetValue():
                self.PowerBinderBtn.RemoveError('undef')
            else:
                self.PowerBinderBtn.AddError('undef', 'The bind contents have not been defined.')
                isWellFormed = False

        if len(bc.GetValue()) <= 255:
            bc.RemoveError('length')
        else:
            bc.AddError('length', 'This bind is longer than 255 characters, which will cause problems in-game.')
            isWellFormed = False

        bk = self.Ctrls[self.MakeCtlName('BindKey')]
        if bk.Key:
            bk.RemoveError('undef')
        else:
            bk.AddError('undef', 'The keybind has not been selected')
            isWellFormed = False

        return isWellFormed

    def PopulateBindFiles(self):
        if not self.checkIfWellFormed():
            wx.MessageBox(f"Custom Bind \"{self.Title}\" is not complete or has errors.  Not written to bindfile.")
            return
        resetfile = wx.App.Get().Main.Profile.ResetFile()
        bk = self.Ctrls[self.MakeCtlName('BindKey')]
        bc = self.Ctrls[self.MakeCtlName('BindContents')]

        resetfile.SetBind(bk.Key, self.Title, self.Page, bc.GetValue())
