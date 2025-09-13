# base class for all the individual tabs

#  The Page keeps a list of each of the (non-static) controls on itself.
#  It then tries to gatekeep these behind .GetState() and .SetState()
#  in reality, we need to get directly at the controls occasionally
#  to change a wx.Choice's list, for example.  Then we just trawl
#  through page.Ctrls directly.  This could be improved.

#  page.GetState('FPSBindKey')
#  page.SetState('Archetype', 'Blaster')

import json
import wx
import wx.lib.colourselect as csel
from UI.KeySelectDialog import bcKeyButton
from UI.PowerPicker import PowerPicker


class Page(wx.ScrolledWindow):

    def __init__(self, parent, bind_events : bool = True):
        super().__init__(parent)

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(self.MainSizer, 1, flag = wx.ALL|wx.EXPAND, border = 16)

        self.SetSizer(paddingSizer)

        self.Profile = parent
        self.TabTitle : str = type(self).__name__

        self.Ctrls : dict = {}

    def GetState(self, key):
        control = self.Ctrls.get(key, None)
        if not control:
            wx.LogWarning(f"Unknown control in GetState: {key} - this is a bug.")
            return ''
        # We might be tempted to short-circuit out if the control is not enabled
        # but that breaks things terribly during window init.  Might be worth tracking
        # down and fixing but not today.
        if isinstance(control, wx.DirPickerCtrl):
            return control.GetPath()
        elif isinstance(control, PowerPicker):
            # we de-json this on the way out in ProfileData.AsJSON()
            return json.dumps({
                'power'    : control.GetLabel(),
                'iconfile' : control.IconFilename,
            })
        elif isinstance(control, bcKeyButton):
            return control.Key
        elif isinstance(control, wx.Button):
            return control.GetLabel()
        elif isinstance(control, wx.ColourPickerCtrl) or isinstance(control, csel.ColourSelect):
            return control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        elif isinstance(control, wx.Choice) or isinstance(control, wx.ComboBox):
            sel = control.GetSelection()
            if sel != wx.NOT_FOUND: return control.GetString(sel)
            else                  : return ''
        elif isinstance(control, wx.ColourPickerCtrl) or isinstance(control, csel.ColourSelect):
            return control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        elif isinstance(control, wx.StaticText):
            return control.GetLabel()
        elif getattr(control, 'GetValue', None):
            return control.GetValue()
        elif getattr(control, 'GetPath', None):
            return control.GetPath()
        else:
            wx.LogError(f"control '{key}' has no GetValue() - this is a bug")
            return ''

    def SetState(self, key, value):
        control = self.Ctrls.get(key, None)
        if not control:
            wx.LogError(f"Got into SetState for key {key} with no control - this is a bug.")
            return

        if isinstance(control, wx.Button):
            return control.SetLabel(value)
        elif isinstance(control, wx.Choice):
            if isinstance(value, str):
                value = control.FindString(value)
                if value == wx.NOT_FOUND: value = 0
            return control.SetSelection(value)
        elif isinstance(control, wx.StaticText):
            return control.SetLabel(value)
        elif getattr(control, 'SetValue', None):
            return control.SetValue(value)
        elif getattr(control, 'SetPath', None):
            return control.SetPath(value)
        else:
            wx.LogError(f"{control} has no SetValue() - this is a bug.")

    def OnCommandEvent(self, evt):
        if evt: evt.Skip()
        # TODO:  "unless (some way to opt things out of this), then..."
        self.Profile.SetModified()

    def GetKeyBinds(self):
        binds = []
        for ctrlname, ctrl in self.Ctrls.items():
            if isinstance(ctrl, bcKeyButton):
                if not ctrl.IsThisEnabled(): continue
                binds.append( [ctrlname, ctrl.Key] )
        return binds

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
    def PopulateBindFiles(self) -> bool:
        return True

    # return a list of all bindfiles
    def AllBindFiles(self):
        wx.LogWarning(f"AllBindFiles called on parent Page, needs implementing in {type(self).__name__}.")
        return {
            'files' : [],
            'dirs'  : [],
        }
