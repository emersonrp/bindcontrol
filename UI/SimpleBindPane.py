import wx
import UI
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.PowerBinder import PowerBinder

### CustomBind subclasses for the individual bind types

class SimpleBindPane(CustomBindPaneParent):
    def __init__(self, page, init = {}):
        super().__init__(page, init)

        self.Description = "Simple Bind"

        self.PowerBinder = None

    def Serialize(self):
        data = {
            'Type'     : 'SimpleBind',
            'Title'    : self.Title,
            'Contents' : self.PowerBinder.GetValue() if self.PowerBinder else '',
            'Key'      : self.Ctrls[self.MakeCtlName('BindKey')].Key,
        }
        if self.PowerBinder:
            if self.PowerBinder.PowerBinderDialog():
                data['PowerBinderDlg'] = self.PowerBinder.PowerBinderDialog().SaveToData()
            else:
                wx.LogWarning(f'Unable to save PowerBinder data for Simple Bind "{self.Title}"')
        return data

    def BuildBindUI(self, page):
        pane = self.GetPane()
        setattr(pane, 'Page', page)

        BindSizer = wx.BoxSizer(wx.HORIZONTAL)

        powerbinderdata = self.Init.get('PowerBinderDlg', {})

        BindSizer.Add(wx.StaticText(pane, -1, "Bind Contents:"), 0, wx.ALIGN_CENTER_VERTICAL)
        pb = PowerBinder(pane, powerbinderdata)
        pb.SetValue(self.Init.get('Contents', ''))
        pb.Bind(wx.EVT_TEXT, self.onContentsChanged)
        self.PowerBinder = pb
        self.Ctrls[self.MakeCtlName('PowerBinder')] = pb
        BindSizer.Add(pb, 1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)

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

        if self.PowerBinder:
            self.PowerBinder.SetToolTip('')
            if self.PowerBinder.GetValue():
                self.PowerBinder.RemoveError('undef')
            else:
                self.PowerBinder.AddError('undef', 'The bind contents have not been defined.')
                isWellFormed = False

            if len(self.PowerBinder.GetValue()) <= 255:
                self.PowerBinder.RemoveError('length')
            else:
                self.PowerBinder.AddError('length', 'This bind is longer than 255 characters, which will cause problems in-game.')
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
        pb = self.PowerBinder

        resetfile.SetBind(bk.Key, self.Title, self.Page, pb.GetValue())
