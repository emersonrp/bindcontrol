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
        self.MenuListBox.Bind(wx.EVT_LISTBOX, self.OnListSelect)

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

            if newmenu:
                idx = self.MenuListBox.Append(newmenu.Title)
                self.MenuListBox.SetClientData(idx, newmenu)
                self.MenuListBox.SetSelection(idx)
                self.CurrentMenu = newmenu

    def OnListSelect(self, evt):
        idx = evt.GetSelection()
        menu = self.MenuListBox.GetClientData(idx)
        self.CurrentMenu = menu

class Popmenu(FM.FlatMenu):
    def __init__(self, parent):
        super().__init__(parent)

        self.ContextMenu = Popmenu_ContextMenu(self)
        self.Title = ''

    # hook the right click behavior to tell ContextMenu who got right-clicked
    def ProcessMouseRClick(self, pos):
        (result, menuid) = self.HitTest(pos)
        if result == FM.MENU_HT_ITEM:
            self.ContextMenu.CurrentMenuItem = self.GetMenuItems()[menuid]
        super().ProcessMouseRClick(pos)

    def WriteToFile(self, filename):
        ...

    def ReadFromFile(self, filename:str|Path):
        PopmenuFile = Path(filename)
        if not PopmenuFile.is_file():
            wx.LogError(f"Tried to edit a missing or non-file popmenu: {filename}")
            return {}

        contents = PopmenuFile.read_text()

        self.BuildFromLines(contents.splitlines(), True)


    def BuildFromLines(self, lines, is_main_request = False):

        if is_main_request:  # this is the top level request, peel off the outside layers
            while lines:
                line = lines.pop(0).strip()
                line = re.sub(r'\s*//.*', '', line) # remove comments

                if line == '': continue
                elif match := re.match(r'Menu\s+(.*)', line):
                    self.Title = match.group(1).strip('"')

                    if lines.pop(0).strip() != '{':
                        wx.LogError("Menu statement not followed by a '{', canceling")
                        return
                    else:
                        break

        # OK, we should be into the juicy innards of the file.  Push "lines" through it
        while lines:
            line = lines.pop(0).strip()

            line = re.sub(r'\s*//.*', '', line) # remove comments

            if line == '':
                continue
            elif line == "}":
                # return from recursive call, which was made down below when we found a "Menu"
                return
            elif line == "Divider":
                self.AppendItem(PEDivider(self, {}))
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

                LockedOptions = {}
                for lockedline in LockedData:
                    linematch = re.match(r'(\w+)\s+(.*)', lockedline)
                    if not linematch:
                        wx.LogError(f'Malformed line in LockedOption section: "{line}", canceling')
                        return {}

                    OptName, OptPayload = linematch.group(1,2)
                    OptName = OptName.strip('"')
                    OptPayload = OptPayload.strip('"')

                    if not OptName in ('DisplayName', 'Command', 'Authbit', 'Badge', 'RewardToken', 'StoreProduct', 'Icon', 'PowerReady'):
                        wx.LogError(f'Unknown keyword "{OptName}" in LockedOption section, canceling')
                        return {}

                    LockedOptions[OptName] = OptPayload

                optname = LockedOptions['DisplayName']
                if not optname:
                    wx.LogError("There was a LockedOption with no DisplayName, that's bad, canceling")
                    return

                self.AppendItem(PELockedOption(self, LockedOptions))
            elif match := re.match(r'Title\s+(.*)', line):
                self.AppendItem(PETitle(self, match.group(1).strip('"')))
            elif match := re.match(r'Menu\s+(.*)', line):
                MenuName = match.group(1).strip('"')
                if lines.pop(0).strip() != '{':
                    wx.LogError("Menu statement not followed by a '{', canceling")
                    return {}
                newMenu = Popmenu(self)
                newMenu.BuildFromLines(lines)
                self.AppendItem(PEMenu(self, {MenuName: newMenu}))
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

                self.AppendItem(PEOption(self, {Optname.strip('"') : OptPayload}))

class Popmenu_ContextMenu(FM.FlatMenu):
    def __init__(self, parent):
        super().__init__(parent)

        editMenu   = FM.FlatMenuItem(self, wx.ID_ANY, "Edit")
        deleteMenu = FM.FlatMenuItem(self, wx.ID_ANY, "Delete")
        moveUpMenu = FM.FlatMenuItem(self, wx.ID_ANY, "Move Up")
        moveDnMenu = FM.FlatMenuItem(self, wx.ID_ANY, "Move Down")
        self.AppendItem(editMenu)
        self.AppendItem(deleteMenu)
        self.AppendItem(moveUpMenu)
        self.AppendItem(moveDnMenu)

        self.ParentMenu = parent
        self.CurrentMenuItem = None

        self.Bind(wx.EVT_MENU, self.OnContextEdit, editMenu)
        self.Bind(wx.EVT_MENU, self.OnContextDelete, deleteMenu)
        self.Bind(wx.EVT_MENU, self.OnContextMoveUp, moveUpMenu)
        self.Bind(wx.EVT_MENU, self.OnContextMoveDown, moveDnMenu)

    def OnContextEdit(self, _):
        if cmi := self.CurrentMenuItem:
            wx.MessageBox(f'Edit not yet implemented;  would be editing "{cmi.GetLabel()}"', "Edit Item")
        else:
            wx.LogError("Context menu had no menu item to work with -- this is a bug!")

    def OnContextDelete(self, _):
        if cmi := self.CurrentMenuItem:
            result = wx.MessageBox(f'About to delete menu item "{cmi.GetLabel()}" -- this cannot be undone.  Continue?', "Delete Menu Item", wx.YES_NO)
            if result == wx.NO: return

            self.ParentMenu.DestroyItem(cmi)
            self.CurrentMenuItem = None
        else:
            wx.LogError("Context menu had no menu item to work with -- this is a bug!")

    def OnContextMoveUp(self, _):
        if cmi := self.CurrentMenuItem:
            currentPosition = self.ParentMenu.FindMenuItemPosSimple(cmi)
            self.ParentMenu.Remove(cmi)
            self.ParentMenu.InsertItem(currentPosition - 1, cmi)
        else:
            wx.LogError("Context menu had no menu item to work with -- this is a bug!")

    def OnContextMoveDown(self, _):
        if cmi := self.CurrentMenuItem:
            currentPosition = self.ParentMenu.FindMenuItemPosSimple(cmi)
            self.ParentMenu.Remove(cmi)
            self.ParentMenu.InsertItem(currentPosition + 1, cmi)
        else:
            wx.LogError("Context menu had no menu item to work with -- this is a bug!")

class PEMenuItem(FM.FlatMenuItem):
    def __init__(self, parent, data, **kwargs):
        super().__init__(parent, wx.ID_ANY, **kwargs)

        self.Parent = parent
        self.SetContextMenu(parent.ContextMenu)
        self.Data = data

class PEMenu(PEMenuItem):
    def __init__(self, parent, data):
        [(menuname, submenu)] = data.items()
        super().__init__(parent, label = menuname, data = data)
        self.SetSubMenu(submenu)

class PETitle(PEMenuItem):
    def __init__(self, parent, data):
        super().__init__(parent, label = data, data = data)
        self.Enable(False)

class PEDivider(PEMenuItem):
    def __init__(self, parent, data):
        super().__init__(parent, data, kind = wx.ITEM_SEPARATOR)

class PEOption(PEMenuItem):
    def __init__(self, parent, data):
        [(optname, _)] = data.items()
        super().__init__(parent, data, label = optname)

class PELockedOption(PEMenuItem):
    def __init__(self, parent, data):
        super().__init__(parent, data, label = data['DisplayName'])

itemclasses = {
    'Title'        : PETitle,
    'Divider'      : PEDivider,
    'Option'       : PEOption,
    'LockedOption' : PELockedOption,
    'Menu'         : PEMenu,
}
