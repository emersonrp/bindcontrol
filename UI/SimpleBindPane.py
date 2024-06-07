import re
import wx
import UI
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.PowerBinderDialog import PowerBinderButton

### CustomBind subclasses for the individual bind types

class SimpleBindPane(CustomBindPaneParent):
    def __init__(self, page, init = {}):
        CustomBindPaneParent.__init__(self, page, init)

        self.PowerBinderDlg = None

    def Serialize(self):
        data = {
            'Type'     : 'SimpleBind',
            'Title'    : self.Title,
            'Contents' : self.Ctrls[self.MakeCtlName('BindContents')].GetValue(),
            'Key'      : self.Ctrls[self.MakeCtlName('BindKey')].Key,
        }
        if self.PowerBinderDlg: data['PowerBinderDlg'] = self.PowerBinderDlg.SaveToData()
        return data

    def BuildBindUI(self, page):
        pane = self.GetPane()
        pane.Page = page

        BindSizer = wx.BoxSizer(wx.HORIZONTAL)

        BindContentsCtrl = wx.TextCtrl(pane, -1, self.Init.get('Contents', ''))
        BindContentsCtrl.Bind(wx.EVT_TEXT, self.onContentsChanged)

        powerbinderdata = self.Init.get('PowerBinderDlg', {})

        BindSizer.Add(wx.StaticText(pane, -1, "Bind Contents:"),              0, wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(BindContentsCtrl,                                       1, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        pbb = PowerBinderButton(pane, BindContentsCtrl, powerbinderdata)
        BindSizer.Add(pbb, 0, wx.ALIGN_CENTER_VERTICAL)
        self.PowerBinderDlg = pbb.PowerBinderDialog
        self.Ctrls[self.MakeCtlName('BindContents')] = BindContentsCtrl

        BindKeyCtrl = bcKeyButton(pane, -1, {
            'CtlName' : self.MakeCtlName("BindKey"),
            'Page'    : page,
            'Key'     : self.Init.get('Key', ''),
        })
        BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.onKeyChanged)

        BindSizer.Add(wx.StaticText(pane, -1, "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(BindKeyCtrl,                          0, wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[BindKeyCtrl.CtlName] = BindKeyCtrl
        UI.Labels[BindKeyCtrl.CtlName] = f'Simple Bind "{self.Title}"'

        BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(BindSizer, 1, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)
        self.checkIfWellFormed()

    def onContentsChanged(self, _):
        self.checkIfWellFormed()

    def onKeyChanged(self, _):
        self.checkIfWellFormed()
        if self.Profile:
            self.Profile.CheckAllConflicts()

    def checkIfWellFormed(self):
        isWellFormed = True

        bc = self.Ctrls[self.MakeCtlName('BindContents')]
        bc.SetToolTip('')
        if bc.GetValue() and len(bc.GetValue()) <= 255:
            bc.SetBackgroundColour(wx.NullColour)
        else:
            bc.SetBackgroundColour((255,200,200))
            if len(bc.GetValue()) > 255:
                bc.SetToolTip("This bind is longer than 255 characters, which will cause problems in-game.")
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
        resetfile = wx.App.Get().Profile.ResetFile()
        bk = self.Ctrls['BindKey']
        bc = self.Ctrls['BindContents']

        resetfile.SetBind(bk.Key, self.Title, self.Page, bc.GetValue())
