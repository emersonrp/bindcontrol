from typing import Any, TYPE_CHECKING
from collections.abc import Callable

if TYPE_CHECKING:
    from Page import Page as bcPage
    import wx
    import wx.lib.stattext as ST

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

    def MakeBind(self, *args):
        raise(Exception('"MakeBind" called on something that isn\'t a KeyButton!  This is a bug.'))

    def ShowEntryIf(self, *args):
        raise(Exception('"MakeBind" called on something that isn\'t a cgChoice!  This is a bug.'))
