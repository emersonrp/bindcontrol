import wx
import UI
from KeyBind import KeyBind
from UI.KeySelectDialog import KeySelectEventHandler


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
            ctlLabel = bc_wxStaticText(ctlParent, -1, label + ':')

        if ctlType == ('keybutton'):
            control = bc_wxKeyButton( ctlParent, -1, Init[ctlName])
            control.Bind(wx.EVT_BUTTON, KeySelectEventHandler)
            control.Bind(wx.EVT_RIGHT_DOWN, self.ClearButton)
            control.CtlName = ctlName

        elif (ctlType == 'combo') or (ctlType == "combobox"):
            control = bc_wxComboBox(
                ctlParent, -1, Init[ctlName],
                choices = contents or (), style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback )

        elif ctlType == ('text'):
            control = bc_wxTextCtrl(ctlParent, -1, Init[ctlName])

        elif ctlType == ('choice'):
            contents = contents if contents else []
            control = bc_wxChoice(ctlParent, -1, choices = contents)
            if callback:
                control.Bind(wx.EVT_CHOICE, callback )

        elif ctlType == ('statictext'):
            control = bc_wxStaticText(ctlParent, -1, contents)

        elif ctlType == ('checkbox'):
            control = bc_wxCheckBox(ctlParent, -1, contents)
            control.SetValue(bool(Init[ctlName]))
            padding = 10
            if callback:
                control.Bind(wx.EVT_CHECKBOX, callback )

        elif ctlType == ('spinbox'):
            control = bc_wxSpinCtrl(ctlParent, -1)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('dirpicker'):
            control = bc_wxDirPickerCtrl(
                ctlParent, -1, Init[ctlName], Init[ctlName],
                #style = wx.DIRP_USE_TEXTCTRL|wx.DIRP_SMALL,
            )
        elif ctlType == ('colorpicker'):
            control = bc_wxColourPickerCtrl( ctlParent, -1, contents)

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


### wee custom classes wrapping each control type and extending them
### with our KeyBind mixin.

class bc_wxKeyButton(wx.Button, KeyBind):
    def __init__(self, *args, **kwargs):
        wx.Button.__init__(self, *args, **kwargs)

class bc_wxComboBox(wx.ComboBox, KeyBind):
    def __init__(self, *args, **kvargs):
        wx.ComboBox.__init__(self, *args, **kvargs)

class bc_wxTextCtrl(wx.TextCtrl, KeyBind):
    def __init__(self, *args, **kvargs):
        wx.TextCtrl.__init__(self, *args, **kvargs)

class bc_wxChoice(wx.Choice, KeyBind):
    def __init__(self, *args, **kvargs):
        wx.Choice.__init__(self, *args, **kvargs)

class bc_wxStaticText(wx.StaticText, KeyBind):
    def __init__(self, *args, **kvargs):
        wx.StaticText.__init__(self, *args, **kvargs)

class bc_wxCheckBox(wx.CheckBox, KeyBind):
    def __init__(self, *args, **kvargs):
        wx.CheckBox.__init__(self, *args, **kvargs)

class bc_wxSpinCtrl(wx.SpinCtrl, KeyBind):
    def __init__(self, *args, **kvargs):
        wx.SpinCtrl.__init__(self, *args, **kvargs)

class bc_wxDirPickerCtrl(wx.DirPickerCtrl, KeyBind):
    def __init__(self, *args, **kvargs):
        wx.DirPickerCtrl.__init__(self, *args, **kvargs)

class bc_wxColourPickerCtrl(wx.ColourPickerCtrl, KeyBind):
    def __init__(self, *args, **kvargs):
        wx.ColourPickerCtrl.__init__(self, *args, **kvargs)
