# UI / logic for the 'general' panel
import wx
import UI

from GameData import Archetypes, Origins, MiscPowers
from UI.ControlGroup import ControlGroup
from Page import Page

class General(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        profile = parent
        # TODO - make bindsdir os-agnostic
        # TODO - find CoH install and put them there?
        # TODO - help text about WINEPREFIX etc for Mac/Linux users
        self.Init = {
            'Name': 'Profile',
            'Archetype': 'Scrapper',
            'Origin': "Magic",
            'Primary': 'Martial Arts',
            'Secondary': 'Super Reflexes',
            'Epic': 'Weapon Mastery',
            'BindsDir': "/home/emerson",
            'ResetKey': 'CTRL+M',
            'ResetFeedback': 1,
            'Pool1': '',
            'Pool2': '',
            'Pool3': '',
            'Pool4': '',
            'UseSplitModKeys': False,
        }

    def BuildPage(self):

        topSizer = wx.BoxSizer(wx.VERTICAL)

        powersBox = ControlGroup(self, self, 'Powers and Info')
        powersBox.AddLabeledControl(
            ctlName = 'Name',
            ctlType = 'text',
        )
        powersBox.AddLabeledControl(
            ctlName = 'Archetype',
            ctlType = 'combo',
            contents = sorted(Archetypes),
            tooltip = '',
            callback = self.pickArchetype,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Origin',
            ctlType = 'combo',
            contents = Origins,
            tooltip = '',
            callback = self.pickOrigin,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Primary',
            ctlType = 'combo',
            # contents = sorted(ArchData['Primary']),
            tooltip = '',
            callback = self.pickPrimaryPowerSet,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Secondary',
            ctlType = 'combo',
            # contents = sorted(ArchData['Secondary']),
            tooltip = '',
            callback = self.pickSecondaryPowerSet,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Epic',
            ctlType = 'combo',
            # contents = sorted(ArchData['Epic']),
            tooltip = '',
            callback = self.pickEpicPowerSet,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Pool1',
            ctlType = 'combo',
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Pool2',
            ctlType = 'combo',
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Pool3',
            ctlType = 'combo',
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Pool4',
            ctlType = 'combo',
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            ctlName = 'BindsDir',
            ctlType = 'dirpicker',
        )
        powersBox.AddLabeledControl(
            ctlName = 'ResetKey',
            ctlType = 'keybutton',
            tooltip = 'This key is used by certain modules to reset binds to a sane state.',
        )

        powersBox.AddLabeledControl(
            ctlName = 'ResetFeedback',
            ctlType = 'checkbox',
        )

        topSizer.Add(powersBox)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag=wx.ALL|wx.EXPAND, border = 20)

        self.SetSizer(paddingSizer)
        return self

    def pickArchetype(self, event):
        # TODO fill in Primary / Secondary powers pickers
        pass

    def pickOrigin(self, event):
        # TODO do we need to take any action based on this?
        pass

    def pickPoolPower(self, event):
        pass

    def pickPrimaryPowerSet(self, event):
        pass

    def pickSecondaryPowerSet(self, event):
        pass

    def pickEpicPowerSet(self, event):
        pass


    UI.Labels.update({
        'BindsDir'        : 'Base Binds Directory',
        'ResetFile'       : 'Reset All Binds file',
        'ResetKey'        : 'Reset All Binds',
        'ResetFeedback'   : 'Enable Reset Feedback Self-/tell',
        'UseSplitModKeys' : 'Bind left and right modifier keys separately',
    })

