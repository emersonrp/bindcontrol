from functools import partial
import re
import wx
import UI
import GameData
from Icon import GetIcon
from Help import ShowHelpWindow
from UI.BindWizard import WizardParent
from UI.IncarnateBox import IncarnateBox
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED

class IncarnateSet(WizardParent):
    WizardName  = 'Incarnate Powers Set'
    WizToolTip  = 'Create a keybind that, with multiple presses, will load a particular set of Incarnate Powers'

    def BuildUI(self, init = {}):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(wx.Size(700,-1))

        if setName := init.get('Title', ''):
            setName = f' "{setName}"'

        self.SetTitle(f"Incarnate Set{setName}")

        self.IncarnateBox = IncarnateBox(self, GameData.Server)
        if wizdata := init.get('WizData', None):
            if incdata := wizdata.get('IncData', None):
                self.IncarnateBox.FillWith(incdata)
        mainSizer.Add(self.IncarnateBox, 1, wx.EXPAND|wx.ALL, 10)

        return mainSizer

    def Serialize(self):
        return {
            'IncData' : self.GetData(),
            'BindKey' : self.BindKeyCtrl.Key,
        }

    def GetData(self):
        return self.IncarnateBox.GetData()

    def PaneContents(self):
        panel = wx.Panel(self.CollPane.GetPane())
        panel.Bind(wx.EVT_LEFT_DOWN, self.CollPane.ReshowWizard)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)

        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        incarnateData = self.IncarnateBox.GetData()
        for slot in ['Alpha', 'Interface', 'Judgement', 'Destiny', 'Lore', 'Hybrid', 'Genesis',]:
            if slotData := incarnateData.get(slot, None):
                icon = GetIcon(slotData['iconfile'])
                bitmap = wx.GenericStaticBitmap(panel, wx.ID_ANY, icon)
                bitmap.Bind(wx.EVT_ENTER_WINDOW, partial(self.OnHoverIcon, f"<b>{slot}</b>: {slotData['power']}"))
                bitmap.Bind(wx.EVT_LEAVE_WINDOW, partial(self.OnHoverIcon, None))
                bitmap.Bind(wx.EVT_LEFT_DOWN, self.CollPane.ReshowWizard)
                listSizer.Add(bitmap, 0, wx.ALL, 5)
        self.HoverDisplay = wx.StaticText(panel, wx.ID_ANY)
        self.HoverDisplay.Bind(wx.EVT_LEFT_DOWN, self.CollPane.ReshowWizard)
        listSizer.Add(self.HoverDisplay, 1, wx.ALL, 10)

        panelSizer.Add(listSizer, 1, wx.ALIGN_CENTER|wx.ALL, 15)

        bindkey = self.CollPane.Init.get('BindKey', '')
        BindSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindKeyCtrl = bcKeyButton(panel, -1, {
            'CtlName' : self.CollPane.MakeCtlName("BindKey"),
            'Page'    : self.CollPane.Page,
            'Key'     : bindkey,
        })
        self.BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.OnKeyChanged)
        BindSizer.Add(wx.StaticText(panel, -1, "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(self.BindKeyCtrl,                      0, wx.ALIGN_CENTER_VERTICAL)
        self.CollPane.Page.Ctrls[self.BindKeyCtrl.CtlName] = self.BindKeyCtrl
        UI.Labels[self.BindKeyCtrl.CtlName] = f'Incarnate Set Bind "{self.Title}"'

        panelSizer.Add(BindSizer, 0, wx.EXPAND|wx.ALL, 15)
        panel.SetSizer(panelSizer)

        self.OnHoverIcon('')
        self.CheckIfWellFormed()

        return panel

    def OnHoverIcon(self, markup, evt = None):
        if markup:
            self.HoverDisplay.SetForegroundColour(wx.BLACK)
            self.HoverDisplay.SetLabelMarkup(markup)
        else:
            self.HoverDisplay.SetForegroundColour(wx.Colour(128, 128, 128))
            self.HoverDisplay.SetLabelMarkup("Incarnate Power Set - Hover any icon for details")
        if evt: evt.Skip()

    def OnKeyChanged(self, _):
        profile = wx.App.Get().Main.Profile
        profile.SetModified()
        profile.CheckAllConflicts()
        self.CheckIfWellFormed()

    def CheckIfWellFormed(self):
        isWellFormed = True

        bk = self.CollPane.Page.Ctrls[self.CollPane.MakeCtlName('BindKey')]
        if bk.Key:
            bk.RemoveError('undef')
        else:
            bk.AddError('undef', 'The keybind has not been selected')
            isWellFormed = False

        return isWellFormed

    def PopulateBindFiles(self):
        if not self.CheckIfWellFormed():
            wx.MessageBox(f"Incarnate Set Bind \"{self.Title}\" is not complete or has errors.  Not written to bindfile.")
            return

        profile = wx.App.Get().Main.Profile

        incdata = self.GetData()
        incarnate_lines = ['']
        title = re.sub(r'\W+', '', self.CollPane.Title)
        fake_blf = profile.BLF('wiz', f'{title}X')
        extra_len = len(f"$$bindloadfilesilent {fake_blf}$$t $name, X of X, Press Again")
        for slot, data in incdata.items():
            if data['power'] == "Disable Slot":
                incarnate_command = f'incarnateunequipbyslot {slot}'
            else:
                powername = re.sub(r' ', '_', data['power'])
                incarnate_command = f'incarnate_equip {slot} {powername}'
            if len(incarnate_lines[-1]) == 0:
                incarnate_lines[-1] = incarnate_command
            elif (len(incarnate_lines[-1]) + len(incarnate_command)) > (255 - extra_len):
                incarnate_lines.append(incarnate_command)
            else:
                incarnate_lines[-1] = f'{incarnate_lines[-1]}$${incarnate_command}'

        for i, line in enumerate(incarnate_lines):
            bindfile = profile.GetBindFile('wiz', f'{title}{i}')

            if (i+1 < len(incarnate_lines)):
                nextfile = i+1
                line = line + f'$$t $name, {i+1} of {len(incarnate_lines)}, Press Again'
            else:
                nextfile = 0
                line = line + '$$t $name, Set Loaded'

            line = line + profile.BLF('wiz', f'{title}{nextfile}')
            if i == 0: # start with the reset file, too
                profile.ResetFile().SetBind(self.BindKeyCtrl.MakeFileKeyBind(line))
            bindfile.SetBind(self.BindKeyCtrl.MakeFileKeyBind(line))

    def ShowHelp(self, evt = None):
        if evt: evt.Skip()
        ShowHelpWindow(self, 'IncarnateWizard.html')
