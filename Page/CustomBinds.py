import wx
from functools import partial
from typing import Any, TYPE_CHECKING
from pathlib import Path
from pubsub import pub
import json

from Icon import GetIcon
from Page import Page
from Help import HelpButton
if TYPE_CHECKING:
    from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.BufferBindPane  import BufferBindPane
from UI.SimpleBindPane  import SimpleBindPane
from UI.ComplexBindPane import ComplexBindPane
from UI.WizardBindPane  import WizardBindPane, WizPickerMenu
from UI.KeySelectDialog import bcKeyButton

class CustomBindControlButton(wx.BitmapButton):
    def __init__(self, parent, bitmap):
        super().__init__(parent, bitmap = bitmap)
        self.BindPane: wx.Window|None = None
        self.BindSizer: wx.Sizer|None = None

class CustomBinds(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.TabTitle : str                        = "Custom Binds"
        self.Panes    : list[CustomBindPaneParent] = []
        self.Init     : dict[str, Any]             = {}

        pub.subscribe(self.OnVerboseBindsChanged, 'prefschanged.verbosebinds')
        pub.subscribe(self.OnBindsChanged, 'updatebinds')
        pub.subscribe(self.OnDeletePanel, 'deletepanel.bind')
        pub.subscribe(self.OnAddPanel, 'addpanel.bind')

    def BuildPage(self) -> None:

        # sizer for the buttons
        buttonSizer         = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item buttons
        newCustomBindButton = wx.Button(self, label = "New Custom Bind")
        newCustomBindButton.Bind(wx.EVT_BUTTON, self.OnNewCustomBindButton)
        buttonSizer.Add(newCustomBindButton, wx.ALIGN_CENTER)
        buttonSizer.Add(HelpButton(self, 'CustomBinds.html'), 0, wx.ALIGN_CENTER|wx.RIGHT, 5)

        launchBindWizardButton = wx.Button(self, label = "Launch Custom Bind Wizard")
        launchBindWizardButton.Bind(wx.EVT_BUTTON, self.OnBindWizardButton)
        buttonSizer.Add(launchBindWizardButton, wx.ALIGN_CENTER)
        buttonSizer.Add(HelpButton(self, 'WizardBinds.html'), 0, wx.ALIGN_CENTER|wx.RIGHT, 5)

        importBindButton = wx.Button(self, label = "Import Custom Bind")
        importBindButton.Bind(wx.EVT_BUTTON, self.OnImportBindButton)
        buttonSizer.Add(importBindButton, wx.ALIGN_CENTER)
        buttonSizer.Add(HelpButton(self, 'ImportBind.html'), 0, wx.ALIGN_CENTER, 5)

        # a scrollable window and sizer for the collection of collapsible panes
        self.PaneSizer     = wx.BoxSizer(wx.VERTICAL)
        self.scrolledPanel = wx.ScrolledWindow(self, style = wx.VSCROLL)
        self.scrolledPanel.SetScrollRate(10,10) # necessary to enable scrolling at all.
        self.scrolledPanel.SetSizer(self.PaneSizer)

        # Panel to show if we have no bindpanes, describing what's going on here
        BlankSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BlankPanel = wx.Panel(self)
        helptext = wx.StaticText(self.BlankPanel, style = wx.ALIGN_CENTER,
                                 label = "Create a Custom Bind using the buttons above",
                                 size = wx.Size(-1, 50))
        helptext.SetFont(wx.Font(wx.FontInfo(16).Bold()))
        BlankSizer.Add(helptext, 1, wx.ALIGN_CENTER_VERTICAL)
        self.BlankPanel.SetSizer(BlankSizer)
        self.BlankPanel.Layout()

        # add the two parts of the layout, bottom one expandable
        self.MainSizer.Add(buttonSizer,     0, wx.EXPAND|wx.BOTTOM, 16)
        self.MainSizer.Add(self.BlankPanel, 1, wx.EXPAND)

        # disable scrolling on the main page's ScrolledWindow.
        # This is black magic, and may still act squirrely.
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)

        self.Layout()

    def OnBindsChanged(self):
        self.UpdateAllBinds()
        self.Refresh()

    def OnVerboseBindsChanged(self):
        for pane in self.Panes:
            pane.UpdateLabel()

    def OnNewCustomBindButton(self, evt) -> None:
        popupmenu = wx.Menu()
        for bindtype in ['Simple', 'Complex', 'Buffer']:
            item = wx.MenuItem(popupmenu, wx.ID_ANY, f"New {bindtype} Bind")
            item.SetBitmap(GetIcon('UI', f"{bindtype}Bind"))
            popupmenu.Append(item)
            popupmenu.Bind(wx.EVT_MENU, partial(self.OnCustomBindMenu, bindtype), item)
        evt.GetEventObject().PopupMenu(popupmenu)
        evt.Skip()

    def OnCustomBindMenu(self, bindtype, evt) -> None:
        bindclass = {
            'Simple' : SimpleBindPane,
            'Complex' : ComplexBindPane,
            'Buffer' : BufferBindPane,
        }[bindtype]
        self.AddBindToPage(bindpane = bindclass(self))
        evt.Skip()

    def OnBindWizardButton(self, evt = None) -> None:
        if evt:
            evt.GetEventObject().PopupMenu(WizPickerMenu(self))
            evt.Skip()

    # I don't totally like binding the menu back upstream to this,
    # but the other way seems just as weirdly intrusive.
    def OnBindWizardPicked(self, wizClass = None, evt = None):
        if wizClass:
            newWizBindPane = WizardBindPane(self, init = {'WizClass' : wizClass})
            self.AddBindToPage(bindpane = newWizBindPane)
            if newWizBindPane in self.Panes: # did we cancel the add?
                newWizBindPane.Wizard.ShowWizard()
        if evt: evt.Skip()

    def OnImportBindButton(self, evt) -> None:
            # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Import Custom Bind",
                           defaultDir = wx.ConfigBase.Get().Read('ProfilePath'),
                           wildcard="BindControl Custom Bind files (*.bcb)|*.bcb|All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            filepath = Path(fileDialog.GetPath())
            try:
                bindjson = filepath.read_text()
                binddata = json.loads(bindjson)
                binddata.pop('CustomID', None)

                if bindpane := self.BuildBindPaneFromData(binddata):
                    self.AddBindToPage(bindpane = bindpane)
                    existingBindsNames = [pane.Title for pane in self.Panes if pane != bindpane]
                    if bindpane.Title in existingBindsNames:
                        bindpane.SetPanelLabel(new = True)

            except Exception as e:
                wx.LogError(f'Cannot import custom bind "{filepath.name}": {e}')

        evt.Skip()

    def BuildBindPaneFromData(self, binddata):
        bindpane = None
        if binddata['Type'] == "SimpleBind":
            bindpane = SimpleBindPane(self, init = binddata)
        elif binddata['Type'] == "BufferBind":
            bindpane = BufferBindPane(self, init = binddata)
        elif binddata['Type'] == "ComplexBind":
            bindpane = ComplexBindPane(self, init = binddata)
        elif binddata['Type'] == "WizardBind":
            bindpane = WizardBindPane(self, init = binddata)
        else:
            wx.LogError("No valid custom bind found.")

        return bindpane

    def OnAddPanel(self, panel):
        self.AddBindToPage(panel) # to get the args named right, sigh.

    def AddBindToPage(self, bindpane = None) -> None:
        if not bindpane:
            wx.LogError("Something tried to add an empty bindpane to the page.  This is a bug.")
            return

        if not bindpane.Title: # this is from a "New Bind" button
            if not bindpane.SetPanelLabel(new = True):
                return

        if len(self.Panes) == 0:
            # the BlankWindow is still in there
            self.BlankPanel.Hide()
            self.scrolledPanel.Show()
            self.MainSizer.Replace(self.BlankPanel, self.scrolledPanel)
            self.MainSizer.Layout()

        if not bindpane.CustomID:
            # probably need to re-examine why we need this in two places in the bindpane
            bindpane.CustomID = self.Profile.GetCustomID()
            bindpane.Init['CustomID'] = bindpane.CustomID
        else:
            # Re-ID the bindpane if the ID is a dupe.  This should never
            # have happened but it did and we need to fix it in existing
            # profiles that have this situation
            for p in self.Panes:
                if p.CustomID == bindpane.CustomID:
                    bindpane.CustomID = self.Profile.GetCustomID()
                    bindpane.Init['CustomID'] = bindpane.CustomID
                    break

        bindpane.UpdateLabel()

        self.Panes.append(bindpane)

        bindpane.BuildBindUI()

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount(), bindpane, 0, wx.ALL|wx.EXPAND, 10)
        bindpane.Pane.Expand()
        self.Layout()

    def OnDeletePanel(self, panel):
        self.doDeleteBindPane(panel) # need do to this to get the args named right.  This is dumb.

    def doDeleteBindPane(self, bindpane) -> None:
        for ctrlname in bindpane.Ctrls:
            if self.Ctrls.get(ctrlname):
                del self.Ctrls[ctrlname]

        if bindpane in self.Panes:
            self.Panes.remove(bindpane)

        if bindpane.Title and self.Profile:
            # won't have a Title if it was a cancelled new bind, for which we want to
            # gloss over and not poke this out there.
            self.Profile.UpdateData('CustomBinds', { 'CustomID' : bindpane.CustomID, 'Action' : 'delete' })

        bindpane.DestroyLater()

        if len(self.Panes) == 0:
            # need to put back the blankpanel
            self.scrolledPanel.Hide()
            self.BlankPanel.Show()
            self.MainSizer.Replace(self.scrolledPanel, self.BlankPanel)

        self.Layout()

    def GetKeyBinds(self):
        binds = super().GetKeyBinds()
        for pane in self.Panes:
            for ctrlname, ctrl in pane.Ctrls.items():
                if isinstance(ctrl, bcKeyButton):
                    if not ctrl.IsEnabled(): continue
                    binds.append( [ctrlname, ctrl.Key] )
        return binds

    def UpdateAllBinds(self) -> None:
        for pane in self.Panes:
            self.Profile.UpdateData('CustomBinds', pane.Serialize())

    def PopulateBindFiles(self) -> bool:
        errors = ''
        for pane in self.Panes:
            if pane.CheckIfWellFormed():
                pane.PopulateBindFiles()
            else:
                errors = errors + f"\n - {pane.Title}"

        if errors:
            wx.MessageBox(f"The following custom binds contain errors, and will not be written to the bindfiles: {errors}", "Errors Found")
        return True

    # TODO:  this contains knowledge of the innards of ComplexBinds, BufferBinds, etc
    # and probably should query each of those entities for which directories to check
    def AllBindFiles(self) -> dict:
        files = []
        dirs  = []
        for d in ['cbinds', 'cb', 'buff', 'wiz']:
            fpbd = self.FullPaneBindsDir(d)
            if fpbd:
                files.extend(fpbd['files'])
                dirs .extend(fpbd['dirs'])

        return {
            'files' : files,
            'dirs'  : dirs,
        }

    def FullPaneBindsDir(self, bdir) -> dict[str, list]:
        files = []
        dirs  = [bdir]
        panebindsdir = Path(self.Profile.BindsDir(), bdir)
        if panebindsdir.is_dir():
            for item in panebindsdir.glob('**/*'):
                if item.is_file():
                    files.append(self.Profile.GetBindFile(bdir, item.name))
                elif item.is_dir():
                    dirs.append(item)

        return {
            'files' : files,
            'dirs'  : dirs,
        }

class BindDeletionDialog(wx.Dialog):
    def __init__(self, parent, bindpane):
        super().__init__(parent, title = "Delete Bind")

        self.DeleteFilesCB = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(wx.StaticText(self, label = f'Delete Custom Bind "{bindpane.Title}"?'), 0, wx.ALL, 20)

        if isinstance(bindpane, ComplexBindPane) or isinstance(bindpane, BufferBindPane) or isinstance(bindpane, WizardBindPane):
            self.DeleteFilesCB = wx.CheckBox(self, label = "Delete all associated bindfiles")
            self.DeleteFilesCB.SetValue(True)
            mainSizer.Add(self.DeleteFilesCB, 0, wx.ALL|wx.ALIGN_CENTER, 10)

        mainSizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.ALL|wx.ALIGN_CENTER, 20)

        self.SetSizerAndFit(mainSizer)

