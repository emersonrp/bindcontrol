import wx
import UI
import Utility

from UI.ControlGroup import ControlGroup
from Page import Page


class TeamPetSelect(Page):
    ordinals = ("First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth")

    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Team / Pet Select"
        self.Init = {
            'TPSEnable'   : True,
            'TPSSelMode'  : '',
            'TeamSelect1' : 'UNBOUND',
            'TeamSelect2' : 'UNBOUND',
            'TeamSelect3' : 'UNBOUND',
            'TeamSelect4' : 'UNBOUND',
            'TeamSelect5' : 'UNBOUND',
            'TeamSelect6' : 'UNBOUND',
            'TeamSelect7' : 'UNBOUND',
            'TeamSelect8' : 'UNBOUND',
            'EnablePet' : True,
            'SelNextPet' : 'UNBOUND',
            'SelPrevPet' : 'UNBOUND',
            'IncPetSize' : 'UNBOUND',
            'DecPetSize' : 'UNBOUND',
            'EnableTeam' : True,
            'SelNextTeam' : 'A',
            'SelPrevTeam' : 'G',
            'IncTeamSize' : 'P',
            'DecTeamSize' : 'H',
            'IncTeamPos'  : '4',
            'DecTeamPos'  : '8',
            'Reset'       : '',
        }

    def BuildPage(self):

        if not self.GetState('Mode'): self.SetState('Mode', 1)

        for i in (1,2,3,4,5,6,7,8):
            if not self.GetState(f"sel{i}"):
                self.SetState(f"sel{i}", "UNBOUND")

        topSizer = wx.BoxSizer(wx.VERTICAL)

        ##### header
        headerSizer = wx.FlexGridSizer(0,2,10,10)

        enablecb = wx.CheckBox( self, -1, 'Enable Team/Pet Select')
        enablecb.SetToolTip( wx.ToolTip('Check this to enable the Team/Pet Select Binds') )

        helpbutton = wx.BitmapButton(self, -1, Utility.Icon('Help'))
        helpbutton.Bind(wx.EVT_BUTTON, self.help)

        headerSizer.Add(enablecb, 0, wx.ALIGN_CENTER_VERTICAL)
        headerSizer.Add(helpbutton, wx.ALIGN_RIGHT, 0)

        topSizer.Add(headerSizer)

        ##### direct-select keys
        TPSDirectBox = ControlGroup(self, self, 'Direct Team/Pet Select')

        TPSDirectBox.AddLabeledControl(
            ctlName = 'TPSSelMode',
            ctlType = 'combo',
            contents = ['Teammates, then pets','Pets, then teammates','Teammates Only','Pets Only'],
            tooltip = 'Choose the order in which teammates and pets are selected with sequential keypresses',
        )
        for selectid in (1,2,3,4,5,6,7,8):
            TPSDirectBox.AddLabeledControl(
                ctlName = f"TeamSelect{selectid}",
                ctlType = 'keybutton',
                tooltip = f"Choose the key that will select team member / pet {selectid}",
            )
        topSizer.Add(TPSDirectBox)

        ##### Pet Select Binds
        PetSelBox = ControlGroup(self, self, 'Pet Select')

        PetSelBox.AddLabeledControl(
            ctlName = 'SelNextPet',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will select the next pet from the currently selected one',
        )
        PetSelBox.AddLabeledControl(
            ctlName = 'SelPrevPet',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will select the previous pet from the currently selected one',
        )
        PetSelBox.AddLabeledControl(
            ctlName = 'IncPetSize',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will increase the size of your pet/henchman group rotation',
        )
        PetSelBox.AddLabeledControl(
            ctlName = 'DecPetSize',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will decrease the size of your pet/henchman group rotation',
        )
        topSizer.Add(PetSelBox)

        ##### Team Select Binds
        TeamSelBox = ControlGroup(self, self, 'Team Select')
        TeamSelBox.AddLabeledControl(
            ctlName ='SelNextTeam',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will select the next teammate from the currently selected one',
        )
        TeamSelBox.AddLabeledControl(
            ctlName ='SelPrevTeam',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will select the previous teammate from the currently selected one',
        )
        TeamSelBox.AddLabeledControl(
            ctlName ='IncTeamSize',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will increase the size of your teammate rotation',
        )
        TeamSelBox.AddLabeledControl(
            ctlName ='DecTeamSize',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will decrease the size of your teammate rotation',
        )
        TeamSelBox.AddLabeledControl(
            ctlName ='IncTeamPos',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will move you to the next higher slot in the team rotation',
        )
        TeamSelBox.AddLabeledControl(
            ctlName ='DecTeamPos',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will move you to the next lower slot in the team rotation',
        )
        TeamSelBox.AddLabeledControl(
            ctlName ='Reset',
            ctlType = 'keybutton',
            tooltip = 'Choose the key that will reset your team rotation to solo',
        )
        topSizer.Add(TeamSelBox)

        self.TabTitle = 'Team / Pet Selection'

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(topSizer, flag = wx.ALL|wx.EXPAND, border = 16)
        self.SetSizer(paddingSizer)

    def PopulateBindFiles(self):
        profile    = self.Profile
        ResetFile  = profile.ResetFile
        if (self.GetState('TPSSelMode') < 3):
            selmethod = "teamselect"
            selnummod = 0
            selmethod1 = "petselect"
            selnummod1 = 1
            if (self.GetState('TPSSelMode') == 2):
                selmethod = "petselect"
                selnummod = 1
                selmethod1 = "teamselect"
                selnummod1 = 0
            selresetfile = profile.GetBindFile("tps","reset.txt")
            for i in (1,2,3,4,5,6,7,8):
                selfile = profile.GetBindFile("tps",f"sel{i}.txt")
                ResetFile.   SetBind(self.GetState(f"TeamSelect{i}"),"selmethod " + (i - selnummod) + BindFile.BLF(profile,'tps',"sel{i}.txt"))
                selresetfile.SetBind(self.GetState(f"TeamSelect{i}"),"selmethod " + (i - selnummod) + BindFile.BLF(profile,'tps',"sel{i}.txt"))
                for j in (1,2,3,4,5,6,7,8):
                    if (i == j):
                        selfile.SetBind(self.GetState(f"TeamSelect{j}"),"selmethod1 " + (j - selnummod1) + BindFile.BLF(profile,'tps',"reset.txt"))
                    else:
                        selfile.SetBind(self.GetState(f"TeamSelect{j}"),"selmethod " +  (j - selnummod)  + BindFile.BLF(profile,'tps',"selj.txt"))

        else:
            selmethod = "teamselect"
            selnummod = 0
            if (self.GetState('TPSSelMode') == 4):
                selmethod = "petselect"
                selnummod = 1
            for i in (1,2,3,4,5,6,7,8):
                ResetFile.SetBind(self.GetState('sel1'),"selmethod " + (i - selnummod))

        if (self.GetState('PetSelEnable')):
            tpsCreatePetSet(profile,1,0,profile.ResetFile)
            for size in (1,2,3,4,5,6,7,8):
                for sel in range(size):
                    file = profile.GetBindFile("tps",f"pet{size}{sel}.txt")
                    tpsCreatePetSet(profile,size,sel,file)


        if (self.GetState('TeamSelEnable')):
            tpsCreateTeamSet(profile,1,0,0,profile.ResetFile)
            for size in (1,2,3,4,5,6,7,8):
                for pos in range(size):
                    for sel in range(size):
                        if (sel != pos or sel == 0):
                            file = profile.GetBindFile("tps", f"team{size}{pos}{sel}.txt")
                            tpsCreateTeamSet(profile,size,pos,sel,file)


    def tpsCreatePetSet(self, profile, tsize, tsel, file):
        # tsize is the size of the team at the moment
        # tpos is the position of the player at the moment, or 0 if unknown
        # tsel is the currently selected team member as far as the bind knows, or 0 if unknown
        #file.SetBind(TPS.reset,'tell name, Re-Loaded Single Key Team Select Bind.' + BindFile.BLF(profile, 'petsel', '10.txt')
        if (tsize < 8):
            file.SetBind(self.GetState('IncPetSize'),'tell name, ' + formatPetConfig(tsize+1) + BindFile.BLF(profile, 'tps', (tsize+1) + "tsel.txt"))
        else:
            file.SetBind(self.GetState('DecPetSize'),'nop')

        if (tsize == 1):
            file.SetBind(self.GetState('DecPetSize'),'nop')
            file.SetBind(self.GetState('SelNextPet'),'petselect 0' + BindFile.BLF(profile, 'tps', tsize + '1.txt'))
            file.SetBind(self.GetState('SelPrevPet'),'petselect 0' + BindFile.BLF(profile, 'tps', tsize + '1.txt'))
        else:
            (selnext,selprev) = (tsel+1,tsel-1)
            if (selnext > tsize): selnext = 1
            if (selprev < 1):     selprev = tsize
            newsel = tsel
            if (tsize-1 < tsel): newsel = tsize-1
            if (tsize == 2):     newsel = 0
            file.SetBind(self.GetState('DecPetSize'),'tell name, ' + formatPetConfig(tsize-1) + BindFile.BLF(profile, 'tps', (tsize-1) + newsel + '.txt'))
            file.SetBind(self.GetState('SelNextPet'),'petselect ' + (selnext-1) + BindFile.BLF(profile, 'tps', tsize + selnext + '.txt'))
            file.SetBind(self.GetState('SelPrevPet'),'petselect ' + (selprev-1) + BindFile.BLF(profile, 'tps', tsize + selprev + '.txt'))

    def formatPetConfig(self, which):
        return "[" + ordinals[which - 1] + " Pet ]"

    def tpsCreateTeamSet(self, profile, tsize, tpos, tsel, file):
        #  tsize is the size of the team at the moment
        #  tpos is the position of the player at the moment, or 0 if unknown
        #  tsel is the currently selected team member as far as the bind knows, or 0 if unknown
        file.SetBind(self.GetState('Reset'),'tell name, Re-Loaded Single Key Team Select Bind' + BindFile.BLF(profile, 'teamsel2', '100.txt'))
        if (tsize < 8):
            file.SetBind(self.GetState('IncTeamSize'),'tell name, ' + formatTeamConfig(tsize+1,tpos) + BindFile.BLF(profile, 'teamsel2',(tsize+1) + tpos + tsel + '.txt'))
        else:
            file.SetBind(self.GetState('IncTeamSize'),'nop')

        if (tsize == 1):
            file.SetBind(self.GetState('DecTeamSize'),'nop')
            file.SetBind(self.GetState('IncTeamPos'), 'nop')
            file.SetBind(self.GetState('DecTeamPos'), 'nop')
            file.SetBind(self.GetState('SelNextTeam'),'nop')
            file.SetBind(self.GetState('SelPrevTeam'),'nop')
        else:
            (selnext,selprev) = (tsel+1,tsel-1)
            if (selnext > tsize): selnext = 1
            if (selprev < 1)    : selprev = tsize
            if (selnext == tpos): selnext = selnext + 1
            if (selprev == tpos): selprev = selprev - 1
            if (selnext > tsize): selnext = 1
            if (selprev < 1)    : selprev = tsize

            (tposup,tposdn) = (tpos+1,tpos-1)
            if (tposup > tsize): tposup = 0
            if (tposdn < 0)    : tposdn = tsize

            (newpos,newsel) = (tpos,tsel)
            if (tsize-1 < tpos): newpos = tsize-1
            if (tsize-1 < tsel): newsel = tsize-1
            if (tsize == 2)    : newpos = newsel = 0

            file.SetBind(self.GetState('DecTeamSize'),'tell name, ' + formatTeamConfig(tsize-1,newpos) + BindFile.BLF(profile, 'teamsel2', (tsize-1) + newpos + newsel + '.txt'))
            file.SetBind(self.GetState('IncTeamPos'), 'tell name, ' + formatTeamConfig(tsize,  tposup) + BindFile.BLF(profile, 'teamsel2', tsize + tposup + tsel + '.txt'))
            file.SetBind(self.GetState('DecTeamPos'), 'tell name, ' + formatTeamConfig(tsize,  tposdn) + BindFile.BLF(profile, 'teamsel2', tsize + tposdn + tsel + '.txt'))

            file.SetBind(self.GetState('SelNextTeam'),'teamselect ' + selnext + BindFile.BLF(profile, 'teamsel2', tsize + tpos + selnext + '.txt'))
            file.SetBind(self.GetState('SelPrevTeam'),'teamselect ' + selprev + BindFile.BLF(profile, 'teamsel2', tsize + tpos + selprev + '.txt'))

    def formatTeamConfig(self, size, pos):
        sizetext = f"{size}-Man"
        postext = ", No Spot"
        if (pos > 0)  : postext = f", {ordinals[pos-1]} Spot"
        if (size == 1): sizetext = "Solo"; postext = ""
        if (size == 2): sizetext = "Duo"
        if (size == 3): sizetext = "Trio"
        return f"[{sizetext}{postext}]"

    def findconflicts(self, profile):
        TPS = profile.TeamPetSelect
        for i in range(1,9):
            Utility.CheckConflict(TPS,f"TeamSelect{i}",f"Team/Pet {i} Key")

        Utility.CheckConflict(TPS,"SelNextPet","Select next henchman")
        Utility.CheckConflict(TPS,"SelPrevPet","Select previous henchman")
        Utility.CheckConflict(TPS,"IncPetSize","Increase Henchman Group Size")
        Utility.CheckConflict(TPS,"DecPetSize","Decrease Henchman Group Size")

    def bindisused(self, profile):
        return self.GetState('Enabled')

    def HelpText(self):
        return """
    Team/Pet Direct Selection binds contributed by ShieldBearer.

    Single Key Team Selection binds based on binds from Weap0nX.
    """

    UI.Labels.update({
        'TPSSelMode' : "Team/Pet selection mode",
        'TeamSelect1' : "Select First Team Member/Pet",
        'TeamSelect2' : "Select Second Team Member/Pet",
        'TeamSelect3' : "Select Third Team Member/Pet",
        'TeamSelect4' : "Select Fourth Team Member/Pet",
        'TeamSelect5' : "Select Fifth Team Member/Pet",
        'TeamSelect6' : "Select Sixth Team Member/Pet",
        'TeamSelect7' : "Select Seventh Team Member/Pet",
        'TeamSelect8' : "Select Eighth Team Member/Pet",
        'SelNextPet' : 'Select Next Pet',
        'SelPrevPet' : 'Select Previous Pet',
        'IncPetSize' : 'Increase Pet Group Size',
        'DecPetSize' : 'Decrease Pet Group Size',
        'SelNextTeam' : 'Select Next Team Member',
        'SelPrevTeam' : 'Select Previous Team Member',
        'IncTeamSize' : 'Increase Team Size',
        'DecTeamSize' : 'Decrease Team Size',
        'IncTeamPos'  : 'Increase Team Position',
        'DecTeamPos'  : 'Decrease Team Position',
        'Reset'       : 'Reset to Solo',
    })
