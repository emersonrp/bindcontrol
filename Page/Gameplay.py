import wx
from typing import Any
import UI
from Page import Page
from BLF import BLF
from Help import HelpButton

from BindFile import KeyBind

from UI.ControlGroup import ControlGroup, cgChoice
from UI.KeySelectDialog import bcKeyButton

ordinals : tuple = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth")
DefaultTeamBinds : dict[str, tuple] = {
    'Modern'           : (
        'SHIFT+F1', 'SHIFT+F2', 'SHIFT+F3', 'SHIFT+F4', 'SHIFT+F5', 'SHIFT+F6', 'SHIFT+F7', 'SHIFT+F8',
    ),
    'Classic'          : (
        'SHIFT+1', 'SHIFT+2', 'SHIFT+3', 'SHIFT+4', 'SHIFT+5', 'SHIFT+6', 'SHIFT+7', 'SHIFT+8',
    ),
}
DefaultTeamBinds['Joystick'] = DefaultTeamBinds['Classic']
DefaultTeamBinds['Launch (Issue 0)'] = DefaultTeamBinds['Classic']


class Gameplay(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.TabTitle : str = "Gameplay"

        if self.Profile.Server() == 'Homecoming':
            self.NumTrays : int = 4
            self.TrayLabels : tuple = ('', 'First', 'Second', 'Third', 'Server')
            self.KeybindProfiles : dict[str, tuple] = {
                'Modern'           : ('','','ALT','SHIFT','CTRL'),
                'Classic'          : ('','','ALT','CTRL',''),
                'Joystick'         : ('','','ALT','',''),
                'Launch (Issue 0)' : ('','','ALT','',''),
            }
        else: # Rebirth
            self.NumTrays : int = 5
            self.TrayLabels : tuple = ('', 'First', 'Second', 'Third', 'Fourth', 'Server')
            self.KeybindProfiles : dict[str, tuple] = {
                'Default'  : ('','','ALT','CTRL','',''),
                'Joystick' : ('','','ALT','','',''),
                'Original' : ('','','ALT','','',''),
            }

        self.Init : dict[str, Any] = {
            'TPSEnable'              : False,
            'RemoveDefaultTeamBinds' : False,
            'TPSSelMode'             : "Teammates, then pets",
            'TeamSelect1'            : '',
            'TeamSelect2'            : '',
            'TeamSelect3'            : '',
            'TeamSelect4'            : '',
            'TeamSelect5'            : '',
            'TeamSelect6'            : '',
            'TeamSelect7'            : '',
            'TeamSelect8'            : '',

            'TeamEnable'  : False,
            'SelNextTeam' : '',
            'SelPrevTeam' : '',
            'IncTeamSize' : '',
            'DecTeamSize' : '',
            'IncTeamPos'  : '',
            'DecTeamPos'  : '',
            'TeamReset'   : '',

            'Assist'     : '',
            'Location'   : '',
            'Interact'   : '',
            'Menu'       : '',
            'Release'    : '',
            'GameReturn' : '',
            'Sheathe'    : '',
            'Stuck'      : '',
            'DialogYes'  : '',
            'DialogNo'   : '',

            'Tray1Enabled' : False,
            'Tray2Enabled' : False,
            'Tray3Enabled' : False,
            'Tray4Enabled' : False,
        }
        for tray in (range(self.NumTrays, 0, -1)):
            mod = ('', '', 'ALT+', 'SHIFT+', 'CTRL+', '')[tray]
            name = self.TrayLabels[tray]
            self.Init[f"Tray{tray}Next"] = ''
            self.Init[f"Tray{tray}Prev"] = ''
            UI.Labels[f"Tray{tray}Next"] = "Next Tray"
            UI.Labels[f"Tray{tray}Prev"] = "Previous Tray"
            for button in (1,2,3,4,5,6,7,8,9,0):
                ctlname = f'Tray{tray}Button{button}'
                self.Init[ctlname] = f"{mod}{button}"
                UI.Labels[ctlname] = f"{name} Tray, Button {button}"

    def BuildPage(self) -> None:

        ##### Power Tray Buttons
        self.TraySizer = wx.StaticBoxSizer(wx.VERTICAL, self, label = 'Power Tray Buttons')
        staticbox = self.TraySizer.GetStaticBox()

        # Horizontal sizer for "help" button
        GridHelpSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Tray Grid
        trayGridSizer = wx.FlexGridSizer(14,4,0)

        self.FillTrayButtons = {}
        for b in (range(1,self.NumTrays+1)):
            self.FillTrayButtons[b] = wx.Button(staticbox, label = "Fill")
            self.FillTrayButtons[b].Tray = b
            self.FillTrayButtons[b].Bind(wx.EVT_BUTTON, self.OnFillTray)
            self.FillTrayButtons[b].SetToolTip("Fill the buttons with the numbers 1 - 0.  Hold a modifier key while clicking to use that modifier key in the binds.")

        for tray in (range(self.NumTrays, 0, -1)):
            label = self.TrayLabels[tray]
            checkbox = wx.CheckBox(staticbox, label = f"{label} Tray")
            checkbox.SetValue(self.Init.get(f'Tray{tray}Enabled', False))
            checkbox.Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
            self.Ctrls[f'Tray{tray}Enabled'] = checkbox
            trayGridSizer.Add(checkbox, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)

            for button in (1,2,3,4,5,6,7,8,9,0):
                ctlname = f'Tray{tray}Button{button}'
                traybutton = bcKeyButton(staticbox, init = {
                    'CtlName'       : ctlname,
                    'Key'           : self.Init[ctlname],
                    'AlwaysShorten' : True,
                })
                self.Ctrls[ctlname] = traybutton

                trayGridSizer.Add(traybutton, 1, wx.EXPAND)
            trayGridSizer.Add(self.FillTrayButtons[tray], 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

            if tray == self.NumTrays:  # is the server tray
                trayGridSizer.Add(wx.StaticText(staticbox, label = "Prev Tray"), 1, wx.ALIGN_CENTER)
                trayGridSizer.Add(wx.StaticText(staticbox, label = "Next Tray"), 1, wx.ALIGN_CENTER)
            else:
                prevbutton = bcKeyButton(staticbox, init = { 'CtlName' : f"Tray{tray}Prev",})
                self.Ctrls[f"Tray{tray}Prev"] = prevbutton
                nextbutton = bcKeyButton(staticbox, init = { 'CtlName' : f"Tray{tray}Next",})
                self.Ctrls[f"Tray{tray}Next"] = nextbutton
                trayGridSizer.Add(prevbutton, 1, wx.ALIGN_CENTER)
                trayGridSizer.Add(nextbutton, 1, wx.ALIGN_CENTER)

        GridHelpSizer.Add(trayGridSizer, 0, wx.ALL, 10)
        if self.Profile.Server() == 'Rebirth':
            traygridbutton = HelpButton(staticbox, 'PowerTrayButtonsRebirth.html')
        else:
            traygridbutton = HelpButton(staticbox, 'PowerTrayButtons.html')
        GridHelpSizer.Add(traygridbutton, 0, wx.ALL, 10)

        self.TraySizer.Add(GridHelpSizer, 0, wx.ALL, 10)

        # Keybind Profile picker
        KBProfileSizer = wx.BoxSizer(wx.HORIZONTAL)

        KBProfileText = wx.StaticText(staticbox, label = "Keybind Profile:")
        KBProfileSizer.Add(KBProfileText, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)
        KBProfilePicker = cgChoice(staticbox, choices = list(self.KeybindProfiles.keys()))
        KBProfilePicker.SetSelection(0)
        KBProfilePicker.CtlLabel = KBProfileText
        UI.Labels['KBProfile'] = "Keybind Profile"
        self.Ctrls['KBProfile'] = KBProfilePicker
        KBProfilePicker.SetToolTip("This should be set to match the Keybind Profile you have set in the in-game options.")
        KBProfilePicker.Bind( wx.EVT_CHOICE, self.OnKeybindProfilePicker )
        KBProfileSizer.Add(KBProfilePicker, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        KeepExistingCB = wx.CheckBox(staticbox, label = "Keep Existing / Default Tray Binds")
        KeepExistingCB.SetValue(False)
        UI.Labels['KeepExisting'] = "Keep Existing / Default Tray Binds"
        self.Ctrls['KeepExisting'] = KeepExistingCB
        KeepExistingCB.SetToolTip("Check this box to keep existing power tray binds in addition to BindControl-generated binds.  Check the help button to the right for more information.")
        KBProfileSizer.Add(KeepExistingCB, 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)

        KBProfileSizer.Add(HelpButton(staticbox, 'KeepExistingTrayBinds.html'), 0, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 5)


        self.TraySizer.Add(KBProfileSizer, 0, wx.ALL, 10)
        # Bottom Sizer for narrower boxes
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        ##### Enable TPS Direct Select
        tpsenablepanel = wx.Panel(self)
        tpsenablesizer = wx.FlexGridSizer(2)

        tpsenable = wx.CheckBox(tpsenablepanel, label = 'Enable Team/Pet Select')
        tpsenable.SetToolTip('Check this to enable the Combined Team/Pet Select Binds')
        tpsenable.Bind(wx.EVT_CHECKBOX, self.OnTPSEnable)
        self.Ctrls['TPSEnable'] = tpsenable
        tpsenable.SetValue(self.Init['TPSEnable'])

        tpsenablesizer.Add(tpsenable, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        tpsenablesizer.Add(HelpButton(tpsenablepanel, 'TPSBinds.html'), 0)

        removedefaultbinds = wx.CheckBox(tpsenablepanel, label = 'Remove Default Team Select Binds')
        removedefaultbinds.SetToolTip('Check this to disable the default team-selection binds that the game provides.')
        self.Ctrls['RemoveDefaultTeamBinds'] = removedefaultbinds
        removedefaultbinds.SetValue(self.Init['RemoveDefaultTeamBinds'])

        tpsenablesizer.Add(removedefaultbinds, 1, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        tpsenablesizer.Add(HelpButton(tpsenablepanel, 'RemoveDefaultTeamBinds.html'), 0)

        tpsenablepanel.SetSizer(tpsenablesizer)

        ##### direct-select keys
        TPSDirectBox = ControlGroup(self, self, 'Combined Team/Pet Select', topcontent = tpsenablepanel)

        TPSDirectBox.AddControl(
            ctlName = 'TPSSelMode',
            ctlType = 'choice',
            contents = ['Teammates, then pets','Pets, then teammates','Teammates Only','Pets Only'],
            tooltip = 'Choose the order in which teammates and pets are selected with sequential keypresses',
        )
        for selectid in (1,2,3,4,5,6,7,8):
            TPSDirectBox.AddControl(
                ctlName = f"TeamSelect{selectid}",
                ctlType = 'keybutton',
                tooltip = f"Choose the key that will select team member / pet {selectid}",
            )

        ##### Next/Prev Team Select Binds
        teamenablepanel = wx.Panel(self)
        teamenablesizer = wx.BoxSizer(wx.HORIZONTAL)
        teamenable = wx.CheckBox(teamenablepanel, label = 'Enable Team Select')
        teamenable.SetToolTip('Check this to enable the Next/Prev Team Select Binds')
        teamenable.Bind(wx.EVT_CHECKBOX, self.OnTeamEnable)
        self.Ctrls['TeamEnable'] = teamenable
        teamenable.SetValue(self.Init['TeamEnable'])

        teamenablesizer.Add(teamenable, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        teamenablesizer.Add(HelpButton(teamenablepanel, 'TeamSelectBinds.html'), 0)
        teamenablepanel.SetSizer(teamenablesizer)

        TeamSelBox = ControlGroup(self, self, 'Team Select', topcontent = teamenablepanel)
        for b in (
            ['SelPrevTeam', 'Choose the key that will select the previous teammate from the currently selected one'],
            ['SelNextTeam', 'Choose the key that will select the next teammate from the currently selected one']    ,
            ['DecTeamSize', 'Choose the key that will decrease the size of your teammate rotation']                 ,
            ['IncTeamSize', 'Choose the key that will increase the size of your teammate rotation']                 ,
            ['DecTeamPos' , 'Choose the key that will move you to the next lower position in the team rotation']    ,
            ['IncTeamPos' , 'Choose the key that will move you to the next higher position in the team rotation']   ,
            ['TeamReset'  , 'Choose the key that will reset your next/prev teammate binds to Solo / No Position']   ,
        ):
            TeamSelBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        # Helpful Binds
        HelpfulBox = ControlGroup(self, self, 'Miscellaneous Helpful Binds')
        for b in (
            ['Assist'     , 'Choose the key that will target your target\'s current target']                      ,
            ['Location'   , 'Choose the key that will display your current coordinates in the chat window']       ,
            ['Interact'   , 'Choose the key that will interact with the object or entity in front of you']        ,
            ['Menu'       , 'Choose the key that will open the main menu']                                        ,
            ['Release'    , 'Choose the key that will release you to the hospital after a defeat']                ,
            ['GameReturn' , 'Choose the key that will close all extra windows and dialogs and return to the game'],
            ['Sheathe'    , 'Choose the key that will put away your weapons']                                     ,
            ['Stuck'      , 'Choose the key that will try to get you unstuck if you are stuck in geometry']       ,
            ['DialogYes'  , 'Choose the key that will answer OK, Yes, or Accept to the current dialog']           ,
            ['DialogNo'   , 'Choose the key that will answer OK, No, or Cancel to the current dialog']            ,
        ):
            HelpfulBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        bottomSizer.Add(TPSDirectBox,  0, wx.ALL|wx.EXPAND, 10)
        bottomSizer.Add(TeamSelBox,    0, wx.ALL|wx.EXPAND, 10)
        bottomSizer.Add(HelpfulBox,    0, wx.ALL|wx.EXPAND, 10)
        self.MainSizer.Add(self.TraySizer,   flag = wx.ALL|          wx.ALIGN_CENTER_HORIZONTAL, border = 16)
        self.MainSizer.Add(bottomSizer, flag = wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL, border = 16)

    def SynchronizeUI(self, evt = None) -> None:
        self.OnTPSEnable()
        self.OnTeamEnable()

        AnyTray = False
        for tray in (range(1,self.NumTrays+1)):
            self.FillTrayButtons[tray].Enable(self.GetState(f"Tray{tray}Enabled"))
            for button in (1,2,3,4,5,6,7,8,9,0):
                self.Ctrls[f"Tray{tray}Button{button}"].Enable(self.GetState(f'Tray{tray}Enabled'))
            if tray != self.NumTrays:  # not the server tray
                self.Ctrls[f"Tray{tray}Prev"].Enable(self.GetState(f"Tray{tray}Enabled"))
                self.Ctrls[f"Tray{tray}Next"].Enable(self.GetState(f"Tray{tray}Enabled"))
            if self.GetState(f'Tray{tray}Enabled'):
                AnyTray = True
        self.Ctrls['KeepExisting'].Enable(AnyTray)

        self.OnKeybindProfilePicker()

        if evt: evt.Skip()

    def OnKeybindProfilePicker(self, evt = None) -> None:
        pickerval = self.GetState('KBProfile')

        # Fill in the disabled / default keys on the powertray slots with their
        # default values, basically informationally.
        for tray in (range(1,self.NumTrays+1)):
            # skip trays we have activated and therefore might have changed values for
            if self.GetState(f"Tray{tray}Enabled"): continue
            modkey = self.KeybindProfiles[pickerval][tray]
            for button in (1,2,3,4,5,6,7,8,9,0):
                if modkey:
                    buttonval = f"{modkey}+{button}"
                elif tray == 1:
                    buttonval = str(button)
                else:
                    buttonval = ""

                # don't fill in the default value if we're using it somewhere else.
                if self.Profile.CheckConflict(buttonval, ''): continue

                # we could in principle call button.ClearButton() instead of these
                # three lines, but that throws us in an infinite loop
                self.Ctrls[f"Tray{tray}Button{button}"].SetLabel(buttonval)
                self.Ctrls[f"Tray{tray}Button{button}"].Key = buttonval

        self.Profile.CheckAllConflicts()
        if evt: evt.Skip()

    def OnFillTray(self, evt) -> None:
        evtbutton = evt.EventObject
        tray = evtbutton.Tray
        mod = ''
        if   wx.GetKeyState(wx.WXK_SHIFT)   : mod = "SHIFT+"
        elif wx.GetKeyState(wx.WXK_CONTROL) : mod = "CTRL+"
        elif wx.GetKeyState(wx.WXK_ALT)     : mod = "ALT+"
        for button in (1,2,3,4,5,6,7,8,9,0):
            self.Ctrls[f"Tray{tray}Button{button}"].SetLabel(f"{mod}{button}")
            self.Ctrls[f"Tray{tray}Button{button}"].Key = f"{mod}{button}"
        self.Profile.CheckAllConflicts()
        if evt: evt.Skip()

    def OnTPSEnable(self, evt = None) -> None:
        self.EnableControls(self.GetState('TPSEnable'),
            ['TPSSelMode','TeamSelect1','TeamSelect2','TeamSelect3',
            'TeamSelect4', 'TeamSelect5','TeamSelect6','TeamSelect7',
            'TeamSelect8', 'RemoveDefaultTeamBinds'])
        if evt: evt.Skip()

    def OnTeamEnable(self, evt = None) -> None:
        self.EnableControls(self.GetState('TeamEnable'),
            ['SelNextTeam', 'SelPrevTeam','IncTeamSize', 'DecTeamSize',
            'IncTeamPos', 'DecTeamPos', 'TeamReset'])
        if evt: evt.Skip()

    def PopulateBindFiles(self) -> bool:
        ResetFile = self.Profile.ResetFile()
        server = self.Profile.Server()

        ### Tray buttons
        for button in (1,2,3,4,5,6,7,8,9,0):
            slotbutton = button if button != 0 else 10
            if self.GetState('Tray1Enabled'):
                ResetFile.SetBind(self.Ctrls[f"Tray1Button{button}"].MakeBind(f"powexec_slot {slotbutton}"))
            if self.GetState('Tray2Enabled'):
                self.CheckForDefaultKeyToClear(2, button)
                pe_as = "powexec_altslot" if server == "Homecoming" else "px_at1"
                ResetFile.SetBind(self.Ctrls[f"Tray2Button{button}"].MakeBind(f"{pe_as} {slotbutton}"))
            if self.GetState('Tray3Enabled'):
                self.CheckForDefaultKeyToClear(3, button)
                pe_a2 = "powexec_alt2slot" if server == "Homecoming" else "px_at2"
                ResetFile.SetBind(self.Ctrls[f"Tray3Button{button}"].MakeBind(f"{pe_a2} {slotbutton}"))
            if self.GetState('Tray4Enabled'):
                self.CheckForDefaultKeyToClear(4, button)
                pe_ss = 'powexec_serverslot' if server == "Homecoming" else 'px_at3'
                ResetFile.SetBind(self.Ctrls[f"Tray4Button{button}"].MakeBind(f"{pe_ss} {slotbutton}"))
            if self.Ctrls.get('Tray5Enabled') and self.GetState('Tray5Enabled'):
                self.CheckForDefaultKeyToClear(5, button)
                pe_ss = 'px_sv'  # Rebirth only
                ResetFile.SetBind(self.Ctrls[f"Tray5Button{button}"].MakeBind(f"{pe_ss} {slotbutton}"))

        if self.GetState('Tray1Enabled'):
            ResetFile.SetBind(self.Ctrls["Tray1Prev"].MakeBind("prev_tray"))
            ResetFile.SetBind(self.Ctrls["Tray1Next"].MakeBind("next_tray"))
        if self.GetState('Tray2Enabled'):
            ResetFile.SetBind(self.Ctrls["Tray2Prev"].MakeBind("prev_tray_alt"))
            ResetFile.SetBind(self.Ctrls["Tray2Next"].MakeBind("next_tray_alt"))
        if self.GetState('Tray3Enabled'):
            ResetFile.SetBind(self.Ctrls["Tray3Prev"].MakeBind("prev_tray_alt2"))
            ResetFile.SetBind(self.Ctrls["Tray3Next"].MakeBind("next_tray_alt2"))
        if server == "Rebirth" and self.GetState('Tray4Enabled'):
            ResetFile.SetBind(self.Ctrls["Tray4Prev"].MakeBind("prev_tray_alt3"))
            ResetFile.SetBind(self.Ctrls["Tray4Next"].MakeBind("next_tray_alt3"))

        ### Team / Pet Select
        if self.GetState('TPSEnable'):
            if (self.GetState('TPSSelMode') != "Pets Only"
                    and
                self.GetState('TPSSelMode') != "Teammates Only"):

                selmethod = "teamselect"
                selnummod = 0
                selmethod1 = "petselect"
                selnummod1 = 1
                if (self.GetState('TPSSelMode') == "Pets, then teammates"):
                    selmethod = "petselect"
                    selnummod = 1
                    selmethod1 = "teamselect"
                    selnummod1 = 0
                selresetfile = self.Profile.GetBindFile("teamsel","reset.txt")
                for i in (1,2,3,4,5,6,7,8):
                    selfile = self.Profile.GetBindFile("teamsel",f"sel{i}.txt")
                    ResetFile.   SetBind(self.Ctrls[f"TeamSelect{i}"].MakeBind([f"{selmethod} {i - selnummod}", self.Profile.BLF('teamsel',f"sel{i}.txt")]))
                    selresetfile.SetBind(self.Ctrls[f"TeamSelect{i}"].MakeBind([f"{selmethod} {i - selnummod}", self.Profile.BLF('teamsel',f"sel{i}.txt")]))
                    for j in (1,2,3,4,5,6,7,8):
                        if (i == j):
                            selfile.SetBind(self.Ctrls[f"TeamSelect{j}"].MakeBind([f"{selmethod1} {j - selnummod1}", self.Profile.BLF('teamsel',"reset.txt")]))
                        else:
                            selfile.SetBind(self.Ctrls[f"TeamSelect{j}"].MakeBind([f"{selmethod} {j - selnummod}"  , self.Profile.BLF('teamsel',f"sel{j}.txt")]))

            else:
                selmethod = "teamselect"
                selnummod = 0
                if (self.GetState('TPSSelMode') == "Pets Only"):
                    selmethod = "petselect"
                    selnummod = 1
                for i in (1,2,3,4,5,6,7,8):
                    ResetFile.SetBind(self.Ctrls[f'TeamSelect{i}'].MakeBind(f"{selmethod} {i - selnummod}"))

            if self.GetState('RemoveDefaultTeamBinds'):
                for i, key in enumerate(DefaultTeamBinds[self.GetState('KBProfile')]):
                    if not self.Profile.CheckConflict(f"TeamSelect{i}", ''):
                        ResetFile.SetBind(KeyBind(key, '', self, 'nop'))

        # Prev / Next team binds
        if self.GetState('TeamEnable'):
            self.ts2CreateSet(1,0,0,self.Profile.ResetFile())
            for tsize in 1,2,3,4,5,6,7,8:
                for tpos in range(tsize+1):
                    for tsel in range(tsize+1):
                        if (tsel != tpos) or (tsel == 0):
                            file = self.Profile.GetBindFile('teamsel2', f'{tsize}{tpos}{tsel}.txt')
                            self.ts2CreateSet(tsize, tpos, tsel, file)

        ResetFile.SetBind(self.Ctrls['Assist']    .MakeBind('assist'))
        ResetFile.SetBind(self.Ctrls['Location']  .MakeBind('loc'))
        ResetFile.SetBind(self.Ctrls['Interact']  .MakeBind('interact'))
        ResetFile.SetBind(self.Ctrls['Menu']      .MakeBind('menu'))
        ResetFile.SetBind(self.Ctrls['Release']   .MakeBind('release'))
        ResetFile.SetBind(self.Ctrls['GameReturn'].MakeBind('gamereturn'))
        ResetFile.SetBind(self.Ctrls['Sheathe']   .MakeBind('sheathe'))
        ResetFile.SetBind(self.Ctrls['Stuck']     .MakeBind('stuck'))
        ResetFile.SetBind(self.Ctrls['DialogYes'] .MakeBind('dialog_yes'))
        ResetFile.SetBind(self.Ctrls['DialogNo']  .MakeBind('dialog_no'))

        return True

    def CheckForDefaultKeyToClear(self, traynum, button) -> None:
        if not self.GetState("KeepExisting"):
            if KBProfile := self.KeybindProfiles.get(self.GetState('KBProfile')):
                if DefModKey := KBProfile[traynum]:
                    DefKey = f"{DefModKey}+{button}"
                    if self.GetState(f"Tray{traynum}Button{button}") != DefKey and not self.Profile.CheckConflict(DefKey, ''):
                        self.Profile.ResetFile().SetBind(KeyBind(DefKey, "", self, "nop"))

    def AllBindFiles(self) -> dict[str, list]:
        files = [self.Profile.GetBindFile("teamsel", "reset.txt")]
        dirs  = ["teamsel", "teamsel2"]

        for i in (1,2,3,4,5,6,7,8):
            files.append(self.Profile.GetBindFile("teamsel", f"sel{i}.txt"))

        for tsize in 1,2,3,4,5,6,7,8:
            for tpos in range(tsize+1):
                for tsel in range(tsize+1):
                    if (tsel != tpos) or (tsel == 0):
                        files.append(self.Profile.GetBindFile('teamsel2', f'{tsize}{tpos}{tsel}.txt'))

        return {
            'files' : files,
            'dirs'  : dirs,
        }

    def formatTeamConfig(self, size, pos) -> str:
        sizetext = f"{size}-Man"
        postext = ", No Spot"
        if pos > 0   : postext = f", {ordinals[pos-1]} Spot"
        if size == 1 :
            sizetext = "Solo"
            postext = ""
        if size == 2 : sizetext = "Duo"
        if size == 3 : sizetext = "Trio"
        return f"[{sizetext}{postext}]"

    def ts2CreateSet(self, tsize, tpos, tsel, file) -> None:
        # tsize is the size of the team at the moment
        # tpos is the position of the player at the moment, or 0 if unknown
        # tsel is the currently selected team member as far as the bind knows, or 0 if unknown
        file.SetBind(self.GetState('TeamReset'), self, UI.Labels['TeamReset'], f'tell $name, Re-Loaded Next/Prev Team Select Bind.$${BLF()} {self.Profile.GameBindsDir()}\\teamsel2\\100.txt')
        if tsize < 8:
            file.SetBind(self.GetState('IncTeamSize'), self, UI.Labels['IncTeamSize'], f'tell $name, {self.formatTeamConfig(tsize+1,tpos)}$${BLF()} {self.Profile.GameBindsDir()}\\teamsel2\\{tsize+1}{tpos}{tsel}.txt')
        else:
            file.SetBind(self.GetState('IncTeamSize'), self, UI.Labels['IncTeamSize'], 'nop')

        if tsize == 1:
            file.SetBind(self.GetState('DecTeamSize'), self, UI.Labels['DecTeamSize'], 'nop')
            file.SetBind(self.GetState('IncTeamPos'),  self, UI.Labels['IncTeamPos'],  'nop')
            file.SetBind(self.GetState('DecTeamPos'),  self, UI.Labels['DecTeamPos'],  'nop')
            file.SetBind(self.GetState('SelNextTeam'), self, UI.Labels['SelNextTeam'], 'nop')
            file.SetBind(self.GetState('SelPrevTeam'), self, UI.Labels['SelPrevTeam'], 'nop')
        else:
            selnext,selprev = tsel+1,tsel-1
            if selnext > tsize : selnext = 1
            if selprev < 1     : selprev = tsize
            if selnext == tpos : selnext = selnext + 1
            if selprev == tpos : selprev = selprev - 1
            if selnext > tsize : selnext = 1
            if selprev < 1     : selprev = tsize
            tposup,tposdn = tpos+1,tpos-1
            # These next two lines are added by emerson to the original CityBinder logic
            # to fix an issue where if the binds were currently "at" position X, and you
            # tried to inc/dec your position to X, it wouldn't find the (semi-correctly)
            # nonexistent bind file.  This is suboptimal.
            if tposup == tsel  : tposup = tposup + 1
            if tposdn == tsel  : tposdn = tposdn - 1
            # end emerson addition
            if tposup > tsize  : tposup = 0
            if tposdn < 0      : tposdn = tsize
            newpos,newsel = tpos,tsel
            if tsize-1 < tpos  : newpos = tsize-1
            if tsize-1 < tsel  : newsel = tsize-1
            if tsize == 2:
                newpos = 0
                newsel = 0
            file.SetBind(self.GetState('DecTeamSize'), self, UI.Labels['DecTeamSize'], f'tell $name, {self.formatTeamConfig(tsize-1,newpos)}$${BLF()} {self.Profile.GameBindsDir()}\\teamsel2\\{tsize-1}{newpos}{newsel}.txt')
            file.SetBind(self.GetState('IncTeamPos'),  self, UI.Labels['IncTeamPos'],  f'tell $name, {self.formatTeamConfig(tsize,  tposup)}$${BLF()} {self.Profile.GameBindsDir()}\\teamsel2\\{tsize  }{tposup}{tsel  }.txt')
            file.SetBind(self.GetState('DecTeamPos'),  self, UI.Labels['DecTeamPos'],  f'tell $name, {self.formatTeamConfig(tsize,  tposdn)}$${BLF()} {self.Profile.GameBindsDir()}\\teamsel2\\{tsize  }{tposdn}{tsel  }.txt')
            file.SetBind(self.GetState('SelNextTeam'), self, UI.Labels['SelNextTeam'], f'teamselect {selnext}$${BLF()} {self.Profile.GameBindsDir()}\\teamsel2\\{tsize}{tpos}{selnext}.txt')
            file.SetBind(self.GetState('SelPrevTeam'), self, UI.Labels['SelPrevTeam'], f'teamselect {selprev}$${BLF()} {self.Profile.GameBindsDir()}\\teamsel2\\{tsize}{tpos}{selprev}.txt')

    UI.Labels.update({
        'TPSSelMode' : "Team / Pet Select Mode",

        'SelNextTeam' : "Select Next Teammate",
        'SelPrevTeam' : "Select Previous Teammate",
        'IncTeamSize' : "Increase Team Size",
        'DecTeamSize' : "Decrease Team Size",
        'IncTeamPos'  : "Increase Team Position",
        'DecTeamPos'  : "Decrease Team Position",
        'TeamReset'   : "Reset Team Rotation",

        'Assist'     : 'Assist Target',
        'Location'   : "Show Coordinates",
        'Menu'       : "Main Menu",
        'Release'    : "Release to Hospital",
        'GameReturn' : "Return to Game",
        'Sheathe'    : "Sheathe Weapons",
        'Stuck'      : "Try to Get Unstuck",
        'DialogYes'  : "Answer Yes to Dialog",
        'DialogNo'   : "Answer No to Dialog",
    })

    for i in range(1,9):
        UI.Labels[f'TeamSelect{i}'] = f"Select {ordinals[i-1]} Team Member / Pet"

