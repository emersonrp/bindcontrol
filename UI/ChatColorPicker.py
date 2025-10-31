import wx
import wx.lib.colourselect as csel
import wx.lib.newevent

from UI.CGControls import CGControlMixin, cgStaticText

ChatColorPickerChanged, EVT_CHATCOLORPICKER_CHANGED = wx.lib.newevent.NewCommandEvent()

class ChatColorPicker(wx.BoxSizer):
    def __init__(self, parent, page, prefix, cols) -> None:
        super().__init__(wx.HORIZONTAL)

        self.borderLabel = cgStaticText(parent, label = "Border:")
        self.borderPicker = bcColourSelect(parent, colour = cols['border'], size = wx.Size(30,30))
        self.borderPicker.CtlName = f"{prefix}Border"
        self.borderPicker.CtlLabel = self.borderLabel
        page.Ctrls[f"{prefix}Border"] = self.borderPicker
        self.Add(self.borderLabel,  0, wx.LEFT|wx.ALIGN_CENTER, 5)
        self.Add(self.borderPicker, 0, wx.LEFT|wx.ALIGN_CENTER, 5)

        self.backgroundLabel = cgStaticText(parent, label = "Bkgnd:")
        self.backgroundPicker = bcColourSelect(parent, colour = cols['background'], size = wx.Size(30,30))
        self.backgroundPicker.CtlName = f"{prefix}Background"
        self.backgroundPicker.CtlLabel = self.backgroundLabel
        page.Ctrls[f"{prefix}Background"] = self.backgroundPicker
        self.Add(self.backgroundLabel,  0, wx.LEFT|wx.ALIGN_CENTER, 5)
        self.Add(self.backgroundPicker, 0, wx.LEFT|wx.ALIGN_CENTER, 5)

        self.textLabel = cgStaticText(parent, label = "Text:")
        self.textPicker = bcColourSelect(parent, colour = cols['text'], size = wx.Size(30,30))
        self.textPicker.CtlName = f"{prefix}Foreground"
        self.textPicker.CtlLabel = self.textLabel
        page.Ctrls[f"{prefix}Foreground"] = self.textPicker
        self.Add(self.textLabel,  0, wx.LEFT|wx.ALIGN_CENTER, 5)
        self.Add(self.textPicker, 0, wx.LEFT|wx.ALIGN_CENTER, 5)

        self.example = wx.Panel(parent)
        self.exampleSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.exampleText = cgStaticText(self.example, style = wx.ALIGN_CENTER_HORIZONTAL,)
        self.exampleText.SetLabelMarkup("<big>  Example Text  </big>")
        page.Ctrls[f"{prefix}Example"] = self.example
        self.exampleSizer.Add(self.exampleText, 0, wx.ALL, 3)
        self.example.SetSizerAndFit(self.exampleSizer)
        self.onColorChanged()

        self.borderPicker.Bind(csel.EVT_COLOURSELECT, self.onColorChanged)
        self.backgroundPicker.Bind(csel.EVT_COLOURSELECT, self.onColorChanged)
        self.textPicker.Bind(csel.EVT_COLOURSELECT, self.onColorChanged)

        self.borderPicker.Bind(EVT_CHATCOLORPICKER_CHANGED, self.onColorChanged)
        self.backgroundPicker.Bind(EVT_CHATCOLORPICKER_CHANGED, self.onColorChanged)
        self.textPicker.Bind(EVT_CHATCOLORPICKER_CHANGED, self.onColorChanged)

        self.Add(self.example, 0, wx.LEFT|wx.ALIGN_CENTER, 15)

    def onColorChanged(self, evt = None) -> None:
        if evt: evt.Skip()
        self.example    .SetBackgroundColour(self.borderPicker.GetColour())
        self.exampleText.SetBackgroundColour(self.backgroundPicker.GetColour())
        self.exampleText.SetForegroundColour(self.textPicker.GetColour())
        self.exampleText.Refresh()

def ChatColors(fg,bg,bd) -> str: return f'<color {fg}><bgcolor {bg}><bordercolor {bd}>'

class bcColourSelect(CGControlMixin, csel.ColourSelect): # pyright: ignore
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    # Post an event so the Example Text updates if we set this programmatically
    def SetColour(self, colour):
        super().SetColour(colour)
        wx.PostEvent(self, ChatColorPickerChanged(id = wx.NewIdRef(), control = self))
