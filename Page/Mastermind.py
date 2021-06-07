import wx

from Page import Page

import BindFile

class Mastermind(Page):
    petCommandKeyDefinitions = (
            {
                'label'      : 'Select All',
                'basename'      : 'PetSelectAll',
                'tooltipdetail' : 'select all of your pets',
            },
            {
                'label'      : 'Select Minions',
                'basename'      : 'PetSelectMinions',
                'tooltipdetail' : 'select your "minion" pets',
            },
            {
                'label'      : 'Select Lieutenants',
                'basename'      : 'PetSelectLieutenants',
                'tooltipdetail' : 'select your "lieutenant" pets',
            },
            {
                'label'      : 'Select Boss',
                'basename'      : 'PetSelectBoss',
                'tooltipdetail' : 'select your "boss" pet',
            },
            {
                'label'      : 'Bodyguard',
                'basename'      : 'PetBodyguard',
                'tooltipdetail' : 'put your selected pets into Bodyguard mode',
            },
            {
                'label'      : 'Aggressive',
                'basename'      : 'PetAggressive',
                'tooltipdetail' : 'set your selected pets to "Aggressive" mode',
            },
            {
                'label'      : 'Defensive',
                'basename'      : 'PetDefensive',
                'tooltipdetail' : 'set your selected pets to "Defensive" mode',
            },
            {
                'label'      : 'Passive',
                'basename'      : 'PetPassive',
                'tooltipdetail' : 'set your selected pets to "Passive" mode',
            },
            {
                'label'      : 'Attack',
                'basename'      : 'PetAttack',
                'tooltipdetail' : 'order your selected pets to Attack your target',
            },
            {
                'label'      : 'Follow',
                'basename'      : 'PetFollow',
                'tooltipdetail' : 'order your selected pets to Follow you',
            },
            {
                'label'      : 'Stay',
                'basename'      : 'PetStay',
                'tooltipdetail' : 'order your selected pets to Stay at their current location',
            },
            {
                'label'      : 'Go To',
                'basename'      : 'PetGoto',
                'tooltipdetail' : 'order your selected pets to Go To a targeted location',
            },
        )

    def __init__(self, parent):
        Page.__init__(self, parent)

        self.State = {
            'Enable' : False,

            'PetSelectAll' : 'ALT+V',
            'PetSelectAllResponse' : 'Orders?',
            'PetSelectAllResponseMethod' : 'Petsay',

            'PetSelectMinions' : 'ALT+Z',
            'PetSelectMinionsResponse' : 'Orders?',
            'PetSelectMinionsResponseMethod' : 'Petsay',

            'PetSelectLieutenants' : 'ALT+X',
            'PetSelectLieutenantsResponse' : 'Orders?',
            'PetSelectLieutenantsResponseMethod' : 'Petsay',

            'PetSelectBoss' : 'ALT+C',
            'PetSelectBossResponse' : 'Orders?',
            'PetSelectBossResponseMethod' : 'Petsay',

            'PetBodyguard' : 'ALT+G',
            'PetBodyguardResponse' : 'Bodyguarding.',
            'PetBodyguardResponseMethod' : 'Petsay',

            'PetAggressive' : 'ALT+A',
            'PetAggressiveResponse' : 'Kill On Sight.',
            'PetAggressiveResponseMethod' : 'Petsay',

            'PetDefensive' : 'ALT+S',
            'PetDefensiveResponse' : 'Return Fire Only.',
            'PetDefensiveResponseMethod' : 'Petsay',

            'PetPassive' : 'ALT+D',
            'PetPassiveResponse' : 'At Ease.',
            'PetPassiveResponseMethod' : 'Petsay',

            'PetAttack' : 'ALT+Q',
            'PetAttackResponse' : 'Open Fire!',
            'PetAttackResponseMethod' : 'Petsay',

            'PetFollow' : 'ALT+W',
            'PetFollowResponse' : 'Falling In.',
            'PetFollowResponseMethod' : 'Petsay',

            'PetStay' : 'ALT+E',
            'PetStayResponse' : 'Holding This Position',
            'PetStayResponseMethod' : 'Petsay',

            'PetGoto' : 'ALT+LBUTTON',
            'PetGotoResponse' : 'Moving To Checkpoint.',
            'PetGotoResponseMethod' : 'Petsay',

            'PetBodyguardMode' : 1,
            'PetBodyguardAttack' : '',
            'PetBodyguardGoto' : '',

            'PetBackgroundAttack' : 'UNBOUND', # TODO -- need UI for this
            'PetBackgroundGoto' : 'UNBOUND',   # TODO -- need UI for this
            'PetBackgroundAttackEnabled' : 0,  # TODO -- need UI for this
            'PetBackgroundGotoEnabled' : 0,    # TODO -- need UI for this

            'PetChatToggle' : 'ALT+M',
            'PetSelect1' : 'F1',
            'PetSelect2' : 'F2',
            'PetSelect3' : 'F3',
            'PetSelect4' : 'F4',
            'PetSelect5' : 'F5',
            'PetSelect6' : 'F6',

            'Pet1Name' : 'Crow T Robot',
            'Pet2Name' : 'Tom Servo',
            'Pet3Name' : 'Cambot',
            'Pet4Name' : 'Gypsy',
            'Pet5Name' : 'Mike',
            'Pet6Name' : 'Joel',

            'Pet1Bodyguard' : 0,
            'Pet2Bodyguard' : 1,
            'Pet3Bodyguard' : 0,
            'Pet4Bodyguard' : 0,
            'Pet5Bodyguard' : 1,
            'Pet6Bodyguard' : 0,
        }

        self.TabTitle = "Mastermind / Pet Binds"

    def FillTab(self):

        sizer = wx.BoxSizer(wx.VERTICAL)

        useCB = wx.CheckBox( self, -1, 'Enable Mastermind Pet Binds')
        useCB.SetToolTip(wx.ToolTip('Check this to enable the Mastermind Pet Action Binds'))
        sizer.Add(useCB, 0, wx.ALL, 10)

        # TODO - add checkbox handler to hide/show (enable/disable?) the bodyguard options
        # TODO -- actually, automagically enable/disable these depending on whether any pets have their
        # individual "Bodyguard" checkboxes checked.
        bgCB = wx.CheckBox( self, -1, 'Enable Bodyguard Mode Binds')
        bgCB.SetToolTip(wx.ToolTip('Check this to enable the Bodyguard Mode Binds'))
        bgCB.SetValue(self.State['PetBodyguardMode'])
        sizer.Add(bgCB, 0, wx.ALL, 10)

        sizer.AddSpacer(10)

        # Iterate the data structure at the bottom and make the grid of controls for the basic pet binds
        ChatOptions = ('Local','Self-Tell','Petsay','---' )
        PetCommandKeyRows = wx.FlexGridSizer(0,5,2,2)
        for k in self.petCommandKeyDefinitions:

            basename = k['basename'];  # all of the fieldnames we look up in the MMP are based on this value

            al = wx.StaticText(self, -1, k['label'])
            ab = wx.Button    (self, -1, self.State[basename])

            cl = wx.StaticText(self, -1, "Respond via:")
            cm = wx.ComboBox  (self, -1, self.State[f"{basename}ResponseMethod"],
                    wx.DefaultPosition, wx.DefaultSize, ChatOptions, wx.CB_READONLY)
            cr = wx.TextCtrl  (self, -1, self.State[f"{basename}Response"])

            tip = k['tooltipdetail']
            ab.SetToolTip( wx.ToolTip("Choose the key combo that will $tip"))
            cm.SetToolTip( wx.ToolTip("Choose the method your pets will use to respond when they are in chatty mode and you $tip"))
            cr.SetToolTip( wx.ToolTip("Choose the chat response your pets will give when you $tip"))
            cr.SetMinSize( [250, -1] )

            PetCommandKeyRows.Add(al, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            PetCommandKeyRows.Add(ab, 0, wx.EXPAND)
            PetCommandKeyRows.Add(cl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            PetCommandKeyRows.Add(cm)
            PetCommandKeyRows.Add(cr, 0, wx.EXPAND)

        sizer.Add(PetCommandKeyRows)

        sizer.AddSpacer(15)

        # get the pet names, whether they're bodyguards, and binds to select them directly
        # TODO -- probably want to enable/disable various bits of this based on whether bodyguard is
        # active, or whether we have names, or whatever
        PetNames = wx.FlexGridSizer(0,5,5,5)
        for PetID in range(1,7):

            pn = wx.TextCtrl(self,  -1, self.State[f"Pet{PetID}Name"])
            pn.SetToolTip( wx.ToolTip(f"Specify Pet {PetID}'s Name for individual selection") )

            cb = wx.CheckBox(self, -1, "Bodyguard" )
            cb.SetValue(self.State[f"Pet{PetID}Bodyguard"])
            cb.SetToolTip( wx.ToolTip(f"Select whether pet {PetID} acts as Bodyguard") )

            bn = wx.Button(self, -1, self.State[f"PetSelect{PetID}"])
            bn.SetToolTip( wx.ToolTip(f"Choose the Key Combo to Select Pet {PetID}"))

            PetNames.Add( wx.StaticText(self, -1, f"Pet {PetID}'s Name"), 0, wx.ALIGN_CENTER_VERTICAL)
            PetNames.Add( pn )
            PetNames.Add( cb, 0, wx.ALIGN_CENTER_VERTICAL)
            PetNames.Add( wx.StaticText(self, -1, f"Select Pet {PetID}"), 0, wx.ALIGN_CENTER_VERTICAL)
            PetNames.Add( bn )

        sizer.Add(PetNames)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(sizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizerAndFit(paddingSizer)

    def HelpText(self):
        """
        The Original Mastermind Control Binds
        were created in CoV Beta by Khaiba
        a.k.a. Sandolphan
        Bodyguard code inspired directly from
        Sandolphan's Bodyguard binds.
        Thugs added by Konoko!
        """

    def mmBGSelBind(self, profile, file, PetBodyguardResponse, powers):
        MMP =    profile.Pages['MastermindPets'].State
        if (self.State['bg_enable']):
            #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
            #  first check if any full tier groups are bodyguards.  full tier groups are either All BG or all NBG.
            if (self.State['Pet1Bodyguard']) : tier1bg = tier1bg + 1
            if (self.State['Pet2Bodyguard']) : tier1bg = tier1bg + 1
            if (self.State['Pet3Bodyguard']) : tier1bg = tier1bg + 1
            if (self.State['Pet4Bodyguard']) : tier2bg = tier2bg + 1
            if (self.State['Pet5Bodyguard']) : tier2bg = tier2bg + 1
            if (self.State['Pet6Bodyguard']) : tier3bg = tier3bg + 1
            #  if tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
            #  if tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
            #  tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
            #  so, add all fullgroups into the bgsay command.
            #  first check if tier1bg + tier2bg + tier3bg == 6, if so, we can get away with petsayall.
            if (((tier1bg + tier2bg + tier3bg) == 6) or (self.State['PetBodyguardResponseMethod'] != 3)):
                saymethall = ("local ",'tell, $name ',"petsayall ","")
                bgsay = self.State['PetBodyguardResponseMethod'] + PetBodyguardResponse
            else:
                if (tier1bg == 3):
                    bgsay = bgsay + f"$$petsaypow {powers['min']} {PetBodyguardResponse}"
                else:
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.State['Pet1Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet1Name']} {PetBodyguardResponse}"
                    if (self.State['Pet2Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet2Name']} {PetBodyguardResponse}"
                    if (self.State['Pet3Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet3Name']} {PetBodyguardResponse}"

                if (tier2bg == 2):
                    bgsay = bgsay + f"$$petsaypow ltspow {PetBodyguardResponse}"
                else:
                    if (self.State['Pet4Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet4Name']} {PetBodyguardResponse}" 
                    if (self.State['Pet5Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet5Name']} {PetBodyguardResponse}" 

                if (tier3bg == 1):
                    bgsay = bgsay + f"$$petsaypow {powers['bos']} {PetBodyguardResponse}"

            if ((tier1bg + tier2bg + tier3bg) == 6):
                bgset = '$$petcomall def fol'
            else:
                if (tier1bg == 3):
                    bgset = bgset + f"$$petcompow {powers['min']} def fol"
                else:
                    #  use petsayname commands for those tier1s that are bodyguards.
                    if (self.State['Pet1Bodyguard']) : bgset = bgset + f"$$petcomname {self.State['Pet1Name']} def fol"
                    if (self.State['Pet2Bodyguard']) : bgset = bgset + f"$$petcomname {self.State['Pet2Name']} def fol"
                    if (self.State['Pet3Bodyguard']) : bgset = bgset + f"$$petcomname {self.State['Pet3Name']} def fol"

                if (tier2bg == 2):
                    bgset = bgset + f"$$petcompow {powers['lts']} def fol"
                else:
                    if (self.State['Pet4Bodyguard']) : bgset = bgset + f"$$petcomname {self.State['Pet4Name']} def fol" 
                    if (self.State['Pet5Bodyguard']) : bgset = bgset + f"$$petcomname {self.State['Pet5Name']} def fol" 

                if (tier3bg == 1):
                    bgset = bgset + f"$$petcompow {powers['bos']} def fol"

            file.SetBind(self.State[ 'selbgm' ], bgsay + bgset + BindFile.BLF(profile, 'mmbinds','\cbguarda.txt'))

    def mmBGActBind(self, profile, filedn, fileup, action, say, powers):

        MMP =    profile.Pages['MastermindPets'].State
        key    = self.State[f"Pet{action}"]
        method = self.State[f"Pet{action}ResponseMethod"]

        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
        if (self.State['Pet1Bodyguard']) : tier1bg = tier1bg + 1
        if (self.State['Pet2Bodyguard']) : tier1bg = tier1bg + 1
        if (self.State['Pet3Bodyguard']) : tier1bg = tier1bg + 1
        if (self.State['Pet4Bodyguard']) : tier2bg = tier2bg + 1
        if (self.State['Pet5Bodyguard']) : tier2bg = tier2bg + 1
        if (self.State['Pet6Bodyguard']) : tier3bg = tier3bg + 1
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
                if (not self.State['Pet1Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet1Name']} {say}" 
                if (not self.State['Pet2Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet2Name']} {say}" 
                if (not self.State['Pet3Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet3Name']} {say}" 

            if (tier2bg == 0):
                bgsay = bgsay + f"$$petsaypow {powers['lts']} {say}"
            else :
                if (not self.State['Pet4Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet4Name']} {say}" 
                if (not self.State['Pet5Bodyguard']) : bgsay = bgsay + f"$$petsayname {self.State['Pet5Name']} {say}" 

            if (tier3bg == 0):
                bgsay = bgsay + f"$$petsaypow {powers['bos']} {say}"

        if ((tier1bg + tier2bg + tier3bg) == 0):
            bgact = '$$petcomall ' + action
        else :
            if (tier1bg == 0):
                bgact = bgact + f"$$petcompow {powers['min']} {action}"
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (not self.State['Pet1Bodyguard']) : bgact = bgact + f"$$petcomname {self.State['Pet1Name']} {action}" 
                if (not self.State['Pet2Bodyguard']) : bgact = bgact + f"$$petcomname {self.State['Pet2Name']} {action}" 
                if (not self.State['Pet3Bodyguard']) : bgact = bgact + f"$$petcomname {self.State['Pet3Name']} {action}" 

            if (tier2bg == 0):
                bgact = bgact + f"$$petcompow {powers['lts']} {action}"
            else :
                if (not self.State['Pet4Bodyguard']) : bgact = bgact + f"$$petcomname {self.State['Pet4Name']} {action}" 
                if (not self.State['Pet5Bodyguard']) : bgact = bgact + f"$$petcomname {self.State['Pet5Name']} {action}" 

            if (tier3bg == 0):
                bgact = bgact + '$$petcompow ' + f"{powers['bos']} {action}"

        cbWriteToggleBind(filedn,fileup,key,bgsay,bgact,filedn.BLFPath,fileup.BLFPath)

    def mmBGActBGBind(self, profile, filedn, fileup, action, say, powers):

        MMP =    profile.Pages['MastermindPets'].State
        key =    MMP[ "PetBackground{action}"]
        method = MMP[f"Pet{action}ResponseMethod"]

        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
        if (MMP['Pet1Bodyguard']) : tier1bg = tier1bg + 1
        if (MMP['Pet2Bodyguard']) : tier1bg = tier1bg + 1
        if (MMP['Pet3Bodyguard']) : tier1bg = tier1bg + 1
        if (MMP['Pet4Bodyguard']) : tier2bg = tier2bg + 1
        if (MMP['Pet5Bodyguard']) : tier2bg = tier2bg + 1
        if (MMP['Pet6Bodyguard']) : tier3bg = tier3bg + 1
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
                if (MMP['Pet1Bodyguard']) : bgsay = bgsay + f"$$petsayname {MMP['Pet1Name']} {say}" 
                if (MMP['Pet2Bodyguard']) : bgsay = bgsay + f"$$petsayname {MMP['Pet2Name']} {say}" 
                if (MMP['Pet3Bodyguard']) : bgsay = bgsay + f"$$petsayname {MMP['Pet3Name']} {say}" 

            if (tier2bg == 2):
                bgsay = bgsay + f"$$petsaypow {powers['lts']} {say}"
            else :
                if (MMP['Pet4Bodyguard']) : bgsay = bgsay + f"$$petsayname {MMP['Pet4Name']} {say}" 
                if (MMP['Pet5Bodyguard']) : bgsay = bgsay + f"$$petsayname {MMP['Pet5Name']} {say}" 

            if (tier3bg == 1):
                bgsay = bgsay + f"$$petsaypow {powers['bos']} {say}"

        if ((tier1bg + tier2bg + tier3bg) == 6):
            bgact = '$$petcomall ' + action
        else :
            if (tier1bg == 3):
                bgact = bgact + f"$$petcompow {powers['min']} {action}"
            else :
                #  use petsayname commands for those tier1s that are bodyguards.
                if (MMP['Pet1Bodyguard']) : bgact = bgact + f"$$petcomname {MMP['Pet1Name']} {action}" 
                if (MMP['Pet2Bodyguard']) : bgact = bgact + f"$$petcomname {MMP['Pet2Name']} {action}" 
                if (MMP['Pet3Bodyguard']) : bgact = bgact + f"$$petcomname {MMP['Pet3Name']} {action}" 

            if (tier2bg == 2):
                bgact = bgact + f"$$petcompow {powers['lts']} {action}"
            else :
                if (MMP['Pet4Bodyguard']) : bgact = bgact + f"$$petcomname {MMP['Pet4Name']} {action}" 
                if (MMP['Pet5Bodyguard']) : bgact = bgact + f"$$petcomname {MMP['Pet5Name']} {action}" 

            if (tier3bg == 1):
                bgact = bgact + f"$$petcompow {powers['bos']} {action}"

        # file.SetBind(MMP['selbgm'],bgsay.$bgset.BindFile.BLF($profile, 'mmbinds','\mmbinds\\cbguarda.txt'))
        cbWriteToggleBind(filedn,fileup,key,bgsay,bgact,filedn.BLFPath,fileup.BLFPath)

    def mmQuietBGSelBind(self, profile, file, powers):
        MMP =    profile.Pages['MastermindPets'].State
        if (MMP['bg_enable']):
            #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
            #  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
            if (MMP['Pet1Bodyguard']) : tier1bg = tier1bg + 1
            if (MMP['Pet2Bodyguard']) : tier1bg = tier1bg + 1
            if (MMP['Pet3Bodyguard']) : tier1bg = tier1bg + 1
            if (MMP['Pet4Bodyguard']) : tier2bg = tier2bg + 1
            if (MMP['Pet5Bodyguard']) : tier2bg = tier2bg + 1
            if (MMP['Pet6Bodyguard']) : tier3bg = tier3bg + 1
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
                    if (MMP['Pet1Bodyguard']) : bgset = bgset + f"$$petcomname {MMP['Pet1Name']} def fol" 
                    if (MMP['Pet2Bodyguard']) : bgset = bgset + f"$$petcomname {MMP['Pet2Name']} def fol" 
                    if (MMP['Pet3Bodyguard']) : bgset = bgset + f"$$petcomname {MMP['Pet3Name']} def fol" 

                if (tier2bg == 2):
                    bgset = bgset + f"$$petcompow {powers['lts']} def fol"
                else :
                    if (MMP['Pet4Bodyguard']) : bgset = bgset + f"$$petcomname {MMP['Pet4Name']} def fol" 
                    if (MMP['Pet5Bodyguard']) : bgset = bgset + f"$$petcomname {MMP['Pet5Name']} def fol" 

                if (tier3bg == 1):
                    bgset = bgset + f"$$petcompow {powers['bos']} def fol"

            file.SetBind(MMP['selbgm'], bgset + BindFile.BLF(profile, 'mmbinds','\mmbinds\\bguarda.txt'))

    def mmQuietBGActBind(self, profile, filedn, fileup, action, powers):

        MMP =    profile.Pages['MastermindPets'].State
        key = MMP[f"PetBackground{action}"]

        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
        if (MMP['Pet1Bodyguard']) : tier1bg = tier1bg + 1
        if (MMP['Pet2Bodyguard']) : tier1bg = tier1bg + 1
        if (MMP['Pet3Bodyguard']) : tier1bg = tier1bg + 1
        if (MMP['Pet4Bodyguard']) : tier2bg = tier2bg + 1
        if (MMP['Pet5Bodyguard']) : tier2bg = tier2bg + 1
        if (MMP['Pet6Bodyguard']) : tier3bg = tier3bg + 1
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
                if (not MMP['Pet1Bodyguard']): bgact = bgact + f"$$petcomname {MMP['Pet1Name']} {action}" 
                if (not MMP['Pet2Bodyguard']): bgact = bgact + f"$$petcomname {MMP['Pet2Name']} {action}" 
                if (not MMP['Pet3Bodyguard']): bgact = bgact + f"$$petcomname {MMP['Pet3Name']} {action}" 

            if (tier2bg == 0):
                bgact = bgact + f"$$petcompow {powers['lts']} {action}"
            else :
                if (not MMP['Pet4Bodyguard']): bgact = bgact + f"$$petcomname {MMP['Pet4Name']} {action}"
                if (not MMP['Pet5Bodyguard']): bgact = bgact + f"$$petcomname {MMP['Pet5Name']} {action}"

            if (tier3bg == 0): bgact = bgact + f"$$petcompow {powers['bos']} {action}"

        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(key,bgact)

    def mmQuietBGActBGBind(self, profile, filedn, fileup, action, powers):

        MMP =    profile.Pages['MastermindPets'].State
        key    = MMP["PetBackground$action"]
        method = MMP["Pet${action}ResponseMethod"]

        #  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
        #  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
        if (MMP['Pet1Bodyguard']) : tier1bg = tier1bg + 1
        if (MMP['Pet2Bodyguard']) : tier1bg = tier1bg + 1
        if (MMP['Pet3Bodyguard']) : tier1bg = tier1bg + 1
        if (MMP['Pet4Bodyguard']) : tier2bg = tier2bg + 1
        if (MMP['Pet5Bodyguard']) : tier2bg = tier2bg + 1
        if (MMP['Pet6Bodyguard']) : tier3bg = tier3bg + 1
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
                if (MMP['Pet1Bodyguard']): bgact = bgact + f"$$petcomname {MMP['Pet1Name']} {action}" 
                if (MMP['Pet2Bodyguard']): bgact = bgact + f"$$petcomname {MMP['Pet2Name']} {action}" 
                if (MMP['Pet3Bodyguard']): bgact = bgact + f"$$petcomname {MMP['Pet3Name']} {action}" 

            if (tier2bg == 2):
                bgact = bgact + f"$$petcompow  {powers['lts']} {action}"
            else :
                if (MMP['Pet4Bodyguard']) : bgact = bgact + f"$$petcomname {MMP['Pet4Name']} {action}" 
                if (MMP['Pet5Bodyguard']) : bgact = bgact + f"$$petcomname {MMP['Pet5Name']} {action}" 

            if (tier3bg == 1) : bgact = bgact + f"$$petcompow {powers['bos']} {action}"

        # 'petcompow ',,grp.' Stay'
        filedn.SetBind(key,bgact)

    def mmSubBind(self, profile, file, fn, grp, powers):
        MMP =    profile.Pages['MastermindPets'].State
        for cmd  in ('SelectAll', 'SelectMinions', 'SelectLieutenants', 'SelectBoss', 'Bodyguard',
                'Aggressive', 'Defensive', 'Passive', 'Attack', 'Follow', 'Stay', 'Goto'):
            if (self.State[f"Pet{cmd}ResponseMethod"] != 'None') : PetResponses[cmd] = self.State[f"Pet{cmd}Response"]

        file.SetBind(self.State['PetSelectAll'],        self.State['PetSelectAllResponseMethod']         + f" PetResponses['SelectAll']"         + BindFile.BLF(profile, 'mmbinds','call.txt'))
        file.SetBind(self.State['PetSelectMinions'],    self.State['PetSelectMinionsResponseMethod']     + f" PetResponses['SelectMinions']"     + BindFile.BLF(profile, 'mmbinds','ctier1.txt'))
        file.SetBind(self.State['PetSelectLieutenants'],self.State['PetSelectLieutenantsResponseMethod'] + f" PetResponses['SelectLieutenants']" + BindFile.BLF(profile, 'mmbinds','ctier2.txt'))
        file.SetBind(self.State['PetSelectBoss'],       self.State['PetSelectBossResponseMethod']        + f" PetResponses['SelectBoss']"        + BindFile.BLF(profile, 'mmbinds','ctier3.txt'))

        mmBGSelBind(profile,file,PetResponses['Bodyguard'],powers)

        if grp: petcom = f"$$petcompow{grp}"
        else:   petcom =  "petcomall"
        for cmd in ('Aggressive','Defensive','Attack','Follow','Stay','Goto'):
            file.SetBind(self.State[f"Pet[cmd]"],self.State[f"Pet[cmd]ResponseMethod"] + f" {PetResponses[cmd]}{petcom} {cmd}")

        if (self.State['PetBackgroundAttackEnabled'])  : file.SetBind(self.State['PetBackgroundAttack'],'nop')
        if (self.State['PetBackgroundGotoenabled'])    : file.SetBind(self.State['PetBackgroundGoto'],'nop')
        file.SetBind(self.State['chattykey'],'tell $name, Non-Chatty Mode' + BindFile.BLF(profile, 'mmbinds',f"{fn}.txt"))

    def mmBGSubBind(self, profile, filedn, fileup, fn, powers):
        MMP =    profile.Pages['MastermindPets'].State
        PetResponses = {}
        for cmd in ('SelectAll','SelectMinions','SelectLieutenants','SelectBoss','Bodyguard','Aggressive','Defensive','Passive','Attack','Follow','Stay','Goto'):
            if (MMP[f'Pet{cmd}ResponseMethod'] != None) : PetResponses[cmd] = MMP[f'Pet{cmd}Response']

        filedn.SetBind(MMP['PetSelectAll'],        MMP['PetSelectAllResponseMethod']         +  f" {PetResponses['SelectAll']}"         + BindFile.BLF(profile, 'mmbinds','call.txt'))
        filedn.SetBind(MMP['PetSelectMinions'],    MMP['PetSelectMinionsResponseMethod']     +  f" {PetResponses['SelectMinions']}"     + BindFile.BLF(profile, 'mmbinds','ctier1.txt'))
        filedn.SetBind(MMP['PetSelectLieutenants'],MMP['PetSelectLieutenantsResponseMethod'] +  f" {PetResponses['SelectLieutenants']}" + BindFile.BLF(profile, 'mmbinds','ctier2.txt'))
        filedn.SetBind(MMP['PetSelectBoss'],       MMP['PetSelectBossResponseMethod']        +  f" {PetResponses['SelectBoss']}"        + BindFile.BLF(profile, 'mmbinds','ctier3.txt'))
        mmBGSelBind(profile,filedn,PetResponses['Bodyguard'],powers)

        for cmd in ('Aggressive','Defensive','Attack','Follow','Stay','Goto'):
            mmBGActBind(profile, filedn, fileup, cmd, PetResponses[cmd], powers)

        if (MMP['PetBackgroundAttackenabled']):
            mmBGActBGBind( profile, filedn, fileup,'Attack', PetResponses['Attack'], powers)

        if (MMP['PetBackgroundGotoenabled']):
            mmBGActBGBind( profile, filedn, fileup,'Goto', PetResponses['Goto'], powers)

        filedn.SetBind(MMP['chattykey'],'tell $name, Non-Chatty Mode' + BindFile.BLF(profile, 'mmbinds',f"{fn}a.txt"))

    def mmQuietSubBind(self, profile, file, fn, grp, powers):
        MMP = profile.Pages['MastermindPets'].State
        file.SetBind(MMP['PetSelectAll'],        BindFile.BLFs(profile, 'mmbinds','all.txt'))
        file.SetBind(MMP['PetSelectMinions'],    BindFile.BLFs(profile, 'mmbinds','tier1.txt'))
        file.SetBind(MMP['PetSelectLieutenants'],BindFile.BLFs(profile, 'mmbinds','tier2.txt'))
        file.SetBind(MMP['PetSelectBoss'],       BindFile.BLFs(profile, 'mmbinds','tier3.txt'))
        mmQuietBGSelBind(profile, file, powers)

        if grp: petcom = f"$$petcompow{grp}"
        else:   petcom =  '$$petcomall'
        for cmd in ('Aggressive','Defensive','Attack','Follow','Stay','Goto'):
            file.SetBind(MMP[f"Pet{cmd}"],f"{petcom} {cmd}")

        if (MMP['PetBackgroundAttackenabled'])  : file.SetBind(MMP['PetBackgroundAttack'] ,'nop')
        if (MMP['PetBackgroundGotoenabled'])    : file.SetBind(MMP['PetBackgroundGoto']   ,'nop')

        file.SetBind(MMP['chattykey'],'tell $name, Chatty Mode' + BindFile.BLF(profile, 'mmbinds','c' + fn + '.txt'))

    def mmQuietBGSubBind(profile, filedn, fileup, fn, powers):
        MMP = profile.Pages['MastermindPets'].State
        filedn.SetBind(MMP['PetSelectAll'],        BindFile.BLFs(profile, 'mmbinds','all.txt'))
        filedn.SetBind(MMP['PetSelectMinions'],    BindFile.BLFs(profile, 'mmbinds','tier1.txt'))
        filedn.SetBind(MMP['PetSelectLieutenants'],BindFile.BLFs(profile, 'mmbinds','tier2.txt'))
        filedn.SetBind(MMP['PetSelectBoss'],       BindFile.BLFs(profile, 'mmbinds','tier3.txt'))

        mmQuietBGSelBind(profile,filedn,powers)
        for cmd in ('Aggressive','Defensive','Passive','Attack','Follow','Stay','Goto'):
            mmQuietBGActBind(profile, filedn, fileup, cmd, powers)

        if (MMP['PetBackgroundAttackenabled']):
            mmQuietBGActBGBind(profile, filedn, fileup,'Attack', powers)

        if (MMP['PetBackgroundGotoenabled']):
            mmQuietBGActBGBind(profile, filedn, fileup,'Goto', powers)

        filedn.SetBind(MMP['chattykey'],'tell $name, Chatty Mode' + BindFile.BLF(profile, 'mmbinds','c' + fn + 'a.txt'))

    def PopulateBindFiles(self):
        profile = self.Profile
        ResetFile = profile.ResetFile
        MMP       = profile.Pages['MastermindPets'].State

        if (MMP['petselenable']):
            if (MMP['Pet1Nameenabled']) : ResetFile.SetBind(MMP['sel0'],f"petselectname {MMP['Pet1Name']}") 
            if (MMP['Pet2Nameenabled']) : ResetFile.SetBind(MMP['sel1'],f"petselectname {MMP['Pet2Name']}") 
            if (MMP['Pet3Nameenabled']) : ResetFile.SetBind(MMP['sel2'],f"petselectname {MMP['Pet3Name']}") 
            if (MMP['Pet4Nameenabled']) : ResetFile.SetBind(MMP['sel3'],f"petselectname {MMP['Pet4Name']}") 
            if (MMP['Pet5Nameenabled']) : ResetFile.SetBind(MMP['sel4'],f"petselectname {MMP['Pet5Name']}") 
            if (MMP['Pet6Nameenabled']) : ResetFile.SetBind(MMP['sel5'],f"petselectname {MMP['Pet6Name']}") 

        allfile = profile.GetBindFile('mmbinds','all.txt')
        minfile = profile.GetBindFile('mmbinds','tier1.txt')
        ltsfile = profile.GetBindFile('mmbinds','tier2.txt')
        bosfile = profile.GetBindFile('mmbinds','tier3.txt')

        if (MMP['bg_enable']):
            bgfiledn = profile.GetBindFile('mmbinds','bguarda.txt')
            #  since we never need to split lines up in this fashion
            #  comment the next line out so an empty file is not created.
            # bgfileup = $profile.GetBindFile($profile['base'] + "\\mmbinds\\bguardb.txt")

        callfile = profile.GetBindFile('mmbinds','call.txt')
        cminfile = profile.GetBindFile('mmbinds','ctier1.txt')
        cltsfile = profile.GetBindFile('mmbinds','ctier2.txt')
        cbosfile = profile.GetBindFile('mmbinds','ctier3.txt')

        if (MMP['bg_enable']):
            cbgfiledn = profile.GetBindFile('mmbinds','cbguarda.txt')
            cbgfileup = profile.GetBindFile('mmbinds','cbguardb.txt')

        # TODO!!!  get this into / from GameData
        MMPowers = {
            "Mercenaries" : { 'min' : "sol",  'lts' : "spec", 'bos' : "com", },
            "Ninjas"      : { 'min' : "gen",  'lts' : "joun", 'bos' : "oni", },
            "Robotics"    : { 'min' : "dron", 'lts' : "prot", 'bos' : "ass", },
            "Necromancy"  : { 'min' : "zom",  'lts' : "grav", 'bos' : "lich", },
            "Thugs"       : { 'min' : "thu",  'lts' : "enf",  'bos' : "bru", },
        }
        powers = MMPowers[ profile.Pages['General']['Primary'] ]

        # "Local","Self-Tell","Petsay","None"
        mmSubBind(profile, ResetFile,"all",None, powers)
        mmQuietSubBind(profile, allfile,"all",None, powers)
        mmQuietSubBind(profile,minfile,"tier1",powers['min'],powers)
        mmQuietSubBind(profile,ltsfile,"tier2",powers['lts'],powers)
        mmQuietSubBind(profile,bosfile,"tier3",powers['bos'],powers)
        if (MMP['bg_enable']):
            mmQuietBGSubBind(profile,bgfiledn,bgfileup,"bguard",powers)

        mmSubBind(profile,callfile,"all",None,powers)
        mmSubBind(profile,cminfile,"tier1",powers['min'],powers)
        mmSubBind(profile,cltsfile,"tier2",powers['lts'],powers)
        mmSubBind(profile,cbosfile,"tier3",powers['bos'],powers)

        if (MMP['bg_enable']): mmBGSubBind(profile,cbgfiledn,cbgfileup,"bguard",powers)

    def findconflicts(self):
        profile = self.Profile

        MMP = profile.Pages['MastermindPets'].State
        if (MMP['petselenable']) :
            for i in range(1,7):
                if (MMP[f'pet{i}nameenabled']): cbCheckConflict(MMP, f"sel{i-1}Select Pet {i}")

        cbCheckConflict(MMP["PetSelectAll"],"Select All Pets")
        cbCheckConflict(MMP["PetSelectMinions"],"Select Minions")
        cbCheckConflict(MMP["PetSelectLieutenants"],"Select Lieutenants")
        cbCheckConflict(MMP["PetSelectBoss"],"Select Boss Pet")
        cbCheckConflict(MMP["PetAggressive"],"Set Pets Aggressive")
        cbCheckConflict(MMP["PetDefensive"],"Set Pets Defensive")
        cbCheckConflict(MMP["PetPassive"],"Set Pets Passive")
        cbCheckConflict(MMP["PetAttack"],"Pet Order: Attack")
        cbCheckConflict(MMP["PetFollow"],"Pet Order: Follow")
        cbCheckConflict(MMP["PetStay"],"Pet Order: Stay")
        cbCheckConflict(MMP["PetGoto"],"Pet Order: Goto")
        cbCheckConflict(MMP["chattykey"],"Pet Action Bind Chatty Mode Toggle")
        if (MMP['bg_enable']):
            cbCheckConflict(MMP["selbgm"],"Bodyguard Mode")
            if (MMP['PetBackgroundAttackenabled']) : cbCheckConflict(MMP["PetBackgroundAttack"],"Pet Order: BG Attack")
            if (MMP['PetBackgroundGotoenabled'])   : cbCheckConflict(MMP["PetBackgroundGoto"]  ,"Pet Order: BG Goto")

    def bindisused(self): return profile.Pages['MastermindPets']['enabled']


