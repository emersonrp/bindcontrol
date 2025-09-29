import wx
import wx.lib.colourselect as csel

class ChatColorPicker(wx.BoxSizer):
    def __init__(self, parent, page, prefix, cols) -> None:
        super().__init__(wx.HORIZONTAL)

        self.borderLabel = wx.StaticText(parent, label = "Border:")
        self.borderPicker = csel.ColourSelect(parent, colour = cols['border'], size = wx.Size(30,30))
        setattr(self.borderPicker, "CtlName", f"{prefix}Border")
        setattr(self.borderPicker, "CtlLabel", self.borderLabel)
        page.Ctrls[f"{prefix}Border"] = self.borderPicker
        self.Add(self.borderLabel,  0, wx.LEFT|wx.ALIGN_CENTER, 5)
        self.Add(self.borderPicker, 0, wx.LEFT|wx.ALIGN_CENTER, 5)

        self.backgroundLabel = wx.StaticText(parent, label = "Bkgnd:")
        self.backgroundPicker = csel.ColourSelect(parent, colour = cols['background'], size = wx.Size(30,30))
        setattr(self.backgroundPicker, "CtlName", f"{prefix}Background")
        setattr(self.backgroundPicker, "CtlLabel", self.backgroundLabel)
        page.Ctrls[f"{prefix}Background"] = self.backgroundPicker
        self.Add(self.backgroundLabel,  0, wx.LEFT|wx.ALIGN_CENTER, 5)
        self.Add(self.backgroundPicker, 0, wx.LEFT|wx.ALIGN_CENTER, 5)

        self.textLabel = wx.StaticText(parent, label = "Text:")
        self.textPicker = csel.ColourSelect(parent, colour = cols['text'], size = wx.Size(30,30))
        setattr(self.textPicker, "CtlName", f"{prefix}Foreground")
        setattr(self.textPicker, "CtlLabel", self.textLabel)
        page.Ctrls[f"{prefix}Foreground"] = self.textPicker
        self.Add(self.textLabel,  0, wx.LEFT|wx.ALIGN_CENTER, 5)
        self.Add(self.textPicker, 0, wx.LEFT|wx.ALIGN_CENTER, 5)

        self.example = wx.Panel(parent)
        self.exampleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.exampleText = wx.StaticText(self.example, style = wx.ALIGN_CENTER_HORIZONTAL,)
        self.exampleText.SetLabelMarkup("<big>  Example Text  </big>")
        self.exampleSizer.Add(self.exampleText, 0, wx.ALL, 3)
        self.example.SetSizerAndFit(self.exampleSizer)
        self.onColorChanged()

        self.borderPicker.Bind(csel.EVT_COLOURSELECT, self.onColorChanged)
        self.backgroundPicker.Bind(csel.EVT_COLOURSELECT, self.onColorChanged)
        self.textPicker.Bind(csel.EVT_COLOURSELECT, self.onColorChanged)

        self.Add(self.example, 0, wx.LEFT|wx.ALIGN_CENTER, 15)

    def onColorChanged(self, _ = None) -> None:
        self.example.SetBackgroundColour(self.borderPicker.GetColour())
        self.exampleText.SetBackgroundColour(self.backgroundPicker.GetColour())
        self.exampleText.SetForegroundColour(self.textPicker.GetColour())
        self.exampleText.Refresh()

def ChatColors(fg,bg,bd) -> str: return f'<color {fg}><bgcolor {bg}><bordercolor {bd}>'
