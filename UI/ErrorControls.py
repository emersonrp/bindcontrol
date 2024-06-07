from typing import Callable
import wx
# Mixin to handle setting/showing errors and tooltips
class ErrorControlMixin:
    Errors                 : dict
    SetBackgroundColour    : Callable
    SetOwnBackgroundColour : Callable
    SetToolTip             : Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Errors = {}

    def AddError(self, errname, tooltip = None):
        self.SetBackgroundColour((255,200,200))
        self.Errors[errname] = tooltip
        self.SetErrorToolTip()

    def RemoveError(self, errname):
        self.Errors.pop(errname, None)
        if not self.Errors:
            self.SetOwnBackgroundColour(wx.NullColour)
        self.SetErrorToolTip()

    def SetErrorToolTip(self):
        tipstrings = self.Errors.values()
        # if we have any non-empty string, set the tooltip
        for tip in tipstrings:
            if tip:
                self.SetToolTip("\n".join(tipstrings))
                return
        self.SetToolTip('')
