import wx

from wx.richtext import RichTextCtrl as RTC
from Page import Page
from Bind.SimpleBind import SimpleBind
from UI.ControlGroup import ControlGroup

class SimpleBinds(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Binds = ()
        self.TabTitle = "Simple Binds"

    def BuildPage(self):
        profile = self.Profile

        self.MainSizer = wx.BoxSizer(wx.VERTICAL) # overall sizer
        self.PaneSizer = wx.BoxSizer(wx.VERTICAL) # sizer for collapsable panes
        buttonSizer    = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item button

        # Stick a button in the bottom sizer
        newBindButton = wx.Button(self, -1, "New Simple Item")
        newBindButton.Bind(wx.EVT_BUTTON, self.AddBindToPage)
        buttonSizer.Add(newBindButton, wx.ALIGN_CENTER)

        # Put blank space into PaneSizer so it expands
        self.PaneSizer.AddStretchSpacer()

        # add the two sub-sizers, top one expandable
        self.MainSizer.Add( self.PaneSizer, 1, wx.EXPAND|wx.ALL)
        self.MainSizer.Add( buttonSizer, 0, wx.EXPAND|wx.ALL)

        # sizer around the whole thing to add padding
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(self.MainSizer, 1, flag = wx.ALL|wx.EXPAND, border = 16)

        # Add any binds that came from a savefile
        for bind in self.Binds:
            bindCP = self.AddBindToPage(bind)

        self.SetSizerAndFit(paddingSizer)
        self.Layout()

    def AddBindToPage(self, _, bindinit = {}):

        bind = SimpleBind(self, bindinit)

        # TODO - if bind is already in there, just scroll to it and pop it open
        bindCP = wx.CollapsiblePane(self, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, bindCP)

        bind.BuildBindUI(bindCP, self)

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount() - 1, bindCP, 0, wx.ALL|wx.EXPAND, 10)
        self.Layout()

    def OnPaneChanged(self, event):
        self.Layout()

    def PopulateBindFiles(self):
        profile   = self.Profile
        ResetFile = profile.ResetFile()

        for b in self.State['binds'].items():
            ResetFile.SetBind(b['key'], Utility.cpBindToString(b['contents']))

    def findconflicts(self):
        for b in self.State['binds'].items():
            Utility.CheckConflict(
                b['key'], "Key", "Simple Bind " + (b['title'] or "Unknown")
            )

    def bindisused(self, profile):
        return bool(len(self.State('binds')))

