import wx
import wx.adv
from UI.PowerBinderCommand import PowerBinderCommand

####### Buff Display Command
class BuffDisplayCmd(PowerBinderCommand):
    Name = "Buff Display Settings"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        self.Ctrls = {}
        self.buffDisplayMap = {
            'Status Window' : {
                'Hide Auto' : 1,
                'Hide Toggles' : 2,
                'No Blinking' : 4,
                'No Stacking' : 8,
                'Numeric Stacking' : 16,
                'Hide Buff Numbers' : 32,
                'Stop Sending Buffs' : 64,
            },
            'Group Window' : {
                'Hide Auto' : 256,
                'Hide Toggles' : 512,
                'No Blinking' : 1024,
                'No Stacking' : 2048,
                'Numeric Stacking' : 4096,
                'Hide Buff Numbers' : 8192,
                'Stop Sending Buffs' : 16384,
            },
            'Pet Window' : {
                'Hide Auto' : 65536,
                'Hide Toggles' : 131072,
                'No Blinking' : 262144,
                'No Stacking' : 524288,
                'Numeric Stacking' : 1048576,
                'Hide Buff Numbers' : 2097152,
                'Stop Sending Buffs' : 4194304,
            },
        }
        masterSizer = wx.BoxSizer(wx.HORIZONTAL)

        for group, controls in self.buffDisplayMap.items():
            groupSizer = wx.StaticBoxSizer(wx.VERTICAL, dialog, group)
            staticBox = groupSizer.GetStaticBox()
            for cb in controls:
                self.Ctrls[f"{group}_{cb}"] = wx.CheckBox(staticBox, label = cb)
                groupSizer.Add(self.Ctrls[f"{group}_{cb}"], 0, wx.ALL, 3)

            masterSizer.Add(groupSizer, 1, wx.EXPAND|wx.ALL, 5)

        return masterSizer

    def CalculateValue(self) -> int:
        total = 0

        for group, controls in self.buffDisplayMap.items():
            for cb in controls:
                checkbox = self.Ctrls[f"{group}_{cb}"]
                if checkbox.IsChecked():
                    total = total + self.buffDisplayMap[group][cb]
        return total

    def MakeBindString(self) -> str:
        return f"optionset buffsettings {self.CalculateValue()}"

    def Serialize(self) -> dict:
        return { 'value' : self.CalculateValue() }

    def Deserialize(self, init) -> None:
        value = init.get('value', 0)

        value = value or 0  # in case we had for some reason 'None' stashed in the init values

        for group, controls in self.buffDisplayMap.items():
            for cb in controls:
                checkbox = self.Ctrls[f"{group}_{cb}"]
                checkbox.SetValue( self.buffDisplayMap[group][cb] & value )
