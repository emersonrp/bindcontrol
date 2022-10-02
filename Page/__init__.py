# base class for all the individual tabs

#  The Page keeps a list of each of the (non-static) controls on itself.
#  It then tries to gatekeep these behind .GetState() and .SetState()
#  in reality, we need to get directly at the controls occasionally
#  to change a wx.Choice's list, for example.  Then we just trawl
#  through page.Ctrls directly.  This could be improved.

#  page.GetState('FPSBindKey')
#  page.SetState('Archetype', 'Blaster')

import wx

import BindFile

class Page(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Profile = parent
        self.TabTitle = type(self).__name__
        self.HelpWindow = None

        self.Ctrls = {}

    def help(self, event):
        if not (self.HelpWindow):
            HelpWindow = wx.MiniFrame ( None, -1, self.TabTitle + " Help",
                       style = wx.CAPTION|wx.CLOSE_BOX|wx.STAY_ON_TOP|wx.RESIZE_BORDER)
            BoxSizer   = wx.BoxSizer  ( wx.VERTICAL )
            HelpText   = wx.StaticText( HelpWindow, -1, self.HelpText())

            BoxSizer.Add( HelpText, 1, wx.EXPAND|wx.ALL, 10)

            HelpWindow.SetSizer(BoxSizer)

            self.HelpWindow = HelpWindow

        self.HelpWindow.Show(not self.HelpWindow.IsShown())

    def GetState(self, key):
        control = self.Ctrls.get(key, None)
        if not control:
            return ''
        if isinstance(control, wx.Button):
            return control.GetLabel()
        elif isinstance(control, wx.Choice) or isinstance(control, wx.ComboBox):
            return control.GetString(control.GetSelection())
        elif isinstance(control, wx.ColourPickerCtrl):
            return control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
        elif getattr(control, 'GetValue', None):
            return control.GetValue()
        elif getattr(control, 'GetPath', None):
            return control.GetPath()
        else:
            print(f"{control} has no GetValue()")

    def SetState(self, key, value):
        control = self.Ctrls.get(key, None)

        if not control:
            print(f"Got into SetState for key {key} with no control")

        if isinstance(control, wx.Button):
            return control.SetLabel(value)
        elif isinstance(control, wx.Choice) or isinstance(control, wx.ComboBox):
            return control.SetSelection(value)
        elif getattr(control, 'SetValue', None):
            return control.SetValue(value)
        elif getattr(control, 'SetPath', None):
            return control.SetPath(value)
        else:
            print(f"{control} has no SetValue()")


    # disable controls by name
    def DisableControls(self, enabled, names):
        for name in names:
            self.Ctrls[name].Enable(enabled)
            if self.Ctrls[name].ctlLabel:
                self.Ctrls[name].ctlLabel.Enable(enabled)

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
    # TODO general logic,
    # profile.GetBindFile(filename)
    # for x in Controls:
        # (do the thing)
        # bindfile.SetBind(the thing)
    # Walk away renee

    def HelpText(self):
        return 'Help not currently implemented here.'

