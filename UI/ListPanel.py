# parent class for bindpanes and macropanes
import json
from pathlib import Path
from pubsub import pub
import re
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
        super().__init__(parent.scrolledPanel)

        self.Ctrls                        = {}
        self.Init        : dict           = init
        self.Title       : str            = init.get('Title', '')
        self.Description : str            = ''
        self.Type        : str            = ''
        self.CustomID    : int|None       = init.get('CustomID')
        if not self.CustomID and self.Profile:
            self.CustomID = self.Profile.GetCustomID()


        self.Class = type(self).__name__

        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.Sizer)

        self.Pane = wx.CollapsiblePane(self, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.Pane.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        self.Pane.SetLabel(self.Title)
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
        renameButton.Bind(wx.EVT_BUTTON, self.SetPanelLabel)
        buttonSizer.Add(renameButton)

        duplicateButton = ListPanelControlButton(self, GetIcon('UI', 'copy'))
        duplicateButton.Pane = self.Pane
        self.DupButton = duplicateButton
        duplicateButton.SetToolTip(f'Duplicate "{self.Title}"')
        duplicateButton.Bind(wx.EVT_BUTTON, self.OnDuplicateButton)
        buttonSizer.Add(duplicateButton)

        exportButton = ListPanelControlButton(self, GetIcon('UI', 'export'))
        exportButton.Pane = self.Pane
        self.ExpButton = exportButton
        exportButton.SetToolTip(f'Export "{self.Title}"')
        exportButton.Bind(wx.EVT_BUTTON, self.OnExportButton)
        buttonSizer.Add(exportButton)

        self.Sizer.Add(buttonSizer, 0, wx.LEFT, 10)

        self.UpdateLabel()

        self.Pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

    def UpdateLabel(self):
        if wx.ConfigBase.Get().ReadBool('VerboseCustomBinds'):
            self.Pane.SetLabel(f"{self.Title} ({self.Description} ID:{self.CustomID})")
        else:
            self.Pane.SetLabel(f"{self.Title}")

    def GetPane(self):
        return self.Pane.GetPane()

    def SetPanelLabel(self, evt, new = False) -> bool:
        # marshal up the files to delete, before we change the name
        deletefiles = None if new else self.AllBindFiles()
        dlg = wx.TextEntryDialog(self, f'Enter name for {self.Description or "bind"}:')
        if self.Title:
            dlg.SetValue(self.Title)

        if dlg.ShowModal() == wx.ID_OK:
            self.Title = dlg.GetValue()
            self.Pane.SetLabel(self.Title)
            if not new:
                self.DelButton.SetToolTip(f'Delete "{self.Title}"')
                self.RenButton.SetToolTip(f'Rename "{self.Title}"')
                self.DupButton.SetToolTip(f'Duplicate "{self.Title}"')
                self.ExpButton.SetToolTip(f'Export "{self.Title}"')
                # if we have files to delete (we do, if not new) then delete them.
                # Also this is bind-specific
                if deletefiles and self.Profile:
                    self.Profile.doDeleteBindFiles(deletefiles)
            # TODO ok now we're doing something bind-specific in here again oops
            pub.sendMessage('updatebinds')
            dlg.Destroy()
            return True # successful name change
        else:
            if new:
                self.doDeletePanel()
            dlg.Destroy()
            return False

    def OnDuplicateButton(self, evt) -> None:
        init = self.Serialize()

        # clear out a few things that we don't want in the new bind
        init.pop('CustomID', None)
        init.pop('Title', None)
        init.pop('Key', None)

        # make a new one of whatever we are.  Is this the sane way to do this?
        newbindpane = self.__class__(init)

        if not newbindpane:
            wx.LogError(f"Error duplicating bind {self.Title}!")
            return

        if self.Page:
            self.Page.AddBindToPage(newbindpane) # pyright: ignore   # TODO pubsub this?

    def OnExportButton(self, evt) -> None:

        bindpane = evt.GetEventObject().BindPane

        shorttitle = re.sub(r'\W+', '', bindpane.Title)

        with wx.FileDialog(self, f'Export Complex Bind "{bindpane.Title}"',
                           defaultFile = f"{shorttitle}.bcb",
                           defaultDir = wx.ConfigBase.Get().Read('ProfilePath'),
                           wildcard = "BindControl Custom Bind Files (*.bcb)|*.bcb|All Files (*.*)|*.*",
                           style = wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            try:
                filepath = Path(pathname)
                binddata = bindpane.Serialize()
                binddata.pop('CustomID', None)
                filepath.write_text(json.dumps(binddata, indent=2))

            except Exception as e:
                wx.LogError(f"Error exporting Complex Bind: {e}")

    def OnDeleteButton(self, evt) -> None:
        with PanelDeletionDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            if dlg.DeleteFilesCB and dlg.DeleteFilesCB.GetValue():
                # do the delete of the files
                # TODO PUBSUB
                if self.Profile:
                    files = self.AllBindFiles()
                    self.Profile.doDeleteBindFiles(files)
        self.doDeletePanel()
        evt.Skip()

    # TODO - is all of this better done in the enclosing page?  Do I need a ListPanelList class
    # to encapsulate a bunch of this?  Probably ugh
    def doDeletePanel(self) -> None:
        # this is wanting to be done up outside, hide and remove the whole thing
        #delButton = self.DelButton
        #sizer = delButton.BindSizer
        #self.PaneSizer.Hide(sizer)
        #self.PaneSizer.Remove(sizer)
        if self.Page:
            for ctrlname in self.Ctrls:
                if self.Page.Ctrls.get(ctrlname) : del self.Page.Ctrls[ctrlname]

        # won't have an ID if it was a cancelled new bind
        # (NO LONGER TRUE AHA!!!)
        # TODO - figure out some new way to decide this was a cancelled new panel
        if self.CustomID and self.Profile:
            # pubsub this?  Generally want some sort of ('updatedata', data=binddata) scheme?
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

    def OnPaneChanged(self, evt) -> None:
        IsCollapsed = evt.GetCollapsed()
        if self.DelButton: self.DelButton.Show(not IsCollapsed)
        if self.RenButton: self.RenButton.Show(not IsCollapsed)
        if self.DupButton: self.DupButton.Show(not IsCollapsed)
        if self.ExpButton: self.ExpButton.Show(not IsCollapsed)
        if self.Page     : self.Page.Layout()

    # this is called when we duplicate a panel.  We'll want to clear any keybuttons
    # to keep the new duplicate panel from starting in a conflicting state
    def ClearKeyBinds(self) -> None:
        for _,ctrl in self.Ctrls.items():
            if isinstance(ctrl, bcKeyButton):
                ctrl.ClearButton(None)

    def Serialize(self) -> dict:
        wx.LogError(f"{self.Class} did not override Serialize.  This is a bug.")
        return {}

    def MakeCtrlName(self, name) -> str:
        return f"{self.Class}_{self.CustomID}_{name}"

    def GetCtrl(self, name):
        return self.Ctrls.get(self.MakeCtrlName(name))

    def SetCtrl(self, name, ctl):
        self.Ctrls[self.MakeCtrlName(name)] = ctl
        return ctl

    # uverride these next two on subclasses
    def CreatesFiles(self): return False
    def AllBindFiles(self):
        return {
            'files': [],
            'dirs':  [],
        }

class PanelDeletionDialog(wx.Dialog):
    def __init__(self, parent):
        bindpane = parent
        super().__init__(parent)
        self.SetTitle(f"Delete {bindpane.GetTitle()}")

        self.DeleteFilesCB = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(wx.StaticText(self, label = f'Delete Custom Bind "{bindpane.Title}"?'), 0, wx.ALL, 20)

        if bindpane.CreatesFiles():
            self.DeleteFilesCB = wx.CheckBox(self, label = "Delete all associated bindfiles")
            self.DeleteFilesCB.SetValue(True)
            mainSizer.Add(self.DeleteFilesCB, 0, wx.ALL|wx.ALIGN_CENTER, 10)

        mainSizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.ALL|wx.ALIGN_CENTER, 20)

        self.SetSizerAndFit(mainSizer)
