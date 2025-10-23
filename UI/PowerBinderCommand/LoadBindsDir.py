import wx
from pathlib import PureWindowsPath
from UI.PowerBinderCommand import PowerBinderCommand
from Util.Paths import GetAllProfileBindsDirs, CheckProfileForBindsDir

####### Load Binds Directory
class LoadBindsDir(PowerBinderCommand):
    Name = "Load Different Profile's Binds"
    Menu = "Misc"
    DeprecatedName = "Load Binds Directory"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        lbSizer = wx.BoxSizer(wx.HORIZONTAL)
        lbText = wx.StaticText(dialog, label = "Load Different Profile's Binds:")
        lbText.SetToolTip('Select an existing profile from which to load a set of bind files')
        lbSizer.Add(lbText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)

        self.NameToDir = {}
        self.DirToName = {}
        profiles = GetAllProfileBindsDirs(wx.ConfigBase.Get())
        for p in profiles:
            if bd := CheckProfileForBindsDir(wx.ConfigBase.Get(), p):
                self.NameToDir[bd] = p
                self.DirToName[p] = bd

        self.lbPicker = wx.Choice(dialog, choices = sorted(self.NameToDir.keys(), key = str.casefold))
        self.lbPicker.SetToolTip('Select an existing profile directory from which to load a set of bind files')
        lbSizer.Add(self.lbPicker, 1, wx.ALIGN_CENTER_VERTICAL)

        mainSizer.Add(lbSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        self.lbResetCB = wx.CheckBox(dialog, label = "Reset All Keybinds Before Loading")
        self.lbResetCB.SetValue(True)

        mainSizer.Add(self.lbResetCB, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        return mainSizer

    def MakeBindString(self) -> str:

        # If the specified binds directory disappeared between runs, we'd crash, so handle that.
        if self.lbPicker.GetSelection() == wx.NOT_FOUND: return ''

        config = wx.ConfigBase.Get()
        if config.Exists('GameBindPath'):
            bindpath = config.Read('GameBindPath')
        else:
            bindpath = config.Read('BindPath')

        reset = ""
        if self.lbResetCB.GetValue():
            reset = "unbindall$$"

        pname = self.lbPicker.GetStringSelection()
        resetfilepath = PureWindowsPath(bindpath) / self.NameToDir[pname] / 'reset.txt'
        return reset + 'bindloadfile ' + str(resetfilepath)

    # for backwards compatibility, we store the dir, not the name
    def Serialize(self) -> dict:
        return {
            'LoadBindProfile' : self.NameToDir[self.lbPicker.GetStringSelection()],
            'ResetKeybinds'   : self.lbResetCB.GetValue(),
        }

    def Deserialize(self, init) -> None:
        if init.get('LoadBindProfile', ''):
            self.lbPicker.SetStringSelection(self.DirToName.get(init['LoadBindProfile'], ''))
        self.lbResetCB.SetValue(init.get('ResetKeybinds', False))
