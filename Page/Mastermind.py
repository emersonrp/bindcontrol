import wx
import UI

# Sandolphan / Khaiba's guide to these controls found at:
# https://guidescroll.com/2011/07/city-of-heroes-mastermind-numeric-keypad-pet-controls/
#
# Originally: https://web.archive.org/web/20120904222729/http://boards.cityofheroes.com/showthread.php?t=117256

from Page import Page
from UI.ControlGroup import ControlGroup

import BindFile

class Mastermind(Page):
    petCommandKeyDefinitions = (
            {
                'label'      : 'Select All',
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
                'tooltipdetail' : 'put your selected pets into Bodyguard mode',
            },
        )

    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Profile = parent
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

            'PetBodyguard' : 'UNBOUND',
            'PetBodyguardResponse' : 'Bodyguarding.',
            'PetBodyguardResponseMethod' : 'Petsay',

            'PetAggressive' : 'NUMPAD4',
            'PetAggressiveResponse' : 'Kill On Sight.',
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
            'PetGotoResponse' : 'Moving To Checkpoint.',
            'PetGotoResponseMethod' : 'Petsay',

            'PetStay' : 'DECIMAL',
            'PetStayResponse' : 'Holding This Position',
            'PetStayResponseMethod' : 'Petsay',

            'PetBodyguardMode' : 1,
            'PetBodyguardAttack' : '',
            'PetBodyguardGoto' : '',

            'EnablePetActionBinds': 1,

            'PetChatToggle' : 'ALT+M',
            'PetSelect1' : 'F1',
            'PetSelect2' : 'F2',
            'PetSelect3' : 'F3',
            'PetSelect4' : 'F4',
            'PetSelect5' : 'F5',
            'PetSelect6' : 'F6',

            'Pet1Name' : '',
            'Pet2Name' : '',
            'Pet3Name' : '',
            'Pet4Name' : '',
            'Pet5Name' : '',
            'Pet6Name' : '',

            'Pet1Bodyguard' : 0,
            'Pet2Bodyguard' : 1,
            'Pet3Bodyguard' : 0,
            'Pet4Bodyguard' : 0,
            'Pet5Bodyguard' : 1,
            'Pet6Bodyguard' : 0,
        }

        self.TabTitle = "Mastermind / Pet Binds"

    def BuildPage(self):

        sizer = wx.BoxSizer(wx.VERTICAL)

        # get the pet names, whether they're bodyguards, and binds to select them directly
        # TODO -- probably want to enable/disable various bits of this based on whether bodyguard is
        # active, or whether we have names, or whatever
        petNames = ControlGroup(self, self, width = 5, label = "Pet Info and Selection Binds",flexcols=[1,4])

        for PetID in range(1,7):

            petNames.AddControl(
                ctlName = f"Pet{PetID}Name",
                ctlType = 'text',
                tooltip = f"Specify Pet {PetID}'s Name for individual selection",
            )
            petNames.AddControl(
                noLabel = True,
                ctlName = f"Pet{PetID}Bodyguard",
                ctlType = 'checkbox',
                contents = "Bodyguard",
                tooltip = f"Select whether pet {PetID} acts as Bodyguard",
            )
            petNames.AddControl(
                ctlName = f"PetSelect{PetID}",
                ctlType = "keybutton",
                tooltip = f"Choose the Key Combo to Select Pet {PetID}"
            )

        # TODO - add checkbox handler to hide/show (enable/disable?) the bodyguard options
        # TODO -- actually, automagically enable/disable these depending on whether any pets have their
        # individual "Bodyguard" checkboxes checked.
        bgCB = wx.CheckBox( self, -1, 'Enable Bodyguard Mode Binds')
        bgCB.SetToolTip(wx.ToolTip('Check this to enable the Bodyguard Mode Binds'))
        bgCB.SetValue(self.Init['PetBodyguardMode'])
        self.Ctrls['EnablePetBodyguardBinds'] = bgCB

        petCommandsKeys = ControlGroup(self, self, width = 5, label = "Pet Action Binds", flexcols = [1,4])

        # shim the Chatty Mode toggle in there, above the chat responses
        useCB = petCommandsKeys.AddControl(
            ctlName = 'EnablePetActionBinds',
            ctlType = 'checkbox',
            tooltip = 'Check this to enable the Mastermind Pet Action Binds'
        )
        petCommandsKeys.AddControl(
            ctlName = 'PetChatToggle',
            ctlType = 'keybutton',
            tooltip = 'Choose the key combo that will toggle your pet\'s Chatty Mode',
        )
        petCommandsKeys.AddControl( ctlName = 'spacer3', ctlType = 'statictext', noLabel = True,)


        # Iterate the data structure at the top and make the grid of controls for the basic pet binds
        ChatOptions = ('Local','Self-Tell','Petsay','---' )
        for command in self.petCommandKeyDefinitions:

            petCommandsKeys.AddControl(
                ctlName = command['ctrlName'],
                ctlType = 'keybutton',
                tooltip = "Choose the key combo that will " + command['tooltipdetail'],
            )

            petCommandsKeys.AddControl(
                ctlName = command['ctrlName'] + 'ResponseMethod',
                ctlType = 'combobox',
                contents = ChatOptions,
                tooltip = "Choose how your pets will respond when they are in chatty mode and you " + command['tooltipdetail'],
            )
            petCommandsKeys.AddControl(
                noLabel = True,
                ctlName = command['ctrlName'] + "Response",
                ctlType = "text",
                tooltip = "Choose the chat response your pets give when you " + command['tooltipdetail'],
            )

        cbSizer = wx.BoxSizer(wx.HORIZONTAL)
        cbSizer.Add(useCB, 0, wx.ALL, 16)
        cbSizer.Add(bgCB, 0, wx.ALL, 10)

        sizer.Add(petNames, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 16)
        sizer.AddSpacer(10)
        sizer.Add(cbSizer, 0, wx.EXPAND)
        sizer.Add(petCommandsKeys, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 16)

        self.SetSizerAndFit(sizer)

        self.OnArchetypePowerChange()

    # not actually an event listener, gets called explicitly
    def OnArchetypePowerChange(self):
        arch = self.Profile.General.GetState('Archetype')
        pset = self.Profile.General.GetState('Primary')

        for _, control in self.Ctrls.items():
            control.Enable(bool(arch == "Mastermind" and pset))


    def HelpText(self):
        return """
        The Original Mastermind Control Binds
        were created in CoV Beta by Khaiba
        a.k.a. Sandolphan
        Bodyguard code inspired directly from
        Sandolphan's Bodyguard binds.
        Thugs added by Konoko!
        """

    def mmBGSelBind(self, profile, file, PetBodyguardResponse, powers):
        if (self.GetState('bg_enable')):
            #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
            #  first check if any full tier groups are bodyguards.  full tier groups are either All BG or all NBG.
            if (self.GetState('Pet1Bodyguard')) : tier1bg = tier1bg + 1
            if (self.GetState('Pet2Bodyguard')) : tier1bg = tier1bg + 1
            if (self.GetState('Pet3Bodyguard')) : tier1bg = tier1bg + 1
            if (self.GetState('Pet4Bodyguard')) : tier2bg = tier2bg + 1
            if (self.GetState('Pet5Bodyguard')) : tier2bg = tier2bg + 1
            if (self.GetState('Pet6Bodyguard')) : tier3bg = tier3bg + 1
            #  if tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
            #  if tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
            #  tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
            #  so, add all fullgroups into the bgsay command.
            #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
            if (((tier1bg + tier2bg + tier3bg) == 6) or (self.GetState('PetBodyguardResponseMethod') != 3)):
                saymethall = ("local ",'tell, $name ',"petsayall ","")
                bgsay = self.GetState('PetBodyguardResponseMethod') + PetBodyguardResponse
            else:
                if (tier1bg == 3):
                    bgsay = bgsay + f"$$petsaypow {powers['min']} {PetBodyguardResponse}"
                else:
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.GetState('Pet1Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet1Name')} {PetBodyguardResponse}"
                    if (self.GetState('Pet2Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet2Name')} {PetBodyguardResponse}"
                    if (self.GetState('Pet3Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet3Name')} {PetBodyguardResponse}"

                if (tier2bg == 2):
                    bgsay = bgsay + f"$$petsaypow {powers['lts']} {PetBodyguardResponse}"
                else:
                    if (self.GetState('Pet4Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet4Name')} {PetBodyguardResponse}"
                    if (self.GetState('Pet5Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet5Name')} {PetBodyguardResponse}"

                if (tier3bg == 1):
                    bgsay = bgsay + f"$$petsaypow {powers['bos']} {PetBodyguardResponse}"

            if ((tier1bg + tier2bg + tier3bg) == 6):
                bgset = '$$petcomall def fol'
            else:
                if (tier1bg == 3):
                    bgset = bgset + f"$$petcompow {powers['min']} def fol"
                else:
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.GetState('Pet1Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet1Name')} def fol"
                    if (self.GetState('Pet2Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet2Name')} def fol"
                    if (self.GetState('Pet3Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet3Name')} def fol"

                if (tier2bg == 2):
                    bgset = bgset + f"$$petcompow {powers['lts']} def fol"
                else:
                    if (self.GetState('Pet4Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet4Name')} def fol"
                    if (self.GetState('Pet5Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet5Name')} def fol"

                if (tier3bg == 1):
                    bgset = bgset + f"$$petcompow {powers['bos']} def fol"

            file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind([bgsay + bgset, profile.GetBindFile('mmbinds','cbguarda.txt').BLF()]))

    def mmBGActBind(self, profile, filedn, fileup, action, say, powers):

        key    = self.GetState(f"Pet{action}")
        method = self.GetState(f"Pet{action}ResponseMethod")

        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
        if (self.GetState('Pet1Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet2Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet3Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet4Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet5Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet6Bodyguard')) : tier3bg = tier3bg + 1
        #  if tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  if tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
        #  so, add all fullgroups into the bgsay command.
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if (((tier1bg + tier2bg + tier3bg) == 0) or (method != 3)):
            saymethall = ("local ",'tell, $name ',"petsayall ","")
            bgsay = method + say
        else:
            if (tier1bg == 0):
                bgsay = bgsay + f"$$petsaypow {powers['min']} $say"
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.GetState('Pet1Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet1Name')} {say}"
                if (not self.GetState('Pet2Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet2Name')} {say}"
                if (not self.GetState('Pet3Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet3Name')} {say}"

            if (tier2bg == 0):
                bgsay = bgsay + f"$$petsaypow {powers['lts']} {say}"
            else :
                if (not self.GetState('Pet4Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet4Name')} {say}"
                if (not self.GetState('Pet5Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet5Name')} {say}"

            if (tier3bg == 0):
                bgsay = bgsay + f"$$petsaypow {powers['bos']} {say}"

        if ((tier1bg + tier2bg + tier3bg) == 0):
            bgact = '$$petcomall ' + action
        else :
            if (tier1bg == 0):
                bgact = bgact + f"$$petcompow {powers['min']} {action}"
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.GetState('Pet1Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet1Name')} {action}"
                if (not self.GetState('Pet2Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet2Name')} {action}"
                if (not self.GetState('Pet3Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet3Name')} {action}"

            if (tier2bg == 0):
                bgact = bgact + f"$$petcompow {powers['lts']} {action}"
            else :
                if (not self.GetState('Pet4Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet4Name')} {action}"
                if (not self.GetState('Pet5Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet5Name')} {action}"

            if (tier3bg == 0):
                bgact = bgact + '$$petcompow ' + f"{powers['bos']} {action}"

        cbWriteToggleBind(filedn,fileup,key,bgsay,bgact,filedn.BLFPath,fileup.BLFPath)

    def mmBGActBGBind(self, profile, filedn, fileup, action, say, powers):

        key =    self.GetState( "PetBackground{action}")
        method = self.GetState(f"Pet{action}ResponseMethod")

        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
        if (self.GetState('Pet1Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet2Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet3Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet4Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet5Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet6Bodyguard')) : tier3bg = tier3bg + 1
        #  if tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  if tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
        #  so, add all fullgroups into the bgsay command.
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if (((tier1bg + tier2bg + tier3bg) == 6) or (method != 3)):
            saymethall = ("local ",'tell, $name ',"petsayall ","")
            bgsay = method + say
        else :
            if (tier1bg == 3):
                bgsay = bgsay + f"$$petsaypow {powers['min']} {say}"
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (self.GetState('Pet1Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet1Name')} {say}"
                if (self.GetState('Pet2Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet2Name')} {say}"
                if (self.GetState('Pet3Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet3Name')} {say}"

            if (tier2bg == 2):
                bgsay = bgsay + f"$$petsaypow {powers['lts']} {say}"
            else :
                if (self.GetState('Pet4Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet4Name')} {say}"
                if (self.GetState('Pet5Bodyguard')) : bgsay = bgsay + f"$$petsayname {self.GetState('Pet5Name')} {say}"

            if (tier3bg == 1):
                bgsay = bgsay + f"$$petsaypow {powers['bos']} {say}"

        if ((tier1bg + tier2bg + tier3bg) == 6):
            bgact = '$$petcomall ' + action
        else :
            if (tier1bg == 3):
                bgact = bgact + f"$$petcompow {powers['min']} {action}"
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (self.GetState('Pet1Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet1Name')} {action}"
                if (self.GetState('Pet2Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet2Name')} {action}"
                if (self.GetState('Pet3Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet3Name')} {action}"

            if (tier2bg == 2):
                bgact = bgact + f"$$petcompow {powers['lts']} {action}"
            else :
                if (self.GetState('Pet4Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet4Name')} {action}"
                if (self.GetState('Pet5Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet5Name')} {action}"

            if (tier3bg == 1):
                bgact = bgact + f"$$petcompow {powers['bos']} {action}"

        # file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind(bgsay.$bgset.BindFile.BLF($profile, 'mmbinds','\mmbinds\\cbguarda.txt')))
        cbWriteToggleBind(filedn,fileup,key,bgsay,bgact,filedn.BLFPath,fileup.BLFPath)

    def mmQuietBGSelBind(self, profile, file, powers):
        if (self.GetState('bg_enable')):
            #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
            #  first check if any full tier groups are bodyguards.  full tier groups are either All BG or all NBG.
            if (self.GetState('Pet1Bodyguard')) : tier1bg = tier1bg + 1
            if (self.GetState('Pet2Bodyguard')) : tier1bg = tier1bg + 1
            if (self.GetState('Pet3Bodyguard')) : tier1bg = tier1bg + 1
            if (self.GetState('Pet4Bodyguard')) : tier2bg = tier2bg + 1
            if (self.GetState('Pet5Bodyguard')) : tier2bg = tier2bg + 1
            if (self.GetState('Pet6Bodyguard')) : tier3bg = tier3bg + 1
            #  if tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
            #  if tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
            #  tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
            #  so, add all fullgroups into the bgsay command.
            #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
            if ((tier1bg + tier2bg + tier3bg) == 6):
                bgset = "petcomall def fol"
            else :
                if (tier1bg == 3):
                    bgset = bgset + f"$$petcompow {powers['min']} def fol"
                else :
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.GetState('Pet1Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet1Name')} def fol"
                    if (self.GetState('Pet2Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet2Name')} def fol"
                    if (self.GetState('Pet3Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet3Name')} def fol"

                if (tier2bg == 2):
                    bgset = bgset + f"$$petcompow {powers['lts']} def fol"
                else :
                    if (self.GetState('Pet4Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet4Name')} def fol"
                    if (self.GetState('Pet5Bodyguard')) : bgset = bgset + f"$$petcomname {self.GetState('Pet5Name')} def fol"

                if (tier3bg == 1):
                    bgset = bgset + f"$$petcompow {powers['bos']} def fol"

            file.SetBind(self.Ctrls['PetBodyguard'].MakeFileKeyBind([bgset, profile.GetBindFile('mmbinds','mmbinds','bguarda.txt').BLF()]))

    def mmQuietBGActBind(self, profile, filedn, fileup, action, powers):

        key = self.GetState(f"PetBackground{action}")

        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
        if (self.GetState('Pet1Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet2Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet3Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet4Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet5Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet6Bodyguard')) : tier3bg = tier3bg + 1
        #  if tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  if tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
        #  so, add all fullgroups into the bgsay command.
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if ((tier1bg + tier2bg + tier3bg) == 0):
            bgact = "petcomall $action"
        else :
            if (tier1bg == 0):
                bgact = bgact + f"$$petcompow {powers['min']} {action}"
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.GetState('Pet1Bodyguard')): bgact = bgact + f"$$petcomname {self.GetState('Pet1Name')} {action}"
                if (not self.GetState('Pet2Bodyguard')): bgact = bgact + f"$$petcomname {self.GetState('Pet2Name')} {action}"
                if (not self.GetState('Pet3Bodyguard')): bgact = bgact + f"$$petcomname {self.GetState('Pet3Name')} {action}"

            if (tier2bg == 0):
                bgact = bgact + f"$$petcompow {powers['lts']} {action}"
            else :
                if (not self.GetState('Pet4Bodyguard')): bgact = bgact + f"$$petcomname {self.GetState('Pet4Name')} {action}"
                if (not self.GetState('Pet5Bodyguard')): bgact = bgact + f"$$petcomname {self.GetState('Pet5Name')} {action}"

            if (tier3bg == 0): bgact = bgact + f"$$petcompow {powers['bos']} {action}"

        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(key, "bgact", "Mastermind", bgact)

    def mmQuietBGActBGBind(self, profile, filedn, fileup, action, powers):

        key    = self.GetState("PetBackground$action")
        method = self.GetState("Pet${action}ResponseMethod")

        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
        if (self.GetState('Pet1Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet2Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet3Bodyguard')) : tier1bg = tier1bg + 1
        if (self.GetState('Pet4Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet5Bodyguard')) : tier2bg = tier2bg + 1
        if (self.GetState('Pet6Bodyguard')) : tier3bg = tier3bg + 1
        #  if tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  if tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
        #  tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
        #  so, add all fullgroups into the bgsay command.
        #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
        if ((tier1bg + tier2bg + tier3bg) == 6):
            bgact = "petcomall $action"
        else :
            if (tier1bg == 3):
                bgact = bgact + f"$$petcompow {powers['min']} {action}"
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (self.GetState('Pet1Bodyguard')): bgact = bgact + f"$$petcomname {self.GetState('Pet1Name')} {action}"
                if (self.GetState('Pet2Bodyguard')): bgact = bgact + f"$$petcomname {self.GetState('Pet2Name')} {action}"
                if (self.GetState('Pet3Bodyguard')): bgact = bgact + f"$$petcomname {self.GetState('Pet3Name')} {action}"

            if (tier2bg == 2):
                bgact = bgact + f"$$petcompow  {powers['lts']} {action}"
            else :
                if (self.GetState('Pet4Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet4Name')} {action}"
                if (self.GetState('Pet5Bodyguard')) : bgact = bgact + f"$$petcomname {self.GetState('Pet5Name')} {action}"

            if (tier3bg == 1) : bgact = bgact + f"$$petcompow {powers['bos']} {action}"

        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(key, "bgact", "Mastermind", bgact)

    def mmSubBind(self, profile, file, fn, grp, powers):
        PetResponses = {}
        for cmd  in ('SelectAll', 'SelectMinions', 'SelectLieutenants', 'SelectBoss', 
                'Aggressive', 'Defensive', 'Passive', 'Attack', 'Follow', 'Goto', 'Stay','Bodyguard',):
            PetResponses[cmd] = ''
            if (self.GetState(f"Pet{cmd}ResponseMethod") != 'None') : PetResponses[cmd] = self.GetState(f"Pet{cmd}Response")

        file.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind([
                     self.GetState('PetSelectAllResponseMethod') + f" {PetResponses['SelectAll']}", profile.GetBindFile('mmbinds','call.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind([
                     self.GetState('PetSelectMinionsResponseMethod') + f" {PetResponses['SelectMinions']}", profile.GetBindFile('mmbinds','ctier1.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind([
                     self.GetState('PetSelectLieutenantsResponseMethod') + f" {PetResponses['SelectLieutenants']}", profile.GetBindFile('mmbinds','ctier2.txt').BLF()]))
        file.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind([
                     self.GetState('PetSelectBossResponseMethod') + f" {PetResponses['SelectBoss']}", profile.GetBindFile('mmbinds','ctier3.txt').BLF()]))

        self.mmBGSelBind(profile,file,PetResponses['Bodyguard'],powers)

        if grp: petcom = f"$$petcompow {grp}"
        else:   petcom =  "petcomall"
        for cmd in ('Aggressive','Defensive','Attack','Follow','Goto', 'Stay'):
            print(cmd)
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(self.GetState(f"Pet{cmd}ResponseMethod") + f" {PetResponses[cmd]}{petcom} {cmd}"))

        if (self.GetState('PetBackgroundAttackEnabled'))  : file.SetBind(self.Ctrls['PetBackgroundAttack'].MakeFileKeyBind('nop'))
        if (self.GetState('PetBackgroundGotoenabled'))    : file.SetBind(self.Ctrls['PetBackgroundGoto'].MakeFileKeyBind('nop'))
        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.GetBindFile('mmbinds',f"{fn}.txt").BLF()]))

    def mmBGSubBind(self, profile, filedn, fileup, fn, powers):
        PetResponses = {}
        for cmd in ('SelectAll','SelectMinions','SelectLieutenants','SelectBoss','Aggressive','Defensive','Passive','Attack','Follow','Goto', 'Stay', 'Bodyguard',):
            if (self.GetState(f'Pet{cmd}ResponseMethod') != None) : PetResponses[cmd] = self.GetState(f'Pet{cmd}Response')

        filedn.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind([self.GetState('PetSelectAllResponseMethod') + f" {PetResponses['SelectAll']}", profile.GetBindFile('mmbinds','call.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind([self.GetState('PetSelectMinionsResponseMethod') + f" {PetResponses['SelectMinions']}", profile.GetBindFile('mmbinds','ctier1.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind([self.GetState('PetSelectLieutenantsResponseMethod') + f" {PetResponses['SelectLieutenants']}", profile.GetBindFile('mmbinds','ctier2.txt').BLF()]))
        filedn.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind([self.GetState('PetSelectBossResponseMethod') + f" {PetResponses['SelectBoss']}", profile.GetBindFile('mmbinds','ctier3.txt').BLF()]))
        self.mmBGSelBind(profile,filedn,PetResponses['Bodyguard'],powers)

        for cmd in ('Aggressive','Defensive','Attack','Follow','Goto', 'Stay'):
            self.mmBGActBind(profile, filedn, fileup, cmd, PetResponses[cmd], powers)

        if (self.GetState('PetBackgroundAttackenabled')):
            self.mmBGActBGBind( profile, filedn, fileup,'Attack', PetResponses['Attack'], powers)

        if (self.GetState('PetBackgroundGotoenabled')):
            self.mmBGActBGBind( profile, filedn, fileup,'Goto', PetResponses['Goto'], powers)

        filedn.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.GetBindFile('mmbinds',f"{fn}a.txt").BLF()]))

    def mmQuietSubBind(self, profile, file, fn, grp, powers):
        file.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind(profile.GetBindFile('mmbinds','all.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier1.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier2.txt').BLF()))
        file.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier3.txt').BLF()))
        self.mmQuietBGSelBind(profile, file, powers)

        if grp: petcom = f"$$petcompow {grp}"
        else:   petcom =  '$$petcomall'
        for cmd in ('Aggressive','Defensive','Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(f"{petcom} {cmd}"))

        if (self.GetState('PetBackgroundAttackenabled'))  : file.SetBind(self.Ctrls['PetBackgroundAttack'].MakeFileKeyBind('nop'))
        if (self.GetState('PetBackgroundGotoenabled'))    : file.SetBind(self.Ctrls['PetBackgroundGoto'].MakeFileKeyBind('nop'))

        file.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind('tell $name, Chatty Mode' + profile.GetBindFile('mmbinds','c' + fn + '.txt').BLF()))

    def mmQuietBGSubBind(self, profile, filedn, fileup, fn, powers):
        filedn.SetBind(self.Ctrls['PetSelectAll'].MakeFileKeyBind(profile.GetBindFile('mmbinds','all.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectMinions'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier1.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier2.txt').BLF()))
        filedn.SetBind(self.Ctrls['PetSelectBoss'].MakeFileKeyBind(profile.GetBindFile('mmbinds','tier3.txt').BLF()))

        self.mmQuietBGSelBind(profile,filedn,powers)
        for cmd in ('Aggressive','Defensive','Passive','Attack','Follow','Goto', 'Stay'):
            self.mmQuietBGActBind(profile, filedn, fileup, cmd, powers)

        if (self.GetState('PetBackgroundAttackenabled')):
            self.mmQuietBGActBGBind(profile, filedn, fileup,'Attack', powers)

        if (self.GetState('PetBackgroundGotoenabled')):
            self.mmQuietBGActBGBind(profile, filedn, fileup,'Goto', powers)

        filedn.SetBind(self.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Chatty Mode', profile.GetBindFile('mmbinds','c' + fn + 'a.txt').BLF()]))

    def PopulateBindFiles(self):

        ### TODO
        #return
        ### TODO

        profile = self.Profile

        ResetFile = profile.ResetFile()

        if (self.GetState('petselenable')):
            if (self.GetState('Pet1Nameenabled')) : ResetFile.SetBind(self.Ctrls['sel0'].MakeFileKeyBind(f"petselectname {self.GetState('Pet1Name')}"))
            if (self.GetState('Pet2Nameenabled')) : ResetFile.SetBind(self.Ctrls['sel1'].MakeFileKeyBind(f"petselectname {self.GetState('Pet2Name')}"))
            if (self.GetState('Pet3Nameenabled')) : ResetFile.SetBind(self.Ctrls['sel2'].MakeFileKeyBind(f"petselectname {self.GetState('Pet3Name')}"))
            if (self.GetState('Pet4Nameenabled')) : ResetFile.SetBind(self.Ctrls['sel3'].MakeFileKeyBind(f"petselectname {self.GetState('Pet4Name')}"))
            if (self.GetState('Pet5Nameenabled')) : ResetFile.SetBind(self.Ctrls['sel4'].MakeFileKeyBind(f"petselectname {self.GetState('Pet5Name')}"))
            if (self.GetState('Pet6Nameenabled')) : ResetFile.SetBind(self.Ctrls['sel5'].MakeFileKeyBind(f"petselectname {self.GetState('Pet6Name')}"))

        allfile = profile.GetBindFile('mmbinds','all.txt')
        minfile = profile.GetBindFile('mmbinds','tier1.txt')
        ltsfile = profile.GetBindFile('mmbinds','tier2.txt')
        bosfile = profile.GetBindFile('mmbinds','tier3.txt')

        if (self.GetState('bg_enable')):
            bgfiledn = profile.GetBindFile('mmbinds','bguarda.txt')
            #  since we never need to split lines up in this fashion
            #  comment the next line out so an empty file is not created.
            # bgfileup = $profile.GetBindFile($profile['base'] + "\\mmbinds\\bguardb.txt")

        callfile = profile.GetBindFile('mmbinds','call.txt')
        cminfile = profile.GetBindFile('mmbinds','ctier1.txt')
        cltsfile = profile.GetBindFile('mmbinds','ctier2.txt')
        cbosfile = profile.GetBindFile('mmbinds','ctier3.txt')

        if (self.GetState('bg_enable')):
            cbgfiledn = profile.GetBindFile('mmbinds','cbguarda.txt')
            cbgfileup = profile.GetBindFile('mmbinds','cbguardb.txt')

        # TODO!!!  get this into / from GameData
        self.MMPowerSets = {
            "Beast Mastery"   : { 'min' : 'wol', 'lts'  : 'lio', 'bos'  : 'dir' },
            "Demon Summoning" : { 'min' : 'lin', 'lts'  : 'mons', 'bos' : 'pri' },
            "Mercenaries"     : { 'min' : "sol",  'lts' : "spec", 'bos' : "com", },
            "Necromancy"      : { 'min' : "zom",  'lts' : "grav", 'bos' : "lich", },
            "Ninjas"          : { 'min' : "gen",  'lts' : "joun", 'bos' : "oni", },
            "Robotics"        : { 'min' : "dron", 'lts' : "prot", 'bos' : "ass", },
            "Thugs"           : { 'min' : "thu",  'lts' : "enf",  'bos' : "bru", },
        }
        powers = self.MMPowerSets[ profile.General.GetState('Primary') ]

        # "Local","Self-Tell","Petsay","None"
        self.mmSubBind(profile, ResetFile,"all",None, powers)
        self.mmQuietSubBind(profile, allfile,"all",None, powers)
        self.mmQuietSubBind(profile,minfile,"tier1",powers['min'],powers)
        self.mmQuietSubBind(profile,ltsfile,"tier2",powers['lts'],powers)
        self.mmQuietSubBind(profile,bosfile,"tier3",powers['bos'],powers)
        if (self.GetState('bg_enable')):
            self.mmQuietBGSubBind(profile,bgfiledn,bgfileup,"bguard",powers)

        self.mmSubBind(profile,callfile,"all",None,powers)
        self.mmSubBind(profile,cminfile,"tier1",powers['min'],powers)
        self.mmSubBind(profile,cltsfile,"tier2",powers['lts'],powers)
        self.mmSubBind(profile,cbosfile,"tier3",powers['bos'],powers)

        if (self.GetState('bg_enable')): self.mmBGSubBind(profile,cbgfiledn,cbgfileup,"bguard",powers)

    def findconflicts(self):
        if (self.GetState('petselenable')) :
            for i in range(1,7):
                if (self.GetState(f'pet{i}nameenabled')): cbCheckConflict(self.State, f"sel{i-1}Select Pet {i}")

        cbCheckConflict(self.GetState("PetSelectAll")         , "Select All Pets")
        cbCheckConflict(self.GetState("PetSelectMinions")     , "Select Minions")
        cbCheckConflict(self.GetState("PetSelectLieutenants") , "Select Lieutenants")
        cbCheckConflict(self.GetState("PetSelectBoss")        , "Select Boss Pet")
        cbCheckConflict(self.GetState("PetAggressive")        , "Set Pets Aggressive")
        cbCheckConflict(self.GetState("PetDefensive")         , "Set Pets Defensive")
        cbCheckConflict(self.GetState("PetPassive")           , "Set Pets Passive")
        cbCheckConflict(self.GetState("PetAttack")            , "Pet Order: Attack")
        cbCheckConflict(self.GetState("PetFollow")            , "Pet Order: Follow")
        cbCheckConflict(self.GetState("PetStay")              , "Pet Order: Stay")
        cbCheckConflict(self.GetState("PetGoto")              , "Pet Order: Goto")
        cbCheckConflict(self.GetState("PetChatToggle")        , "Pet Action Bind Chatty Mode Toggle")
        if (self.GetState('bg_enable')):
            cbCheckConflict(self.GetState("PetBodyguard"),"Bodyguard Mode")
            if (self.GetState('PetBackgroundAttackenabled')) : cbCheckConflict(self.GetState("PetBackgroundAttack"),"Pet Order: BG Attack")
            if (self.GetState('PetBackgroundGotoenabled'))   : cbCheckConflict(self.GetState("PetBackgroundGoto")  ,"Pet Order: BG Goto")

    def bindisused(self): return profile.Mastermind['enabled']


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
            'PetSelectAllResponseMethod'         : "Response to Select All",
            'PetSelectMinionsResponseMethod'     : "Response to Select Minions",
            'PetSelectLieutenantsResponseMethod' : "Response to Select Lieutenants",
            'PetSelectBossResponseMethod'        : "Response to Select Boss",
            'PetAggressiveResponseMethod'        : "Response to Set Aggressive",
            'PetDefensiveResponseMethod'         : "Response to Set Defensive",
            'PetPassiveResponseMethod'           : "Response to Set Passive",
            'PetAttackResponseMethod'            : "Response to Attack",
            'PetFollowResponseMethod'            : "Response to Follow",
            'PetGotoResponseMethod'              : "Response to Goto",
            'PetStayResponseMethod'              : "Response to Stay",
            'PetBodyguardResponseMethod'         : "Response to Bodyguard Mode",
            'EnablePetActionBinds'               : "Enable Pet Action Binds",
            'PetChatToggle'                      : "Chat Mode Toggle",
        })
