# parent class for various custom bindpane types
import wx

class CustomBindPaneParent(wx.CollapsiblePane):
    def __init__(self, page, init = {}):
        wx.CollapsiblePane.__init__(self, page.scrolledPane,
                style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        self.Ctrls = {}
        self.Page  = page
        self.Init  = init
        self.Title = ''

        self.bindclass      = type(self).__name__

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

    def BuildBindUI(self, _):
        # build the UI needed to edit/create this bind, and shim
        # it into 'parent'
        pass

    def PopulateBindFiles(self):
        print(f"Inside {self.bindclass} PopulateBindFiles")
        # for overriding on child classes this will be called in the course of
        # the Custom Binds page doing its own PopulateBindFiles, iteratively
        # over all of its kids

    def Serialize(self):
        print(f"Inside {self.bindclass} Serialize, please override")

    def OnPaneChanged(self, _):
        self.Page.Layout()
