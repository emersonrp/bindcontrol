import wx
import re
from typing import Any
import UI
import Icon
from Page import Page
import GameData
from UI.ChatColorPicker import ChatColorPicker, ChatColors
from UI.CGControls import cgStaticText
from UI.KeySelectDialog import bcKeyButton

tabs = {
    'Single'   : 'Single',
    'Dual'     : 'Dual',
    'Team'     : 'Team',
    'DualTeam' : 'Dual Team',
}

keycontrols = []
revkeycontrols = []
chatcontrols = []
revchatcontrols = []

class InspirationPopper(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.TabTitle : str = "Inspiration Popper"

        self.Init : dict[str, Any] = {}

    def BuildPage(self) -> None:
        for tab in tabs:
            for name, Insp in GameData.Inspirations[tab].items():
                self.Init[f'{tab}{name}Key']        = ""
                self.Init[f'{tab}Rev{name}Key']     = ""
                self.Init[f"{tab}{name}Border"]     = Insp['dkcolor']
                self.Init[f"{tab}{name}Foreground"] = Insp['dkcolor']
                self.Init[f"{tab}{name}Background"] = Insp['ltcolor']
        self.Init.update({
            'EnableInspBinds'          : False,
            'EnableRevInspBinds'       : False,
            'EnableTells'              : True,
            'UseSuperInsp'             : False,
            'SingleAccuracyKey'        : "SHIFT+A",
            'SingleHealthKey'          : "SHIFT+S",
            'SingleDamageKey'          : "SHIFT+D",
            'SingleEnduranceKey'       : "SHIFT+Q",
            'SingleDefenseKey'         : "SHIFT+W",
            'SingleBreakFreeKey'       : "SHIFT+E",
            'SingleResistDamageKey'    : "SHIFT+SPACE",
            'SingleResurrectionKey'    : "SHIFT+TILDE",
        })

        UI.Labels['Enable'] = "Enable Inspiration Popper"

        for tab in tabs:
            for order in ("", "Rev"):
                for Insp in GameData.Inspirations[tab]:
                    InspDesc = Insp
                    if InspDesc == "ResistDamage": InspDesc = "Resist Damage"
                    if InspDesc == "BreakFree"   : InspDesc = "Break Free"
                    UI.Labels[f"{tab}{order}{Insp}Key"]     = f"{InspDesc} Key"

                    keygroup = keycontrols if not order else revkeycontrols
                    keygroup.append(f"{tab}{order}{Insp}Key")

                    chatgroup = chatcontrols if not order else revchatcontrols
                    chatgroup.append(f"{tab}{order}{Insp}Border")
                    chatgroup.append(f"{tab}{order}{Insp}Background")
                    chatgroup.append(f"{tab}{order}{Insp}Foreground")
                    chatgroup.append(f"{tab}{order}{Insp}Example")

        centeringSizer = wx.BoxSizer(wx.VERTICAL)

        optionsSizer = wx.BoxSizer(wx.HORIZONTAL)

        # "Use Order" options
        self.UseOrderBox = wx.StaticBoxSizer(wx.VERTICAL, self, "Use Order")

        self.useCB = wx.CheckBox(self.UseOrderBox.GetStaticBox(), label = 'Enable Largest-First Binds')
        self.useCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Inspiration Popper Binds (largest inspirations used first)'))
        self.useCB.SetValue(self.Init['EnableInspBinds'])
        self.Ctrls['EnableInspBinds'] = self.useCB
        self.UseOrderBox.Add(self.useCB, 1, wx.ALL, 6)
        self.useCB.Bind(wx.EVT_CHECKBOX, self.OnEnableCB)

        self.useRevCB = wx.CheckBox(self.UseOrderBox.GetStaticBox(), label = 'Enable Smallest-First Binds')
        self.useRevCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Reverse Inspiration Popper Binds (smallest inspirations used first)'))
        self.useRevCB.SetValue(self.Init['EnableRevInspBinds'])
        self.Ctrls['EnableRevInspBinds'] = self.useRevCB
        self.UseOrderBox.Add(self.useRevCB, 1, wx.ALL, 6)
        self.useRevCB.Bind(wx.EVT_CHECKBOX, self.OnEnableRevCB)

        optionsSizer.Add(self.UseOrderBox, 1, wx.EXPAND, 0)

        # General Options
        self.OptionsBox = wx.StaticBoxSizer(wx.VERTICAL, self, "Options")

        self.useSuperInspCB = wx.CheckBox(self.OptionsBox.GetStaticBox(), label = 'Use Super Inspirations')
        self.useSuperInspCB.SetToolTip(wx.ToolTip(
            'Check this to include Super Inspirations in the Inspiration Popper binds.  If you\'re concerned about accidental activation and would prefer to use Super Inspirations manually, leave this unchecked.'))
        self.useSuperInspCB.SetValue(self.Init['UseSuperInsp'])
        self.Ctrls['UseSuperInsp'] = self.useSuperInspCB
        self.OptionsBox.Add(self.useSuperInspCB, 0, wx.ALL, 6)

        self.enableTellsCB = wx.CheckBox(self.OptionsBox.GetStaticBox(), label = 'Enable self-/tell feedback')
        self.enableTellsCB.SetToolTip(wx.ToolTip(
            'Check this box to have your toon /tell you whenever you pop an inspiration.'))
        self.enableTellsCB.SetValue(self.Init['EnableTells'])
        self.Ctrls['EnableTells'] = self.enableTellsCB
        self.OptionsBox.Add(self.enableTellsCB, 0, wx.ALL, 6)
        self.enableTellsCB.Bind(wx.EVT_CHECKBOX, self.OnEnableTellCB)

        optionButtonBox = wx.BoxSizer(wx.HORIZONTAL)
        byInspColorButton      = wx.Button(self.OptionsBox.GetStaticBox(), label = "Color-coded")
        byInspColorButton     .SetToolTip("Reset self-/tell colors according to inspiration type")
        optionButtonBox.Add(byInspColorButton,      1, wx.ALL, 10)
        byInspColorButton.Bind(wx.EVT_BUTTON, self.OnByInspColorButton)

        self.OptionsBox.Add(optionButtonBox)

        optionsSizer.Add(self.OptionsBox, 1, wx.EXPAND|wx.LEFT, 10)

        centeringSizer.Add(optionsSizer, 1, wx.BOTTOM|wx.EXPAND, 10)

        self.InspTabs = wx.Notebook(self, style = wx.NB_TOP|wx.NB_FIXEDWIDTH, name = 'InspTabs')
        self.InspTabs.SetPadding(wx.Size(2,0))
        il = wx.ImageList(18,18)
        self.InspTabs.AssignImageList(il)
        for tab, tabname in tabs.items():
            tabpanel = wx.Panel(self.InspTabs)
            idx1 = il.Add(Icon.GetIcon("UI", f"Insp{tab}").GetBitmap(wx.Size(32,32)))
            self.InspTabs.AddPage(tabpanel, tabname, imageId = idx1)
            tabsizer = wx.BoxSizer(wx.VERTICAL)

            InspBox  = wx.StaticBoxSizer(wx.VERTICAL, tabpanel, "Large Inspirations First")
            InspRows = wx.FlexGridSizer(3,0,3)
            InspRows.AddGrowableCol(1)
            InspBox.Add(InspRows, 1, wx.ALL|wx.EXPAND, 10)

            RevInspBox  = wx.StaticBoxSizer(wx.VERTICAL, tabpanel, "Small Inspirations First")
            RevInspRows = wx.FlexGridSizer(3,0,3)
            RevInspRows.AddGrowableCol(1)
            RevInspBox.Add(RevInspRows, 1, wx.ALL|wx.EXPAND, 10)

            for Insp, InspData in GameData.Inspirations[tab].items():
                for order in ("", "Rev"):
                    rowSet = RevInspRows if order else InspRows
                    box    = RevInspBox  if order else InspBox

                    keybutton = bcKeyButton(box.GetStaticBox())
                    keybutton.CtlName = f"{tab}{order}{Insp}Key"
                    kblabel = cgStaticText(box.GetStaticBox(), label = UI.Labels[keybutton.CtlName] + ":")
                    keybutton.CtlLabel = kblabel
                    self.Ctrls[keybutton.CtlName] = keybutton
                    keybutton.Page = self
                    keybutton.SetLabel(self.Init[keybutton.CtlName])
                    keybutton.Key = self.Init[keybutton.CtlName]

                    # reverse the colors if we're doing team inspirations
                    ltcolor = 'ltcolor'
                    dkcolor = 'dkcolor'
                    if tab == "Team" or tab == "DualTeam":
                        ltcolor = 'dkcolor'
                        dkcolor = 'ltcolor'

                    chatcolorpicker = ChatColorPicker(box.GetStaticBox(), self, f"{tab}{order}{Insp}",
                        {
                          'border'     : InspData[dkcolor],
                          'background' : InspData[ltcolor],
                          'text'       : InspData[dkcolor],
                        })

                    rowSet.Add(kblabel,         0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 3)
                    rowSet.Add(keybutton,       0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 3)
                    rowSet.Add(chatcolorpicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)

            tabsizer.Add(InspBox, 0, wx.EXPAND|wx.ALL, 10)
            tabsizer.Add(RevInspBox, 0, wx.EXPAND|wx.ALL, 10)

            tabpanel.SetSizerAndFit(tabsizer)

        centeringSizer.Add(self.InspTabs, 0, wx.EXPAND)

        self.MainSizer.Add(centeringSizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

    def SynchronizeUI(self) -> None:
        self.OnEnableCB()
        self.OnEnableRevCB()
        self.OnEnableTellCB()

    def OnByInspColorButton(self, _) -> None:
        for tab in tabs:
            for Insp, InspData in GameData.Inspirations[tab].items():
                for order in ("", "Rev"):
                    # reverse the colors if we're doing team inspirations
                    ltcolor = 'ltcolor'
                    dkcolor = 'dkcolor'
                    if tab == "Team" or tab == "DualTeam":
                        ltcolor = 'dkcolor'
                        dkcolor = 'ltcolor'

                    self.Ctrls[f'{tab}{order}{Insp}Border']    .SetColour(InspData[dkcolor])
                    self.Ctrls[f'{tab}{order}{Insp}Background'].SetColour(InspData[ltcolor])
                    self.Ctrls[f'{tab}{order}{Insp}Foreground'].SetColour(InspData[dkcolor])

    def OnEnableCB(self, evt = None) -> None:
        if evt: evt.Skip()
        self.EnableControls(self.useCB.IsChecked(), keycontrols)
        if self.enableTellsCB.IsChecked(): self.OnEnableTellCB()

    def OnEnableRevCB(self, evt = None) -> None:
        if evt: evt.Skip()
        self.EnableControls(self.useRevCB.IsChecked(), revkeycontrols)
        if self.enableTellsCB.IsChecked(): self.OnEnableTellCB()

    def OnEnableTellCB(self, evt = None) -> None:
        if evt: evt.Skip()
        enabled = self.enableTellsCB.IsChecked()
        self.EnableControls(enabled and self.useCB   .IsChecked(), chatcontrols)
        self.EnableControls(enabled and self.useRevCB.IsChecked(), revchatcontrols)
        # Hide the Example Text boxes if they're not needed
        for c in chatcontrols:
            if re.search('Example', c):
                self.Ctrls[c].Show(enabled and self.useCB.IsChecked())
        for c in revchatcontrols:
            if re.search('Example', c):
                self.Ctrls[c].Show(enabled and self.useRevCB.IsChecked())

    def PopulateBindFiles(self) -> bool:
        ResetFile = self.Profile.ResetFile()

        for tab in tabs:
            for Insp in sorted(GameData.Inspirations[tab]):

                tiers = GameData.Inspirations[tab][Insp]['tiers']
                # "reverse" order is as it is in gamebinds, smallest first
                reverseOrder = [f"inspexecname {s}" for s in tiers]
                # If we don't want to use Super Insps, trim them from the end of the reverse list
                if not self.GetState('UseSuperInsp'): del reverseOrder[-1:]
                # Then flip it around for "forward" largest-first order
                forwardOrder = reverseOrder[::-1]

                if self.GetState("EnableTells"):
                    bc = self.GetState(f'{tab}{Insp}Border')
                    bg = self.GetState(f'{tab}{Insp}Background')
                    fg = self.GetState(f'{tab}{Insp}Foreground')
                    forwardOrder.insert(0, f'tell $name, {ChatColors(fg, bg, bc)}{Insp}')
                    bc = self.GetState(f'{tab}Rev{Insp}Border')
                    bg = self.GetState(f'{tab}Rev{Insp}Background')
                    fg = self.GetState(f'{tab}Rev{Insp}Foreground')
                    reverseOrder.insert(0, f'tell $name, {ChatColors(fg, bg, bc)}{Insp}')

                if self.GetState('EnableInspBinds'):
                    ResetFile.SetBind(self.Ctrls[f"{tab}{Insp}Key"].MakeBind(forwardOrder))
                if self.GetState('EnableRevInspBinds'):
                    ResetFile.SetBind(self.Ctrls[f"{tab}Rev{Insp}Key"].MakeBind(reverseOrder))

        return True

    # we only fiddle with ResetFile, which is already taken care of.
    def AllBindFiles(self) -> dict[str, list]:
        return {
            'files' : [],
            'dirs'  : [],
        }
