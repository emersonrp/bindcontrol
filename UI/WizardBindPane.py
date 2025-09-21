from typing import Dict, Any
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.BindWizard import rev_wiz

import wx

class WizardBindPane(CustomBindPaneParent):
    def __init__(self, page, wizClass, init = {}) -> None:

        super().__init__(page, init)

        self.WizClass    = wizClass
        self.Description = wizClass.WizardName
        self.Type        = "WizardBind"
        self.Wizard      = wizClass(self, init)

        if init:
            init = init.get('WizData', {})

        self.Init = init

    def Serialize(self) -> Dict[str, Any]:
        data = self.CreateSerialization({
            'WizClass' : rev_wiz[self.WizClass],
            'WizData'  : self.Wizard.Serialize(),
        })
        return data

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
