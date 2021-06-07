import wx
import Utility
from Page import Page

class FPSDisplay(Page):

    def __init__(self, parent):
        Page.__init__(self, parent)
        self.TabTitle = "FPS / Netgraph"
        self.State = {
            'Enable': True,
            'Bindkey': "P",
        }

    def FillTab(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        useCB = wx.CheckBox( self, -1, 'Enable FPS Binds')
        useCB.SetToolTip(wx.ToolTip('Check this to enable the FPS and Netgraph Toggle Binds'))
        sizer.Add(useCB, 0, wx.ALL, 10)

        minisizer = wx.FlexGridSizer(0,2,5,5)
        minisizer.Add( wx.StaticText(self, -1, 'Toggle FPS/Netgraph'),
                0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        minisizer.Add( wx.Button(self, -1, self.State['Bindkey']))

        sizer.Add(minisizer)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(sizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizerAndFit(paddingSizer)

        return self

    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile
        ResetFile.SetBind(self.Profile.FPS['Bindkey'],'++showfps++netgraph')

    def findconflicts(self):
        Utility.CheckConflict(self.Profile.FPS,"Bindkey","FPS Display Toggle")

    def bindisused(self):
        return self.State['Enable']

