import wx
import re
import UI
from BLF import BLF
from Help import HelpButton
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED

# Sandolphan / Khaiba's guide to these controls found at:
# https://guidescroll.com/2011/07/city-of-heroes-mastermind-numeric-keypad-pet-controls/
#
# Originally: https://web.archive.org/web/20120904222729/http://boards.cityofheroes.com/showthread.php?t=117256

from Page import Page
from UI.ControlGroup import ControlGroup, cgTextCtrl

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

            'PetBodyguard' : 'MULTIPLY',
            'PetBodyguardResponse' : 'Bodyguarding.',
            'PetBodyguardResponseMethod' : 'Petsay',

            'PetBodyguardStay' : '',
            'PetBodyguardStayResponse' : 'Covering this Location.',
            'PetBodyguardStayResponseMethod' : 'Petsay',

            'PetCmdEnable': False,

            'PetChatToggle' : 'LALT+M',
            'PetSelect1' : '',
            'PetSelect2' : '',
            'PetSelect3' : '',
            'PetSelect4' : '',
            'PetSelect5' : '',
            'PetSelect6' : '',

            'Pet1Name' : '',
            'Pet2Name' : '',
            'Pet3Name' : '',
            'Pet4Name' : '',
            'Pet5Name' : '',
            'Pet6Name' : '',

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
        # TODO is this Gamedata?
        self.MMPowerSets = {
            "Beast Mastery"   :{
                'powers': { 'min' : 'wol',  'lts' : 'lio',  'bos' : 'dir',  },
                'names':  [ 'Howler Wolf', 'Howler Wolf', 'Alpha Howler Wolf',
                           'Lion', 'Lion', 'Dire Wolf' ],
            },
            "Demon Summoning" :{
                'powers': { 'min' : 'lin',  'lts' : 'mons', 'bos' : 'pri',  },
                'names' : [ 'Fiery Demonling', 'Cold Demonling', 'Hellfire Demonling',
                           'Ember Demon', 'Hellfire Gargoyle', 'Demon Prince', ],
            },
            "Mercenaries"     :{
                'powers': { 'min' : "sol",  'lts' : "spec", 'bos' : "com",  },
                'names' : [ 'Soldier', 'Soldier', 'Medic', 'Spec Ops', 'Spec Ops', 'Commando'],
            },
            "Necromancy"      :{
                'powers': { 'min' : "zom",  'lts' : "grav", 'bos' : "lich", },
                'names' : [ 'Zombie', 'Zombie', 'Zombie', 'Grave Knight', 'Grave Knight', 'Lich' ],
            },
            "Ninjas"          :{
                'powers': { 'min' : "gen",  'lts' : "joun", 'bos' : "oni",  },
                'names' : [ 'Genin', 'Genin', 'Genin', 'Jounin', 'Jounin', 'Oni', ],
            },
            "Robotics"        :{
                'powers': { 'min' : "dron", 'lts' : "prot", 'bos' : "ass",  },
                'names' : [ 'Drone', 'Drone', 'Drone', 'Protector Bot', 'Protector Bot', 'Assault Bot', ],
            },
            "Thugs"           :{
                'powers': { 'min' : "thu",  'lts' : "enf",  'bos' : "bru",  },
                'names' : [ 'Punk', 'Punk', 'Arsonist', 'Enforcer', 'Enforcer', 'Bruiser', ],
            },
        }
        self.TabTitle = "Mastermind / Pet Binds"
        self.uniqueNames = []

    def BuildPage(self):

        # get the pet names and binds to select them directly
        PetNames  = wx.StaticBoxSizer(wx.HORIZONTAL, self, label = "Pet Names and By-Name Keybinds")
        PetNameSB = PetNames.GetStaticBox()
        PetInner = wx.GridBagSizer(hgap = 5, vgap = 5)
        PetNames.Add(PetInner, 1, wx.ALL|wx.EXPAND, 10)
        self.PetNameLabel = wx.StaticText(PetNameSB, label = "Pet Name:")
        self.PetKeyLabel  = wx.StaticText(PetNameSB, label = "Select by Name:")
        PetInner.Add(self.PetNameLabel, (1,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        PetInner.Add(self.PetKeyLabel,  (2,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        for i in (1,2,3,4,5,6):
            name = cgTextCtrl(PetNameSB, style = wx.TE_CENTRE)
            setattr(name, "CtlLabel", None)
            self.Ctrls[f'Pet{i}Name'] = name
            name.Bind(wx.EVT_TEXT, self.OnNameTextChange)

            petdesc = ['Minion Pet 1', 'Minion Pet 2', 'Minion Pet 3',
                       'Lieutenant Pet 1', 'Lieutenant Pet 2', 'Boss Pet'][i-1]
            label = wx.StaticText(PetNameSB, label = petdesc)
            button = bcKeyButton(PetNameSB, -1, init = {
                'CtlName'  : f'PetSelect{i}',
                'CtlLabel' : label,
                'Key'      : self.Init[f'PetSelect{i}'],
            })
            self.Ctrls[f'PetSelect{i}'] = button

            petcb = wx.CheckBox(PetNameSB, -1, "Bodyguard")
            self.Ctrls[f"Pet{i}Bodyguard"] = petcb
            petcb.SetToolTip(f"Select whether {petdesc} acts as Bodyguard when Bodyguard Mode is activated")

            PetInner.Add(label,  (0,i), flag=wx.EXPAND|wx.ALIGN_CENTER)
            PetInner.Add(name,   (1,i), flag=wx.EXPAND)
            PetInner.Add(button, (2,i), flag=wx.EXPAND)
            PetInner.Add(petcb,  (3,i), flag=wx.EXPAND|wx.ALIGN_CENTER)
            PetInner.AddGrowableCol(i)

        nameDefaultButton = wx.Button(PetNameSB, -1, 'Defaults')
        nameDefaultButton.SetToolTip('Set your pet names to the default values for your powerset.')
        nameDefaultButton.Bind(wx.EVT_BUTTON, self.OnNameDefaultButton)
        PetInner.Add(nameDefaultButton, (1,7), flag = wx.EXPAND)

        petcmdenable = wx.Panel(self)
        petcmdenablesizer = wx.BoxSizer(wx.HORIZONTAL)
        petcmdenable.SetSizer(petcmdenablesizer)
        petcmdenablecb = wx.CheckBox(petcmdenable, -1, 'Enable Pet Action Binds')
        petcmdenablecb.SetToolTip( wx.ToolTip('Check this to enable the Mastermind Pet Action Binds') )
        petcmdenablecb.Bind(wx.EVT_CHECKBOX, self.OnPetCmdEnable)
        self.Ctrls['PetCmdEnable'] = petcmdenablecb
        petcmdenablecb.SetValue(self.Init['PetCmdEnable'])
        petcmdhelpbutton = HelpButton(petcmdenable, 'PetActionBinds.html')
        petcmdenablesizer.Add(petcmdenablecb, 0, wx.ALIGN_CENTER_VERTICAL)
        petcmdenablesizer.Add(petcmdhelpbutton, 0)

        # Iterate the data structure at the top and make the grid of controls for the basic pet binds
        petCommandsKeys = ControlGroup(self, self, width = 5,
                                       label = "Pet Action Binds", flexcols = [4], topcontent = petcmdenable)
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
        # add some space above it
        for i in [1,2,3,4,5,6,7,8]:
            petCommandsKeys.AddControl( ctlName = f'spacer{i}', ctlType = 'statictext', noLabel = True,)

        bgCB = petCommandsKeys.AddControl(
            noLabel  = True,
            ctlName  = 'PetBodyguardEnabled',
            ctlType  = 'checkbox',
            contents = 'Enable Bodyguard Mode Binds',
            tooltip  = 'Check this to enable the Bodyguard Mode Binds',
        )
        bgCB.Bind(wx.EVT_CHECKBOX, self.OnBGCheckboxes)

        staticbox = petCommandsKeys.GetStaticBox()
        petCommandsKeys.InnerSizer.Add(HelpButton(staticbox, "BodyguardBinds.html"))

        # add another spacer row below.  This is ugly
        for i in [1,2,3,4,5,6,7,8]:
            petCommandsKeys.AddControl( ctlName = f'spacer{i}', ctlType = 'statictext', noLabel = True,)

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
        petCommandsKeys.AddControl(
            ctlName = 'PetBodyguardStay',
            ctlType = 'keybutton',
            tooltip = "Choose the key combo that will command your bodyguards to stay at their current location",
        )
        petCommandsKeys.AddControl(
            ctlName = 'PetBodyguardStayResponseMethod',
            ctlType = 'combobox',
            contents = [ "Local", "Self-tell", "Petsay", "---", ],
            tooltip = "Choose how your bodyguards will respond when they are in chatty mode and you order them to stay at their current location",
        )
        petCommandsKeys.AddControl(
            noLabel = True,
            ctlName = "PetBodyguardStayResponse",
            ctlType = "text",
            tooltip = "Choose the chat response your bodyguards give when you order them to stay at their current location",
        )
        #
        # Pet Next/Prev select binds
        petnpenable = wx.Panel(self)
        petnpenablesizer = wx.BoxSizer(wx.HORIZONTAL)
        petnpenable.SetSizer(petnpenablesizer)
        petnpenablecb = wx.CheckBox(petnpenable, -1, 'Enable Prev/Next Pet Select Binds')
        petnpenablecb.SetToolTip( wx.ToolTip('Check this to enable the Prev/Next Pet Select Binds') )
        petnpenablecb.Bind(wx.EVT_CHECKBOX, self.OnPetNPChange)
        self.Ctrls['PetNPEnable'] = petnpenablecb
        petnpenablecb.SetValue(self.Init['PetNPEnable'])
        petnphelpbutton = HelpButton(petnpenable, 'PetPrevNextBinds.html')
        petnpenablesizer.Add(petnpenablecb, 0, wx.ALIGN_CENTER_VERTICAL)
        petnpenablesizer.Add(petnphelpbutton, 0)

        PetSelBox = ControlGroup(self, self, label="Prev/Next Pet Select Binds",
                                 width=8, flexcols=[1,3,5,7], topcontent = petnpenable)
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
            self.Ctrls[b[0]].Bind(EVT_KEY_CHANGED, self.OnPetNPChange)

        # Bring it all together
        self.MainSizer.Add(PetNames, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 16)
        self.MainSizer.Add(petCommandsKeys, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 16)
        self.MainSizer.AddSpacer(10)

        self.MainSizer.Add(PetSelBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 16)

        self.SynchronizeUI()

    def SynchronizeUI(self):
        ismm = self.Profile.Archetype() == "Mastermind"
        pset = self.Profile.General.GetState('Primary')

        # TODO let's not do this for now -- we should instead maybe do a "fill with
        # default" button?  In any case, currently if we pick MM, we get beast names
        # loaded immediately, then they're full and don't update when we select Robots or w/e
        #
        # if self.Profile.General.GetState('Name'): # profile is loaded
        #     if ismm:
        #         names = self.MMPowerSets[ self.Profile.General.GetState('Primary') ]['names']
        #         for i in (1,2,3,4,5,6):
        #             value = names[i-1]
        #             currvalue = self.GetState(f'Pet{i}Name')
        #             if not currvalue or currvalue == '':
        #                 self.SetState(f'Pet{i}Name', value)

        for control in self.Ctrls.values(): control.Enable(bool(ismm and pset))
        self.PetNameLabel.Enable(bool(ismm and pset))
        self.PetKeyLabel .Enable(bool(ismm and pset))
        self.OnPetCmdEnable()
        self.OnPetNPChange()

    def OnNameDefaultButton(self, _ = None):
        result = wx.MessageBox("This will set your pet names to the default values for your powerset.  They will likely need to be changed to make by-name selection and Bodyguard Mode binds work.  Continue?", "Set To Default", wx.YES_NO)
        if result == wx.NO: return
        defaults = self.MMPowerSets[self.Profile.Primary()]['names']
        for i, petname in enumerate(defaults):
            self.SetState(f'Pet{i+1}Name', petname)

    def OnPetCmdEnable(self, evt = None):
        self.Freeze()
        enabled = self.GetState('PetCmdEnable')
        for command in self.petCommandKeyDefinitions:
            self.EnableControls(enabled, [
                command['ctrlName'], command['ctrlName']+"ResponseMethod", command['ctrlName']+"Response"
            ])
        self.EnableControls(enabled,
            ['PetChatToggle'    ,
             'PetBodyguard'     , 'PetBodyguardResponseMethod'     , 'PetBodyguardResponse'     ,
             'PetBodyguardStay' , 'PetBodyguardStayResponseMethod' , 'PetBodyguardStayResponse' ,
            ])
        # now re-check the BG stuff that we just enabled.
        self.OnBGCheckboxes()
        self.Thaw()
        if evt: evt.Skip()

    def OnPetNPChange(self, evt = None):
        enabled = self.GetState('PetNPEnable')
        self.EnableControls(enabled, ['SelNextPet', 'SelPrevPet', 'IncPetSize', 'DecPetSize'])
        if enabled:
            for ctrlname in ['SelNextPet', 'SelPrevPet', 'IncPetSize', 'DecPetSize']:
                ctrl = self.Ctrls[ctrlname]
                if ctrl.Key:
                    ctrl.RemoveError('undef')
                else:
                    label = ctrl.CtlLabel.GetLabel().strip(':')
                    ctrl.AddError('undef', f'"{label}" must be set if Prev/Next binds are enabled.  These will not be written to the bindfiles until this is corrected.')
        else:
            for ctrlname in ['SelNextPet', 'SelPrevPet', 'IncPetSize', 'DecPetSize']:
                ctrl = self.Ctrls[ctrlname]
                ctrl.RemoveError('undef')
        if evt: evt.Skip()

    def OnNameTextChange(self, evt = None):
        self.CheckBGModeNames()
        self.CheckNamesAreUnique()
        if evt: evt.Skip()

    def OnBGCheckboxes(self, evt = None):
        petcmdenabled = self.GetState('PetCmdEnable')

        bgEnabled = self.GetState('PetBodyguardEnabled')

        for c in [
            'PetBodyguard'     , 'PetBodyguardResponseMethod'     , 'PetBodyguardResponse'     ,
            'PetBodyguardStay' , 'PetBodyguardStayResponseMethod' , 'PetBodyguardStayResponse' ,
        ]:
            self.Ctrls[c].Enable(petcmdenabled and bgEnabled)

        for petid in [1,2,3,4,5,6]:
            self.Ctrls[f"Pet{petid}Bodyguard"].Enable(petcmdenabled and bgEnabled)

        self.CheckBGModeNames()
        self.CheckNamesAreUnique()

        if evt: evt.Skip()

    def CheckBGModeNames(self):
        if self.GetState('PetBodyguardEnabled'):
            for i in (1,2,3,4,5,6):
                ctrl = self.Ctrls[f'Pet{i}Name']
                if ctrl.GetValue():
                    ctrl.RemoveError('undef')
                else:
                    ctrl.AddError('undef', 'By-Name selection and Bodyguard Mode require the pet name be filled in.')

    def CheckNamesAreUnique(self):
        if (self.Profile.Archetype() == "Mastermind"):
            names = []
            wasMultiWord = [False] * 6
            for i in (1,2,3,4,5,6):
                ctrl = self.Ctrls[f'Pet{i}Name']
                value = ctrl.GetValue()
                # if we contain multiple words, use the longest
                words = value.split()
                if len(words) > 1:
                    wasMultiWord[i-1] = True
                    value = max(words, key = len)
                names.append(value)

            # we stash this away every time we calculate it so we can
            # extract it trivially when we write binds
            self.uniqueNames = FindSmallestUniqueSubstring(names)
            for i in (1,2,3,4,5,6):
                ctrl = self.Ctrls[f'Pet{i}Name']
                if self.uniqueNames[i-1]:
                    ctrl.RemoveError('unique')
                else:
                    MWWarning = "  BindControl only uses the longest word of a multi-word name." if wasMultiWord[i-1] else ""
                    ctrl.AddError('unique', f'This pet name is not different enough to identify it uniquely.{MWWarning}')
        else:
            for i in (1,2,3,4,5,6):
                ctrl = self.Ctrls[f'Pet{i}Name']
                ctrl.RemoveError('unique')


    ### BIND CREATION METHODS

    # set selected pets to BG Mode, chatty version
    def mmBGSelBind(self, file, PetBodyguardResponse, powers):
        if not self.GetState('PetBodyguardEnabled'): return

        profile = self.Profile
        bgset = []
        bgsay = []
        method = self.GetChatMethod(f"PetBodyguardResponseMethod")
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
                        method = f"petsayname {self.uniqueNames[0]} "
                    bgsay.append(method + PetBodyguardResponse)
                if (self.GetState('Pet2Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[1]} "
                    bgsay.append(method + PetBodyguardResponse)
                if (self.GetState('Pet3Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[2]} "
                    bgsay.append(method + PetBodyguardResponse)

            if (tier2bg == 2):
                if re.match('petsay', method): method = f"petsaypow {powers['lts']} "
                bgsay.append(method + PetBodyguardResponse)
            else:
                if (self.GetState('Pet4Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[3]} "
                    bgsay.append(method + PetBodyguardResponse)
                if (self.GetState('Pet5Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[4]} "
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
                if (self.GetState('Pet1Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[0]} def fol")
                if (self.GetState('Pet2Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[1]} def fol")
                if (self.GetState('Pet3Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[2]} def fol")

            if (tier2bg == 2):
                bgset.append(f"petcompow {powers['lts']} def fol")
            else:
                if (self.GetState('Pet4Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[3]} def fol")
                if (self.GetState('Pet5Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[4]} def fol")

            if (tier3bg == 1):
                bgset.append(f"petcompow {powers['bos']} def fol")

        keyBindContents = bgsay + bgset + [profile.GetBindFile('mmb','cbga.txt').BLF()]
        file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(keyBindContents))

    # perform selected action with non-BG pets, chatty version.  This does not work.
    def mmBGActBind(self, filedn, fileup, action, say, powers):

        key    = self.GetState(f"Pet{action}")
        name   = UI.Labels[f"Pet{action}"]
        method = self.GetChatMethod(f"Pet{action}ResponseMethod")

        bgact = []
        bgsay = []
        (tier1bg, tier2bg, tier3bg) = self.CountBodyguards()
        #  first check if tier1bg + tier2bg + tier3bg == 0, if so, we can get away with petsayall.
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
                        method = f"petsayname {self.uniqueNames[0]} "
                    bgsay.append(f"{method}{say}")
                if (not self.GetState('Pet2Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[1]} "
                    bgsay.append(f"{method}{say}")
                if (not self.GetState('Pet3Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[2]} "
                    bgsay.append(f"{method}{say}")

            if (tier2bg == 0):
                if re.match('petsay', method): method = f"petsaypow {powers['lts']} "
                bgsay.append(f"{method} {say}")
            else :
                if (not self.GetState('Pet4Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[3]} "
                    bgsay.append(f"{method}{say}")
                if (not self.GetState('Pet5Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[4]} "
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
                if (not self.GetState('Pet1Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[0]} {action}")
                if (not self.GetState('Pet2Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[1]} {action}")
                if (not self.GetState('Pet3Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[2]} {action}")

            if (tier2bg == 0):
                bgact.append(f"petcompow {powers['lts']} {action}")
            else :
                if (not self.GetState('Pet4Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[3]} {action}")
                if (not self.GetState('Pet5Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[4]} {action}")

            if (tier3bg == 0):
                bgact.append('petcompow ' + f"{powers['bos']} {action}")

        filedn.SetBind(key, name, self, ["+ $$"] + bgsay + [fileup.BLF()])
        fileup.SetBind(key, name, self, ["- $$"] + bgact + [filedn.BLF()])

    # perform selected action with BG pets, chatty version.  This does not work.
    def mmBGActBGBind(self, filedn, fileup, action, say, powers):
        key =    self.GetState(f"PetBodyguard{action}")
        name = UI.Labels[f"PetBodyguard{action}"]
        method = self.GetChatMethod(f"PetBodyguard{action}ResponseMethod")

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
                        method = f"petsayname {self.uniqueNames[0]} "
                    bgsay.append(f"{method}{say}")
                if (self.GetState('Pet2Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[1]} "
                    bgsay.append(f"{method}{say}")
                if (self.GetState('Pet3Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[2]} "
                    bgsay.append(f"{method}{say}")

            if (tier2bg == 2):
                if re.match('petsay', method): method = f"petsaypow {powers['lts']} "
                bgsay.append(f"{method} {say}")
            else :
                if (self.GetState('Pet4Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[3]} "
                    bgsay.append(f"{method}{say}")
                if (self.GetState('Pet5Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[4]} "
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
                if (self.GetState('Pet1Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[0]} {action}")
                if (self.GetState('Pet2Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[1]} {action}")
                if (self.GetState('Pet3Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[2]} {action}")

            if (tier2bg == 2):
                bgact.append(f"petcompow {powers['lts']} {action}")
            else :
                if (self.GetState('Pet4Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[3]} {action}")
                if (self.GetState('Pet5Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[4]} {action}")

            if (tier3bg == 1):
                bgact.append(f"petcompow {powers['bos']} {action}")

        # file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(bgsay.$bgset.BindFile.BLF($profile, 'mmb','\mmb\\cbga.txt')))
        filedn.SetBind(key, name, self, ["+ $$"] + bgsay + [fileup.BLF()])
        fileup.SetBind(key, name, self, ["- $$"] + bgact + [filedn.BLF()])

    # Set selected pets to BG Mode, quiet version
    def mmQuietBGSelBind(self, file, powers):
        profile = self.Profile
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
                    if (self.GetState('Pet1Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[0]} def fol")
                    if (self.GetState('Pet2Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[1]} def fol")
                    if (self.GetState('Pet3Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[2]} def fol")

                if (tier2bg == 2):
                    bgset.append(f"petcompow {powers['lts']} def fol")
                else :
                    if (self.GetState('Pet4Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[3]} def fol")
                    if (self.GetState('Pet5Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[4]} def fol")

                if (tier3bg == 1):
                    bgset.append(f"petcompow {powers['bos']} def fol")

            file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(bgset + [profile.GetBindFile('mmb','bga.txt').BLF()]))

    # perform selected action with non-BG pets, quiet version.  This does not work.
    def mmQuietBGActBind(self, filedn, action, powers):

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
                if (not self.GetState('Pet1Bodyguard')): bgact.append(f"petcomname {self.uniqueNames[0]} {action}")
                if (not self.GetState('Pet2Bodyguard')): bgact.append(f"petcomname {self.uniqueNames[1]} {action}")
                if (not self.GetState('Pet3Bodyguard')): bgact.append(f"petcomname {self.uniqueNames[2]} {action}")

            if (tier2bg == 0):
                bgact.append(f"petcompow {powers['lts']} {action}")
            else :
                if (not self.GetState('Pet4Bodyguard')): bgact.append(f"petcomname {self.uniqueNames[3]} {action}")
                if (not self.GetState('Pet5Bodyguard')): bgact.append(f"petcomname {self.uniqueNames[4]} {action}")

            if (tier3bg == 0): bgact.append(f"petcompow {powers['bos']} {action}")

        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(key, name, self, bgact)

    # perform selected action with BG pets, quiet version.  This does not work.
    def mmQuietBGActBGBind(self, filedn, action, powers):

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
                if (self.GetState('Pet1Bodyguard')): bgact.append(f"petcomname {self.uniqueNames[0]} {action}")
                if (self.GetState('Pet2Bodyguard')): bgact.append(f"petcomname {self.uniqueNames[1]} {action}")
                if (self.GetState('Pet3Bodyguard')): bgact.append(f"petcomname {self.uniqueNames[2]} {action}")

            if (tier2bg == 2):
                bgact.append(f"petcompow  {powers['lts']} {action}")
            else :
                if (self.GetState('Pet4Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[3]} {action}")
                if (self.GetState('Pet5Bodyguard')) : bgact.append(f"petcomname {self.uniqueNames[4]} {action}")

            if (tier3bg == 1) : bgact.append(f"petcompow {powers['bos']} {action}")

        if not bgact: return
        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(key, name, self, bgact)

    # set up "all" and "tierx" files with command binds, chatty version
    def mmSubBind(self, file, fn, grp, powers):
        profile = self.Profile

        file.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind([
            self.GetChatString('SelectAll'), profile.GetBindFile('mmb','call.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind([
            self.GetChatString('SelectMinions', 'min'), profile.GetBindFile('mmb','ctier1.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind([
            self.GetChatString('SelectLieutenants', 'lts'), profile.GetBindFile('mmb','ctier2.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind([
            self.GetChatString('SelectBoss', 'bos'), profile.GetBindFile('mmb','ctier3.txt').BLF()]))

        bgresponse = self.GetState('PetBodyguardResponse') if self.GetChatString(f"Bodyguard") else ''
        self.mmBGSelBind(file,bgresponse,powers)

        if grp: petcom = f"$$petcompow {grp}"
        else:   petcom =  "$$petcomall"
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(self.GetChatString(cmd) + f" {petcom} {cmd}"))

        if (self.GetState('PetBodyguardEnabled')):
            file.SetBind(self.Ctrls['PetBodyguardStay'].MakeFileKeyBind('nop'))

        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.GetBindFile('mmb',f"{fn}.txt").BLF()]))

    # set up BG Mode files, chatty version -- the mmBGAct* innards of this probably don't work.
    def mmBGSubBind(self, filedn, fileup, fn, powers):
        profile = self.Profile
        PetResponses = {}
        for cmd in ('Aggressive','Defensive','Passive','Attack','Follow','Goto', 'Stay', 'Bodyguard', 'BodyguardStay', ):
            PetResponses[cmd] = ''
            if self.GetChatMethod(f'Pet{cmd}ResponseMethod'):
                PetResponses[cmd] = self.GetState(f'Pet{cmd}Response')

        filedn.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind(
            [self.GetChatString('SelectAll'), profile.GetBindFile('mmb','call.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind(
            [self.GetChatString('SelectMinions', 'min'), profile.GetBindFile('mmb','ctier1.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(
            [self.GetChatString('SelectLieutenants', 'lts'), profile.GetBindFile('mmb','ctier2.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind(
            [self.GetChatString('SelectBoss', 'bos'), profile.GetBindFile('mmb','ctier3.txt').BLF()]))

        self.mmBGSelBind(filedn, PetResponses['Bodyguard'], powers)

        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            self.mmBGActBind(filedn, fileup, cmd, PetResponses[cmd], powers)

        if (self.GetState('PetBodyguardEnabled')):
            self.mmBGActBGBind(filedn, fileup,'Stay', PetResponses['BodyguardStay'], powers)

        filedn.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.GetBindFile('mmb',f"{fn}a.txt").BLF()]))

    # set up "all" and "tierx" files with command binds, quiet version
    def mmQuietSubBind(self, file, fn, grp, powers):
        profile = self.Profile
        file.SetBind(self.Ctrls['PetSelectAll']        .MakeFileKeyBind(profile.GetBindFile('mmb','all.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectMinions']    .MakeFileKeyBind(profile.GetBindFile('mmb','tier1.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.GetBindFile('mmb','tier2.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectBoss']       .MakeFileKeyBind(profile.GetBindFile('mmb','tier3.txt').BLF()))
        self.mmQuietBGSelBind(file, powers)

        if grp: petcom = f"petcompow {grp}"
        else:   petcom =  'petcomall'
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(f"{petcom} {cmd}"))

        if (self.GetState('PetBodyguardEnabled')):
            file.SetBind(self.Ctrls['PetBodyguardStay'].MakeFileKeyBind('nop'))

        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Chatty Mode', profile.GetBindFile('mmb','c' + fn + '.txt').BLF()]))

    # set up BG Mode files, quiet version -- the mmBGAct* innards of this probably don't work.
    def mmQuietBGSubBind(self, filedn, fn, powers):
        profile = self.Profile
        filedn.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind(profile.GetBindFile('mmb','all.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind(profile.GetBindFile('mmb','tier1.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.GetBindFile('mmb','tier2.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind(profile.GetBindFile('mmb','tier3.txt').BLF()))

        self.mmQuietBGSelBind(filedn, powers)

        for cmd in ('Aggressive','Defensive','Passive', 'Attack', 'Follow','Stay', 'Goto'):
            self.mmQuietBGActBind(filedn, cmd, powers)

        self.mmQuietBGActBGBind(filedn, 'Stay', powers)
        self.mmQuietBGActBGBind(filedn, 'Goto', powers)

        filedn.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Chatty Mode', profile.GetBindFile('mmb','c' + fn + 'a.txt').BLF()]))

    def PopulateBindFiles(self):

        profile = self.Profile
        ResetFile = profile.ResetFile()

        ### Sandolphan binds
        if self.GetState('PetCmdEnable'):
            powers = self.MMPowerSets[ profile.General.GetState('Primary') ]['powers']

            self.mmSubBind(ResetFile, "all", None, powers)

            #### "Quiet" versions
            allfile = profile.GetBindFile('mmb','all.txt')
            minfile = profile.GetBindFile('mmb','tier1.txt')
            ltsfile = profile.GetBindFile('mmb','tier2.txt')
            bosfile = profile.GetBindFile('mmb','tier3.txt')

            self.mmQuietSubBind(allfile , "all"   , None          , powers)
            self.mmQuietSubBind(minfile , "tier1" , powers['min'] , powers)
            self.mmQuietSubBind(ltsfile , "tier2" , powers['lts'] , powers)
            self.mmQuietSubBind(bosfile , "tier3" , powers['bos'] , powers)
            if (self.GetState('PetBodyguardEnabled')):
                bgfiledn = profile.GetBindFile('mmb','bga.txt')
                self.mmQuietBGSubBind(bgfiledn,"bg",powers)

            #### "Chatty" versions
            callfile = profile.GetBindFile('mmb','call.txt')
            cminfile = profile.GetBindFile('mmb','ctier1.txt')
            cltsfile = profile.GetBindFile('mmb','ctier2.txt')
            cbosfile = profile.GetBindFile('mmb','ctier3.txt')

            self.mmSubBind(callfile , "all"   , None          , powers)
            self.mmSubBind(cminfile , "tier1" , powers['min'] , powers)
            self.mmSubBind(cltsfile , "tier2" , powers['lts'] , powers)
            self.mmSubBind(cbosfile , "tier3" , powers['bos'] , powers)
            if (self.GetState('PetBodyguardEnabled')):
                cbgfiledn = profile.GetBindFile('mmb','cbga.txt')
                cbgfileup = profile.GetBindFile('mmb','cbgb.txt')
                self.mmBGSubBind(cbgfiledn,cbgfileup,"bg",powers)

        ### By-name select binds.
        for i in [1,2,3,4,5,6]:
            name = self.GetState(f"Pet{i}Name")
            # TODO - sanity-check regarding spaces in names
            ResetFile.SetBind(
                self.Ctrls[f"PetSelect{i}"].MakeFileKeyBind(f"petselectname {name}")
            )

        ### Prev / next pet binds
        if (self.GetState('PetNPEnable') and
            self.GetState('IncPetSize') and self.GetState('DecPetSize') and
            self.GetState('SelNextPet') and self.GetState('SelPrevPet')
        ):
            self.psCreateSet(6,0,self.Profile.ResetFile())
            for tsize in 1,2,3,4,5,6:
                for tsel in range(0,tsize+1):
                    file = self.Profile.GetBindFile('petsel', f"{tsize}{tsel}.txt")
                    self.psCreateSet(tsize,tsel,file)

    def psCreateSet(self, tsize, tsel, file):
        # tsize is the size of the team at the moment
        # tpos is the position of the player at the moment, or 0 if unknown
        # tsel is the currently selected team member as far as the bind knows, or 0 if unknown
        #file.SetBind(self.reset,'tell $name, Re-Loaded Prev/Next Team Select Bind.$${BLF()} {self.Profile.GameBindsDir()}\\petsel\\10.txt')
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
        powers   = self.MMPowerSets[ self.Profile.General.GetState('Primary') ]['powers']
        # This is terrible, I accidentally optimized away the original way of doing this.
        if target == "all": petsay = "petsayall "
        else:               petsay = "petsaypow " + powers[target] + " "

        return {
            'Local'     : 'local ',
            'Self-tell' : 'tell $name, ',
            'Petsay'    : petsay,
            '---'       : '',
        }[chatdesc]

    def GetChatString(self, cmd, target = 'all'):
        response = ''
        method = self.GetChatMethod(f'Pet{cmd}ResponseMethod', target)
        if method:
            response = method + self.GetState(f"Pet{cmd}Response")
        return response


    def CountBodyguards(self):
        tier1bg = 0
        tier2bg = 0
        tier3bg = 0
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
            'all'     , 'tier1'    , 'tier2'    , 'tier3'   ,
            'alla'    , 'tier1a'   , 'tier2a'   , 'tier3a'  ,
            'call'    , 'ctier1'   , 'ctier2'   , 'ctier3'  ,
            'calla'   , 'ctier1a'  , 'ctier2a'  , 'ctier3a' ,
            'bga'     , 'cbga'     , 'cbgb'     ,
            # these next three are old but we'll keep them in the list for now
            'bguarda' , 'cbguarda' , 'cbguardb' ,
        ]:
            # putting the old "mmbinds" dir in here for now to clean up old bindsdirs
            files.append(self.Profile.GetBindFile('mmbinds', f'{fn}.txt'))
            files.append(self.Profile.GetBindFile('mmb',     f'{fn}.txt'))

            for tsize in 1,2,3,4,5,6:
                for tsel in range(0,tsize+1):
                    files.append(self.Profile.GetBindFile('petsel', f"{tsize}{tsel}.txt"))

        return {
            'files' : files,
            # putting the old "mmbinds" dir in here for now to clean up old bindsdirs
            'dirs'  : ['mmbinds', 'mmb', 'petsel'],
        }


    for cmd in petCommandKeyDefinitions:
        UI.Labels[cmd['ctrlName']] = cmd['label']
    UI.Labels.update({
        'Pet1Name'                           : "First Pet's Name",
        'Pet2Name'                           : "Second Pet's Name",
        'Pet3Name'                           : "Third Pet's Name",
        'Pet4Name'                           : "Fourth Pet's Name",
        'Pet5Name'                           : "Fifth Pet's Name",
        'Pet6Name'                           : "Sixth Pet's Name",
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
        'PetChatToggle'                      : "Pet Chatty Mode Toggle",
        'PetBodyguard'                       : "Bodyguard Follow",
        'PetBodyguardResponseMethod'         : "Pet Response",
        'PetBodyguardStay'                   : "Bodyguard Stay",
        'PetBodyguardStayResponseMethod'     : "Pet Response",
        'PetNPEnable'                        : 'Enable Prev/Next Pet Binds',
        'SelNextPet'                         : "Select Next Pet",
        'SelPrevPet'                         : "Select Previous Pet",
        'IncPetSize'                         : "Increase Pet Group Size",
        'DecPetSize'                         : "Decrease Pet Group Size",
    })

# https://stackoverflow.com/questions/11245481/find-the-smallest-unique-substring-for-each-string-in-an-array
#
# Oho I see that I used the "brute force" method from the above URL instead
# of the "elegant" one.  Still it's blazingly fast for these six short strings,
# enough so that we can use it on every TextCtrl change.  If people start to
# complain of lag, we can experiment with the elegant one.
def FindSmallestUniqueSubstring(names):
    uniqueNames = [''] * len(names)
    ### For each name
    for nameInd, name in enumerate(names):
        ### For each possible substring length
        for windowSize in range(1,len(name)+1):
            ### For each starting index of a substring
            for substrInd in range(0, len(name)-windowSize+1):
                substr = name[substrInd:substrInd+windowSize].lower()
                foundMatch = False
                ### For each other name
                for otherNameInd in range(0, len(names)):
                    if (nameInd != otherNameInd) and (names[otherNameInd].lower().find(substr) >= 0):
                        foundMatch = True
                        break

                if not foundMatch:
                    ### This substr works!
                    uniqueNames[nameInd] = substr
                    break
            else:
                # continue if the inner loop did not break
                continue
            # Inner loop broke, break again
            break

    return uniqueNames
