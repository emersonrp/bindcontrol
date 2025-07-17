import re
import wx
import UI
from Help import ShowHelpWindow
from Page.Mastermind import MMPowerSets
from UI.BindWizard import WizardParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED

class RenamePets(WizardParent):
    WizardName  = 'Rename Mastermind Pets'
    WizToolTip  = 'Create a keybind that will rename your pets in-game to match your BindControl configuration'

    def BuildUI(self, dialog, init = {}):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(wx.Size(700,-1))

        profile = wx.App.Get().Main.Profile

        if setName := init.get('Title', ''):
            setName = f' "{setName}"'

        dialog.SetTitle(f"Rename Pets{setName}")

        topControlSizer = wx.BoxSizer(wx.HORIZONTAL)

        # we only care up to level 24 on Homecoming, up to 26 on Rebirth
        maxValue = 24 if profile.Server == 'Homecoming' else 26
        self.LevelSlider = wx.Slider(dialog, minValue = 1, maxValue = maxValue, value = maxValue,
                                     style = wx.SL_LABELS|wx.SL_AUTOTICKS)
        self.LevelSlider.Bind(wx.EVT_SCROLL, self.OnLevelChanged)
        self.LevelSlider.SetToolTip('Select the level of your Mastermind')

        topControlSizer.Add(wx.StaticText(dialog, label = "Mastermind level:"), 0, wx.ALIGN_CENTER_VERTICAL)
        topControlSizer.Add(self.LevelSlider, 1, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)

        PetBoxSizer = wx.BoxSizer(wx.HORIZONTAL)

        Groups = {
            'min' : wx.StaticBoxSizer(wx.HORIZONTAL, dialog),
            'lts' : wx.StaticBoxSizer(wx.HORIZONTAL, dialog),
            'bos' : wx.StaticBoxSizer(wx.HORIZONTAL, dialog),
        }

        minBox1 = PetBox(Groups['min'], self, 1)
        minBox2 = PetBox(Groups['min'], self, 2)
        minBox3 = PetBox(Groups['min'], self, 3)
        ltsBox1 = PetBox(Groups['lts'], self, 4)
        ltsBox2 = PetBox(Groups['lts'], self, 5)
        bosBox  = PetBox(Groups['bos'], self, 6)

        Groups['min'].Add(minBox1, 1, wx.EXPAND|wx.ALL, 5)
        Groups['min'].Add(minBox2, 1, wx.EXPAND|wx.ALL, 5)
        Groups['min'].Add(minBox3, 1, wx.EXPAND|wx.ALL, 5)
        Groups['lts'].Add(ltsBox1, 1, wx.EXPAND|wx.ALL, 5)
        Groups['lts'].Add(ltsBox2, 1, wx.EXPAND|wx.ALL, 5)
        Groups['bos'].Add(bosBox , 1, wx.EXPAND|wx.ALL, 5)

        petPowers = MMPowerSets[profile.Primary()]

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
        profile = wx.App.Get().Main.Profile
        profile.SetModified()
        profile.CheckAllConflicts()
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

        profile = wx.App.Get().Main.Profile

    def AllBindFiles(self):
        profile = wx.App.Get().Main.Profile
        title = re.sub(r'\W+', '', self.BindPane.Title)

        return {
            'files' : [
                profile.GetBindFile('wiz', f'{title}1.txt'),
                profile.GetBindFile('wiz', f'{title}2.txt'),
            ],
            'dirs'  : [],
        }

    def ShowHelp(self, evt = None):
        if evt: evt.Skip()
        ShowHelpWindow(self.BindPane, 'PetRename.html')

    def OnLevelChanged(self, evt = None):
        if evt: evt.Skip()

    def OnPetNameChanged(self, evt = None):
        if evt: evt:Skip()

class PetBox(wx.Panel):
    def __init__(self, parent, wizard, boxnum):
        super().__init__(parent.GetStaticBox())

        profile = wx.App.Get().Main.Profile
        petPowers = MMPowerSets[profile.Primary()]
        c = profile.Mastermind.Ctrls

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(wx.StaticText(self, label = petPowers['names'][boxnum - 1]), wx.ALIGN_CENTER|wx.ALL, 5)
        self.PetName = wx.TextCtrl(self, value = c[f'Pet{boxnum}Name'].GetValue(), style = wx.TE_CENTER)
        self.PetName.SetHint('New Pet Name')
        self.PetName.Bind(wx.EVT_TEXT, wizard.OnPetNameChanged)
        sizer.Add(self.PetName, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(sizer)
