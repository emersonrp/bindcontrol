import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### SG Mode
class SGModeCmd(PowerBinderCommand):
    Name = "Supergroup Mode"
    Menu = "Social"
    DeprecatedName = "SG Mode Toggle"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        sgmodeSizer = wx.BoxSizer(wx.HORIZONTAL)
        sgmodeSizer.Add(wx.StaticText(dialog, label = "Supergroup Mode:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)

        self.sgmodeToggleRB = wx.RadioButton(dialog, label =  "Toggle", style = wx.RB_GROUP)
        self.sgmodeOnRB     = wx.RadioButton(dialog, label =  "On")
        self.sgmodeOffRB    = wx.RadioButton(dialog, label =  "Off")

        sgmodeSizer.Add(self.sgmodeToggleRB, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sgmodeSizer.Add(self.sgmodeOnRB, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5)
        sgmodeSizer.Add(self.sgmodeOffRB, 0, wx.ALIGN_CENTER_VERTICAL)

        CenteringSizer.Add(sgmodeSizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        return CenteringSizer

    def MakeBindString(self) -> str:
        if self.sgmodeOnRB.GetValue():
            return 'sgmodeset 1'
        elif self.sgmodeOffRB.GetValue():
            return 'sgmodeset 0'
        else:
            return 'sgmode'

    def Serialize(self) -> dict:
        if self.sgmodeOnRB.GetValue():
            val = "On"
        elif self.sgmodeOffRB.GetValue():
            val = "Off"
        else:
            val = "Toggle"

        return {"value" : val}

    def Deserialize(self, init) -> None:
        val = init.get('value', '')
        if val == "On":
            self.sgmodeOnRB.SetValue(True)
        elif val == "Off":
            self.sgmodeOffRB.SetValue(True)
        else:
            self.sgmodeToggleRB.SetValue(True)
