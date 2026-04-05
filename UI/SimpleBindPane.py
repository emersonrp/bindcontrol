from pubsub import pub
from typing import Any
import wx
import UI
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.PowerBinder import PowerBinder
from Icon import GetIcon

### CustomBind subclasses for the individual bind types

class SimpleBindPane(CustomBindPaneParent):
    def __init__(self, page, init : dict|None = None) -> None:
        init = init or {}
        super().__init__(page, init)

        self.Description = "Simple Bind"
        self.Type        = "SimpleBind"

        self.PressBinder   = None
        self.ReleaseBinder = None

    def Serialize(self) -> dict[str, Any]:
        bindkey = self.GetCtrl('BindKey')
        data = self.CreateSerialization({
            'Contents' : self.PressBinder.GetValue() if self.PressBinder else '',
            'Key'      : bindkey.Key if bindkey else '',
            'isPRBind' : self.IsPR(),
            'RContents': self.ReleaseBinder.GetValue() if self.ReleaseBinder else '',
        })
        if self.PressBinder:
            data['PowerBinderDlg'] = self.PressBinder.SaveToData()
        if self.ReleaseBinder:
            data['ReleaseBinderDlg'] = self.ReleaseBinder.SaveToData()
        else:
            wx.LogWarning(f'Unable to save PowerBinder data for Simple Bind "{self.Title}"')

        return data

    def BuildBindUI(self):
        pane = self.Pane.GetPane()

        self.BindSizer = wx.FlexGridSizer(5, 5, 0)
        self.BindSizer.AddGrowableCol(1)

        powerbinderdata   = self.Init.get('PowerBinderDlg', {})
        releasebinderdata = self.Init.get('ReleaseBinderDlg', {})

        self.PressText = wx.StaticText(pane, label = "Bind Contents:")
        self.BindSizer.Add(self.PressText, 0, wx.ALIGN_CENTER_VERTICAL)

        pb = PowerBinder(pane, powerbinderdata, contents = self.Init.get('Contents', ''))
        pb.Bind(wx.EVT_TEXT, self.onContentsChanged)
        self.PressBinder = pb
        self.SetCtrl('PowerBinder', pb)
        self.BindSizer.Add(pb, 1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.EXPAND, 5)

        self.PRButton = wx.BitmapToggleButton(pane, label = GetIcon('UI', 'add_circle'))
        self.BindSizer.Add(self.PRButton, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        self.PRButton.SetToolTip("Separate Press/Release Actions for This Bind")
        self.PRButton.SetValue(self.Init.get('isPRBind', False))
        self.PRButton.Bind(wx.EVT_TOGGLEBUTTON, self.onPRButtonClicked)

        BindKeyCtrl = bcKeyButton(pane, init = {
            'CtlName' : self.MakeCtrlName("BindKey"),
            'Page'    : self.Page,
            'Key'     : self.Init.get('Key', ''),
        })
        BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.onKeyChanged)

        self.BindSizer.Add(wx.StaticText(pane, label = "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        self.BindSizer.Add(BindKeyCtrl,                          0, wx.ALIGN_CENTER_VERTICAL)
        self.SetCtrl('BindKey', BindKeyCtrl)
        UI.Labels[BindKeyCtrl.CtlName] = f'Simple Bind "{self.Title}"'

        self.ReleaseText = wx.StaticText(pane, label = "Release Action:")
        self.BindSizer.Add(self.ReleaseText, 0, wx.ALIGN_CENTER_VERTICAL)

        rb = PowerBinder(pane, releasebinderdata, contents = self.Init.get('RContents', ''))
        rb.Bind(wx.EVT_TEXT, self.onContentsChanged)
        self.ReleaseBinder = rb
        self.SetCtrl('ReleaseBinder', rb)
        self.BindSizer.Add(rb, 1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.EXPAND, 5)

        self.BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.HORIZONTAL)
        border.Add(self.BindSizer, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 10)
        pane.SetSizer(border)
        self.onPRButtonClicked()
        self.CheckIfWellFormed()

    def onPRButtonClicked(self, evt = None) -> None:
        if evt: evt.Skip()
        checked = self.IsPR()
        if self.ReleaseText:
            self.BindSizer.Show(self.ReleaseText, checked)
        if self.ReleaseBinder:
            self.BindSizer.Show(self.ReleaseBinder, checked)
        self.PressText.SetLabel('Press Action:' if checked else 'Bind Contents:')
        self.CheckIfWellFormed()
        self.BindSizer.Layout()
        if self.Page:
            self.Page.Layout()

    def onContentsChanged(self, evt) -> None:
        evt.Skip()
        pub.sendMessage('updatebinds')
        self.CheckIfWellFormed()

    def onKeyChanged(self, evt) -> None:
        evt.Skip()
        self.CheckIfWellFormed()

    def IsPR(self):
        return self.PRButton.GetValue()

    def AllBindFiles(self) -> dict:
        cid = self.CustomID
        files = []
        if p := self.Profile:
            files = [p.GetBindFile('sb', f'{cid}-p.txt'), p.GetBindFile('sb', f'{cid}-r.txt')] if self.IsPR() else []
        return {
            'files' : files,
            'dirs'  : ['sb'],
        }

    def CheckIfWellFormed(self) -> bool:
        isWellFormed = True

        for binder in (self.PressBinder, self.ReleaseBinder):
            if binder and binder.IsShown():
                binder.SetToolTip('')
                if binder.GetValue():
                    binder.RemoveError('undef')
                else:
                    binder.AddError('undef', 'The bind contents have not been defined.')
                    isWellFormed = False

                if len(binder.GetValue()) <= 255:
                    binder.RemoveError('length')
                else:
                    binder.AddError('length', 'This bind is longer than 255 characters, which will cause problems in-game.')
                    isWellFormed = False

        if bk := self.GetCtrl('BindKey'):
            if bk.Key:
                bk.RemoveError('undef')
            else:
                bk.AddError('undef', 'The keybind has not been selected')
                isWellFormed = False

        return isWellFormed

    def PopulateBindFiles(self) -> None:
        cid = self.CustomID
        if ctrl := self.GetCtrl('BindKey'):
            key = ctrl.Key
            if p := self.Profile:
                resetfile = p.ResetFile()
                if self.IsPR():
                    # press/release bind, do it in resetfile plus two more, sigh.
                    pfile = p.GetBindFile('sb', f"{cid}-p.txt")
                    rfile = p.GetBindFile('sb', f"{cid}-r.txt")
                    if pb := self.PressBinder:
                        if rb := self.ReleaseBinder:
                            resetfile.SetBind(key, self.Title, self.Page, "+$$" + pb.GetValue() + '$$' + rfile.BLF())
                            pfile    .SetBind(key, self.Title, self.Page, "+$$" + pb.GetValue() + '$$' + rfile.BLF())
                            rfile    .SetBind(key, self.Title, self.Page, "+$$" + rb.GetValue() + '$$' + pfile.BLF())
                else:
                    if pb := self.PressBinder:
                        resetfile.SetBind(key, self.Title, self.Page, pb.GetValue())
