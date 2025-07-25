import wx
import re
import UI
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
            {
                'label'      : 'Bodyguard',
                'ctrlName'      : 'PetBodyguard',
                'tooltipdetail' : 'order your Bodyguard pets to enter Bodyguard Mode',
            },
        )

    def __init__(self, parent):
        Page.__init__(self, parent)

        self.PetBoxes = []

        self.Init = {
            'Enable' : False,

            'RenamePets' : '',

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

            'PetBodyguard' : 'MULTIPLY',
            'PetBodyguardResponse' : 'Bodyguarding.',
            'PetBodyguardResponseMethod' : 'Petsay',

            'PetCmdEnable': False,

            'PetChatToggle' : 'ALT+M',
            'PetChattyDefault' : True,
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
        PetNames  = wx.StaticBoxSizer(wx.VERTICAL, self, label = "Pet Names and By-Name Keybinds")
        PetNameSB = PetNames.GetStaticBox()
        PetInner = wx.BoxSizer(wx.HORIZONTAL)

        for i in range(6):
            petdesc = ['Minion 1', 'Minion 2', 'Minion 3', 'Lieutenant 1', 'Lieutenant 2', 'Boss'][i]
            PBSB = wx.StaticBox(PetNameSB, style = wx.ALIGN_CENTER|wx.NO_BORDER, label = petdesc)
            box = wx.StaticBoxSizer(PBSB, wx.VERTICAL)

            name = cgTextCtrl(PBSB, style = wx.TE_CENTRE)
            setattr(name, "CtlLabel", None)
            self.Ctrls[f'Pet{i+1}Name'] = name
            name.Bind(wx.EVT_TEXT, self.OnNameTextChange)

            button = bcKeyButton(PBSB, -1, init = {
                'CtlName'  : f'PetSelect{i+1}',
                'ToolTip'  : f'Choose the key that will select {petdesc}',
                'Key'      : self.Init[f'PetSelect{i+1}'],
            })
            self.Ctrls[f'PetSelect{i+1}'] = button

            petcb = wx.CheckBox(PBSB, -1, "Bodyguard")
            self.Ctrls[f"Pet{i+1}Bodyguard"] = petcb
            petcb.SetToolTip(f"Select whether {petdesc} acts as Bodyguard when Bodyguard Mode is activated")

            box.Add(name,   1, wx.EXPAND|wx.ALL, 3)
            box.Add(button, 1, wx.EXPAND|wx.ALL, 3)
            box.Add(petcb,  1, wx.ALIGN_CENTER|wx.ALL, 3)

            PetInner.Add(box, 1, wx.EXPAND|wx.ALL, 3)
            self.PetBoxes.append(box)

        PetExtraCtrls = wx.BoxSizer(wx.HORIZONTAL)
        maxValue = 24 if self.Profile.Server == 'Homecoming' else 26
        self.LevelSlider = wx.Slider(PetNameSB, minValue = 1, maxValue = maxValue, value = maxValue,
                                     style = wx.SL_VALUE_LABEL|wx.SL_AUTOTICKS)
        self.LevelSlider.Bind(wx.EVT_SLIDER, self.OnLevelChanged)
        self.LevelSlider.SetToolTip('Select the level of your Mastermind - set to max for higher levels')
        self.Ctrls['MMLevel'] = self.LevelSlider

        RenameLabel = wx.StaticText(PetNameSB, -1, 'Rename Pets:')
        self.RenamePetsButton = bcKeyButton(PetNameSB, -1, init = {
                'CtlName'  : 'RenamePets',
                'Key'      : self.Init['RenamePets'],
            })
        self.RenamePetsButton.SetToolTip('Choose the key that will rename your pets, in-game, to match the names set in BindControl')
        self.Ctrls['RenamePets'] = self.RenamePetsButton

        PetExtraCtrls.Add(wx.StaticText(PetNameSB, -1, 'Mastermind Level:'), 0, wx.ALIGN_CENTER_VERTICAL)
        PetExtraCtrls.Add(self.LevelSlider, 1, wx.ALIGN_CENTER_VERTICAL)
        PetExtraCtrls.Add(RenameLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10)
        PetExtraCtrls.Add(self.RenamePetsButton, 0, wx.ALIGN_CENTER_VERTICAL)
        PetExtraCtrls.Add(HelpButton(PetNameSB, 'PetNames.html'), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10)

        PetNames.Add(PetInner,      1, wx.EXPAND|wx.ALL, 10)
        PetNames.Add(PetExtraCtrls, 0, wx.EXPAND|wx.ALL, 15)

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
                size    = wx.Size(500, -1),
            )
        petCommandsKeys.AddControl(
            ctlName = 'PetChatToggle',
            ctlType = 'keybutton',
            tooltip = 'Choose the key combo that will toggle your pets\' chattiness level',
        )
        petCommandsKeys.AddControl(
            ctlName = 'PetChattyDefault',
            ctlType = "checkbox",
            tooltip = "Choose whether pets are chatty or silent after a binds reset",
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
        self.MainSizer.Add(PetNames, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        self.MainSizer.Add(petCommandsKeys, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)
        self.MainSizer.AddSpacer(10)

        self.MainSizer.Add(PetSelBox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

    def SynchronizeUI(self):
        ismm = self.Profile.Archetype() == "Mastermind"
        pset = self.Profile.Primary()

        for control in self.Ctrls.values(): control.Enable(bool(ismm and pset))
        self.RenamePetsButton.Enable(bool(ismm and pset))
        self.OnPetCmdEnable()
        self.OnPetNPChange()
        self.OnLevelChanged()

    def OnLevelChanged(self, evt = None):
        if evt: evt.Skip()
        bossLevel = 22 if self.Profile.Server == 'Homecoming' else 26
        lvl = self.LevelSlider.GetValue()
        self.PetBoxes[1].GetStaticBox().Enable(lvl >= 6)
        self.PetBoxes[2].GetStaticBox().Enable(lvl >= 18)
        self.PetBoxes[3].GetStaticBox().Enable(lvl >= 12)
        self.PetBoxes[4].GetStaticBox().Enable(lvl >= 24)
        self.PetBoxes[5].GetStaticBox().Enable(lvl >= bossLevel)
        self.CheckUndefNames()
        self.CheckUniqueNames()

    def OnPetCmdEnable(self, evt = None):
        self.Freeze()
        enabled = self.GetState('PetCmdEnable') and self.Profile.Archetype() == "Mastermind"
        for command in self.petCommandKeyDefinitions:
            self.EnableControls(enabled, [
                command['ctrlName'], command['ctrlName']+"ResponseMethod", command['ctrlName']+"Response"
            ])
        self.EnableControls(enabled , ['PetChatToggle', 'PetChattyDefault', ])

        for petid in [1,2,3,4,5,6]:
            self.Ctrls[f"Pet{petid}Bodyguard"].Enable(enabled)

        self.CheckUndefNames()
        self.CheckUniqueNames()
        self.Thaw()
        if evt: evt.Skip()

    def OnPetNPChange(self, evt = None):
        enabled = self.GetState('PetNPEnable') and self.Profile.Archetype() == "Mastermind"
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
        self.CheckUndefNames()
        self.CheckUniqueNames()
        if evt: evt.Skip()

    def CheckUndefNames(self):
        for i in (1,2,3,4,5,6):
            ctrl = self.Ctrls[f'Pet{i}Name']
            if not ctrl.IsEnabled():
                ctrl.RemoveError('undef')
                continue

            if ctrl.GetValue():
                ctrl.RemoveError('undef')
            else:
                ctrl.AddError('undef', 'By-Name selection and Bodyguard Mode require the pet name be filled in.')

    def CheckUniqueNames(self):
        if (self.Profile.Archetype() == "Mastermind"):
            names = []
            for i in (1,2,3,4,5,6):
                ctrl = self.Ctrls[f'Pet{i}Name']
                value = ctrl.GetValue().strip() # don't allow whitespace at the ends
                names.append(value)

            # we stash this away every time we calculate it so we can
            # extract it trivially when we write binds
            self.uniqueNames = FindSmallestUniqueSubstring(names)
            for i in (1,2,3,4,5,6):
                ctrl = self.Ctrls[f'Pet{i}Name']
                if not ctrl.IsEnabled():
                    ctrl.RemoveError('unique')
                    continue

                if self.uniqueNames[i-1]:
                    ctrl.RemoveError('unique')
                else:
                    ctrl.AddError('unique', f'This pet name is not different enough to identify it uniquely.  This is likely to cause issues with by-name and bodyguard binds.')
        else:
            for i in (1,2,3,4,5,6):
                ctrl = self.Ctrls[f'Pet{i}Name']
                ctrl.RemoveError('unique')


    ### BIND CREATION METHODS

    # set selected pets to BG Mode, chatty version
    def mmBGSelBind(self, file, PetBodyguardResponse, powers):
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

        file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(bgsay + bgset))

    # Set selected pets to BG Mode, quiet version
    def mmQuietBGSelBind(self, file, powers):
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

        file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(bgset))

    # set up "all" and "tierx" files with command binds, chatty version
    def mmSubBind(self, file, fn, grp, powers):
        profile = self.Profile

        file.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind([
            self.GetChatString('SelectAll'), profile.BLF('mmb','call.txt')]))
        file.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind([
            self.GetChatString('SelectMinions', powers['min']), profile.BLF('mmb','ctier1.txt')]))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind([
            self.GetChatString('SelectLieutenants', powers['lts']), profile.BLF('mmb','ctier2.txt')]))
        file.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind([
            self.GetChatString('SelectBoss', powers['bos']), profile.BLF('mmb','ctier3.txt')]))

        bgfresponse = self.GetState('PetBodyguardResponse') if self.GetChatString(f"Bodyguard") else ''
        self.mmBGSelBind(file,bgfresponse,powers)

        if   grp == 'sel'       : petcom =  'petcom'
        elif grp                : petcom = f'petcompow {grp}'
        else                    : petcom =  'petcomall'
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind([self.GetChatString(cmd, grp or 'all'), f"{petcom} {cmd}"]))

        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.BLF('mmb',f"{fn}.txt")]))

    # set up "all" and "tierx" files with command binds, quiet version
    def mmQuietSubBind(self, file, fn, grp, powers):
        profile = self.Profile
        file.SetBind(self.Ctrls['PetSelectAll']        .MakeFileKeyBind(profile.BLF('mmb','all.txt')))
        file.SetBind(self.Ctrls['PetSelectMinions']    .MakeFileKeyBind(profile.BLF('mmb','tier1.txt')))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.BLF('mmb','tier2.txt')))
        file.SetBind(self.Ctrls['PetSelectBoss']       .MakeFileKeyBind(profile.BLF('mmb','tier3.txt')))
        self.mmQuietBGSelBind(file, powers)

        if   grp == 'sel'       : petcom =  'petcom'
        elif grp                : petcom = f"petcompow {grp}"
        else                    : petcom =  'petcomall'
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(f"{petcom} {cmd}"))

        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Chatty Mode', profile.BLF('mmb','c' + fn + '.txt')]))

    def PopulateBindFiles(self):

        profile = self.Profile
        ResetFile = profile.ResetFile()

        if not profile.Archetype() == 'Mastermind': return True

        # First, deduce which "pet name boxes" need checking, and in what order.
        OrderedPetBoxes = []
        petPowers = self.MMPowerSets[self.Profile.Primary()]
        # now order them by powername, alphabetically, to match the in-game pet list
        revPowers = dict(sorted(petPowers['powers'].items(), key = lambda item: item[1]))
        for grp in revPowers:
            if grp == "min":
                if self.PetBoxes[0].GetStaticBox().IsEnabled():
                    OrderedPetBoxes.append([0, self.PetBoxes[0]])
                if self.PetBoxes[1].GetStaticBox().IsEnabled():
                    OrderedPetBoxes.append([1, self.PetBoxes[1]])
                if self.PetBoxes[2].GetStaticBox().IsEnabled():
                    OrderedPetBoxes.append([2, self.PetBoxes[2]])
            elif grp == "lts":
                if self.PetBoxes[3].GetStaticBox().IsEnabled():
                    OrderedPetBoxes.append([3, self.PetBoxes[3]])
                if self.PetBoxes[4].GetStaticBox().IsEnabled():
                    OrderedPetBoxes.append([4, self.PetBoxes[4]])
            elif grp == "bos":
                if self.PetBoxes[5].GetStaticBox().IsEnabled():
                    OrderedPetBoxes.append([5, self.PetBoxes[5]])

        # Now complain if any of the needed boxes isn't unique
        needUniqueNames = False
        for i in range(6):
            for [_, box] in OrderedPetBoxes:
                if self.PetBoxes[i] == box:
                    if self.Ctrls[f'PetSelect{i+1}'].GetLabel():
                        needUniqueNames = True
                        break
        if self.Ctrls['PetBodyguard'].GetLabel():
            needUniqueNames = True

        if needUniqueNames:
            for i in range(6):
                for [_, box] in OrderedPetBoxes:
                    if self.PetBoxes[i] == box:
                        ctrl = self.Ctrls[f'Pet{i+1}Name']
                        if ctrl.IsEnabled() and ctrl.HasAnyError():
                            result = wx.MessageBox("One or more of your pet names has errors.  You can continue to write these binds but they are likely not to work well in-game.  Continue?", "Name Error", wx.YES_NO)
                            if result == wx.NO: return False
                            break

        # Finally, let's write the RenamePets Bind if we want it
        if self.RenamePetsButton.GetLabel():
            rpCommands = []
            for i, pair in enumerate(OrderedPetBoxes):
                if not pair: continue
                (j, box) = pair
                petnamebox = self.Ctrls[f'Pet{j+1}Name']
                rpCommands.append(f'petselect {i}')
                rpCommands.append(f'petrename "{petnamebox.GetValue()}"')
                ResetFile.SetBind(self.RenamePetsButton.MakeFileKeyBind(rpCommands))

        ### Sandolphan binds
        if self.GetState('PetCmdEnable'):
            powers = self.MMPowerSets[ profile.General.GetState('Primary') ]['powers']

            if self.GetState('PetChattyDefault'):
                self.mmSubBind(ResetFile, "all", None, powers)
            else:
                self.mmQuietSubBind(ResetFile, "all", None, powers)

            #### "Quiet" versions
            allfile = profile.GetBindFile('mmb','all.txt')
            minfile = profile.GetBindFile('mmb','tier1.txt')
            ltsfile = profile.GetBindFile('mmb','tier2.txt')
            bosfile = profile.GetBindFile('mmb','tier3.txt')
            selfile = profile.GetBindFile('mmb','sel.txt')

            self.mmQuietSubBind(allfile , "all"   , None          , powers)
            self.mmQuietSubBind(minfile , "tier1" , powers['min'] , powers)
            self.mmQuietSubBind(ltsfile , "tier2" , powers['lts'] , powers)
            self.mmQuietSubBind(bosfile , "tier3" , powers['bos'] , powers)
            self.mmQuietSubBind(selfile , "sel"   , 'sel'         , powers)

            #### "Chatty" versions
            callfile = profile.GetBindFile('mmb','call.txt')
            cminfile = profile.GetBindFile('mmb','ctier1.txt')
            cltsfile = profile.GetBindFile('mmb','ctier2.txt')
            cbosfile = profile.GetBindFile('mmb','ctier3.txt')
            cselfile = profile.GetBindFile('mmb','csel.txt')

            self.mmSubBind(callfile , "all"   , None          , powers)
            self.mmSubBind(cminfile , "tier1" , powers['min'] , powers)
            self.mmSubBind(cltsfile , "tier2" , powers['lts'] , powers)
            self.mmSubBind(cbosfile , "tier3" , powers['bos'] , powers)
            self.mmSubBind(cselfile , "sel"   , 'sel'         , powers)

        ### By-name select binds.
        # TODO - would this make more sense fully integrated into mm(Quiet)SubBind?
        for pet in [1,2,3,4,5,6]:
            feedback = ''
            selfile = "sel.txt"
            if self.GetState('PetChattyDefault'):
                feedback = self.GetChatString('SelectAll', pet)
                selfile = "csel.txt"
            ResetFile.SetBind(
                self.Ctrls[f"PetSelect{pet}"].MakeFileKeyBind(
                    [feedback, f"petselectname {self.uniqueNames[pet-1]}", profile.BLF('mmb', selfile)]
                )
            )

        ### Prev / next pet binds
        if (self.GetState('PetNPEnable') and
            self.GetState('IncPetSize') and self.GetState('DecPetSize') and
            self.GetState('SelNextPet') and self.GetState('SelPrevPet')
        ):
            self.psCreateSet(6,0,ResetFile)
            for tsize in 1,2,3,4,5,6:
                for tsel in range(0,tsize+1):
                    file = self.Profile.GetBindFile('petsel', f"{tsize}{tsel}.txt")
                    self.psCreateSet(tsize,tsel,file)

        return True

    def psCreateSet(self, tsize, tsel, file):
        # tsize is the size of the team at the moment
        # tsel is the currently selected team member as far as the bind knows, or 0 if unknown

        c = self.Ctrls
        p = self.Profile

        if tsize < 6:
            file.SetBind(c['IncPetSize'].MakeFileKeyBind([
                f'tell $name, [{tsize+1} Pet]', p.BLF('petsel', f'{tsize+1}.txt')
            ]))
        else:
            file.SetBind(c['IncPetSize'].MakeFileKeyBind('nop'))
        if tsize == 1:
            file.SetBind(c['DecPetSize'].MakeFileKeyBind('nop'))
            file.SetBind(c['SelNextPet'].MakeFileKeyBind([
                f'petselect 0', p.BLF('petsel', f'{tsize}1.txt'), p.BLF('mmb', 'csel.txt'),
            ]))
            file.SetBind(c['SelPrevPet'].MakeFileKeyBind([
                f'petselect 0', p.BLF('petsel', f'{tsize}1.txt'), p.BLF('mmb', 'csel.txt'),
            ]))
        else:
            selnext,selprev = tsel+1,tsel-1
            if selnext > tsize : selnext = 1
            if selprev < 1 : selprev = tsize
            newsel = tsel
            if tsize-1 < tsel : newsel = tsize-1
            if tsize == 2 : newsel = 0
            file.SetBind(c['DecPetSize'].MakeFileKeyBind([
                f'tell $name, [{tsize-1} Pet]', p.BLF('petsel', f'{tsize-1}{newsel}.txt')
            ]))
            file.SetBind(c['SelNextPet'].MakeFileKeyBind([
                f'petselect {selnext-1}', p.BLF('petsel', f'{tsize}{selnext}.txt'), p.BLF('mmb', 'csel.txt'),
            ]))
            file.SetBind(c['SelPrevPet'].MakeFileKeyBind([
                f'petselect {selprev-1}', p.BLF('petsel', f'{tsize}{selprev}.txt'), p.BLF('mmb', 'csel.txt'),
            ]))

    def GetChatMethod(self, control, target:str|int = 'all'):
        chatdesc = self.GetState(control)
        if   target == 'all'         : petsay = "petsayall "
        elif target == 'sel'         : petsay = "petsay "
        elif isinstance(target, int) : petsay = f"petsayname {self.uniqueNames[target-1]} "
        else                         : petsay = f"petsaypow {target} "

        return {
            'Local'     : 'local ',
            'Self-tell' : 'tell $name, ',
            'Petsay'    : petsay,
            '---'       : '',
        }[chatdesc]

    def GetChatString(self, cmd, target:str|int = 'all'):
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
            'all'   , 'tier1'   , 'tier2'   , 'tier3'   ,
            'alla'  , 'tier1a'  , 'tier2a'  , 'tier3a'  ,
            'call'  , 'ctier1'  , 'ctier2'  , 'ctier3'  ,
            'calla' , 'ctier1a' , 'ctier2a' , 'ctier3a' ,
            'sel'   , 'csel',
            'bga'   , 'cbga'    , 'cbgb'    ,
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
        'PetSelect1'                         : "Select First Pet",
        'PetSelect2'                         : "Select Second Pet",
        'PetSelect3'                         : "Select Third Pet",
        'PetSelect4'                         : "Select Fourth Pet",
        'PetSelect5'                         : "Select Fifth Pet",
        'PetSelect6'                         : "Select Sixth Pet",
        'RenamePets'                         : "Rename Pets",
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
        'PetChattyDefault'                   : "Chatty is Default",
        'PetBodyguard'                       : "Bodyguard Mode",
        'PetBodyguardResponseMethod'         : "Pet Response",
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
                    # If it contains a space, put "" around it
                    if re.match(r'\s', substr):
                        substr = f'"{substr}"'
                    uniqueNames[nameInd] = substr
                    break
            else:
                # continue if the inner loop did not break
                continue
            # Inner loop broke, break again
            break

    return uniqueNames
