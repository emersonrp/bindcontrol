# UI / logic for the 'general' panel
import wx
from pathlib import Path
import UI
from UI.PowerBinderDialog import PowerBinderButton

from GameData import Archetypes, Origins, MiscPowers
from UI.ControlGroup import ControlGroup
from Page import Page

class General(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        profile = parent

        self.Init = {
            'Name': 'Profile',
            'Origin': "Magic",
            'Archetype': 'Mastermind',
            'Primary': '',
            'Secondary': '',
            'Epic': 'Weapon Mastery',
            # TODO - find CoH install and put them there?
            # TODO - help text about WINEPREFIX etc for Mac/Linux users
            'BindsDir': str(Path.home().joinpath("cohbinds")),
            'ResetKey': 'LCTRL+R',
            'ResetFeedback': 1,
            'Pool1': '',
            'Pool2': '',
            'Pool3': '',
            'Pool4': '',
            'UseSplitModKeys': False,
        }

    def BuildPage(self):

        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        powersBox = ControlGroup(self, self, 'Powers and Info')
        powersBox.AddControl(
            ctlName = 'Name',
            ctlType = 'text',
        )
        powersBox.AddControl(
            ctlName = 'Origin',
            ctlType = 'choice',
            contents = Origins,
            tooltip = '',
            callback = self.OnPickOrigin,
        )
        powersBox.AddControl(
            ctlName = 'Archetype',
            ctlType = 'choice',
            contents = sorted(Archetypes),
            tooltip = '',
            callback = self.OnPickArchetype,
        )
        powersBox.AddControl(
            ctlName = 'Primary',
            ctlType = 'choice',
            # contents = sorted(ArchData['Primary']),
            tooltip = '',
            callback = self.OnPickPrimaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Secondary',
            ctlType = 'choice',
            # contents = sorted(ArchData['Secondary']),
            tooltip = '',
            callback = self.OnPickSecondaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Epic',
            ctlType = 'choice',
            # contents = sorted(ArchData['Epic']),
            tooltip = '',
            callback = self.OnPickEpicPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Pool1',
            ctlType = 'choice',
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool2',
            ctlType = 'choice',
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool3',
            ctlType = 'choice',
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool4',
            ctlType = 'choice',
            contents = sorted(MiscPowers['Pool']),
            tooltip = '',
            callback = self.OnPickPoolPower,
        )

        prefsBox = ControlGroup(self, self, 'Preferences')
        prefsBox.AddControl(
            ctlName = 'BindsDir',
            ctlType = 'dirpicker',
        )
        prefsBox.AddControl(
            ctlName = 'ResetKey',
            ctlType = 'keybutton',
            tooltip = 'This key is used by certain modules to reset binds to a sane state.',
        )

        prefsBox.AddControl(
            ctlName = 'ResetFeedback',
            ctlType = 'checkbox',
        )

        prefsBox.AddControl(
            ctlName = 'UseSplitModKeys',
            ctlType = 'checkbox',
        )

        topSizer.Add(powersBox, 0, wx.ALL, 6)
        topSizer.Add(prefsBox, 0, wx.ALL, 6)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag=wx.ALL|wx.EXPAND, border = 20)

        testPowerBinder = PowerBinderButton(self, None)
        paddingSizer.Add(testPowerBinder, flag=wx.ALL|wx.EXPAND, border = 20)

        # pre-fill the Primary/secondary pickers
        self.OnPickArchetype()

        self.SetSizerAndFit(paddingSizer)

    def PopulateBindFiles(self):
        resetfile = self.Profile.ResetFile()

        # TODO - the toggling of sprint is probably an SoD option
        resetfile.SetBind(self.Ctrls['ResetKey'].KeyBind.MakeFileKeyBind(
                    [
                        resetfile.BLF(),
                        't $name, Keybinds reloaded.',
                        'up 0', 'down 0', 'forward 0', 'backward 0', 'left 0', 'right 0',
                        'powexecname Sprint',
                        'powexecunqueue',
                        't $name, SoD Binds Reset'
                    ]))

    ### EVENT HANDLERS
    def OnPickArchetype(self, event = {}):
        choice = self.Ctrls['Archetype']
        index  = choice.GetSelection()
        arch   = choice.GetString(index)

        self.Ctrls['Primary'].Clear()
        self.Ctrls['Secondary'].Clear()
        self.Ctrls['Epic'].Clear()

        Primaries   = Archetypes[arch]['Primary']
        Secondaries = Archetypes[arch]['Secondary']
        Epix        = Archetypes[arch]['Epic']

        for p in Primaries   : self.Ctrls['Primary'].Append(p)
        for s in Secondaries : self.Ctrls['Secondary'].Append(s)
        for e in Epix        : self.Ctrls['Epic'].Append(e)

        self.Ctrls['Primary'].SetSelection(0)
        self.Ctrls['Secondary'].SetSelection(0)
        self.Ctrls['Epic'].SetSelection(0)

        if getattr(self.Profile, 'Mastermind', None):
            self.Profile.Mastermind.OnArchetypePowerChange()

        self.Fit()


    # Event handlers
    def OnPickOrigin(self, event):
        # TODO do we need to take any action based on this?
        pass

    def OnPickPoolPower(self, event):
        pass

    def OnPickPrimaryPowerSet(self, event):
        self.Profile.Mastermind.OnArchetypePowerChange()

    def OnPickSecondaryPowerSet(self, event):
        pass

    def OnPickEpicPowerSet(self, event):
        pass

    def GetPowers(self):
        archetype = self.GetState('Archetype')
        primary   = self.GetState('Primary')
        secondary = self.GetState('Secondary')
        epic      = self.GetState('Epic')
        # TODO, for 1-4, collect up pool powers
        # TODO - maybe also Incarnate stuff?

        arch = Archetypes.get(archetype, None)
        if not arch: return []

        powers = []
        pp = Archetypes[archetype]['Primary'].get(primary, None)
        if pp: powers.extend(pp)
        sp = Archetypes[archetype]['Secondary'].get(secondary, None)
        if sp: powers.extend(sp)
        ep = Archetypes[archetype]['Epic'].get(epic, None)
        if ep: powers.extend(ep)

        return powers


    UI.Labels.update({
        'BindsDir'        : 'Base Binds Directory',
        'ResetFile'       : 'Reset All Binds file',
        'ResetKey'        : 'Reset All Binds',
        'ResetFeedback'   : 'Enable Reset Feedback Self-/tell',
        'UseSplitModKeys' : 'Bind left and right modifier keys separately',
    })

