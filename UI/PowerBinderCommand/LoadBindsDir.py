import wx
from pathlib import PureWindowsPath
import Models.ProfileData as ProfileData
from UI.PowerBinderCommand import PowerBinderCommand

####### Load Binds Directory
class LoadBindsDir(PowerBinderCommand):
    Name = "Load Binds Directory"
    Menu = "Misc"

    def BuildUI(self, dialog):
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        lbSizer = wx.BoxSizer(wx.HORIZONTAL)
        lbText = wx.StaticText(dialog, -1, "Load Binds Directory:")
        lbText.SetToolTip('Select an existing profile directory from which to load a set of bind files')
        lbSizer.Add(lbText, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)

        profiles = ProfileData.GetAllProfileBindsDirs(wx.ConfigBase.Get())

        self.lbPicker = wx.Choice(dialog, -1, choices = sorted(profiles))
        self.lbPicker.SetToolTip('Select an existing profile directory from which to load a set of bind files')
        lbSizer.Add(self.lbPicker, 1, wx.ALIGN_CENTER_VERTICAL)

        mainSizer.Add(lbSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        self.lbResetCB = wx.CheckBox(dialog, -1, "Reset All Keybinds Before Loading")
        self.lbResetCB.SetValue(True)

        mainSizer.Add(self.lbResetCB, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        return mainSizer

    def MakeBindString(self):

        # If the specified binds directory disappeared between runs, we'd crash, so handle that.
        if self.lbPicker.GetSelection() == wx.NOT_FOUND: return ''

        config = wx.ConfigBase.Get()
        if config.Exists('GameBindPath'):
            bindpath = config.Read('GameBindPath')
        else:
            bindpath = config.Read('BindPath')

        reset = ""
        if self.lbResetCB.GetValue():
            reset = "keybind_reset$$"

        resetfilepath = PureWindowsPath(bindpath) / self.lbPicker.GetString(self.lbPicker.GetSelection()) / 'reset.txt'
        return reset + 'bindloadfile ' + str(resetfilepath)

    def Serialize(self):
        return {'LoadBindProfile' : self.lbPicker.GetString(self.lbPicker.GetSelection()),
                'ResetKeybinds'   : self.lbResetCB.GetValue(),
                }

    def Deserialize(self, init):
        if init.get('LoadBindProfile', ''): self.lbPicker.SetSelection(self.lbPicker.FindString(init['LoadBindProfile']))
        self.lbResetCB.SetValue(init.get('ResetKeybinds', False))
