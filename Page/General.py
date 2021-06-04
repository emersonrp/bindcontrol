# UI / logic for the 'general' panel
import wx

from GameData import GameData
from UI.ControlGroup import ControlGroup
from Page import Page

class General(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

    def InitKeys(self, profile):
        self.Profile = profile
        profile.General = self
        profile.PageState[self] = {
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


    def FillTab(self):
        General = self.Profile.General
        State   = self.Profile.PageState[self]

        ArchData = GameData['Archetypes'][State['Archetype']]

        topSizer = wx.BoxSizer(wx.VERTICAL)

        powersBox = ControlGroup(self, 'Powers and Info')
        powersBox.AddLabeledControl(
            value = 'Name',
            ctltype = 'text',
            parent = self,
            module = General,
        )
        powersBox.AddLabeledControl(
            value = 'Archetype',
            ctltype = 'combo',
            parent = self,
            module = General,
            contents = sorted(GameData['Archetypes']),
            tooltip = '',
            callback = self.pickArchetype,
        )
        powersBox.AddLabeledControl(
            value = 'Origin',
            ctltype = 'combo',
            parent = self,
            module = General,
            contents = GameData['Origins'],
            tooltip = '',
            callback = self.pickOrigin,
        )
        powersBox.AddLabeledControl(
            value = 'Primary',
            ctltype = 'combo',
            parent = self,
            module = General,
            contents = sorted(ArchData['Primary']),
            tooltip = '',
            callback = self.pickPrimaryPowerSet,
        )
        powersBox.AddLabeledControl(
            value = 'Secondary',
            ctltype = 'combo',
            parent = self,
            module = General,
            contents = sorted(ArchData['Secondary']),
            tooltip = '',
            callback = self.pickSecondaryPowerSet,
        )
        powersBox.AddLabeledControl(
            value = 'Epic',
            ctltype = 'combo',
            parent = self,
            module = General,
            contents = sorted(ArchData['Epic']),
            tooltip = '',
            callback = self.pickEpicPowerSet,
        )
        powersBox.AddLabeledControl(
            value = 'Pool1',
            ctltype = 'combo',
            parent = self,
            module = General,
            contents = sorted(GameData['MiscPowers']['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            value = 'Pool2',
            ctltype = 'combo',
            parent = self,
            module = General,
            contents = sorted(GameData['MiscPowers']['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            value = 'Pool3',
            ctltype = 'combo',
            parent = self,
            module = General,
            contents = sorted(GameData['MiscPowers']['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            value = 'Pool4',
            ctltype = 'combo',
            parent = self,
            module = General,
            contents = sorted(GameData['MiscPowers']['Pool']),
            tooltip = '',
            callback = self.pickPoolPower,
        )
        powersBox.AddLabeledControl(
            value = 'BindsDir',
            ctltype = 'dirpicker',
            parent = self,
            module = General,
        )
        powersBox.AddLabeledControl(
            value = 'ResetKey',
            ctltype = 'keybutton',
            parent = self,
            module = General,
            tooltip = 'This key is used by certain modules to reset binds to a sane state.',
        )

        powersBox.AddLabeledControl(
            value = 'ResetFeedback',
            ctltype = 'checkbox',
            parent = self,
            module = General,
        )

        writeBindsButton = wx.Button( self, -1, 'Write Binds!' )
        powersBox.Add( writeBindsButton, 0, wx.ALL)
        writeBindsButton.Bind(wx.EVT_BUTTON, self.Profile.WriteBindFiles )

        topSizer.Add(powersBox)
        self.SetSizer(topSizer)
        return self

    def pickArchetype(self, event):
        State['Archetype'] = event.GetEventObject.GetValue
        self.fillPickers()

    def pickOrigin(self):
        self.fillPickers()

    def pickPrimaryPowerSet(self, event):
        State['Primary'] = event.GetEventObject.GetValue
        self.fillPickers

    def pickSecondaryPowerSet(self, event):
        State['Secondary'] = event.GetEventObject.GetValue
        self.fillPickers


    def pickEpicPowerSet(self, event):
        State['Epic'] = event.GetEventObject.GetValue
        self.fillPickers

    def pickPoolPower(self, event):
        # TODO TODO TODO
        return

    def fillPickers(self):

        g = self.Profile.General

        ArchData = GameData['Archetypes'][g.Archetype]
        aPicker = wx.Window.FindWindowById(id('Archetype'))
        aPicker.SetStringSelection(g.Archetype)

        oPicker = wx.Window.FindWindowById(id('Origin'))
        oPicker.SetStringSelection(g.Origin)

        pPicker = wx.Window.FindWindowById(id('Primary'))
        pPicker.Clear()
        pPicker.Append(sorted(ArchData['Primary']))
        pPicker.SetStringSelection(g.Primary) or pPicker.SetSelection(1)

        sPicker = wx.Window.FindWindowById(id('Secondary'))
        sPicker.Clear()
        sPicker.Append(sorted(ArchData['Secondary']))
        sPicker.SetStringSelection(g.Secondary) or sPicker.SetSelection(1)

        ePicker = wx.Window.FindWindowById(id('Epic'))
        ePicker.Clear()
        ePicker.Append(sorted(ArchData['Epic']))
        ePicker.SetStringSelection(g.Epic) or sPicker.SetSelection(1)

        for i in [1, 2, 3, 4]:
            ppPicker = wx.Window.FindWindowById(id("Pooli"))
            ppPicker.Clear()
            ppPicker.Append(sorted(GameData['MiscPowers']['Pool']))
            ppPicker.SetStringSelection(g[Pooli]) or ppPicker.SetSelection(1)

