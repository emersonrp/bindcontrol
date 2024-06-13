import wx
import re
import UI
from BLF import BLF
from Help import HelpButton
from UI.KeySelectDialog import bcKeyButton

# Sandolphan / Khaiba's guide to these controls found at:
# https://guidescroll.com/2011/07/city-of-heroes-mastermind-numeric-keypad-pet-controls/
#
# Originally: https://web.archive.org/web/20120904222729/http://boards.cityofheroes.com/showthread.php?t=117256

from Page import Page
from UI.ControlGroup import ControlGroup

class Mastermind(Page):
    petCommandKeyDefinitions = (
            {
                'label'      : 'Select All Pets',
                'ctrlName'      : 'PetSelectAll',
                'tooltipdetail' : 'select all of your pets',
            },
            {
                'label'      : 'Select Minions',
                'ctrlName'      : 'PetSelectMinions',
                'tooltipdetail' : 'select your "minion" pets',
            },
            {
                'label'      : 'Select Lieutenants',
                'ctrlName'      : 'PetSelectLieutenants',
                'tooltipdetail' : 'select your "lieutenant" pets',
            },
            {
                'label'      : 'Select Boss',
                'ctrlName'      : 'PetSelectBoss',
                'tooltipdetail' : 'select your "boss" pet',
            },
            {
                'label'      : 'Aggressive',
                'ctrlName'      : 'PetAggressive',
                'tooltipdetail' : 'set your selected pets to "Aggressive" mode',
            },
            {
                'label'      : 'Defensive',
                'ctrlName'      : 'PetDefensive',
                'tooltipdetail' : 'set your selected pets to "Defensive" mode',
            },
            {
                'label'      : 'Passive',
                'ctrlName'      : 'PetPassive',
                'tooltipdetail' : 'set your selected pets to "Passive" mode',
            },
            {
                'label'      : 'Attack',
                'ctrlName'      : 'PetAttack',
                'tooltipdetail' : 'order your selected pets to Attack your target',
            },
            {
                'label'      : 'Follow',
                'ctrlName'      : 'PetFollow',
                'tooltipdetail' : 'order your selected pets to Follow you',
            },
            {
                'label'      : 'Go To',
                'ctrlName'      : 'PetGoto',
                'tooltipdetail' : 'order your selected pets to Go To a targeted location',
            },
            {
                'label'      : 'Stay',
                'ctrlName'      : 'PetStay',
                'tooltipdetail' : 'order your selected pets to Stay at their current location',
            },
        )

    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Init = {
            'Enable' : False,

            'PetSelectAll' : 'NUMPAD0',
            'PetSelectAllResponse' : 'Orders?',
            'PetSelectAllResponseMethod' : 'Petsay',

            'PetSelectMinions' : 'NUMPAD1',
            'PetSelectMinionsResponse' : 'Orders?',
            'PetSelectMinionsResponseMethod' : 'Petsay',

            'PetSelectLieutenants' : 'NUMPAD2',
            'PetSelectLieutenantsResponse' : 'Orders?',
            'PetSelectLieutenantsResponseMethod' : 'Petsay',

            'PetSelectBoss' : 'NUMPAD3',
            'PetSelectBossResponse' : 'Orders?',
            'PetSelectBossResponseMethod' : 'Petsay',

            'PetBodyguard' : 'MULTIPLY',
            'PetBodyguardResponse' : 'Bodyguarding.',
            'PetBodyguardResponseMethod' : 'Petsay',

            'PetAggressive' : 'NUMPAD4',
            'PetAggressiveResponse' : 'Kill on Sight.',
            'PetAggressiveResponseMethod' : 'Petsay',

            'PetDefensive' : 'NUMPAD5',
            'PetDefensiveResponse' : 'Return Fire Only.',
            'PetDefensiveResponseMethod' : 'Petsay',

            'PetPassive' : 'NUMPAD6',
            'PetPassiveResponse' : 'At Ease.',
            'PetPassiveResponseMethod' : 'Petsay',

            'PetAttack' : 'NUMPAD7',
            'PetAttackResponse' : 'Open Fire!',
            'PetAttackResponseMethod' : 'Petsay',

            'PetFollow' : 'NUMPAD8',
            'PetFollowResponse' : 'Falling In.',
            'PetFollowResponseMethod' : 'Petsay',

            'PetGoto' : 'NUMPAD9',
            'PetGotoResponse' : 'Moving to Checkpoint.',
            'PetGotoResponseMethod' : 'Petsay',

            'PetStay' : 'DIVIDE',
            'PetStayResponse' : 'Holding this Position.',
            'PetStayResponseMethod' : 'Petsay',

            'PetBodyguardEnabled' : False,
            'PetBodyguardAttackEnabled' : False,
            'PetBodyguardGotoEnabled' : False,
            'PetBodyguardAttack' : '',
            'PetBodyguardGoto' : '',

            'PetCmdEnable': False,

            'PetChatToggle' : 'LALT+M',
            'PetSelect1' : 'F1',
            'PetSelect2' : 'F2',
            'PetSelect3' : 'F3',
            'PetSelect4' : 'F4',
            'PetSelect5' : 'F5',
            'PetSelect6' : 'F6',

            'Pet1Name' : 'Soldier',
            'Pet2Name' : 'Grunt',
            'Pet3Name' : 'Medic',
            'Pet4Name' : 'Spy',
            'Pet5Name' : 'Spec Ops',
            'Pet6Name' : 'Commando',

            'Pet1Bodyguard' : 0,
            'Pet2Bodyguard' : 0,
            'Pet3Bodyguard' : 0,
            'Pet4Bodyguard' : 0,
            'Pet5Bodyguard' : 0,
            'Pet6Bodyguard' : 0,

            'PetNPEnable'   : False,
            'SelNextPet'  : '',
            'SelPrevPet'  : '',
            'IncPetSize'  : '',
            'DecPetSize'  : '',
        }
        self.MMPowerSets = {
            "Beast Mastery"   : { 'min' : 'wol',  'lts' : 'lio',  'bos' : 'dir',  },
            "Demon Summoning" : { 'min' : 'lin',  'lts' : 'mons', 'bos' : 'pri',  },
            "Mercenaries"     : { 'min' : "sol",  'lts' : "spec", 'bos' : "com",  },
            "Necromancy"      : { 'min' : "zom",  'lts' : "grav", 'bos' : "lich", },
            "Ninjas"          : { 'min' : "gen",  'lts' : "joun", 'bos' : "oni",  },
            "Robotics"        : { 'min' : "dron", 'lts' : "prot", 'bos' : "ass",  },
            "Thugs"           : { 'min' : "thu",  'lts' : "enf",  'bos' : "bru",  },
        }
        self.TabTitle = "Mastermind / Pet Binds"

    def BuildPage(self):

        sizer = wx.BoxSizer(wx.VERTICAL)

        petcmdenablesizer = wx.BoxSizer(wx.HORIZONTAL)
        petcmdenable = wx.CheckBox( self, -1, 'Enable Pet Action Binds')
        petcmdenable.SetToolTip( wx.ToolTip('Check this to enable the Mastermind Pet Action Binds') )
        petcmdenable.Bind(wx.EVT_CHECKBOX, self.OnPetCmdEnable)
        self.Ctrls['PetCmdEnable'] = petcmdenable
        petcmdenable.SetValue(self.Init['PetCmdEnable'])
        petcmdhelpbutton = HelpButton(self, 'PetActionBinds.html')
        petcmdenablesizer.Add(petcmdenable, 0, wx.ALIGN_CENTER_VERTICAL)
        petcmdenablesizer.Add(petcmdhelpbutton, 0)

        # Iterate the data structure at the top and make the grid of controls for the basic pet binds
        petCommandsKeys = ControlGroup(self, self, width = 5, label = "Pet Action Binds", flexcols = [4])
        for command in self.petCommandKeyDefinitions:
            petCommandsKeys.AddControl(
                ctlName = command['ctrlName'],
                ctlType = 'keybutton',
                tooltip = "Choose the key combo that will " + command['tooltipdetail'],
            )
            petCommandsKeys.AddControl(
                ctlName = command['ctrlName'] + 'ResponseMethod',
                ctlType = 'combobox',
                contents = [ "Local", "Self-tell", "Petsay", "---", ],
                tooltip = "Choose how your pets will respond when they are in chatty mode and you " + command['tooltipdetail'],
            )
            petCommandsKeys.AddControl(
                noLabel = True,
                ctlName = command['ctrlName'] + "Response",
                ctlType = "text",
                tooltip = "Choose the chat response your pets give when you " + command['tooltipdetail'],
            )
        petCommandsKeys.AddControl(
            ctlName = 'PetChatToggle',
            ctlType = 'keybutton',
            tooltip = 'Choose the key combo that will toggle your pet\'s Chatty Mode',
        )

        ### Bodyguard mode controls packed into the spacer differently
        for i in [1,2,3,4]:
            petCommandsKeys.AddControl( ctlName = f'spacer{i}', ctlType = 'statictext', noLabel = True,)

        bgCB = petCommandsKeys.AddControl(
            noLabel  = True,
            ctlName  = 'PetBodyguardEnabled',
            ctlType  = 'checkbox',
            contents = 'Enable Bodyguard Mode Binds',
            tooltip  = 'Check this to enable the Bodyguard Mode Binds',
        )
        bgCB.Bind(wx.EVT_CHECKBOX, self.OnBGCheckboxes)

        petCommandsKeys.AddControl( ctlName = f'spacer5', ctlType = 'statictext', noLabel = True,)

        staticbox = petCommandsKeys.GetStaticBox()
        bgSelectText = wx.StaticText(staticbox, label = "Select Bodyguard Pets:")
        petCommandsKeys.InnerSizer.Add(bgSelectText, 1, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        bgsizer = wx.BoxSizer(wx.HORIZONTAL)
        petcbs = []
        for PetID in [1,2,3,4,5,6]:
            petcb = wx.CheckBox(staticbox, -1, str(PetID))
            petcbs.append(petcb)
            self.Ctrls[f"Pet{PetID}Bodyguard"] = petcb
            setattr(petcb, "CtlLabel", bgSelectText)
            petcb.SetToolTip(f"Select whether pet {PetID} acts as Bodyguard")
            bgsizer.Add(petcb, 0, wx.LEFT|wx.RIGHT, 5)

        petCommandsKeys.InnerSizer.Add(bgsizer, 1, wx.ALIGN_CENTER_VERTICAL)


        petCommandsKeys.AddControl(
            ctlType = 'keybutton',
            ctlName = 'PetBodyguard',
            tooltip = 'Choose the key combo that will put your designated pets into Bodyguard mode, while still commanding the others',
        )
        petCommandsKeys.AddControl(
            ctlName = 'PetBodyguardResponseMethod',
            ctlType = 'combobox',
            contents = [ "Local", "Self-tell", "Petsay", "---", ],
            tooltip = "Choose how your pets will respond when they are in chatty mode and you put your designated pets into Bodyguard mode, while still commanding the others",
        )
        petCommandsKeys.AddControl(
            noLabel = True,
            ctlName = "PetBodyguardResponse",
            ctlType = "text",
            tooltip = "Choose the chat response your pets give when you put your designated pets into Bodyguard mode, while still commanding the others",
        )
        # BGAttack and BGGoto formatted differently
        petCommandsKeys.AddControl(
            ctlName = 'PetBodyguardAttack',
            ctlType = 'keybutton',
            tooltip = "Choose the key combo that will command your bodyguards to attack your target",
        )
        enableBGAttack = wx.CheckBox(staticbox, -1, "Enable")
        enableBGAttack.Bind(wx.EVT_CHECKBOX, self.OnBGCheckboxes)
        enableBGAttack.SetValue(self.Init['PetBodyguardAttackEnabled'])
        setattr(enableBGAttack, "CtlLabel", None)
        self.Ctrls['PetBodyguardAttackEnabled'] = enableBGAttack
        petCommandsKeys.InnerSizer.Add(enableBGAttack, 0, wx.ALL|wx.EXPAND, 5)
        petCommandsKeys.InnerSizer.Add(wx.StaticText(staticbox, -1, ''))
        petCommandsKeys.InnerSizer.Add(wx.StaticText(staticbox, -1, ''))

        petCommandsKeys.AddControl(
            ctlName = 'PetBodyguardGoto',
            ctlType = 'keybutton',
            tooltip = "Choose the key combo that will command your bodyguards to go to a targeted location",
        )
        enableBGGoto = wx.CheckBox(petCommandsKeys.GetStaticBox(), -1, "Enable")
        enableBGGoto.Bind(wx.EVT_CHECKBOX, self.OnBGCheckboxes)
        enableBGGoto.SetValue(self.Init['PetBodyguardGotoEnabled'])
        setattr(enableBGGoto, "CtlLabel", None)
        self.Ctrls['PetBodyguardGotoEnabled'] = enableBGGoto
        petCommandsKeys.InnerSizer.Add(enableBGGoto, 0, wx.ALL|wx.EXPAND, 5)


        petselenable = wx.CheckBox( self, -1, 'Enable Pet By-Name Binds')
        petselenable.SetToolTip( wx.ToolTip('Check this to enable the By-Name Selection Binds') )
        petselenable.Bind(wx.EVT_CHECKBOX, self.OnPetSelEnable)

        self.Ctrls['PetSelEnable'] = petselenable

        # get the pet names and binds to select them directly
        PetNames  = wx.StaticBoxSizer(wx.HORIZONTAL, self, label = "Pet Names and By-Name Keybinds")
        PetInner = wx.GridBagSizer(hgap = 5, vgap = 5)
        PetNames.Add(PetInner, 1, wx.ALL|wx.EXPAND, 10)
        self.PetNameLabel = wx.StaticText(self, label = "Pet Name:")
        self.PetKeyLabel  = wx.StaticText(self, label = "Select Key:")
        PetInner.Add(self.PetNameLabel, (1,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        PetInner.Add(self.PetKeyLabel,  (2,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        for i in (1,2,3,4,5,6):
            label = wx.StaticText(self, label = f'Pet {i}')
            button = bcKeyButton(self, -1, init = {
                'CtlName'  : f'PetSelect{i}',
                'CtlLabel' : label,
                'Key'      : self.Init[f'PetSelect{i}'],
            })
            self.Ctrls[f'PetSelect{i}'] = button
            name = wx.TextCtrl(self)
            name.Bind(wx.EVT_TEXT, self.OnNameTextChange)
            setattr(name, "CtlLabel", None)
            self.Ctrls[f'Pet{i}Name'] = name

            PetInner.Add(label,  (0,i), flag=wx.EXPAND|wx.ALIGN_CENTER)
            PetInner.Add(name,   (1,i), flag=wx.EXPAND)
            PetInner.Add(button, (2,i), flag=wx.EXPAND)
            PetInner.AddGrowableCol(i)

        # Pet Next/Prev select binds
        petnpenablesizer = wx.BoxSizer(wx.HORIZONTAL)
        petnpenable = wx.CheckBox( self, -1, 'Enable Single Key Pet Select Binds')
        petnpenable.SetToolTip( wx.ToolTip('Check this to enable the Single Key Pet Select Binds') )
        petnpenable.Bind(wx.EVT_CHECKBOX, self.OnPetNPEnable)
        self.Ctrls['PetNPEnable'] = petnpenable
        petnpenable.SetValue(self.Init['PetNPEnable'])
        petnphelpbutton = HelpButton(self, 'PetOneKeyBinds.html')
        petnpenablesizer.Add(petnpenable, 0, wx.ALIGN_CENTER_VERTICAL)
        petnpenablesizer.Add(petnphelpbutton, 0)

        PetSelBox = ControlGroup(self, self, label="Single Key Pet Select Binds", width=8, flexcols=[1,3,5,7])
        for b in (
            ['SelNextPet', 'Choose the key that will select the next pet from the currently selected one'],
            ['SelPrevPet', 'Choose the key that will select the previous pet from the currently selected one'],
            ['IncPetSize', 'Choose the key that will increase the size of your pet/henchman group rotation'],
            ['DecPetSize', 'Choose the key that will decrease the size of your pet/henchman group rotation'],
        ):
            PetSelBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        # Bring it all together
        sizer.Add(petcmdenablesizer, 0, wx.EXPAND|wx.TOP|wx.LEFT, 16)
        sizer.Add(petCommandsKeys, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 16)
        sizer.AddSpacer(10)
        sizer.Add(petselenable, 0, wx.EXPAND|wx.ALL, 16)
        sizer.Add(PetNames, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 16)

        sizer.Add(petnpenablesizer, 0, wx.EXPAND|wx.ALL, 16)
        sizer.Add(PetSelBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 16)

        self.SynchronizeUI()

        self.SetSizerAndFit(sizer)

    def SynchronizeUI(self):
        arch = self.Profile.General.GetState('Archetype')
        pset = self.Profile.General.GetState('Primary')

        for _, control in self.Ctrls.items():
            control.Enable(bool(arch == "Mastermind" and pset))
        self.PetNameLabel.Enable(bool(arch == "Mastermind" and pset))
        self.PetKeyLabel .Enable(bool(arch == "Mastermind" and pset))
        self.OnPetCmdEnable()
        self.OnPetSelEnable()
        self.OnPetNPEnable()

    def OnPetCmdEnable(self, evt = None):
        self.Freeze()
        enabled = self.GetState('PetCmdEnable')
        for command in self.petCommandKeyDefinitions:
            self.EnableControls(enabled, [
                command['ctrlName'], command['ctrlName']+"ResponseMethod", command['ctrlName']+"Response"
            ])
        self.EnableControls(enabled,
            [ 'PetChatToggle', 'PetBodyguard',
             'PetBodyguardResponseMethod', 'PetBodyguardResponse', 'PetBodyguardAttack',
             'PetBodyguardAttackEnabled', 'PetBodyguardGoto', 'PetBodyguardGotoEnabled' ])
        self.OnBGCheckboxes()
        self.Thaw()
        if evt: evt.Skip()

    def OnPetSelEnable(self, evt = None):
        enabled = bool(self.GetState('PetSelEnable'))
        for i in [1,2,3,4,5,6]:
            self.EnableControls(enabled, [ f"Pet{i}Name", f"PetSelect{i}" ])
        self.PetNameLabel.Enable(enabled)
        self.PetKeyLabel .Enable(enabled)

        self.OnBGCheckboxes()
        if evt: evt.Skip()

    def OnPetNPEnable(self, evt = None):
        enabled = bool(self.GetState('PetNPEnable'))
        self.EnableControls(enabled, ['SelNextPet', 'SelPrevPet', 'IncPetSize', 'DecPetSize'])
        if evt: evt.Skip()

    def OnNameTextChange(self, evt):
        ctrl = evt.EventObject
        if re.search(' ', ctrl.GetValue()):
            ctrl.SetBackgroundColour([255,200,200])
            ctrl.SetToolTip("This pet name contains spaces, which will cause this pet's by-name binds not to work.  Change your pet's name to something without spaces.")
        else:
            ctrl.SetBackgroundColour(wx.NullColour)
            ctrl.SetToolTip('')

    def OnBGCheckboxes(self, evt = None):
        petcmdenabled = self.GetState('PetCmdEnable')

        bgEnabled = self.GetState('PetBodyguardEnabled')
        bgAttack  = self.GetState('PetBodyguardAttackEnabled')
        bgGoto    = self.GetState('PetBodyguardGotoEnabled')

        for c in ['PetBodyguard','PetBodyguardResponseMethod','PetBodyguardResponse']:
            self.Ctrls[c].Enable(petcmdenabled and bgEnabled)

        self.Ctrls['PetBodyguardAttack'].Enable(petcmdenabled and bgEnabled and bgAttack)
        self.Ctrls['PetBodyguardGoto']  .Enable(petcmdenabled and bgEnabled and bgGoto)

        self.Ctrls['PetBodyguardAttackEnabled'].Enable(petcmdenabled and bgEnabled)
        self.Ctrls['PetBodyguardGotoEnabled']  .Enable(petcmdenabled and bgEnabled)

        for petid in [1,2,3,4,5,6]:
            self.Ctrls[f"Pet{petid}Bodyguard"].Enable(petcmdenabled and bgEnabled)
        if evt: evt.Skip()

    ### BIND CREATION METHODS
    def mmBGSelBind(self, profile, file, PetBodyguardResponse, powers):
        bgset = []
        bgsay = []
        method = self.GetChatMethod(f"PetBodyguardResponseMethod")
        if (self.GetState('PetBodyguardEnabled')):
            (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()

            #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
            if (((tier1bg + tier2bg + tier3bg) == 6)):
                bgsay = [method + PetBodyguardResponse]
            else:
                if (tier1bg == 3):
                    if re.match('petsay', method): method = f"petsaypow {powers['min']} "
                    bgsay.append(method + PetBodyguardResponse)
                else:
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.GetState('Pet1Bodyguard')) :
                        if re.match('petsay', method):
                            method = f"petsayname {self.GetState('Pet1Name')} "
                        bgsay.append(method + PetBodyguardResponse)
                    if (self.GetState('Pet2Bodyguard')) :
                        if re.match('petsay', method):
                            method = f"petsayname {self.GetState('Pet2Name')} "
                        bgsay.append(method + PetBodyguardResponse)
                    if (self.GetState('Pet3Bodyguard')) :
                        if re.match('petsay', method):
                            method = f"petsayname {self.GetState('Pet3Name')} "
                        bgsay.append(method + PetBodyguardResponse)

                if (tier2bg == 2):
                    if re.match('petsay', method): method = f"petsaypow {powers['lts']} "
                    bgsay.append(method + PetBodyguardResponse)
                else:
                    if (self.GetState('Pet4Bodyguard')) :
                        if re.match('petsay', method):
                            method = f"petsayname {self.GetState('Pet4Name')} "
                        bgsay.append(method + PetBodyguardResponse)
                    if (self.GetState('Pet5Bodyguard')) :
                        if re.match('petsay', method):
                            method = f"petsayname {self.GetState('Pet5Name')} "
                        bgsay.append(method + PetBodyguardResponse)

                if (tier3bg == 1):
                    if re.match('petsay', method): method = f"petsaypow {powers['bos']} "
                    bgsay.append(method + PetBodyguardResponse)

            if ((tier1bg + tier2bg + tier3bg) == 6):
                bgset = ['petcomall def fol']
            else:
                if (tier1bg == 3):
                    bgset.append(f"petcompow {powers['min']} def fol")
                else:
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.GetState('Pet1Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet1Name')} def fol")
                    if (self.GetState('Pet2Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet2Name')} def fol")
                    if (self.GetState('Pet3Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet3Name')} def fol")

                if (tier2bg == 2):
                    bgset.append(f"petcompow {powers['lts']} def fol")
                else:
                    if (self.GetState('Pet4Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet4Name')} def fol")
                    if (self.GetState('Pet5Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet5Name')} def fol")

                if (tier3bg == 1):
                    bgset.append(f"petcompow {powers['bos']} def fol")

            keyBindContents = bgsay + bgset + [profile.GetBindFile('mmbinds','cbguarda.txt').BLF()]
            file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(keyBindContents))

    def mmBGActBind(self, _, filedn, fileup, action, say, powers):

        key    = self.GetState(f"Pet{action}")
        name   = UI.Labels[f"Pet{action}"]
        method = self.GetChatMethod(f"Pet{action}ResponseMethod")

        bgact = []
        bgsay = []
        (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if (((tier1bg + tier2bg + tier3bg) == 0) or method == 'petsayall'):
            method = self.GetChatMethod(f"Pet{action}ResponseMethod")
            bgsay = [method + say]
        else:
            if (tier1bg == 0):
                if re.match('petsay', method): method = f"petsaypow {powers['min']} "
                bgsay.append(f"{method} {say}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.GetState('Pet1Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet1Name')} "
                    bgsay.append(f"{method}{say}")
                if (not self.GetState('Pet2Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet2Name')} "
                    bgsay.append(f"{method}{say}")
                if (not self.GetState('Pet3Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet3Name')} "
                    bgsay.append(f"{method}{say}")

            if (tier2bg == 0):
                if re.match('petsay', method): method = f"petsaypow {powers['lts']} "
                bgsay.append(f"{method} {say}")
            else :
                if (not self.GetState('Pet4Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet4Name')} "
                    bgsay.append(f"{method}{say}")
                if (not self.GetState('Pet5Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet5Name')} "
                    bgsay.append(f"{method}{say}")

            if (tier3bg == 0):
                if re.match('petsay', method): method = f"petsaypow {powers['bos']} "
                bgsay.append(f"{method}{say}")

        if ((tier1bg + tier2bg + tier3bg) == 0):
            bgact = ['petcomall ' + action]
        else :
            if (tier1bg == 0):
                bgact.append(f"petcompow {powers['min']} {action}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.GetState('Pet1Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet1Name')} {action}")
                if (not self.GetState('Pet2Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet2Name')} {action}")
                if (not self.GetState('Pet3Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet3Name')} {action}")

            if (tier2bg == 0):
                bgact.append(f"petcompow {powers['lts']} {action}")
            else :
                if (not self.GetState('Pet4Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet4Name')} {action}")
                if (not self.GetState('Pet5Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet5Name')} {action}")

            if (tier3bg == 0):
                bgact.append('petcompow ' + f"{powers['bos']} {action}")

        filedn.SetBind(key, name, self, ["+ $$"] + bgsay + [fileup.BLF()])
        fileup.SetBind(key, name, self, ["- $$"] + bgact + [filedn.BLF()])

    def mmBGActBGBind(self, _, filedn, fileup, action, say, powers):
        key =    self.GetState(f"PetBodyguard{action}")
        name = UI.Labels[f"PetBodyguard{action}"]
        method = self.GetChatMethod(f"Pet{action}ResponseMethod")

        bgact = []
        bgsay = []
        (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if (((tier1bg + tier2bg + tier3bg) == 6)):
            bgsay = [method + say]
        else :
            if (tier1bg == 3):
                if re.match('petsay', method): method = f"petsaypow {powers['min']} "
                bgsay.append(f"{method} {say}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (self.GetState('Pet1Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet1Name')} "
                    bgsay.append(f"{method}{say}")
                if (self.GetState('Pet2Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet2Name')} "
                    bgsay.append(f"{method}{say}")
                if (self.GetState('Pet3Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet3Name')} "
                    bgsay.append(f"{method}{say}")

            if (tier2bg == 2):
                if re.match('petsay', method): method = f"petsaypow {powers['lts']} "
                bgsay.append(f"{method} {say}")
            else :
                if (self.GetState('Pet4Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet4Name')} "
                    bgsay.append(f"{method}{say}")
                if (self.GetState('Pet5Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.GetState('Pet5Name')} "
                    bgsay.append(f"{method}{say}")

            if (tier3bg == 1):
                if re.match('petsay', method): method = f"petsaypow {powers['bos']} "
                bgsay.append(f"{method}{say}")

        if ((tier1bg + tier2bg + tier3bg) == 6):
            bgact = ['petcomall ' + action]
        else :
            if (tier1bg == 3):
                bgact.append(f"petcompow {powers['min']} {action}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (self.GetState('Pet1Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet1Name')} {action}")
                if (self.GetState('Pet2Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet2Name')} {action}")
                if (self.GetState('Pet3Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet3Name')} {action}")

            if (tier2bg == 2):
                bgact.append(f"petcompow {powers['lts']} {action}")
            else :
                if (self.GetState('Pet4Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet4Name')} {action}")
                if (self.GetState('Pet5Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet5Name')} {action}")

            if (tier3bg == 1):
                bgact.append(f"petcompow {powers['bos']} {action}")

        # file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(bgsay.$bgset.BindFile.BLF($profile, 'mmbinds','\mmbinds\\cbguarda.txt')))
        filedn.SetBind(key, name, self, ["+ $$"] + bgsay + [fileup.BLF()])
        fileup.SetBind(key, name, self, ["- $$"] + bgact + [filedn.BLF()])

    def mmQuietBGSelBind(self, profile, file, powers):
        if (self.GetState('PetBodyguardEnabled')):
            bgset = []
            (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
            #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
            if ((tier1bg + tier2bg + tier3bg) == 6):
                bgset = ["petcomall def fol"]
            else :
                if (tier1bg == 3):
                    bgset.append(f"petcompow {powers['min']} def fol")
                else :
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.GetState('Pet1Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet1Name')} def fol")
                    if (self.GetState('Pet2Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet2Name')} def fol")
                    if (self.GetState('Pet3Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet3Name')} def fol")

                if (tier2bg == 2):
                    bgset.append(f"petcompow {powers['lts']} def fol")
                else :
                    if (self.GetState('Pet4Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet4Name')} def fol")
                    if (self.GetState('Pet5Bodyguard')) : bgset.append(f"petcomname {self.GetState('Pet5Name')} def fol")

                if (tier3bg == 1):
                    bgset.append(f"petcompow {powers['bos']} def fol")

            file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(bgset + [profile.GetBindFile('mmbinds','bguarda.txt').BLF()]))

    def mmQuietBGActBind(self, _, filedn, __, action, powers):

        key = self.GetState(f"Pet{action}")
        name = UI.Labels[f"Pet{action}"]

        bgact = []
        (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if ((tier1bg + tier2bg + tier3bg) == 0):
            bgact = [f"petcomall {action}"]
        else :
            if (tier1bg == 0):
                bgact.append(f"petcompow {powers['min']} {action}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.GetState('Pet1Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet1Name')} {action}")
                if (not self.GetState('Pet2Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet2Name')} {action}")
                if (not self.GetState('Pet3Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet3Name')} {action}")

            if (tier2bg == 0):
                bgact.append(f"petcompow {powers['lts']} {action}")
            else :
                if (not self.GetState('Pet4Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet4Name')} {action}")
                if (not self.GetState('Pet5Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet5Name')} {action}")

            if (tier3bg == 0): bgact.append(f"petcompow {powers['bos']} {action}")

        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(key, name, self, bgact)

    def mmQuietBGActBGBind(self, _, filedn, __, action, powers):

        key  = self.GetState(f"PetBodyguard{action}")
        name = UI.Labels[f"PetBodyguard{action}"]

        bgact = []
        (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if ((tier1bg + tier2bg + tier3bg) == 6):
            bgact = [f"petcomall {action}"]
        else :
            if (tier1bg == 3):
                bgact.append(f"petcompow {powers['min']} {action}")
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (self.GetState('Pet1Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet1Name')} {action}")
                if (self.GetState('Pet2Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet2Name')} {action}")
                if (self.GetState('Pet3Bodyguard')): bgact.append(f"petcomname {self.GetState('Pet3Name')} {action}")

            if (tier2bg == 2):
                bgact.append(f"petcompow  {powers['lts']} {action}")
            else :
                if (self.GetState('Pet4Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet4Name')} {action}")
                if (self.GetState('Pet5Bodyguard')) : bgact.append(f"petcomname {self.GetState('Pet5Name')} {action}")

            if (tier3bg == 1) : bgact.append(f"petcompow {powers['bos']} {action}")

        if not bgact: return
        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(key, name, self, bgact)

    def mmSubBind(self, profile, file, fn, grp, powers):
        PetResponses = {}
        for cmd in ('SelectAll', 'SelectMinions', 'SelectLieutenants', 'SelectBoss',
                'Aggressive', 'Defensive', 'Passive', 'Attack', 'Follow', 'Goto', 'Stay','Bodyguard',):
            PetResponses[cmd] = ''
            if self.GetChatMethod(f"Pet{cmd}ResponseMethod") : PetResponses[cmd] = self.GetState(f"Pet{cmd}Response")

        file.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind([
            self.GetChatMethod('PetSelectAllResponseMethod') + f"{PetResponses['SelectAll']}", profile.GetBindFile('mmbinds','call.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind([
            self.GetChatMethod('PetSelectMinionsResponseMethod', 'min') + f"{PetResponses['SelectMinions']}", profile.GetBindFile('mmbinds','ctier1.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind([
            self.GetChatMethod('PetSelectLieutenantsResponseMethod', 'lts') + f"{PetResponses['SelectLieutenants']}", profile.GetBindFile('mmbinds','ctier2.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind([
            self.GetChatMethod('PetSelectBossResponseMethod', 'bos') + f"{PetResponses['SelectBoss']}", profile.GetBindFile('mmbinds','ctier3.txt').BLF()]))

        self.mmBGSelBind(profile,file,PetResponses['Bodyguard'],powers)

        if grp: petcom = f"$$petcompow {grp}"
        else:   petcom =  "$$petcomall"
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(self.GetChatMethod(f"Pet{cmd}ResponseMethod") + f"{PetResponses[cmd]}{petcom} {cmd}"))

        if (self.GetState('PetBodyguardAttackEnabled'))  : file.SetBind(self.Ctrls['PetBodyguardAttack'].MakeFileKeyBind('nop'))
        if (self.GetState('PetBodyguardGotoEnabled'))    : file.SetBind(self.Ctrls['PetBodyguardGoto'].MakeFileKeyBind('nop'))
        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.GetBindFile('mmbinds',f"{fn}.txt").BLF()]))

    def mmBGSubBind(self, profile, filedn, fileup, fn, powers):
        PetResponses = {}
        for cmd in ('SelectAll','SelectMinions','SelectLieutenants','SelectBoss','Aggressive','Defensive','Passive','Attack','Follow','Goto', 'Stay', 'Bodyguard',):
            PetResponses[cmd] = ''
            if self.GetChatMethod(f'Pet{cmd}ResponseMethod') : PetResponses[cmd] = self.GetState(f'Pet{cmd}Response')

        filedn.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind(
            [self.GetChatMethod('PetSelectAllResponseMethod') + f"{PetResponses['SelectAll']}", profile.GetBindFile('mmbinds','call.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind(
            [self.GetChatMethod('PetSelectMinionsResponseMethod', 'min') + f"{PetResponses['SelectMinions']}", profile.GetBindFile('mmbinds','ctier1.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(
            [self.GetChatMethod('PetSelectLieutenantsResponseMethod', 'lts') + f"{PetResponses['SelectLieutenants']}", profile.GetBindFile('mmbinds','ctier2.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind(
            [self.GetChatMethod('PetSelectBossResponseMethod', 'bos') + f"{PetResponses['SelectBoss']}", profile.GetBindFile('mmbinds','ctier3.txt').BLF()]))
        self.mmBGSelBind(profile,filedn,PetResponses['Bodyguard'],powers)

        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            self.mmBGActBind(profile, filedn, fileup, cmd, PetResponses[cmd], powers)

        if (self.GetState('PetBodyguardAttackEnabled')):
            self.mmBGActBGBind( profile, filedn, fileup,'Attack', PetResponses['Attack'], powers)

        if (self.GetState('PetBodyguardGotoEnabled')):
            self.mmBGActBGBind( profile, filedn, fileup,'Goto', PetResponses['Goto'], powers)

        filedn.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.GetBindFile('mmbinds',f"{fn}a.txt").BLF()]))

    def mmQuietSubBind(self, profile, file, fn, grp, powers):
        file.SetBind(self.Ctrls['PetSelectAll']        .MakeFileKeyBind(profile.GetBindFile('mmbinds','all.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectMinions']    .MakeFileKeyBind(profile.GetBindFile('mmbinds','tier1.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier2.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectBoss']       .MakeFileKeyBind(profile.GetBindFile('mmbinds','tier3.txt').BLF()))
        self.mmQuietBGSelBind(profile, file, powers)

        if grp: petcom = f"petcompow {grp}"
        else:   petcom =  'petcomall'
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(f"{petcom} {cmd}"))

        if (self.GetState('PetBodyguardAttackEnabled'))  : file.SetBind(self.Ctrls['PetBodyguardAttack'].MakeFileKeyBind('nop'))
        if (self.GetState('PetBodyguardGotoEnabled'))    : file.SetBind(self.Ctrls['PetBodyguardGoto'].MakeFileKeyBind('nop'))

        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Chatty Mode', profile.GetBindFile('mmbinds','c' + fn + '.txt').BLF()]))

    def mmQuietBGSubBind(self, profile, filedn, fileup, fn, powers):
        filedn.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind(profile.GetBindFile('mmbinds','all.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier1.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier2.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier3.txt').BLF()))

        self.mmQuietBGSelBind(profile,filedn,powers)

        for cmd in ('Aggressive','Defensive','Passive', 'Attack', 'Follow','Stay', 'Goto'):
            self.mmQuietBGActBind(profile, filedn, fileup, cmd, powers)

        if (self.GetState('PetBodyguardAttackEnabled')):
            self.mmQuietBGActBGBind(profile, filedn, fileup,'Attack', powers)

        if (self.GetState('PetBodyguardGotoEnabled')):
            self.mmQuietBGActBGBind(profile, filedn, fileup,'Goto', powers)

        filedn.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Chatty Mode', profile.GetBindFile('mmbinds','c' + fn + 'a.txt').BLF()]))

    def PopulateBindFiles(self):

        profile = self.Profile
        ResetFile = profile.ResetFile()

        if self.GetState('PetCmdEnable'):
            powers = self.MMPowerSets[ profile.General.GetState('Primary') ]

            #### "Quiet" versions
            allfile = profile.GetBindFile('mmbinds','all.txt')
            minfile = profile.GetBindFile('mmbinds','tier1.txt')
            ltsfile = profile.GetBindFile('mmbinds','tier2.txt')
            bosfile = profile.GetBindFile('mmbinds','tier3.txt')

            self.mmSubBind(profile      , ResetFile   , "all"    , None          , powers)
            self.mmQuietSubBind(profile , allfile     , "all"    , None          , powers)
            self.mmQuietSubBind(profile , minfile     , "tier1"  , powers['min'] , powers)
            self.mmQuietSubBind(profile , ltsfile     , "tier2"  , powers['lts'] , powers)
            self.mmQuietSubBind(profile , bosfile     , "tier3"  , powers['bos'] , powers)
            if (self.GetState('PetBodyguardEnabled')):
                # citybinder had this commented out, and the file was empty if created
                # bgfileup = profile.GetBindFile('mmbinds','bguardb.txt')
                bgfiledn = profile.GetBindFile('mmbinds','bguarda.txt')
                self.mmQuietBGSubBind(profile,bgfiledn,None,"bguard",powers)

            #### "Chatty" versions
            callfile = profile.GetBindFile('mmbinds','call.txt')
            cminfile = profile.GetBindFile('mmbinds','ctier1.txt')
            cltsfile = profile.GetBindFile('mmbinds','ctier2.txt')
            cbosfile = profile.GetBindFile('mmbinds','ctier3.txt')

            self.mmSubBind(profile , callfile , "all"   , None          , powers)
            self.mmSubBind(profile , cminfile , "tier1" , powers['min'] , powers)
            self.mmSubBind(profile , cltsfile , "tier2" , powers['lts'] , powers)
            self.mmSubBind(profile , cbosfile , "tier3" , powers['bos'] , powers)
            if (self.GetState('PetBodyguardEnabled')):
                cbgfiledn = profile.GetBindFile('mmbinds','cbguarda.txt')
                cbgfileup = profile.GetBindFile('mmbinds','cbguardb.txt')
                self.mmBGSubBind(profile,cbgfiledn,cbgfileup,"bguard",powers)

        if self.GetState('PetSelEnable'):
            for i in [1,2,3,4,5,6]:
                name = self.GetState(f"Pet{i}Name")
                ResetFile.SetBind(
                    self.Ctrls[f"PetSelect{i}"].MakeFileKeyBind(f"petselectname {name}")
                )
        #
        # Prev / next pet binds
        if self.GetState('PetNPEnable'):
            self.psCreateSet(1,0,self.Profile.ResetFile())
            for tsize in 1,2,3,4,5,6:
                for tsel in range(0,tsize+1):
                    file = self.Profile.GetBindFile('petsel', f"{tsize}{tsel}.txt")
                    self.psCreateSet(tsize,tsel,file)

    def psCreateSet(self, tsize, tsel, file):
        # tsize is the size of the team at the moment
        # tpos is the position of the player at the moment, or 0 if unknown
        # tsel is the currently selected team member as far as the bind knows, or 0 if unknown
        #file.SetBind(self.reset,'tell $name, Re-Loaded Single Key Team Select Bind.$${BLF()} {self.Profile.GameBindsDir()}\\petsel\\10.txt')
        if tsize < 6:
            file.SetBind(self.GetState('IncPetSize'), self, UI.Labels['IncPetSize'], f'tell $name, [{tsize+1} Pet]$${BLF()} {self.Profile.GameBindsDir()}\\petsel\\{tsize+1}{tsel}.txt')
        else:
            file.SetBind(self.GetState('IncPetSize'), self, UI.Labels['IncPetSize'], 'nop')
        if tsize == 1:
            file.SetBind(self.GetState('DecPetSize'), self, UI.Labels['DecPetSize'], 'nop')
            file.SetBind(self.GetState('SelNextPet'), self, UI.Labels['SelNextPet'], f'petselect 0$${BLF()} {self.Profile.GameBindsDir()}\\petsel\\{tsize}1.txt')
            file.SetBind(self.GetState('SelPrevPet'), self, UI.Labels['SelPrevPet'], f'petselect 0$${BLF()} {self.Profile.GameBindsDir()}\\petsel\\{tsize}1.txt')
        else:
            selnext,selprev = tsel+1,tsel-1
            if selnext > tsize : selnext = 1
            if selprev < 1 : selprev = tsize
            newsel = tsel
            if tsize-1 < tsel : newsel = tsize-1
            if tsize == 2 : newsel = 0
            file.SetBind(self.GetState('DecPetSize'), self, UI.Labels['DecPetSize'], f'tell $name, [{tsize-1} Pet]$${BLF()} {self.Profile.GameBindsDir()}\\petsel\\{tsize-1}{newsel}.txt')
            file.SetBind(self.GetState('SelNextPet'), self, UI.Labels['SelNextPet'], f'petselect {selnext-1}$${BLF()} {self.Profile.GameBindsDir()}\\petsel\\{tsize}{selnext}.txt')
            file.SetBind(self.GetState('SelPrevPet'), self, UI.Labels['SelPrevPet'], f'petselect {selprev-1}$${BLF()} {self.Profile.GameBindsDir()}\\petsel\\{tsize}{selprev}.txt')

    def GetChatMethod(self, control, target = 'all'):
        chatdesc = self.GetState(control)
        powers   = self.MMPowerSets[ self.Profile.General.GetState('Primary') ]
        # This is terrible, I accidentally optimized away the original way of doing this.
        if target == "all": petsay = "petsayall "
        else:               petsay = "petsaypow " + powers[target] + " "

        return {
            'Local'     : 'local ',
            'Self-tell' : 'tell $name, ',
            'Petsay'    : petsay,
            '---'       : '',
        }[chatdesc]

    def CountBodyguards(self):
        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are either All BG or all NBG.
        #  if tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  if tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  tier3bg is ALWAYS a full group, with only one member, it is either BG or NBG
        #  so, add all full groups into the bgsay command.
        tier1bg = tier2bg = tier3bg = 0
        if (self.GetState('Pet1Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet2Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet3Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet4Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet5Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet6Bodyguard')) : tier3bg = tier3bg + 1
        return (tier1bg, tier2bg, tier3bg)

    def AllBindFiles(self):
        files = []
        # not clear that all of these are used but let's be thorough
        for fn in [
            'all'     , 'tier1'    , 'tier2'   , 'tier3'   ,
            'alla'    , 'tier1a'   , 'tier2a'  , 'tier3a'  ,
            'call'    , 'ctier1'   , 'ctier2'  , 'ctier3'  ,
            'calla'   , 'ctier1a'  , 'ctier2a' , 'ctier3a' ,
            'bguarda' , 'cbguarda' ,
        ]:
            files.append(self.Profile.GetBindFile('mmbinds', f'{fn}.txt'))

        return {
            'files' : files,
            'dirs'  : ['mmbinds'],
        }


    for cmd in petCommandKeyDefinitions:
        UI.Labels[cmd['ctrlName']] = cmd['label']
    UI.Labels.update({
        'PetSelEnable'                       : "Enable By-Name Pet Selection",
        'Pet1Name'                           : "First Pet's Name",
        'Pet2Name'                           : "Second Pet's Name",
        'Pet3Name'                           : "Third Pet's Name",
        'Pet4Name'                           : "Fourth Pet's Name",
        'Pet5Name'                           : "Fifth Pet's Name",
        'Pet6Name'                           : "Sixth Pet's Name",
        'PetSelect1'                         : "Select First Pet",
        'PetSelect2'                         : "Select Second Pet",
        'PetSelect3'                         : "Select Third Pet",
        'PetSelect4'                         : "Select Fourth Pet",
        'PetSelect5'                         : "Select Fifth Pet",
        'PetSelect6'                         : "Select Sixth Pet",
        'PetSelectAllResponseMethod'         : "Pet Response",
        'PetSelectMinionsResponseMethod'     : "Pet Response",
        'PetSelectLieutenantsResponseMethod' : "Pet Response",
        'PetSelectBossResponseMethod'        : "Pet Response",
        'PetAggressiveResponseMethod'        : "Pet Response",
        'PetDefensiveResponseMethod'         : "Pet Response",
        'PetPassiveResponseMethod'           : "Pet Response",
        'PetAttackResponseMethod'            : "Pet Response",
        'PetFollowResponseMethod'            : "Pet Response",
        'PetGotoResponseMethod'              : "Pet Response",
        'PetStayResponseMethod'              : "Pet Response",
        'PetBodyguard'                       : "Bodyguard Mode",
        'PetBodyguardResponseMethod'         : "Pet Response",
        'PetChatToggle'                      : "Pet Chatty Mode Toggle",
        'PetBodyguardAttack'                 : "BG Mode Attack",
        'PetBodyguardGoto'                   : "BG Mode Goto",
        'PetNPEnable'                        : 'Enable Single Key Pet Binds',
        'SelNextPet'                         : "Select Next Pet",
        'SelPrevPet'                         : "Select Previous Pet",
        'IncPetSize'                         : "Increase Pet Group Size",
        'DecPetSize'                         : "Decrease Pet Group Size",
    })
