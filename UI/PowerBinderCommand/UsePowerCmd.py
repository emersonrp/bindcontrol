import wx
import re
from UI.PowerPicker import PowerPicker
from Icon import GetIcon
from UI.PowerBinderCommand import PowerBinderCommand

####### Use Power
class UsePowerCmd(PowerBinderCommand):
    Name = "Use Power"
    Menu = "Powers"

    def BuildUI(self, dialog) -> wx.FlexGridSizer:
        self.Dialog = dialog

        self.UsePowerSizer = wx.FlexGridSizer(3, 2, 5, 5)
        self.UsePowerSizer.AddGrowableCol(1)

        server = self.Profile.Server()

        self.UsePowerSizer.Add(wx.StaticText(dialog, label = "Method:"), flag = wx.ALIGN_CENTER_VERTICAL)

        rbSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.usePowerRBToggle = wx.RadioButton(dialog, label = "Toggle", style = wx.ALIGN_CENTER_VERTICAL|wx.RB_GROUP)
        rbSizer.Add(self.usePowerRBToggle, 1)
        self.usePowerRBOn = wx.RadioButton(dialog, label = "On", style = wx.ALIGN_CENTER_VERTICAL)
        rbSizer.Add(self.usePowerRBOn, 1)
        self.usePowerRBOff = wx.RadioButton(dialog, label = "Off", style = wx.ALIGN_CENTER_VERTICAL)
        rbSizer.Add(self.usePowerRBOff, 1)
        if server == 'Homecoming':
            self.usePowerRBLocation = wx.RadioButton(dialog, label = 'Location', style = wx.ALIGN_CENTER_VERTICAL)
            rbSizer.Add(self.usePowerRBLocation, 1)

        self.UsePowerSizer.Add(rbSizer, 1, flag = wx.EXPAND)

        if server == 'Homecoming':
            self.LocText = wx.StaticText(dialog, label = "Location:")
            self.UsePowerSizer.Add(self.LocText, flag = wx.ALIGN_CENTER_VERTICAL)

            self.LocSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.LocMe = wx.RadioButton(dialog, label = 'Me', style = wx.ALIGN_CENTER_VERTICAL|wx.RB_GROUP)
            self.LocSizer.Add(self.LocMe, flag = wx.ALIGN_CENTER_VERTICAL)
            self.LocTarget = wx.RadioButton(dialog, label = 'Target', style = wx.ALIGN_CENTER_VERTICAL)
            self.LocSizer.Add(self.LocTarget, flag = wx.ALIGN_CENTER_VERTICAL)
            self.LocDD = wx.RadioButton(dialog, label = 'Dir/Dist', style = wx.ALIGN_CENTER_VERTICAL)
            self.LocSizer.Add(self.LocDD, flag = wx.ALIGN_CENTER_VERTICAL)
            self.Pdir = wx.Choice(dialog, style = wx.ALIGN_CENTER_VERTICAL,
                                 choices = ['0°', '30°', '60°', '90°', '120°', '150°',
                                            '180°', '210°', '240°', '270°', '300°', '330°'])
            self.LocSizer.Add(self.Pdir, flag = wx.ALIGN_CENTER_VERTICAL)
            self.Dist = wx.Choice(dialog, style = wx.ALIGN_CENTER_VERTICAL,
                                  choices = ["10'", "20'", "30'", "40'", "50'", "60'",
                                             "70'", "80'", "90'", "100'", "110'", "120'", 'max'])
            self.LocSizer.Add(self.Dist, flag = wx.ALIGN_CENTER_VERTICAL)
            self.LocCurs = wx.RadioButton(dialog, label = 'Cursor', style = wx.ALIGN_CENTER_VERTICAL)
            self.LocSizer.Add(self.LocCurs, flag = wx.ALIGN_CENTER_VERTICAL)

            self.UsePowerSizer.Add(self.LocSizer, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 10)

        self.UsePowerSizer.Add(wx.StaticText(dialog, label = "Power:"), flag = wx.ALIGN_CENTER_VERTICAL)
        self.usePowerName = PowerPicker(dialog)
        self.UsePowerSizer.Add(self.usePowerName, 1, flag = wx.EXPAND)

        dialog.Bind(wx.EVT_RADIOBUTTON, self.OnRadioButton)

        self.OnRadioButton()

        return self.UsePowerSizer

    def MakeBindString(self) -> str:
        server = self.Profile.Server()
        if self.usePowerRBToggle.GetValue():
            method = "powexecname"
        elif self.usePowerRBOn.GetValue():
            method = "powexectoggleon" if server == "Homecoming" else "px_tgon"
        elif self.usePowerRBOff.GetValue():
            method = "powexectoggleoff" if server == "Homecoming" else "px_tgof"
        elif self.usePowerRBLocation.GetValue():
            if self.LocMe.GetValue():
                method = "powexeclocation me"
            elif self.LocTarget.GetValue():
                method = "powexeclocation target"
            elif self.LocDD.GetValue():
                pdir = re.sub('°', '', self.Pdir.GetStringSelection())
                dist = re.sub("'", '', self.Dist.GetStringSelection())
                method = f"powexeclocation {pdir}:{dist}"
            elif self.LocCurs.GetValue():
                method = "powexeclocation cursor"
            else:
                wx.LogWarning("Invalid location selected for powexec_location in PowerBindCmd")
                return ''
        else:
            wx.LogWarning('PowerBindCmd "UsePowerCmd" got an impossible value for toggle/on/off')
            return ''

        return f"{method} {self.usePowerName.GetLabel()}"

    def Serialize(self) -> dict:
        if   self.usePowerRBOn.GetValue():
            method = "powexectoggleon"
        elif self.usePowerRBOff.GetValue():
            method = "powexectoggleoff"
        elif self.usePowerRBLocation.GetValue():
            method = "powexeclocation"
        else:
            method = "powexecname"

        serialdata = {
            'method': method,
            'pname' : self.usePowerName.GetLabel(),
            'picon' : self.usePowerName.IconFilename
        }
        if self.Profile.Server() == 'Homecoming' and self.usePowerRBLocation.GetValue():
            if self.LocMe.GetValue():
                serialdata['location'] = "me"
            elif self.LocTarget.GetValue():
                serialdata['location'] = "target"
            elif self.LocDD.GetValue():
                pdir = re.sub('°', '', self.Pdir.GetStringSelection())
                dist = re.sub("'", '', self.Dist.GetStringSelection())
                serialdata['location'] = f"{pdir}:{dist}"
            elif self.LocCurs.GetValue():
                serialdata['location'] = "cursor"

        return serialdata

    def Deserialize(self, init) -> None:
        method = init.get('method', '')
        if method == 'powexectoggleon':
            self.usePowerRBOn.SetValue(True)
        elif method == 'powexectoggleoff':
            self.usePowerRBOff.SetValue(True)
        elif method == 'powexeclocation' and self.Profile.Server() == 'Homecoming':
            location = init.get('location', '')
            dd = bool(re.search(':', location))
            self.usePowerRBLocation.SetValue(True)
            self.LocMe.SetValue(location == 'me')
            self.LocTarget.SetValue(location == 'target')
            self.LocDD.SetValue(dd)
            self.LocCurs.SetValue(location == 'cursor')
            if dd:
                pdir, dist = location.split(':')
                self.Pdir.SetStringSelection(f'{pdir}°')
                self.Dist.SetStringSelection(f"{dist}'")
        else:
            self.usePowerRBToggle.SetValue(True)
        if init.get('pname', ''): self.usePowerName.SetLabel(init['pname'])
        if init.get('picon', ''):
            self.usePowerName.SetBitmap(GetIcon(init['picon']))
            self.usePowerName.IconFilename = init['picon']

        self.OnRadioButton()

    def OKToClose(self) -> bool:
        if self.usePowerName.HasPowerPicked():
            return True
        else:
            wx.MessageBox("You must choose a power.", "Power Not Picked")
            return False

    def OnRadioButton(self, evt = None):
        if self.Profile.Server() == 'Homecoming':
            self.UsePowerSizer.Show(self.LocText, show = self.usePowerRBLocation.GetValue())
            self.UsePowerSizer.Show(self.LocSizer, show = self.usePowerRBLocation.GetValue())
            self.Pdir.Enable(self.LocDD.GetValue())
            self.Dist.Enable(self.LocDD.GetValue())
            self.Dialog.Fit()
            self.Dialog.Layout()
        if evt: evt.Skip()
