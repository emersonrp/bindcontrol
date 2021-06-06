# UI / logic for the 'general' panel
import wx
import UI

from GameData import Archetypes, Origins, MiscPowers
from UI.ControlGroup import ControlGroup
from Page import Page

class General(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.State = {
            'Name': '',
            'Archetype': 'Scrapper',
            'Origin': "Magic",
            'Primary': 'Martial Arts',
            'Secondary': 'Super Reflexes',
            'Epic': 'Weapon Mastery',
            'BindsDir': "c:\\CoHTest\\",
            'ResetFile': self.Profile.GetBindFile('reset.txt'),
            'ResetKey': 'CTRL-M',
            'ResetFeedback': 1,
            'Pool1': '',
            'Pool2': '',
            'Pool3': '',
            'Pool4': '',
        }
        UI.Labels.update({
            'BindsDir' : 'Base Binds Directory',
            'ResetFile' : 'Reset All Binds file',
            'ResetKey' : 'Reset All Binds key',
            'ResetFeedback' : 'Give /say feedback on reset',
        })

    def FillTab(self):

        ArchData = Archetypes[self.State['Archetype']]

        topSizer = wx.BoxSizer(wx.VERTICAL)

        powersBox = ControlGroup(self, 'Powers and Info')
        powersBox.AddLabeledControl(
            value = 'Name',
            ctltype = 'text',
            module = self,
        )
        powersBox.AddLabeledControl(
            value = 'Archetype',
            ctltype = 'combo',
            module = self,
            contents = sorted(Archetypes),
            tooltip = '',
            callback = self.pickArchetype,
        )
        powersBox.AddLabeledControl(
            value = 'Origin',
            ctltype = 'combo',
            module = self,
            contents = Origins,
            tooltip = '',
            callback = self.pickOrigin,
        )
        powersBox.AddLabeledControl(
            value = 'Primary',
            ctltype = 'combo',
            module = self,
            contents = sorted(ArchData['Primary']),
            tooltip = '',
            callback = self.pickPrimaryPowerSet,
        )
        powersBox.AddLabeledControl(
            value = 'Secondary',
            ctltype = 'combo',
            module = self,
            contents = sorted(ArchData['Secondary']),
            tooltip = '',
            callback = self.pickSecondaryPowerSet,
        )
        powersBox.AddLabeledControl(
            value = 'Epic',
            ctltype = 'combo',
            module = self,
            contents = sorted(ArchData['Epic']),
            tooltip = '',
            callback = self.pickEpicPowerSet,
        )
        powersBox.AddLabeledControl(
            value = 'Pool1',
            ctltype = 'combo',
            module = self,
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            value = 'Pool2',
            ctltype = 'combo',
            module = self,
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            value = 'Pool3',
            ctltype = 'combo',
            module = self,
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            value = 'Pool4',
            ctltype = 'combo',
            module = self,
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            value = 'BindsDir',
            ctltype = 'dirpicker',
            module = self,
        )
        powersBox.AddLabeledControl(
            value = 'ResetKey',
            ctltype = 'keybutton',
            module = self,
            tooltip = 'This key is used by certain modules to reset binds to a sane state.',
        )

        powersBox.AddLabeledControl(
            value = 'ResetFeedback',
            ctltype = 'checkbox',
            module = self,
        )

        topSizer.Add(powersBox)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag=wx.ALL|wx.EXPAND, border = 20)

        self.SetSizer(paddingSizer)
        return self

    def pickArchetype(self, event):
        self.State['Archetype'] = event.GetEventObject.GetValue
        self.fillPickers()

    def pickOrigin(self):
        self.fillPickers()

    def pickPrimaryPowerSet(self, event):
        self.State['Primary'] = event.GetEventObject.GetValue
        self.fillPickers

    def pickSecondaryPowerSet(self, event):
        self.State['Secondary'] = event.GetEventObject.GetValue
        self.fillPickers

    def pickEpicPowerSet(self, event):
        self.State['Epic'] = event.GetEventObject.GetValue
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

