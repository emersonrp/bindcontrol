import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Use Power From Tray
class UsePowerFromTrayCmd(PowerBinderCommand):
    Name = "Use Power From Tray"
    Menu = "Powers"

    def BuildUI(self, dialog):
        usePowerFromTraySizer = wx.BoxSizer(wx.HORIZONTAL)
        usePowerFromTraySizer.Add(wx.StaticText(dialog, -1, "Tray:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.usePowerFromTrayTray = wx.Choice(dialog, -1,
               choices = ['Main Tray', 'Alt Tray', 'Alt 2 Tray', 'Tray 1', 'Tray 2', 'Tray 3',
                   'Tray 4', 'Tray 5', 'Tray 6', 'Tray 7', 'Tray 8', 'Tray 9', 'Tray 10'])
        self.usePowerFromTrayTray.SetSelection(0)
        usePowerFromTraySizer.Add(self.usePowerFromTrayTray, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        usePowerFromTraySizer.Add(wx.StaticText(dialog, -1, "Slot:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.usePowerFromTraySlot = wx.Choice(dialog, -1, choices=['1','2','3','4','5','6','7','8','9','10'])
        self.usePowerFromTraySlot.SetSelection(0)
        usePowerFromTraySizer.Add(self.usePowerFromTraySlot, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        return usePowerFromTraySizer

    def MakeBindString(self):
        choice = self.usePowerFromTrayTray
        tray = choice.GetSelection()

        choice = self.usePowerFromTraySlot
        slot   = choice.GetSelection()+1

        mode = "slot"
        mode2 = ''
        if tray > 3:
            mode = "tray"
            mode2 = f" {tray - 3}"
        elif tray == 3:
            mode = "alt2slot"
        elif tray == 2:
            mode = "altslot"

        return f"powexec{mode} {slot}{mode2}"

    def Serialize(self):
        return {
            'tray' : self.usePowerFromTrayTray.GetSelection(),
            'slot' : self.usePowerFromTraySlot.GetSelection(),
        }

    def Deserialize(self, init):
        if init.get('tray', ''): self.usePowerFromTrayTray.SetSelection(init['tray'])
        if init.get('slot', ''): self.usePowerFromTraySlot.SetSelection(init['slot'])
