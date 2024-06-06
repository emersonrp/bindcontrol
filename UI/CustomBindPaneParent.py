# parent class for various custom bindpane types
import re
import wx
from UI.KeySelectDialog import bcKeyButton

class CustomBindPaneParent(wx.CollapsiblePane):
    def __init__(self, page, init = {}):
        wx.CollapsiblePane.__init__(self, page.scrolledPanel,
                style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        self.Ctrls   = {}
        self.Page    = page
        self.Profile = page.Profile
        self.Init    = init
        self.Title   = init.get('Title', '')
        self.SetLabel(self.Title)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        # stash away the bind name inside the inner pane
        self.GetPane().Title = self.Title

        self.bindclass      = type(self).__name__

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

    def BuildBindUI(self, page):
        # build the UI needed to edit/create this bind, and shim
        # it into 'page'
        pass

    def PopulateBindFiles(self):
        print(f"Inside {self.bindclass} PopulateBindFiles")
        # for overriding on child classes this will be called in the course of
        # the Custom Binds page doing its own PopulateBindFiles, iteratively
        # over all of its kids

    def Serialize(self):
        print(f"Inside {self.bindclass} Serialize, please override")
        return {}

    def OnPaneChanged(self, _):
        self.Page.Layout()

    # this is called when we duplicate a bind.  We'll want to clear any keybuttons
    # to keep the new duplicate bind from conflicting
    def ClearKeyBinds(self):
        for _,ctrl in self.Ctrls.items():
            if isinstance(ctrl, bcKeyButton):
                ctrl.ClearButton(None)

    def MakeCtlName(self, name):
        title = re.sub(r'\W+', '', self.Title)
        return f"{self.bindclass}_{title}_{name}"
