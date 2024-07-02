import wx
from Page import Page

from pathlib import Path
import re

import wx.lib.agw.flatmenu as FM
from wx.lib.gizmos import TreeListCtrl

class PopmenuEditor(Page):
    def __init__(self, parent):
        super().__init__(parent)

        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(Sizer)

        LeftPanelWidth = 150 # TODO do this less stupid

        splitter = wx.SplitterWindow(self, style = wx.VERTICAL)
        splitter.SetMinimumPaneSize(LeftPanelWidth)

        MenuList = wx.Panel(splitter)
        MenuListSizer = wx.BoxSizer(wx.VERTICAL)
        MenuList.SetSizer(MenuListSizer)
        NewMenuButton = wx.Button(MenuList, label = "New Menu")
        LoadMenuButton = wx.Button(MenuList, label = "Load Menu")
        DelMenuButton = wx.Button(MenuList, label = "Delete Menu")
        RenMenuButton = wx.Button(MenuList, label = "Rename Menu")
        MenuListSizer.Add(NewMenuButton, 0, wx.EXPAND|wx.ALL, 6)
        MenuListSizer.Add(LoadMenuButton, 0, wx.EXPAND|wx.ALL, 6)
        MenuListSizer.Add(DelMenuButton, 0, wx.EXPAND|wx.ALL, 6)
        MenuListSizer.Add(RenMenuButton, 0, wx.EXPAND|wx.ALL, 6)
        MenuListBox = wx.ListBox(MenuList, style = wx.LB_SINGLE)
        MenuListBox.Insert(['Test Item', 'Popmenu', 'Connor is good'], 0)
        MenuListSizer.Add(MenuListBox, 1, wx.EXPAND|wx.ALL, 6)

        self.MenuEditor = wx.Panel(splitter)
        MESizer = wx.BoxSizer(wx.VERTICAL)
        self.MenuEditor.SetSizer(MESizer)
        self.MenuEditor.Bind(wx.EVT_LEFT_DOWN, self.OnPanelClick)
        self.MenuEditor.Bind(wx.EVT_RIGHT_DOWN, self.OnPanelClick)

        MEButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        MEButtonSizer.Add(wx.Button(self.MenuEditor, label = "Insert Item"), 0, wx.EXPAND|wx.ALL, 6)
        MEButtonSizer.Add(wx.Button(self.MenuEditor, label = "Insert Separator"), 0, wx.EXPAND|wx.ALL, 6)
        MEButtonSizer.Add(wx.Button(self.MenuEditor, label = "Insert Submenu"), 0, wx.EXPAND|wx.ALL, 6)
        MESizer.Add(MEButtonSizer, 0, wx.ALIGN_CENTER|wx.BOTTOM, 15)

        self.MenuTree = Popmenu(self.MenuEditor)
        MESizer.Add(wx.Panel(self.MenuEditor))

        splitter.SplitVertically(MenuList, self.MenuEditor, LeftPanelWidth)

        ButtonPanel = wx.Panel(self)
        ButtonSizer = wx.StaticBoxSizer(wx.VERTICAL, ButtonPanel)
        ButtonPanel.SetSizer(ButtonSizer)
        ButtonParent = ButtonSizer.GetStaticBox()
        ButtonSizer.Add(wx.Button(ButtonParent, label = "Write Popmenu"), 0, wx.EXPAND|wx.ALL, 6)
        ButtonSizer.Add(wx.Button(ButtonParent, label = "Generate Macro"), 0, wx.EXPAND|wx.ALL, 6)

        Sizer.Add(splitter, 1, wx.EXPAND)
        Sizer.Add(ButtonPanel, 0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 6)

        self.Layout()

    def OnPanelClick(self, evt):
        self.MenuTree.Popup(wx.GetMousePosition())
        evt.Skip()

class Popmenu(FM.FlatMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.Append(wx.ID_ANY, "Test 1")
        self.Append(wx.ID_ANY, "Menu Item 2")
        self.AppendSeparator()
        self.Append(wx.ID_ANY, "Connor is cute")

    def WriteToFile(self, filename):
        ...

    def ReadFromFile(self, filename:str|Path):
        PopmenuFile = Path(filename)
        if not PopmenuFile.is_file():
            wx.LogError(f"Tried to edit a missing or non-file popmenu: {filename}")
            return {}

        contents = PopmenuFile.read_text()

        ParsedMenu = self.ParseMenuStructure(contents)


    def ParseMenuStructure(self, data):

        ParsedMenu = []

        lines = data.splitlines()

        while lines:
            line = lines.pop().strip()
            if line == '':
                continue
            elif line == "Divider":
                ParsedMenu.append('Divider')
            elif line == "LockedOption":
                # TODO scoop out everything between { and } lines into LockedData
                LockedData = self.GetBracketedChunk(lines)
                ParsedMenu.append(self.ParseLockedOption(LockedData))
            elif re.match(r'^Menu\s+(.*)', line):
                # TODO scoop out everything between { and } lines into LockedData
                SubMenuData = self.GetBracketedChunk(lines)
                ParsedMenu.append(self.ParseMenuStructure(SubMenuData))
            elif re.match(r'^Option\s+(.*)', line):
                ...
            elif re.match(r'^Title\s+(.*)', line):
                ...

        return ParsedMenu

    def ParseLockedOption(self, data):
        ...

    def GetBracketedChunk(self, data):
        ...
