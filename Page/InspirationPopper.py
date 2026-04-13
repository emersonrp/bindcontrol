import wx
import wx.lib.newevent
import re
from typing import Any

import UI
from Help import HelpButton
import Icon
from Page import Page
import GameData
from UI.ChatColorPicker import ChatColorPicker, ChatColors
from UI.CGControls import cgStaticText
from UI.KeySelectDialog import bcKeyButton
from UI.ProfileAwareControl import ProfileAwareControlMixin

InspOptsChanged, EVT_INSPOPTS_CHANGED = wx.lib.newevent.NewCommandEvent()

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
optcontrols = []
revoptcontrols = []

class InspirationPopper(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.TabTitle : str = "Inspiration Popper"

        self.Init : dict[str, Any] = {}

    def BuildPage(self) -> None:
        for tab in tabs:
            for name in GameData.Inspirations[tab]:
                self.Init[f'{tab}{name}Key']        = ""
                self.Init[f'{tab}Rev{name}Key']     = ""
        self.Init.update({
            'EnableInspBinds'          : False,
            'EnableRevInspBinds'       : False,
            'EnableCombineBinds'       : False,
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
                for Insp, InspInfo in GameData.Inspirations[tab].items():
                    InspDesc = InspInfo['displayname']
                    UI.Labels[f"{tab}{order}{Insp}Key"]     = f"{InspDesc} Key"

                    keygroup = keycontrols if not order else revkeycontrols
                    keygroup.append(f"{tab}{order}{Insp}Key")

                    optgroup = optcontrols if not order else revoptcontrols
                    optgroup.append(f"{tab}{order}{Insp}Opts")

                    chatgroup = chatcontrols if not order else revchatcontrols
                    chatgroup.append(f"{tab}{order}{Insp}Example")

        centeringSizer = wx.BoxSizer(wx.VERTICAL)

        optionsSizer = wx.BoxSizer(wx.HORIZONTAL)

        # "Use Order" options
        self.UseOrderBox = wx.StaticBoxSizer(wx.VERTICAL, self, "Setup Options")

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

        useCombineSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.useCombineBinds = wx.CheckBox(self.UseOrderBox.GetStaticBox(), label = 'Enable press/release inspiration combining')
        self.useCombineBinds.SetToolTip(wx.ToolTip(
            'Check this to enable combining inspirations on keypress.  Check the help button for more information.'))
        self.useCombineBinds.SetValue(self.Init['EnableCombineBinds'])
        self.Ctrls['EnableCombineBinds'] = self.useCombineBinds
        useCombineSizer.Add(self.useCombineBinds, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 6)
        self.useCombineBinds.Bind(wx.EVT_CHECKBOX, self.OnEnableCombineCB)

        combineHelpButton = HelpButton(self.UseOrderBox.GetStaticBox(), 'InspCombineBinds.html')
        useCombineSizer.Add(combineHelpButton, 0, wx.ALIGN_CENTER_VERTICAL)

        self.UseOrderBox.Add(useCombineSizer, 1, wx.ALL, 6)

        optionsSizer.Add(self.UseOrderBox, 1, wx.EXPAND, 0)

        # General Options
        self.OptionsBox = wx.StaticBoxSizer(wx.VERTICAL, self, "Bind Options")

        self.useSuperInspCB = wx.CheckBox(self.OptionsBox.GetStaticBox(), label = 'Use Super Inspirations')
        self.useSuperInspCB.SetToolTip(wx.ToolTip(
            'Check this to include Super Inspirations in the Inspiration Popper binds.  If you\'re concerned about accidental activation and would prefer to use Super Inspirations manually, leave this unchecked.  Super Inspirations cannot be combined.'))
        self.useSuperInspCB.SetValue(self.Init['UseSuperInsp'])
        self.Ctrls['UseSuperInsp'] = self.useSuperInspCB
        self.OptionsBox.Add(self.useSuperInspCB, 0, wx.ALL, 6)

        self.enableTellsCB = wx.CheckBox(self.OptionsBox.GetStaticBox(), label = 'Enable inspiration-colored self-/tell feedback')
        self.enableTellsCB.SetToolTip(wx.ToolTip(
            'Check this box to have your toon /tell you whenever you pop an inspiration.'))
        self.enableTellsCB.SetValue(self.Init['EnableTells'])
        self.Ctrls['EnableTells'] = self.enableTellsCB
        self.OptionsBox.Add(self.enableTellsCB, 0, wx.ALL, 6)
        self.enableTellsCB.Bind(wx.EVT_CHECKBOX, self.OnEnableTellCB)

        optionButtonBox = wx.BoxSizer(wx.HORIZONTAL)
        byInspColorButton = wx.Button(self.OptionsBox.GetStaticBox(), label = "Color-coded")
        byInspColorButton.SetToolTip("Reset self-/tell colors according to inspiration type")
        optionButtonBox.Add(byInspColorButton,      1, wx.ALL, 10)

        self.OptionsBox.Add(optionButtonBox)

        optionsSizer.Add(self.OptionsBox, 1, wx.EXPAND|wx.LEFT, 10)

        centeringSizer.Add(optionsSizer, 1, wx.BOTTOM|wx.EXPAND, 10)

        self.InspTabs = wx.Notebook(self, style = wx.NB_TOP|wx.NB_FIXEDWIDTH, name = 'InspTabs')
        self.InspTabs.SetPadding(wx.Size(2,0))
        il = wx.ImageList(18,18)
        self.InspTabs.AssignImageList(il)
        for tab, tabname in tabs.items():
            tabpanel = wx.Panel(self.InspTabs)
            idx1 = il.Add(Icon.GetIcon("UI", f"Insp{tab}").GetBitmap(wx.Size(18,18)))
            self.InspTabs.AddPage(tabpanel, tabname, imageId = idx1)
            tabsizer = wx.BoxSizer(wx.HORIZONTAL)

            InspBox  = wx.StaticBoxSizer(wx.VERTICAL, tabpanel, "Large Inspirations First")
            InspRows = wx.FlexGridSizer(4,0,3)
            InspRows.AddGrowableCol(1)
            InspBox.Add(InspRows, 1, wx.ALL|wx.EXPAND, 10)

            RevInspBox  = wx.StaticBoxSizer(wx.VERTICAL, tabpanel, "Small Inspirations First")
            RevInspRows = wx.FlexGridSizer(4,0,3)
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
                    keybutton.SetValue(self.Init[keybutton.CtlName])

                    optsbutton = None
                    if tab == 'Single':
                        optsname = f"{tab}{order}{Insp}Opts"
                        optsbutton = InspOptsButton(box.GetStaticBox(), self, Insp)
                        optsbutton.CtlName = optsname
                        self.Ctrls[optsname] = optsbutton

                    chatcolorpicker = ChatColorPicker(box.GetStaticBox(), (tab, order, Insp), InspData)

                    rowSet.Add(kblabel,         0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 3)
                    rowSet.Add(keybutton,       0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 3)
                    if optsbutton:
                        rowSet.Add(optsbutton,      0, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 3)
                    else:
                        rowSet.AddSpacer(1)
                    rowSet.Add(chatcolorpicker, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
                    self.Ctrls[f'{tab}{order}{Insp}Colors'] = chatcolorpicker

            tabsizer.Add(InspBox, 0, wx.EXPAND|wx.ALL, 10)
            tabsizer.Add(RevInspBox, 0, wx.EXPAND|wx.ALL, 10)

            tabpanel.SetSizerAndFit(tabsizer)

        centeringSizer.Add(self.InspTabs, 0, wx.EXPAND)

        self.MainSizer.Add(centeringSizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

    def SynchronizeUI(self) -> None:
        self.OnEnableCB()
        self.OnEnableRevCB()
        self.OnEnableCombineCB()
        self.OnEnableTellCB()

    def OnEnableCB(self, evt = None) -> None:
        if evt: evt.Skip()
        self.EnableControls(self.useCB.IsChecked(), keycontrols)
        self.ShowControls(self.useCB.IsChecked() and self.useCombineBinds.IsChecked(), optcontrols)
        if self.enableTellsCB.IsChecked(): self.OnEnableTellCB()

    def OnEnableRevCB(self, evt = None) -> None:
        if evt: evt.Skip()
        self.EnableControls(self.useRevCB.IsChecked(), revkeycontrols)
        self.ShowControls(self.useRevCB.IsChecked() and self.useCombineBinds.IsChecked(), revoptcontrols)
        if self.enableTellsCB.IsChecked(): self.OnEnableTellCB()

    def OnEnableCombineCB(self, evt = None) -> None:
        if evt: evt.Skip()
        self.OnEnableCB()
        self.OnEnableRevCB()

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
                # "reverse" order is as it is in GameData, smallest first
                reverseOrder = [f"inspexecname {s}" for s in tiers]
                # If we don't want to use Super Insps, trim them from the end of the reverse list
                if not self.GetState('UseSuperInsp'): del reverseOrder[-1:]
                # Then flip it around for "forward" largest-first order
                forwardOrder = reverseOrder[::-1]

                if self.GetState("EnableTells"):
                    cols = self.Ctrls[f'{tab}{Insp}Colors'].GetValue()
                    fg = cols['foreground']
                    bg = cols['background']
                    bc = cols['border']
                    forwardOrder.insert(0, f'tell $name, {ChatColors(fg, bg, bc)}{Insp}')
                    rcols = self.Ctrls[f'{tab}Rev{Insp}Colors'].GetValue()
                    fg = rcols['foreground']
                    bg = rcols['background']
                    bc = rcols['border']
                    reverseOrder.insert(0, f'tell $name, {ChatColors(fg, bg, bc)}{Insp}')

                # this is terribly tangle, I know.
                usecombine = self.GetState('EnableCombineBinds')
                inspabbr = Insp[0:3].lower()
                for order in '', 'Rev':
                    if self.GetState(f'Enable{order}InspBinds'):
                        key = self.Ctrls[f'{tab}{order}{Insp}Key']
                        if not key.GetValue(): continue
                        orderlines = forwardOrder if not order else reverseOrder
                        if usecombine and (tab == 'Single'):
                            combinelines = self.Ctrls[f"{tab}{order}{Insp}Opts"].GetCombineLines()
                            for i, line in enumerate(combinelines):
                                nx = i+1 if (i+1 < len(combinelines)) else 0
                                rev = '' if not order else 'r'
                                downfile = self.Profile.GetBindFile('ip', f'{inspabbr}d{rev}{i}.txt')
                                upfile   = self.Profile.GetBindFile('ip', f'{inspabbr}u{rev}{i}.txt')
                                if i == 0:
                                    ResetFile.SetBind(key.MakeBind(["+", line, upfile.BLF()]))
                                downfile.SetBind(key.MakeBind(["+", line, upfile.BLF()]))
                                upfile  .SetBind(key.MakeBind(["+", *orderlines, self.Profile.BLF('ip', f'{inspabbr}d{rev}{nx}.txt')]))
                        else:
                            ResetFile.SetBind(key.MakeBind(orderlines))

        return True

    # we only fiddle with ResetFile, which is already taken care of.
    def AllBindFiles(self) -> dict[str, list]:
        return {
            'files' : [],
            'dirs'  : [],
        }

class InspOptsButton(ProfileAwareControlMixin, wx.Panel):
    def __init__(self, parent, page, insptype):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)

        self.OptsButton = wx.BitmapToggleButton(self, label = Icon.GetIcon('UI', 'combine'))
        self.OptsButton.SetToolTip(f"Inspiration Combine Options for {insptype}")
        self.OptsButton.Bind(wx.EVT_TOGGLEBUTTON, self.OnOptsButton)

        sizer.Add(self.OptsButton)

        self.Page = page
        self.InspType = insptype
        self.CtlName = ''
        self.CtlLabel = None

        # Where we keep state
        self.CombineInsps = []

        # the UI elements
        self.Dialog = None
        self.CombineCBs = {}

    def OnOptsButton(self, evt):
        if evt: evt.Skip(False) # don't do normal toggle behavior

        if not self.Dialog:
            self.Dialog = wx.Dialog(self.Parent, title = "Inspiration Combine Options")

            mainSizer = wx.BoxSizer(wx.VERTICAL)

            self.Dialog.SetSizer(mainSizer)

            # Just a line at the top indicating this dialog's context:
            infoSizer = wx.BoxSizer(wx.HORIZONTAL)
            inspinfo = GameData.Inspirations['Single'][self.InspType]
            baseicon = Icon.GetIcon('Inspirations', inspinfo['tiers'][0])

            infoSizer.Add(wx.StaticText  (self.Dialog, label = 'Target Type:'), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            infoSizer.Add(wx.StaticBitmap(self.Dialog, bitmap = baseicon),      0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            infoSizer.Add(wx.StaticText  (self.Dialog, label = self.InspType),  0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

            mainSizer.Add(infoSizer, 0, wx.EXPAND|wx.ALL, 10)

            # sizer for the checkboxes for the other types to combine
            self.CBSizer = wx.StaticBoxSizer(wx.VERTICAL, self.Dialog, 'Combine Types')
            mainSizer.Add(self.CBSizer, 0, wx.EXPAND|wx.ALL, 10)

            buttonSizer = self.Dialog.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
            optsHelpButton = HelpButton(self.Dialog, 'InspCombineOpts.html')
            buttonSizer.Prepend(optsHelpButton)
            mainSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 10)

        self.PopulateDialog()
        self.Dialog.Fit()
        self.Dialog.Layout()

        if self.Dialog.ShowModal() == wx.ID_OK:
            # set the actual state vars.
            self.CombineInsps = [i for i,cb in self.CombineCBs.items() if cb.IsChecked()]
            wx.PostEvent(self.Page, InspOptsChanged(wx.NewId(), control = self))
        self.OptsButton.SetValue(bool(self.CombineInsps))

    def PopulateDialog(self):
        self.CBSizer.Clear(delete_windows = True)
        self.CombineCBs.clear()

        othertypes = dict(GameData.Inspirations['Single'].items())
        othertypes.pop(self.InspType)
        for insptype, info in othertypes.items():
            typecb = InspirationTypeCheckBox(self.CBSizer.GetStaticBox(), insptype)
            self.CBSizer.Add(typecb, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
            typecb.SetValue(info['displayname'] in self.CombineInsps)
            self.CombineCBs[info['displayname']] = typecb

        self.Layout()

    def GetCombineLines(self):
        slashcommand = 'mergeinsp' if self.Profile.Server() == 'Homecoming' else 'inspcombine'
        combineitems = []
        for insptype in self.CombineInsps:
            insptype = re.sub(' ', '', insptype) # ugh this gets old
            for idx in range(3):
                srcinsp = re.sub(' ', '_', GameData.Inspirations['Single'][insptype]['tiers'][idx])
                dstinsp = re.sub(' ', '_', GameData.Inspirations['Single'][self.InspType]['tiers'][idx])
                combineitems.append(f'{slashcommand} {srcinsp} {dstinsp}')

        combinelines = []
        inspabbr = self.InspType[0:3].lower()
        blflen = len(self.Profile.BLF('ip', f'{inspabbr}drx.txt'))
        for item in combineitems:
            combinelines = combinelines or ['']
            # check whether what's there, plus '$$' and "+$$"  plus the BLF length, plus the new item is going to exceed 250-ish
            if (len(combinelines[-1]) + 5 + blflen + len(item)) > 250:
                combinelines.append(item) # make a new line
            else:
                combinelines[-1] = combinelines[-1] + '$$' + item # glom onto the existing one
        return combinelines

    def GetValue(self):
        return { 'CombineInsps'  : self.CombineInsps, }

    def SetValue(self, value):
        self.CombineInsps = value.get('CombineInsps', [])
        self.OptsButton.SetValue( bool(self.CombineInsps) ) # toggle "on" if there are any CombineInsps

# call with parent, insp type keyname ("Accuracy" "BreakFree" etc)
class InspirationTypeCheckBox(wx.Panel):
    def __init__(self, parent, insptype):
        super().__init__(parent)

        self.InspType = insptype

        inspdata = GameData.Inspirations['Single'][insptype]

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.CheckBox = wx.CheckBox(self)
        sizer.Add(self.CheckBox, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        mininsp = inspdata['tiers'][0] # get min tier icon just because
        mininsp = re.sub(' ', '', mininsp)

        bitmap = wx.StaticBitmap(self, bitmap = Icon.GetIcon('Inspirations', mininsp))
        sizer.Add(bitmap, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        bitmap.Bind(wx.EVT_LEFT_DOWN, self.OnSomethingClicked)

        self.TypeLabel = wx.StaticText(self, label = inspdata['displayname'])
        sizer.Add(self.TypeLabel, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.TypeLabel.Bind(wx.EVT_LEFT_DOWN, self.OnSomethingClicked)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnSomethingClicked)

        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.TypeLabel.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.TypeLabel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        self.SetSizer(sizer)

    def SetValue(self, value:bool):
        self.CheckBox.SetValue(value)

    def GetValue(self):
        return self.CheckBox.GetValue()

    def IsChecked(self):
        return self.CheckBox.IsChecked()

    def OnSomethingClicked(self, evt):
        evt.Skip()
        self.CheckBox.SetValue(not self.CheckBox.GetValue())

    def OnEnterWindow(self, evt):
        evt.Skip()
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUHILIGHT))
        self.TypeLabel.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

    def OnLeaveWindow(self, evt):
        evt.Skip()
        self.SetBackgroundColour(wx.NullColour)
        self.TypeLabel.SetForegroundColour(wx.NullColour)
