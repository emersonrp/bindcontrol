# parent class for various custom bindpane types
from typing import Any
import wx
from UI.KeySelectDialog import bcKeyButton

class CustomBindPaneParent(wx.CollapsiblePane):
    def __init__(self, page, init : dict|None = None) -> None:
        init = init or {}
        super().__init__(page.scrolledPanel, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        self.Ctrls                        = {}
        self.Page                         = page
        self.Profile                      = page.Profile
        self.Init        : dict           = init
        self.Title       : str            = init.get('Title', '')
        self.Description : str            = ''
        self.Type        : str            = ''
        self.CustomID    : int|None       = init.get('CustomID')
        self.DelButton   : wx.Button|None = None
        self.RenButton   : wx.Button|None = None
        self.DupButton   : wx.Button|None = None
        self.ExpButton   : wx.Button|None = None
        self.SetLabel(self.Title)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        # stash away the bind name inside the inner pane
        setattr(self.GetPane(), 'Title', self.Title)

        self.bindclass = type(self).__name__

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

    def BuildBindUI(self, page) -> None:
        wx.LogError(f"{self.bindclass} did not override BuildBindUI.  This is a bug.")
        # build the UI needed to edit/create this bind, and shim
        # it into 'page'

    def CheckIfWellFormed(self) -> bool:
        wx.LogWarning(f"{self.bindclass} did not override CheckIfWellFormed.  This is a bug.")
        return False

    def PopulateBindFiles(self) -> None:
        wx.LogError(f"{self.bindclass} did not override PopulateBindFiles.  This is a bug.")
        # for overriding on child classes this will be called in the course of
        # the Custom Binds page doing its own PopulateBindFiles, iteratively
        # over all of its kids

    def CreateSerialization(self, data) -> dict[str, Any]:
        return {
            'CustomID' : self.CustomID,
            'Type'     : self.Type,
            'Title'    : self.Title,
            **data
        }

    def Serialize(self) -> dict:
        wx.LogError(f"{self.bindclass} did not override Serialize.  This is a bug.")
        return {}

    def OnPaneChanged(self, evt) -> None:
        IsCollapsed = evt.GetCollapsed()
        if self.DelButton: self.DelButton.Show(not IsCollapsed)
        if self.RenButton: self.RenButton.Show(not IsCollapsed)
        if self.DupButton: self.DupButton.Show(not IsCollapsed)
        if self.ExpButton: self.ExpButton.Show(not IsCollapsed)
        self.Page.Layout()

    # this is called when we duplicate a bind.  We'll want to clear any keybuttons
    # to keep the new duplicate bind from conflicting
    def ClearKeyBinds(self) -> None:
        for _,ctrl in self.Ctrls.items():
            if isinstance(ctrl, bcKeyButton):
                ctrl.ClearButton(None)

    def MakeCtrlName(self, name) -> str:
        return f"{self.bindclass}_{self.CustomID}_{name}"

    def GetCtrl(self, name):
        return self.Ctrls[self.MakeCtrlName(name)]

    def SetCtrl(self, name, ctl):
        self.Ctrls[self.MakeCtrlName(name)] = ctl
        return ctl
