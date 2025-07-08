import wx
import os, sys, importlib
from Help import HelpButton
from Icon import GetIcon
from pathlib import Path
from UI.ControlGroup import cgTextCtrl

class PowerBinderDialog(wx.Dialog):
    def __init__(self, parent, button, init = {}):
        super().__init__(parent, -1, "PowerBinder", style = wx.DEFAULT_DIALOG_STYLE)

        self.Page = parent.Page
        self.CurrentState = init

        self.LoadModules()

        self.EditDialog = None # make this at dialog-show time in LoadFromCurrentState
        self.Button = button
        self.AddStepMenu = self.makeAddStepMenu()

        sizer = wx.BoxSizer(wx.VERTICAL);
        self.mainSizer = sizer

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        AddStepButton = wx.Button(self, -1, 'Add Step')
        AddStepButton.Bind(wx.EVT_BUTTON, self.OnAddStepButton)
        AddStepButton.Bind(wx.EVT_MENU,   self.OnAddStepMenu)
        choiceSizer.Add(AddStepButton, 1, wx.LEFT, 10)
        choiceSizer.Add(HelpButton(self, "PowerBinder.html", type="window"), 0, wx.LEFT, 10)
        sizer.Add(choiceSizer, 1, wx.EXPAND|wx.BOTTOM, 10)

        rearrangeCtrl = wx.BoxSizer(wx.HORIZONTAL)

        self.RearrangeList = wx.RearrangeList(self, -1, size = wx.Size(550,400))
        self.RearrangeList.Bind(wx.EVT_LISTBOX, self.OnListSelect)
        self.RearrangeList.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRearrangeEdit)
        rearrangeCtrl.Add(self.RearrangeList, 1)

        rearrangeButtons = wx.BoxSizer(wx.VERTICAL)
        self.DelButton = wx.Button(self, -1, "Delete")
        self.DelButton.Bind(wx.EVT_BUTTON, self.OnRearrangeDelete)
        self.EditButton = wx.Button(self, -1, "Edit")
        self.EditButton.Bind(wx.EVT_BUTTON, self.OnRearrangeEdit)
        self.EditButton.Disable()
        upButton = wx.Button(self, -1, "\u25B2")
        upButton.Bind(wx.EVT_BUTTON, self.OnRearrangeUp)
        downButton = wx.Button(self, -1, "\u25BC")
        downButton.Bind(wx.EVT_BUTTON, self.OnRearrangeDown)
        rearrangeButtons.Add(upButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(downButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(self.EditButton, 1, wx.BOTTOM, 10)
        rearrangeButtons.Add(self.DelButton, 1, wx.BOTTOM, 10)
        rearrangeCtrl.Add(rearrangeButtons, 0, wx.LEFT, 10)

        sizer.Add(rearrangeCtrl, 0, wx.EXPAND|wx.TOP|wx.BOTTOM)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.BindStringDisplay = cgTextCtrl(self, -1, style=wx.TE_READONLY)
        choiceSizer.Add(wx.StaticText(self, -1, "Bind String:"), 0,
                        wx.ALIGN_CENTER_VERTICAL)
        choiceSizer.Add(self.BindStringDisplay, 1, wx.LEFT, 10)

        sizer.Add(choiceSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 16)

        sizer.Add(self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL), 0, wx.EXPAND)

        # need to dig around and get the OK button since we show this dialog modelessly now.
        okButton = self.FindWindow(self.GetAffirmativeId())
        okButton.Bind(wx.EVT_BUTTON, self.OnOKButton)

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL);
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10);

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.Fit()

    def Show(self, show = True):
        if show:
            self.LoadFromCurrentState()
            bindstring = self.MakeBindString()
            if bindstring != self.Button.tgtTxtCtrl.GetValue():
                self.BindStringDisplay.AddError('nomatch', "The PowerBinder configuration doesn't match the bind string saved with the profile.  Check that the PowerBinder dialog is configured correctly before pressing 'OK' as this will overwrite the saved bind string.")
        retval = super().Show(show)
        self.SetFocus()
        return retval

    # Load plugins / modules from UI/PowerBinderCommand directory
    def LoadModules(self):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        path = Path(base_path) / 'PowerBinderCommand'

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
                    print(f"Class {modclass} didn't define 'Name' - this is a bug")

                # TODO?  If we ever rename something more than once, we'll need this to be a list
                if depName := getattr(modclass, 'DeprecatedName', ''):
                    deprecatedCommandClasses[depName] = modclass

                # we treat "Custom Bind" specially in the menu, so skip the "Menu" step for it
                if modName == "Custom Bind": continue

                if modMenu := getattr(modclass, 'Menu', ''):
                    menuStructure[modMenu].append(modName)
                else:
                    print(f"Module {modclass} didn't define 'Menu' - this is a bug")

            else:
                print(f"Module {mod} didn't define a class of the same name - this is a bug!")

    def LoadFromCurrentState(self):
        if self.EditDialog: self.EditDialog.Destroy()
        self.EditDialog = PowerBinderEditDialog(self)
        self.RearrangeList.Clear()

        for item in self.CurrentState:
            for type, data in item.items():
                commandClass = commandClasses.get(type, None)
                if not commandClass:
                    commandClass = deprecatedCommandClasses.get(type, None)
                    if not commandClass:
                        wx.LogError(f"Profile contained unknown custom bind command class {type}; ignoring it and continuing.")
                        continue
                newCommand = commandClass(self.EditDialog, data)
                index = self.RearrangeList.Append(newCommand.MakeListEntryString())
                self.RearrangeList.SetClientData(index, newCommand)
                if newCommand.UI:
                    self.EditDialog.mainSizer.Insert(0, newCommand.UI, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
                    self.EditDialog.mainSizer.Hide(newCommand.UI)
        self.UpdateBindStringDisplay()

    def SaveToData(self):
        # initialize this from CurrentState in case we just tried to save the profile
        # without ever having Show()ed the dialog and therefore haven't ever populated it.
        self.LoadFromCurrentState()
        return self.GetCurrentState()

    def GetCurrentState(self):
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

    def OnAddStepButton(self, evt):
        button = evt.EventObject
        if not self.AddStepMenu:
            self.AddStepMenu = self.makeAddStepMenu()
        button.PopupMenu(self.AddStepMenu)

    def OnOKButton(self, _):
        if self.Button.tgtTxtCtrl:
            bindString = self.MakeBindString()
            self.BindStringDisplay.RemoveError('nomatch')
            if bindString != self.Button.tgtTxtCtrl.GetValue():
                self.Button.tgtTxtCtrl.SetValue(bindString)
                wx.App.Get().Main.Profile.SetModified()
        self.CurrentState = self.GetCurrentState()
        self.Close()

    def OnRearrangeDelete(self, _):
        current = self.RearrangeList.GetSelection()
        if current == wx.NOT_FOUND: return

        self.RearrangeList.Delete(current)
        self.UpdateBindStringDisplay()

    def OnRearrangeUp(self, _):
        self.RearrangeList.MoveCurrentUp()
        self.UpdateBindStringDisplay()

    def OnRearrangeDown(self, _):
        self.RearrangeList.MoveCurrentDown()
        self.UpdateBindStringDisplay()

    def OnRearrangeEdit(self, _):
        index = self.RearrangeList.GetSelection()

        # check whether we have an object already attached to this choice
        cmdObject = None
        try:
            cmdObject = self.RearrangeList.GetClientData(index)
        except Exception:
            pass

        if cmdObject:
            self.ShowEditDialogFor(cmdObject)
            self.RearrangeList.SetString(index, cmdObject.MakeListEntryString())
        else:
            print("cmdObject was None")
        self.UpdateBindStringDisplay()

    # OnAddStepMenu creates a new step and adds it to the rearrangelist
    def OnAddStepMenu(self, evt):
        menuitem = self.AddStepMenu.FindItemById(evt.GetId())
        chosenName = menuitem.GetItemLabel()

        # make a new command object, attached to the parent dialog
        newCommandClass = commandClasses[chosenName]
        newCommand = newCommandClass(self.EditDialog)

        # show the edit dialog if this command needs it
        if newCommand.UI and self.EditDialog:
            self.EditDialog.mainSizer.Insert(0, newCommand.UI, 1, wx.ALL|wx.EXPAND, 10)
            if (self.ShowEditDialogFor(newCommand) == wx.ID_CANCEL):
                self.EditDialog.mainSizer.Remove(newCommand.UI)
                return

        newBindIndex = self.RearrangeList.Append(newCommand.MakeListEntryString())
        self.RearrangeList.Select(newBindIndex)
        self.RearrangeList.SetClientData(newBindIndex, newCommand)

        self.OnListSelect()
        self.UpdateBindStringDisplay()

    def OnListSelect(self, _ = None):
        selected = self.RearrangeList.GetSelection()

        if selected != wx.NOT_FOUND:
            selCommand = self.RearrangeList.GetClientData(selected)
            if selCommand.UI:
                self.EditButton.Enable()
            else:
                self.EditButton.Disable()

    def UpdateBindStringDisplay(self):
        bindstring = self.MakeBindString()
        self.BindStringDisplay.SetValue(bindstring)

        # If they made any change, assume they're moving on with their lives and stop bugging about it not matching.
        self.BindStringDisplay.RemoveError('nomatch')

        if len(bindstring) > 255:
            self.BindStringDisplay.AddError('toolong', 'This bind string is longer than the maximum 255 characters and will likely not work as expected, if at all.')
        else:
            self.BindStringDisplay.RemoveError('toolong')
            self.BindStringDisplay.SetToolTip(bindstring)

    def MakeBindString(self):
        cmdBindStrings = []
        for index in range(self.RearrangeList.GetCount()):
            c = self.RearrangeList.GetClientData(index)
            if c: cmdBindStrings.append(c.MakeBindString())

        bindstring = ('$$'.join(cmdBindStrings))
        return bindstring

    # TODO - this is all reaching down into the innards of EditDialog and should probably
    # instead be a method on that class.
    def ShowEditDialogFor(self, command):
        if not command.UI or not self.EditDialog: return

        self.EditDialog.mainSizer.Show(command.UI)

        self.EditDialog.mainSizer.Fit(self.EditDialog)

        self.EditDialog.SetTitle(f'Editing Step "{commandRevClasses[type(command)]}"')
        returnval = self.EditDialog.ShowModal()

        self.EditDialog.mainSizer.Hide(command.UI)

        return returnval

    def makeAddStepMenu(self):

        stepMenu = wx.Menu()

        for subname in menuStructure:
            submenu = wx.Menu()
            stepMenu.AppendSubMenu(submenu, subname)
            for classname in menuStructure[subname]:
                submenu.Append(wx.ID_ANY, classname)

        stepMenu.Append(wx.ID_ANY, 'Custom Bind')

        return stepMenu

class PowerBinderButton(wx.BitmapButton):

    def __init__(self, parent, tgtTxtCtrl, init = {}):
        super().__init__(parent, -1, bitmap = GetIcon('UI', 'gear'))
        self.Init = init
        self.Dialog = None
        self.DialogParent = parent

        self.tgtTxtCtrl = tgtTxtCtrl
        self.Bind(wx.EVT_BUTTON, self.PowerBinderEventHandler)
        self.SetToolTip("Launch PowerBinder")

    def PowerBinderEventHandler(self, _):
        self.PowerBinderDialog().Show()

    def SaveToData(self):
        return self.PowerBinderDialog().SaveToData()

    def PowerBinderDialog(self):
        if not self.Dialog:
            self.Dialog = PowerBinderDialog(self.DialogParent, self, self.Init)
        return self.Dialog


class PowerBinderEditDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, -1, "Edit Step",
           style = wx.DEFAULT_DIALOG_STYLE)

        outerSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.SetMinSize(wx.Size(500, 150))

        self.Page = parent.Page

        self.mainSizer.Add(
            self.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL),
            0, wx.EXPAND|wx.ALL, 10)

        outerSizer.Add(self.mainSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 3)

        self.SetSizerAndFit(outerSizer)
        self.Layout()
        self.Fit()

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

