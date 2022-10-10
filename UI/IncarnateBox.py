import wx
import wx.lib.buttons as buttons

class IncarnateBox(wx.StaticBoxSizer):
    def __init__(self, parent):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent, 'Incarnate Powers')

        staticbox = self.GetStaticBox()

        incarnateSizer = wx.GridBagSizer(4, 4)

        self.Add(incarnateSizer, 1, wx.EXPAND|wx.ALL, 6)

        self.hybridInc    = IncarnatePicker(staticbox, label = "Hybrid")
        self.loreInc      = IncarnatePicker(staticbox, label = "Lore")
        self.destinyInc   = IncarnatePicker(staticbox, label = "Destiny")
        self.judgementInc = IncarnatePicker(staticbox, label = "Judgement")
        self.interfaceInc = IncarnatePicker(staticbox, label = "Interface")
        self.alphaInc     = IncarnatePicker(staticbox, label = "Alpha")

        incarnateSizer.Add(self.hybridInc,    [0,1], [1,2], wx.EXPAND)
        incarnateSizer.Add(self.loreInc,      [1,0], [1,2], wx.EXPAND|wx.LEFT, 12)
        incarnateSizer.Add(self.destinyInc,   [1,2], [1,2], wx.EXPAND|wx.RIGHT, 12)
        incarnateSizer.Add(self.judgementInc, [2,0], [1,2], wx.EXPAND|wx.LEFT, 12)
        incarnateSizer.Add(self.interfaceInc, [2,2], [1,2], wx.EXPAND|wx.RIGHT, 12)
        incarnateSizer.Add(self.alphaInc,     [3,1], [1,2], wx.EXPAND|wx.BOTTOM, 12)

        incarnateSizer.AddGrowableCol(0)
        incarnateSizer.AddGrowableCol(1)
        incarnateSizer.AddGrowableCol(2)
        incarnateSizer.AddGrowableCol(3)

class IncarnatePicker(wx.StaticBoxSizer):
    def __init__(self, parent, label = ""):
        wx.StaticBoxSizer.__init__(self, wx.HORIZONTAL, parent)
        staticbox = self.GetStaticBox()

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.IncName = wx.StaticText(staticbox, wx.ID_ANY,
                    label + "\n", style = wx.ALIGN_CENTER)
        #self.IncIcon = wx.Button(staticbox,size=[36,36])
        self.IncIcon = buttons.GenButton(staticbox, size=wx.Size(36,36),
                    style = wx.BORDER_NONE)
        self.IncIcon.SetBackgroundColour(bgColors[label])

        hsizer.Add(self.IncName, 1, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(self.IncIcon, 0, wx.ALIGN_CENTER_VERTICAL)

        self.Add(hsizer, 1, wx.EXPAND|wx.RIGHT|wx.BOTTOM, 12)


bgColors = {
    'Alpha'     : [255, 180, 180],
    'Destiny'   : [180, 180, 180],
    'Hybrid'    : [255, 180, 180],
    'Interface' : [180, 180, 255],
    'Judgement' : [180, 255, 180],
    'Lore'      : [255, 180, 255],
}
