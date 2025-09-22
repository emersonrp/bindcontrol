import sys
import importlib
import wx
from Util.Paths import GetRootDirPath

class WizardParent(object):
    def __init__(self, parent, init):
        self.BindPane = parent
        self.Profile = parent.Profile
        self.Init = init
        self.WizardDialog = None

    def Dialog(self):
        if not self.WizardDialog:
            wd = wx.Dialog(self.BindPane)
            mainSizer = wx.BoxSizer(wx.VERTICAL)

            mainSizer.Add(self.BuildUI(wd, self.Init), 1, wx.EXPAND)

            buttonsizer = wd.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL|wx.HELP)
            helpbutton = wd.FindWindow(wx.ID_HELP)
            helpbutton.Bind(wx.EVT_BUTTON, self.ShowHelp)
            okbutton = wd.FindWindow(wx.ID_OK)
            okbutton.Bind(wx.EVT_BUTTON, self.UpdateAndRefresh)

            mainSizer.Add(buttonsizer, 0, wx.EXPAND|wx.ALL, 10)

            wd.SetSizerAndFit(mainSizer)

            self.WizardDialog = wd
        return self.WizardDialog

    def ShowWizard(self, evt = None):
        self.Dialog().Show(True)
        if evt: evt.Skip()

    def PaneContents(self) -> wx.Panel:
        ...

    def ShowHelp(self, evt = None):
        ...

    def BuildUI(self, dialog, init) -> wx.Sizer:
        ...

    def UpdateAndRefresh(self, evt):
        evt.Skip()
        self.Profile.UpdateData('CustomBinds', self.BindPane.Serialize())
        self.BindPane.BuildBindUI(None)

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

