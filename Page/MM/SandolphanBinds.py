import wx
import re
import UI
from Help import HelpButton

# Sandolphan / Khaiba's guide to these controls found at:
# https://guidescroll.com/2011/07/city-of-heroes-mastermind-numeric-keypad-pet-controls/
#
# Originally: https://web.archive.org/web/20120904222729/http://boards.cityofheroes.com/showthread.php?t=117256

from UI.ControlGroup import ControlGroup

class SandolphanBinds(wx.Panel):
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
    def __init__(self, page, bindsnotebook):
        super().__init__(bindsnotebook)
        self.Page = page
        self.uniqueNames = []

        page.Init.update({

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
        })

        SandolphanSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(SandolphanSizer)

        # Iterate the data structure at the top and make the grid of controls for the basic pet binds
        petCommandsKeys = ControlGroup(self, page, width = 5, label = "", flexcols = [4])
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

        staticbox = petCommandsKeys.GetStaticBox()
        BGCBSizer = wx.BoxSizer(wx.HORIZONTAL)
        petlabels = ['Minion 1', 'Minion 2', 'Minion 3', 'lieutenant 1', 'lieutenant 2', 'Boss']
        cblabels  = ['Minion 1 BG', 'Minion 2 BG', 'Minion 3 BG', 'Lt 1 BG', 'Lt 2 BG', 'Boss BG']
        for cb in range(6):
            checkbox = wx.CheckBox(staticbox, label = cblabels[cb])
            page.Ctrls[f"Pet{cb+1}Bodyguard"] = checkbox
            checkbox.SetToolTip(f"Select whether {petlabels[cb]} acts as Bodyguard when Bodyguard Mode is activated")

            BGCBSizer.Add(checkbox, flag = wx.ALIGN_CENTER_VERTICAL)

        petCommandsKeys.InnerSizer.Add(BGCBSizer, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)

        SandolphanSizer.Add(petCommandsKeys, 0, wx.EXPAND|wx.ALL, 0)

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
                if (self.Page.GetState('Pet1Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[0]} "
                    bgsay.append(method + PetBodyguardResponse)
                if (self.Page.GetState('Pet2Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[1]} "
                    bgsay.append(method + PetBodyguardResponse)
                if (self.Page.GetState('Pet3Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[2]} "
                    bgsay.append(method + PetBodyguardResponse)

            if (tier2bg == 2):
                if re.match('petsay', method): method = f"petsaypow {powers['lts']} "
                bgsay.append(method + PetBodyguardResponse)
            else:
                if (self.Page.GetState('Pet4Bodyguard')) :
                    if re.match('petsay', method):
                        method = f"petsayname {self.uniqueNames[3]} "
                    bgsay.append(method + PetBodyguardResponse)
                if (self.Page.GetState('Pet5Bodyguard')) :
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
                if (self.Page.GetState('Pet1Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[0]} def fol")
                if (self.Page.GetState('Pet2Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[1]} def fol")
                if (self.Page.GetState('Pet3Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[2]} def fol")

            if (tier2bg == 2):
                bgset.append(f"petcompow {powers['lts']} def fol")
            else:
                if (self.Page.GetState('Pet4Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[3]} def fol")
                if (self.Page.GetState('Pet5Bodyguard')):
                    bgset.append(f"petcomname {self.uniqueNames[4]} def fol")

            if (tier3bg == 1):
                bgset.append(f"petcompow {powers['bos']} def fol")

        file.SetBind(self.Page.Ctrls['PetBodyguard'].MakeFileKeyBind(bgsay + bgset))

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
                if (self.Page.GetState('Pet1Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[0]} def fol")
                if (self.Page.GetState('Pet2Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[1]} def fol")
                if (self.Page.GetState('Pet3Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[2]} def fol")

            if (tier2bg == 2):
                bgset.append(f"petcompow {powers['lts']} def fol")
            else :
                if (self.Page.GetState('Pet4Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[3]} def fol")
                if (self.Page.GetState('Pet5Bodyguard')) : bgset.append(f"petcomname {self.uniqueNames[4]} def fol")

            if (tier3bg == 1):
                bgset.append(f"petcompow {powers['bos']} def fol")

        file.SetBind(self.Page.Ctrls['PetBodyguard'].MakeFileKeyBind(bgset))

    # set up "all" and "tierx" files with command binds, chatty version
    def mmSubBind(self, file, fn, grp, powers):
        profile = self.Page.Profile

        file.SetBind(self.Page.Ctrls['PetSelectAll'].MakeFileKeyBind([
            self.GetChatString('SelectAll'), profile.BLF('mmb','call.txt')]))
        file.SetBind(self.Page.Ctrls['PetSelectMinions'].MakeFileKeyBind([
            self.GetChatString('SelectMinions', powers['min']), profile.BLF('mmb','ctier1.txt')]))
        file.SetBind(self.Page.Ctrls['PetSelectLieutenants'].MakeFileKeyBind([
            self.GetChatString('SelectLieutenants', powers['lts']), profile.BLF('mmb','ctier2.txt')]))
        file.SetBind(self.Page.Ctrls['PetSelectBoss'].MakeFileKeyBind([
            self.GetChatString('SelectBoss', powers['bos']), profile.BLF('mmb','ctier3.txt')]))

        bgfresponse = self.Page.GetState('PetBodyguardResponse') if self.GetChatString(f"Bodyguard") else ''
        self.mmBGSelBind(file,bgfresponse,powers)

        if   grp == 'sel'       : petcom =  'petcom'
        elif grp                : petcom = f'petcompow {grp}'
        else                    : petcom =  'petcomall'
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Page.Ctrls[f"Pet{cmd}"].MakeFileKeyBind([self.GetChatString(cmd, grp or 'all'), f"{petcom} {cmd}"]))

        file.SetBind(self.Page.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Non-Chatty Mode', profile.BLF('mmb',f"{fn}.txt")]))

    # set up "all" and "tierx" files with command binds, quiet version
    def mmQuietSubBind(self, file, fn, grp, powers):
        profile = self.Page.Profile
        file.SetBind(self.Page.Ctrls['PetSelectAll']        .MakeFileKeyBind(profile.BLF('mmb','all.txt')))
        file.SetBind(self.Page.Ctrls['PetSelectMinions']    .MakeFileKeyBind(profile.BLF('mmb','tier1.txt')))
        file.SetBind(self.Page.Ctrls['PetSelectLieutenants'].MakeFileKeyBind(profile.BLF('mmb','tier2.txt')))
        file.SetBind(self.Page.Ctrls['PetSelectBoss']       .MakeFileKeyBind(profile.BLF('mmb','tier3.txt')))
        self.mmQuietBGSelBind(file, powers)

        if   grp == 'sel'       : petcom =  'petcom'
        elif grp                : petcom = f"petcompow {grp}"
        else                    : petcom =  'petcomall'
        for cmd in ('Aggressive','Defensive','Passive', 'Attack','Follow','Goto', 'Stay'):
            file.SetBind(self.Page.Ctrls[f"Pet{cmd}"].MakeFileKeyBind(f"{petcom} {cmd}"))

        file.SetBind(self.Page.Ctrls['PetChatToggle'].MakeFileKeyBind(['tell $name, Chatty Mode', profile.BLF('mmb','c' + fn + '.txt')]))

    def PopulateBindFiles(self):

        profile = self.Page.Profile
        ResetFile = profile.ResetFile()

        powers = self.Page.MMPowerSets[ profile.General.GetState('Primary') ]['powers']

        if self.Page.GetState('PetChattyDefault'):
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

        return True

    def psCreateSet(self, tsize, tsel, file):
        # tsize is the size of the team at the moment
        # tsel is the currently selected team member as far as the bind knows, or 0 if unknown

        c = self.Page.Ctrls
        p = self.Page.Profile

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
        chatdesc = self.Page.GetState(control)
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
            response = method + self.Page.GetState(f"Pet{cmd}Response")
        return response

    def CountBodyguards(self):
        tier1bg = 0
        tier2bg = 0
        tier3bg = 0
        if (self.Page.GetState('Pet1Bodyguard')) : tier1bg = tier1bg + 1
        if (self.Page.GetState('Pet2Bodyguard')) : tier1bg = tier1bg + 1
        if (self.Page.GetState('Pet3Bodyguard')) : tier1bg = tier1bg + 1
        if (self.Page.GetState('Pet4Bodyguard')) : tier2bg = tier2bg + 1
        if (self.Page.GetState('Pet5Bodyguard')) : tier2bg = tier2bg + 1
        if (self.Page.GetState('Pet6Bodyguard')) : tier3bg = tier3bg + 1
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
            files.append(self.Page.Profile.GetBindFile('mmbinds', f'{fn}.txt'))
            files.append(self.Page.Profile.GetBindFile('mmb',     f'{fn}.txt'))

            for tsize in 1,2,3,4,5,6:
                for tsel in range(0,tsize+1):
                    files.append(self.Page.Profile.GetBindFile('petsel', f"{tsize}{tsel}.txt"))

        return {
            'files' : files,
            # putting the old "mmbinds" dir in here for now to clean up old bindsdirs
            'dirs'  : ['mmbinds', 'mmb', 'petsel'],
        }


    for cmd in petCommandKeyDefinitions:
        UI.Labels[cmd['ctrlName']] = cmd['label']
    UI.Labels.update({
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
    })
