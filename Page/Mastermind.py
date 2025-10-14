import wx
import re

import GameData
from Help import HelpButton
from Page import Page
from Page.MM.SandolphanBinds import SandolphanBinds
from Page.MM.qwyNumpad import qwyNumpad
from Page.MM.qwyPetMouse import qwyPetMouse
import UI
from UI.ControlGroup import cgTextCtrl
from UI.KeySelectDialog import bcKeyButton

class Mastermind(Page):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.PetBoxes = []

        self.Init = {
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
        }
        self.TabTitle = "Mastermind / Pet Binds"

    def BuildPage(self) -> None:

        # get the pet names and binds to select them directly
        self.PetNames  = wx.StaticBoxSizer(wx.HORIZONTAL, self, label = "Pet Names and By-Name Selection")
        PetNameSB = self.PetNames.GetStaticBox()
        PetInner = wx.BoxSizer(wx.HORIZONTAL)

        for i in range(6):
            petdesc      = ['Minion 1', 'Minion 2', 'Minion 3', 'Lieutenant 1', 'Lieutenant 2', 'Boss'][i]
            petdescshort = ['Min 1'   , 'Min 2'   , 'Min 3'   , 'Lt 1'        , 'Lt 2'        , 'Boss'][i]

            PBSB = wx.StaticBox(PetNameSB, style = wx.ALIGN_CENTER|wx.NO_BORDER, label = petdesc)
            box = wx.StaticBoxSizer(PBSB, wx.VERTICAL)

            petname = cgTextCtrl(PBSB, style = wx.TE_CENTRE)
            setattr(petname, "CtlLabel", None)
            self.Ctrls[f'Pet{i+1}Name'] = petname
            petname.SetHint(f"{petdescshort} name")
            petname.Bind(wx.EVT_TEXT, self.OnNameTextChange)

            ctlname = f"Pet{i+1}Select"
            button = bcKeyButton(PBSB, init = {
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

        maxValue = 24 if self.Profile.Server() == 'Homecoming' else 26
        LevelLabel = wx.StaticText(PetNameSB, label = 'Mastermind Level:')
        self.LevelSlider = wx.Slider(PetNameSB, minValue = 1, maxValue = maxValue, value = maxValue,
                                     style = wx.SL_VALUE_LABEL|wx.SL_AUTOTICKS)
        self.LevelSlider.Bind(wx.EVT_SLIDER, self.OnLevelChanged)
        LevelLabel      .SetToolTip('Select the level of your Mastermind - set to max for higher levels')
        self.LevelSlider.SetToolTip('Select the level of your Mastermind - set to max for higher levels')
        self.Ctrls['MMLevel'] = self.LevelSlider

        RenameLabel = wx.StaticText(PetNameSB, label = 'Rename Pets:')
        RenameLabel          .SetToolTip('Choose the key that will rename your pets, in-game, to match the names set in BindControl')
        self.RenamePetsButton = bcKeyButton(PetNameSB, init = {
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

        self.PetNames.Add(PetInner,      1, wx.EXPAND|wx.ALL, 10)
        self.PetNames.Add(PetExtraCtrls, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 15)

        # Sub-tabs for selection of MM Bind style
        self.BindStyleNotebook = wx.Notebook(self, style = wx.BORDER_NONE)
        self.BindStyleNotebook.SetPadding(wx.Size(50,0))
        self.Ctrls['BindStyle'] = self.BindStyleNotebook

        self.SandolphanPage  = SandolphanBinds(self, self.BindStyleNotebook)
        self.qwyNumpadPage   = qwyNumpad      (self, self.BindStyleNotebook)
        self.qwyPetMousePage = qwyPetMouse    (self, self.BindStyleNotebook)

        self.BindStyleNotebook.AddPage(self.NoBindStylePage(), "No Binds")
        self.BindStyleNotebook.AddPage(self.SandolphanPage, "Sandolphan Binds")
        self.BindStyleNotebook.AddPage(self.qwyNumpadPage, "qwy Numpad Binds")
        self.BindStyleNotebook.AddPage(self.qwyPetMousePage, "qwy PetMouse Binds")
        self.BindStyleNotebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnBindStyleChanged)

        self.BindstyleLabel = wx.Panel(self)
        bindstyleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindstyleLabel.SetSizer(bindstyleSizer)
        bindstyleSizer.Add(wx.StaticText(self.BindstyleLabel, label = "Select Mastermind binds type:"), 0, wx.ALIGN_CENTER|wx.ALL, 10)
        bindstyleSizer.Add(HelpButton(self.BindstyleLabel, 'MMBindStyle.html'), 0, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 10)

        self.MainSizer.Add(self.PetNames, 0, wx.EXPAND|wx.BOTTOM, 16)
        self.MainSizer.Add(self.BindstyleLabel, 0, wx.EXPAND)
        self.MainSizer.Add(self.BindStyleNotebook, 1, wx.EXPAND)

        self.SynchronizeUI()

    def NoBindStylePage(self):
        page = wx.Panel(self.BindStyleNotebook)

        BlankSizer = wx.BoxSizer(wx.HORIZONTAL)
        helptext = wx.StaticText(page, style = wx.ALIGN_CENTER,
                                 label = "No Mastermind bind style selected.\nBy-name selection binds will still work.")
        helptext.SetFont(wx.Font(wx.FontInfo(16).Bold()))
        BlankSizer.Add(helptext, 1, wx.ALIGN_CENTER_VERTICAL)
        page.SetSizer(BlankSizer)
        page.Layout()

        return page

    def GetKeyBinds(self):
        binds = super().GetKeyBinds()

        bindstyle = self.BindStyle()

        if bindstyle == 'qwy Numpad':
            binds = binds + self.qwyNumpadPage.GetKeyBinds()

        return binds

    def BindStyle(self):
        return ['No Binds', 'Sandolphan', 'qwy Numpad', 'qwy PetMouse'][self.BindStyleNotebook.GetSelection()]

    def GetPetName(self, idx):
        cblabels  = ['Minion 1', 'Minion 2', 'Minion 3', 'Lt 1', 'Lt 2', 'Boss']
        return self.Ctrls[f'Pet{idx+1}Name'].GetValue() or cblabels[idx]

    def SynchronizeUI(self) -> None:
        ismm = self.Profile.Archetype() == "Mastermind"
        pset = self.Profile.Primary()

        # disable these for non-mm even though the tab is missing so WriteBinds doesn't find them
        # TODO - it's weird-feeling to have the whole page turned off when you haven't picked
        # a primary powerset yet.  We probably need some sort of warning somewhere somehow.
        for control in self.Ctrls.values(): control.Enable(bool(ismm and pset))
        self.OnLevelChanged()
        if self.BindStyle() == 'Sandolphan':
            self.SandolphanPage.SynchronizeUI()
        if self.BindStyle() == 'qwy Numpad':
            self.qwyNumpadPage.SynchronizeUI()

        self.OnBindStyleChanged()

    def OnBindStyleChanged(self, evt = None):
        bindstyle = self.BindStyle()
        for ctrl in self.SandolphanPage.SandolphanKeyButtons.values():
            ctrl.Enable(bindstyle == 'Sandolphan')

        for ctrl in self.qwyPetMousePage.qwyPetMouseKeyButtons.values():
            ctrl.Enable(bindstyle == 'qwy PetMouse')

        self.Profile.CheckAllConflicts()

        # we want to re-fill the gameplay trays if we're no longer using '2' and '4' from PetMouse
        # TODO - should this just be part of CheckAllConflicts?
        self.Profile.Gameplay.OnKeybindProfilePicker()

        if bindstyle == 'Sandolphan':
            self.SandolphanPage.SynchronizeUI()
        elif bindstyle == 'qwy Numpad':
            self.qwyNumpadPage.SynchronizeUI()

        if evt: evt.Skip()

    def OnLevelChanged(self, evt = None) -> None:
        if evt: evt.Skip()
        bossLevel = 22 if self.Profile.Server() == 'Homecoming' else 26
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
        if self.BindStyle() == 'Sandolphan':
            self.SandolphanPage.SynchronizeUI()
        elif self.BindStyle() == 'qwy Numpad':
            self.qwyNumpadPage.SynchronizeUI()
        if evt: evt.Skip()

    def CheckUndefNames(self) -> None:
        for i in (1,2,3,4,5,6):
            ctrl = self.Ctrls[f'Pet{i}Name']
            # No errors if the control is disabled please
            if not ctrl.IsEnabled() or ctrl.GetValue():
                ctrl.RemoveError('undef')
            else:
                ctrl.AddError('undef', 'Many BindControl Mastermind binds require the pet name be filled in.')

    def CheckUniqueNames(self) -> None:
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
                # No errors if the control is disabled please
                if not ctrl.IsEnabled() or not ctrl.GetValue() or self.uniqueNames[i-1]:
                    ctrl.RemoveError('unique')
                else:
                    ctrl.AddError('unique', 'This pet name is not different enough to identify it uniquely.  This is likely to cause issues with many of BindControl\'s Mastermind binds.')

    def PopulateBindFiles(self) -> bool:

        profile = self.Profile
        ResetFile = profile.ResetFile()

        if not profile.Archetype() == 'Mastermind': return True

        # First, deduce which "pet name boxes" need checking, and in what order.
        OrderedPetBoxes = []
        petPowers = GameData.MMPowerSets[profile.Primary()]['abbrs']
        # now order them by powername, alphabetically, to match the in-game pet list
        # We need this to get them in the right order for "petselect" in the rename bind
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
        if self.BindStyle() in ['Sandolphan', 'qwy PetMouse']:
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
        for pet in range(6):
            feedback = ''
            selfile = ''
            # TODO - would this make more sense fully integrated into mm(Quiet)SubBind?
            if self.BindStyle() == 'Sandolphan':
                selfile = 'sel.txt'
                if self.GetState('PetChattyDefault'):
                    feedback = self.SandolphanPage.GetChatString('PetSelectAll', pet+1)
                    selfile = 'csel.txt'
                selfile = profile.BLF('mmb', selfile)
            ResetFile.SetBind(
                self.Ctrls[f"Pet{pet+1}Select"].MakeBind(
                    [feedback, f"petselectname {self.uniqueNames[pet]}", selfile]
                )
            )

        ### Then, the bindstyles
        bindstyle = self.BindStyle()
        if bindstyle == 'Sandolphan':
            self.SandolphanPage.PopulateBindFiles()
        elif bindstyle == 'qwy Numpad':
            self.qwyNumpadPage.PopulateBindFiles()
        elif bindstyle == 'qwy PetMouse':
            self.qwyPetMousePage.PopulateBindFiles()

        return True

    def AllBindFiles(self) -> dict[str, list]:
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
                for tsel in range(tsize+1):
                    files.append(self.Profile.GetBindFile('petsel', f"{tsize}{tsel}.txt"))

        # Might be nice to wedge AllBindFiles into each page so they control their own etc etc.
        for fn in ['all', 'min1', 'min2', 'min3', 'lt1', 'lt2', 'bos', 'mins', 'lts', '1up', '2up', '1sel', '2sel', '3sel']:
            files.append(self.Profile.GetBindFile('mmqn', f'{fn}.txt'))

        for fn in ['off', 'all', 't1-1', 't1-2', 't1-3', 't2-1', 't2-2', 't3']:
            files.append(self.Profile.GetBindFile('mmqpm', f'{fn}.txt'))

        return {
            'files' : files,
            # putting the old "mmbinds" dir in here for now to clean up old bindsdirs
            'dirs'  : ['mmbinds', 'mmb', 'petsel', 'mmqn', 'mmqpm'],
        }

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
def FindSmallestUniqueSubstring(names) -> list:
    uniqueNames = [''] * len(names)
    ### For each name
    for nameInd, name in enumerate(names):
        ### For each possible substring length
        for windowSize in range(1,len(name)+1):
            ### For each starting index of a substring
            for substrInd in range(len(name)-windowSize+1):
                substr = name[substrInd:substrInd+windowSize].lower()
                foundMatch = False
                ### For each other name
                for otherNameInd in range(len(names)):
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
