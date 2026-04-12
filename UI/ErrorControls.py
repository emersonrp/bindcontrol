from collections.abc import Callable
import wx
from wx.lib.buttons import GenButton
import bcColours

# Mixin to handle setting/showing errors and tooltips
class ErrorControlMixin:
    GetBackgroundColour    : Callable
    SetBackgroundColour    : Callable
    SetDefaultStyle        : Callable
    SetToolTip             : Callable
    GetTextCtrl            : Callable
    HasTextCtrl            : Callable
    Refresh                : Callable
    IsEnabled              : Callable
    Bind                   : Callable

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.Errors         : dict           = {}
        self.Warnings       : dict           = {}
        self.DefaultToolTip : str            = ''
        self.DisabledColor  : wx.Colour|None = None
        self.BGColour       : wx.Colour|None = None

        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnSystemColoursChanged)
        self.OnSystemColoursChanged()

    def Enable(self, enable = True) -> bool:
        if not enable:
            self.RemoveError('conflict')
            self.SetBackgroundColour(self.DisabledColor)
        else:
            self.SetBackgroundColour(self.BGColour)
        return super().Enable(enable) # pyright: ignore

    def AddWarning(self, errname, tooltip = None) -> None:
        if not self.Errors:
            self.SetFullBackgroundColour(bcColours.WarningColour())
        self.Warnings[errname] = tooltip
        self.SetErrorToolTip()
        self.Refresh()

    def RemoveWarning(self, errname) -> None:
        self.Warnings.pop(errname, None)
        if not self.Errors and not self.Warnings:
            self.SetFullBackgroundColour(self.BGColour if self.IsEnabled() else self.DisabledColor)
        elif not self.Errors:
            self.SetFullBackgroundColour(bcColours.WarningColour())
        self.SetErrorToolTip()
        self.Refresh()

    def AddError(self, errname, tooltip = None) -> None:
        self.SetFullBackgroundColour(bcColours.ErrorColour())
        self.Errors[errname] = tooltip
        self.SetErrorToolTip()
        self.Refresh()

    def RemoveError(self, errname) -> None:
        self.Errors.pop(errname, None)
        if not self.Errors and not self.Warnings:
            self.SetFullBackgroundColour(self.BGColour if self.IsEnabled() else self.DisabledColor)
        elif not self.Errors:
            self.SetFullBackgroundColour(bcColours.WarningColour())
        self.SetErrorToolTip()
        self.Refresh()

    def HasErrors(self) -> bool: return bool(self.Errors)

    def HasWarnings(self) -> bool: return bool(self.Warnings)

    def ClearErrors(self) -> None:
        # make a list copy of self.Errors first b/c we change self.Errors in the loop
        errors = list(self.Errors)
        for error in errors: self.RemoveError(error)
        self.SetErrorToolTip()
        self.Refresh()

    # Do some dancing in here to make sure multi-line text controls get their contents updated
    def SetFullBackgroundColour(self, colour) -> None:
        target = self.StylingTarget()
        target.SetBackgroundColour(colour)
        if isinstance(target, wx.TextCtrl) and target.IsMultiLine():
            target.SelectAll()
            newstyle = wx.TextAttr(wx.NullColour, target.GetBackgroundColour())
            [start, end] = target.GetSelection()
            target.SetStyle(start, end, newstyle)
            target.SelectNone()

    def OnSystemColoursChanged(self, evt = None):
        if evt: evt.Skip()
        if isinstance(self, wx.TextCtrl):
            self.BGColour = self.GetBackgroundColour()
        else:
            if isinstance(self, GenButton):
                self.BGColour      = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT)
                self.DisabledColor = wx.NullColour
            else:
                self.BGColour = wx.NullColour

        if self.HasErrors():
            self.SetFullBackgroundColour(bcColours.ErrorColour())
        elif self.HasWarnings():
            self.SetFullBackgroundColour(bcColours.WarningColour())
        elif not self.IsEnabled():
            self.SetFullBackgroundColour(self.DisabledColor)
        else:
            self.SetFullBackgroundColour(self.BGColour)

    def StylingTarget(self):
        return self.GetTextCtrl() if (isinstance(self, wx.PickerBase) and self.HasTextCtrl()) else self

    def SetErrorToolTip(self) -> None:
        tipstrings = list(self.Errors.values()) + list(self.Warnings.values())
        # if we have any non-empty string, set the tooltip
        for tip in tipstrings:
            if tip:
                self.SetToolTip("\n".join(tipstrings))
                return

        self.SetToolTip(self.DefaultToolTip)
