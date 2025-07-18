import re
import wx
import UI
from Help import ShowHelpWindow
from Page.Mastermind import MMPowerSets
from UI.BindWizard import WizardParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.ControlGroup import cgTextCtrl
from Util import FindSmallestUniqueSubstring

class RenamePets(WizardParent):
    WizardName  = 'Rename Mastermind Pets'
    WizToolTip  = 'Create a keybind that will rename your pets in-game to match your BindControl configuration'

    @classmethod
    def CheckIfValidForProfile(cls, profile):
        return profile.Archetype() == "Mastermind"

    def BuildUI(self, dialog, init = {}):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(wx.Size(700,-1))

        if setName := init.get('Title', ''):
            setName = f' "{setName}"'

        dialog.SetTitle(f"Rename Pets{setName}")

        topControlSizer = wx.BoxSizer(wx.HORIZONTAL)

        # we only care up to level 24 on Homecoming, up to 26 on Rebirth
        maxValue = 24 if self.Profile.Server == 'Homecoming' else 26
        self.LevelSlider = wx.Slider(dialog, minValue = 1, maxValue = maxValue, value = maxValue,
                                     style = wx.SL_LABELS|wx.SL_AUTOTICKS)
        self.LevelSlider.Bind(wx.EVT_SCROLL, self.OnLevelChanged)
        self.LevelSlider.SetToolTip('Select the level of your Mastermind')

        topControlSizer.Add(wx.StaticText(dialog, label = "Mastermind level:"), 0, wx.ALIGN_CENTER_VERTICAL)
        topControlSizer.Add(self.LevelSlider, 1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)

        PetBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Groups are so we can put things in the right order.  This might not be The Way.
        Groups = {
            'min' : wx.StaticBoxSizer(wx.HORIZONTAL, dialog),
            'lts' : wx.StaticBoxSizer(wx.HORIZONTAL, dialog),
            'bos' : wx.StaticBoxSizer(wx.HORIZONTAL, dialog),
        }
        self.Boxes = [
            PetBox(Groups['min'], self, 1),
            PetBox(Groups['min'], self, 2),
            PetBox(Groups['min'], self, 3),
            PetBox(Groups['lts'], self, 4),
            PetBox(Groups['lts'], self, 5),
            PetBox(Groups['bos'], self, 6),
        ]
        Groups['min'].Add(self.Boxes[0], 1, wx.EXPAND|wx.ALL, 5)
        Groups['min'].Add(self.Boxes[1], 1, wx.EXPAND|wx.ALL, 5)
        Groups['min'].Add(self.Boxes[2], 1, wx.EXPAND|wx.ALL, 5)
        Groups['lts'].Add(self.Boxes[3], 1, wx.EXPAND|wx.ALL, 5)
        Groups['lts'].Add(self.Boxes[4], 1, wx.EXPAND|wx.ALL, 5)
        Groups['bos'].Add(self.Boxes[5], 1, wx.EXPAND|wx.ALL, 5)

        # "revPowers" is ["min", "lts", "bos"] sorted by their power name for the current archetype
        petPowers = MMPowerSets[self.Profile.Primary()]
        revPowers = dict(sorted(petPowers['powers'].items(), key = lambda item: item[1]))
        for grp in revPowers:
            PetBoxSizer.Add(Groups[grp], 0, wx.EXPAND|wx.ALL, 5)

        mainSizer.Add(topControlSizer, 1, wx.EXPAND|wx.ALL, 10)
        mainSizer.Add(PetBoxSizer,     1, wx.EXPAND|wx.ALL, 10)

        return mainSizer

    def Serialize(self):
        return {
            'IncData' : self.Init.get('WizData', {}).get('IncData', {}),
            'BindKey' : self.BindKeyCtrl.Key,
        }

    def PaneContents(self):
        bindpane = self.BindPane
        panel = wx.Panel(bindpane.GetPane())
        panel.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)

        bindkey = bindpane.Init.get('BindKey', '')
        BindSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindKeyCtrl = bcKeyButton(panel, -1, {
            'CtlName' : bindpane.MakeCtlName("BindKey"),
            'Page'    : bindpane.Page,
            'Key'     : bindkey,
        })
        self.BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.OnKeyChanged)
        BindSizer.Add(wx.StaticText(panel, -1, "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(self.BindKeyCtrl,                      0, wx.ALIGN_CENTER_VERTICAL)
        bindpane.Page.Ctrls[self.BindKeyCtrl.CtlName] = self.BindKeyCtrl
        UI.Labels[self.BindKeyCtrl.CtlName] = f'Rename Pets Bind "{bindpane.Title}"'

        panelSizer.Add(BindSizer, 0, wx.EXPAND|wx.ALL, 15)
        panel.SetSizer(panelSizer)

        self.CheckIfWellFormed()

        return panel

    def OnKeyChanged(self, _):
        self.Profile.SetModified()
        self.Profile.CheckAllConflicts()
        self.CheckIfWellFormed()

    def CheckIfWellFormed(self):
        isWellFormed = True

        bk = self.BindPane.Page.Ctrls.get(self.BindPane.MakeCtlName('BindKey'), None)
        if not bk:
            wx.LogError(f"BindKey missing from Ctrls in RenamePets.CheckIfWellFormed - this is a bug!")
            isWellFormed = False

        if bk.Key:
            bk.RemoveError('undef')
        else:
            bk.AddError('undef', 'The keybind has not been selected')
            isWellFormed = False

        return isWellFormed

    def PopulateBindFiles(self):
        if not self.CheckIfWellFormed():
            wx.MessageBox(f"Rename Pets Bind \"{self.Dialog().Title}\" is not complete or has errors.  Not written to bindfile.")
            return

    def AllBindFiles(self):
        title = re.sub(r'\W+', '', self.BindPane.Title)

        return {
            'files' : [
                self.Profile.GetBindFile('wiz', f'{title}1.txt'),
                self.Profile.GetBindFile('wiz', f'{title}2.txt'),
            ],
            'dirs'  : [],
        }

    def ShowHelp(self, evt = None):
        if evt: evt.Skip()
        ShowHelpWindow(self.BindPane, 'RenamePets.html')

    def OnLevelChanged(self, evt = None):
        if evt: evt.Skip()
        maxLevel = 24 if self.Profile.Server == 'Homecoming' else 26
        lvl = self.LevelSlider.GetValue()
        self.Boxes[1].Enable(lvl >= 6)
        self.Boxes[2].Enable(lvl >= 18)
        self.Boxes[3].Enable(lvl >= 12)
        self.Boxes[4].Enable(lvl >= 24)
        self.Boxes[5].Enable(lvl >= maxLevel)

    def OnPetNameChanged(self, evt = None):
        self.CheckUndefNames()
        self.CheckUniqueNames()
        if evt: evt.Skip()

    def CheckUndefNames(self):
        for box in self.Boxes:
            ctrl = box.PetName
            if ctrl.GetValue():
                ctrl.RemoveError('undef')
            else:
                ctrl.AddError('undef', 'By-Name selection and Bodyguard Mode require the pet name be filled in.')

    def CheckUniqueNames(self):
        names = []
        for box in self.Boxes:
            value = box.PetName.GetValue().strip() # don't allow whitespace at the ends
            names.append(value)

        # we stash this away every time we calculate it so we can
        # extract it trivially when we write binds
        # TODO - do we need to do this in the BindWizard?
        self.uniqueNames = FindSmallestUniqueSubstring(names)
        for i, box in enumerate(self.Boxes):
            if self.uniqueNames[i]:
                box.PetName.RemoveError('unique')
            else:
                box.PetName.AddError('unique', f'This pet name is not different enough to identify it uniquely.  This is likely to cause issues with by-name and bodyguard binds.')

class PetBox(wx.Panel):
    def __init__(self, parent, wizard, boxnum):
        super().__init__(parent.GetStaticBox())

        profile = wx.App.Get().Main.Profile
        petPowers = MMPowerSets[profile.Primary()]
        c = profile.Mastermind.Ctrls

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(wx.StaticText(self, label = petPowers['names'][boxnum - 1]), wx.ALIGN_CENTER|wx.ALL, 5)
        self.PetName = cgTextCtrl(self, value = c[f'Pet{boxnum}Name'].GetValue(), style = wx.TE_CENTER)
        self.PetName.SetHint('New Pet Name')
        self.PetName.Bind(wx.EVT_TEXT, wizard.OnPetNameChanged)
        sizer.Add(self.PetName, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(sizer)
