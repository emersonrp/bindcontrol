import wx
import UI
import Utility

from UI.ControlGroup import ControlGroup
from Page import Page

class FPSDisplay(Page):

    def __init__(self, parent):
        Page.__init__(self, parent)
        self.TabTitle = "FPS / Netgraph"
        self.Init = {
            'FPSEnable': True,
            'FPSBindKey': "P",
        }

    def BuildPage(self):
        topSizer = wx.BoxSizer(wx.VERTICAL)

        controlsBox = ControlGroup(self, self, self.TabTitle)
        controlsBox.AddLabeledControl(
            ctlName = 'FPSEnable',
            ctlType = 'checkbox',
            callback = self.OnEnableCB,
        )
        controlsBox.AddLabeledControl(
            ctlName = 'FPSBindKey',
            ctlType = 'keybutton',
        )
        topSizer.Add(controlsBox)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizerAndFit(paddingSizer)

        return self


    def OnEnableCB(self, evt):
        self.Controls['FPSBindKey'].Enable(evt.EventObject.IsChecked())

    # TODO -- need two files to make this a toggle.
    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile
        ResetFile.SetBind(self.Profile.FPS['Bindkey'],'++showfps++netgraph')

    def findconflicts(self):
        Utility.CheckConflict(self.Profile.FPS,"Bindkey","FPS Display Toggle")

    def bindisused(self):
        return self.GetState('Enable')

    UI.Labels.update({
        'FPSEnable'  : "Enable the FPS/Netgraph bind",
        'FPSBindKey' : "Turn on FPS and Netgraph",
    })

