import re
import wx
import wx.lib.colourselect as csel
import wx.lib.newevent

import GameData

from UI.CGControls import CGControlMixin, cgStaticText
from Util.Profile import GetCurrentProfile

ChatColorPickerChanged, EVT_CHATCOLORPICKER_CHANGED = wx.lib.newevent.NewCommandEvent()

def ChatColors(fg,bg,bd) -> str: return f'<color {fg}><bgcolor {bg}><bordercolor {bd}>'

# the calling convention to create one of this is WAY too complicated.
class ChatColorPicker(wx.Panel):
    def __init__(self, parent, page, prefix:tuple, initcols:dict):
        super().__init__(parent)

        self.Page = page
        self.PrefixBits = prefix
        self.Prefix = ''.join(prefix)
        self.Colors = initcols

        self.Dialog = None

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Back to main control:
        self.example = ExampleText(self)
        if page: page.Ctrls[f"{self.Prefix}Example"] = self.example

        sizer.Add(self.example, 0, wx.ALIGN_CENTER|wx.RESERVE_SPACE_EVEN_IF_HIDDEN)

        self.SetSizer(sizer)
        self.Fit()
        self.Layout()

    # calling code needs to call this after __init__.  What is the right way to do this?
    def MakeDialog(self):
        if not self.Dialog:
            self.Dialog = ChatColorPickerWindow(self)

    def OnClickExample(self, evt):
        evt.Skip()
        initbrd = self.Colors['border']
        initbkg = self.Colors['background']
        inittxt = self.Colors['foreground']
        self.MakeDialog()
        if self.Dialog and self.Dialog.ShowModal() == wx.ID_OK:
            bdcolor = self.Dialog.borderPicker    .GetColour()
            bgcolor = self.Dialog.backgroundPicker.GetColour()
            txcolor = self.Dialog.textPicker      .GetColour()
            if isinstance(bdcolor, wx.Colour): bdcolor = bdcolor.GetAsString(wx.C2S_HTML_SYNTAX)
            if isinstance(bgcolor, wx.Colour): bgcolor = bgcolor.GetAsString(wx.C2S_HTML_SYNTAX)
            if isinstance(txcolor, wx.Colour): txcolor = txcolor.GetAsString(wx.C2S_HTML_SYNTAX)
            self.Colors = {
                'border'     : bdcolor,
                'background' : bgcolor,
                'foreground'       : txcolor,
            }
            self.example.UpdateExampleBitmap()
            if self.Page:
                wx.PostEvent(self.Page, ChatColorPickerChanged(id = wx.NewIdRef(), control = self))
        else:
            if self.Dialog:
                self.Dialog.borderPicker    .SetColour(initbrd)
                self.Dialog.backgroundPicker.SetColour(initbkg)
                self.Dialog.textPicker      .SetColour(inittxt)
                self.Dialog.UpdateChatBubble()

    def GetValue(self):
        return self.Colors

    def SetValue(self, value):
        self.Colors = value
        self.example.UpdateExampleBitmap()

class ExampleText(wx.GenericStaticBitmap):
    def __init__(self, parent):
        super().__init__(parent)
        self.Picker : ChatColorPicker = parent

        self.Bind(wx.EVT_LEFT_DOWN, parent.OnClickExample)

        self.UpdateExampleBitmap()

    def UpdateExampleBitmap(self, _ = None):
        text = "Chat Colors (click to edit)"
        newChatBubble = ChatBubbleBitmap(text = text, textsize = 10, cols = self.Picker.Colors)

        self.SetBitmap(wx.BitmapBundle(newChatBubble))
        self.SetMinSize(newChatBubble.GetSize())
        self.SetMaxSize(newChatBubble.GetSize())

class bcColourSelect(CGControlMixin, csel.ColourSelect): # pyright: ignore
    def __init__(self, parent, colour = wx.NullColour):
        super().__init__(parent, colour = colour, size = wx.Size(30,30))

class ChatColorPickerWindow(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title = 'Chat Color Selection')
        self.Picker : ChatColorPicker = parent

        dialogSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(dialogSizer)

        self.BubbleBitmap = wx.GenericStaticBitmap(self, size = wx.Size(500, 120))
        self.BubbleBitmap.SetScaleMode(wx.GenericStaticBitmap.Scale_AspectFit)
        dialogSizer.Add(self.BubbleBitmap, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 20)

        ctrlSizer = wx.BoxSizer(wx.HORIZONTAL)

        borderLabel  = cgStaticText(self, label = "Border:")
        self.borderPicker = bcColourSelect(self, colour = parent.Colors['border'])
        self.borderPicker.Bind(csel.EVT_COLOURSELECT, self.OnColorChanged)
        ctrlSizer.Add(     borderLabel , 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)
        ctrlSizer.Add(self.borderPicker, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)

        backgroundLabel  = cgStaticText(self, label = "Background:")
        self.backgroundPicker = bcColourSelect(self, colour = parent.Colors['background'])
        self.backgroundPicker.Bind(csel.EVT_COLOURSELECT, self.OnColorChanged)
        ctrlSizer.Add(     backgroundLabel , 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)
        ctrlSizer.Add(self.backgroundPicker, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)

        textLabel  = cgStaticText(self, label = "Text:")
        self.textPicker = bcColourSelect(self, colour = parent.Colors['foreground'])
        self.textPicker.Bind(csel.EVT_COLOURSELECT, self.OnColorChanged)
        ctrlSizer.Add(     textLabel , 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)
        ctrlSizer.Add(self.textPicker, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 3)

        ctrlSizer.Layout()

        dialogSizer.Add(ctrlSizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10)
        buttonSizer = self.CreateStdDialogButtonSizer(wx.APPLY|wx.OK|wx.CANCEL)
        defaultButton = self.FindWindowById(wx.ID_APPLY, self)
        defaultButton.SetLabel('Defaults')
        defaultButton.Bind(wx.EVT_BUTTON, self.OnDefaultButton)
        dialogSizer.Add(buttonSizer, 0, wx.EXPAND|wx.ALL, 10)

        self.UpdateChatBubble()
        self.Fit()
        self.Layout()

    def OnColorChanged(self, evt = None):
        if evt: evt.Skip()
        self.UpdateChatBubble()
        self.Layout()

        self.Picker.example.UpdateExampleBitmap()

    def UpdateChatBubble(self):

        inspname = re.sub(r'([A-Z])', r' \1', self.Picker.PrefixBits[2])
        text = f"{GetCurrentProfile().ProfileName()}: {inspname}"
        cols = {
            'background' : self.backgroundPicker.GetColour(),
            'border'     : self.borderPicker.GetColour(),
            'foreground' : self.textPicker.GetColour(),
        }

        newChatBubble = ChatBubbleBitmap(text = text, textsize = 18, zigzag = True, cols = cols)

        self.BubbleBitmap.SetBitmap(wx.BitmapBundle(newChatBubble))
        self.BubbleBitmap.SetMinSize(newChatBubble.GetSize())
        self.BubbleBitmap.SetMaxSize(newChatBubble.GetSize())

    def OnDefaultButton(self, evt):
        bgcolor = '#FFFFFF'
        bdcolor = '#000000'
        txcolor = '#000000'

        # we have a bunch of places where we're assuming this is in the context
        # of the inspiration popper but it shouldn't be just for that.
        tab, _, insp = self.Picker.PrefixBits
        if tab and insp:
            InspData = GameData.Inspirations[tab][insp]
            dkcolor = InspData['dkcolor']
            ltcolor = InspData['ltcolor']
            if re.search('Team', tab): dkcolor, ltcolor = ltcolor, dkcolor
            bdcolor = txcolor = dkcolor
            bgcolor           = ltcolor

        self.borderPicker    .SetColour(bdcolor)
        self.backgroundPicker.SetColour(bgcolor)
        self.textPicker      .SetColour(txcolor)
        self.UpdateChatBubble()
        self.Layout()

def ChatBubbleBitmap(text = '', textsize = 14, zigzag = False, cols = None):
    cols = cols or {'border' : '#000000', 'background' : '#FFFFFF', 'foreground' : '#000000'}

    dummyBitmap = wx.Bitmap.FromRGBA(300, 120, 0, 0, 0, 0)

    mdc = wx.MemoryDC()
    mdc.SelectObject(dummyBitmap)

    # make the text poop and get the extent
    font = wx.Font(wx.FontInfo(textsize).FaceName("Montreal-DemiBold"))
    mdc.SetFont(font)
    extent = mdc.GetTextExtent(text)

    # now let's make another bitmap of the right size and stick it into our DC
    mdc.SelectObject(wx.NullBitmap)
    zzheight = 46 if zigzag else 0
    hpadding = 10
    vpadding = 5

    bubbleBitmap = wx.Bitmap.FromRGBA(extent.GetWidth() + (hpadding * 2) + 2, extent.GetHeight() + (vpadding * 2) + 2 + zzheight, 0, 0, 0, 0)
    bubbleBitmap.UseAlpha(True)
    mdc.SelectObject(bubbleBitmap)

    mid = int(bubbleBitmap.GetWidth() / 2)

    bgcolor = cols['background']
    bdcolor = cols['border']
    fgcolor = cols['foreground']

    dc = wx.GCDC(mdc)
    dc.SetFont(font)

    # ok we have our text location.  Set up pen and brush and draw the rectangle
    dc.SetPen(wx.Pen(wx.Colour(bdcolor), width = 3))
    dc.SetBrush(wx.Brush(wx.Colour(bgcolor)))
    dc.DrawRoundedRectangle(1, 1, extent.GetWidth() + (hpadding * 2), extent.GetHeight() + (vpadding * 2), 4)

    # And then draw the text
    dc.SetTextForeground(wx.Colour(fgcolor))
    dc.DrawText(text, hpadding, vpadding)

    if zigzag:
        # OK, now we're going to draw the zigzag below
        bottomEdge = extent.GetHeight() + vpadding
        dc.SetPen(wx.Pen(wx.NullColour, 0, style = wx.PENSTYLE_TRANSPARENT))
        dc.DrawPolygon([(mid - 5,  bottomEdge),      (mid - 10, bottomEdge + 32), (mid,     bottomEdge + 18), (mid + 5, bottomEdge)])
        dc.DrawPolygon([(mid - 10, bottomEdge + 32), (mid,      bottomEdge + 18), (mid + 9, bottomEdge + 12), (mid - 3, bottomEdge + 26)])
        dc.DrawPolygon([(mid + 9,  bottomEdge + 12), (mid - 3,  bottomEdge + 26), (mid - 3, bottomEdge + 46)])

        # and put the lines around it
        dc.SetPen(wx.Pen(wx.BLACK, width = 2))
        dc.DrawLineList([(mid - 5,  bottomEdge + 6 , mid - 10, bottomEdge + 32),
                         (mid - 10, bottomEdge + 32, mid - 3,  bottomEdge + 26),
                         (mid - 3,  bottomEdge + 26, mid - 3,  bottomEdge + 46),
                         (mid - 3,  bottomEdge + 46, mid + 9,  bottomEdge + 12),
                         (mid + 9,  bottomEdge + 12, mid,      bottomEdge + 18),
                         (mid,      bottomEdge + 18, mid + 5,  bottomEdge + 6)
                         ])

    return bubbleBitmap
