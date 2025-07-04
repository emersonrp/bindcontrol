import wx
from UI.BindWizard import WizardParent
from UI.IncarnateBox import IncarnateBox

class IncarnateConfig(WizardParent):
    WizardName  = 'Incarnate Powers Set'
    WizToolTip  = 'Create a keybind that, with multiple presses, will load a particular set of Incarnate Powers'

    def __init__(self, init):
        super().__init__(init)

    def BuildUI(self, init = {}):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(wx.Size(700,-1))

        if setName := init.get('Title', ''):
            setName = f' "{setName}"'

        self.SetTitle(f"Incarnate Set{setName}")

        incarnateBox = IncarnateBox(self, wx.App.Get().Main.Profile.Server)
        mainSizer.Add(incarnateBox, 1, wx.EXPAND|wx.ALL, 10)

        return mainSizer
