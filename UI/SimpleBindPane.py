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
            'Contents' : self.Ctrls['BindContents'].GetValue(),
            'Key'      : self.Ctrls['BindKey'].Key,
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
        self.Ctrls['BindContents'] = BindContentsCtrl

        BindKeyCtrl = bcKeyButton(pane, -1, {
            'CtlName' : f"{self.bindclass}BindKey",
            'Page'    : page,
            'Key'     : self.Init.get('Key', ''),
        })
        BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.onKeyChanged)

        BindSizer.Add(wx.StaticText(pane, -1, "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(BindKeyCtrl,                          0, wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls['BindKey'] = BindKeyCtrl
        UI.Labels[BindKeyCtrl.CtlName] = "Simple Bind "

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

    def checkIfWellFormed(self):
        isWellFormed = True

        bc = self.Ctrls['BindContents']
        bc.SetToolTip('')
        if bc.GetValue() and len(bc.GetValue()) <= 255:
            bc.SetBackgroundColour(wx.NullColour)
        else:
            bc.SetBackgroundColour((255,200,200))
            if len(bc.GetValue()) > 255:
                bc.SetToolTip("This bind is longer than 255 characters, which will cause problems in-game.")
            isWellFormed = False

        bk = self.Ctrls['BindKey']
        if bk.Key:
            bk.SetError(False)
        else:
            bk.SetError(True)
            isWellFormed = False

        return isWellFormed

    def PopulateBindFiles(self):
        if not self.checkIfWellFormed():
            wx.LogError(f"Custom Bind \"{self.Title}\" is not complete or has errors.")
            raise Exception
        resetfile = wx.App.Get().Profile.ResetFile()
        bk = self.Ctrls['BindKey']
        bc = self.Ctrls['BindContents']

        resetfile.SetBind(bk.Key, self.Title, self.Page, bc.GetValue())
