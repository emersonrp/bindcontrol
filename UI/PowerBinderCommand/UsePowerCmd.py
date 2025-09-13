import wx
from UI.PowerPicker import PowerPicker
from Icon import GetIcon
from UI.PowerBinderCommand import PowerBinderCommand

####### Use Power
class UsePowerCmd(PowerBinderCommand):
    Name = "Use Power"
    Menu = "Powers"

    def BuildUI(self, dialog):
        usePowerSizer = wx.FlexGridSizer(2, 2, 5, 5)
        usePowerSizer.AddGrowableCol(1)

        usePowerSizer.Add(wx.StaticText(dialog, -1, "Method:"), flag = wx.ALIGN_CENTER_VERTICAL)

        rbSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.usePowerRBToggle = wx.RadioButton(dialog, -1, "Toggle", style = wx.ALIGN_CENTER_VERTICAL|wx.RB_GROUP)
        rbSizer.Add(self.usePowerRBToggle, 1)
        self.usePowerRBOn = wx.RadioButton(dialog, -1, "On", style = wx.ALIGN_CENTER_VERTICAL)
        rbSizer.Add(self.usePowerRBOn, 1)
        self.usePowerRBOff = wx.RadioButton(dialog, -1, "Off", style = wx.ALIGN_CENTER_VERTICAL)
        rbSizer.Add(self.usePowerRBOff, 1)

        usePowerSizer.Add(rbSizer, 1, flag = wx.EXPAND)

        usePowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), flag = wx.ALIGN_CENTER_VERTICAL)
        self.usePowerName = PowerPicker(dialog)
        usePowerSizer.Add(self.usePowerName, 1, flag = wx.EXPAND)

        return usePowerSizer

    def MakeBindString(self):
        server = self.Profile.Server()
        if self.usePowerRBToggle.GetValue():
            method = "powexecname"
        elif self.usePowerRBOn.GetValue():
            method = "powexectoggleon" if server == "Homecoming" else "px_tgon"
        elif self.usePowerRBOff.GetValue():
            method = "powexectoggleoff" if server == "Homecoming" else "px_tgof"
        else:
            wx.LogWarning('PowerBindCmd "UsePowerCmd" got an impossible value for toggle/on/off')
            return ''

        return f"{method} {self.usePowerName.GetLabel()}"

    def Serialize(self):
        if   self.usePowerRBOn.GetValue():
            method = "powexectoggleon"
        elif self.usePowerRBOff.GetValue():
            method = "powexectoggleoff"
        else:
            method = "powexecname"

        return {
            'method': method,
            'pname' : self.usePowerName.GetLabel(),
            'picon' : self.usePowerName.IconFilename
        }

    def Deserialize(self, init):
        method = init.get('method', '')
        if method == 'powexectoggleon':
            self.usePowerRBOn.SetValue(True)
        elif method == 'powexectoggleoff':
            self.usePowerRBOff.SetValue(True)
        else:
            self.usePowerRBToggle.SetValue(True)
        if init.get('pname', ''): self.usePowerName.SetLabel(init['pname'])
        if init.get('picon', ''):
            self.usePowerName.SetBitmap(GetIcon(init['picon']))
            self.usePowerName.IconFilename = init['picon']

    def OKToClose(self):
        if self.usePowerName.HasPowerPicked():
            return True
        else:
            wx.MessageBox("You must choose a power.", "Power Not Picked")
            return False
