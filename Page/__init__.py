# base class for all the individual tabs

#  The Page keeps a list of each of the (non-static) controls on itself.
#  It then tries to gatekeep these behind .GetState() and .SetState()
#  in reality, we need to get directly at the controls occasionally
#  to change a wx.Choice's list, for example.  Then we just trawl
#  through page.Ctrls directly.  This could be improved.

#  page.GetState('FPSBindKey')
#  page.SetState('Archetype', 'Blaster')

import wx
import wx.lib.colourselect as csel
from UI.KeySelectDialog import bcKeyButton

class Page(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Profile = parent
        self.TabTitle = type(self).__name__

        self.Ctrls = {}

    def GetState(self, key):
        control = self.Ctrls.get(key, None)
        if not control:
            wx.LogError(f"Unknown control in GetState: {key}")
            return ''
        # We might be tempted to short-circuit out if the control is not enabled
        # but that breaks things terribly during window init.  Might be worth tracking
        # down and fixing but not today.
        if isinstance(control, bcKeyButton):
            return control.Key
        elif isinstance(control, wx.Button):
            return control.GetLabel()
        elif isinstance(control, wx.Choice) or isinstance(control, wx.ComboBox):
            sel = control.GetSelection()
            if sel != -1: return control.GetString(control.GetSelection())
            else        : return ''
        elif isinstance(control, wx.ColourPickerCtrl) or isinstance(control, csel.ColourSelect):
            return control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        elif getattr(control, 'GetValue', None):
            return control.GetValue()
        elif getattr(control, 'GetPath', None):
            return control.GetPath()
        else:
            wx.LogError(f"{control} has no GetValue()")
            return ''

    def SetState(self, key, value):
        control = self.Ctrls.get(key, None)

        if not control:
            wx.LogError(f"Got into SetState for key {key} with no control")
            return

        if isinstance(control, wx.Button):
            return control.SetLabel(value)
        elif isinstance(control, wx.Choice):
            if isinstance(value, str):
                value = control.FindString(value)
                if value == wx.NOT_FOUND: value = 0
            return control.SetSelection(value)
        elif getattr(control, 'SetValue', None):
            return control.SetValue(value)
        elif getattr(control, 'SetPath', None):
            return control.SetPath(value)
        else:
            wx.LogError(f"{control} has no SetValue()")


    # disable controls by name
    def EnableControls(self, enabled, names):
        for name in names:
            self.Ctrls[name].Enable(enabled)

    ##### stubs for overriding (shoes for industry!)
    def SynchronizeUI(self):
        return

    # create and display the UI for this page
    def BuildPage(self):
        return

    # create and fill the BindFile object with Bind objects
    # NB - no state should be kept in the page
    def PopulateBindFiles(self):
        return

    def HelpText(self):
        return 'Help not currently implemented here.'

