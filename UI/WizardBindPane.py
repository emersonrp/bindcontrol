from UI.CustomBindPaneParent import CustomBindPaneParent

import wx

class WizardBindPane(CustomBindPaneParent):
    def __init__(self, page, wizClass, init = {}):

        super().__init__(page, init)

        self.WizClass    = wizClass
        self.Description = wizClass.WizardName
        self.Wizard      = wizClass(self, init)

        if not init:
            # show wizard
            result = self.Wizard.ShowModal()
            if result == wx.ID_CANCEL:
                self.Abort = True
                return
            # else fill up init
            init = self.Wizard.GetData()

        self.Init = init
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClickPane)

    def OnClickPane(self, evt):
        self.Wizard.ShowModal(self.Init)
        evt.Skip()

    def BuildBindUI(self, page):
        pane = self.GetPane()
        setattr(pane, 'Page', page)

        # Get the juicy innards from the Wizard class and put them in the bindpane
        PaneContents = self.Wizard.PaneContents(self)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(PaneContents, 1, wx.EXPAND|wx.ALL, 10)

        pane.SetSizer(mainSizer)
        pane.Layout()
