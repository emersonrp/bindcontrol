import wx
from UI.PowerPicker import PowerPicker
from Icon import GetIcon
from UI.PowerBinderCommand import PowerBinderCommand

####### Auto Power
class AutoPowerCmd(PowerBinderCommand):
    Name = "Auto Power"
    Menu = "Powers"
    def BuildUI(self, dialog):
        autoPowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(dialog, -1, "Power:")
        label.SetToolTip("Turn on auto-attack for the specified power")
        autoPowerSizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.autoPowerName = PowerPicker(dialog)
        self.autoPowerName.SetToolTip("Turn on auto-attack for the specified power")
        autoPowerSizer.Add(self.autoPowerName, 1, wx.ALIGN_CENTER_VERTICAL)

        return autoPowerSizer

    def MakeBindString(self):
        cmd = "powexecauto" if self.Profile.Server == 'Homecoming' else 'px_at'
        return f"{cmd} {self.autoPowerName.GetLabel()}"

    def Serialize(self):
        return {
            'pname' : self.autoPowerName.GetLabel(),
            'picon' : self.autoPowerName.IconFilename
        }

    def Deserialize(self, init):
        if init.get('pname', ''): self.autoPowerName.SetLabel(init['pname'])
        if init.get('picon', ''): self.autoPowerName.SetBitmap(GetIcon(init['picon']))
