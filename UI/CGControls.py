# pyright: reportIncompatibleMethodOverride=false
import platform
from typing import Any, TYPE_CHECKING
from collections.abc import Callable

import wx
from wx.adv import BitmapComboBox
from wx.lib.expando import ExpandoTextCtrl
from wx.lib.stattext import GenStaticText

if TYPE_CHECKING: from Page import Page as bcPage

from UI.ErrorControls import ErrorControlMixin
from UI.KeySelectDialog import bcKeyButton

# Mixin to enable/show controls' labels when they are enabled/shown
class CGControlMixin:
    GetContainingSizer     : Callable
    SetBackgroundColour    : Callable
    SetOwnBackgroundColour : Callable

    def __init__(self, *args, **kwargs) -> None:
        self.CtlLabel : cgStaticText | None = None
        self.Page     : bcPage|None         = None
        self.Data     : Any                 = None
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
class cgExpandoTextCtrl (CGControlMixin, ErrorControlMixin, ExpandoTextCtrl)     :
    def __init__(self, *args, **kwargs) -> None: super().__init__(*args, **kwargs)
class cgStaticText      (CGControlMixin, ErrorControlMixin, wx.StaticText if platform.system() == 'Windows' else GenStaticText): # pyright: ignore
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
