import os, sys
import importlib
from pathlib import Path
import wx

class WizardParent(wx.Dialog):
    WizardName  = ''
    WizToolTip  = ''

    def __init__(self, parent, init = {}):
        super().__init__(parent)

        self.BindPane = parent

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        mainSizer.Add(self.BuildUI(init), 1, wx.EXPAND)

        buttonsizer = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL|wx.HELP)
        helpbutton = self.FindWindow(wx.ID_HELP)
        helpbutton.Bind(wx.EVT_BUTTON, self.ShowHelp)
        okbutton = self.FindWindow(wx.ID_OK)
        okbutton.Bind(wx.EVT_BUTTON, self.RefreshUI)

        mainSizer.Add(buttonsizer, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizerAndFit(mainSizer)

    def BuildUI(self, init) -> wx.Sizer:
        ...

    def PaneContents(self) -> wx.Panel:
        ...

    def GetData(self) -> dict:
        ...

    def ShowHelp(self, evt = None):
        ...

    def RefreshUI(self, evt):
        evt.Skip()
        self.BindPane.BuildBindUI(None)

    def ShowWizard(self, evt = None):
        self.Show(True)
        if evt: evt.Skip()

class WizPickerDialog(wx.Dialog):
    def __init__(self, parent):

        super().__init__(parent, -1, 'Bind Wizard')

        self.WizClass = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        wcSizer = wx.BoxSizer(wx.VERTICAL)
        wcSizer.Add(wx.StaticText(self, wx.ID_ANY, 'Select a Bind Wizard to run:'), 0, wx.EXPAND|wx.BOTTOM, 20)
        for classname, wizClass in wizards.items():
            wizbutton = wx.Button(self, wx.ID_ANY, label = classname)
            wizbutton.SetToolTip(wizClass.WizToolTip)
            wcSizer.Add(wizbutton, 1, wx.EXPAND)
            setattr(wizbutton, 'WizClass', wizClass)
            wizbutton.Bind(wx.EVT_BUTTON, self.OnWizPicked)

        mainSizer.Add(wcSizer, 1, wx.EXPAND|wx.ALL, 20)

        self.SetSizer(mainSizer)

    def OnWizPicked(self, evt):
        if evt: evt.Skip()
        self.WizClass = evt.GetEventObject().WizClass
        self.Hide()

# Load plugins / modules from UI/BindWizard directory
def LoadModules():
    path = Path(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))

    for package_file in sorted(path.glob('*.py')):
        package = package_file.stem
        if package == '__init__': continue

        modstr = "UI.BindWizard." + package
        # check if we've already loaded this one, if so, we've done this before, bail out
        if modstr in sys.modules: return

        # do the actual importing
        mod = importlib.import_module(modstr)

        if modclass := getattr(mod, package, None):

            if modName := getattr(modclass, 'WizardName', ''):
                wizards[modName] = modclass
                rev_wiz[modclass] = modName
            else:
                print(f"Class {modclass} didn't define 'Name' - this is a bug")
        else:
            print(f"Module {mod} didn't define a class of the same name - this is a bug!")

wizards = {}
rev_wiz = {}
LoadModules()

