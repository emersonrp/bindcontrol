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
        self.State = {
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

        UI.Labels.update({
            'BindsDir'        : 'Base Binds Directory',
            'ResetFile'       : 'Reset All Binds file',
            'ResetKey'        : 'Reset All Binds key',
            'ResetFeedback'   : 'Enable Reset Feedback Self-/tell',
            'UseSplitModKeys' : 'Bind left and right modifier keys separately',
        })

    def FillTab(self):

        ArchData = Archetypes[self.State['Archetype']]

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
            contents = sorted(ArchData['Primary']),
            tooltip = '',
            callback = self.pickPrimaryPowerSet,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Secondary',
            ctlType = 'combo',
            contents = sorted(ArchData['Secondary']),
            tooltip = '',
            callback = self.pickSecondaryPowerSet,
        )
        powersBox.AddLabeledControl(
            ctlName = 'Epic',
            ctlType = 'combo',
            contents = sorted(ArchData['Epic']),
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
        self.State['Archetype'] = event.GetEventObject.GetValue()
        self.fillPickers()

    def pickOrigin(self):
        self.fillPickers()

    def pickPrimaryPowerSet(self, event):
        self.State['Primary'] = event.GetEventObject.GetValue()
        self.fillPickers

    def pickSecondaryPowerSet(self, event):
        self.State['Secondary'] = event.GetEventObject.GetValue()
        self.fillPickers

    def pickEpicPowerSet(self, event):
        self.State['Epic'] = event.GetEventObject.GetValue()
        self.fillPickers

    def pickPoolPower(self, event):
        # TODO TODO TODO
        return

    def fillPickers(self):
        ArchData = Archetypes[self.Archetype]
        aPicker = wx.Window.FindWindowById(id('Archetype'))
        aPicker.SetStringSelection(self.State['Archetype'])

        oPicker = wx.Window.FindWindowById(id('Origin'))
        oPicker.SetStringSelection(self.State['Origin'])

        pPicker = wx.Window.FindWindowById(id('Primary'))
        pPicker.Clear()
        pPicker.Append(sorted(ArchData['Primary']))
        pPicker.SetStringSelection(self.State['Primary']) or pPicker.SetSelection(1)

        sPicker = wx.Window.FindWindowById(id('Secondary'))
        sPicker.Clear()
        sPicker.Append(sorted(ArchData['Secondary']))
        sPicker.SetStringSelection(self.State['Secondary']) or sPicker.SetSelection(1)

        ePicker = wx.Window.FindWindowById(id('Epic'))
        ePicker.Clear()
        ePicker.Append(sorted(ArchData['Epic']))
        ePicker.SetStringSelection(self.State['Epic']) or sPicker.SetSelection(1)

        for i in [1, 2, 3, 4]:
            ppPicker = wx.Window.FindWindowById(id("Pooli"))
            ppPicker.Clear()
            ppPicker.Append(sorted(MiscPowers['Pool']))
            ppPicker.SetStringSelection(g[Pooli]) or ppPicker.SetSelection(1)

