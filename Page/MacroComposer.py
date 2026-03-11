import wx

from typing import Any

from Page import Page
from Help import HelpButton
from Icon import GetIcon

class MacroComposer(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.TabTitle : str             = "Macro Composer"
        self.Panes    : list[MacroPane] = []
        self.Init     : dict[str, Any]  = {}

    def BuildPage(self) -> None:
        # sizer for the buttons
        buttonSizer         = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item buttons
        newMacroButton = wx.Button(self, label = "Create New Macro")
        newMacroButton.Bind(wx.EVT_BUTTON, self.OnNewMacroButton)
        buttonSizer.Add(newMacroButton, wx.ALIGN_CENTER)
        buttonSizer.Add(HelpButton(self, 'MacroComposer.html'), 0, wx.ALIGN_CENTER|wx.RIGHT, 5)

        # a scrollable window and sizer for the collection of collapsible panes
        self.PaneSizer     = wx.BoxSizer(wx.VERTICAL)
        self.scrolledPanel = wx.ScrolledWindow(self, style = wx.VSCROLL)
        self.scrolledPanel.SetScrollRate(10,10) # necessary to enable scrolling at all.
        self.scrolledPanel.SetSizer(self.PaneSizer)

        # Panel to show if we have no macropanes, describing what's going on here
        BlankSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BlankPanel = wx.Panel(self)
        helptext = wx.StaticText(self.BlankPanel, style = wx.ALIGN_CENTER,
                                 label = "Create a Macro using the button above")
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

    def SynchronizeUI(self) -> None:
        ...

    def PopulateBindFiles(self) -> bool: return True

    def AllBindFiles(self) -> dict[str, list]: return {}

    def OnNewMacroButton(self, evt):
        self.AddMacroToPage(macropane = MacroPane(self))
        evt.Skip()

    def AddMacroToPage(self, macropane = None) -> None:
        if not macropane:
            wx.LogError("Something tried to add an empty macropane to the page.  This is a bug.")
            return

        if not macropane.Title: # this is from a "New Bind" button
            if not self.SetMacroPaneLabel(None, macropane, new = True):
                return

        if len(self.Panes) == 0:
            # the BlankWindow is still in there
            self.BlankPanel.Hide()
            self.scrolledPanel.Show()
            self.MainSizer.Replace(self.BlankPanel, self.scrolledPanel)
            self.MainSizer.Layout()

        macropane.UpdateLabel()

        self.Panes.append(macropane)

        macropane.BuildMacroUI(self)

        # put it in a box with control buttons
        ctrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrlSizer.Add(macropane, 1, wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        deleteButton = CustomBindControlButton(self.scrolledPanel, GetIcon('UI', 'delete'))
        deleteButton.MacroPane  = macropane
        deleteButton.CtrlSizer = ctrlSizer
        macropane.DelButton = deleteButton
        deleteButton.SetToolTip(f'Delete macro "{macropane.Title}"')
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDeleteButton)
        buttonSizer.Add(deleteButton)

        renameButton = CustomBindControlButton(self.scrolledPanel, GetIcon('UI', 'rename'))
        renameButton.MacroPane = macropane
        macropane.RenButton = renameButton
        renameButton.SetToolTip(f'Rename macro "{macropane.Title}"')
        renameButton.Bind(wx.EVT_BUTTON, self.SetMacroPaneLabel)
        buttonSizer.Add(renameButton)

        duplicateButton = CustomBindControlButton(self.scrolledPanel, GetIcon('UI', 'copy'))
        duplicateButton.MacroPane = macropane
        macropane.DupButton = duplicateButton
        duplicateButton.SetToolTip(f'Duplicate macro "{macropane.Title}"')
        duplicateButton.Bind(wx.EVT_BUTTON, self.OnDuplicateButton)
        buttonSizer.Add(duplicateButton)

        exportButton = CustomBindControlButton(self.scrolledPanel, GetIcon('UI', 'export'))
        exportButton.MacroPane = macropane
        macropane.ExpButton = exportButton
        exportButton.SetToolTip(f'Export macro "{macropane.Title}"')
        exportButton.Bind(wx.EVT_BUTTON, self.OnExportButton)
        buttonSizer.Add(exportButton)

        ctrlSizer.Add(buttonSizer, 0, wx.LEFT, 10)

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount(), ctrlSizer, 0, wx.ALL|wx.EXPAND, 10)
        macropane.Expand()
        self.Layout()

    def OnDeleteButton(self, evt):
        ...

    def OnDuplicateButton(self, evt):
        ...

    def OnExportButton(self, evt):
        ...

    def doDeleteMacroPane(self, macropane):
        ...

    def SetMacroPaneLabel(self, evt, macropane = None, new = False) -> bool:
        if not macropane:
            macropane = evt.GetEventObject().MacroPane
        if not macropane:
            wx.LogError("Tried to set a MacroPane label without a macropane.  This is a bug.")
            return False

        # marshal up the files to delete, before we change the name
        if macroDesc := macropane.Description:
            macroDesc = f' "{macroDesc}"'
        dlg = wx.TextEntryDialog(self, f'Enter name for{macroDesc} macro:')
        if macropane.Title:
            dlg.SetValue(macropane.Title)

        if dlg.ShowModal() == wx.ID_OK:
            macropane.Title = dlg.GetValue()
            macropane.SetLabel(macropane.Title)
            if not new:
                macropane.DelButton.SetToolTip(f'Delete macro "{macropane.Title}"')
                macropane.RenButton.SetToolTip(f'Rename macro "{macropane.Title}"')
                macropane.DupButton.SetToolTip(f'Duplicate macro "{macropane.Title}"')
                macropane.ExpButton.SetToolTip(f'Export macro "{macropane.Title}"')
            self.Refresh()
            dlg.Destroy()
            return True # successful name change
        else: # they hit 'cancel'
            if new:
                self.doDeleteMacroPane(macropane)
            dlg.Destroy()
            return False

class MacroPane(wx.CollapsiblePane):
    def __init__(self, page, init : dict|None = None) -> None:
        super().__init__(page.scrolledPanel, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        self.Title       : str = ''
        self.Description : str = ''

    def BuildMacroUI(self, page):
        pane = self.GetPane()
        macroSizer = wx.BoxSizer(wx.HORIZONTAL)

        macroSizer.Add(wx.StaticText(pane, label = "Icon:"), 0, flag = wx.ALIGN_CENTER_VERTICAL)
        self.IconButton = wx.Button(pane)
        macroSizer.Add(self.IconButton, 0, flag = wx.ALIGN_CENTER_VERTICAL)

        fieldSizer = wx.FlexGridSizer(2, 5, 5)
        fieldSizer.AddGrowableCol(1)
        fieldSizer.Add(wx.StaticText(pane, label = "Contents:"), 0, flag = wx.ALIGN_CENTER_VERTICAL)
        fieldSizer.Add(wx.TextCtrl(pane, value = "Test Contents"), 1, flag = wx.ALIGN_CENTER_VERTICAL)

        fieldSizer.Add(wx.StaticText(pane, label = "Tooltip:"), 0, flag = wx.ALIGN_CENTER_VERTICAL)
        fieldSizer.Add(wx.TextCtrl(pane, value = "Test Tooltip"), 1, flag = wx.ALIGN_CENTER_VERTICAL)

        macroSizer.Add(fieldSizer, 0, flag = wx.ALIGN_CENTER_VERTICAL)

        pane.SetSizer(macroSizer)

    def UpdateLabel(self):
        self.SetLabel(f"{self.Title}")

class CustomBindControlButton(wx.BitmapButton):
    def __init__(self, parent, bitmap):
        super().__init__(parent, bitmap = bitmap)
        self.MacroPane: wx.Window|None = None
        self.CtrlSizer: wx.Sizer |None = None

class MacroIconMenu(wx.Menu):
    def __init__(self):
        super().__init__()

