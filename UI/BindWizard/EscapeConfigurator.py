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
    'EscSheathe'     : 'Sheathe Weapons',
})

class EscapeConfigurator(WizardParent):
    WizardName  = 'Escape Configurator'
    WizToolTip  = 'Bind various interesting functions to your Escape key'

    def BuildUI(self, dialog, init : dict|None = None):
        init = init or {}

        mainSizer = ControlGroup(dialog, self.Profile.CustomBinds)

        mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscUnselect',
            tooltip = 'Unselect any selected units or items',
        )
        mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscUnqueue',
            tooltip = 'Unqueue any power that is about to fire',
        )
        mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscWindows',
            tooltip = 'Close all non-essential windows, clearing the screen',
        )
        mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscExitMission',
            tooltip = 'Exit a completed mission',
        )
        mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscResetCam',
            tooltip = 'Reset the camera to behind the player',
        )
        mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscNoReward',
            tooltip = 'Select "No Reward" from a reward choice list',
        )
        mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscDialogNo',
            tooltip = 'Answer "OK" or "No" or "Cancel" to a dialog',
        )
        mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscMenu',
            tooltip = 'Open the Main Menu',
        )
        mainSizer.AddControl(
            ctlType = 'checkbox',
            ctlName = 'EscSheathe',
            tooltip = 'Sheathe any drawn weapons',
        )

        return mainSizer

    def Serialize(self):
        return {
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
        ...

    def AllBindFiles(self):
        return {
            'files' : [],
            'dirs'  : [],
        }

    def ShowHelp(self, evt = None):
        if evt: evt.Skip()
        ShowHelpWindow(self.BindPane, 'EscapeConfigurator.html')
