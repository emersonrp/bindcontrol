# pyright: reportIncompatibleMethodOverride=false
from typing import Any, Callable
import platform

import wx
from wx.adv import BitmapComboBox
import wx.lib.stattext as ST
from wx.lib.expando import ExpandoTextCtrl

from UI.ErrorControls import ErrorControlMixin
from Page import Page as bcPage
import UI
from UI.KeySelectDialog import bcKeyButton

class ControlGroup(wx.StaticBoxSizer):
    def __init__(self, parent, page, label = '', width = 2, flexcols : list|None = None, topcontent = None) -> None:
        flexcols = flexcols or [0]

        super().__init__(wx.VERTICAL, parent, label = label)
        self.vertCenteringSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.Page = page
        self.Ctrls = []

        # usually for an "enable this stuff" checkbox in a wx.Panel
        if topcontent:
            topcontent.Reparent(self.GetStaticBox())
            self.Add(topcontent, 0, wx.ALL|wx.EXPAND, 5)

        self.InnerSizer = wx.FlexGridSizer(width,3,3)
        for col in flexcols: self.InnerSizer.AddGrowableCol(col)

        self.vertCenteringSizer.Add(self.InnerSizer, 1, wx.ALIGN_CENTER_VERTICAL)
        self.Add(self.vertCenteringSizer, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)

    def AddControl(self,
                   ctlType  : str           = '',
                   ctlName  : str           = '',
                   noLabel  : bool          = False,
                   contents : Any           = '',
                   tooltip  : str           = '',
                   callback : Callable|None = None,
                   label    : str           = '',
                   data     : Any           = None,
                   size     : wx.Size       = wx.DefaultSize,
       ):

        if not ctlName:
            wx.LogError("Tried to make a labeled control without a CtlName.  This is a bug.")
            raise(Exception)

        Init      = self.Page.Init
        CtlParent = self.GetStaticBox()
        CtlLabel  = None

        padding = 0

        label = label or UI.Labels.get(ctlName, ctlName)
        if not noLabel:
            # This ST.GenStaticText is so we can intercept clicks on it, but
            # the background color is wrong on Windows in a way I can't work out,
            # and clicks work with wx.StaticText on Windows anyway, so...
            if platform.system() != 'Windows':
                CtlLabel = ST.GenStaticText(CtlParent, -1, label + ':')
            else:
                CtlLabel = wx.StaticText(CtlParent, -1, label + ':')

        if ctlType == ('keybutton'):
            control = cgbcKeyButton( CtlParent, -1,)
            control.SetLabel(Init[ctlName])
            # push context onto the button, we'll thank me later
            control.CtlName = ctlName
            control.Key     = Init[ctlName]

        elif (ctlType == 'combo') or (ctlType == "combobox"):
            control = cgComboBox(
                CtlParent, -1, Init[ctlName], size = size,
                choices = contents or (), style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback)

        elif (ctlType == 'bmcombo') or (ctlType == "bmcombobox"):
            choices = []
            bitmaps = []
            for c in contents:
                choices.append(c[0])
                bitmaps.append(c[1])
            control = cgBMComboBox(
                CtlParent, -1, '',
                style = wx.CB_READONLY,
                choices = choices, size = size,
            )
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback)
            for i, entry in enumerate(bitmaps):
                control.SetItemBitmap(i, entry)
            index = control.FindString(Init[ctlName])
            if index == -1:
                control.SetValue(Init[ctlName])
            else:
                control.SetSelection(index)

        elif ctlType == ('text'):
            control = cgTextCtrl(CtlParent, -1, Init[ctlName], size = size)

        elif ctlType == ('choice'):
            contents = contents if contents else []
            control = cgChoice(CtlParent, -1, choices = contents, size = size)
            control.SetStringSelection(Init[ctlName])
            if callback:
                control.Bind(wx.EVT_CHOICE, callback)

        elif ctlType == ('statictext'):
            control = cgStaticText(CtlParent, -1, Init.get(ctlName, ''), size = size)

        elif ctlType == ('checkbox'):
            control = cgCheckBox(CtlParent, -1, contents, size = size)
            control.SetValue(bool(Init.get(ctlName, False)))
            padding = 6
            if callback:
                control.Bind(wx.EVT_CHECKBOX, callback)

        elif ctlType == ('spinbox'):
            control = cgSpinCtrl(CtlParent, -1, size = size)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('spinboxfractional'):
            control = cgSpinCtrlDouble(CtlParent, inc = 0.05, size = size)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('dirpicker'):
            control = cgDirPickerCtrl(
                CtlParent, -1, Init[ctlName], Init[ctlName], size = size,
            )
        elif ctlType == ('colorpicker'):
            control = cgColourPickerCtrl( CtlParent, -1, contents, size = (30,30))

        else:
            raise Exception(f"Got a ctlType in ControlGroup that I don't know: {ctlType}.  This is a bug.")

        # stash away the page that the control belongs to
        control.Page = self.Page

        # And any user-defined data.  I thought wx had a scheme for this but no?
        control.Data = data

        if not noLabel and CtlLabel:
            self.InnerSizer.Add(CtlLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 6)
            control.CtlLabel = CtlLabel
            setattr(CtlLabel, "control", control)

        # Pack'em in there
        if tooltip and tooltip != '':
            control.DefaultToolTip = tooltip
            control.SetToolTip(tooltip)

        # make checkboxes' labels click to check them
        if ctlType == ('checkbox') and control.CtlLabel:
            control.CtlLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        self.InnerSizer.Add(control, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, padding)
        self.Ctrls.append(control)
        self.Page.Ctrls[ctlName] = control

        self.Layout()
        return control

    def EnableCtrls(self, show) -> None:
        for c in self.Ctrls:
            c.Enable(show)

    # check or uncheck checkboxes when clicking the associated label
    def OnCBLabelClick(self, evt) -> None:
        cblabel = evt.EventObject
        cblabel.control.SetValue(not cblabel.control.IsChecked())
        fakeevt = wx.CommandEvent(wx.wxEVT_CHECKBOX)
        fakeevt.SetEventObject(cblabel.control)
        wx.PostEvent(cblabel.control, fakeevt)
        evt.Skip()

# Mixin to enable/show controls' labels when they are enabled/shown
class CGControlMixin:
    GetContainingSizer     : Callable
    SetBackgroundColour    : Callable
    SetOwnBackgroundColour : Callable

    def __init__(self, *args, **kwargs) -> None:
        self.CtlLabel : ST.GenStaticText | wx.StaticText | None = None
        self.Page     : bcPage|None                             = None
        self.Data     : Any                                     = None
        super().__init__(*args, **kwargs)

    def Enable(self, enable = True) -> bool:
        if self.CtlLabel: self.CtlLabel.Enable(enable)
        return super().Enable(enable) # pyright: ignore

    def Show(self, show = True) -> bool:
        self.GetContainingSizer().Show(self, show = show)
        self.Enable(show)
        if self.CtlLabel:
            self.GetContainingSizer().Show(self.CtlLabel, show = show)
            self.CtlLabel.Enable(show)
        if self.Page: self.Page.Layout()
        return True

    def SetToolTip(self, tooltip) -> bool:
        if self.CtlLabel:
            self.CtlLabel.SetToolTip(tooltip)
        return super().SetToolTip(tooltip) # pyright: ignore

# Miniclasses to use mixins
class cgbcKeyButton     (CGControlMixin,                    bcKeyButton)         :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgButton          (CGControlMixin, ErrorControlMixin, wx.Button)           :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgComboBox        (CGControlMixin, ErrorControlMixin, wx.ComboBox)         :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgBMComboBox      (CGControlMixin, ErrorControlMixin, BitmapComboBox)      :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgTextCtrl        (CGControlMixin, ErrorControlMixin, wx.TextCtrl)         :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgExpandoTextCtrl (CGControlMixin, ErrorControlMixin, ExpandoTextCtrl)         :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgStaticText      (CGControlMixin, ErrorControlMixin, wx.StaticText)       :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgCheckBox        (CGControlMixin, ErrorControlMixin, wx.CheckBox)         :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgSpinCtrl        (CGControlMixin, ErrorControlMixin, wx.SpinCtrl)         :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgSpinCtrlDouble  (CGControlMixin, ErrorControlMixin, wx.SpinCtrlDouble)   :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgDirPickerCtrl   (CGControlMixin, ErrorControlMixin, wx.DirPickerCtrl)    :
    def __init__(self, *args, **kwargs):
        super().__init__(*args, style = wx.DIRP_USE_TEXTCTRL|wx.DIRP_SMALL, **kwargs)
        self.SetTextCtrlProportion(1)
        self.GetTextCtrl().SetEditable(False)
class cgColourPickerCtrl(CGControlMixin, ErrorControlMixin, wx.ColourPickerCtrl) :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgChoice          (CGControlMixin, ErrorControlMixin, wx.Choice)           :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
    def ShowEntryIf(self, entry: str, condition: bool):
        idx    = self.FindString(entry)
        exists = idx != wx.NOT_FOUND
        if condition:
            if not exists: self.Append(entry)
        else:
            if exists: self.Delete(idx)
