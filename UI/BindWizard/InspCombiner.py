import re
import wx
from wx.adv import BitmapComboBox
import GameData
from Icon import GetIcon, GetIconBitmap
import UI
from UI.BindWizard import WizardParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED

class InspCombiner(WizardParent):
    WizardName  = 'Inspiration Combiner'
    WizToolTip  = 'Create a keybind that, with multiple presses, will combine inspirations and optionally consume them'
    WizHelpFile = 'InspCombiner.html'
    IconPath    = ('Inspirations', 'FuriousRage')

    def __init__(self, parent, init) -> None:
        super().__init__(parent, init)

    def BuildUI(self, dialog, init : dict|None = None) -> wx.Sizer:

        init = init or {}
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.SetMinSize(wx.Size(700,-1))

        # picker for which type we're working with
        typePickerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.TypePicker = BitmapComboBox(dialog, style = wx.CB_READONLY)
        for info in GameData.Inspirations['Single'].values():
            baseicon = GetIconBitmap('Inspirations', info['tiers'][0])
            self.TypePicker.Append(info['displayname'], baseicon)
        self.TypePicker.SetSelection(0)
        self.TypePicker.Bind(wx.EVT_COMBOBOX, self.GetCorrectInspCheckboxes)

        typePickerSizer.Add(wx.StaticText(dialog, label = 'Inspiration Type:', style=wx.ALIGN_RIGHT), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        typePickerSizer.Add(self.TypePicker, 1, wx.ALL, 5)

        mainSizer.Add(typePickerSizer, 0, wx.EXPAND|wx.ALL, 10)

        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        # sizer for the various option-style toggles
        optsSizer = wx.StaticBoxSizer(wx.VERTICAL, dialog, 'Options')
        bottomSizer.Add(optsSizer, 1, wx.EXPAND|wx.ALL, 10)

        # sizer for the checkboxes for the other types to combine
        self.CBSizer = wx.StaticBoxSizer(wx.VERTICAL, dialog, 'Combine Inspiration Types')
        bottomSizer.Add(self.CBSizer, 1, wx.EXPAND|wx.ALL, 10)

        mainSizer.Add(bottomSizer, 0, wx.EXPAND|wx.ALL, 10)

        self.GetCorrectInspCheckboxes()

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
        # TODO actual pane contents go here once we figure them out
        panelSizer.Add(listSizer, 1, wx.ALIGN_CENTER|wx.ALL, 15)

        # And the bind key
        bindkey = bindpane.Init.get('BindKey', '')
        BindSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.BindKeyCtrl = bcKeyButton(panel, init = {
            'CtlName' : bindpane.MakeCtrlName("BindKey"),
            'Page'    : bindpane.Page,
            'Key'     : bindkey,
        })
        self.BindKeyCtrl.Bind(EVT_KEY_CHANGED, self.OnKeyChanged)
        BindSizer.Add(wx.StaticText(panel, label = "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(self.BindKeyCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        bindpane.Ctrls[self.BindKeyCtrl.CtlName] = self.BindKeyCtrl
        UI.Labels[self.BindKeyCtrl.CtlName] = f'Incarnate Set Bind "{bindpane.Title}"'

        panelSizer.Add(BindSizer, wx.ALL, 10)

        panel.SetSizer(panelSizer)

        return panel

    def OnKeyChanged(self, evt = None):
        if evt: evt.Skip()

    def UpdateState(self):
        self.State = { 'WizData' : { } }

    def GetCorrectInspCheckboxes(self, evt = None):
        if evt: evt.Skip()

        currtype = self.TypePicker.GetStringSelection()
        self.CBSizer.Clear(delete_windows = True)
        for insptype in GameData.Inspirations['Single']:
            if insptype == currtype: continue
            self.CBSizer.Add(InspirationTypeCheckBox(self.CBSizer.GetStaticBox(), insptype), 0, wx.ALIGN_LEFT|wx.ALL, 5)

        self.Dialog().Layout()

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

# call with parent, insp name
class InspirationTypeCheckBox(wx.Panel):
    def __init__(self, parent, insptype):
        super().__init__(parent)

        self.InspType = insptype

        inspdata = GameData.Inspirations['Single'][insptype]

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.CheckBox = wx.CheckBox(self)
        sizer.Add(self.CheckBox, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        insp = inspdata['tiers'][0] # get min tier icon just because
        insp = re.sub(' ', '', insp)

        bitmap = wx.StaticBitmap(self, bitmap = GetIcon('Inspirations', insp))
        sizer.Add(bitmap, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        bitmap.Bind(wx.EVT_LEFT_DOWN, self.OnSomethingClicked)

        # this speaks to some sort of lack of vision on my part in GameData
        label = wx.StaticText(self, label = inspdata['displayname'])
        sizer.Add(label, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        label.Bind(wx.EVT_LEFT_DOWN, self.OnSomethingClicked)

        self.SetSizer(sizer)

    def OnSomethingClicked(self, evt):
        evt.Skip()
        self.CheckBox.SetValue(not self.CheckBox.GetValue())
