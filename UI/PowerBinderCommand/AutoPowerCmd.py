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
        autoPowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.autoPowerName = PowerPicker(dialog)
        autoPowerSizer.Add(self.autoPowerName, 1, wx.ALIGN_CENTER_VERTICAL)

        return autoPowerSizer

    def MakeBindString(self):
        return f"powexecauto {self.autoPowerName.GetLabel()}"

    def Serialize(self):
        return {
            'pname' : self.autoPowerName.GetLabel(),
            'picon' : self.autoPowerName.IconFilename
        }

    def Deserialize(self, init):
        if init.get('pname', ''): self.autoPowerName.SetLabel(init['pname'])
        if init.get('picon', ''): self.autoPowerName.SetBitmap(GetIcon(init['picon']))
