import wx
import re

# Sandolphan / Khaiba's guide to these controls found at:
# https://guidescroll.com/2011/07/city-of-heroes-mastermind-numeric-keypad-pet-controls/
#
# Originally: https://web.archive.org/web/20120904222729/http://boards.cityofheroes.com/showthread.php?t=117256

import GameData
from Page import Page
from Page.MM.qwyBinds import qwyBinds
from Page.MM.SandolphanBinds import SandolphanBinds
from Help import HelpButton
import UI
from UI.KeySelectDialog import bcKeyButton
from UI.ControlGroup import ControlGroup, cgTextCtrl

class Mastermind(Page):
    UI.Labels.update({
        'Pet1Select'                         : "Select First Minion Pet",
        'Pet2Select'                         : "Select Second Minion Pet",
        'Pet3Select'                         : "Select Third Minion Pet",
        'Pet4Select'                         : "Select First Lieutenant Pet",
        'Pet5Select'                         : "Select Second Lieutenant Pet",
        'Pet6Select'                         : "Select Boss Pet",

        'SelNextPet'                         : "Select Next Pet",
        'SelPrevPet'                         : "Select Previous Pet",
        'IncPetSize'                         : "Increase Pet Group Size",
        'DecPetSize'                         : "Decrease Pet Group Size",
    })

    def __init__(self, parent):
        super().__init__(parent)

        self.PetBoxes = []

        self.Init = {
            'Enable' : False,

            'RenamePets' : '',

            'Pet1Select' : '',
            'Pet2Select' : '',
            'Pet3Select' : '',
            'Pet4Select' : '',
            'Pet5Select' : '',
            'Pet6Select' : '',

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

            'SelNextPet'  : '',
            'SelPrevPet'  : '',
            'IncPetSize'  : '',
            'DecPetSize'  : '',
        }
        # TODO is this Gamedata?
        self.TabTitle = "Mastermind / Pet Binds"

    def BuildPage(self):

        # get the pet names and binds to select them directly
        PetNames  = wx.StaticBoxSizer(wx.HORIZONTAL, self, label = "Pet Names and By-Name Keybinds")
        PetNameSB = PetNames.GetStaticBox()
        PetInner = wx.BoxSizer(wx.HORIZONTAL)

        for i in range(6):
            petdesc      = ['Minion 1', 'Minion 2', 'Minion 3', 'Lieutenant 1', 'Lieutenant 2', 'Boss'][i]
            petdescshort = ['Minion 1', 'Minion 2', 'Minion 3', 'Lt 1'        , 'Lt 2'        , 'Boss'][i]

            PBSB = wx.StaticBox(PetNameSB, style = wx.ALIGN_CENTER|wx.NO_BORDER, label = petdesc)
            box = wx.StaticBoxSizer(PBSB, wx.VERTICAL)

            petname = cgTextCtrl(PBSB, style = wx.TE_CENTRE)
            setattr(petname, "CtlLabel", None)
            self.Ctrls[f'Pet{i+1}Name'] = petname
            petname.SetHint(f"{petdescshort} name")
            petname.Bind(wx.EVT_TEXT, self.OnNameTextChange)

            ctlname = f"Pet{i+1}Select"
            button = bcKeyButton(PBSB, -1, init = {
                'CtlName'  : ctlname,
                'ToolTip'  : f'Choose the key that will select {petdesc}',
                'Key'      : self.Init[ctlname],
            })
            self.Ctrls[ctlname] = button

            box.Add(petname, 0, wx.EXPAND|wx.ALL, 3)
            box.Add(button,  0, wx.EXPAND|wx.ALL, 3)

            PetInner.Add(box, 1, wx.EXPAND|wx.ALL, 3)
            self.PetBoxes.append(box)

        PetExtraCtrls = wx.BoxSizer(wx.VERTICAL)
        PetExtraTop = wx.BoxSizer(wx.HORIZONTAL)
        PetExtraBottom = wx.BoxSizer(wx.HORIZONTAL)

        maxValue = 24 if self.Profile.Server == 'Homecoming' else 26
        LevelLabel = wx.StaticText(PetNameSB, -1, 'Mastermind Level:')
        self.LevelSlider = wx.Slider(PetNameSB, minValue = 1, maxValue = maxValue, value = maxValue,
                                     style = wx.SL_VALUE_LABEL|wx.SL_AUTOTICKS)
        self.LevelSlider.Bind(wx.EVT_SLIDER, self.OnLevelChanged)
        LevelLabel      .SetToolTip('Select the level of your Mastermind - set to max for higher levels')
        self.LevelSlider.SetToolTip('Select the level of your Mastermind - set to max for higher levels')
        self.Ctrls['MMLevel'] = self.LevelSlider

        RenameLabel = wx.StaticText(PetNameSB, -1, 'Rename Pets:')
        RenameLabel          .SetToolTip('Choose the key that will rename your pets, in-game, to match the names set in BindControl')
        self.RenamePetsButton = bcKeyButton(PetNameSB, -1, init = {
                'CtlName'  : 'RenamePets',
                'Key'      : self.Init['RenamePets'],
                'ToolTip'  :'Choose the key that will rename your pets, in-game, to match the names set in BindControl',
            })
        self.RenamePetsButton.SetToolTip('Choose the key that will rename your pets, in-game, to match the names set in BindControl')
        self.Ctrls['RenamePets'] = self.RenamePetsButton

        PetExtraTop.Add(RenameLabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 6)
        PetExtraTop.Add(self.RenamePetsButton, 1, wx.ALIGN_CENTER_VERTICAL)
        PetExtraTop.Add(HelpButton(PetNameSB, 'PetNames.html'), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 6)

        PetExtraBottom.Add(LevelLabel      , 0, wx.ALIGN_CENTER_VERTICAL)
        PetExtraBottom.Add(self.LevelSlider, 1, wx.ALIGN_CENTER_VERTICAL)
        PetExtraBottom.Add(HelpButton(PetNameSB, 'MMLevelSlider.html'), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 6)

        PetExtraCtrls.Add(PetExtraTop,    0, wx.EXPAND)
        PetExtraCtrls.Add(PetExtraBottom, 0, wx.EXPAND)

        PetNames.Add(PetInner,      1, wx.EXPAND|wx.ALL, 10)
        PetNames.Add(PetExtraCtrls, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 15)


        # Sub-tabs for selection of MM Bind style
        self.BindStyleNotebook = wx.Notebook(self, wx.ID_ANY, style = wx.BORDER_NONE)
        self.BindStyleNotebook.SetPadding(wx.Size(50,0))
        self.Ctrls['BindStyle'] = self.BindStyleNotebook

        BasicSelectPage     = self.BasicSelectPage(self.BindStyleNotebook)
        self.SandolphanPage = SandolphanBinds(self, self.BindStyleNotebook)
        self.qwyNumpadPage  = qwyBinds(self.BindStyleNotebook)
        #qwyMousePage        = qwyMouseBinds(self.BindStyleNotebook) # TODO

        self.BindStyleNotebook.AddPage(BasicSelectPage, "Simple Selection Binds")
        self.BindStyleNotebook.AddPage(self.SandolphanPage, "Sandolphan Binds")
        self.BindStyleNotebook.AddPage(self.qwyNumpadPage, "qwy Numpad Binds")
        #self.BindStyleNotebook.AddPage(qwyMousePage, "qwy Mouse Controls Binds")

        bindstyleLabel = wx.BoxSizer(wx.HORIZONTAL)
        bindstyleLabel.Add(wx.StaticText(self, label = "Select Mastermind binds type:"), 0, wx.ALIGN_CENTER|wx.RIGHT, 10)
        bindstyleLabel.Add(HelpButton(self, 'MMBindStyle.html'), 0, wx.ALIGN_CENTER)

        self.MainSizer.Add(PetNames, 0, wx.EXPAND|wx.BOTTOM, 16)
        self.MainSizer.Add(bindstyleLabel, 0, wx.EXPAND|wx.ALL, 10)
        self.MainSizer.Add(self.BindStyleNotebook, 1, wx.EXPAND)

        self.SynchronizeUI()

    def BasicSelectPage(self, parent):
        BasicPage = wx.ScrolledWindow(parent, wx.ID_ANY)
        BasicSizer = wx.BoxSizer(wx.VERTICAL)
        BasicPage.SetSizer(BasicSizer)

        PetSelBox = ControlGroup(BasicPage, self, label="", width=8, flexcols=[1,3,5,7])
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

        BasicSizer.Add(PetSelBox, 0, wx.EXPAND|wx.ALL, 0)

        return BasicPage

    def BindStyle(self):
        return ['Basic', 'Sandolphan', 'qwy Numpad', 'qwy Mouse'][self.BindStyleNotebook.GetSelection()]

    def SynchronizeUI(self):
        ismm = self.Profile.Archetype() == "Mastermind"
        pset = self.Profile.Primary()

        for control in self.Ctrls.values(): control.Enable(bool(ismm and pset))
        self.RenamePetsButton.Enable(bool(ismm and pset))
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

    def OnNameTextChange(self, evt = None):
        self.CheckUndefNames()
        self.CheckUniqueNames()
        if evt: evt.Skip()

    def CheckUndefNames(self):
        for i in (1,2,3,4,5,6):
            ctrl = self.Ctrls[f'Pet{i}Name']
            if not ctrl.IsEnabled() or ctrl.GetValue():
                ctrl.RemoveError('undef')
            else:
                ctrl.AddError('undef', 'By-Name selection and Bodyguard Mode require the pet name be filled in.')

    def CheckUniqueNames(self):
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
            if not ctrl.IsEnabled() or not ctrl.GetValue() or self.uniqueNames[i-1]:
                ctrl.RemoveError('unique')
            else:
                ctrl.AddError('unique', 'This pet name is not different enough to identify it uniquely.  This is likely to cause issues with many of BindControl\'s Mastermind binds.')

    def PopulateBindFiles(self):

        profile = self.Profile
        ResetFile = profile.ResetFile()

        if not profile.Archetype() == 'Mastermind': return True

        # First, deduce which "pet name boxes" need checking, and in what order.
        OrderedPetBoxes = []
        petPowers = GameData.MMPowerSets[profile.Primary()]['abbrs']
        # now order them by powername, alphabetically, to match the in-game pet list
        for grp in sorted(petPowers):
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
                    if self.Ctrls[f'Pet{i+1}Select'].GetLabel():
                        needUniqueNames = True
                        break
        if self.Ctrls['PetBodyguard'].GetLabel():
            needUniqueNames = True

        if needUniqueNames:
            for i in range(6):
                for [_, box] in OrderedPetBoxes:
                    if self.PetBoxes[i] == box:
                        ctrl = self.Ctrls[f'Pet{i+1}Name']
                        if ctrl.IsEnabled() and ctrl.HasErrors():
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
                ResetFile.SetBind(self.RenamePetsButton.MakeBind(rpCommands))

        ### By-name select binds.
        # TODO - would this make more sense fully integrated into mm(Quiet)SubBind?
        for pet in range(6):
            feedback = ''
            selfile = ''
            if self.BindStyle() == 'Sandolphan':
                selfile = 'sel.txt'
                if self.GetState('PetChattyDefault'):
                    feedback = self.SandolphanPage.GetChatString('SelectAll', pet+1)
                    selfile = 'csel.txt'
                selfile = profile.BLF('mmb', selfile)
            ResetFile.SetBind(
                self.Ctrls[f"Pet{pet+1}Select"].MakeFileKeyBind(
                    [feedback, f"petselectname {self.uniqueNames[pet]}", selfile]
                )
            )

        bindstyle = self.BindStyle()
        if bindstyle == 'Basic':
            ### Prev / next pet binds
            if (
                self.GetState('IncPetSize') and self.GetState('DecPetSize') and
                self.GetState('SelNextPet') and self.GetState('SelPrevPet')
            ):
                self.psCreateSet(6,0,ResetFile)
                for tsize in 1,2,3,4,5,6:
                    for tsel in range(0,tsize+1):
                        file = self.Profile.GetBindFile('petsel', f"{tsize}{tsel}.txt")
                        self.psCreateSet(tsize,tsel,file)
        elif bindstyle == 'Sandolphan':
            self.SandolphanPage.PopulateBindFiles()
        elif bindstyle == 'qwy Numpad':
            self.qwyNumpadPage.PopulateBindFiles()
        #elif bindstyle == 'qwy Mouse':
        #    self.qwyMousePage.PopulateBindFiles()

        return True

    def psCreateSet(self, tsize, tsel, file):
        # tsize is the size of the team at the moment
        # tsel is the currently selected team member as far as the bind knows, or 0 if unknown

        c = self.Ctrls
        p = self.Profile

        if tsize < 6:
            file.SetBind(c['IncPetSize'].MakeBind([
                f'tell $name, [{tsize+1} Pet]', p.BLF('petsel', f'{tsize+1}.txt')
            ]))
        else:
            file.SetBind(c['IncPetSize'].MakeBind('nop'))
        if tsize == 1:
            file.SetBind(c['DecPetSize'].MakeBind('nop'))
            file.SetBind(c['SelNextPet'].MakeBind([
                f'petselect 0', p.BLF('petsel', f'{tsize}1.txt'), p.BLF('mmb', 'csel.txt'),
            ]))
            file.SetBind(c['SelPrevPet'].MakeBind([
                f'petselect 0', p.BLF('petsel', f'{tsize}1.txt'), p.BLF('mmb', 'csel.txt'),
            ]))
        else:
            selnext,selprev = tsel+1,tsel-1
            if selnext > tsize : selnext = 1
            if selprev < 1 : selprev = tsize
            newsel = tsel
            if tsize-1 < tsel : newsel = tsize-1
            if tsize == 2 : newsel = 0
            file.SetBind(c['DecPetSize'].MakeBind([
                f'tell $name, [{tsize-1} Pet]', p.BLF('petsel', f'{tsize-1}{newsel}.txt')
            ]))
            file.SetBind(c['SelNextPet'].MakeBind([
                f'petselect {selnext-1}', p.BLF('petsel', f'{tsize}{selnext}.txt'), p.BLF('mmb', 'csel.txt'),
            ]))
            file.SetBind(c['SelPrevPet'].MakeBind([
                f'petselect {selprev-1}', p.BLF('petsel', f'{tsize}{selprev}.txt'), p.BLF('mmb', 'csel.txt'),
            ]))

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

        for fn in ['pad', 'min1', 'min2', 'min3', 'lt1', 'lt2', 'bos', 'mins', 'lts', '1up', '2up']:
            files.append(self.Profile.GetBindFile('mmqn', f'{fn}.txt'))

        return {
            'files' : files,
            # putting the old "mmbinds" dir in here for now to clean up old bindsdirs
            'dirs'  : ['mmbinds', 'mmb', 'petsel', 'mmqn'],
        }

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
