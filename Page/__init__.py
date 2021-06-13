# base class for all the individual tabs

#  The Page keeps a list of each of the (non-static) controls on itself.
#  It then tries to gatekeep these behind .GetState() and .SetState()
#  in reality, we need to get directly at the controls occasionally
#  to change a wx.Choice's list, for example.  Then we just trawl
#  through page.Controls directly.  This could be improved.
#
#  There is an analogous CtrlLabels dict in case we want to get at
#  the static labels for the controls for some reason.
#  TODO -- if not, remove that notion from here and from ControlGroup

#  page.GetState('FPSBindKey')
#  page.SetState('Archetype', 'Blaster')

import wx

import BindFile

class Page(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Profile = parent
        self.TabTitle = type(self).__name__

        self.Controls = {}
        self.CtrlLabels = {}

    def help(self, event):
        if not (self.HelpWindow):
            HelpWindow = wx.MiniFrame .new( undef, -1, self.TabTitle + " Help",)
            BoxSizer   = wx.BoxSizer  .new( wx.VERTICAL )
            Panel      = wx.Panel     .new( HelpWindow, -1 )
            HelpText   = wx.StaticText.new( Panel, -1, self.HelpText, [10,10] )

            BoxSizer.Add( Panel, 1, wx.EXPAND )

            HelpWindow.SetSizer(BoxSizer)

            self.HelpWindow = HelpWindow

        self.HelpWindow.Show(not self.HelpWindow.IsShown())

    def GetState(self, key):
        control = self.Controls.get(key, None)
        if not control:
            return
        if isinstance(control, wx.Button):
            return control.GetLabel()
        elif isinstance(control, wx.Choice) or isinstance(control, wx.ComboBox):
            return control.GetSelection()
        elif getattr(control, 'GetValue', None):
            return control.GetValue()
        elif getattr(control, 'GetPath', None):
            return control.GetPath()
        else:
            print(f"{control} has no GetValue()")

    def SetState(self, key, value):
        control = self.Controls.get(key, None)

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

    ##### stubs for overriding (shoes for industry!)

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

