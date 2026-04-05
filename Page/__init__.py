# base class for all the individual tabs

#  The Page keeps a list of each of the (non-static) controls on itself.
#  It then tries to gatekeep these behind .GetState() and .SetState()
#  in reality, we need to get directly at the controls occasionally
#  to change a wx.Choice's list, for example.  Then we just trawl
#  through page.Ctrls directly.  This could be improved.

# Much later observation:  gating behind GetState and SetState wreaks
# havoc on the entire notion of type checking, since GetState can in
# principle return str|bool|list|etc.  Undoing this would be tangly
# but might be The Right Thing.

#  page.GetState('FPSBindKey')
#  page.SetState('Archetype', 'Blaster')

import json
from typing import TYPE_CHECKING, Final
from pubsub import pub

import wx
import wx.lib.colourselect as csel
if TYPE_CHECKING:
    from Profile import Profile as bcProfile
from UI.KeySelectDialog import bcKeyButton

class Page(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)

        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(self.MainSizer, 1, flag = wx.ALL|wx.EXPAND, border = 16)

        self.SetSizer(paddingSizer)

        self.Profile  : bcProfile = parent
        self.TabTitle : str = type(self).__name__
        self.Server   : Final[str] = self.Profile.Server()

        self.Ctrls : dict = {}
        self.Init  : dict = {}

        pub.subscribe(self.OnCommandPubSub, 'chatcolorpickerchanged')
        pub.subscribe(self.OnCommandPubSub, 'powerbinderchanged')
        pub.subscribe(self.OnCommandPubSub, 'powerpickerchanged')
        pub.subscribe(self.OnCommandPubSub, 'powerselectorchanged')

    def OnCommandPubSub(self, control):
        self.Profile.DoCommand(self, control)

    def GetState(self, key) -> str:
        control = self.Ctrls.get(key)
        if not control:
            wx.LogWarning(f"Unknown control in GetState: {key} - this is a bug.")
            return ''

        retval = None
        if isinstance(control, wx.DirPickerCtrl):
            retval = control.GetPath()
        elif isinstance(control, (wx.ColourPickerCtrl, csel.ColourSelect)):
            retval = control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        elif isinstance(control, (wx.Choice, wx.ComboBox)):
            retval = control.GetStringSelection()
        elif isinstance(control, wx.Notebook):
            retval = control.GetPageText(control.GetSelection())
        elif getattr(control, 'GetValue', None):
            retval = control.GetValue()
        elif getattr(control, 'GetPath', None):
            retval = control.GetPath()
        else:
            wx.LogError(f"control '{control.CtlName}' has no GetValue() - this is a bug")
            retval = ''

        if isinstance(retval, (dict, list)):
            retval = json.dumps(retval)

        return retval

    def SetState(self, key, value) -> str|int|None:
        control = self.Ctrls.get(key)
        if not control:
            wx.LogError(f"Got into SetState for key {key} with no control - this is a bug.")
            return ''

        if isinstance(control, wx.Choice):
            if isinstance(value, str):
                return control.SetStringSelection(value)
            else:
                return control.SetSelection(value)
        elif isinstance(control, wx.Notebook):
            for i in range(control.GetPageCount()):
                if control.GetPageText(i) == value:
                    return control.SetSelection(i)
        elif getattr(control, 'SetValue', None):
            return control.SetValue(value)
        elif getattr(control, 'SetPath', None):
            return control.SetPath(value)
        else:
            wx.LogError(f"Control '{control.CtlName}' has no SetValue() - this is a bug.")

    def GetKeyBinds(self):
        binds = []
        for ctrlname, ctrl in self.Ctrls.items():
            if isinstance(ctrl, bcKeyButton):
                # we need IsThisEnabled() instead of IsEnabled() because on Windows
                # IsEnabled is falsie for everything when checking from the prefs
                # dialog.  I thiiiink that's because it's modal, so everything else
                # is "disabled" temporarily.  IsThisEnabled() gets the right thing.
                if not ctrl.IsThisEnabled(): continue
                binds.append( [ctrlname, ctrl.Key] )
        return binds

    # disable controls by name
    def EnableControls(self, enabled, names) -> None:
        for name in names:
            if name in self.Ctrls:
                self.Ctrls[name].Enable(enabled)

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
