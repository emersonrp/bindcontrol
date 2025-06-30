import os, sys
import importlib
from pathlib import Path

import wx

wizards = {}

class BindWizard(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, -1, 'Bind Wizard')

        self.LoadModules()

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        wcSizer = wx.BoxSizer(wx.VERTICAL)
        for wizClass in wizards.keys():
            wizbutton = wx.Button(self, wx.ID_ANY, label = wizClass)
            wizbutton.SetToolTip(wizards[wizClass].WizToolTip)
            wcSizer.Add(wizbutton, 1, wx.EXPAND)
            wizbutton.Bind(wx.EVT_BUTTON, wizards[wizClass].ShowWizard)

        mainSizer.Add(wcSizer, 1, wx.EXPAND|wx.ALL, 10)

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


class WizardParent():
    WizardName = ''
    WizToolTip = ''
    WizDialog  = None

    def __init__(self):
        ...

    def ShowWizard(self, init = {}):
        ...
