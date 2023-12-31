from typing import Any, Callable

import wx
from wx.adv import BitmapComboBox
import wx.lib.stattext as ST

import UI
from UI.KeySelectDialog import bcKeyButton

class ControlGroup(wx.StaticBoxSizer):

    def __init__(self, parent, page, label = '', width = 2, flexcols = [0]):
        wx.StaticBoxSizer.__init__(self, wx.VERTICAL, parent, label = label)

        self.Page    = page

        self.InnerSizer = wx.FlexGridSizer(width,3,3)
        for col in flexcols: self.InnerSizer.AddGrowableCol(col)
        self.Add(self.InnerSizer, 1, wx.ALL|wx.EXPAND, 10)

    def AddControl(self,
                   ctlType  : str = '',
                   ctlName  : str = '',
                   noLabel  : bool = False,
                   contents : Any = '',
                   tooltip  : str = '',
                   callback : Callable|None = None
        ):

        if not ctlName:
            wx.LogError(f"Tried to make a labeled control without a CtlName!")
            raise(Exception)

        Init      = self.Page.Init
        CtlParent = self.GetStaticBox()
        CtlLabel  = None

        padding = 0

        label = UI.Labels.get(ctlName, ctlName)
        if not noLabel:
            # This ST.GenStaticText is so we can intercept clicks on it, but
            # the background color is wrong on Windows in a way I can't work out,
            # and clicks work on Windows anyway, so...
            if wx.Platform != '__WXMSW__':
                CtlLabel = ST.GenStaticText(CtlParent, -1, label + ':')
            else:
                CtlLabel = wx.StaticText(CtlParent, -1, label + ':')

        if ctlType == ('keybutton'):
            control = cgbcKeyButton( CtlParent, -1, )
            control.SetLabel(Init[ctlName])
            # push context onto the button, we'll thank me later
            control.CtlName = ctlName
            control.Page    = self.Page
            control.Key     = Init[ctlName]

        elif (ctlType == 'combo') or (ctlType == "combobox"):
            control = cgComboBox(
                CtlParent, -1, Init[ctlName],
                choices = contents or (), style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback )

        elif (ctlType == 'bmcombo') or (ctlType == "bmcombobox"):
            control = cgBMComboBox(
                CtlParent, -1, '',
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
            control = cgTextCtrl(CtlParent, -1, Init[ctlName])

        elif ctlType == ('choice'):
            contents = contents if contents else []
            control = cgChoice(CtlParent, -1, choices = contents)
            control.SetSelection(control.FindString(Init[ctlName]))
            if callback:
                control.Bind(wx.EVT_CHOICE, callback )

        elif ctlType == ('statictext'):
            control = cgStaticText(CtlParent, -1, contents)

        elif ctlType == ('checkbox'):
            control = cgCheckBox(CtlParent, -1, contents)
            control.SetValue(bool(Init[ctlName]))
            padding = 6
            if callback:
                control.Bind(wx.EVT_CHECKBOX, callback )

        elif ctlType == ('spinbox'):
            control = cgSpinCtrl(CtlParent, -1)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('spinboxfractional'):
            control = cgSpinCtrlDouble(CtlParent, inc = 0.05)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('dirpicker'):
            control = cgDirPickerCtrl(
                CtlParent, -1, Init[ctlName], Init[ctlName],
            )
        elif ctlType == ('colorpicker'):
            control = cgColourPickerCtrl( CtlParent, -1, contents, size = (30,30))

        else:
            wx.LogError(f"Got a ctlType in ControlGroup that I don't know: {ctlType}")
            raise Exception

        # Pack'em in there
        if tooltip: control.SetToolTip( wx.ToolTip(tooltip) )

        if not noLabel and CtlLabel:
            CtlLabel.SetToolTip( wx.ToolTip(tooltip))
            self.InnerSizer.Add( CtlLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 6)
            control.CtlLabel = CtlLabel
            setattr(CtlLabel, "control", control)

        # make checkboxes' labels click to check them
        if ctlType == ('checkbox') and control.CtlLabel:
            control.CtlLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        self.InnerSizer.Add( control, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, padding)
        self.Page.Ctrls[ctlName] = control

        self.Layout()
        return control

    # check or uncheck checkboxes when clicking the associated label
    def OnCBLabelClick(self, evt):
        cblabel = evt.EventObject
        cblabel.control.SetValue(not cblabel.control.IsChecked())
        fakeevt = wx.CommandEvent(wx.EVT_CHECKBOX.typeId, cblabel.control.GetId())
        wx.PostEvent(cblabel.control, fakeevt)
        evt.Skip()

class HasLabelMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CtlLabel : ST.GenStaticText | wx.StaticText | None = None

    def Enable(self, doEnable):
        super().Enable(doEnable)
        if self.CtlLabel: self.CtlLabel.Enable(doEnable)

class cgbcKeyButton     (HasLabelMixin, bcKeyButton)         : pass
class cgComboBox        (HasLabelMixin, wx.ComboBox)         : pass
class cgBMComboBox      (HasLabelMixin, BitmapComboBox)      : pass
class cgTextCtrl        (HasLabelMixin, wx.TextCtrl)         : pass
class cgChoice          (HasLabelMixin, wx.Choice)           : pass
class cgStaticText      (HasLabelMixin, wx.StaticText)       : pass
class cgCheckBox        (HasLabelMixin, wx.CheckBox)         : pass
class cgSpinCtrl        (HasLabelMixin, wx.SpinCtrl)         : pass
class cgSpinCtrlDouble  (HasLabelMixin, wx.SpinCtrlDouble)   : pass
class cgDirPickerCtrl   (HasLabelMixin, wx.DirPickerCtrl)    : pass
class cgColourPickerCtrl(HasLabelMixin, wx.ColourPickerCtrl) : pass

