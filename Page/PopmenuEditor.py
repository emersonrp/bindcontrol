import pprint
import wx
from Page import Page

from pathlib import Path
import re

import wx.lib.agw.flatmenu as FM

class PopmenuEditor(Page):
    def __init__(self, parent):
        super().__init__(parent)

        self.CurrentMenu = None

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
        self.MenuListBox = wx.ListBox(MenuList, style = wx.LB_SINGLE)
        MenuListSizer.Add(self.MenuListBox, 1, wx.EXPAND|wx.ALL, 6)

        LoadMenuButton.Bind(wx.EVT_BUTTON, self.OnLoadButton)

        self.MenuEditor = wx.Panel(splitter)
        MESizer = wx.BoxSizer(wx.VERTICAL)
        self.MenuEditor.SetSizer(MESizer)

        MEButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        MEButtonSizer.Add(wx.Button(self.MenuEditor, label = "Insert Item"), 0, wx.EXPAND|wx.ALL, 6)
        MEButtonSizer.Add(wx.Button(self.MenuEditor, label = "Insert Separator"), 0, wx.EXPAND|wx.ALL, 6)
        MEButtonSizer.Add(wx.Button(self.MenuEditor, label = "Insert Submenu"), 0, wx.EXPAND|wx.ALL, 6)
        MESizer.Add(MEButtonSizer, 0, wx.ALIGN_CENTER|wx.BOTTOM, 15)

        MiddlePanel = wx.Panel(self.MenuEditor)
        MiddleSizer = wx.BoxSizer(wx.VERTICAL)
        MiddlePanel.SetSizer(MiddleSizer)
        MESizer.Add(MiddlePanel)
        TestMenuButton = wx.Button(MiddlePanel, label = "Test Current Popmenu")
        TestMenuButton.Bind(wx.EVT_BUTTON, self.OnTestMenuButton)
        MiddleSizer.Add(TestMenuButton, 0, wx.ALL, 10)

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

    def OnTestMenuButton(self, evt):
        if self.CurrentMenu:
            self.CurrentMenu.Popup(wx.GetMousePosition())
        evt.Skip()

    def OnLoadButton(self, _):
        with wx.FileDialog(self, "Load Popmenu file", wildcard="MNU files (*.mnu)|*.mnu",
                                            defaultDir = '/home/emerson/Downloads',   # TODO TODO TODO remove this line
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            newmenu = Popmenu(self)
            newmenu.ReadFromFile(fileDialog.GetPath())

            if newmenu and newmenu.MenuStructure:
                idx = self.MenuListBox.Append(newmenu.Title)
                self.MenuListBox.SetClientData(idx, newmenu)
                self.MenuListBox.SetSelection(idx)
                self.CurrentMenu = newmenu


class Popmenu(FM.FlatMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.MenuStructure = {}

    def WriteToFile(self, filename):
        ...

    def ReadFromFile(self, filename:str|Path):
        PopmenuFile = Path(filename)
        if not PopmenuFile.is_file():
            wx.LogError(f"Tried to edit a missing or non-file popmenu: {filename}")
            return {}

        contents = PopmenuFile.read_text()

        MenuStructure = self.ParseMenuStructure(contents.splitlines())

        pprint.pp(MenuStructure)

        # detangle the outermost husk that ParseMenuStructure wraps everything in...
        # This is -terrible- and super fragile.
        if MenuStructure:
            self.Title = list(MenuStructure[0]['Menu'].keys())[0]
            self.MenuStructure = MenuStructure

        else:
            wx.LogError("Something went wrong in ReadFromFile, no MenuStructure returned!")
            return


    def ParseMenuStructure(self, lines):

        ParsedMenu = []

        while lines:
            line = lines.pop(0).strip()

            line = re.sub(r'\s*//.*', '', line) # remove comments

            if line == '':
                continue
            elif line == "}":
                # return from recursive call, which was made down below when we found a "Menu"
                return ParsedMenu
            elif line == "Divider":
                ParsedMenu.append('Divider')
            elif line == "LockedOption":

                LockedData = []
                firstline = lines.pop(0).strip()
                if firstline != "{":
                    wx.LogError(f'Malformed LockedOption section:  expected "{{", got "{firstline}", canceling')
                    return {}
                nextline = lines.pop(0).strip()
                while nextline != "}":
                    LockedData.append(nextline)
                    nextline = lines.pop(0).strip()

                LockedOptions = []
                for lockedline in LockedData:
                    linematch = re.match(r'(\w+)\s+(.*)', lockedline)
                    if not linematch:
                        wx.LogError(f'Malformed line in LockedOption section: "{line}", canceling')
                        return {}

                    OptName, OptPayload = linematch.group(1,2)
                    OptName = OptName.strip('"')

                    if not OptName in ('DisplayName', 'Command', 'Authbit', 'Badge', 'RewardToken', 'StoreProduct', 'Icon', 'PowerReady'):
                        wx.LogError(f'Unknown keyword "{OptName}" in LockedOption section, canceling')
                        return {}

                    LockedOptions.append({OptName : OptPayload})

                ParsedMenu.append({'LockedOption' : LockedOptions})
            elif match := re.match(r'Title\s+(.*)', line):
                ParsedMenu.append({'Title', match[1].strip('"')})
            elif match := re.match(r'Menu\s+(.*)', line):
                MenuName = match.group(1)
                if lines.pop(0).strip() != '{':
                    wx.LogError("Menu statement not followed by a '{', canceling")
                    return False
                ParsedMenu.append({'Menu' : {MenuName.strip('"') : self.ParseMenuStructure(lines)}})
            elif match := re.match(r'Option\s+(.*)', line):
                OptionData = match.group(1)
                #
                # TODO - do popmenus ever use single quotes?
                if re.match(r'"', OptionData):
                    splitmatch = re.match(r'"([^"]+)"\s+(.*)', OptionData)
                else:
                    splitmatch = re.match(r'([^\s]+)\s+(.*)', OptionData)
                if splitmatch:
                    Optname, OptPayload = splitmatch.group(1,2)
                else:
                    wx.LogError(f'Invalid "Option" clause in popmenu: "{OptionData}", canceling')
                    return {}

                if re.match(r'"', OptPayload):
                    OptPayload = OptPayload.strip('"')
                elif plmatch := re.match(r'<&(.*)&>', OptPayload):
                    OptPayload = plmatch.group(1)

                ParsedMenu.append({'Option' : {Optname.strip('"') : OptPayload}})

        return ParsedMenu
