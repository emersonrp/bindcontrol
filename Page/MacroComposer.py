import wx
import re

from typing import Any

from Page import Page
from Help import HelpButton
from Icon import GetIcon, GetIconBitmap, MACRO_ICON_NAMES
from UI.PowerBinder import PowerBinder

class MacroComposer(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.TabTitle : str             = "Macro Composer"
        self.Panes    : list[MacroPane] = []
        self.Init     : dict[str, Any]  = {}

        self.IconPicker = MacroIconPicker(self)

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
        self.Page = page

        pane = self.GetPane()
        macroSizer = wx.BoxSizer(wx.HORIZONTAL)

        macroSizer.Add(wx.StaticText(pane, label = "Icon:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.IconButton = wx.BitmapButton(pane, size = wx.Size(60,60))
        self.IconButton.Bind(wx.EVT_BUTTON, self.OnIconButton)
        self.IconButton.Bind(wx.EVT_RIGHT_DOWN, self.OnIconButtonRClick)
        macroSizer.Add(self.IconButton, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        fieldSizer = wx.FlexGridSizer(2, 5, 5)
        fieldSizer.AddGrowableCol(1)
        fieldSizer.Add(wx.StaticText(pane, label = "Contents:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.MacroContents = PowerBinder(pane)
        fieldSizer.Add(self.MacroContents, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        fieldSizer.Add(wx.StaticText(pane, label = "Tooltip:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.ToolTipText = wx.TextCtrl(pane)
        self.ToolTipText.SetHint('Optional in-game tooltip for the macro button')
        fieldSizer.Add(self.ToolTipText, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        macroSizer.Add(fieldSizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        borderSizer = wx.BoxSizer(wx.VERTICAL)
        borderSizer.Add(macroSizer, 1, wx.ALL|wx.EXPAND, 15)

        pane.SetSizer(borderSizer)

    def UpdateLabel(self):
        self.SetLabel(f"{self.Title}")

    def OnIconButton(self, evt):
        iconpicker = self.Page.IconPicker
        if iconpicker.ShowModal() == wx.ID_OK:
            item = iconpicker.IconList.GetFirstSelected()
            iconname = iconpicker.IconList.GetItemText(item)
            self.IconButton.SetToolTip(iconname)
            self.IconButton.SetLabel(iconname)
            self.IconButton.SetBitmap(GetIconBitmap('macros', iconname))

    def OnIconButtonRClick(self, evt):
        self.IconButton.SetToolTip('')
        self.IconButton.SetLabel('')
        self.IconButton.SetBitmap(GetIconBitmap('Empty'))

class CustomBindControlButton(wx.BitmapButton):
    def __init__(self, parent, bitmap):
        super().__init__(parent, bitmap = bitmap)
        self.MacroPane: wx.Window|None = None
        self.CtrlSizer: wx.Sizer |None = None

class MacroIconPicker(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title = "Macro Icon", size = wx.Size(500,600))

        # TODO do we want to move all the color stuff away into Util somewhere?
        self.YCC_COLORS = {
            'Red' : (0.299, 127.831264, 128.5),
            'Orange' : (0.6212745098039216, 127.64933866666667, 128.27013207843137),
            'Yellow' : (0.8859999999999999, 127.49990000000001, 128.081312),
            'Green' : (0.44197647058823525, 127.7505024, 127.68475256470589),
            'Blue' : (0.114, 128.5, 127.918688),
            'Violet' : (0.2629137254901961, 128.41596285490198, 128.16770760784314),
        }

        # where we squirrel away the actual Icon objects, indexed the same as MACRO_ICON_NAMES
        self.Icons = wx.ImageList(32, 32, True)

        IconSizer = wx.BoxSizer(wx.VERTICAL)

        searchSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.SearchBox = wx.TextCtrl(self)
        self.SearchBox.SetHint('Search')
        self.SearchBox.Bind(wx.EVT_TEXT, self.OnSearchBox)
        searchSizer.Add(self.SearchBox, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        colorHelp = HelpButton(self, 'ColorFilter.html')
        searchSizer.Add(colorHelp, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.ColorChoice = wx.Choice(self, choices = ['', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet'])
        self.ColorChoice.Bind(wx.EVT_CHOICE, self.OnColorChoice)
        searchSizer.Add(self.ColorChoice, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        IconSizer.Add(searchSizer, 0, wx.EXPAND|wx.ALL, 10)

        self.IconList = wx.ListCtrl(self, style = wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_NO_HEADER)
        IconSizer.Add(self.IconList, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        IconSizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(IconSizer)

    def ShowModal(self):
        self.FillList()
        return super().ShowModal()

    def OnColorChoice(self, evt):
        self.FillList()

    def OnSearchBox(self, evt):
        self.FillList()

    def FillList(self):
        searchString = self.SearchBox.GetValue()
        searchColor  = self.ColorChoice.GetStringSelection()

        self.IconList.ClearAll()

        # Build the Icons cache list once.  Do it here later on because
        # Icon.py has been caching these in a background thread.
        if not self.Icons.GetImageCount() > 0:
            for m in MACRO_ICON_NAMES:
                self.Icons.Add(GetIconBitmap('macros', m))
            self.IconList.SetImageList(self.Icons, wx.IMAGE_LIST_SMALL)

        self.IconList.InsertColumn(0, '', width = 450)

        index = 0
        for iconidx, micon in enumerate(MACRO_ICON_NAMES):
            if searchString and not re.search(searchString, micon, re.IGNORECASE): continue

            if searchColor and not self.color_dist(self.YCC_COLORS[searchColor], MACRO_ICON_NAMES[micon]) < 0.12: continue

            self.IconList.InsertItem(index, micon, iconidx)
            index = index + 1

    # color functions / etc for icon color filter
    def color_dist(self, c1, c2):
        """ returns the squared euklidian distance between two color vectors in yuv space """
        return sum( (a-b)**2 for a,b in zip(c1, c2, strict = True) )

