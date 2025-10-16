import wx
import importlib
import sys
from typing import Any

from UI.CustomBindPaneParent import CustomBindPaneParent
from Util.Paths import GetRootDirPath


class WizardBindPane(CustomBindPaneParent):
    def __init__(self, page, wizClass, init : dict|None = None) -> None:
        init = init or {}
        super().__init__(page, init)

        self.WizClass    = wizClass
        self.Description = wizClass.WizardName
        self.Type        = "WizardBind"
        self.Wizard      = wizClass(self, init)

        if init:
            init = init.get('WizData', {})

        self.Init = init or {}

    def Serialize(self) -> dict[str, Any]:
        data = self.CreateSerialization({
            'WizClass' : rev_wiz[self.WizClass],
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

class WizPickerDialog(wx.Dialog):
    def __init__(self, parent):

        super().__init__(parent, -1, 'Bind Wizard')

        self.WizClass = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        wcSizer = wx.BoxSizer(wx.VERTICAL)
        wcSizer.Add(wx.StaticText(self, wx.ID_ANY, 'Select a Bind Wizard:'), 0, wx.EXPAND|wx.BOTTOM, 20)
        for classname, wizClass in wizards.items():
            wizbutton = wx.Button(self, wx.ID_ANY, label = classname)
            wizbutton.SetToolTip(wizClass.WizToolTip)
            wcSizer.Add(wizbutton, 1, wx.EXPAND)
            setattr(wizbutton, 'WizClass', wizClass)
            wizbutton.Bind(wx.EVT_BUTTON, self.OnWizPicked)

            # Turn off the button if we just can have one, like "Escape Configurator"
            # This is a little hacky, innit?
            if wizClass.IsUnique:
                for pane in parent.Panes:
                    if hasattr(pane, 'WizClass') and (pane.WizClass == wizClass):
                        wizbutton.Enable(False)
                        wizbutton.SetToolTip(f'You can only have one instance of "{classname}" per-Profile')

        mainSizer.Add(wcSizer, 1, wx.EXPAND|wx.ALL, 20)

        self.SetSizer(mainSizer)

    def OnWizPicked(self, evt):
        if evt: evt.Skip()
        self.WizClass = evt.GetEventObject().WizClass
        self.Hide()

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
                rev_wiz[modclass] = modName
            else:
                wx.LogError(f"Class {modclass} didn't define 'Name' - this is a bug")
        else:
            wx.LogError(f"Module {mod} didn't define a class of the same name - this is a bug!")

wizards = {}
rev_wiz = {}
LoadModules()
