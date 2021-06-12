import wx
import UI
from UI.KeyBindDialog import KeyPickerEventHandler


class ControlGroup(wx.StaticBoxSizer):

    def __init__(self, parent, page, label = '', width = 2, flexcols = [0]):
        wx.StaticBoxSizer.__init__(self, wx.VERTICAL, parent, label = label)

        self.Page   = page

        self.InnerSizer = wx.FlexGridSizer(0,width,3,3)
        for col in flexcols: self.InnerSizer.AddGrowableCol(col)
        self.Add(self.InnerSizer, 0, wx.ALL|wx.EXPAND, 16)

    def AddLabeledControl(self,
            ctlType = '', ctlName = '', noLabel = False,
            contents = '', tooltip = '', callback = None):

        if not ctlName:
            wx.ErrorLog(f"Tried to make a labeled control without a CtlName!")
            raise(Error)

        sizer     = self.InnerSizer
        Init      = self.Page.Init
        ctlParent = self.GetStaticBox()

        padding = 2

        label = UI.Labels.get(ctlName, ctlName)
        if not noLabel:
            ctlLabel = wx.StaticText(ctlParent, -1, label + ':')

        if ctlType == ('keybutton'):
            control = wx.Button( ctlParent, -1, Init[ctlName])
            control.Bind(wx.EVT_BUTTON, KeyPickerEventHandler)
            control.Bind(wx.EVT_RIGHT_DOWN, self.ClearButton)
            control.CtlName = ctlName

        elif (ctlType == 'combo') or (ctlType == "combobox"):
            control = wx.ComboBox(
                ctlParent, -1, Init[ctlName],
                choices = contents or (), style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback )

        elif ctlType == ('text'):
            control = wx.TextCtrl(ctlParent, -1, Init[ctlName])

        elif ctlType == ('statictext'):
            control = wx.StaticText(ctlParent, -1, contents)

        elif ctlType == ('checkbox'):
            control = wx.CheckBox(ctlParent, -1, contents)
            control.SetValue(bool(Init[ctlName]))
            padding = 10
            if callback:
                control.Bind(wx.EVT_CHECKBOX, callback )

        elif ctlType == ('spinbox'):
            control = wx.SpinCtrl(ctlParent, -1)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('dirpicker'):
            control = wx.DirPickerCtrl(
                ctlParent, -1, Init[ctlName], Init[ctlName],
                style = wx.DIRP_USE_TEXTCTRL|wx.ALL,
            )
        elif ctlType == ('colorpicker'):
            control = wx.ColourPickerCtrl( ctlParent, -1, contents)


        else: wx.LogError(f"Got a ctlType in ControlGroup that I don't know: {ctlType}")

        # Pack'em in there
        if tooltip:
            control.SetToolTip( wx.ToolTip(tooltip))

        if not noLabel:
            sizer.Add( ctlLabel,    0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            self.Page.CtrlLabels[ctlName] = ctlLabel

        sizer.Add( control, 0, wx.ALL|wx.EXPAND, padding)
        self.Page.Controls[ctlName]   = control

        self.Layout()

    def ClearButton(self, evt):
        evt.EventObject.SetLabel("UNBOUND")

