import wx
import UI
import Utility
from Page import Page
from GameData import Inspirations
from UI.ControlGroup import ControlGroup

class InspirationPopper(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Inspiration Popper"

        self.Init = {
            'EnableInspBinds'    : True,
            'EnableRevInspBinds' : True,
            'AccuracyKey'        : "LSHIFT+A",
            'HealthKey'          : "LSHIFT+S",
            'DamageKey'          : "LSHIFT+D",
            'EnduranceKey'       : "LSHIFT+Q",
            'DefenseKey'         : "LSHIFT+W",
            'BreakFreeKey'       : "LSHIFT+E",
            'ResistDamageKey'    : "LSHIFT+SPACE",
            'ResurrectionKey'    : "LSHIFT+TILDE",
            'RevAccuracyKey'     : "UNBOUND",
            'RevHealthKey'       : "UNBOUND",
            'RevDamageKey'       : "UNBOUND",
            'RevEnduranceKey'    : "UNBOUND",
            'RevDefenseKey'      : "UNBOUND",
            'RevBreakFreeKey'    : "UNBOUND",
            'RevResistDamageKey' : "UNBOUND",
            'RevResurrectionKey' : "UNBOUND",
            'DisableTells'       : False,
        }
        for Insp in Inspirations:
            self.Init[f"{Insp}Border"]     = Inspirations[Insp]['color']
            self.Init[f"{Insp}Foreground"] = wx.BLACK
            self.Init[f"{Insp}Background"] = wx.WHITE

    def BuildPage(self):

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.InspRows =    ControlGroup(self, self, width=8)
        self.RevInspRows = ControlGroup(self, self, width=8)

        for Insp in Inspirations:
            revkey = f"Rev{Insp}Key"
            colors = f"{Insp}Colors"
            revcol = f"Rev{colors}"

            for order in ("", "Rev"):

                rowSet = self.RevInspRows if order else self.InspRows

                rowSet.AddLabeledControl(
                    ctlType = 'keybutton',
                    ctlName = f"{order}{Insp}Key",
                    tooltip = f"Choose the key combo to activate a {Insp} inspiration",
                )

                rowSet.AddLabeledControl(
                    ctlType = 'colorpicker',
                    ctlName = f"{order}{Insp}Border",
                    contents = Inspirations[Insp]['color'],
                )

                rowSet.AddLabeledControl(
                    ctlType = 'colorpicker',
                    ctlName = f"{order}{Insp}Background",
                    contents = wx.WHITE,
                )
                rowSet.AddLabeledControl(
                    ctlType = 'colorpicker',
                    ctlName = f"{order}{Insp}Foreground",
                    contents = wx.BLACK,
                )


        self.useCB = wx.CheckBox( self, -1, 'Enable Inspiration Popper Binds (prefer largest)')
        self.useCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Inspiration Popper Binds, (largest used first)'))
        self.useCB.SetValue(self.Init['EnableInspBinds'])
        self.Controls['EnableInspBinds'] = self.useCB
        sizer.Add(self.useCB, 0, wx.ALL, 10)
        self.useCB.Bind(wx.EVT_CHECKBOX, self.OnEnableCB)

        sizer.Add(self.InspRows, 0, wx.EXPAND)

        sizer.AddSpacer(20)

        self.useRevCB = wx.CheckBox( self, -1,
                'Enable Reverse Inspiration Popper Binds (prefer smallest)')
        self.useRevCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Reverse Inspiration Popper Binds, (smallest used first)'))
        self.useRevCB.SetValue(self.Init['EnableRevInspBinds'])
        self.Controls['EnableRevInspBinds'] = self.useRevCB
        sizer.Add(self.useRevCB, 0, wx.ALL, 10)
        self.useRevCB.Bind(wx.EVT_CHECKBOX, self.OnEnableRevCB)

        sizer.Add(self.RevInspRows, 0, wx.EXPAND)


        self.disableTellsCB = wx.CheckBox( self, -1,
                'Disable self-/tell feedback')
        self.disableTellsCB.SetToolTip(wx.ToolTip(
            'Check this box to avoid having your toon tell you whenever you pop an inspiration.'))
        self.disableTellsCB.SetValue(self.Init['DisableTells'])
        self.Controls['DisableTells'] = self.disableTellsCB
        sizer.Add(self.disableTellsCB, 0, wx.ALL, 10)
        self.disableTellsCB.Bind(wx.EVT_CHECKBOX, self.OnDisableTellCB)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(sizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizerAndFit(paddingSizer)

    def OnEnableCB(self, evt):
        enable = evt.EventObject.IsChecked()
        notells = self.disableTellsCB.IsChecked()
        for Insp in Inspirations:
            self.Controls[f"{Insp}Key"].Enable(enable)
            self.Controls[f"{Insp}Border"].Enable(enable and not notells)
            self.Controls[f"{Insp}Background"].Enable(enable and not notells)
            self.Controls[f"{Insp}Foreground"].Enable(enable and not notells)

    def OnEnableRevCB(self, evt):
        enable = evt.EventObject.IsChecked()
        notells = self.disableTellsCB.IsChecked()
        for Insp in Inspirations:
            self.Controls[f"Rev{Insp}Key"].Enable(enable)
            self.Controls[f"Rev{Insp}Border"].Enable(enable and not notells)
            self.Controls[f"Rev{Insp}Background"].Enable(enable and not notells)
            self.Controls[f"Rev{Insp}Foreground"].Enable(enable and not notells)

    def OnDisableTellCB(self, evt):
        enable = evt.EventObject.IsChecked()
        forward  = self.useCB.IsChecked()
        reverse  = self.useRevCB.IsChecked()
        for Insp in Inspirations:
            self.Controls[f"{Insp}Border"].Enable(not enable and forward)
            self.Controls[f"{Insp}Background"].Enable(not enable and forward)
            self.Controls[f"{Insp}Foreground"].Enable(not enable and forward)
            self.Controls[f"Rev{Insp}Border"].Enable(not enable and reverse)
            self.Controls[f"Rev{Insp}Background"].Enable(not enable and reverse)
            self.Controls[f"Rev{Insp}Foreground"].Enable(not enable and reverse)

    def PopulateBindFiles(self):
        profile = self.Profile

        ResetFile = profile.ResetFile()

        for Insp in sorted(Inspirations):

            tiers = Inspirations[Insp]['tiers']
            forwardOrder = list(map(lambda s: f"inspexecname {s}", tiers))
            reverseOrder = forwardOrder[::-1]

            if not self.GetState("DisableTells"):
                bc = self.GetState(f'{Insp}Border')
                bg = self.GetState(f'{Insp}Background')
                fg = self.GetState(f'{Insp}Foreground')
                forwardOrder.insert(0, f'tell $name, {Utility.ChatColors(fg, bg, bc)}{Insp}')
                bc = self.GetState(f'Rev{Insp}Border')
                bg = self.GetState(f'Rev{Insp}Background')
                fg = self.GetState(f'Rev{Insp}Foreground')
                reverseOrder.insert(0, f'tell $name, {Utility.ChatColors(fg, bg, bc)}{Insp}')

            if self.GetState('EnableInspBinds'):
                ResetFile.SetBind(self.Controls[f"{Insp}Key"].KeyBind.MakeFileKeyBind(forwardOrder))
            if self.GetState('EnableRevInspBinds'):
                ResetFile.SetBind(self.Controls[f"Rev{Insp}Key"].KeyBind.MakeFileKeyBind(reverseOrder))

    def findconflicts(self, profile):
        ### TODO
        return
        ### TODO

        if self.GetState('EnableInspBinds'):
            Utility.CheckConflict(self.State,'acckey',"Accuracy Key")
            Utility.CheckConflict(self.State,'hpkey',"Healing Key")
            Utility.CheckConflict(self.State,'damkey',"Damage Key")
            Utility.CheckConflict(self.State,'endkey',"Endurance Key")
            Utility.CheckConflict(self.State,'defkey',"Defense Key")
            Utility.CheckConflict(self.State,'bfkey',"Breakfree Key")
            Utility.CheckConflict(self.State,'reskey',"Resistance Key")

        if self.GetState('EnableRevInspBinds'):
            Utility.CheckConflict(self.State,'racckey',"Reverse Accuracy Key")
            Utility.CheckConflict(self.State,'rhpkey',"Reverse Healing Key")
            Utility.CheckConflict(self.State,'rdamkey',"Reverse Damage Key")
            Utility.CheckConflict(self.State,'rendkey',"Reverse Endurance Key")
            Utility.CheckConflict(self.State,'rdefkey',"Reverse Defense Key")
            Utility.CheckConflict(self.State,'rbfkey',"Reverse Breakfree Key")
            Utility.CheckConflict(self.State,'rreskey',"Reverse Resistance Key")

    def bindisused(self, profile):
        return bool(self.State['Enable'] or self.State['Reverse'])

    UI.Labels.update({
        'Enable'          : "Enable Inspiration Popper",
        'AccuracyKey'     : "Accuracy Key",
        'HealthKey'       : "Health Key",
        'DamageKey'       : "Damage Key",
        'EnduranceKey'    : "Endurance Key",
        'DefenseKey'      : "Defense Key",
        'BreakFreeKey'    : "Break Free Key",
        'ResistDamageKey' : "Resist Damage Key",
        'ResurrectionKey' : "Resurrection Key",
        'RevAccuracyKey'     : "Reverse Accuracy Key",
        'RevHealthKey'       : "Reverse Health Key",
        'RevDamageKey'       : "Reverse Damage Key",
        'RevEnduranceKey'    : "Reverse Endurance Key",
        'RevDefenseKey'      : "Reverse Defense Key",
        'RevBreakFreeKey'    : "Reverse Break Free Key",
        'RevResistDamageKey' : "Reverse Resist Damage Key",
        'RevResurrectionKey' : "Reverse Resurrection Key",
    })
    for order in ("", "Rev"):
        for Insp in Inspirations:
            UI.Labels[f"{order}{Insp}Border"] = "Border"
            UI.Labels[f"{order}{Insp}Foreground"] = "Foreground"
            UI.Labels[f"{order}{Insp}Background"] = "Background"
