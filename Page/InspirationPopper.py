import wx
import wx.lib.colourselect as csel
from typing import Dict, Any
import UI
import Icon
from Page import Page
import GameData
from UI.ChatColorPicker import ChatColorPicker, ChatColors
from UI.KeySelectDialog import bcKeyButton

tabs = {
    'Single'   : 'Single',
    'Dual'     : 'Dual',
    'Team'     : 'Team',
    'DualTeam' : 'Dual Team',
}

class InspirationPopper(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Inspiration Popper"
        self.chatPickers = {}

        self.Init : Dict[str, Any] = {}

    def BuildPage(self):
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
                    UI.Labels[f"{tab}{order}{Insp}Key"]        = f"{InspDesc} Key"

        centeringSizer = wx.BoxSizer(wx.VERTICAL)

        optionsSizer = wx.BoxSizer(wx.HORIZONTAL)

        # "Use Order" options
        useOrderBox = wx.StaticBoxSizer(wx.VERTICAL, self, "Use Order")

        self.useCB = wx.CheckBox( useOrderBox.GetStaticBox(), -1, 'Enable Largest-First Binds')
        self.useCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Inspiration Popper Binds, (largest inspirations used first)'))
        self.useCB.SetValue(self.Init['EnableInspBinds'])
        self.Ctrls['EnableInspBinds'] = self.useCB
        useOrderBox.Add(self.useCB, 1, wx.ALL, 6)
        self.useCB.Bind(wx.EVT_CHECKBOX, self.OnEnableCB)

        self.useRevCB = wx.CheckBox( useOrderBox.GetStaticBox(), -1, 'Enable Smallest-First Binds')
        self.useRevCB.SetToolTip(wx.ToolTip(
            'Check this to enable the Reverse Inspiration Popper Binds, (smallest inspirations used first)'))
        self.useRevCB.SetValue(self.Init['EnableRevInspBinds'])
        self.Ctrls['EnableRevInspBinds'] = self.useRevCB
        useOrderBox.Add(self.useRevCB, 1, wx.ALL, 6)
        self.useRevCB.Bind(wx.EVT_CHECKBOX, self.OnEnableRevCB)

        optionsSizer.Add(useOrderBox, 1, wx.EXPAND, 0)

        # General Options
        optionsBox = wx.StaticBoxSizer(wx.VERTICAL, self, "Options")
        self.useSuperInspCB = wx.CheckBox( optionsBox.GetStaticBox(), -1, 'Use Super Inspirations')
        self.useSuperInspCB.SetToolTip(wx.ToolTip(
            'Check this to include Super Inspirations in the Inspiration Popper binds.  If you\'re concerned about accidental activation and would prefer to use Super Inspirations manually, leave this unchecked.'))
        self.useSuperInspCB.SetValue(self.Init['UseSuperInsp'])
        self.Ctrls['UseSuperInsp'] = self.useSuperInspCB
        optionsBox.Add(self.useSuperInspCB, 0, wx.ALL, 6)

        self.enableTellsCB = wx.CheckBox( optionsBox.GetStaticBox(), -1, 'Enable self-/tell feedback')
        self.enableTellsCB.SetToolTip(wx.ToolTip(
            'Check this box to avoid having your toon tell you whenever you pop an inspiration.'))
        self.enableTellsCB.SetValue(self.Init['EnableTells'])
        self.Ctrls['EnableTells'] = self.enableTellsCB
        optionsBox.Add(self.enableTellsCB, 0, wx.ALL, 6)
        self.enableTellsCB.Bind(wx.EVT_CHECKBOX, self.OnEnableTellCB)

        optionButtonBox = wx.BoxSizer(wx.HORIZONTAL)
        # profileChatColorButton = wx.Button(optionsBox.GetStaticBox(), label = "Profile's Chat Colors")
        # profileChatColorButton.SetToolTip("Set self-/tell colors to the default profile chat colors")
        byInspColorButton      = wx.Button(optionsBox.GetStaticBox(), label = "Color-coded")
        byInspColorButton     .SetToolTip("Reset self-/tell colors according to inspiration type")
        # optionButtonBox.Add(profileChatColorButton, 1, wx.ALL, 10)
        optionButtonBox.Add(byInspColorButton,      1, wx.ALL, 10)
        # profileChatColorButton.Bind(wx.EVT_BUTTON, self.OnProfileChatColorButton)
        byInspColorButton     .Bind(wx.EVT_BUTTON, self.OnByInspColorButton)

        optionsBox.Add(optionButtonBox)

        optionsSizer.Add(optionsBox, 1, wx.EXPAND|wx.LEFT, 10)

        centeringSizer.Add(optionsSizer, 1, wx.BOTTOM|wx.EXPAND, 10)

        InspTabs = wx.Notebook(self, style = wx.NB_TOP, name = 'InspTabs')
        InspTabs.SetPadding(wx.Size(2,0))
        il = wx.ImageList(18,18)
        InspTabs.AssignImageList(il)
        for tab, tabname in tabs.items():
            tabpanel = wx.Panel(InspTabs)
            idx1 = il.Add(Icon.GetIcon("UI", f"Insp{tab}").GetBitmap(wx.Size(32,32)))
            InspTabs.AddPage(tabpanel, tabname, imageId = idx1)
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

                    keybutton = bcKeyButton(box.GetStaticBox(), wx.ID_ANY)
                    keybutton.CtlName = f"{tab}{order}{Insp}Key"
                    kblabel = wx.StaticText(box.GetStaticBox(), wx.ID_ANY, label = UI.Labels[keybutton.CtlName] + ":")
                    keybutton.CtlLabel = kblabel
                    self.Ctrls[keybutton.CtlName] = keybutton
                    keybutton.Page = self
                    keybutton.SetLabel(self.Init[keybutton.CtlName])
                    keybutton.Key = self.Init[keybutton.CtlName]

                    # reverse the colors if we're doing team inspirations
                    ltcolor = 'ltcolor'; dkcolor = 'dkcolor'
                    if tab == "Team" or tab == "DualTeam":
                        ltcolor = 'dkcolor'; dkcolor = 'ltcolor'

                    chatcolorpicker = ChatColorPicker(box.GetStaticBox(), self, f"{tab}{order}{Insp}",
                        {
                          'border'     : InspData[dkcolor],
                          'background' : InspData[ltcolor],
                          'text'       : InspData[dkcolor],
                        })
                    self.chatPickers[f"{tab}{order}{Insp}"] = chatcolorpicker

                    rowSet.Add(kblabel,         0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 3)
                    rowSet.Add(keybutton,       0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 3)
                    rowSet.Add(chatcolorpicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)

            tabsizer.Add(InspBox, 0, wx.EXPAND|wx.ALL, 10)
            tabsizer.Add(RevInspBox, 0, wx.EXPAND|wx.ALL, 10)

            tabpanel.SetSizerAndFit(tabsizer)

        centeringSizer.Add(InspTabs, 0, wx.EXPAND)

        self.MainSizer.Add(centeringSizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

    def SynchronizeUI(self):
        self.OnEnableCB()
        self.OnEnableRevCB()
        self.OnEnableTellCB()

    def OnProfileChatColorButton(self, _):
        dkcolor = self.Profile.General.GetState('ChatForeground')
        ltcolor = self.Profile.General.GetState('ChatBackground')
        for tab in tabs:
            for Insp in GameData.Inspirations[tab]:
                for order in ("", "Rev"):
                    self.Ctrls[f'{tab}{order}{Insp}Border']    .SetColour(dkcolor)
                    self.Ctrls[f'{tab}{order}{Insp}Background'].SetColour(ltcolor)
                    self.Ctrls[f'{tab}{order}{Insp}Foreground'].SetColour(dkcolor)
                    control = self.Ctrls[f'{tab}{order}{Insp}Border']
                    wx.PostEvent(control, wx.CommandEvent(csel.EVT_COLOURSELECT.typeId, control.GetId()))

    def OnByInspColorButton(self, _):
        for tab in tabs:
            for Insp, InspData in GameData.Inspirations[tab].items():
                for order in ("", "Rev"):
                    # reverse the colors if we're doing team inspirations
                    ltcolor = 'ltcolor'; dkcolor = 'dkcolor'
                    if tab == "Team" or tab == "DualTeam":
                        ltcolor = 'dkcolor'; dkcolor = 'ltcolor'

                    self.Ctrls[f'{tab}{order}{Insp}Border']    .SetColour(InspData[dkcolor])
                    self.Ctrls[f'{tab}{order}{Insp}Background'].SetColour(InspData[ltcolor])
                    self.Ctrls[f'{tab}{order}{Insp}Foreground'].SetColour(InspData[dkcolor])
                    control = self.Ctrls[f'{tab}{order}{Insp}Border']
                    wx.PostEvent(control, wx.CommandEvent(csel.EVT_COLOURSELECT.typeId, control.GetId()))


    def OnEnableCB(self, evt = None):
        controls = []
        for tab in tabs:
            for Insp in GameData.Inspirations[tab]:
                controls.append(f"{tab}{Insp}Key")
                controls.append(f"{tab}{Insp}Border")
                controls.append(f"{tab}{Insp}Background")
                controls.append(f"{tab}{Insp}Foreground")
        self.Freeze()
        self.EnableControls(self.useCB.IsChecked(), controls)
        if self.enableTellsCB.IsChecked():
            self.OnEnableTellCB()
        self.Profile.CheckAllConflicts()
        self.Thaw()
        if evt: evt.Skip()

    def OnEnableRevCB(self, evt = None):
        controls = []
        for tab in tabs:
            for Insp in GameData.Inspirations[tab]:
                controls.append(f"{tab}Rev{Insp}Key")
                controls.append(f"{tab}Rev{Insp}Border")
                controls.append(f"{tab}Rev{Insp}Background")
                controls.append(f"{tab}Rev{Insp}Foreground")
        self.Freeze()
        self.EnableControls(self.useRevCB.IsChecked(), controls)
        if self.enableTellsCB.IsChecked():
            self.OnEnableTellCB()
        self.Profile.CheckAllConflicts()
        self.Thaw()
        if evt: evt.Skip()

    def OnEnableTellCB(self, evt = None):
        enabled = self.enableTellsCB.IsChecked()
        controls = []
        revcontrols = []
        for tab in tabs:
            for Insp in GameData.Inspirations[tab]:
                controls.append(f"{tab}{Insp}Border")
                controls.append(f"{tab}{Insp}Background")
                controls.append(f"{tab}{Insp}Foreground")
                revcontrols.append(f"{tab}Rev{Insp}Border")
                revcontrols.append(f"{tab}Rev{Insp}Background")
                revcontrols.append(f"{tab}Rev{Insp}Foreground")
        if self.useCB.IsChecked():
            self.EnableControls(enabled, controls)
        if self.useRevCB.IsChecked():
            self.EnableControls(enabled, revcontrols)
        if evt: evt.Skip()

    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile()

        for tab in tabs:
            for Insp in sorted(GameData.Inspirations[tab]):

                tiers = GameData.Inspirations[tab][Insp]['tiers']
                # "reverse" order is as it is in gamebinds, smallest first
                reverseOrder = list(map(lambda s: f"inspexecname {s}", tiers))
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
                    ResetFile.SetBind(self.Ctrls[f"{tab}{Insp}Key"].MakeFileKeyBind(forwardOrder))
                if self.GetState('EnableRevInspBinds'):
                    ResetFile.SetBind(self.Ctrls[f"{tab}Rev{Insp}Key"].MakeFileKeyBind(reverseOrder))

        return True

    # we only fiddle with ResetFile, which is already taken care of.
    def AllBindFiles(self):
        return {
            'files' : [],
            'dirs'  : [],
        }
