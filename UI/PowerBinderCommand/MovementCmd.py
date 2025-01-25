import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Movement Command
class MovementCmd(PowerBinderCommand):
    Name = "Movement Commands"
    Menu = "Misc"

    def BuildUI(self, dialog):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.plusbutton = wx.RadioButton(dialog, label = "+", style=wx.RB_GROUP|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.plusbutton, 0, wx.ALIGN_CENTER_VERTICAL)
        self.plusbutton.SetValue(True)

        self.plusplusbutton = wx.RadioButton(dialog, label = "++", style=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.plusplusbutton, 0, wx.ALIGN_CENTER_VERTICAL)

        self.minusbutton = wx.RadioButton(dialog, label = '-', style=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.minusbutton, 0, wx.ALIGN_CENTER_VERTICAL)

        self.commandchoice = wx.Choice(dialog, choices = [
            "forward", "left", "right", "backward", "up", "down",
            "turnleft", "turnright", "first", "autorun", "clicktomove",
        ],)
        sizer.Add(self.commandchoice, 0, wx.ALIGN_CENTER_VERTICAL)
        self.commandchoice.SetSelection(0)

        self.zerobutton = wx.RadioButton(dialog, label = "0", style=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.zerobutton, 0, wx.ALIGN_CENTER_VERTICAL)

        self.onebutton = wx.RadioButton(dialog, label = "1", style=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.onebutton, 0, wx.ALIGN_CENTER_VERTICAL)

        return sizer

    def MakeBindString(self):
        pre = post = ''
        if   self.plusbutton.GetValue()     : pre = "+"
        elif self.plusplusbutton.GetValue() : pre = "++"
        elif self.minusbutton.GetValue()    : pre = "-"
        elif self.zerobutton.GetValue()     : post = " 0"
        elif self.onebutton.GetValue()      : post = " 1"

        command = self.commandchoice.GetString(self.commandchoice.GetSelection())

        return f"{pre}{command}{post}"

    def Serialize(self):
        mod = ''
        if   self.plusbutton.GetValue()     : mod = "plus"
        elif self.plusplusbutton.GetValue() : mod = "plusplus"
        elif self.minusbutton.GetValue()    : mod = "minus"
        elif self.zerobutton.GetValue()     : mod = "zero"
        elif self.onebutton.GetValue()      : mod = "one"

        return {
            'mod'     : mod,
            'command' : self.commandchoice.GetString(self.commandchoice.GetSelection()),
        }

    def Deserialize(self, init):
        mod = init.get('mod', 'plus')

        if   mod == 'plus'     : self.plusbutton.SetValue(True)
        elif mod == 'plusplus' : self.plusplusbutton.SetValue(True)
        elif mod == 'minus'    : self.minusbutton.SetValue(True)
        elif mod == 'zero'     : self.zerobutton.SetValue(True)
        elif mod == 'one'      : self.onebutton.SetValue(True)

        self.commandchoice.SetSelection(self.commandchoice.FindString(init.get('command', 'forward')))
