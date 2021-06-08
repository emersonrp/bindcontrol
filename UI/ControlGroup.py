import wx
import UI

from UI.KeyBindDialog import KeyBindDialog

class ControlGroup(wx.StaticBoxSizer):

    def __init__(self, parent, page, label, width = 2):
        wx.StaticBoxSizer.__init__(self, wx.VERTICAL, parent, label = label)

        self.Parent = parent
        self.Page   = page
        # self.Add(wx.StaticBox( parent, -1), wx.VERTICAL)

        self.InnerSizer = wx.FlexGridSizer(0,width,3,3)
        self.Add(self.InnerSizer, 0, wx.ALIGN_RIGHT|wx.ALL, 16)

    # control will parent itself in self.Parent
    # optional ctlParent arg will pick a different parent for complicated layouts
    def AddLabeledControl(self, ctlParent = None,
            ctlType = '', ctlName = '', noLabel = False,
            contents = '', tooltip = '', callback = None):

        sizer     = self.InnerSizer
        Init      = self.Page.Init
        ctlParent = ctlParent if ctlParent else self.Parent

        padding = 2

        label = UI.Labels.get(ctlName, ctlName)
        if not noLabel:
            text = wx.StaticText(ctlParent, -1, label + ':')

        if ctlType == ('keybutton'):
            control = wx.Button( ctlParent, -1, Init[ctlName])
            control.Bind(wx.EVT_BUTTON, self.KeyPickerDialog)
            control.CtlName = ctlName

        elif (ctlType == 'combo') or (ctlType == "combobox"):
            control = wx.ComboBox(
                ctlParent, -1, Init[ctlName],
                choices = contents or (), style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback )

        elif ctlType == ('text'):
            control = wx.TextCtrl(ctlParent, -1, Init[ctlName])

        elif ctlType == ('checkbox'):
            control = wx.CheckBox(ctlParent, -1)
            control.SetValue(bool(Init[ctlName]))
            padding = 10

        elif ctlType == ('spinbox'):
            control = wx.SpinCtrl(ctlParent, -1)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == ('dirpicker'):
            control = wx.DirPickerCtrl(
                ctlParent, -1, Init[ctlName], Init[ctlName],
                wx.DefaultPosition, wx.DefaultSize,
                wx.DIRP_USE_TEXTCTRL|wx.ALL,
            )
        else: die(f"wtf?!  Got a ctlType that I don't know: {ctlType}")
        if tooltip:
            control.SetToolTip( wx.ToolTip(tooltip))

        if not noLabel:
            sizer.Add( text,    0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add( control, 0, wx.ALL|wx.EXPAND, padding)

        self.Page.Controls[ctlName] = control

        self.Layout()

    def KeyPickerDialog(self, evt):
        button = evt.EventObject

        with KeyBindDialog(self.Parent, button.CtlName, button.Label) as dlg:

            newKey = ''

            if(dlg.ShowModal() == wx.ID_OK): newKey = dlg.Binding

            # TODO -- check for conflicts
            # otherThingWithThatBind = checkConflicts(newKey)

            # re-label the button / set its state
            if newKey:
                evt.EventObject.SetLabel(newKey)
