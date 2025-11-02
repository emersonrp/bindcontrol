from typing import Any
from collections.abc import Callable

import wx

import Exceptions
from Help import HelpButton
from Page import Page as bcPage

import UI
from UI.CGControls import (
    cgbcKeyButton,
    cgComboBox,
    cgBMComboBox,
    cgTextCtrl,
    cgStaticText,
    cgCheckBox,
    cgSpinCtrl,
    cgSpinCtrlDouble,
    cgDirPickerCtrl,
    cgColourPickerCtrl,
    cgChoice,
)
from UI.PowerSelector import PowerSelector

class ControlGroup(wx.StaticBoxSizer):
    def __init__(self, parent, page : bcPage, label = '', width = 2, flexcols : list|None = None, topcontent = None) -> None:
        flexcols = flexcols or [0]

        super().__init__(wx.VERTICAL, parent, label = label)
        self.vertCenteringSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.Page = page
        self.Ctrls = []

        # usually for an "enable this stuff" checkbox in a wx.Panel
        if topcontent:
            topcontent.Reparent(self.GetStaticBox())
            self.Add(topcontent, 0, wx.ALL|wx.EXPAND, 5)

        self.InnerSizer = wx.FlexGridSizer(width,3,3)
        for col in flexcols: self.InnerSizer.AddGrowableCol(col)

        if self.Page.Profile.EditingDefault:
            self.GetStaticBox().SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        self.vertCenteringSizer.Add(self.InnerSizer, 1, wx.ALIGN_CENTER_VERTICAL)
        self.Add(self.vertCenteringSizer, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)

    def AddControl(self,
                   ctlType  : str           = '',
                   ctlName  : str           = '',
                   noLabel  : bool          = False,
                   contents : Any           = '',
                   tooltip  : str           = '',
                   callback : Callable|None = None,
                   label    : str           = '',
                   data     : Any           = None,
                   size     : wx.Size       = wx.DefaultSize,
                   context  : str           = '',
                   helpfile : str           = '',
       ):

        if not ctlName:
            msg = "Tried to make a labeled control without a CtlName.  This is a bug."
            raise Exceptions.UIControlGroupNoCttNameException(msg)

        Init      = self.Page.Init
        CtlParent = self.GetStaticBox()
        CtlLabel  = None

        padding = 0

        label = label or UI.Labels.get(ctlName, ctlName)

        if ctlType == 'keybutton':
            control = cgbcKeyButton(CtlParent)
            control.SetLabel(Init[ctlName])
            # push context onto the button, we'll thank me later
            control.Key     = Init[ctlName]

        elif ctlType == 'powerselector':
            control = PowerSelector(CtlParent, self.Page, context)
            noLabel = True

        elif (ctlType == 'combo') or (ctlType == "combobox"):
            control = cgComboBox(
                CtlParent,
                value = Init[ctlName],
                size = size,
                choices = contents or (),
                style = wx.CB_READONLY)
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback)

        elif (ctlType == 'bmcombo') or (ctlType == "bmcombobox"):
            choices = []
            bitmaps = []
            for c in contents:
                choices.append(c[0])
                bitmaps.append(c[1])
            control = cgBMComboBox(
                CtlParent,
                value = '',
                style = wx.CB_READONLY,
                choices = choices,
                size = size,
            )
            if callback:
                control.Bind(wx.EVT_COMBOBOX, callback)
            for i, entry in enumerate(bitmaps):
                control.SetItemBitmap(i, entry)
            index = control.FindString(Init[ctlName])
            if index == -1:
                control.SetValue(Init[ctlName])
            else:
                control.SetSelection(index)

        elif ctlType == 'text':
            control = cgTextCtrl(CtlParent,
                                 value = Init[ctlName],
                                 size = size)

        elif ctlType == 'choice':
            contents = contents if contents else []
            control = cgChoice(CtlParent, choices = contents, size = size)
            control.SetStringSelection(Init[ctlName])
            if callback:
                control.Bind(wx.EVT_CHOICE, callback)

        elif ctlType == 'statictext':
            control = cgStaticText(CtlParent,
                                   value = Init.get(ctlName, ''),
                                   size = size)

        elif ctlType == 'checkbox':
            control = cgCheckBox(CtlParent,
                                 label = contents,
                                 size = size)
            control.SetValue(bool(Init.get(ctlName, False)))
            if not helpfile:
                padding = 6
            if callback:
                control.Bind(wx.EVT_CHECKBOX, callback)

        elif ctlType == 'spinbox':
            control = cgSpinCtrl(CtlParent, size = size)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == 'spinboxfractional':
            control = cgSpinCtrlDouble(CtlParent, inc = 0.05, size = size)
            control.SetValue(Init[ctlName])
            control.SetRange(*contents)

        elif ctlType == 'dirpicker':
            control = cgDirPickerCtrl(
                CtlParent,
                message = Init[ctlName],
                size = size,
            )

        elif ctlType == 'colorpicker':
            control = cgColourPickerCtrl(
                CtlParent,
                colour = contents,
                size = (30,30),
            )

        else:
            msg = f"Got a ctlType in ControlGroup that I don't know: {ctlType}.  This is a bug."
            raise Exceptions.UIControlGroupUnknownCtlTypeException(msg)

        if not noLabel:
            CtlLabel = cgStaticText(CtlParent, -1, label + ':')

        # Let them all know their own name
        control.CtlName = ctlName # pyright: ignore

        # stash away the page that the control belongs to
        control.Page = self.Page

        # And any user-defined data.  I thought wx had a scheme for this but no?
        control.Data = data

        if not noLabel and CtlLabel:
            self.InnerSizer.Add(CtlLabel, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 6)
            control.CtlLabel = CtlLabel
            CtlLabel.control = control

        # Pack'em in there
        if tooltip and tooltip != '':
            control.DefaultToolTip = tooltip
            control.SetToolTip(tooltip)

        # make checkboxes' labels click to check them
        if ctlType == ('checkbox') and control.CtlLabel:
            control.CtlLabel.Bind(wx.EVT_LEFT_DOWN, self.OnCBLabelClick)

        # if we specified a helpfile, wrap it up with a helpbutton to the right
        if helpfile:
            control.HelpButton = HelpButton(CtlParent, helpfile)

            weeSizer = wx.BoxSizer(wx.HORIZONTAL)
            weeSizer.Add(control.HelpButton, 0)
            weeSizer.Add(control, 1, wx.EXPAND|wx.LEFT, 3)
            payload = weeSizer
        else:
            payload = control

        self.InnerSizer.Add(payload, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, padding)

        self.Ctrls.append(control)
        self.Page.Ctrls[ctlName] = control

        self.Layout()
        return control

    def EnableCtrls(self, show) -> None:
        for c in self.Ctrls:
            c.Enable(show)

    # check or uncheck checkboxes when clicking the associated label
    def OnCBLabelClick(self, evt) -> None:
        cblabel = evt.EventObject
        cblabel.control.SetValue(not cblabel.control.IsChecked())
        fakeevt = wx.CommandEvent(wx.wxEVT_CHECKBOX)
        fakeevt.SetEventObject(cblabel.control)
        wx.PostEvent(cblabel.control, fakeevt)
        evt.Skip()
