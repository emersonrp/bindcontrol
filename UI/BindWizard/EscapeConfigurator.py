import wx
import UI
from Help import ShowHelpWindow
from UI.BindWizard import WizardParent
from UI.ControlGroup import ControlGroup

UI.Labels.update({
    'EscUnselect'    : 'Unselect',
    'EscUnqueue'     : 'Unqueue',
    'EscWindows'     : 'Close All Windows',
    'EscExitMission' : 'Exit Completed Mission',
    'EscResetCam'    : 'Reset Camera',
    'EscNoReward'    : 'Choose No Reward',
    'EscDialogNo'    : 'Answer No to Dialog',
    'EscMenu'        : 'Show Main Menu',
})

class EscapeConfigurator(WizardParent):
    WizardName  = 'Escape Configurator'
    WizToolTip  = 'Bind various interesting functions to your Escape key'

    def BuildUI(self, dialog, init : dict|None = None):
        wizdata = {}
        if init: wizdata = init.get('WizData', {})

        Expln = wx.Panel(dialog)
        ESizr = wx.BoxSizer(wx.HORIZONTAL)
        Expln.SetSizer(ESizr)
        ESizr.Add(wx.StaticText(Expln, label = 'Select the functions that will be bound to the Escape key.\nClick the "Help" button for more information.'), 1, wx.ALL, 6)

        mainSizer = ControlGroup(dialog, self.Profile.CustomBinds, topcontent = Expln)

        self.EscUnselect = mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscUnselect',
            tooltip = 'Unselect any selected units or items',
        )
        self.EscUnselect.SetValue(bool(wizdata.get('EscUnselect'))) # pyright: ignore
        self.EscUnqueue = mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscUnqueue',
            tooltip = 'Unqueue any power that is about to fire',
        )
        self.EscUnqueue.SetValue(bool(wizdata.get('EscUnqueue'))) # pyright: ignore
        self.EscWindows = mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscWindows',
            tooltip = 'Close all non-essential windows, clearing the screen',
        )
        self.EscWindows.SetValue(bool(wizdata.get('EscWindows'))) # pyright: ignore
        self.EscExitMission = mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscExitMission',
            tooltip = 'Exit a completed mission',
        )
        self.EscExitMission.SetValue(bool(wizdata.get('EscExitMission'))) # pyright: ignore
        self.EscResetCam = mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscResetCam',
            tooltip = 'Reset the camera to behind the player',
        )
        self.EscResetCam.SetValue(bool(wizdata.get('EscResetCam'))) # pyright: ignore
        self.EscNoReward = mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscNoReward',
            tooltip = 'Select "No Reward" from a reward choice list',
        )
        self.EscNoReward.SetValue(bool(wizdata.get('EscNoReward'))) # pyright: ignore
        self.EscDialogNo = mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscDialogNo',
            tooltip = 'Answer "OK" or "No" or "Cancel" to a dialog',
        )
        self.EscDialogNo.SetValue(bool(wizdata.get('EscDialogNo'))) # pyright: ignore
        self.EscMenu = mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscMenu',
            tooltip = 'Open the Main Menu',
        )
        self.EscMenu.SetValue(bool(wizdata.get('EscMenu'))) # pyright: ignore
        return mainSizer

    def Serialize(self):
        return {
            'EscUnselect'    : self.EscUnselect   .GetValue(), # pyright: ignore
            'EscUnqueue'     : self.EscUnqueue    .GetValue(), # pyright: ignore
            'EscWindows'     : self.EscWindows    .GetValue(), # pyright: ignore
            'EscExitMission' : self.EscExitMission.GetValue(), # pyright: ignore
            'EscResetCam'    : self.EscResetCam   .GetValue(), # pyright: ignore
            'EscNoReward'    : self.EscNoReward   .GetValue(), # pyright: ignore
            'EscDialogNo'    : self.EscDialogNo   .GetValue(), # pyright: ignore
            'EscMenu'        : self.EscMenu       .GetValue(), # pyright: ignore
        }

    def PaneContents(self):
        bindpane = self.BindPane
        panel = wx.Panel(bindpane.GetPane())
        panel.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)

        panel.SetSizer(panelSizer)

        return panel

    def CheckIfWellFormed(self):
        return True

    def PopulateBindFiles(self):
        commands = []
        if self.EscUnselect.GetValue(): commands.append('unselect') # pyright: ignore
        if self.EscUnqueue.GetValue(): commands.append('unqueue') # pyright: ignore
        if self.EscWindows.GetValue(): commands.append('gamereturn') # pyright: ignore
        if self.EscExitMission.GetValue(): commands.append('requestexitmission 1') # pyright: ignore
        if self.EscResetCam.GetValue(): commands.append('camreset') # pyright: ignore
        if self.EscNoReward.GetValue(): commands.append('clearRewardChoice') # pyright: ignore
        if self.EscDialogNo.GetValue(): commands.append('dialogno') # pyright: ignore
        if self.EscMenu.GetValue(): commands.append('menu') # pyright: ignore


    def AllBindFiles(self):
        return {
            'files' : [],
            'dirs'  : [],
        }

    def ShowHelp(self, evt = None):
        if evt: evt.Skip()
        ShowHelpWindow(self.BindPane, 'EscapeConfigurator.html')
