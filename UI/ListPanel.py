# parent class for bindpanes and macropanes
import json
from pathlib import Path
from pubsub import pub
import re
import wx
from UI.KeySelectDialog import bcKeyButton
from UI.ProfileAwareControl import ProfileAwareControlMixin

from Icon import GetIcon

class UIButton(wx.BitmapButton):
    def __init__(self, parent, icon):
        super().__init__(parent)

        self.Icon = icon

        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnSysColourChanged)
        self.OnSysColourChanged()

    def OnSysColourChanged(self, evt = None):
        if evt: evt.Skip()
        self.SetBitmap(GetIcon('UI', self.Icon))


class ListPanel(ProfileAwareControlMixin, wx.Panel):
    def __init__(self, parent, init : dict|None = None) -> None:
        init = init or {}
        super().__init__(parent.scrolledPanel)

        self.Ctrls                  = {}
        self.Init        : dict     = init
        self.Title       : str      = init.get('Title', '')
        self.Description : str      = ''
        self.Type        : str      = ''
        self.Topic       : str      = 'panel'
        self.CustomID    : int|None = init.get('CustomID')
        self.ExportExt   : str      = 'txt'

        # TODO maybe - now we do this on every __init__, which increments
        # Profile's customID, *even if we cancel* and so the Profile gets
        # flagged as modified.  Not clear how much of a problem this is
        # versus the hassle of fixing it.  Having it do it this way fixes
        # a -bunch- of other race-condition weirdness that happens if we
        # don't have a CustomID at all times.
        if not self.CustomID and self.Profile:
            self.CustomID = self.Profile.GetCustomID()

        self.Class = type(self).__name__

        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.Sizer)

        self.Pane = wx.CollapsiblePane(self, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.Pane.SetLabel(self.Title)
        self.Sizer.Add(self.Pane, 1, wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        deleteButton = UIButton(self, icon = 'delete')
        self.DelButton = deleteButton
        deleteButton.SetToolTip(f'Delete "{self.Title}"')
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDeleteButton)
        buttonSizer.Add(deleteButton)

        renameButton = UIButton(self, icon = 'rename')
        self.RenButton = renameButton
        renameButton.SetToolTip(f'Rename "{self.Title}"')
        renameButton.Bind(wx.EVT_BUTTON, self.OnRenameButton)
        buttonSizer.Add(renameButton)

        duplicateButton = UIButton(self, icon = 'copy')
        self.DupButton = duplicateButton
        duplicateButton.SetToolTip(f'Duplicate "{self.Title}"')
        duplicateButton.Bind(wx.EVT_BUTTON, self.OnDuplicateButton)
        buttonSizer.Add(duplicateButton)

        exportButton = UIButton(self, icon = 'export')
        self.ExpButton = exportButton
        exportButton.SetToolTip(f'Export "{self.Title}"')
        exportButton.Bind(wx.EVT_BUTTON, self.OnExportButton)
        buttonSizer.Add(exportButton)

        self.Sizer.Add(buttonSizer, 0, wx.LEFT, 10)

        self.UpdateLabel()

        self.Pane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)
        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnSystemColoursChanged)

    def UpdateLabel(self):
        if wx.ConfigBase.Get().ReadBool('VerboseCustomBinds'):
            self.Pane.SetLabel(f"{self.Title} ({self.Description} ID:{self.CustomID})")
        else:
            self.Pane.SetLabel(f"{self.Title}")

    def GetPane(self):
        return self.Pane.GetPane()

    def SetPanelLabel(self, new = False) -> bool:
        dlg = wx.TextEntryDialog(self, f'Enter name for {self.Description}:')
        if self.Title:
            dlg.SetValue(self.Title)

        if dlg.ShowModal() == wx.ID_OK:
            self.Title = dlg.GetValue()
            self.UpdateLabel()
            if not new:
                self.DelButton.SetToolTip(   f'Delete {self.Description} "{self.Title}"')
                self.RenButton.SetToolTip(   f'Rename {self.Description} "{self.Title}"')
                self.DupButton.SetToolTip(f'Duplicate {self.Description} "{self.Title}"')
                self.ExpButton.SetToolTip(   f'Export {self.Description} "{self.Title}"')
            dlg.Destroy()
            pub.sendMessage(f'updatepanels.{self.Topic}')
            return True # successful name change
        else:
            if new:
                pub.sendMessage(f'deletepanel.{self.Topic}', panel = self)
                self.DestroyLater()
            dlg.Destroy()
            return False

    def OnRenameButton(self, evt) -> None:
        if evt: evt.Skip()
        self.SetPanelLabel()

    def OnDuplicateButton(self, evt) -> None:
        init = self.Serialize()

        # clear out a few things that we don't want in the new panel
        init.pop('CustomID', None)
        init.pop('Title'   , None)
        init.pop('Key'     , None)

        # make a new one of whatever we are.
        if not (newpanel := self.__class__(self.Page, init)):
            wx.LogError(f"Error duplicating {self.Title}!")
            return

        pub.sendMessage(f'addpanel.{self.Topic}', panel = newpanel)
        pub.sendMessage(f'updatepanels.{self.Topic}')

    # to make this work completely correctly, subclasses need to set
    # self.ExportExt (default 'txt') to something interesting
    #
    # TODO - someday maybe use that info to register file types, but then we
    # have to handle them in BindControl.py in case they're passed in as
    # command-line args, and funnel them to the right code to import/load them
    def OnExportButton(self, evt) -> None:

        shorttitle = re.sub(r'\W+', '', self.Title)

        with wx.FileDialog(self, f'Export {self.Description} "{self.Title}"',
                           defaultFile = f"{shorttitle}.{self.ExportExt}",
                           defaultDir = wx.ConfigBase.Get().Read('ProfilePath'),
                           wildcard = f"BindControl {self.Description} Files (*.{self.ExportExt})|*.{self.ExportExt}|All Files (*.*)|*.*",
                           style = wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            try:
                filepath = Path(pathname)
                paneldata = self.Serialize()
                paneldata.pop('CustomID', None)
                filepath.write_text(json.dumps(paneldata, indent=2))

            except Exception as e:
                wx.LogError(f"Error exporting {self.Description}: {e}")

    # Basic deletion.  Subclasses should override if anything interesting needs happen.
    def OnDeleteButton(self, evt) -> None:
        with PanelDeletionDialog(self) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
        pub.sendMessage(f'deletepanel.{self.Topic}', panel = self)
        self.DestroyLater()
        evt.Skip()

    def OnSystemColoursChanged(self, evt = None):
        if evt: evt.Skip()
        self.Pane.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

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

class PanelDeletionDialog(wx.Dialog):
    def __init__(self, parent):
        panel = parent
        super().__init__(parent)
        self.SetTitle(f"Delete {panel.Title}")

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(wx.StaticText(self, label = f'Delete {panel.Type} "{panel.Title}"?'), 0, wx.ALL, 20)

        mainSizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.ALL|wx.ALIGN_CENTER, 20)

        self.SetSizerAndFit(mainSizer)
