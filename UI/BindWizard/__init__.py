import os, sys
import importlib
from pathlib import Path
from UI.CustomBindPaneParent import CustomBindPaneParent

import wx

wizards = {}

class WizardBindPane(CustomBindPaneParent):
    def __init__(self, page, wizClass, init = {}):

        super().__init__(page, init)

        self.WizClass    = wizClass
        self.Description = wizClass.WizardName

        if not init:
            # show wizard
            with wizClass(self) as wizard:
                result = wizard.ShowModal()
                if result == wx.ID_CANCEL:
                    self.Abort = True
                    return

                # "else"
                # set things up, init?  innards?
                #
                self.Bind(wx.EVT_LEFT_DOWN, self.OnClickPane)

    def OnClickPane(self, evt):
        init = self.Serialize()
        with self.WizClass(self, init) as wizard:
            ...
            wizard.ShowModal()

        evt.Skip()


class BindWizardDialog(wx.Dialog):
    def __init__(self, parent):

        super().__init__(parent, -1, 'Bind Wizard')

        self.LoadModules()
        self.WizClass = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        wcSizer = wx.BoxSizer(wx.VERTICAL)
        wcSizer.Add(wx.StaticText(self, wx.ID_ANY, 'Select a Bind Wizard to run:'), 0, wx.EXPAND|wx.BOTTOM, 20)
        for classname, wizClass in wizards.items():
            wizbutton = wx.Button(self, wx.ID_ANY, label = classname)
            wizbutton.SetToolTip(wizClass.WizToolTip)
            wcSizer.Add(wizbutton, 1, wx.EXPAND)
            setattr(wizbutton, 'WizClass', wizClass)
            wizbutton.Bind(wx.EVT_BUTTON, self.OnWizButton)

        mainSizer.Add(wcSizer, 1, wx.EXPAND|wx.ALL, 20)

        self.SetSizer(mainSizer)

    # Load plugins / modules from UI/BindWizard directory
    def LoadModules(self):
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
                else:
                    print(f"Class {modclass} didn't define 'Name' - this is a bug")
            else:
                print(f"Module {mod} didn't define a class of the same name - this is a bug!")

    def OnWizButton(self, evt):
        if evt: evt.Skip()
        self.WizClass = evt.GetEventObject().WizClass
        self.Hide()

class WizardParent(wx.Dialog):
    WizardName  = ''
    WizToolTip  = ''

    def __init__(self, parent, init = {}):
        super().__init__(parent)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        wizsizer = self.BuildUI(init)

        mainSizer.Add(wizsizer, 1, wx.EXPAND)
        mainSizer.Add(self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL), 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizerAndFit(mainSizer)

    def BuildUI(self, init) -> wx.Sizer:
        ...
