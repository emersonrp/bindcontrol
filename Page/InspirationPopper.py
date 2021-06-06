import wx
import Utility
from Page import Page
from GameData import Inspirations

class InspirationPopper(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Inspiration Popper"

        self.State = {
            'Enable'          : None,
            'AccuracyKey'     : "LSHIFT+A",
            'HealthKey'       : "LSHIFT+S",
            'DamageKey'       : "LSHIFT+D",
            'EnduranceKey'    : "LSHIFT+Q",
            'DefenseKey'      : "LSHIFT+W",
            'BreakFreeKey'    : "LSHIFT+E",
            'ResistDamageKey' : "LSHIFT+SPACE",
        }

    def FillTab(self):

        sizer = wx.BoxSizer(wx.VERTICAL)

        InspRows =    wx.FlexGridSizer(0,10,2,2)
        RevInspRows = wx.FlexGridSizer(0,10,2,2)

        for Insp in sorted(Inspirations):
            revkey = f"Rev{Insp}Key"
            colors = f"{Insp}Colors"
            revcol = f"Rev{colors}"

            if not self.State.get(revkey, None):
                self.State[revkey] = "UNBOUND"
            if not self.State.get(colors, None):
                self.State[colors] = Utility.ColorDefault()
            if not self.State.get(revcol, None):
                self.State[revcol] = Utility.ColorDefault()

            for order in ("", "Rev"):

                if order:
                    rowSet = RevInspRows
                else:
                    rowSet = InspRows

                rowSet.Add( wx.StaticText(self, -1, f"{order} {Insp} Key"), 0,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

                KeyPicker = wx.Button(self, -1, self.State[f"{order}{Insp}Key"])
                KeyPicker.SetToolTip(
                        wx.ToolTip(f"Choose the key combo to activate a {Insp} inspiration") )
                rowSet.Add ( KeyPicker, 0, wx.EXPAND)

                rowSet.AddStretchSpacer(wx.EXPAND)

                ColorsCB = wx.CheckBox(self, -1, '')
                ColorsCB.SetToolTip( wx.ToolTip("Colorize Inspiration-Popper chat feedback") )
                rowSet.Add ( ColorsCB, 0, wx.ALIGN_CENTER_VERTICAL)

                rowSet.Add( wx.StaticText(self, -1, "Border"), 0,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
                bc = self.State[f"{order}{Insp}Colors"]['border']
                rowSet.Add( wx.ColourPickerCtrl(
                        self, -1,
                        wx.Colour(bc['r'], bc['g'], bc['b']),
                        wx.DefaultPosition, wx.DefaultSize,
                    )
                )

                rowSet.Add( wx.StaticText(self, -1, "Background"), 0,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
                bc = self.State[f"{order}{Insp}Colors"]['background']
                rowSet.Add( wx.ColourPickerCtrl(
                        self, -1,
                        wx.Colour(bc['r'], bc['g'], bc['b']),
                        wx.DefaultPosition, wx.DefaultSize,
                    )
                )
                rowSet.Add( wx.StaticText(self, -1, "Text"), 0,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
                fc = self.State[f"{order}{Insp}Colors"]['foreground']
                rowSet.Add( wx.ColourPickerCtrl(
                        self, -1,
                        wx.Colour(fc['r'], fc['g'], fc['b']),
                        wx.DefaultPosition, wx.DefaultSize,
                    )
                )

        useCB = wx.CheckBox( self, -1, 'Enable Inspiration Popper Binds (prefer largest)')
        useCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Inspiration Popper Binds, (largest used first)'))
        sizer.Add(useCB, 0, wx.ALL, 10)

        sizer.Add(InspRows)

        useRevCB = wx.CheckBox( self, -1,
                'Enable Reverse Inspiration Popper Binds (prefer smallest)')
        useCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Reverse Inspiration Popper Binds, (smallest used first)'))
        sizer.Add(useRevCB, 0, wx.ALL, 10)

        sizer.Add(RevInspRows)

        self.SetSizerAndFit(sizer)


    def PopulateBindFiles(self):
        profile = self.Profile

        ResetFile = profile.Pages['General'].State[ResetFile]

        for Insp in sorted(Inspirations):
            forwardOrder = ""
            reverseOrder = ""

            for item in Inspirations[Insp]:
                forwardOrder = forwardOrder + f"inspexecname {item}"

            for item in Inspirations[Insp].reverse():
                reverseOrder = reverseOrder + f"inspexecname {item}"


            if self.State['Feedback']:
                forwardOrder = cbChatColorOutput(self.State[f"{Insp}Colors"]) + Insp + forwardOrder
                reverseOrder = cbChatColorOutput(self.State[f"Rev{Insp}Colors"]) + Insp + reverseOrder

        if self.State['Enable']:
            cbWriteBind(ResetFile, self.State[f"{Insp}Key"], forwardOrder)
        if self.State['Reverse']:
            cbWriteBind(ResetFile, self.State[f"Rev{Insp}Key"], reverseOrder)

    def findconflicts(self, profile):
        if self.State['Enable']:
            Utility.CheckConflict(self.State,'acckey',"Accuracy Key")
            Utility.CheckConflict(self.State,'hpkey',"Healing Key")
            Utility.CheckConflict(self.State,'damkey',"Damage Key")
            Utility.CheckConflict(self.State,'endkey',"Endurance Key")
            Utility.CheckConflict(self.State,'defkey',"Defense Key")
            Utility.CheckConflict(self.State,'bfkey',"Breakfree Key")
            Utility.CheckConflict(self.State,'reskey',"Resistance Key")

        if self.State['Reverse']:
            Utility.CheckConflict(self.State,'racckey',"Reverse Accuracy Key")
            Utility.CheckConflict(self.State,'rhpkey',"Reverse Healing Key")
            Utility.CheckConflict(self.State,'rdamkey',"Reverse Damage Key")
            Utility.CheckConflict(self.State,'rendkey',"Reverse Endurance Key")
            Utility.CheckConflict(self.State,'rdefkey',"Reverse Defense Key")
            Utility.CheckConflict(self.State,'rbfkey',"Reverse Breakfree Key")
            Utility.CheckConflict(self.State,'rreskey',"Reverse Resistance Key")

    def bindisused(self, profile):
        return bool(self.State['Enable'] or self.State['Reverse'])
