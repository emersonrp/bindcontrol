import wx
import string
import UI

def PowerBinderEventHandler(evt):
    button = evt.EventObject

    with PowerBinderDialog(button.Parent) as dlg:

        if(dlg.ShowModal() == wx.ID_OK): pass

class PowerBinderDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "PowerBinder", style = wx.DEFAULT_DIALOG_STYLE)

        sizer = wx.BoxSizer(wx.VERTICAL);

        self.rearrangeCtrl = wx.RearrangeCtrl(self, -1, size=(350,300))
        sizer.Add(self.rearrangeCtrl, 1, wx.EXPAND)

        choiceSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bindChoice = wx.Choice(self, -1, choices= [
            'Auto Power', 'Away From Keyboard', 'Chat Command',
            'Chat Command (Global)', 'Costume Change', 'Custom Bind',
            'Emote', 'Power Abort', 'Power Unqueue', 'SG Mode Toggle',
            'Target Custom', 'Target Enemy', 'Target Friend',
            'Team/Pet Select', 'Unselect', 'Use Insp by Name',
            'Use Insp From Row / Custom', 'Use Power', 'Use Power From Tray',
            'Window Toggle',
        ])
        self.bindChoice.SetSelection(self.bindChoice.FindString("Use Power"))
        choiceSizer.Add(self.bindChoice, 0, wx.ALIGN_CENTER_VERTICAL)
        addButton = wx.Button(self, -1, "Add")
        choiceSizer.Add(addButton, 0, wx.ALIGN_CENTER_VERTICAL)
        addButton.Bind(wx.EVT_BUTTON, self.AddSomething)


        sizer.Add(choiceSizer, 0, wx.EXPAND|wx.TOP, 16)
        sizer.Add(self.CreateSeparatedButtonSizer(wx.OK|wx.CANCEL|wx.HELP), 0)

        # Wrap everything in a vbox to add some padding
        vbox = wx.BoxSizer(wx.VERTICAL);
        vbox.Add(sizer, 0, wx.EXPAND|wx.ALL, 10);

        self.SetSizerAndFit(vbox);
        self.Layout()
        self.SetFocus()


    def AddSomething(self, evt):
        chosenName = self.bindChoice.GetString(self.bindChoice.GetSelection())

        self.rearrangeCtrl.GetList().Append(chosenName)


