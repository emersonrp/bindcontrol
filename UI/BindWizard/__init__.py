import wx
from Help import ShowHelpWindow

class WizardParent:
    WizardName  = ''
    WizToolTip  = ''
    WizHelpFile = ''
    IconPath    = ('Empty',) # trailing , is important
    IsUnique    = False

    def __init__(self, parent, init):
        self.BindPane = parent
        self.Profile = parent.Profile
        self.State = init
        self.WizardDialog = None
        wx.CallAfter(self.Dialog)

    def Dialog(self):
        if not self.WizardDialog:
            self.WizardDialog = WizardDialog(self.BindPane, self)

        self.WizardDialog.Fit()
        self.WizardDialog.SetInitialSize(self.WizardDialog.GetSize())
        self.WizardDialog.Center()
        return self.WizardDialog

    def onOKClicked(self, evt):
        self.BindPane.UpdateAndRefresh(evt)
        if evt: evt.Skip()

    # for overriding in wizards
    def onCancelClicked(self, evt):
        if evt: evt.Skip()

    def ShowWizard(self, evt = None):
        self.Dialog().Show(True)
        self.Dialog().Raise()
        if evt: evt.Skip()

    def PaneContents(self) -> wx.Panel:
        ...

    def ShowHelp(self, evt = None):
        if evt: evt.Skip()
        ShowHelpWindow(self.BindPane, self.WizHelpFile)

    def BuildUI(self, dialog, init) -> wx.Sizer:
        ...

    def UpdateState(self):
        ...

class WizardDialog(wx.Dialog):
    def __init__(self, parent, wizard):
        super().__init__(parent)

        self.BindPane = parent
        self.Wizard   = wizard

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        if bindName := self.BindPane.Title:
            bindName = f' "{bindName}"'

        self.SetTitle(f"{wizard.WizardName}{bindName}")

        mainSizer.Add(wizard.BuildUI(self, self.State), 1, wx.EXPAND)

        buttonflags = wx.OK|wx.CANCEL|wx.HELP if wizard.WizHelpFile else wx.OK|wx.CANCEL
        buttonsizer = self.CreateStdDialogButtonSizer(buttonflags)
        if wizard.WizHelpFile:
            helpbutton = self.FindWindow(wx.ID_HELP)
            helpbutton.Bind(wx.EVT_BUTTON, self.ShowHelp)
        okbutton = self.FindWindow(wx.ID_OK)
        okbutton.Bind(wx.EVT_BUTTON, self.Wizard.onOKClicked)

        cancelbutton = self.FindWindow(wx.ID_CANCEL)
        cancelbutton.Bind(wx.EVT_BUTTON, self.Wizard.onCancelClicked)

        mainSizer.Add(buttonsizer, 0, wx.EXPAND|wx.ALL, 10)

        self.Bind(wx.EVT_SIZE, self.OnSizeDebug)

        self.SetSizerAndFit(mainSizer)
        self.Layout()

    def OnSizeDebug(self, evt):
        print("GOT A SIZE")
        print(evt.GetSize())
