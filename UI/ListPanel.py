# parent class for bindpanes and macropanes
from pubsub import pub
from typing import Any
import wx
from UI.KeySelectDialog import bcKeyButton
from UI.ProfileAwareControl import ProfileAwareControlMixin

from Icon import GetIcon

class ListPanelControlButton(wx.BitmapButton):
    def __init__(self, parent, bitmap):
        super().__init__(parent, bitmap = bitmap)
        self.Pane: wx.Window|None = None

class ListPanel(ProfileAwareControlMixin, wx.Panel):
    def __init__(self, parent, init : dict|None = None) -> None:
        init = init or {}
        super().__init__(parent)

        self.Ctrls                        = {}
        self.Init        : dict           = init
        self.Title       : str            = init.get('Title', '')
        self.Description : str            = ''
        self.Type        : str            = ''
        self.CustomID    : int|None       = init.get('CustomID') or self.Profile.GetCustomID()
        self.DelButton   : wx.Button|None = None
        self.RenButton   : wx.Button|None = None
        self.DupButton   : wx.Button|None = None
        self.ExpButton   : wx.Button|None = None
        self.SetLabel(self.Title)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        self.Class = type(self).__name__

        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.setSizer(self.Sizer)

        self.Pane = wx.CollapsiblePane(self.Page.scrolledPanel, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.Sizer.Add(self.Pane, 1, wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        deleteButton = ListPanelControlButton(self, GetIcon('UI', 'delete'))
        deleteButton.Pane  = self.Pane
        self.DelButton = deleteButton
        deleteButton.SetToolTip(f'Delete "{self.Title}"')
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDeleteButton)
        buttonSizer.Add(deleteButton)

        renameButton = ListPanelControlButton(self, GetIcon('UI', 'rename'))
        renameButton.Pane = self.Pane
        self.RenButton = renameButton
        renameButton.SetToolTip(f'Rename "{self.Title}"')
        renameButton.Bind(wx.EVT_BUTTON, self.SetBindPaneLabel)
        buttonSizer.Add(renameButton)

        duplicateButton = ListPanelControlButton(self, GetIcon('UI', 'copy'))
        duplicateButton.Pane = self.Pane
        self.DupButton = duplicateButton
        duplicateButton.SetToolTip(f'Duplicate "{self.Title}"')
        duplicateButton.Bind(wx.EVT_BUTTON, self.OnDuplicateButton)
        buttonSizer.Add(duplicateButton)

        exportButton = ListPanelControlButton(self.scrolledPanel, GetIcon('UI', 'export'))
        exportButton.Pane = self.Pane
        self.ExpButton = exportButton
        exportButton.SetToolTip(f'Export "{self.Title}"')
        exportButton.Bind(wx.EVT_BUTTON, self.OnExportButton)
        buttonSizer.Add(exportButton)

        self.Sizer.Add(buttonSizer, 0, wx.LEFT, 10)

        self.UpdateLabel()

        self.Pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

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

    def UpdateLabel(self):
        if wx.ConfigBase.Get().ReadBool('VerboseCustomBinds'):
            self.SetLabel(f"{self.Title} ({self.Description} ID:{self.CustomID})")
        else:
            self.SetLabel(f"{self.Title}")

    def SetPanelLabel(self, evt, new = False) -> bool:
        # marshal up the files to delete, before we change the name
        deletefiles = None if new else self.AllBindFiles()
        dlg = wx.TextEntryDialog(self, f'Enter name for {self.Description or "bind"}:')
        if self.Title:
            dlg.SetValue(self.Title)

        if dlg.ShowModal() == wx.ID_OK:
            self.Title = dlg.GetValue()
            self.SetLabel(self.Title)
            if not new:
                self.DelButton.SetToolTip(f'Delete "{self.Title}"')
                self.RenButton.SetToolTip(f'Rename "{self.Title}"')
                self.DupButton.SetToolTip(f'Duplicate "{self.Title}"')
                self.ExpButton.SetToolTip(f'Export "{self.Title}"')
                # if we have files to delete (we do, if not new) then delete them.
                if deletefiles:
                    self.Profile.doDeleteBindFiles(deletefiles)
            self.UpdateAllBinds()
            self.Refresh()
            dlg.Destroy()
            return True # successful name change
        else:
            if new:
                self.doDeletePanel(self)
            dlg.Destroy()
            return False

    def doDeletePanel(self) -> None:
        if delButton := self.DelButton:
            sizer = delButton.BindSizer
            self.PaneSizer.Hide(sizer)
            self.PaneSizer.Remove(sizer)
        for ctrlname in self.Ctrls:
            if self.Ctrls.get(ctrlname) : del self.Ctrls[ctrlname]

        # won't have an ID if it was a cancelled new bind
        # (NO LONGER TRUE AHA!!!)
        # TODO - figure out some new way to decide this was a cancelled new panel
        if self.CustomID:
            self.Profile.UpdateData('CustomBinds', { 'CustomID' : self.CustomID, 'Action' : 'delete' })

        pub.sendMessage('deletepanel', panel = self)
        # TODO - catch 'deletepanel' message in enclosing page and do this next bit:
#        if self in self.Panes:
#            self.Panes.remove(self)
#        if len(self.Panes) == 0:
#            # need to put back the blankpanel
#            self.scrolledPanel.Hide()
#            self.BlankPanel.Show()
#            self.MainSizer.Replace(self.scrolledPanel, self.BlankPanel)
#        self.Layout()

        self.DestroyLater()

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

    # this is called when we duplicate a panel.  We'll want to clear any keybuttons
    # to keep the new duplicate panel from starting in a conflicting state
    def ClearKeyBinds(self) -> None:
        for _,ctrl in self.Ctrls.items():
            if isinstance(ctrl, bcKeyButton):
                ctrl.ClearButton(None)

    def MakeCtrlName(self, name) -> str:
        return f"{self.bindclass}_{self.CustomID}_{name}"

    def GetCtrl(self, name):
        return self.Ctrls.get(self.MakeCtrlName(name))

    def SetCtrl(self, name, ctl):
        self.Ctrls[self.MakeCtrlName(name)] = ctl
        return ctl
