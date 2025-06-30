import wx
from UI.PowerPicker import PowerPicker
from Icon import GetIcon
from UI.PowerBinderCommand import PowerBinderCommand

####### Use Power
class UsePowerCmd(PowerBinderCommand):
    Name = "Use Power"
    Menu = "Powers"

    def BuildUI(self, dialog):
        outerSizer = wx.BoxSizer(wx.HORIZONTAL)

        usePowerSizer = wx.GridBagSizer(5,5)
        usePowerSizer.Add(wx.StaticText(dialog, -1, "Method:"), (0,0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.usePowerRBToggle = wx.RadioButton(dialog, -1, "Toggle", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL)
        usePowerSizer.Add(self.usePowerRBToggle, (0,1))
        self.usePowerRBOn = wx.RadioButton(dialog, -1, "On", style=wx.ALIGN_CENTER_VERTICAL)
        usePowerSizer.Add(self.usePowerRBOn, (0,2))
        self.usePowerRBOff = wx.RadioButton(dialog, -1, "Off", style=wx.ALIGN_CENTER_VERTICAL)
        usePowerSizer.Add(self.usePowerRBOff, (0,3))
        usePowerSizer.Add(wx.StaticText(dialog, -1, "Power:"), (1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        self.usePowerName = PowerPicker(dialog)
        usePowerSizer.Add(self.usePowerName, (1,1), (1,3), flag=wx.EXPAND)
        usePowerSizer.AddGrowableCol(3)

        outerSizer.Add(usePowerSizer, 1, wx.ALIGN_CENTER_VERTICAL)

        return outerSizer

    def MakeBindString(self):
        server = self.Profile.Server
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
