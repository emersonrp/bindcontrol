import wx
from wx.adv import BitmapComboBox
from Page import Page
import UI
from KeyBind import ControlKeyBind
from UI.KeySelectDialog import KeySelectEventHandler


class ControlGroup(wx.StaticBoxSizer):

    def __init__(self, parent, page, label = '', width = 2, flexcols = [0]):
        wx.StaticBoxSizer.__init__(self, wx.VERTICAL, parent, label = label)

        self.Profile = page.Profile
        self.Page    = page

        self.InnerSizer = wx.FlexGridSizer(width,3,3)
        for col in flexcols: self.InnerSizer.AddGrowableCol(col)
        self.Add(self.InnerSizer, 1, wx.ALL|wx.EXPAND, 10)

    def AddControl(self,
        ctlType = '', ctlName = '', noLabel = False,
        contents : str|list = '', tooltip = '', callback = None):

        if not ctlName:
            wx.LogError(f"Tried to make a labeled control without a CtlName!")
            raise(Exception)

        sizer     = self.InnerSizer
        Init      = self.Page.Init
        ctlParent = self.GetStaticBox()

        padding = 0

        label = UI.Labels.get(ctlName, ctlName)
        if not noLabel:
            CtlLabel = wx.StaticText(ctlParent, -1, label + ':')

        if ctlType == ('keybutton'):
            control = bcKeyButton( ctlParent, -1, '' )
            control.SetLabel(Init[ctlName])
            # push context onto the button, we'll thank me later
            control.CtlName = ctlName
            control.Page    = self.Page
            control.Profile = self.Profile
            control.KeyBind = ControlKeyBind(Init[ctlName], label, self.Page.TabTitle)

        elif (ctlType == 'combo') or (ctlType == "combobox"):
            control = wx.ComboBox(
                ctlParent, -1, Init[ctlName],
                choices = contents or (), style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback )

        elif (ctlType == 'bmcombo') or (ctlType == "bmcombobox"):
            control = BitmapComboBox(
                ctlParent, -1, '',
                style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback )
            for entry in contents:
                control.Append(*entry)
            index = control.FindString(Init[ctlName])
            if index == -1:
                control.SetValue(Init[ctlName])
            else:
                control.SetSelection(index)

        elif ctlType == ('text'):
            control = wx.TextCtrl(ctlParent, -1, Init[ctlName])

        elif ctlType == ('choice'):
            contents = contents if contents else []
            control = wx.Choice(ctlParent, -1, choices = contents)
            control.SetSelection(control.FindString(Init[ctlName]))
            if callback:
                control.Bind(wx.EVT_CHOICE, callback )

        elif ctlType == ('statictext'):
            control = wx.StaticText(ctlParent, -1, contents)

        elif ctlType == ('checkbox'):
            control = wx.CheckBox(ctlParent, -1, contents)
            control.SetValue(bool(Init[ctlName]))
            padding = 6
            if callback:
                control.Bind(wx.EVT_CHECKBOX, callback )

        elif ctlType == ('spinbox'):
            control = wx.SpinCtrl(ctlParent, -1)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('dirpicker'):
            control = wx.DirPickerCtrl(
                ctlParent, -1, Init[ctlName], Init[ctlName],
                #style = wx.DIRP_USE_TEXTCTRL|wx.DIRP_SMALL,
            )
        elif ctlType == ('colorpicker'):
            control = wx.ColourPickerCtrl( ctlParent, -1, contents)

        else:
            wx.LogError(f"Got a ctlType in ControlGroup that I don't know: {ctlType}")
            return

        # Pack'em in there
        if tooltip:
            control.SetToolTip( wx.ToolTip(tooltip))

        control.CtlLabel = None
        if not noLabel:
            sizer.Add( CtlLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            control.CtlLabel = CtlLabel
            CtlLabel.control = control

        # make checkboxes' labels click to check them
        # TODO - doesn't work on Linux hmm
        if ctlType == ('checkbox') and control.CtlLabel:
            control.CtlLabel.Bind(wx.EVT_LEFT_DOWN, self.onCBLabelClick)

        sizer.Add( control, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, padding)
        self.Page.Ctrls[ctlName] = control

        self.Layout()
        return control

    def onCBLabelClick(self, evt):
        cblabel = evt.EventObject
        cblabel.control.SetValue(not cblabel.control.IsChecked())
        evt.Skip()

class bcKeyButton(wx.Button):
    def __init__(self, parent, id, init):
        wx.Button.__init__(self, parent, id, init)
        self.CtlName: str
        self.CtlLabel: wx.StaticText
        self.Page: Page
        self.Profile: Profile
        self.KeyBind: ControlKeyBind

        self.Bind(wx.EVT_BUTTON, KeySelectEventHandler)
        self.Bind(wx.EVT_RIGHT_DOWN, self.ClearButton)

    def ClearButton(self, _): self.SetLabel("")

    def MakeFileKeyBind(self, contents):
        return self.KeyBind.MakeFileKeyBind(contents)
