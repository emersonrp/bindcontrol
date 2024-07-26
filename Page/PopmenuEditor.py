import wx
from Page import Page
from Help import HelpHTMLWindow
from UI.ControlGroup import cgTextCtrl
from UI.PrefsDialog import PrefsDialog
from typing import Callable

from pathlib import Path
from datetime import datetime
import re
import platform

import FM.flatmenu as FM

def GetMenuPathForGamePath(gamepath = None):
    gamepath = gamepath or Path(wx.ConfigBase.Get().Read('GamePath'))
    if not gamepath.is_dir():
        wx.MessageBox("Your Game Directory is not set up correctly.  Please visit the Preferences dialog.")
        return

    gamelang = wx.ConfigBase.Get().Read('GameLang')
    menupath = gamepath
    pathparts = ['data', 'Texts', gamelang, 'Menus']
    # Here's a wacky thing we do for Linux / Mac users:
    while pathparts:
        # walk through the parts and find them non-case-sensitively
        pathpart = pathparts.pop(0)
        pathglob = sorted(menupath.glob(pathpart, case_sensitive = False))
        # if we have it, march on
        if pathglob:
            menupath = pathglob[0]
        # Otherwise, glom the rest on there and offer to make the path.
        else:
            menupath = menupath.joinpath(pathpart, *pathparts)
            if wx.MessageBox(f'Menu directory {menupath} does not exist.  Create?', 'No Menu Dir', wx.YES_NO) == wx.NO:
                return
            menupath.mkdir(parents = True)
            break

    return menupath

class PopmenuEditor(Page):
    def __init__(self, parent):
        super().__init__(parent, bind_events = False)

        self.CurrentMenu = None
        self.MenuList = {}  # dict for menu objects for left-side list

        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(Sizer)


        self.LoadedMenuFont = wx.Font(wx.FontInfo().Italic(False).Bold(False))
        self.UnloadedMenuFont = wx.Font(wx.FontInfo().Italic())
        self.ModifiedMenuFont = wx.Font(wx.FontInfo().Bold())

        LeftPanelWidth = 250

        splitter = wx.SplitterWindow(self, style = wx.VERTICAL)
        splitter.SetMinimumPaneSize(LeftPanelWidth)

        MenuList = wx.Panel(splitter)
        MenuListSizer = wx.BoxSizer(wx.VERTICAL)
        MenuList.SetSizer(MenuListSizer)

        self.NewMenuButton       = wx.Button(MenuList, label = "Create New Menu")
        self.ImportMenuButton    = wx.Button(MenuList, label = "Import Menu File to Game Dir")
        self.DeleteMenuButton    = wx.Button(MenuList, label = "Delete Menu from Game Dir")
        self.NewMenuButton.Enable(False)
        self.ImportMenuButton.Enable(False)
        self.DeleteMenuButton.Enable(False)

        MenuListSizer.Add(self.NewMenuButton, 0, wx.EXPAND|wx.ALL, 6)
        MenuListSizer.Add(self.ImportMenuButton, 0, wx.EXPAND|wx.ALL, 6)
        MenuListSizer.Add(self.DeleteMenuButton, 0, wx.EXPAND|wx.ALL, 6)

        self.MenuListCtrl = wx.ListCtrl(MenuList, style = wx.LC_SINGLE_SEL|wx.LC_REPORT)
        self.MenuListCtrl.AppendColumn('Installed Menus', width = LeftPanelWidth - 12)
        MenuListSizer.Add(self.MenuListCtrl, 1, wx.EXPAND|wx.ALL, 6)
        self.MenuListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListSelect)

        self.NewMenuButton.Bind(wx.EVT_BUTTON, self.OnNewMenuButton)
        self.ImportMenuButton.Bind(wx.EVT_BUTTON, self.OnImportMenuButton)
        self.DeleteMenuButton.Bind(wx.EVT_BUTTON, self.OnDeleteMenuButton)

        self.MenuEditor = wx.Panel(splitter)
        MESizer = wx.BoxSizer(wx.VERTICAL)
        self.MenuEditor.SetSizer(MESizer)

        ButtonPanel = wx.Panel(self.MenuEditor)
        ButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        ButtonPanel.SetSizer(ButtonSizer)
        self.TestMenuButton = wx.Button(ButtonPanel, label = "Test Current Menu")
        self.TestMenuButton.Bind(wx.EVT_BUTTON, self.OnTestMenuButton)
        self.TestMenuButton.Enable(False)
        ButtonSizer.Add(self.TestMenuButton, 1, wx.EXPAND|wx.ALL, 6)

        self.WriteMenuButton = wx.Button(ButtonPanel, label = "Write Menu")
        self.WriteMenuButton.Bind(wx.EVT_BUTTON, self.OnWriteMenuButton)
        self.WriteMenuButton.Enable(False)
        ButtonSizer.Add(self.WriteMenuButton, 1, wx.EXPAND|wx.ALL, 6)

        self.MacroButton = wx.Button(ButtonPanel, label = "Generate Macro")
        self.MacroButton.Bind(wx.EVT_BUTTON, self.OnMacroButton)
        self.MacroButton.Enable(False)
        ButtonSizer.Add(self.MacroButton, 1, wx.EXPAND|wx.ALL, 6)

        MESizer.Add(ButtonPanel, 0, wx.ALL|wx.EXPAND, 10)

        # This should contain the instructions
        MiddlePanel = wx.Panel(self.MenuEditor)
        MiddleSizer = wx.BoxSizer(wx.VERTICAL)
        MiddlePanel.SetSizer(MiddleSizer)

        self.CheckGameDirBox = wx.Panel(MiddlePanel)
        self.CheckGameDirBox.SetBackgroundColour((255,200,200))
        CheckGameDirSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.CheckGameDirBox.SetSizer(CheckGameDirSizer)
        CheckGameDirText = wx.StaticText(self.CheckGameDirBox, label = "Your game directory is not set up correctly.  This is required for the Popmenu Editor to work.  Please visit the Preferences dialog.")
        CheckGameDirSizer.Add(CheckGameDirText, 1, wx.ALIGN_CENTER|wx.ALL, 10)
        OpenPrefsButton = wx.Button(self.CheckGameDirBox, label = "Open Preferences")
        OpenPrefsButton.Bind(wx.EVT_BUTTON, self.OnOpenPrefsButton)
        CheckGameDirSizer.Add(OpenPrefsButton,  0, wx.EXPAND|wx.ALL, 10)
        self.CheckGameDirBox.Hide()

        self.CheckMenuDirBox = wx.Panel(MiddlePanel)
        self.CheckMenuDirBox.SetBackgroundColour((255,200,200))
        CheckMenuDirSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.CheckMenuDirBox.SetSizer(CheckMenuDirSizer)
        CheckMenuDirText = wx.StaticText(self.CheckMenuDirBox, label = "Your Popmenu directory does not exist.  BindControl can create it for you.")
        CheckMenuDirSizer.Add(CheckMenuDirText, 1, wx.ALIGN_CENTER|wx.ALL, 10)
        CreateDirButton = wx.Button(self.CheckMenuDirBox, label = "Create Directory")
        CreateDirButton.Bind(wx.EVT_BUTTON, GetMenuPathForGamePath)
        CheckMenuDirSizer.Add(CreateDirButton,  0, wx.EXPAND|wx.ALL, 10)
        self.CheckMenuDirBox.Hide()

        self.InstructionBox = HelpHTMLWindow(MiddlePanel, "PopmenuInstructions.html", size = wx.DefaultSize)

        MiddleSizer.Add(self.CheckGameDirBox, 0, wx.EXPAND|wx.ALL, 15)
        MiddleSizer.Add(self.CheckMenuDirBox, 0, wx.EXPAND|wx.ALL, 15)
        MiddleSizer.Add(self.InstructionBox,  1, wx.EXPAND|wx.ALL, 25)

        MESizer.Add(MiddlePanel, 1, wx.EXPAND|wx.ALL, 10)

        splitter.SplitVertically(MenuList, self.MenuEditor, LeftPanelWidth)

        Sizer.Add(splitter, 1, wx.EXPAND)

        self.Layout()

    def OnOpenPrefsButton(self, _):
        with PrefsDialog(self) as dlg:
            dlg.ShowAndUpdatePrefs()
        self.SynchronizeUI()

    def SynchronizeUI(self, _ = None):
        NoErrors = True
        gamepath = Path(wx.ConfigBase.Get().Read('GamePath'))
        if gamepath.is_dir():
            self.CheckGameDirBox.Hide()
        else:
            self.CheckGameDirBox.Show()
            NoErrors = False

        if NoErrors:
            if GetMenuPathForGamePath():
                self.CheckMenuDirBox.Hide()
            else:
                self.CheckMenuDirBox.Show()
                NoErrors = False

        # TODO - if we have no installed menus, this will try again and again
        # every time we switch to the tab.  That's not a dealbreaker I guess
        if NoErrors and (self.MenuListCtrl.GetItemCount() == 0):
            self.LoadMenusFromMenuDir()

        self.NewMenuButton.Enable(NoErrors)
        self.ImportMenuButton.Enable(NoErrors)

    def OnTestMenuButton(self, evt):
        if self.CurrentMenu:
            self.CurrentMenu.Popup(wx.GetMousePosition())
        evt.Skip()

    def OnWriteMenuButton(self, _):
        # GetMenuPathForGamePath shows its own errors
        if not (menupath := GetMenuPathForGamePath()):
            return

        cm = self.CurrentMenu
        if cm:
            filepath = menupath / f"{cm.Title}.mnu"
            if filepath.is_file():
                mlc = self.MenuListCtrl
                info = self.MenuList.get(mlc.GetItemData(mlc.FindItem(-1, cm.Title)), {})
                if not info:
                    wx.LogError(f"Can't get info for current menu {cm.Title}")
                    return
                if info['filename'] != str(filepath):
                    if wx.MessageBox(f'The file "{filepath}" already exists and was not the source of this menu.  Overwrite?', 'Menu Exists', wx.YES_NO) == wx.NO:
                        return

            # OK, we have sanity-checked (TODO: there might be more of this to come) - let's write the file.
            try:
                cm.WriteToFile(filepath)
            except Exception as e:
                wx.LogError(f"Something broke inside WriteToFile: {e}")

        else: # cm is falsey
            wx.LogError("No current menu to save, canceling.  This is a bug.")

    def OnMacroButton(self, _):
        cm = self.CurrentMenu
        if cm:
            with wx.Dialog(self, title = f"Macro for {cm.Title}",) as dlg:
                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.Add(wx.StaticText(dlg, label = "Paste the following into the game to create your macro button:"), 1, wx.EXPAND|wx.ALL, 10)
                sizer.Add(wx.TextCtrl(dlg, value = f"/macro {cm.Title} popmenu {cm.Title}", style = wx.TE_READONLY), 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
                sizer.Add(dlg.CreateButtonSizer(wx.OK), 1, wx.EXPAND|wx.ALL, 10)
                dlg.SetSizerAndFit(sizer)
                dlg.Layout()

                dlg.ShowModal()

    def OnNewMenuButton(self, _ = None):
        mlc = self.MenuListCtrl
        newmenuname = self.GetNewMenuName()
        newmenu = Popmenu(self)
        newmenu.Title = newmenuname
        newmenu.AppendItem(PETitle(newmenu, newmenuname))
        listitem = mlc.Append([newmenuname])
        mlc.SetItemData(listitem, menuID := wx.NewId())
        self.MenuList[menuID] = {'menu' : newmenu}
        newmenu.SetModified()

    def LoadMenusFromMenuDir(self):
        # GetMenuPathForGamePath shows its own errors
        menupath = GetMenuPathForGamePath()

        if menupath:
            for menufile in sorted(menupath.glob('*.mnu', case_sensitive = False)):
                with menufile.open() as f:
                    menuname = ''
                    while not menuname:
                        line = f.readline().strip()
                        if match := re.match(r'Menu\s+(.*)', line):
                            menuname = match.group(1).strip('"')

                    item = self.MenuListCtrl.Append([menuname])
                    self.MenuListCtrl.SetItemFont(item, self.UnloadedMenuFont)
                    self.MenuListCtrl.SetItemData(item, menuID := wx.NewId())
                    self.MenuList[menuID] = {'filename': str(menufile)}

                    f.close()

    def GetNewMenuName(self, dupe_menu_name = None):
        if dupe_menu_name:
            wx.MessageBox(f'There already exists a menu called "{dupe_menu_name}" - please select a different name.', "Menu Already Exists", wx.OK)

        with wx.TextEntryDialog(self, "Enter new menu name", "New Menu") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                newmenuname = dlg.GetValue()
                if self.MenuListCtrl.FindItem(-1, newmenuname) != wx.NOT_FOUND:
                    return self.GetNewMenuName(dupe_menu_name = newmenuname)
                else:
                    return newmenuname

    def OnImportMenuButton(self, _):
        # GetMenuPathForGamePath shows its own errors
        if not (menupath := GetMenuPathForGamePath()):
            return

        with wx.FileDialog(self, "Import Popmenu file", wildcard="MNU files (*.mnu)|*.mnu",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            origfilepath = fileDialog.GetPath()
            newmenu = Popmenu(self)
            if newmenu.ReadFromFile(origfilepath):
                filepath = menupath / Path(origfilepath).name
                item = None
                if self.MenuListCtrl.FindItem(-1, newmenu.Title) != wx.NOT_FOUND:
                    newmenu.Title = self.GetNewMenuName(dupe_menu_name = newmenu.Title)

                try:
                    item = self.MenuListCtrl.Append([newmenu.Title])
                    self.MenuList[menuID := wx.NewId()] = {'menu': newmenu, 'filename': str(filepath)}
                    self.MenuListCtrl.SetItemData(item, menuID)
                    self.MenuListCtrl.Select(item)
                    self.ToggleTopButtons(True)
                    self.CurrentMenu = newmenu
                    newmenu.WriteToFile(filepath)
                except Exception as e:
                    wx.LogError(f"Something went wrong importing menu file: {e}")
                    if item:
                        self.MenuListCtrl.DeleteItem(item)


    def OnDeleteMenuButton(self, _):
        mlc = self.MenuListCtrl
        selection = mlc.GetFirstSelected()
        menuname = mlc.GetItemText(selection)
        info = self.MenuList.get(mlc.GetItemData(selection), {})

        result = wx.MessageBox(f'This will delete "{menuname}" from this list, and from the menu directory.  This cannot be undone.  Continue?', "Delete Menu Item", wx.YES_NO)
        if result == wx.NO: return

        if filename := info.get('filename', None):
            # TODO do we want any further sanity checking?
            Path(filename).unlink(missing_ok = True)

        mlc.DeleteItem(selection)

    def OnListSelect(self, evt):
        item = evt.GetIndex()
        info = self.MenuList.get(self.MenuListCtrl.GetItemData(item), {})
        if menu := info.get('menu', None):
            self.CurrentMenu = menu
        elif filename := info.get('filename', None):
            newmenu = Popmenu(self)
            if newmenu.ReadFromFile(filename):
                self.MenuList[self.MenuListCtrl.GetItemData(item)] = {'filename': filename, 'menu': newmenu}
                self.MenuListCtrl.SetItemFont(item, self.LoadedMenuFont)
                self.CurrentMenu = newmenu
            else:
                del newmenu
                self.CurrentMenu = None
        else:
            wx.LogError("Something was in the menu list that had no filename or menu attached.  This is a bug.")

        if self.CurrentMenu:
            self.ToggleTopButtons(True)
            self.TestMenuButton.SetLabel(f'Test "{self.MenuListCtrl.GetItemText(item)}"')
        else:
            self.ToggleTopButtons(False)
            self.TestMenuButton.SetLabel("Test Current Menu")

        if evt: evt.Skip()

    def ToggleTopButtons(self, show):
        self.TestMenuButton.Enable(show)
        self.WriteMenuButton.Enable(show)
        self.MacroButton.Enable(show)
        self.DeleteMenuButton.Enable(show)

    def CheckForModifiedMenus(self):
        mlc = self.MenuListCtrl
        for item in range(0, mlc.GetItemCount()):
            info = self.MenuList.get(mlc.GetItemData(item), {})
            menu = info.get('menu', None)
            if menu and menu.Modified:
                return True

class Popmenu(FM.FlatMenu):
    ContextMenu    = None
    SubContextMenu = None
    ProgressDialog = None
    def __init__(self, parent):
        super().__init__(parent)

        # Let's make just one of each context menu for the whole class
        Popmenu.ContextMenu    = Popmenu.ContextMenu    or Popmenu_ContextMenu(self)
        Popmenu.SubContextMenu = Popmenu.SubContextMenu or Popmenu_SubContextMenu(self)
        self.Title             = ''
        self.LockedData        = []
        self.CreditComments    = []  # top-level popmenus we keep the opening comments for credit's sake
        self.Modified          = False

    def SetModified(self, modified = True):
        # pass this up from submenus.  There's probably a more correct way to do this
        if isinstance(self.Parent, Popmenu):
            self.Parent.SetModified(modified)
        else:
            self.Modified = modified
            mlc = self.Parent.MenuListCtrl
            item = mlc.FindItem(-1, self.Title)
            font = (self.Parent.ModifiedMenuFont if modified else self.Parent.LoadedMenuFont)
            mlc.SetItemFont(item, font)

    def Dismiss(self, dismissParent = False, resetOwner = False):
        # TODO - here's where we need to come up with logic not to dismiss
        # just because a menu item got clicked.  But when -do- we dismiss?
        # This is going to be fiddly.

        # First stab - did we click on a menu item?  Don't close that menu, if so
        # TODO this sorta works but breaks if we right-click and edit/delete/etc
        # (result, _) = self.HitTest(self.ScreenToClient(wx.GetMousePosition()))
        # if result != FM.MENU_HT_ITEM:
             super().Dismiss(dismissParent, resetOwner)

    # hook the right click behavior to tell ContextMenu who got right-clicked
    def ProcessMouseRClick(self, pos):
        (result, menuid) = self.HitTest(pos)
        if result == FM.MENU_HT_ITEM:
            menuitem = self.GetMenuItems()[menuid]
            if menuitem: menuitem.ConfigureContextMenu()
        super().ProcessMouseRClick(pos)

    # recursive method to write the file to <filepath> -- no sanity-checking is done inside here.
    def WriteToFile(self, filepath, outputlines = [], indentlevel = 0):
        # If this is the outermost request (indent == 0), add the credits
        if indentlevel == 0:
            if outputlines:
                wx.LogError("top level WriteToFile got outputlines - this is a bug")
                return

            outputlines = self.CreditComments
            outputlines.append('')
            outputlines.append(f'// Saved from BindControl {datetime.now()}')

        # top of each "menu" clause, insert the initial two lines
        indent = "    " * indentlevel
        outputlines.append(f'{indent}Menu "{self.Title}"')
        outputlines.append(f'{indent}{{')
        indentlevel += 1
        indent = "    " * indentlevel

        # now loop
        for menuitem in self.GetMenuItems():
            if isinstance(menuitem, PEDivider):
                outputlines.append(f"{indent}Divider")
            elif isinstance(menuitem, PETitle):
                outputlines.append(f'{indent}Title "{menuitem.Data}"')
            elif isinstance(menuitem, PEOption):
                [(optname, optpayload)] = menuitem.Data.items()
                if re.search('"', optpayload):
                    optpayload = f"<&{optpayload}&>"
                else:
                    optpayload = f'"{optpayload}"'
                outputlines.append(f'{indent}Option "{optname}" {optpayload}')
            elif isinstance(menuitem, PEMenu):
                [(subname, submenu)] = menuitem.Data.items()
                if submenu:
                    submenu.WriteToFile(filepath, outputlines, indentlevel)
                else:
                    raise Exception(f"Submenu entry {subname} had no menu attached.  This is a bug.")
            elif isinstance(menuitem, PELockedOption):
                outputlines.append(f"{indent}LockedOption")
                outputlines.append(f"{indent}{{")
                for (LOName, LOStuff) in menuitem.Data.items():
                    outputlines.append(f"{indent}    {LOName} {LOStuff}")
                outputlines.append(f"{indent}}}")
            else:
                raise Exception(f"There was a mystery item inside menu {self.Title}, canceling write.  This is a bug.")
        indentlevel -= 1
        indent = "    " * indentlevel
        outputlines.append(f"{indent}}}")

        if indentlevel > 0: return

        outputfile = Path(filepath)
        try:
            # Let's \r\n so we're writing Windows files in all cases
            outputfile.write_text('\r\n'.join(outputlines), newline = '')
            self.SetModified(False)
        except Exception as e:
            wx.LogError(f"Something went wrong writing to {filepath}: {e}")

    def ReadFromFile(self, filename:str|Path):
        PopmenuFile = Path(filename)
        if not PopmenuFile.is_file():
            wx.LogError(f"Tried to edit a missing or non-file popmenu: {filename}")
            return {}

        try:
            contents = PopmenuFile.read_text()
        except Exception:
            try:
                contents = PopmenuFile.read_text(encoding = 'latin_1')
            except Exception:
                try:
                    contents = PopmenuFile.read_text(encoding = 'cp1252')
                except Exception as e:
                    wx.LogError(f'Invalid characters found in file {filename}: {e} - canceling')
                    return False

        lines = contents.splitlines()
        # Windows only can use ~ 30K unique IDs.  BadgeReporterExtended.mnu will crash it
        if platform.system() == 'Windows' and len(lines) > 27000:
            result = wx.MessageBox("This menu file is pathologically large.  Attempting to load it may cause strange behaviors or even crash BindControl.  Continue?", "Menu too large", wx.YES_NO)
            if result == wx.NO: return False

        self.BuildFromLines(lines, 'main')

        # Just in case we didn't finish the dialog for some reason, finish it
        if Popmenu.ProgressDialog:
            Popmenu.ProgressDialog.Update(Popmenu.ProgressDialog.GetRange())
            Popmenu.ProgressDialog.Destroy()
            Popmenu.ProgressDialog = None

        return True

    def BuildFromLines(self, lines, request_type = ''):
        is_main_request = request_type == "main"
        is_lock_request = request_type == "lock"

        if is_main_request:  # this is the top level request, peel off the outside layers
            # first let's clean our data
            newlines = []
            foundFirstMenu = False
            while lines:
                line = lines.pop(0).strip()

                # collect the initial // comments into the credits before snipping them
                if not foundFirstMenu:
                    if re.match(r'//', line):
                        self.CreditComments.append(line)
                    if re.match(r'Menu\s+(.*)', line):
                        foundFirstMenu = True

                # next, match for any non-URL '//' in there
                if re.search(r'(?<!\:)//', line):
                    # and remove comments
                    line = re.sub(r'\s*//.*', '', line)

                # Then, look for } at the end of a content-filled line
                if line != '}' and re.search('}$', line):
                    # and if it's there, snip it off and insert a '}' line instead
                    line = re.sub(r'\s*}$', '', line)
                    lines.insert(0, '}')
                line = line.strip() # once more with feeling

                if line: newlines.append(line)

            lines = newlines

            # now start over.  Look for the initial "Menu" which should be near or at the top now.
            while lines:
                line = lines.pop(0)
                if match := re.match(r'Menu\s+(.*)', line):
                    self.Title = match.group(1).strip('"')
                    break

        # Let's instantiate the Progress Dialog iff we're the main request
        if is_main_request:
            Popmenu.ProgressDialog = wx.ProgressDialog('Loading', f'Loading popmenu "{self.Title}"...', len(lines),
                                                      style = wx.PD_APP_MODAL|wx.PD_AUTO_HIDE|wx.PD_REMAINING_TIME)

        # OK, we should be into the juicy innards of the file.  Push the rest of "lines" through it
        while lines:
            line = lines.pop(0)
            if Popmenu.ProgressDialog:
                Popmenu.ProgressDialog.Update(Popmenu.ProgressDialog.GetValue() + 1)

            if is_lock_request:  # we're in a lockedoption subrequest, act differently
                if   line == '{': continue
                elif line == '}': # end of lock section, process accumulated stuff
                    LockedOptions = {}
                    for lockedline in self.LockedData:
                        linematch = re.match(r'(\w+)(\s+(.*))?', lockedline)
                        if not linematch:
                            wx.LogWarning(f'Malformed line in LockedOption section: "{line}", skipping')
                            continue

                        OptName, OptPayload = linematch.group(1,3)
                        OptName = OptName.strip('"')
                        OptPayload = str(OptPayload).strip('"')

                        OptName = self.NormalizeOptName(OptName)

                        if not OptName in ('DisplayName', 'Command', 'Authbit', 'Badge', 'RewardToken', 'StoreProduct', 'Icon', 'PowerReady', 'PowerOwned',):
                            wx.LogWarning(f'Unknown keyword "{OptName}" with payload "{OptPayload}" in LockedOption section {LockedOptions["DisplayName"]}, skipping it')
                            continue

                        LockedOptions[OptName] = OptPayload

                    optname = LockedOptions['DisplayName']
                    if not optname:
                        wx.LogWarning("There was a LockedOption with no DisplayName, skipping LockedOption section")
                        return

                    self.AppendItem(PELockedOption(self, LockedOptions))
                    self.LockedData = []
                    return
                else: # normal line
                    self.LockedData.append(line)
            else:
                if   line == '{': continue
                elif line == "}": return     # was a recursive "menu" call
                elif line == "Divider":
                    self.AppendItem(PEDivider(self, {}))
                elif line == "LockedOption":
                    self.BuildFromLines(lines, 'lock')
                elif match := re.match(r'Title\s+(.*)', line):
                    self.AppendItem(PETitle(self, match.group(1).strip('"')))
                elif match := re.match(r'Menu\s+(.*)', line):
                    MenuName = match.group(1).strip('"')
                    newMenu = Popmenu(self)
                    newMenu.Title = MenuName
                    newMenu.BuildFromLines(lines)
                    self.AppendItem(PEMenu(self, {MenuName: newMenu}))
                elif match := re.match(r'Option\s+(.*)', line):
                    OptionData = match.group(1)
                    if re.match(r'"', OptionData):
                        splitmatch = re.match(r'"([^"]+)"(\s+(.*))?', OptionData)
                    else:
                        splitmatch = re.match(r'([^\s]+)\(s+(.*))?', OptionData)
                    if splitmatch:
                        Optname, OptPayload = splitmatch.group(1,3)
                    else:
                        wx.LogError(f'Invalid "Option" clause in popmenu: "{OptionData}", canceling')
                        return {}
                    # "mission_helper.mnu" has Options with a name but no payload.  Ugly but we support now.
                    OptPayload = OptPayload or 'nop'
                    if re.match(r'"', OptPayload):
                        OptPayload = OptPayload.strip('"')
                    elif plmatch := re.match(r'<&(.*)&>', OptPayload):
                        OptPayload = plmatch.group(1)
                    self.AppendItem(PEOption(self, {Optname.strip('"') : OptPayload}))

    def NormalizeOptName(self, optname):
        for opt in ('DisplayName', 'Command', 'Authbit', 'Badge', 'RewardToken', 'StoreProduct', 'Icon', 'PowerReady', 'PowerOwned',):
            if optname.lower() == opt.lower():
                return opt

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

    def OnContextEdit(self, _):
        if cmi := self.CurrentMenuItem:
            if cmi.ShowEditor():
                self.Parent.SetModified()

    def OnContextDelete(self, _):
        if cmi := self.CurrentMenuItem:
            result = wx.MessageBox(f'About to delete menu item "{cmi.GetLabel()}" -- this cannot be undone.  Continue?', "Delete Menu Item", wx.YES_NO)
            if result == wx.NO: return

            self.Parent.DestroyItem(cmi)
            self.Parent.SetModified()
            self.CurrentMenuItem = None

    def OnContextMoveUp(self, _):
        if cmi := self.CurrentMenuItem:
            currentPosition = self.Parent.FindMenuItemPosSimple(cmi)
            self.Parent.Remove(cmi)
            self.Parent.InsertItem(currentPosition - 1, cmi)
            self.Parent.SetModified()

    def OnContextMoveDown(self, _):
        if cmi := self.CurrentMenuItem:
            currentPosition = self.Parent.FindMenuItemPosSimple(cmi)
            self.Parent.Remove(cmi)
            self.Parent.InsertItem(currentPosition + 1, cmi)
            self.Parent.SetModified()

    def OnContextInsert(self, evt):
        menuid = evt.GetId()
        if item := self.FindItem(menuid):
            if newitem := self.MakeNewItemForInsert(item):
                index = self.Parent.FindMenuItemPosSimple(self.CurrentMenuItem)
                self.Parent.InsertItem(index + 1, newitem)
                self.Parent.SetModified()

    def MakeNewItemForInsert(self, item):
        if   item.GetLabel() == "Submenu": data = {'' : Popmenu(self.Parent)}
        elif item.GetLabel() == "Option":  data = {'': ''}
        else: data = {}
        menuitemclass = itemclasses.get(item.GetLabel(), None)
        if menuitemclass:
            newitem = menuitemclass(self.Parent, data)
            return newitem.ShowEditor()
        else:
            wx.LogError(f"Unknown new menu item {item.GetLabel()}: this is a bug!")
            return False

class Popmenu_SubContextMenu(Popmenu_ContextMenu):
    def __init__(self, parent):
        super().__init__(parent)

        SubInsertMenu        = FM.FlatMenu(self)
        SubMenuMenuItem      = FM.FlatMenuItem(SubInsertMenu, wx.ID_ANY, "Submenu")
        SubTitleMenuItem     = FM.FlatMenuItem(SubInsertMenu, wx.ID_ANY, "Title")
        SubOptionMenuItem    = FM.FlatMenuItem(SubInsertMenu, wx.ID_ANY, "Option")
        SubLockedOptMenuItem = FM.FlatMenuItem(SubInsertMenu, wx.ID_ANY, "LockedOption")
        SubDividerMenuItem   = FM.FlatMenuItem(SubInsertMenu, wx.ID_ANY, "Divider")
        SubInsertMenu.AppendItem(SubMenuMenuItem)
        SubInsertMenu.AppendItem(SubTitleMenuItem)
        SubInsertMenu.AppendItem(SubOptionMenuItem)
        SubInsertMenu.AppendItem(SubLockedOptMenuItem)
        SubInsertMenu.AppendItem(SubDividerMenuItem)

        self.SubInsertMenuItem = FM.FlatMenuItem(self, wx.ID_ANY, 'Insert into Submenu')
        self.SubInsertMenuItem.SetSubMenu(SubInsertMenu)
        self.AppendItem(self.SubInsertMenuItem)

        SubInsertMenu.Bind(wx.EVT_MENU, self.OnContextSubInsert)

    def OnContextSubInsert(self, evt):
        menuid = evt.GetId()
        if item := self.FindItem(menuid):
            if newitem := self.MakeNewItemForInsert(item):
                self.CurrentMenuItem.GetSubMenu().AppendItem(newitem) # pyright: ignore


# Base Menu Item Class
class PEMenuItem(FM.FlatMenuItem):
    EditorDialog: Callable
    TitleFont = None
    def __init__(self, parent, data, label = ''):
        super().__init__(parent, wx.ID_ANY, label = label)

        self.SetContextMenu(parent.ContextMenu)
        self.Parent = parent
        self.Data   = data
        self.Editor = None
        PEMenuItem.TitleFont = PEMenuItem.TitleFont or wx.Font(wx.FontInfo().Bold())

    def ConfigureContextMenu(self):
        if cm := self.GetContextMenu():
            cm.CurrentMenuItem = self
            cm.EditMenuItem.Enable(self.HasEditor())
            menuid = self.Parent.FindMenuItemPosSimple(self)
            cm.MoveUpMenuItem.Enable(menuid != 0)
            cm.MoveDnMenuItem.Enable(menuid != len(self.Parent.GetMenuItems())-1)

    def ShowEditor(self):
        if not self.HasEditor(): return self
        self.Editor = self.Editor or self.EditorDialog()
        if self.Editor:
            if self.Editor.ShowModal() == wx.ID_OK:
                self.OnEditorUpdate()
                return self
            else:
                return False
        else:
            wx.LogError(f"Tried to edit {type(self).__name__} which has no self.Editor - this is a bug")

    def HasEditor(self):
        return hasattr(self, 'EditorDialog') and callable(getattr(self, 'EditorDialog'))

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
        self.SetContextMenu(parent.SubContextMenu)

    def EditorDialog(self):
        return wx.TextEntryDialog(self.Parent, message = "Menu Name:",
                                  caption = "Editing Menu item", value = self.GetText())

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
        self.SetFont(PEMenuItem.TitleFont)
        self.SetTextColour((128,128,128))

    def EditorDialog(self):
        return wx.TextEntryDialog(self.Parent, message = "Title:",
                                  caption = "Editing Title item", value = self.GetLabel())

    def OnEditorUpdate(self):
        newlabel = self.Editor.GetValue() # pyright: ignore
        self.Data = newlabel
        self.SetText(newlabel)
        self.Parent.UpdateItem(self)

class PEDivider(PEMenuItem):
    def __init__(self, parent, data):
        super().__init__(parent, data, label = "--------------------")

class PEOption(PEMenuItem):
    def __init__(self, parent, data = {'': ''}):
        [(optname, _)] = data.items()
        super().__init__(parent, data, label = optname or '')

    def EditorDialog(self):
        dialog = wx.Dialog(self.Parent, title = "Editing Option item",)
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
        name = data.get('DisplayName', '')
        super().__init__(parent, data, label = name)

    def EditorDialog(self):
        self.Ctrls = {}
        dialog = wx.Dialog(self.Parent, title = "Editing LockedOption item")
        paddingsizer = wx.BoxSizer(wx.VERTICAL)
        dialog.SetSizer(paddingsizer)

        sbsizer = wx.StaticBoxSizer(wx.VERTICAL, dialog, label = "LockedOption parameters")

        staticbox = sbsizer.GetStaticBox()

        gridsizer = wx.FlexGridSizer(2, 2, 5)
        for ctrl in ['DisplayName', 'Command', 'Icon', 'Authbit', 'Badge', 'RewardToken', 'StoreProduct', 'PowerReady', 'PowerOwned']:
            gridsizer.Add(wx.StaticText(staticbox, label = ctrl, style=wx.ALIGN_RIGHT), 0, wx.ALIGN_CENTER)
            self.Ctrls[ctrl] = cgTextCtrl(staticbox, size = (400, -1), value = self.Data.get(ctrl, ''))
            self.Ctrls[ctrl].Bind(wx.EVT_TEXT, self.CheckEditorFieldsForError)
            gridsizer.Add(self.Ctrls[ctrl], 1, wx.EXPAND)

        buttons = dialog.CreateButtonSizer(wx.OK|wx.CANCEL)

        sbsizer.Add(gridsizer, 1, wx.EXPAND|wx.ALL, 10)

        paddingsizer.Add(sbsizer, 1, wx.TOP|wx.RIGHT|wx.LEFT, 16)
        paddingsizer.Add(buttons, 0, wx.EXPAND|wx.ALL, 16)

        dialog.Bind(wx.EVT_BUTTON, self.OnOKButton, id = wx.ID_OK)

        self.CheckEditorFieldsForError()
        dialog.Fit()

        return dialog

    def OnOKButton(self, evt):
        if self.CheckEditorFieldsForError(): return
        evt.Skip()

    def CheckEditorFieldsForError(self, _ = None):
        hasError = False
        c = self.Ctrls
        if c['DisplayName'].GetValue() == '':
            c['DisplayName'].AddError('undef', 'DisplayName is mandatory')
            hasError = True
        else:
            c['DisplayName'].RemoveError('undef')

        AllUnset = True
        AtLeastOne = ['Authbit', 'Badge', 'RewardToken', 'StoreProduct', 'PowerReady', 'PowerOwned']
        for ctrl in AtLeastOne:
            if c[ctrl].GetValue() != '':
                AllUnset = False
                break

        for ctrl in AtLeastOne:
            if AllUnset:
                c[ctrl].AddError('unset', 'At least one of Authbit, Badge, RewardToken, StoreProduct, PowerReady, or PowerOwned must be set')
                hasError = True
            else:
                c[ctrl].RemoveError('unset')

        return hasError

    def OnEditorUpdate(self):
        data = {}
        for ctrl in ['DisplayName', 'Command', 'Icon', 'Authbit', 'Badge', 'RewardToken', 'StoreProduct', 'PowerReady', 'PowerOwned']:
            data[ctrl] = self.Ctrls[ctrl].GetValue()

        self.Data = data
        self.SetText(data['DisplayName'])
        self.Parent.UpdateItem(self)

itemclasses = {
    'Title'        : PETitle,
    'Divider'      : PEDivider,
    'Option'       : PEOption,
    'LockedOption' : PELockedOption,
    'Menu'         : PEMenu,
    'Submenu'      : PEMenu,
}
