# UI / logic for the 'general' panel
import wx
from pathlib import Path
import UI
from Utility import Icon
from UI.PowerPicker import PowerPicker

from GameData import Archetypes, Origins, MiscPowers
from UI.ControlGroup import ControlGroup
from Page import Page

class General(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Init = {
            'Name': 'Profile',
            'Origin': "Magic",
            'Archetype': 'Mastermind',
            'Primary': '',
            'Secondary': '',
            'Epic': 'Weapon Mastery',
            # TODO - help text about WINEPREFIX etc for Mac/Linux users
            'BindsDir': str(Path.home().joinpath("cohbinds")),
            # TODO put this back to Z:\\cohbinds\\
            'GameBindsDir' : "Z:\\cbcohbinds\\",
            'ResetKey': 'LCTRL+R',
            'ResetFeedback': 1,
            'Pool1': '',
            'Pool2': '',
            'Pool3': '',
            'Pool4': '',
            'UseSplitModKeys': False,
            'FlushAllBinds' : False,
        }

    def BuildPage(self):

        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        powersBox = ControlGroup(self, self, 'Powers and Info')
        powersBox.AddControl(
            ctlName = 'Name',
            ctlType = 'text',
        )

        originchoices = []
        for Origin in Origins:
            originchoices.append([Origin, Icon(Origin)])
        originpicker = powersBox.AddControl(
            ctlName = 'Origin',
            ctlType = 'bmcombo',
            contents = originchoices,
            callback = self.OnPickOrigin,
        )
        originpicker.SetMinSize([200,-1])

        archchoices = []
        for Arch in sorted(Archetypes):
            archchoices.append([Arch, Icon(Arch)])
        archpicker = powersBox.AddControl(
            ctlName = 'Archetype',
            ctlType = 'bmcombo',
            contents = archchoices,
            callback = self.OnPickArchetype,
        )
        archpicker.SetMinSize([200,-1])

        powersBox.AddControl(
            ctlName = 'Primary',
            ctlType = 'choice',
            # contents = sorted(ArchData['Primary']),
            callback = self.OnPickPrimaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Secondary',
            ctlType = 'choice',
            # contents = sorted(ArchData['Secondary']),
            callback = self.OnPickSecondaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Epic',
            ctlType = 'choice',
            # contents = sorted(ArchData['Epic']),
            callback = self.OnPickEpicPowerSet,
        )
        poolcontents = sorted(MiscPowers['Pool'])
        poolcontents.insert(0, '')
        powersBox.AddControl(
            ctlName = 'Pool1',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool2',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool3',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool4',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )

        prefsBox = ControlGroup(self, self, 'Preferences')
        prefsBox.AddControl(
            ctlName = 'BindsDir',
            ctlType = 'dirpicker',
        )
        if (wx.Platform != '__WXMSW__'):
            prefsBox.AddControl(
                ctlName = 'GameBindsDir',
                ctlType = 'text',
                tooltip = 'When playing via Wine, the game\'s file paths will be different than the native ones.  Put a Windows path into this box that describes where Wine will find the above directory.',
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

        prefsBox.AddControl(
            ctlName = 'FlushAllBinds',
            ctlType = 'checkbox',
        )

        topSizer.Add(powersBox, 1, wx.ALL, 6)
        topSizer.Add(prefsBox,  2, wx.ALL, 6)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag=wx.ALL|wx.EXPAND, border = 20)

        testPowerPicker = PowerPicker(self)
        paddingSizer.Add(testPowerPicker, flag=wx.ALL|wx.EXPAND, border = 20)

        self.SynchronizeUI()

        self.SetSizerAndFit(paddingSizer)

    def SynchronizeUI(self):
        self.OnPickArchetype()

    def PopulateBindFiles(self):
        resetfile = self.Profile.ResetFile()
        # TODO - the toggling of sprint is probably an SoD option
        resetfile.SetBind(self.Ctrls['ResetKey'].MakeFileKeyBind(
                    [
                        resetfile.BLF(),
                        't $name, Keybinds reloaded.',
                        'up 0', 'down 0', 'forward 0', 'backward 0', 'left 0', 'right 0',
                        'powexecname Sprint',
                        'powexecunqueue',
                        't $name, SoD Binds Reset'
                    ]))

    ### EVENT HANDLERS
    def OnPickArchetype(self, _ = {}):
        arch = self.GetState('Archetype')

        if not arch:
            wx.LogError("Got into OnPickArchetype with arch not set, bailing.")
            return

        self.Ctrls['Primary'].Clear()
        self.Ctrls['Secondary'].Clear()
        self.Ctrls['Epic'].Clear()

        Primaries   = Archetypes[arch]['Primary']
        Secondaries = Archetypes[arch]['Secondary']
        Epix        = Archetypes[arch]['Epic']

        self.Ctrls['Epic'].Append('') # allow us to deselect epic pool

        for p in Primaries   : self.Ctrls['Primary'].Append(p)
        for s in Secondaries : self.Ctrls['Secondary'].Append(s)
        for e in Epix        : self.Ctrls['Epic'].Append(e)

        self.Ctrls['Primary'].SetSelection(0)
        self.Ctrls['Secondary'].SetSelection(0)
        self.Ctrls['Epic'].SetSelection(0)

        if getattr(self.Profile, 'Mastermind', None):
            self.Profile.Mastermind.SynchronizeUI()
        if getattr(self.Profile, 'SoD', None):
            self.Profile.SoD.SynchronizeUI()

        self.Fit()


    # Event handlers
    def OnPickOrigin(self, _):
        # TODO do we need to take any action based on this?
        pass

    def OnPickPoolPower(self, _):
        pass

    def OnPickPrimaryPowerSet(self, _):
        self.Profile.Mastermind.OnArchetypePowerChange()

    def OnPickSecondaryPowerSet(self, _):
        pass

    def OnPickEpicPowerSet(self, _):
        pass

    UI.Labels.update({
        'BindsDir'        : 'Base Binds Directory',
        'GameBindsDir'    : 'In-Game Binds Directory',
        'ResetFile'       : 'Reset All Binds file',
        'ResetKey'        : 'Reset All Binds',
        'ResetFeedback'   : 'Enable Reset Feedback Self-/tell',
        'UseSplitModKeys' : 'Bind left and right modifier keys separately',
        'FlushAllBinds'   : 'Set all binds to default before reapplying',
        'Pool1'           : "Power Pool 1",
        'Pool2'           : "Power Pool 2",
        'Pool3'           : "Power Pool 3",
        'Pool4'           : "Power Pool 4",
    })

