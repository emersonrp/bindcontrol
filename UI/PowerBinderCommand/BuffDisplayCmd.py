import wx
from UI.ControlGroup import ControlGroup
import wx.adv
from UI.PowerBinderCommand import PowerBinderCommand

####### Buff Display Command
class BuffDisplayCmd(PowerBinderCommand):
    Name = "Buff Display Settings"
    Menu = "Graphics / UI"
    Groups = {}

    def BuildUI(self, dialog):
        self.Groups = {}
        self.Page = dialog.Page
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
        groupSizer = wx.BoxSizer(wx.HORIZONTAL)

        for group, controls in self.buffDisplayMap.items():
            self.Groups[group] = ControlGroup(dialog, self.Page, label = group)
            groupid = self.Groups[group].GetStaticBox().GetId()
            for cb, data in controls.items():
                self.Groups[group].AddControl(
                    ctlType = 'checkbox',
                    ctlName = f"{groupid}_{group}_{cb}",
                    label = cb,
                    data = data,
                )

            groupSizer.Add(self.Groups[group])

        return groupSizer

    def CalculateValue(self):
        page = wx.App.Get().Main.Profile.CustomBinds

        total = 0

        for group, controls in self.buffDisplayMap.items():
            groupid = self.Groups[group].GetStaticBox().GetId()
            for cb in controls:
                checkbox = page.Ctrls[f"{groupid}_{group}_{cb}"]
                if checkbox.IsChecked():
                    total = total + checkbox.Data
        return total

    def MakeBindString(self):
        return f"optionset buffsettings {self.CalculateValue()}"

    def Serialize(self):
        return { 'value' : self.CalculateValue() }

    def Deserialize(self, init):
        value = init.get('value', 0)

        value = value or 0  # in case we had for some reason 'None' stashed in the init values

        for group, controls in self.buffDisplayMap.items():
            groupid = self.Groups[group].GetStaticBox().GetId()
            for cb in controls:
                checkbox = self.Page.Ctrls[f"{groupid}_{group}_{cb}"]
                checkbox.SetValue( checkbox.Data & value )
