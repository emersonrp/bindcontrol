import wx
import UI
from BLF import BLF
from Help import HelpButton

from UI.ControlGroup import ControlGroup
from UI.KeySelectDialog import bcKeyButton
from Page import Page

ordinals = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth")

class Gameplay(Page):

    def __init__(self, parent):
        Page.__init__(self, parent)
        self.TabTitle = "Gameplay"
        self.Init = {
            'TPSEnable'   : False,
            'TPSSelMode'  : "Teammates, then pets",
            'TeamSelect1' : '',
            'TeamSelect2' : '',
            'TeamSelect3' : '',
            'TeamSelect4' : '',
            'TeamSelect5' : '',
            'TeamSelect6' : '',
            'TeamSelect7' : '',
            'TeamSelect8' : '',

            'TeamEnable'  : False,
            'SelNextTeam' : '',
            'SelPrevTeam' : '',
            'IncTeamSize' : '',
            'DecTeamSize' : '',
            'IncTeamPos'  : '',
            'DecTeamPos'  : '',
            'TeamReset'   : '',

            'QuitToDesktop' : '',
            'InviteTarget'  : '',
            'FPSBindKey'      : '',
            'NetgraphBindKey' : '',

            'Tray1Enabled' : False,
            'Tray2Enabled' : False,
            'Tray3Enabled' : False,
            'Tray4Enabled' : False,
        }
        for tray in (3,2,1):
            mod = ['', '', 'ALT+', 'SHIFT+'][tray]
            for button in (1,2,3,4,5,6,7,8,9,0):
                ctlname = f'Tray{tray}Button{button}'
                self.Init[ctlname] = f"{mod}{button}"
                UI.Labels[ctlname] = f"Tray {tray}, Button {button}"

        for button in (1,2,3,4,5,6,7,8,9,0):
            ctlname = f'Tray4Button{button}'
            self.Init[ctlname] = f"CTRL+{button}"
            UI.Labels[ctlname] = f"Server Tray, Button {button}"


    def BuildPage(self):

        ##### Power Tray Buttons
        traySizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label = 'Power Tray Buttons')
        staticbox = traySizer.GetStaticBox()

        self.FillTrayButtons = {}
        for b in (1,2,3,4):
            self.FillTrayButtons[b] = wx.Button(staticbox, wx.ID_ANY, "Fill")
            setattr(self.FillTrayButtons[b], 'Tray', b)
            self.FillTrayButtons[b].Bind(wx.EVT_BUTTON, self.OnFillTray)
            self.FillTrayButtons[b].SetToolTip("Fill the buttons with the numbers 1 - 0.  Hold a modifier key while clicking to use that modifier key in the binds.")

        trayGridSizer = wx.FlexGridSizer(12,4,0)
        # server tray at the top
        checkbox = wx.CheckBox(staticbox, wx.ID_ANY, label = f"Server Tray")
        checkbox.SetValue(self.Init.get(f'Tray4Enabled', False))
        checkbox.Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        self.Ctrls[f'Tray4Enabled'] = checkbox
        trayGridSizer.Add(checkbox, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)

        for button in (1,2,3,4,5,6,7,8,9,0):
            ctlname = f'Tray4Button{button}'
            traybutton = bcKeyButton(staticbox, wx.ID_ANY, init = {
                'CtlName'       : ctlname,
                'Key'           : self.Init[ctlname],
                'AlwaysShorten' : True,
            })
            self.Ctrls[ctlname] = traybutton

            trayGridSizer.Add(traybutton, 1, wx.EXPAND)
        trayGridSizer.Add(self.FillTrayButtons[4], 1, wx.EXPAND|wx.LEFT, 10)

        # Then the three main trays
        for tray in (3,2,1):
            checkbox = wx.CheckBox(staticbox, wx.ID_ANY, label = f"Tray {tray}")
            checkbox.SetValue(self.Init.get(f'Tray{tray}Enabled', False))
            checkbox.Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
            self.Ctrls[f'Tray{tray}Enabled'] = checkbox
            trayGridSizer.Add(checkbox, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)

            for button in (1,2,3,4,5,6,7,8,9,0):
                ctlname = f'Tray{tray}Button{button}'
                traybutton = bcKeyButton(staticbox, wx.ID_ANY, init = {
                    'CtlName'       : ctlname,
                    'Key'           : self.Init[ctlname],
                    'AlwaysShorten' : True,
                })
                self.Ctrls[ctlname] = traybutton

                trayGridSizer.Add(traybutton, 1, wx.EXPAND)
            trayGridSizer.Add(self.FillTrayButtons[tray], 1, wx.EXPAND|wx.LEFT, 10)

        traySizer.Add(trayGridSizer, 0, wx.ALL, 10)
        traygridbutton = HelpButton(staticbox, 'PowerTrayButtons.html')
        traySizer.Add(traygridbutton, 0, wx.ALL, 10)

        # Bottom Sizer for narrower boxes
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)

        ##### Enable TPS Direct Select
        tpsenablesizer = wx.BoxSizer(wx.HORIZONTAL)

        tpsenable = wx.CheckBox( self, -1, 'Enable Team/Pet Select')
        tpsenable.SetToolTip( wx.ToolTip('Check this to enable the Combined Team/Pet Select Binds') )
        tpsenable.Bind(wx.EVT_CHECKBOX, self.OnTPSEnable)
        self.Ctrls['TPSEnable'] = tpsenable
        tpsenable.SetValue(self.Init['TPSEnable'])

        tpshelpbutton = HelpButton(self, 'TPSBinds.html')

        tpsenablesizer.Add(tpsenable, 0, wx.ALIGN_CENTER_VERTICAL)
        tpsenablesizer.Add(tpshelpbutton, wx.ALIGN_RIGHT)

        leftSizer.Add(tpsenablesizer, 0, wx.ALL, 10)

        ##### direct-select keys
        TPSDirectBox = ControlGroup(self, self, 'Combined Team/Pet Select')

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
        leftSizer.Add(TPSDirectBox, 0, wx.EXPAND|wx.ALL, 10)

        ##### Next/Prev Team Select Binds
        teamenablesizer = wx.BoxSizer(wx.HORIZONTAL)
        teamenable = wx.CheckBox( self, -1, 'Enable Team Select')
        teamenable.SetToolTip( wx.ToolTip('Check this to enable the Next/Prev Team Select Binds') )
        teamenable.Bind(wx.EVT_CHECKBOX, self.OnTeamEnable)
        self.Ctrls['TeamEnable'] = teamenable
        teamenable.SetValue(self.Init['TeamEnable'])

        teamhelpbutton = HelpButton(self, 'TeamSelectBinds.html')

        teamenablesizer.Add(teamenable, 0, wx.ALIGN_CENTER_VERTICAL)
        teamenablesizer.Add(teamhelpbutton, wx.ALIGN_RIGHT)

        rightSizer.Add(teamenablesizer, 0, wx.ALL, 10)

        TeamSelBox = ControlGroup(self, self, 'Team Select')
        for b in (
            ['SelPrevTeam' , 'Choose the key that will select the previous teammate from the currently selected one'] ,
            ['SelNextTeam' , 'Choose the key that will select the next teammate from the currently selected one']     ,
            ['DecTeamSize' , 'Choose the key that will decrease the size of your teammate rotation']                  ,
            ['IncTeamSize' , 'Choose the key that will increase the size of your teammate rotation']                  ,
            ['DecTeamPos'  , 'Choose the key that will move you to the next lower position in the team rotation']         ,
            ['IncTeamPos'  , 'Choose the key that will move you to the next higher position in the team rotation']        ,
            ['TeamReset'   , 'Choose the key that will reset your next/prev teammate binds to Solo / No Position']                             ,
        ):
            TeamSelBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )
        rightSizer.Add(TeamSelBox, 0, wx.EXPAND|wx.ALL, 10)

        ### Helpful Binds
        HelpfulSizer = ControlGroup(self, self, 'Helpful Binds')
        for b in (
            ['QuitToDesktop'   , 'Choose the key that will quit directly to the desktop']  ,
            ['InviteTarget'    , 'Choose the key that will invite your target to a group'] ,
            ['FPSBindKey'      , 'Choose the key that will toggle the FPS Display']        ,
            ['NetgraphBindKey' , 'Choose the key that will toggle the Netgraph Display']   ,
        ):
            HelpfulSizer.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        rightSizer.Add(HelpfulSizer, 0, wx.EXPAND|wx.ALL, 10)

        bottomSizer.Add(leftSizer,  0, wx.ALL|wx.EXPAND, 10)
        bottomSizer.Add(rightSizer, 0, wx.ALL|wx.EXPAND, 10)
        self.MainSizer.Add(traySizer,   flag = wx.ALL|          wx.ALIGN_CENTER_HORIZONTAL, border = 16)
        self.MainSizer.Add(bottomSizer, flag = wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_HORIZONTAL, border = 16)

        self.SynchronizeUI()

    def SynchronizeUI(self, evt = None):
        self.OnTPSEnable()
        self.OnTeamEnable()
        for tray in (1,2,3,4):
            self.FillTrayButtons[tray].Enable(self.GetState(f"Tray{tray}Enabled"))
            for button in (1,2,3,4,5,6,7,8,9,0):
                self.Ctrls[f"Tray{tray}Button{button}"].Enable(self.GetState(f'Tray{tray}Enabled'))
        self.Profile.CheckAllConflicts()
        if evt: evt.Skip()

    def OnFillTray(self, evt):
        evtbutton = evt.EventObject
        tray = evtbutton.Tray
        mod = ''
        if   wx.GetKeyState(wx.WXK_SHIFT)   : mod = "SHIFT+"
        elif wx.GetKeyState(wx.WXK_CONTROL) : mod = "CTRL+"
        elif wx.GetKeyState(wx.WXK_ALT)     : mod = "ALT+"
        for button in (1,2,3,4,5,6,7,8,9,0):
            self.Ctrls[f"Tray{tray}Button{button}"].Key = f"{mod}{button}"
            self.Ctrls[f"Tray{tray}Button{button}"].SetLabel(f"{mod}{button}")
        self.Profile.CheckAllConflicts()
        if evt: evt.Skip()

    def OnTPSEnable(self, evt = None):
        self.EnableControls(self.GetState('TPSEnable'),
            ['TPSSelMode','TeamSelect1','TeamSelect2','TeamSelect3',
            'TeamSelect4', 'TeamSelect5','TeamSelect6','TeamSelect7',
            'TeamSelect8'])
        if evt: evt.Skip()

    def OnTeamEnable(self, evt = None):
        self.EnableControls(self.GetState('TeamEnable'),
            ['SelNextTeam', 'SelPrevTeam','IncTeamSize', 'DecTeamSize',
            'IncTeamPos', 'DecTeamPos', 'TeamReset'])
        if evt: evt.Skip()

    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile()

        ### Tray buttons
        for button in (1,2,3,4,5,6,7,8,9,0):
            slotbutton = button if button != 0 else 10
            if self.GetState('Tray1Enabled'):
                ResetFile.SetBind(self.Ctrls[f"Tray1Button{button}"].MakeFileKeyBind(f"powexec_slot {slotbutton}"))
            if self.GetState('Tray2Enabled'):
                ResetFile.SetBind(self.Ctrls[f"Tray2Button{button}"].MakeFileKeyBind(f"powexec_altslot {slotbutton}"))
            if self.GetState('Tray3Enabled'):
                ResetFile.SetBind(self.Ctrls[f"Tray3Button{button}"].MakeFileKeyBind(f"powexec_alt2slot {slotbutton}"))
            if self.GetState('Tray4Enabled'):
                ResetFile.SetBind(self.Ctrls[f"Tray4Button{button}"].MakeFileKeyBind(f"powexec_serverslot {slotbutton}"))


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
                    ResetFile.   SetBind(self.Ctrls[f"TeamSelect{i}"].MakeFileKeyBind([f"{selmethod} {i - selnummod}", self.Profile.BLF('teamsel',f"sel{i}.txt")]))
                    selresetfile.SetBind(self.Ctrls[f"TeamSelect{i}"].MakeFileKeyBind([f"{selmethod} {i - selnummod}", self.Profile.BLF('teamsel',f"sel{i}.txt")]))
                    for j in (1,2,3,4,5,6,7,8):
                        if (i == j):
                            selfile.SetBind(self.Ctrls[f"TeamSelect{j}"].MakeFileKeyBind([f"{selmethod1} {j - selnummod1}", self.Profile.BLF('teamsel',"reset.txt")]))
                        else:
                            selfile.SetBind(self.Ctrls[f"TeamSelect{j}"].MakeFileKeyBind([f"{selmethod} {j - selnummod}"  , self.Profile.BLF('teamsel',f"sel{j}.txt")]))

            else:
                selmethod = "teamselect"
                selnummod = 0
                if (self.GetState('TPSSelMode') == "Pets Only"):
                    selmethod = "petselect"
                    selnummod = 1
                for i in (1,2,3,4,5,6,7,8):
                    ResetFile.SetBind(self.Ctrls[f'TeamSelect{i}'].MakeFileKeyBind(f"{selmethod} {i - selnummod}"))

            ResetFile = self.Profile.ResetFile()

        # Prev / Next team binds
        if self.GetState('TeamEnable'):
            self.ts2CreateSet(1,0,0,self.Profile.ResetFile())
            for tsize in 1,2,3,4,5,6,7,8:
                for tpos in range(0,tsize+1):
                    for tsel in range(0,tsize+1):
                        if (tsel != tpos) or (tsel == 0):
                            file = self.Profile.GetBindFile('teamsel2', f'{tsize}{tpos}{tsel}.txt')
                            self.ts2CreateSet(tsize, tpos, tsel, file)

        ### Helpful Binds
        ResetFile.SetBind(self.Ctrls['QuitToDesktop']  .MakeFileKeyBind('quit'))
        ResetFile.SetBind(self.Ctrls['InviteTarget']   .MakeFileKeyBind('invite $target'))
        ResetFile.SetBind(self.Ctrls['FPSBindKey']     .MakeFileKeyBind('++showfps'))
        ResetFile.SetBind(self.Ctrls['NetgraphBindKey'].MakeFileKeyBind('++netgraph'))

    def AllBindFiles(self):
        files = [self.Profile.GetBindFile("teamsel", "reset.txt")]
        dirs  = ["teamsel", "teamsel2"]

        for i in (1,2,3,4,5,6,7,8):
            files.append(self.Profile.GetBindFile("teamsel", f"sel{i}.txt"))

        for tsize in 1,2,3,4,5,6,7,8:
            for tpos in range(0,tsize+1):
                for tsel in range(0,tsize+1):
                    if (tsel != tpos) or (tsel == 0):
                        files.append(self.Profile.GetBindFile('teamsel2', f'{tsize}{tpos}{tsel}.txt'))

        return {
            'files' : files,
            'dirs'  : dirs,
        }

    def formatTeamConfig(self, size, pos):
        sizetext = f"{size}-Man"
        postext = ", No Spot"
        if pos > 0   : postext = f", {ordinals[pos-1]} Spot"
        if size == 1 : sizetext = "Solo"; postext = ""
        if size == 2 : sizetext = "Duo"
        if size == 3 : sizetext = "Trio"
        return f"[{sizetext}{postext}]"

    def ts2CreateSet(self, tsize, tpos, tsel, file):
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
            if tsize == 2      : newpos = 0; newsel = 0
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

        'QuitToDesktop' : 'Quit to Desktop',
        'InviteTarget'  : 'Invite Target to Group',

        'FPSBindKey'      : "Toggle FPS Display",
        'NetgraphBindKey' : "Toggle Netgraph Display",
    })

    for i in range(1,9):
        UI.Labels[f'TeamSelect{i}'] = f"Select {ordinals[i-1]} Team Member / Pet"
