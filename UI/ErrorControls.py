from typing import Callable
import wx
# Mixin to handle setting/showing errors and tooltips
class ErrorControlMixin:
    GetBackgroundColour    : Callable
    SetBackgroundColour    : Callable
    SetDefaultStyle        : Callable
    SetToolTip             : Callable
    GetTextCtrl            : Callable
    HasTextCtrl            : Callable
    Refresh                : Callable

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Errors         : dict = {}
        self.Warnings       : dict = {}
        self.DefaultToolTip : str = ''
        self.BGColour       : wx.Colour = self.GetBackgroundColour() if isinstance(self, wx.TextCtrl) else wx.NullColour

    def Enable(self, enable = True):
        if enable == False:
            self.RemoveError('conflict')
        return super().Enable(enable) # pyright: ignore

    def AddWarning(self, errname, tooltip = None):
        if not self.Errors:
            self.SetFullBackgroundColour((255,255,200))
        self.Warnings[errname] = tooltip
        self.SetErrorToolTip()
        self.Refresh()

    def RemoveWarning(self, errname):
        self.Warnings.pop(errname, None)
        if not self.Errors and not self.Warnings:
            self.SetFullBackgroundColour(self.BGColour)
        elif not self.Errors:
            self.SetFullBackgroundColour((255,255,200))
        self.SetErrorToolTip()
        self.Refresh()

    def AddError(self, errname, tooltip = None):
        self.SetFullBackgroundColour((255,200,200))
        self.Errors[errname] = tooltip
        self.SetErrorToolTip()
        self.Refresh()

    def RemoveError(self, errname):
        self.Errors.pop(errname, None)
        if not self.Errors and not self.Warnings:
            self.SetFullBackgroundColour(self.BGColour)
        elif not self.Errors:
            self.SetFullBackgroundColour((255,255,200))
        self.SetErrorToolTip()
        self.Refresh()

    def HasErrors(self): return bool(self.Errors)

    def ClearErrors(self):
        # get a list first b/c we change it in the loop
        errors = list(self.Errors)
        for error in errors: self.RemoveError(error)
        self.SetErrorToolTip()
        self.Refresh()

    # Do some dancing in here to make sure multi-line text controls get their contents updated
    def SetFullBackgroundColour(self, colour):
        target = self.StylingTarget()
        target.SetBackgroundColour(colour)
        if isinstance(target, wx.TextCtrl) and target.IsMultiLine():
            target.SelectAll()
            newstyle = wx.TextAttr(wx.NullColour, target.GetBackgroundColour())
            [start, end] = target.GetSelection()
            target.SetStyle(start, end, newstyle)
            target.SelectNone()

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
