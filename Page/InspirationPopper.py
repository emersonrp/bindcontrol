import wx
import UI
from Page import Page
from GameData import Inspirations
from UI.ControlGroup import ControlGroup

tabnames = {
    'Basic' : 'Basic Inspirations',
    'Dual' : 'Dual Inspirations',
    'Team' : 'Team Inspirations',
    'DualTeam' : 'Dual Team Inspirations',
}

class InspirationPopper(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Inspiration Popper"

        self.Init = {}

        for tab in tabnames:
            self.Init[f'{tab}AccuracyKey']        = ""
            self.Init[f'{tab}HealthKey']          = ""
            self.Init[f'{tab}DamageKey']          = ""
            self.Init[f'{tab}EnduranceKey']       = ""
            self.Init[f'{tab}DefenseKey']         = ""
            self.Init[f'{tab}BreakFreeKey']       = ""
            self.Init[f'{tab}ResistDamageKey']    = ""
            self.Init[f'{tab}ResurrectionKey']    = ""
            self.Init[f'{tab}RevAccuracyKey']     = ""
            self.Init[f'{tab}RevHealthKey']       = ""
            self.Init[f'{tab}RevDamageKey']       = ""
            self.Init[f'{tab}RevEnduranceKey']    = ""
            self.Init[f'{tab}RevDefenseKey']      = ""
            self.Init[f'{tab}RevBreakFreeKey']    = ""
            self.Init[f'{tab}RevResistDamageKey'] = ""
            self.Init[f'{tab}RevResurrectionKey'] = ""
            for Insp in Inspirations:
                self.Init[f"{tab}{Insp}Border"]     = Inspirations[Insp]['bordercolor']
                self.Init[f"{tab}{Insp}Foreground"] = Inspirations[Insp]['bordercolor']
                self.Init[f"{tab}{Insp}Background"] = Inspirations[Insp]['color']

        self.Init.update({
            'EnableInspBinds'         : False,
            'EnableRevInspBinds'      : False,
            'DisableTells'            : False,
            'BasicAccuracyKey'        : "SHIFT+A",
            'BasicHealthKey'          : "SHIFT+S",
            'BasicDamageKey'          : "SHIFT+D",
            'BasicEnduranceKey'       : "SHIFT+Q",
            'BasicDefenseKey'         : "SHIFT+W",
            'BasicBreakFreeKey'       : "SHIFT+E",
            'BasicResistDamageKey'    : "SHIFT+SPACE",
            'BasicResurrectionKey'    : "SHIFT+TILDE",
            'BasicRevAccuracyKey'     : "SHIFT+CTRL+A",
            'BasicRevHealthKey'       : "SHIFT+CTRL+S",
            'BasicRevDamageKey'       : "SHIFT+CTRL+D",
            'BasicRevEnduranceKey'    : "SHIFT+CTRL+Q",
            'BasicRevDefenseKey'      : "SHIFT+CTRL+W",
            'BasicRevBreakFreeKey'    : "SHIFT+CTRL+E",
            'BasicRevResistDamageKey' : "SHIFT+CTRL+SPACE",
            'BasicRevResurrectionKey' : "SHIFT+CTRL+TILDE",
        })

    def BuildPage(self):

        sizer = wx.BoxSizer(wx.VERTICAL)

        InspTabs = wx.Notebook(self, style = wx.NB_TOP, name = 'InspTabs')

        # TODO - make this radio buttons more like CB4HC does it.
        self.useCB = wx.CheckBox( self, -1, 'Enable Inspiration Popper Binds (prefer largest)')
        self.useCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Inspiration Popper Binds, (largest used first)'))
        self.useCB.SetValue(self.Init['EnableInspBinds'])
        self.Ctrls['EnableInspBinds'] = self.useCB
        sizer.Add(self.useCB, 0, wx.ALL, 10)
        self.useCB.Bind(wx.EVT_CHECKBOX, self.OnEnableCB)

        self.useRevCB = wx.CheckBox( self, -1,
                'Enable Reverse Inspiration Popper Binds (prefer smallest)')
        self.useRevCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Reverse Inspiration Popper Binds, (smallest used first)'))
        self.useRevCB.SetValue(self.Init['EnableRevInspBinds'])
        self.Ctrls['EnableRevInspBinds'] = self.useRevCB
        sizer.Add(self.useRevCB, 0, wx.ALL, 10)
        self.useRevCB.Bind(wx.EVT_CHECKBOX, self.OnEnableRevCB)

        for tab, tabname in tabnames.items():
            tabpanel = wx.Panel(InspTabs)
            InspTabs.AddPage(tabpanel, tabname)
            tabsizer = wx.BoxSizer(wx.VERTICAL)

            InspRows =    ControlGroup(tabpanel, self, width=8, label = "Large Inspirations First")
            RevInspRows = ControlGroup(tabpanel, self, width=8, label = "Small Inspirations First")

            for Insp in Inspirations:
                for order in ("", "Rev"):
                    rowSet = RevInspRows if order else InspRows

                    rowSet.AddControl(
                        ctlType = 'keybutton',
                        ctlName = f"{tab}{order}{Insp}Key",
                        tooltip = f"Choose the key combo to activate a {Insp} inspiration",
                    )

                    rowSet.AddControl(
                        ctlType = 'colorpicker',
                        ctlName = f"{tab}{order}{Insp}Border",
                        contents = Inspirations[Insp]['bordercolor'],
                    )

                    rowSet.AddControl(
                        ctlType = 'colorpicker',
                        ctlName = f"{tab}{order}{Insp}Background",
                        contents = Inspirations[Insp]['color'],
                    )
                    rowSet.AddControl(
                        ctlType = 'colorpicker',
                        ctlName = f"{tab}{order}{Insp}Foreground",
                        contents = Inspirations[Insp]['bordercolor'],
                    )

            tabsizer.Add(InspRows, 0, wx.EXPAND|wx.ALL, 10)
            tabsizer.Add(RevInspRows, 0, wx.EXPAND|wx.ALL, 10)

            tabpanel.SetSizerAndFit(tabsizer)

        sizer.Add(InspTabs, 1, wx.EXPAND)

        self.disableTellsCB = wx.CheckBox( self, -1,
                'Disable self-/tell feedback')
        self.disableTellsCB.SetToolTip(wx.ToolTip(
            'Check this box to avoid having your toon tell you whenever you pop an inspiration.'))
        self.disableTellsCB.SetValue(self.Init['DisableTells'])
        self.Ctrls['DisableTells'] = self.disableTellsCB
        sizer.Add(self.disableTellsCB, 0, wx.ALL, 10)
        self.disableTellsCB.Bind(wx.EVT_CHECKBOX, self.OnDisableTellCB)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(sizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizerAndFit(paddingSizer)

        self.SynchronizeUI()


    def SynchronizeUI(self):
        self.OnEnableCB()
        self.OnEnableRevCB()
        self.OnDisableTellCB()

    def OnEnableCB(self, evt = None):
        controls = []
        for tab in tabnames:
            for Insp in Inspirations:
                controls.append(f"{tab}{Insp}Key")
                controls.append(f"{tab}{Insp}Border")
                controls.append(f"{tab}{Insp}Background")
                controls.append(f"{tab}{Insp}Foreground")
        self.Freeze()
        self.DisableControls(self.useCB.IsChecked(), controls)
        if self.disableTellsCB.IsChecked():
            self.OnDisableTellCB()
        self.Thaw()
        if evt: evt.Skip()

    def OnEnableRevCB(self, evt = None):
        controls = []
        for tab in tabnames:
            for Insp in Inspirations:
                controls.append(f"{tab}Rev{Insp}Key")
                controls.append(f"{tab}Rev{Insp}Border")
                controls.append(f"{tab}Rev{Insp}Background")
                controls.append(f"{tab}Rev{Insp}Foreground")
        self.Freeze()
        self.DisableControls(self.useRevCB.IsChecked(), controls)
        if self.disableTellsCB.IsChecked():
            self.OnDisableTellCB()
        self.Thaw()
        if evt: evt.Skip()

    def OnDisableTellCB(self, evt = None):
        enabled = not self.disableTellsCB.IsChecked()
        controls = []
        revcontrols = []
        for Insp in Inspirations:
            controls.append(f"{Insp}Border")
            controls.append(f"{Insp}Background")
            controls.append(f"{Insp}Foreground")
            revcontrols.append(f"Rev{Insp}Border")
            revcontrols.append(f"Rev{Insp}Background")
            revcontrols.append(f"Rev{Insp}Foreground")
        if self.useCB.IsChecked():
            self.DisableControls(enabled, controls)
        if self.useRevCB.IsChecked():
            self.DisableControls(enabled, revcontrols)
        if evt: evt.Skip()

    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile()

        for Insp in sorted(Inspirations):

            tiers = Inspirations[Insp]['tiers']
            # "reverse" order is as it is in gamebinds, smallest first
            reverseOrder = list(map(lambda s: f"inspexecname {s}", tiers))
            forwardOrder = reverseOrder[::-1]

            if not self.GetState("DisableTells"):
                bc = self.GetState(f'{Insp}Border')
                bg = self.GetState(f'{Insp}Background')
                fg = self.GetState(f'{Insp}Foreground')
                forwardOrder.insert(0, f'tell $name, {ChatColors(fg, bg, bc)}{Insp}')
                bc = self.GetState(f'Rev{Insp}Border')
                bg = self.GetState(f'Rev{Insp}Background')
                fg = self.GetState(f'Rev{Insp}Foreground')
                reverseOrder.insert(0, f'tell $name, {ChatColors(fg, bg, bc)}{Insp}')

            if self.GetState('EnableInspBinds'):
                ResetFile.SetBind(self.Ctrls[f"{Insp}Key"].MakeFileKeyBind(forwardOrder))
            if self.GetState('EnableRevInspBinds'):
                ResetFile.SetBind(self.Ctrls[f"Rev{Insp}Key"].MakeFileKeyBind(reverseOrder))

    UI.Labels['Enable'] = "Enable Inspiration Popper"

    for tab in tabnames:
        UI.Labels[f'{tab}AccuracyKey']        = "Accuracy Key"
        UI.Labels[f'{tab}HealthKey']          = "Health Key"
        UI.Labels[f'{tab}DamageKey']          = "Damage Key"
        UI.Labels[f'{tab}EnduranceKey']       = "Endurance Key"
        UI.Labels[f'{tab}DefenseKey']         = "Defense Key"
        UI.Labels[f'{tab}BreakFreeKey']       = "Break Free Key"
        UI.Labels[f'{tab}ResistDamageKey']    = "Resist Damage Key"
        UI.Labels[f'{tab}ResurrectionKey']    = "Resurrection Key"
        UI.Labels[f'{tab}RevAccuracyKey']     = "Accuracy Key"
        UI.Labels[f'{tab}RevHealthKey']       = "Health Key"
        UI.Labels[f'{tab}RevDamageKey']       = "Damage Key"
        UI.Labels[f'{tab}RevEnduranceKey']    = "Endurance Key"
        UI.Labels[f'{tab}RevDefenseKey']      = "Defense Key"
        UI.Labels[f'{tab}RevBreakFreeKey']    = "Break Free Key"
        UI.Labels[f'{tab}RevResistDamageKey'] = "Resist Damage Key"
        UI.Labels[f'{tab}RevResurrectionKey'] = "Resurrection Key"

        for order in ("", "Rev"):
            for Insp in Inspirations:
                UI.Labels[f"{tab}{order}{Insp}Border"]     = "Border"
                UI.Labels[f"{tab}{order}{Insp}Foreground"] = "Foreground"
                UI.Labels[f"{tab}{order}{Insp}Background"] = "Background"

def ChatColors(fg,bg,bd): return f'<color {fg}><bgcolor {bg}><bordercolor {bd}>'

