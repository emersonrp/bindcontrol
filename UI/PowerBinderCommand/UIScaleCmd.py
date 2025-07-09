import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Window Save / Load
class UIScaleCmd(PowerBinderCommand):
    Name = "UI Scale"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog):
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(wx.StaticText(dialog, wx.ID_ANY, "UI Scale"), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.ScaleSC = wx.SpinCtrlDouble(dialog, wx.ID_ANY, style = wx.ALIGN_RIGHT,
                                         min = 0.01, max = 10, initial = 1, inc = .01)
        sizer.Add(self.ScaleSC, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        CenteringSizer.Add(sizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        return CenteringSizer

    def MakeBindString(self):
        return f'uiscale {self.ScaleSC.GetValue()}'

    def Serialize(self):
        return {
            'scale' : self.ScaleSC.GetValue(),
        }

    def Deserialize(self, init):
        self.ScaleSC.SetValue(init.get('scale', 1))
