import os, sys
import importlib
from pathlib import Path

import wx

class BindWizard(wx.Dialog):
    def __init__(self, parent):

        wx.Dialog.__init__(self, parent, -1, 'Bind Wizard')

        self.LoadModules()

        bwSizer = wx.BoxSizer(wx.VERTICAL)


    # Load plugins / modules from UI/BindWizard directory
    def LoadModules(self):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        path = Path(base_path) / 'BindWizard'

        for package_file in sorted(path.glob('*.py')):
            package = package_file.stem
            if package == '__init__': continue

            modstr = "UI.BindWizard." + package
            # check if we've already loaded this one, if so, we've done this before, bail out
            if modstr in sys.modules: return

            # do the actual importing
            mod = importlib.import_module(modstr)

            if modclass := getattr(mod, package, None):

                # put the class into menuStructure, commandClasses, and commandRevClasses
                if modName := getattr(modclass, 'Name', ''):
                    wizardClasses[modName] = modclass
                else:
                    print(f"Class {modclass} didn't define 'Name' - this is a bug")

            else:
                print(f"Module {mod} didn't define a class of the same name - this is a bug!")


wizardClasses = {}
