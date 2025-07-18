from typing import Callable
import wx
# Mixin to handle setting/showing errors and tooltips
class ErrorControlMixin:
    SetBackgroundColour    : Callable
    SetOwnBackgroundColour : Callable
    SetToolTip             : Callable
    GetTextCtrl            : Callable
    HasTextCtrl            : Callable
    Refresh                : Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Errors         : dict = {}
        self.Warnings       : dict = {}
        self.DefaultToolTip : str = ''

    def Enable(self, enable = True):
        if enable == False:
            self.RemoveError('conflict')
        return super().Enable(enable) # pyright: ignore

    def AddWarning(self, errname, tooltip = None):
        if not self.Errors:
            self.StylingTarget().SetBackgroundColour((255,255,200))
        self.Warnings[errname] = tooltip
        self.SetErrorToolTip()
        self.Refresh()

    def RemoveWarning(self, errname):
        self.Warnings.pop(errname, None)
        if not self.Errors and not self.Warnings:
            self.StylingTarget().SetOwnBackgroundColour(wx.NullColour)
        elif not self.Errors:
            self.StylingTarget().SetOwnBackgroundColour((255,255,200))
        self.SetErrorToolTip()
        self.Refresh()

    def AddError(self, errname, tooltip = None):
        self.StylingTarget().SetBackgroundColour((255,200,200))
        self.Errors[errname] = tooltip
        self.SetErrorToolTip()
        self.Refresh()

    def RemoveError(self, errname):
        self.Errors.pop(errname, None)
        if not self.Errors and not self.Warnings:
            self.StylingTarget().SetOwnBackgroundColour(wx.NullColour)
        elif not self.Errors:
            self.StylingTarget().SetOwnBackgroundColour((255,255,200))
        self.SetErrorToolTip()
        self.Refresh()

    # TODO pick one of these next two and stick with it
    def HasAnyError(self): return self.Errors != {}

    def HasErrors(self): return bool(self.Errors)

    def ClearErrors(self):
        # get a list first b/c we change it in the loop
        errors = list(self.Errors)
        for error in errors: self.RemoveError(error)
        self.SetErrorToolTip()
        self.Refresh()

    def StylingTarget(self):
        return self.GetTextCtrl() if (isinstance(self, wx.PickerBase) and self.HasTextCtrl()) else self

    def SetErrorToolTip(self):
        tipstrings = list(self.Errors.values()) + list(self.Warnings.values())
        # if we have any non-empty string, set the tooltip
        for tip in tipstrings:
            if tip:
                self.SetToolTip("\n".join(tipstrings))
                return

        self.SetToolTip(self.DefaultToolTip)
