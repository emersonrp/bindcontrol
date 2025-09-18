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

    def __init__(self, parent, init):
        super().__init__(parent, init)
        self.IncarnateBox = None

    def BuildUI(self, dialog, init = {}):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(wx.Size(700,-1))

        if setName := init.get('Title', ''):
            setName = f' "{setName}"'

        dialog.SetTitle(f"Incarnate Set{setName}")

        self.IncarnateBox = IncarnateBox(dialog, GameData.Server)
        if wizdata := init.get('WizData', None):
            if incdata := wizdata.get('IncData', None):
                self.IncarnateBox.FillWith(incdata)
        mainSizer.Add(self.IncarnateBox, 1, wx.EXPAND|wx.ALL, 10)

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

        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Fill Init from the dialog, if it exists
        if self.IncarnateBox:
            if not self.Init.get('WizData', None):
                self.Init['WizData'] = {}
            newdata = self.IncarnateBox.Serialize()
            if self.Init['WizData'].get('IncData', {}) != newdata:
                wx.App.Get().Main.Profile.SetModified()
                self.Init['WizData']['IncData'] = newdata
        # and then in either case, build the Pane from Init
        incarnateData = self.Init.get('WizData', {}).get('IncData', {})
        for slot in ['Alpha', 'Interface', 'Judgement', 'Destiny', 'Lore', 'Hybrid', 'Genesis',]:
            if slotData := incarnateData.get(slot, None):
                icon = GetIcon(slotData['iconfile'])
                bitmap = wx.GenericStaticBitmap(panel, wx.ID_ANY, icon)
                bitmap.Bind(wx.EVT_ENTER_WINDOW, partial(self.OnHoverIcon, f"<b>{slot}</b>: {slotData['power']}"))
                bitmap.Bind(wx.EVT_LEAVE_WINDOW, partial(self.OnHoverIcon, None))
                bitmap.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
                listSizer.Add(bitmap, 0, wx.ALL, 5)
        self.HoverDisplay = wx.StaticText(panel, wx.ID_ANY)
        self.HoverDisplay.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
        listSizer.Add(self.HoverDisplay, 1, wx.ALL, 10)

        panelSizer.Add(listSizer, 1, wx.ALIGN_CENTER|wx.ALL, 15)

        bindkey = bindpane.Init.get('BindKey', '')
        BindSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindKeyCtrl = bcKeyButton(panel, -1, {
            'CtlName' : bindpane.MakeCtlName("BindKey"),
            'Page'    : bindpane.Page,
            'Key'     : bindkey,
        })
        self.BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.onKeyChanged)
        BindSizer.Add(wx.StaticText(panel, -1, "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(self.BindKeyCtrl,                      0, wx.ALIGN_CENTER_VERTICAL)
        bindpane.Ctrls[self.BindKeyCtrl.CtlName] = self.BindKeyCtrl
        UI.Labels[self.BindKeyCtrl.CtlName] = f'Incarnate Set Bind "{bindpane.Title}"'

        panelSizer.Add(BindSizer, 0, wx.EXPAND|wx.ALL, 15)
        panel.SetSizer(panelSizer)

        self.OnHoverIcon('')
        self.CheckIfWellFormed()

        return panel

    def UpdateAndRefresh(self, evt):
        if self.IncarnateBox:
            self.Init = { 'WizData' : { 'IncData' : self.IncarnateBox.Serialize() } }
        super().UpdateAndRefresh(evt)

    def OnHoverIcon(self, markup, evt = None):
        if markup:
            self.HoverDisplay.SetForegroundColour(wx.BLACK)
            self.HoverDisplay.SetLabelMarkup(markup)
        else:
            self.HoverDisplay.SetForegroundColour(wx.Colour(128, 128, 128))
            self.HoverDisplay.SetLabelMarkup("Incarnate Power Set - Hover any icon for details;  click anywhere to edit")
        if evt: evt.Skip()

    def onKeyChanged(self, evt):
        evt.Skip()
        self.CheckIfWellFormed()

    def CheckIfWellFormed(self):
        isWellFormed = True

        bk = self.BindPane.Ctrls.get(self.BindPane.MakeCtlName('BindKey'), None)
        if not bk:
            wx.LogError(f"BindKey missing from Ctrls in IncarnateSet.CheckIfWellFormed - this is a bug!")
            isWellFormed = False

        if bk.Key:
            bk.RemoveError('undef')
        else:
            bk.AddError('undef', 'The keybind has not been selected')
            isWellFormed = False

        return isWellFormed

    def PopulateBindFiles(self):
        if not self.CheckIfWellFormed():
            wx.MessageBox(f"Incarnate Set Bind \"{self.Dialog().Title}\" is not complete or has errors.  Not written to bindfile.")
            return

        profile = wx.App.Get().Main.Profile

        incdata = self.Init.get('WizData', {}).get('IncData', {})
        incarnate_lines = ['']
        title = re.sub(r'\W+', '', self.BindPane.Title)
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
            bindfile = profile.GetBindFile('wiz', f'{title}{i}.txt')

            if (i+1 < len(incarnate_lines)):
                nextfile = i+1
                line = line + f'$$t $name, {i+1} of {len(incarnate_lines)}, Press Again'
            else:
                nextfile = 0
                line = line + '$$t $name, Set Loaded'

            line = line + profile.BLF('wiz', f'{title}{nextfile}')
            if i == 0: # start with the reset file, too
                profile.ResetFile().SetBind(self.BindKeyCtrl.MakeBind(line))
            bindfile.SetBind(self.BindKeyCtrl.MakeBind(line))

    def AllBindFiles(self):
        profile = wx.App.Get().Main.Profile
        title = re.sub(r'\W+', '', self.BindPane.Title)

        files = []

        for i in range(6): # should not ever possibly be six steps, but....
            files.append(profile.GetBindFile('wiz', f'{title}{i}.txt'))
        return {
            'files' : files,
            'dirs'  : [],
        }

    def ShowHelp(self, evt = None):
        if evt: evt.Skip()
        ShowHelpWindow(self.BindPane, 'IncarnateWizard.html')
