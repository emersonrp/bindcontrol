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
        TestMenuButton = wx.Button(self.MenuEditor, label = "Test Current Popmenu")
        TestMenuButton.Bind(wx.EVT_BUTTON, self.OnTestMenuButton)
        MESizer.Add(TestMenuButton, 0, wx.ALL, 10)

        # This should contain the instructions
        MiddlePanel = wx.Panel(self.MenuEditor)
        MiddleSizer = wx.BoxSizer(wx.VERTICAL)
        MiddlePanel.SetSizer(MiddleSizer)
        MESizer.Add(MiddlePanel, 1, wx.EXPAND|wx.ALL, 10)

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
        cm = self.ContextMenu
        (result, menuid) = self.HitTest(pos)
        if result == FM.MENU_HT_ITEM:
            cm.ConfigureForMenuItem(menuid)
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

        self.EditMenuItem   = FM.FlatMenuItem(self, wx.ID_ANY, "Edit")
        self.DeleteMenuItem = FM.FlatMenuItem(self, wx.ID_ANY, "Delete")
        self.MoveUpMenuItem = FM.FlatMenuItem(self, wx.ID_ANY, "Move Up")
        self.MoveDnMenuItem = FM.FlatMenuItem(self, wx.ID_ANY, "Move Down")

        InsertMenu        = FM.FlatMenu(self)
        MenuMenuItem      = FM.FlatMenuItem(InsertMenu, wx.ID_ANY, "Submenu")
        TitleMenuItem     = FM.FlatMenuItem(InsertMenu, wx.ID_ANY, "Title")
        OptionMenuItem    = FM.FlatMenuItem(InsertMenu, wx.ID_ANY, "Option")
        LockedOptMenuItem = FM.FlatMenuItem(InsertMenu, wx.ID_ANY, "LockedOption")
        DividerMenuItem   = FM.FlatMenuItem(InsertMenu, wx.ID_ANY, "Divider")
        InsertMenu.AppendItem(MenuMenuItem)
        InsertMenu.AppendItem(TitleMenuItem)
        InsertMenu.AppendItem(OptionMenuItem)
        InsertMenu.AppendItem(LockedOptMenuItem)
        InsertMenu.AppendItem(DividerMenuItem)

        self.AppendItem(self.EditMenuItem)
        self.AppendItem(self.DeleteMenuItem)
        self.AppendItem(self.MoveUpMenuItem)
        self.AppendItem(self.MoveDnMenuItem)
        self.AppendSubMenu(InsertMenu, 'Insert')

        self.CurrentMenuItem = None

        self.Bind(wx.EVT_MENU, self.OnContextEdit, self.EditMenuItem)
        self.Bind(wx.EVT_MENU, self.OnContextDelete, self.DeleteMenuItem)
        self.Bind(wx.EVT_MENU, self.OnContextMoveUp, self.MoveUpMenuItem)
        self.Bind(wx.EVT_MENU, self.OnContextMoveDown, self.MoveDnMenuItem)
        InsertMenu.Bind(wx.EVT_MENU, self.OnContextInsert)

    def ConfigureForMenuItem(self, menuid):
        self.CurrentMenuItem = self.Parent.GetMenuItems()[menuid]
        self.EditMenuItem.Enable(self.CurrentMenuItem.Editor != None)
        self.MoveUpMenuItem.Enable(menuid != 0)
        self.MoveDnMenuItem.Enable(menuid != len(self.Parent.GetMenuItems())-1)

    def OnContextEdit(self, _):
        if cmi := self.CurrentMenuItem:
            cmi.ShowEditor()

    def OnContextDelete(self, _):
        if cmi := self.CurrentMenuItem:
            result = wx.MessageBox(f'About to delete menu item "{cmi.GetLabel()}" -- this cannot be undone.  Continue?', "Delete Menu Item", wx.YES_NO)
            if result == wx.NO: return

            self.Parent.DestroyItem(cmi)
            self.CurrentMenuItem = None

    def OnContextMoveUp(self, _):
        if cmi := self.CurrentMenuItem:
            currentPosition = self.Parent.FindMenuItemPosSimple(cmi)
            self.Parent.Remove(cmi)
            self.Parent.InsertItem(currentPosition - 1, cmi)

    def OnContextMoveDown(self, _):
        if cmi := self.CurrentMenuItem:
            currentPosition = self.Parent.FindMenuItemPosSimple(cmi)
            self.Parent.Remove(cmi)
            self.Parent.InsertItem(currentPosition + 1, cmi)

    def OnContextInsert(self, evt):
        menuid = evt.GetId()
        if item := self.FindItem(menuid):
            data = {}
            # TODO how do we insert something into an empty submenu?  This is a problem.
            if item.GetLabel() == "Submenu": data = {'' : Popmenu(self.Parent)}
            menuitemclass = itemclasses.get(item.GetLabel(), None)
            newitem = menuitemclass(self.Parent, data)
            index = self.Parent.FindMenuItemPosSimple(self.CurrentMenuItem)
            self.Parent.InsertItem(index + 1, newitem)
            newitem.ShowEditor()

# Base Menu Item Class
class PEMenuItem(FM.FlatMenuItem):
    def __init__(self, parent, data, **kwargs):
        super().__init__(parent, wx.ID_ANY, **kwargs)

        self.SetContextMenu(parent.ContextMenu)
        self.Parent = parent
        self.Data   = data
        self.Editor = self.EditorDialog()

    def ShowEditor(self):
        if self.Editor:
            if self.Editor.ShowModal() == wx.ID_OK:
                self.OnEditorUpdate()
        else:
            wx.LogError(f"Tried to edit {type(self).__name__} which has no self.Editor")

    def EditorDialog(self) -> wx.Dialog|None:
        wx.LogError(f"Editor not implemented for {type(self).__name__}")
        return None

    def OnEditorUpdate(self):
        wx.LogError(f"Editor update not implemented for {type(self).__name__}")

    def Serialize(self):
        wx.LogError(f"Serialize not implemented yet for {type(self).__name__}")
        return ""

# subclasses
class PEMenu(PEMenuItem):
    def __init__(self, parent, data):
        [(menuname, submenu)] = data.items()
        super().__init__(parent, data, label = menuname)
        self.SetSubMenu(submenu)

    def EditorDialog(self):
        return wx.TextEntryDialog(self.Parent, message = "Menu Name:",
                                  caption = "Editing menu item", value = self.GetText())

    def OnEditorUpdate(self):
        newlabel = self.Editor.GetValue() # pyright: ignore
        oldlabel = self.GetText()
        if oldlabel in self.Data:
            self.Data[newlabel] = self.Data[oldlabel]
            del self.Data[oldlabel]
        else:
            wx.LogError(f"Something went wrong trying to update a PEMenu: no such key {oldlabel}")
        self.SetText(newlabel)
        self.Parent.UpdateItem(self)

class PETitle(PEMenuItem):
    def __init__(self, parent, data):
        super().__init__(parent, data, label = data)
        self.SetFont(wx.Font(wx.FontInfo().Italic()))
        self.SetTextColour((128,128,128))

    def EditorDialog(self):
        return wx.TextEntryDialog(self.Parent, message = "Title:",
                                  caption = "Editing title item", value = self.GetLabel())

    def OnEditorUpdate(self):
        newlabel = self.Editor.GetValue() # pyright: ignore
        self.Data = newlabel
        self.SetText(newlabel)
        self.Parent.UpdateItem(self)

class PEDivider(PEMenuItem):
    def __init__(self, parent, data):
        super().__init__(parent, data, kind = wx.ITEM_SEPARATOR)

    def EditorDialog(self): return None
    def OnEditorUpdate(self): wx.LogError("Called OnEditorUpdate for a PEDivider, how did you get here?  This is a bug.")

class PEOption(PEMenuItem):
    def __init__(self, parent, data):
        [(optname, _)] = data.items()
        super().__init__(parent, data, label = optname)

    def EditorDialog(self):
        dialog = wx.Dialog(self.Parent, title = "Editing option item",)
        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dialog.SetSizer(dlgSizer)

        fieldSizer = wx.FlexGridSizer(2, 2, 5)
        fieldSizer.AddGrowableCol(1)
        [(optname, optstring)] = self.Data.items()
        fieldSizer.Add(wx.StaticText(dialog, label = "Name:", style = wx.ALIGN_RIGHT), 0, wx.ALIGN_CENTER_VERTICAL)
        self.NameField = wx.TextCtrl(dialog, value = optname)
        fieldSizer.Add(self.NameField, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        fieldSizer.Add(wx.StaticText(dialog, label = "Value:", style = wx.ALIGN_RIGHT), 0, wx.ALIGN_CENTER_VERTICAL)
        self.ValueField = wx.TextCtrl(dialog, value = optstring)
        fieldSizer.Add(self.ValueField, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)

        buttons = dialog.CreateButtonSizer(wx.OK|wx.CANCEL)

        dlgSizer.Add(fieldSizer, 1, wx.EXPAND|wx.ALL, 10)
        dlgSizer.Add(buttons,    0, wx.EXPAND|wx.ALL, 10)

        return dialog

    def OnEditorUpdate(self):
        newlabel = self.NameField.GetValue()
        newvalue = self.ValueField.GetValue()

        self.Data = {newlabel : newvalue}
        self.SetText(newlabel)
        self.Parent.UpdateItem(self)


class PELockedOption(PEMenuItem):
    def __init__(self, parent, data):
        super().__init__(parent, data, label = data['DisplayName'])

itemclasses = {
    'Title'        : PETitle,
    'Divider'      : PEDivider,
    'Option'       : PEOption,
    'LockedOption' : PELockedOption,
    'Menu'         : PEMenu,
    'Submenu'      : PEMenu,
}
