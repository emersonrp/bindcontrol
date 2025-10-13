# base class for all the individual tabs

#  The Page keeps a list of each of the (non-static) controls on itself.
#  It then tries to gatekeep these behind .GetState() and .SetState()
#  in reality, we need to get directly at the controls occasionally
#  to change a wx.Choice's list, for example.  Then we just trawl
#  through page.Ctrls directly.  This could be improved.

#  page.GetState('FPSBindKey')
#  page.SetState('Archetype', 'Blaster')

import json
from typing import Any, TYPE_CHECKING
import wx
import wx.adv
import wx.lib.colourselect as csel
if TYPE_CHECKING:
    from Profile import Profile as bcProfile
    from UI.ControlGroup import bcControl
from UI.KeySelectDialog import bcKeyButton
from UI.PowerPicker import PowerPicker
from Icon import GetIcon

class Page(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(self.MainSizer, 1, flag = wx.ALL|wx.EXPAND, border = 16)

        self.SetSizer(paddingSizer)

        self.Profile  : bcProfile = parent
        self.TabTitle : str = type(self).__name__

        self.Ctrls : dict[str, bcControl] = {}
        self.Init  : dict[str, Any]       = {}

    def GetState(self, key):
        control = self.Ctrls.get(key)
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
        elif isinstance(control, (wx.Choice, wx.ComboBox)):
            sel = control.GetSelection()
            if sel != wx.NOT_FOUND: return control.GetString(sel)
            else                  : return ''
        elif isinstance(control, (wx.ColourPickerCtrl, csel.ColourSelect)):
            return control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        elif isinstance(control, wx.Notebook):
            return control.GetPageText(control.GetSelection())
        # TODO - I don't think we ever GetState on a StaticText, but maybe?
        # elif isinstance(control, wx.StaticText):
        #     return control.GetLabel()
        elif isinstance(control, (wx.ComboBox, wx.TextCtrl, wx.CheckBox, wx.adv.BitmapComboBox, wx.Slider, wx.SpinCtrl, wx.SpinCtrlDouble)):
            return control.GetValue()
        else:
            wx.LogError(f"control '{key}' type is unknown in GetState() - this is a bug")
            return ''

    def SetState(self, key, value) -> str|int|None:
        control = self.Ctrls.get(key)
        if not control:
            wx.LogError(f"Got into SetState for key {key} with no control - this is a bug.")
            return ''

        if isinstance(control, PowerPicker):
            if power := value.get('power'):
                control.SetLabel(power)
            if iconfile := value.get('iconfile'):
                control.IconFilename = iconfile
                control.SetBitmap(GetIcon(control.IconFilename))
        elif isinstance(control, wx.Button):
            if isinstance(control, bcKeyButton):
                control.Key = value
            return control.SetLabel(value)
        elif isinstance(control, wx.Choice):
            if isinstance(value, str):
                return control.SetStringSelection(value)
            else:
                return control.SetSelection(value)
        elif isinstance(control, (wx.ColourPickerCtrl, csel.ColourSelect)):
            if isinstance(value, tuple):
                colour = wx.Colour(*value)
            else:
                colour = wx.Colour()
                colour.Set(value)
            return control.SetColour(colour)
        elif isinstance(control, wx.Notebook):
            for i in range(control.GetPageCount()):
                if control.GetPageText(i) == value:
                    return control.SetSelection(i) # pyright: ignore  # for some reason type narrowing isn't working right
        elif isinstance(control, wx.StaticText):
            return control.SetLabel(value)
        elif isinstance(control, (wx.ComboBox, wx.TextCtrl, wx.adv.BitmapComboBox)):
            return control.SetValue(value)
        elif isinstance(control, (wx.CheckBox)):
            return control.SetValue(bool(value))
        elif isinstance(control, (wx.Slider, wx.SpinCtrl)):
            return control.SetValue(int(value))
        elif isinstance(control, (wx.SpinCtrlDouble)):
            return control.SetValue(float(value))
        elif isinstance(control, wx.DirPickerCtrl):
            return control.SetPath(value)
        else:
            wx.LogError(f"control '{key}' type is unknown in SetState() - this is a bug.")

    def GetKeyBinds(self):
        binds = []
        for ctrlname, ctrl in self.Ctrls.items():
            if isinstance(ctrl, bcKeyButton):
                if not ctrl.IsThisEnabled(): continue
                binds.append( [ctrlname, ctrl.Key] )
        return binds

    # disable controls by name
    def EnableControls(self, enabled, names) -> None:
        for name in names:
            self.Ctrls[name].Enable(bool(enabled))

    ##### stubs for overriding (shoes for industry!)
    def SynchronizeUI(self) -> None:
        return

    # create and display the UI for this page
    def BuildPage(self) -> None:
        return

    # create and fill the BindFile object with Bind objects
    # NB - no state should be kept in the page
    def PopulateBindFiles(self) -> bool:
        return True

    # return a list of all bindfiles
    def AllBindFiles(self) -> dict[str, list]:
        wx.LogWarning(f"AllBindFiles called on parent Page, needs implementing in {type(self).__name__}.")
        return {
            'files' : [],
            'dirs'  : [],
        }
