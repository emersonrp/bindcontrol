import wx
from Page import Page

class FPSDisplay(Page):

    def __init__(self, parent):
        Page.__init__(self, parent)
        self.TabTitle = "FPS / Netgraph"

    def InitKeys(self, profile):
        profile.PageState[self] = {
            'Enable': 1,
            'Bindkey': "P",
        }

    def FillTab(self):

        State = self.Profile.PageState[self]

        sizer = wx.BoxSizer(wx.VERTICAL)

        useCB = wx.CheckBox( self, -1, 'Enable FPS Binds')
        useCB.SetToolTip(wx.ToolTip('Check this to enable the FPS and Netgraph Toggle Binds'))
        sizer.Add(useCB, 0, wx.ALL, 10)

        minisizer = wx.FlexGridSizer(0,2,5,5)
        minisizer.Add( wx.StaticText(self, -1, 'Toggle FPS/Netgraph'), 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        minisizer.Add( wx.Button(self, -1, State['Bindkey']))

        sizer.Add(minisizer)

        self.SetSizerAndFit(sizer)

        return self

    def PopulateBindFiles(self):
        ResetFile = self.Profile.General['ResetFile']
        ResetFile.SetBind(self.Profile.FPS['Bindkey'],'++showfps++netgraph')

    def findconflicts(self):
        cbCheckConflict(self.Profile.FPS,"Bindkey","FPS Display Toggle")

    def bindisused(self):
        return self.Profile.PageState[self]['Enable']

