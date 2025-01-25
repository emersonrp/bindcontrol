import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Window Color
class WindowColorCmd(PowerBinderCommand):
    Name = "Window Color"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog):
        windowColorSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ColorBorder  = wx.Panel(dialog, -1, size = (150, 150))
        borderSizer = wx.BoxSizer(wx.VERTICAL)
        self.ColorBorder.SetSizer(borderSizer)
        self.ColorDisplay = wx.StaticText(self.ColorBorder, -1, size = (140, 140))
        borderSizer.Add(self.ColorDisplay, 0, wx.ALL, 5)

        windowColorSizer.Add(self.ColorBorder, 0, wx.ALIGN_CENTER|wx.RIGHT, 15)

        RGBASizer = wx.FlexGridSizer(3, 4, 5)

        RGBASizer.Add(wx.StaticText(dialog, label = "R:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.RSlider = wx.Slider(dialog, -1, size = (300, -1), value = 36, minValue = 0, maxValue = 255)
        self.RSlider.Bind(wx.EVT_SCROLL, self.UpdateFromSlider)
        RGBASizer.Add(self.RSlider, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.RReadout = wx.SpinCtrl(dialog, -1, initial = 128, min = 0, max = 255)
        self.RReadout.Bind(wx.EVT_TEXT, self.UpdateFromText)
        RGBASizer.Add(self.RReadout, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)

        RGBASizer.Add(wx.StaticText(dialog, label = "G:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.GSlider = wx.Slider(dialog, -1, size = (300, -1), value = 145, minValue = 0, maxValue = 255)
        self.GSlider.Bind(wx.EVT_SCROLL, self.UpdateFromSlider)
        RGBASizer.Add(self.GSlider, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.GReadout = wx.SpinCtrl(dialog, -1, initial = 128, min = 0, max = 255)
        self.GReadout.Bind(wx.EVT_TEXT, self.UpdateFromText)
        RGBASizer.Add(self.GReadout, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)

        RGBASizer.Add(wx.StaticText(dialog, label = "B:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.BSlider = wx.Slider(dialog, -1, size = (300, -1), value = 255, minValue = 0, maxValue = 255)
        self.BSlider.Bind(wx.EVT_SCROLL, self.UpdateFromSlider)
        RGBASizer.Add(self.BSlider, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.BReadout = wx.SpinCtrl(dialog, -1, initial = 128, min = 0, max = 255)
        self.BReadout.Bind(wx.EVT_TEXT, self.UpdateFromText)
        RGBASizer.Add(self.BReadout, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)

        RGBASizer.Add(wx.StaticText(dialog, label = "A:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.ASlider = wx.Slider(dialog, -1, size = (300, -1), value = 255, minValue = 0, maxValue = 255)
        self.ASlider.Bind(wx.EVT_SCROLL, self.UpdateFromSlider)
        RGBASizer.Add(self.ASlider, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.AReadout = wx.SpinCtrl(dialog, -1, initial = 128, min = 0, max = 255)
        self.AReadout.Bind(wx.EVT_TEXT, self.UpdateFromText)
        RGBASizer.Add(self.AReadout, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)

        windowColorSizer.Add(RGBASizer)

        self.UpdateFromSlider()

        return windowColorSizer

    def MakeBindString(self):
        Rval = self.RSlider.GetValue()
        Gval = self.GSlider.GetValue()
        Bval = self.BSlider.GetValue()
        Aval = self.ASlider.GetValue()
        return f"windowcolor {Rval} {Gval} {Bval} {Aval}"

    def Serialize(self):
        return {
            'Rval' : self.RSlider.GetValue(),
            'Gval' : self.GSlider.GetValue(),
            'Bval' : self.BSlider.GetValue(),
            'Aval' : self.ASlider.GetValue(),
        }

    def Deserialize(self, init):
        self.RSlider.SetValue(init['Rval'])
        self.GSlider.SetValue(init['Gval'])
        self.BSlider.SetValue(init['Bval'])
        self.ASlider.SetValue(init['Aval'])
        self.UpdateFromSlider()

    def UpdateFromSlider(self, _ = None):
        Rval = self.RSlider.GetValue()
        Gval = self.GSlider.GetValue()
        Bval = self.BSlider.GetValue()
        Aval = self.ASlider.GetValue()
        self.ColorBorder.SetBackgroundColour((Rval, Gval, Bval))
        self.ColorDisplay.SetBackgroundColour((Aval, Aval, Aval))
        self.RReadout.SetValue(Rval)
        self.GReadout.SetValue(Gval)
        self.BReadout.SetValue(Bval)
        self.AReadout.SetValue(Aval)
        self.ColorBorder.Refresh()

    def UpdateFromText(self, _ = None):
        Rval = self.RReadout.GetValue()
        Gval = self.GReadout.GetValue()
        Bval = self.BReadout.GetValue()
        Aval = self.AReadout.GetValue()
        self.ColorBorder.SetBackgroundColour((Rval, Gval, Bval))
        self.ColorDisplay.SetBackgroundColour((Aval, Aval, Aval))
        self.RSlider.SetValue(Rval)
        self.GSlider.SetValue(Gval)
        self.BSlider.SetValue(Bval)
        self.ASlider.SetValue(Aval)
        self.ColorBorder.Refresh()
