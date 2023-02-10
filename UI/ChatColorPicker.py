import wx

class ChatColorPicker(wx.BoxSizer):

    def __init__(self, parent, prefix, cols):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)

        self.Add(wx.StaticText(parent, label = "Border:"), 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.borderPicker = wx.ColourPickerCtrl(parent, colour = cols['border'], size = (30,30))
        self.Add(self.borderPicker, 0, wx.ALL|wx.ALIGN_CENTER, 5)

        self.Add(wx.StaticText(parent, label = "Background:"), 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.backgroundPicker = wx.ColourPickerCtrl(parent, colour = cols['background'], size = (30,30))
        self.Add(self.backgroundPicker, 0, wx.ALL|wx.ALIGN_CENTER, 5)

        self.Add(wx.StaticText(parent, label = "Text:"), 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.textPicker = wx.ColourPickerCtrl(parent, colour = cols['text'], size = (30,30))
        self.Add(self.textPicker, 0, wx.ALL|wx.ALIGN_CENTER, 5)

        self.example = wx.Panel(parent)
        self.exampleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.exampleText = wx.StaticText(self.example, style = wx.ALIGN_CENTER_HORIZONTAL,)
        self.exampleText.SetLabelMarkup("<big>  Example  </big>")
        self.exampleSizer.Add(self.exampleText, 0, wx.ALL, 3)
        self.example.SetSizerAndFit(self.exampleSizer)
        self.onColorChanged()

        self.borderPicker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.onColorChanged)
        self.backgroundPicker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.onColorChanged)
        self.textPicker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.onColorChanged)

        self.Add(self.example, 0, wx.LEFT|wx.ALIGN_CENTER, 15)

    def onColorChanged(self, _ = None):
        print("Hi got here")
        self.example.SetBackgroundColour(self.borderPicker.GetColour())
        self.exampleText.SetBackgroundColour(self.backgroundPicker.GetColour())
        self.exampleText.SetForegroundColour(self.textPicker.GetColour())

