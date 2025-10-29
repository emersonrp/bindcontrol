import wx
import sys
import importlib
from Help import HelpButton
from wx.lib.expando import EVT_ETC_LAYOUT_NEEDED
from UI.CGControls import cgExpandoTextCtrl
from UI.ErrorControls import ErrorControlMixin
from Util.Paths import GetRootDirPath

import wx.lib.newevent
PowerBinderChanged, EVT_POWERBINDER_CHANGED = wx.lib.newevent.NewCommandEvent()

class PowerBinder(ErrorControlMixin, wx.TextCtrl):
    def __init__(self, parent, init : dict|None = None, extralength = 0):
        init = init or {}
        super().__init__(parent)
        self.CurrentState = init
        self.DialogParent = parent
        self.ExtraLength  = extralength # for complex binds to add the footprint of each step's BLF()

        self.SetHint("Click to launch PowerBinder")

        self.Bind(wx.EVT_LEFT_DOWN, self.OnClickPB)

    def OnClickPB(self, _) -> None:
        self.PowerBinderDialog().Show()

    def SaveToData(self) -> dict:
        return self.CurrentState

    # If we do this at __init__ time, the app doesn't launch.  Investigate why.
    def PowerBinderDialog(self):
        return PowerBinderDialog(self.DialogParent, self)

    def UpdateState(self, bindString, state) -> None:
        self.CurrentState = state
        self.SetValue(bindString)
        wx.PostEvent(self, PowerBinderChanged(wx.NewId()))

class PowerBinderDialog(wx.Dialog):
    def __init__(self, parent, powerbinder) -> None:
        super().__init__(parent, title = "PowerBinder", style = wx.DEFAULT_DIALOG_STYLE)

        self.Page        = parent.Page if hasattr(parent, 'Page') else None
        self.ExtraLength = powerbinder.ExtraLength
        self.PowerBinder = powerbinder

        self.LoadModules()

        self.AddCommandMenu = self.makeAddCommandMenu()

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer = sizer

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        AddCommandButton = wx.Button(self, label = 'Add Command')
        AddCommandButton.Bind(wx.EVT_BUTTON, self.OnAddCommandButton)
        AddCommandButton.Bind(wx.EVT_MENU,   self.OnAddCommandMenu)
        choiceSizer.Add(AddCommandButton, 1, wx.LEFT, 10)
        choiceSizer.Add(HelpButton(self, "PowerBinder.html", wintype="window"), 0, wx.LEFT, 10)
        sizer.Add(choiceSizer, 1, wx.EXPAND|wx.BOTTOM, 10)

        rearrangeCtrl = wx.BoxSizer(wx.HORIZONTAL)

        self.RearrangeList = wx.RearrangeList(self, size = wx.Size(550,400))
        self.RearrangeList.Bind(wx.EVT_LISTBOX, self.OnListSelect)
        self.RearrangeList.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRearrangeEdit)
        rearrangeCtrl.Add(self.RearrangeList, 1)

        rearrangeButtons = wx.BoxSizer(wx.VERTICAL)
        self.DelButton = wx.Button(self, label = "Delete")
        self.DelButton.Bind(wx.EVT_BUTTON, self.OnRearrangeDelete)
        self.EditButton = wx.Button(self, label = "Edit")
        self.EditButton.Bind(wx.EVT_BUTTON, self.OnRearrangeEdit)
        self.EditButton.Disable()
        upButton = wx.Button(self, label = "\u25B2")
        upButton.Bind(wx.EVT_BUTTON, self.OnRearrangeUp)
        downButton = wx.Button(self, label = "\u25BC")
        downButton.Bind(wx.EVT_BUTTON, self.OnRearrangeDown)
        rearrangeButtons.Add(upButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(downButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(self.EditButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(self.DelButton, 1, wx.BOTTOM, 10)
        rearrangeCtrl.Add(rearrangeButtons, 0, wx.LEFT, 10)

        sizer.Add(rearrangeCtrl, 0, wx.EXPAND|wx.TOP|wx.BOTTOM)

        bindStringPreviewSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.BindStringDisplay = cgExpandoTextCtrl(self, style = wx.TE_READONLY)
        self.BindStringDisplay.SetHint("Add Commands to create a bind string")
        bindStringPreviewSizer.Add(wx.StaticText(self, label = "Bind String:"), 0,
                        wx.ALIGN_CENTER_VERTICAL)
        bindStringPreviewSizer.Add(self.BindStringDisplay, 1, wx.LEFT, 10)

        sizer.Add(bindStringPreviewSizer, 0, wx.EXPAND|wx.TOP, 16)

        BSCountSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindStringCount = wx.StaticText(self)
        BSCountSizer.Add(self.BindStringCount, 0)

        if self.ExtraLength:
            BindStringCountHelp = wx.StaticText(self, label = '[?]')
            BindStringCountHelp.SetToolTip('This count includes extra characters that will be added to your Complex Bind when the files are written, and so may be larger than expected.')
            BSCountSizer.Add(BindStringCountHelp, 0, wx.LEFT, 3)

        sizer.Add(BSCountSizer, 0, wx.ALIGN_RIGHT|wx.BOTTOM, 16)

        sizer.Add(self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL), 0, wx.EXPAND)

        # need to dig around and get the OK button since we show this dialog modelessly now.
        okButton = self.FindWindow(self.GetAffirmativeId())
        okButton.Bind(wx.EVT_BUTTON, self.OnOKButton)

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10)

        self.Bind(EVT_ETC_LAYOUT_NEEDED, self.OnBindPreviewResize)

        self.SetSizerAndFit(vbox)
        self.Layout()

    def OnBindPreviewResize(self, evt) -> None:
        self.Fit()
        self.Layout()
        evt.Skip()

    def Show(self, show = True) -> bool:
        if show:
            self.LoadFromCurrentState()
            bindstring = self.MakeBindString()
            if bindstring != self.PowerBinder.GetValue():
                self.BindStringDisplay.AddError('nomatch', "The PowerBinder configuration doesn't match the bind string saved with the profile.  Check that the PowerBinder dialog is configured correctly before pressing 'OK' as this will overwrite the saved bind string.")
        retval = super().Show(show)
        self.SetFocus()
        return retval

    # Load plugins / modules from UI/PowerBinderCommand directory
    def LoadModules(self) -> None:
        path = GetRootDirPath() / 'UI' / 'PowerBinderCommand'

        for package_file in sorted(path.glob('*.py')):
            package = package_file.stem
            if package == '__init__': continue

            modstr = "UI.PowerBinderCommand." + package
            # check if we've already loaded this one, if so, we've done this before, bail out
            if modstr in sys.modules: return

            # do the actual importing
            mod = importlib.import_module(modstr)

            if modclass := getattr(mod, package, None):

                # put the class into menuStructure, commandClasses, and commandRevClasses
                if modName := getattr(modclass, 'Name', ''):
                    commandClasses[modName] = modclass
                    commandRevClasses[modclass] = modName
                else:
                    wx.LogError(f"Class {modclass} didn't define 'Name' - this is a bug")

                # TODO?  If we ever rename something more than once, we'll need this to be a list
                if depName := getattr(modclass, 'DeprecatedName', ''):
                    deprecatedCommandClasses[depName] = modclass

                # we treat "Custom Command" specially in the menu, so skip the "Menu" step for it
                if modName == "Custom Command": continue

                if modMenu := getattr(modclass, 'Menu', ''):
                    menuStructure[modMenu].append(modName)
                else:
                    wx.LogError(f"Module {modclass} didn't define 'Menu' - this is a bug")

            else:
                wx.LogError(f"Module {mod} didn't define a class of the same name - this is a bug!")

    def LoadFromCurrentState(self) -> None:
        self.RearrangeList.Clear()

        for item in self.PowerBinder.CurrentState:
            for cmd_type, data in item.items():
                commandClass = commandClasses.get(cmd_type)
                if not commandClass:
                    commandClass = deprecatedCommandClasses.get(cmd_type)
                    if not commandClass:
                        wx.LogError(f"Profile contained unknown custom bind command class {cmd_type}; ignoring it and continuing.")
                        continue
                newCommand = commandClass(self, data)
                index = self.RearrangeList.Append(newCommand.MakeListEntryString())
                self.RearrangeList.SetClientData(index, newCommand)
        self.UpdateBindStringDisplay()

    def GetCurrentState(self) -> list:
        data = []
        for index in range(self.RearrangeList.GetCount()):
            # check whether we have an object already attached to this choice
            if cmdObject := self.RearrangeList.GetClientData(index):
                if commandClassName := commandRevClasses[type(cmdObject)]:
                    data.append({commandClassName: cmdObject.Serialize()})
                else:
                    wx.LogError(f"Unknown command object type in SaveToData: {cmdObject}.  This is a bug.")
            else:
                wx.LogError(f"Item at index {index} in PowerBinder's RearrangeList didn't have Client Data.  This is a bug.")
        return data

    def OnAddCommandButton(self, evt) -> None:
        button = evt.EventObject
        if not self.AddCommandMenu:
            self.AddCommandMenu = self.makeAddCommandMenu()
        button.PopupMenu(self.AddCommandMenu)

    def OnOKButton(self, _) -> None:
        self.BindStringDisplay.RemoveError('nomatch')
        if self.PowerBinder:
            self.PowerBinder.UpdateState(self.MakeBindString(), self.GetCurrentState())
        self.Close()

    def OnRearrangeDelete(self, _) -> None:
        current = self.RearrangeList.GetSelection()
        if current == wx.NOT_FOUND: return

        self.RearrangeList.Delete(current)
        self.UpdateBindStringDisplay()

    def OnRearrangeUp(self, _) -> None:
        self.RearrangeList.MoveCurrentUp()
        self.UpdateBindStringDisplay()

    def OnRearrangeDown(self, _) -> None:
        self.RearrangeList.MoveCurrentDown()
        self.UpdateBindStringDisplay()

    def OnRearrangeEdit(self, _) -> None:
        index = self.RearrangeList.GetSelection()

        # check whether we have an object already attached to this choice
        cmdObject = None
        try:
            cmdObject = self.RearrangeList.GetClientData(index)
        except Exception:
            pass

        if cmdObject:
            if cmdObject.UseEditDialog and cmdObject.ShowEditDialog() == wx.ID_OK:
                self.RearrangeList.SetString(index, cmdObject.MakeListEntryString())
        else:
            wx.LogError("In OnRearrangeEdit, cmdObject was None.  This is a bug.")

        self.UpdateBindStringDisplay()

    # OnAddCommandMenu creates a new Command and adds it to the rearrangelist
    def OnAddCommandMenu(self, evt) -> None:
        menuitem = self.AddCommandMenu.FindItemById(evt.GetId())
        chosenName = menuitem.GetItemLabel()

        # make a new command object, attached to the parent dialog
        newCommandClass = commandClasses[chosenName]
        newCommand = newCommandClass(self)

        # show the edit dialog if this command needs it
        if newCommand:
            if newCommand.UseEditDialog and newCommand.ShowEditDialog() == wx.ID_CANCEL:
                return

        newBindIndex = self.RearrangeList.Append(newCommand.MakeListEntryString())
        self.RearrangeList.Select(newBindIndex)
        self.RearrangeList.SetClientData(newBindIndex, newCommand)

        self.OnListSelect()
        self.UpdateBindStringDisplay()

    def OnListSelect(self, _ = None) -> None:
        selected = self.RearrangeList.GetSelection()

        if selected != wx.NOT_FOUND:
            cmdObject = self.RearrangeList.GetClientData(selected)
            if cmdObject and cmdObject.UseEditDialog:
                self.EditButton.Enable()
            else:
                self.EditButton.Disable()

    def UpdateBindStringDisplay(self) -> None:
        bindstring = self.MakeBindString()
        self.BindStringDisplay.SetValue(bindstring)

        # If they made any change, assume they're moving on with their lives and stop bugging about it not matching.
        self.BindStringDisplay.RemoveError('nomatch')

        self.BindStringCount.SetLabel(f'{len(bindstring) + self.ExtraLength}/255 characters')

        if len(bindstring) + self.ExtraLength > 255:
            self.BindStringDisplay.AddError('toolong', 'This bind string, when written to file, will be longer than the maximum 255 characters, and will likely not work as expected, if at all.')
        else:
            self.BindStringDisplay.RemoveError('toolong')
            self.BindStringDisplay.SetToolTip(bindstring)

    def MakeBindString(self) -> str:
        cmdBindStrings = []
        for index in range(self.RearrangeList.GetCount()):
            c = self.RearrangeList.GetClientData(index)
            if c: cmdBindStrings.append(c.MakeBindString())

        bindstring = ('$$'.join(cmdBindStrings))
        return bindstring

    def makeAddCommandMenu(self) -> wx.Menu:

        CommandMenu = wx.Menu()

        for subname in menuStructure:
            submenu = wx.Menu()
            CommandMenu.AppendSubMenu(submenu, subname)
            for classname in menuStructure[subname]:
                submenu.Append(wx.ID_ANY, classname)

        CommandMenu.Append(wx.ID_ANY, 'Custom Command')

        return CommandMenu

menuStructure = {
        'Graphics / UI' : [ ],
        'Inspirations'  : [ ],
        'Powers'        : [ ],
        'Social'        : [ ],
        'Targeting'     : [ ],
        'Misc'          : [ ],
        # 'Custom Bind',  # we're going to add "Custom Bind" in by hand at the end,
                          # but I'm leaving it here to remind myself that we do that.
        }
commandClasses = {}
commandRevClasses = {}
deprecatedCommandClasses = {}

