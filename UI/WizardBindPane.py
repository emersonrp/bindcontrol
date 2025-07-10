from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.BindWizard import rev_wiz

import wx

class WizardBindPane(CustomBindPaneParent):
    def __init__(self, page, wizClass, init = {}):

        super().__init__(page, init)

        self.WizClass    = wizClass
        self.Description = wizClass.WizardName
        self.Wizard      = wizClass(self, init)

        if init:
            init = init.get('WizData', {})
        else:
            # show wizard
            result = self.Wizard.Show()
            if result == wx.ID_CANCEL:
                self.Abort = True
                return
            # else fill up init
            init = self.Wizard.GetData()

        self.Init = init

    def Serialize(self):
        data = {
            'Type'     : 'WizardBind',
            'Title'    : self.Title,
            'WizClass' : rev_wiz[self.WizClass],
            'WizData'  : self.Wizard.Serialize(),
        }
        return data

    def PopulateBindFiles(self):
        self.Wizard.PopulateBindFiles()

    def BuildBindUI(self, page):
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

    def ReshowWizard(self, evt):
        if self.Wizard.Show() == wx.ID_OK:
            self.BuildBindUI(None)
        evt.Skip()
