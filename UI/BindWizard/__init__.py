import wx
from Help import ShowHelpWindow

class WizardParent:
    WizardName  = ''
    WizToolTip  = ''
    WizHelpFile = ''
    IsUnique    = False

    def __init__(self, parent, init):
        self.BindPane = parent
        self.Profile = parent.Profile
        self.State = init
        self.WizardDialog = None

    def Dialog(self):
        if not self.WizardDialog:
            wd = wx.Dialog(self.BindPane)
            mainSizer = wx.BoxSizer(wx.VERTICAL)

            if bindName := self.BindPane.Title:
                bindName = f' "{bindName}"'

            wd.SetTitle(f"{self.WizardName}{bindName}")

            mainSizer.Add(self.BuildUI(wd, self.State), 1, wx.EXPAND)

            buttonflags = wx.OK|wx.CANCEL|wx.HELP if self.WizHelpFile else wx.OK|wx.CANCEL
            buttonsizer = wd.CreateStdDialogButtonSizer(buttonflags)
            if self.WizHelpFile:
                helpbutton = wd.FindWindow(wx.ID_HELP)
                helpbutton.Bind(wx.EVT_BUTTON, self.ShowHelp)
            okbutton = wd.FindWindow(wx.ID_OK)
            okbutton.Bind(wx.EVT_BUTTON, self.UpdateAndRefresh)

            mainSizer.Add(buttonsizer, 0, wx.EXPAND|wx.ALL, 10)

            wd.SetSizerAndFit(mainSizer)

            self.WizardDialog = wd
        return self.WizardDialog

    def ShowWizard(self, evt = None):
        self.Dialog().Show(True)
        if evt: evt.Skip()

    def PaneContents(self) -> wx.Panel:
        ...

    def ShowHelp(self, evt = None):
        if evt: evt.Skip()
        ShowHelpWindow(self.BindPane, self.WizHelpFile)

    def BuildUI(self, dialog, init) -> wx.Sizer:
        ...

    # TODO this really sorta belongs upstairs in WizardBindPane but needs refactoring
    # maybe into "Wizard.SetState" and "BindPane.Update" or something
    def UpdateAndRefresh(self, evt):
        if evt: evt.Skip()
        self.Profile.UpdateData('CustomBinds', self.BindPane.Serialize())
        self.BindPane.BuildBindUI(None)
