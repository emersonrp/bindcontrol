import wx
import wx.lib.agw.ultimatelistctrl as ULC
import re
import json

from pathlib import Path
from pubsub import pub
from typing import Any

from Page import Page
from Help import HelpButton
from Icon import GetIcon, GetIconBitmap
from UI.ListPanel import ListPanel
from UI.PowerBinder import PowerBinder
from Util.SourceFileIcons import MACRO_ICON_NAMES, YCC_COLORS

class MacroComposer(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.TabTitle : str             = "Macro Composer"
        self.Panes    : list[MacroPane] = []
        self.Init     : dict[str, Any]  = {}

    def BuildPage(self) -> None:
        # sizer for the buttons
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item buttons
        newMacroButton = wx.Button(self, label = "Create New Macro")
        newMacroButton.Bind(wx.EVT_BUTTON, self.OnNewMacroButton)
        buttonSizer.Add(newMacroButton, wx.ALIGN_CENTER)
        buttonSizer.Add(HelpButton(self, 'MacroComposer.html'), 0, wx.ALIGN_CENTER, 5)
        importMacroButton = wx.Button(self, label = "Import Macro")
        importMacroButton.Bind(wx.EVT_BUTTON, self.OnImportMacroButton)
        buttonSizer.Add(importMacroButton, wx.ALIGN_CENTER)
        buttonSizer.Add(HelpButton(self, 'ImportMacro.html'), 0, wx.ALIGN_CENTER, 5)

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

        pub.subscribe(self.OnContentsChanged, 'macrocontentschanged')

    def AllBindFiles(self) -> dict[str, list]:
        return {
            'files' : [],
            'dirs'  : [],
        }

    def OnNewMacroButton(self, evt):
        self.AddMacroToPage(macropane = MacroPane(self))
        self.UpdateAllMacros()
        evt.Skip()

    def OnImportMacroButton(self, evt):
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Import Macro",
                           defaultDir = wx.ConfigBase.Get().Read('ProfilePath'),
                           wildcard="BindControl Custom Bind files (*.bcm)|*.bcm|All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            filepath = Path(fileDialog.GetPath())
            try:
                bindjson = filepath.read_text()
                macrodata = json.loads(bindjson)
                macrodata.pop('CustomID', None)

                if macropane := MacroPane(self, macrodata):
                    self.AddMacroToPage(macropane = macropane)
                    existingMacroNames = [pane.Title for pane in self.Panes if pane != macropane]
                    if macropane.Title in existingMacroNames:
                        macropane.SetPanelLabel(new = True)

            except Exception as e:
                wx.LogError(f'Cannot import macro "{filepath.name}": {e}')

        evt.Skip()

    def AddMacroToPage(self, macropane = None) -> None:
        if not macropane:
            wx.LogError("Something tried to add an empty macropane to the page.  This is a bug.")
            return

        if not macropane.Title: # this is from a "New Bind" button
            if not macropane.SetPanelLabel(new = True):
                return

        if len(self.Panes) == 0:
            # the BlankWindow is still in there
            self.BlankPanel.Hide()
            self.scrolledPanel.Show()
            self.MainSizer.Replace(self.BlankPanel, self.scrolledPanel)
            self.MainSizer.Layout()

        if not macropane.CustomID:
            macropane.CustomID = self.Profile.GetCustomID()
            macropane.Init['CustomID'] = macropane.CustomID

        macropane.UpdateLabel()
        macropane.SetFakeIconIfNeeded()

        self.Panes.append(macropane)

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount(), macropane, 0, wx.ALL|wx.EXPAND, 10)

        macropane.Pane.Expand()
        self.UpdateAllMacros()
        self.Layout()

    def OnDeleteButton(self, evt):
        delButton = evt.EventObject
        macropane = delButton.MacroPane
        with wx.MessageDialog(self,
                              message = f'Delete macro "{macropane.Title}"?  This cannot be undone.',
                              caption = f'Delete macro "{macropane.Title}"?',
                              style   = wx.OK|wx.CANCEL,
                              ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.doDeleteMacroPane(macropane)
            else:
                return

    def doDeleteMacroPane(self, macropane) -> None:
        if delButton := macropane.DelButton:
            sizer = delButton.MacroSizer
            self.PaneSizer.Hide(sizer)
            self.PaneSizer.Remove(sizer)
        if macropane in self.Panes:
            self.Panes.remove(macropane)
        # won't have an ID if it was a cancelled new bind
        if macropane.CustomID:
            self.Profile.UpdateData('MacroComposer', { 'CustomID' : macropane.CustomID, 'Action' : 'delete' })
        macropane.DestroyLater()
        if len(self.Panes) == 0:
            # need to put back the blankpanel
            self.scrolledPanel.Hide()
            self.BlankPanel.Show()
            self.MainSizer.Replace(self.scrolledPanel, self.BlankPanel)
        self.Layout()

    def OnDuplicateButton(self, evt):
        oldmacropane = evt.EventObject.MacroPane
        init = oldmacropane.Serialize()

        # clear out a few things that we don't want in the new bind
        init.pop('CustomID', None)
        init.pop('Title', None)

        newmacropane = MacroPane(self, init)

        if not newmacropane:
            wx.LogError(f'Error duplicating macro "{oldmacropane.Title}"!')
            return

        self.AddMacroToPage(newmacropane)

    def OnExportButton(self, evt):
        macropane = evt.GetEventObject().MacroPane

        shorttitle = re.sub(r'\W+', '', macropane.Title)

        with wx.FileDialog(self, f'Export Macro "{macropane.Title}"',
                           defaultFile = f"{shorttitle}.bcm",
                           defaultDir = wx.ConfigBase.Get().Read('ProfilePath'),
                           wildcard = "BindControl Macro Files (*.bcm)|*.bcm|All Files (*.*)|*.*",
                           style = wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            try:
                filepath = Path(pathname)
                macrodata = macropane.Serialize()
                macrodata.pop('CustomID', None)
                filepath.write_text(json.dumps(macrodata, indent=2))

            except Exception as e:
                wx.LogError(f"Error exporting Macro: {e}")

    def OnContentsChanged(self, evt = None) -> None:
        if evt: evt.Skip()
        self.UpdateAllMacros()

    def UpdateAllMacros(self) -> None:
        for pane in self.Panes:
            self.Profile.UpdateData('MacroComposer', pane.Serialize())

class MacroPane(ListPanel):
    def __init__(self, parent, init = None):
        super().__init__(parent, init)
        self.Description = "macro"

        pane = self.GetPane()
        macroSizer = wx.BoxSizer(wx.HORIZONTAL)

        macroSizer.Add(wx.StaticText(pane, label = "Icon:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.IconButton = wx.Button(pane, size = wx.Size(60,60), style = wx.BU_NOTEXT)
        if iconname := self.Init.get('Icon'):
            self.IconButton.SetLabel(iconname)
            self.IconButton.SetToolTip(iconname)
            self.IconButton.SetBitmap(GetIcon('Macros', iconname))
        else:
            self.SetFakeIcon()
        self.IconButton.Bind(wx.EVT_BUTTON, self.OnIconButton)
        self.IconButton.Bind(wx.EVT_RIGHT_DOWN, self.OnIconButtonRClick)
        macroSizer.Add(self.IconButton, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        fieldSizer = wx.GridBagSizer(5, 5)
        fieldSizer.Add(wx.StaticText(pane, label = "Contents:"), (0, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        self.MacroContents = PowerBinder(pane, self.Init.get('powerbinderdata'), contents = self.Init.get('Contents', ''))
        self.MacroContents.Bind(wx.EVT_TEXT, self.OnContentsChanged)
        fieldSizer.Add(self.MacroContents, (0, 1), (1, 2), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        self.ToolTipLabel = wx.StaticText(pane, label = "Tooltip:")
        fieldSizer.Add(self.ToolTipLabel, (1, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        self.ToolTipText = wx.TextCtrl(pane)
        self.ToolTipText.SetValue(self.Init.get('ToolTip', ''))
        self.ToolTipText.SetHint('Optional in-game tooltip for the macro button')
        self.ToolTipText.Bind(wx.EVT_TEXT, self.OnContentsChanged)
        fieldSizer.Add(self.ToolTipText, (1, 1), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        stringButton = wx.Button(pane, label = 'Get Macro String')
        stringButton.Bind(wx.EVT_BUTTON, self.OnStringButton)
        fieldSizer.Add(stringButton, (1, 2), flag = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)

        fieldSizer.AddGrowableCol(1)

        macroSizer.Add(fieldSizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        borderSizer = wx.BoxSizer(wx.VERTICAL)
        borderSizer.Add(macroSizer, 1, wx.ALL|wx.EXPAND, 15)

        pane.SetSizer(borderSizer)

        self.CheckToolTipSlot()

    def Serialize(self) -> dict:
        return {
            'CustomID'        : self.CustomID,
            'Title'           : self.Title,
            'Icon'            : self.IconButton.GetLabel() if self.IconButton else '',
            'Contents'        : self.MacroContents.GetValue() if self.MacroContents else '',
            'powerbinderdata' : self.MacroContents.SaveToData() if self.MacroContents else '',
            'ToolTip'         : self.ToolTipText.GetValue() if self.ToolTipText else '',
        }

    def OnIconButton(self, evt):
        button = evt.GetEventObject()
        with MacroIconPicker(self) as iconpicker: # RP: don't try to cache this, make a new one every time ugh
            if iconpicker.ShowModal() == wx.ID_OK:
                item = iconpicker.IconList.GetFirstSelected()
                iconname = iconpicker.IconList.GetItemText(item)
                button.SetToolTip(iconname)
                button.SetLabel(iconname)
                button.SetBitmap(GetIcon('Macros', iconname))
                self.OnContentsChanged()
                self.CheckToolTipSlot()

    def OnIconButtonRClick(self, evt):
        if evt: evt.Skip()
        self.SetFakeIcon()
        self.OnContentsChanged()
        self.CheckToolTipSlot()

    def OnContentsChanged(self, evt = None):
        if evt: evt.Skip()
        pub.sendMessage('macrocontentschanged')

    def SetPanelLabel(self, new = False) -> bool:
        if retval := super().SetPanelLabel(new):
            pub.sendMessage('updatemacros')
        return retval

    def CheckToolTipSlot(self):
        if self.ToolTipText and self.ToolTipLabel:
            enable = bool(self.IconButton) and (self.IconButton.GetLabel() != '')
            self.ToolTipText.Enable(enable)
            self.ToolTipLabel.Enable(enable)
            tooltiptext = '' if enable else 'Tooltip is only supported if an icon is chosen.'
            self.ToolTipText.SetToolTip(tooltiptext)
            self.ToolTipLabel.SetToolTip(tooltiptext)

    def OnStringButton(self, evt):
        with MacroTextDialog(self.Page, self) as dlg:
            dlg.ShowModal()

    def GetMacroString(self) -> str:
        if iconname := (self.IconButton.GetLabel() if self.IconButton else ''):
            macrostring = f'/macro_image "{iconname}" "{self.ToolTipText.GetValue()}" "{self.MacroContents.GetValue()}"'
        else:
            macrostring = f'/macro "{self.Title}" "{self.MacroContents.GetValue()}"'

        return macrostring

    def SetFakeIconIfNeeded(self):
        if self.IconButton and not self.IconButton.GetLabel():
            self.SetFakeIcon()

    def SetFakeIcon(self):
        self.IconButton.SetLabel('')
        self.IconButton.SetToolTip(self.Title)
        self.IconButton.SetBitmap(self.FakeMacroIcon(self.Title))

    def FakeMacroIcon(self, text) -> wx.BitmapBundle:
        bitmapdc = wx.MemoryDC()
        bitmapdc.SelectObject(GetIconBitmap('UI', 'MacroButton'))
        bitmapdc.SetTextForeground(wx.WHITE)
        bitmapdc.SetFont(wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT))
        extent = bitmapdc.GetTextExtent(text)
        bitmapdc.DrawText(text, max(0, int(16 - (extent.x / 2))), int(16 - (extent.y / 2)))
        return wx.BitmapBundle(bitmap = bitmapdc.GetAsBitmap())

class IconVirtualList(ULC.UltimateListCtrl):
    def __init__(self, parent):
        super().__init__(parent, agwStyle = ULC.ULC_REPORT|ULC.ULC_VIRTUAL|ULC.ULC_SINGLE_SEL|ULC.ULC_NO_HEADER|ULC.ULC_USER_ROW_HEIGHT)
        self.InsertColumn(0, '', width = 450)

        self.SetItemCount(len(MACRO_ICON_NAMES))
        self.SetUserLineHeight(40)

        self.Icons = wx.ImageList(32, 32, True)
        self.CurrentList = [] # the current list of names after filters have been applied
        self.NameToIconIdx = {}

        self.SetImageList(self.Icons, wx.IMAGE_LIST_SMALL)

    def OnGetItemText(self, item, col):
        return self.CurrentList[item]

    def OnGetItemImage(self, item):
        name = self.CurrentList[item]
        idx = self.NameToIconIdx.get(name, None) or self.Icons.Add(GetIconBitmap('Macros', name))
        self.NameToIconIdx[name] = idx
        return [idx]

    def OnGetItemToolTip   (self, item, col): return '' # pyright: ignore
    def OnGetItemTextColour(self, item, col): return None # pyright: ignore

    def FillList(self):
        searchString = self.Parent.SearchBox.GetValue() # pyright: ignore
        searchColor  = self.Parent.ColorChoice.GetStringSelection() # pyright: ignore

        self.DeleteAllItems()
        self.CurrentList = []

        for micon in MACRO_ICON_NAMES:
            if searchString and not re.search(re.escape(searchString), micon, re.IGNORECASE): continue

            if searchColor and not self.color_dist(YCC_COLORS[searchColor], MACRO_ICON_NAMES[micon]) < 0.12: continue

            self.CurrentList.append(micon)

        self.SetItemCount(len(self.CurrentList))

    # color functions / etc for icon color filter
    def color_dist(self, c1, c2):
        """ returns the squared euklidian distance between two color vectors in yuv space """
        return sum( (a-b)**2 for a,b in zip(c1, c2, strict = True) )

class MacroIconPicker(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title = "Macro Icon", size = wx.Size(500,600))

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

        self.IconList = IconVirtualList(self)
        IconSizer.Add(self.IconList, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        IconSizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizer(IconSizer)

    def ShowModal(self):
        self.SearchBox.SetValue('')
        self.ColorChoice.SetSelection(0)
        self.IconList.FillList()
        return super().ShowModal()

    def OnColorChoice(self, evt):
        self.IconList.FillList()
        evt.Skip()

    def OnSearchBox(self, evt):
        self.IconList.FillList()
        evt.Skip()

class MacroTextDialog(wx.Dialog):
    def __init__(self, parent, macropane):
        super().__init__(parent, title = f'Macro Text for macro "{macropane.Title}"')

        sizer = wx.BoxSizer(wx.VERTICAL)

        msg = (
               f'To install "{macropane.Title}" into the game, copy and paste\n'
               "the following text into the chat window in-game:"
              )
        sizer.Add( wx.StaticText(self, label = msg, style = wx.ALIGN_CENTER), 0, wx.EXPAND|wx.ALL, 10)

        ### helpful copyable /macro text
        macroSizer = wx.BoxSizer(wx.HORIZONTAL)
        textCtrl = wx.TextCtrl(self,
                       style = wx.TE_READONLY|wx.TE_CENTER,
                       value = macropane.GetMacroString(),
        )
        textCtrl.SetFont(
            wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName = 'Courier')
        )
        # https://wxpython.org/Phoenix/docs/html/wx.Control.html#wx.Control.GetSizeFromTextSize
        textCtrl.SetInitialSize(
            textCtrl.GetSizeFromTextSize(
                textCtrl.GetTextExtent(
                    textCtrl.GetValue()
                )
            )
        )
        macroSizer.Add(textCtrl, 1, wx.EXPAND)

        copyButton = wx.BitmapButton(self, bitmap = GetIcon('UI', 'copy'))
        copyButton.SetToolTip('Copy text')
        macroSizer.Add(copyButton, 0)
        copyButton.Bind(wx.EVT_BUTTON, self.doTextCopy)
        sizer.Add(macroSizer, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, 10)

        self.textctrl = textCtrl

        extraText = '\nThe macro will be placed in the first available power tray slot.'

        sizer.Add(wx.StaticText(self, label = extraText, style = wx.ALIGN_CENTER), 0, wx.EXPAND|wx.ALL, 10)

        sizer.Add(self.CreateButtonSizer(wx.OK), 0, wx.EXPAND|wx.ALL, 10)
        self.SetSizerAndFit(sizer)

    def doTextCopy(self, _):
        dataObj = wx.TextDataObject(self.textctrl.GetValue())
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(dataObj)
            wx.TheClipboard.Flush()
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Couldn't open the clipboard for copying")
