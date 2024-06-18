from typing import Callable
import wx
# Mixin to handle setting/showing errors and tooltips
class ErrorControlMixin:
    Errors                 : dict     = {}
    Warnings               : dict     = {}
    DefaultToolTip         : str      = ''
    SetBackgroundColour    : Callable
    SetOwnBackgroundColour : Callable
    SetToolTip             : Callable

    def Enable(self, enable = True):
        super().Enable(enable) # pyright: ignore
        if enable == False:
            self.RemoveError('conflict')

    def AddWarning(self, errname, tooltip = None):
        if not self.Errors:
            self.SetBackgroundColour((255,255,200))
        self.Warnings[errname] = tooltip
        self.SetErrorToolTip()

    def RemoveWarning(self, errname):
        self.Warnings.pop(errname, None)
        if not self.Errors and not self.Warnings:
            self.SetOwnBackgroundColour(wx.NullColour)
        elif not self.Errors:
            self.SetOwnBackgroundColour((255,255,200))
        self.SetErrorToolTip()

    def AddError(self, errname, tooltip = None):
        self.SetBackgroundColour((255,200,200))
        self.Errors[errname] = tooltip
        self.SetErrorToolTip()

    def RemoveError(self, errname):
        self.Errors.pop(errname, None)
        if not self.Errors and not self.Warnings:
            self.SetOwnBackgroundColour(wx.NullColour)
        elif not self.Errors:
            self.SetOwnBackgroundColour((255,255,200))
        self.SetErrorToolTip()

    def SetErrorToolTip(self):
        tipstrings = list(self.Errors.values()) + list(self.Warnings.values())
        # if we have any non-empty string, set the tooltip
        for tip in tipstrings:
            if tip:
                self.SetToolTip("\n".join(tipstrings))
                return

        self.SetToolTip(self.DefaultToolTip)
