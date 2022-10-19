# UI / logic for the 'general' panel
import wx
import UI
from Icon import GetIcon
from GameData import Archetypes, Origins, MiscPowers

from UI.ControlGroup import ControlGroup
from UI.IncarnateBox import IncarnateBox

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
            'Epic': '',
            'Pool1': '',
            'Pool2': '',
            'Pool3': '',
            'Pool4': '',
        }

    def BuildPage(self):

        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        powersBox = ControlGroup(self, self, 'Powers and Info')
        self.NameCtrl = powersBox.AddControl(
            ctlName = 'Name',
            ctlType = 'text',
        )
        self.NameCtrl.Bind(wx.EVT_TEXT, self.OnNameCtrlChanged)

        originchoices = []
        for Origin in Origins:
            originchoices.append([Origin, GetIcon(Origin)])
        originpicker = powersBox.AddControl(
            ctlName = 'Origin',
            ctlType = 'bmcombo',
            contents = originchoices,
            callback = self.OnPickOrigin,
        )
        originpicker.SetMinSize([200,-1])

        archchoices = []
        for Arch in sorted(Archetypes):
            archchoices.append([Arch, GetIcon(Arch)])
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

        # Incarnate interface
        self.IncarnateBox = IncarnateBox(self)

        topSizer.Add(powersBox, 1, wx.ALL|wx.EXPAND, 6)
        topSizer.Add(self.IncarnateBox,  2, wx.ALL|wx.EXPAND, 6)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag=wx.ALL|wx.EXPAND, border = 20)

        # testPowerPicker = PowerPicker(self)
        # paddingSizer.Add(testPowerPicker, flag=wx.ALL|wx.EXPAND, border = 20)

        self.SynchronizeUI()

        self.SetSizerAndFit(paddingSizer)

    def SynchronizeUI(self):
        self.OnPickArchetype()

    def PopulateBindFiles(self):
        return

    ### EVENT HANDLERS
    def OnPickArchetype(self, evt = {}):
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

        self.Ctrls['Epic']         .Enable(arch != "Peacebringer" and arch != "Warshade")
        self.Ctrls['Epic'].CtlLabel.Enable(arch != "Peacebringer" and arch != "Warshade")

        if getattr(self.Profile, 'Mastermind', None):
            self.Profile.Mastermind.SynchronizeUI()
        if getattr(self.Profile, 'SoD', None):
            self.Profile.SoD.SynchronizeUI()

        self.Fit()
        if evt: evt.Skip()


    # Event handlers
    def OnNameCtrlChanged(self, evt):
        text = self.NameCtrl.GetValue()
        if len(text) == 0:
            self.NameCtrl.SetBackgroundColour((255,200,200))
        else:
            self.NameCtrl.SetBackgroundColour(wx.NullColour)
        evt.Skip()


    def OnPickOrigin(self, evt):
        evt.Skip()

    def OnPickPoolPower(self, evt):
        evt.Skip()

    def OnPickPrimaryPowerSet(self, evt):
        self.Profile.Mastermind.OnArchetypePowerChange()
        evt.Skip()

    def OnPickSecondaryPowerSet(self, evt):
        evt.Skip()

    def OnPickEpicPowerSet(self, evt):
        evt.Skip()

    UI.Labels.update({
        'Pool1'           : "Power Pool 1",
        'Pool2'           : "Power Pool 2",
        'Pool3'           : "Power Pool 3",
        'Pool4'           : "Power Pool 4",
    })
