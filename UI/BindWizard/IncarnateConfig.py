import wx
from UI.BindWizard import WizardParent
from UI.IncarnateBox import IncarnateBox

class IncarnateConfig(WizardParent):
    WizardName = 'Incarnate Powers Set'
    WizToolTip = 'Create a keybind that, with multiple presses, will load a particular set of Incarnate Powers'

    def BuildUI(self, init = {}):
        print("Hi building ui")
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(wx.Size(700,-1))

        incarnateBox = IncarnateBox(self, wx.App.Get().Main.Profile.Server)
        mainSizer.Add(incarnateBox, 1, wx.EXPAND|wx.ALL, 10)

        return mainSizer
