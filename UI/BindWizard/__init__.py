import wx
from Help import ShowHelpWindow

# the thinking behind making this not a wx object itself is so that
# we don't have to build a whole dialog etc to keep state for every
# one of these we load up from a Profile at load time.  We keep State
# here, and lazy-create the dialog.
#
# This makes for some confusing bits going through the code.  This
# needs a little love still but that's why it's done this way.
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

    # this might want to be called ShowWizardDialog hmm.
    def ShowWizard(self, evt = None):
        self.Dialog().Show(True)
        self.Dialog().Raise()
        if evt: evt.Skip()

    # called whenever the dialog is shown from a not-shown state
    def FillDialogFromState(self):
        ...

    # the juicy innards of the dialog
    def PaneContents(self) -> wx.Panel:
        ...

    def ShowHelp(self, evt = None):
        if evt: evt.Skip()
        ShowHelpWindow(self.BindPane, self.WizHelpFile)

    def BuildUI(self, dialog, init) -> wx.Sizer:
        ...

    def UpdateStateFromDialog(self):
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

        mainSizer.Add(wizard.BuildUI(self, wizard.State), 1, wx.EXPAND)

        buttonflags = wx.OK|wx.CANCEL|wx.HELP if wizard.WizHelpFile else wx.OK|wx.CANCEL
        buttonsizer = self.CreateStdDialogButtonSizer(buttonflags)
        if wizard.WizHelpFile:
            helpbutton = self.FindWindow(wx.ID_HELP)
            helpbutton.Bind(wx.EVT_BUTTON, wizard.ShowHelp)
        okbutton = self.FindWindow(wx.ID_OK)
        okbutton.Bind(wx.EVT_BUTTON, self.Wizard.onOKClicked)

        cancelbutton = self.FindWindow(wx.ID_CANCEL)
        cancelbutton.Bind(wx.EVT_BUTTON, self.Wizard.onCancelClicked)

        mainSizer.Add(buttonsizer, 0, wx.EXPAND|wx.ALL, 10)

        self.SetSizerAndFit(mainSizer)
        self.Layout()

    def Show(self, show = True):
        if not self.IsShown():
            self.Wizard.FillDialogFromState()
        return super().Show(show)
