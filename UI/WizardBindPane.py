import wx
import importlib
import sys
from typing import Any
from functools import partial

from UI.CustomBindPaneParent import CustomBindPaneParent
from Util.Paths import GetRootDirPath

class WizardBindPane(CustomBindPaneParent):
    def __init__(self, page, wizClass, init : dict|None = None) -> None:
        init = init or {}
        super().__init__(page, init)

        if isinstance(wizClass, str):
            wizStr = wizClass
            wizClass = wizards.get(wizStr)

            if not wizClass:
                wizStr = init.get('WizClass')
                wizClass = wizards.get(wizStr)

                if not wizClass:
                    raise Exception(f'Unknown BindWizard class "{wizStr}" requested when building BindWizard.  This is a bug')

        self.WizClass    = wizClass
        self.Description = wizClass.WizardName
        self.Type        = "WizardBind"
        self.Wizard      = wizClass(self, init)

        if init:
            init = init.get('WizData', {})

        self.Init = init or {}

        self.Bind(wx.EVT_LEFT_DOWN, self.Wizard.ShowWizard)

    def Serialize(self) -> dict[str, Any]:
        data = self.CreateSerialization({
            'WizClass' : self.WizClass.WizardName,
            'WizData'  : self.Wizard.Serialize(),
        })
        return data

    def CheckIfWellFormed(self) -> bool:
        return self.Wizard.CheckIfWellFormed()

    def PopulateBindFiles(self) -> None:
        self.Wizard.PopulateBindFiles()

    # implement in Wizard class if needed
    def AllBindFiles(self) -> dict:
        if hasattr(self.Wizard, 'AllBindFiles'):
            return self.Wizard.AllBindFiles()
        return {}

    def BuildBindUI(self, page) -> None:
        # if the pane already has stuff, clear it out
        pane = self.GetPane()
        if mainSizer := pane.GetSizer():
            for item in range(mainSizer.GetItemCount()):
                mainSizer.Hide(item)
                mainSizer.Detach(item)
            pane.Layout()
        else:
            mainSizer = wx.BoxSizer(wx.VERTICAL)
            pane.SetSizer(mainSizer)

        # Get the juicy innards from the Wizard class and put them in the bindpane
        mainSizer.Add(self.Wizard.PaneContents(), 1, wx.EXPAND|wx.ALL, 10)

        pane.Layout()

    def UpdateAndRefresh(self, evt):
        if evt: evt.Skip()
        self.Wizard.UpdateStateFromDialog()
        self.Profile.UpdateData('CustomBinds', self.Serialize())
        self.BuildBindUI(None)

class WizButton(wx.Button):
    def __init__(self, parent, label, wizclass):
        super().__init__(parent, wx.ID_ANY, label = label)
        self.WizClass : Any = wizclass
        self.SetToolTip(self.WizClass.WizToolTip)

class WizPickerMenu(wx.Menu):
    def __init__(self, page):

        from Icon import GetIcon
        super().__init__()

        for wizClass in wizards.values():
            menuitem = wx.MenuItem(self, wx.ID_ANY, wizClass.WizardName)
            menuitem.SetBitmap(GetIcon(*wizClass.IconPath))
            self.Append(menuitem)
            self.Bind(wx.EVT_MENU, partial(page.OnBindWizardPicked, wizClass), menuitem)
            # Delete the menuitem if it's a unique item ("Escape Configurator" so far)
            # and we already have one in there.
            # This is a little hacky, innit?
            if wizClass.IsUnique:
                for pane in page.Panes:
                    if hasattr(pane, 'WizClass') and (pane.WizClass == wizClass):
                        menuitem.Enable(False)


# Load plugins / modules from UI/BindWizard directory
def LoadModules():
    path = GetRootDirPath() / 'UI' / 'BindWizard'

    for package_file in sorted(path.glob('*.py')):
        package = package_file.stem
        if package == '__init__': continue

        modstr = f"UI.BindWizard.{package}"
        # check if we've already loaded this one, if so, we've done this before, bail out
        if modstr in sys.modules: return

        # do the actual importing
        mod = importlib.import_module(modstr)

        if modclass := getattr(mod, package, None):

            if modName := getattr(modclass, 'WizardName', ''):
                wizards[modName] = modclass
            else:
                wx.LogError(f"Class {modclass} didn't define 'Name' - this is a bug")
        else:
            wx.LogError(f"Module {mod} didn't define a class of the same name - this is a bug!")

wizards = {}
LoadModules()
