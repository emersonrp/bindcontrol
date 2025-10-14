from functools import partial
import re
import wx
import UI
import GameData
from Icon import GetIcon
from UI.BindWizard import WizardParent
from UI.IncarnateBox import IncarnateBox
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED

class IncarnateSet(WizardParent):
    WizardName  = 'Incarnate Powers Set'
    WizToolTip  = 'Create a keybind that, with multiple presses, will load a particular set of Incarnate Powers'
    WizHelpFile = 'IncarnateWizard.html'

    def __init__(self, parent, init) -> None:
        super().__init__(parent, init)
        self.IncarnateBox : IncarnateBox|None = None

    def BuildUI(self, dialog, init : dict|None = None) -> wx.Sizer:
        init = init or {}
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(wx.Size(700,-1))

        self.IncarnateBox = IncarnateBox(dialog, GameData.Server)
        if wizdata := init.get('WizData'):
            if incdata := wizdata.get('IncData'):
                self.IncarnateBox.FillWith(incdata)
        mainSizer.Add(self.IncarnateBox, 1, wx.EXPAND|wx.ALL, 10)

        return mainSizer

    def Serialize(self):
        return {
            'IncData' : self.State.get('WizData', {}).get('IncData', {}),
            'BindKey' : self.BindKeyCtrl.Key,
        }

    def PaneContents(self):
        bindpane = self.BindPane
        panel = wx.Panel(bindpane.GetPane())
        panel.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)

        listSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Fill State from the dialog, if it exists
        if self.IncarnateBox:
            if not self.State.get('WizData'):
                self.State['WizData'] = {}
            newdata = self.IncarnateBox.Serialize()
            if self.State['WizData'].get('IncData', {}) != newdata:
                self.BindPane.Page.UpdateAllBinds()
                self.State['WizData']['IncData'] = newdata

        # and then in either case, build the Pane from State
        incarnateData = self.State.get('WizData', {}).get('IncData', {})
        for slot in ['Alpha', 'Interface', 'Judgement', 'Destiny', 'Lore', 'Hybrid', 'Genesis',]:
            if slotData := incarnateData.get(slot):
                icon = GetIcon(slotData['iconfile']) # pyright: ignore
                bitmap = wx.GenericStaticBitmap(panel, bitmap = icon)
                bitmap.Bind(wx.EVT_ENTER_WINDOW, partial(self.OnHoverIcon, f"<b>{slot}</b>: {slotData['power']}")) # pyright: ignore
                bitmap.Bind(wx.EVT_LEAVE_WINDOW, partial(self.OnHoverIcon, None))
                bitmap.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
                listSizer.Add(bitmap, 0, wx.ALL, 5)
        self.HoverDisplay = wx.StaticText(panel)
        self.HoverDisplay.Bind(wx.EVT_LEFT_DOWN, self.ShowWizard)
        listSizer.Add(self.HoverDisplay, 1, wx.ALL, 10)

        panelSizer.Add(listSizer, 1, wx.ALIGN_CENTER|wx.ALL, 15)

        bindkey = bindpane.Init.get('BindKey', '')
        BindSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindKeyCtrl = bcKeyButton(panel, init = {
            'CtlName' : bindpane.MakeCtrlName("BindKey"),
            'Page'    : bindpane.Page,
            'Key'     : bindkey,
        })
        self.BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.OnKeyChanged)
        BindSizer.Add(wx.StaticText(panel, label = "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(self.BindKeyCtrl,                      0, wx.ALIGN_CENTER_VERTICAL)
        bindpane.Ctrls[self.BindKeyCtrl.CtlName] = self.BindKeyCtrl
        UI.Labels[self.BindKeyCtrl.CtlName] = f'Incarnate Set Bind "{bindpane.Title}"'

        panelSizer.Add(BindSizer, 0, wx.EXPAND|wx.ALL, 15)
        panel.SetSizer(panelSizer)

        self.OnHoverIcon('')
        self.CheckIfWellFormed()

        return panel

    def UpdateState(self):
        if self.IncarnateBox:
            self.State = { 'WizData' : { 'IncData' : self.IncarnateBox.Serialize() } }

    def OnHoverIcon(self, markup, evt = None):
        if markup:
            self.HoverDisplay.SetForegroundColour(wx.BLACK)
            self.HoverDisplay.SetLabelMarkup(markup)
        else:
            self.HoverDisplay.SetForegroundColour(wx.Colour(128, 128, 128))
            self.HoverDisplay.SetLabelMarkup("Incarnate Power Set - Hover any icon for details;  click anywhere to edit")
        if evt: evt.Skip()

    def OnKeyChanged(self, evt):
        evt.Skip()
        self.CheckIfWellFormed()

    def CheckIfWellFormed(self) -> bool:
        isWellFormed = True

        bk = self.BindPane.GetCtrl('BindKey')
        if not bk:
            wx.LogError("BindKey missing from Ctrls in IncarnateSet.CheckIfWellFormed - this is a bug!")
            isWellFormed = False

        else:
            if bk.Key:
                bk.RemoveError('undef')
            else:
                bk.AddError('undef', 'The keybind has not been selected')
                isWellFormed = False

        return isWellFormed

    def PopulateBindFiles(self):
        profile = self.Profile

        incdata = self.State.get('WizData', {}).get('IncData', {})
        incarnate_lines = ['']
        title = re.sub(r'\W+', '', self.BindPane.Title)
        fake_blf = profile.BLF('wiz', f'{title}X')
        extra_len = len(f"$$bindloadfilesilent {fake_blf}$$t $name, X of X, Press Again")
        for slot, data in incdata.items():
            if data['power'] == "Disable Slot": # pyright: ignore
                incarnate_command = f'incarnateunequipbyslot {slot}'
            else:
                powername = re.sub(r' ', '_', data['power']) # pyright: ignore
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
        title = re.sub(r'\W+', '', self.BindPane.Title)

        files = []

        for i in range(6): # should not ever possibly be six steps, but....
            files.append(self.Profile.GetBindFile('wiz', f'{title}{i}.txt'))
        return {
            'files' : files,
            'dirs'  : [],
        }
