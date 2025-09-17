# parent class for various custom bindpane types
import wx
from UI.KeySelectDialog import bcKeyButton

class CustomBindPaneParent(wx.CollapsiblePane):
    def __init__(self, page, init = {}):
        super().__init__(page.scrolledPanel, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        self.Ctrls              = {}
        self.Page               = page
        self.Profile            = page.Profile
        self.Init        : dict = init
        self.Title       : str  = init.get('Title', '')
        self.Description : str  = ''
        self.Type        : str  = ''
        # RP:  don't do this as .get('CustomID', GetCustomID()).  Love, RP
        # RP:  further expln:  .get(X, Y) runs both of X and Y before evaluating
        # so we end up incrementing CustomID even if we don't use the new value
        self.CustomID    : int            = init.get('CustomID') or page.Profile.GetCustomID()
        self.DelButton   : wx.Button|None = None
        self.RenButton   : wx.Button|None = None
        self.DupButton   : wx.Button|None = None
        self.ExpButton   : wx.Button|None = None
        self.SetLabel(self.Title)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        # stash away the bind name inside the inner pane
        setattr(self.GetPane(), 'Title', self.Title)

        self.bindclass = type(self).__name__

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

        for evt in [
            wx.EVT_CHECKBOX, wx.EVT_BUTTON, wx.EVT_CHOICE, wx.EVT_COMBOBOX, wx.EVT_TEXT, wx.EVT_SPINCTRL,
            wx.EVT_DIRPICKER_CHANGED, wx.EVT_COLOURPICKER_CHANGED, wx.EVT_MENU, wx.EVT_RADIOBUTTON,
            wx.EVT_SLIDER,
        ]:

            self.Bind(evt, self.OnCommandEvent)

    def OnCommandEvent(self, evt):
        evt.Skip()
        self.Profile.UpdateData('CustomBinds', self.Serialize())

    def BuildBindUI(self, page):
        # build the UI needed to edit/create this bind, and shim
        # it into 'page'
        ...

    def PopulateBindFiles(self):
        print(f"Inside {self.bindclass} PopulateBindFiles")
        # for overriding on child classes this will be called in the course of
        # the Custom Binds page doing its own PopulateBindFiles, iteratively
        # over all of its kids

    def CreateSerialization(self, data):
        return {
                'CustomID' : self.CustomID,
                'Type'     : self.Type,
                'Title'    : self.Title,
                **data
                }

    def Serialize(self):
        print(f"Inside {self.bindclass} Serialize, please override")
        return {}

    def OnPaneChanged(self, evt):
        IsCollapsed = evt.GetCollapsed()
        if self.DelButton: self.DelButton.Show(not IsCollapsed)
        if self.RenButton: self.RenButton.Show(not IsCollapsed)
        if self.DupButton: self.DupButton.Show(not IsCollapsed)
        if self.ExpButton: self.ExpButton.Show(not IsCollapsed)
        self.Page.Layout()

    # this is called when we duplicate a bind.  We'll want to clear any keybuttons
    # to keep the new duplicate bind from conflicting
    def ClearKeyBinds(self):
        for _,ctrl in self.Ctrls.items():
            if isinstance(ctrl, bcKeyButton):
                ctrl.ClearButton(None)

    def MakeCtlName(self, name):
        return f"{self.bindclass}_{self.CustomID}_{name}"
