import wx
from UI.PowerBinderCommand import PowerBinderCommand

####### Use Insp From Row / Column
class UseInspRowColCmd(PowerBinderCommand):
    Name = "Use Inspiration From Row/Column"
    Menu = "Inspirations"
    DeprecatedName = "Use Insp From Row/Column"

    def BuildUI(self, dialog) -> wx.BoxSizer:
        CenteringSizer = wx.BoxSizer(wx.VERTICAL)

        useInspRowColumnSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Row:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.useInspRowColumnRow = wx.Choice(dialog, -1, choices=['1','2','3','4', 'Bottom'], style=wx.ALIGN_CENTER_VERTICAL)
        self.useInspRowColumnRow.SetSelection(0)
        useInspRowColumnSizer.Add(self.useInspRowColumnRow, 0, wx.ALIGN_CENTER_VERTICAL)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Column:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 4)
        self.useInspRowColumnCol = wx.Choice(dialog, -1, choices=['1','2','3','4','5'], style=wx.ALIGN_CENTER_VERTICAL)
        self.useInspRowColumnCol.SetSelection(0)
        useInspRowColumnSizer.Add(self.useInspRowColumnCol, 0, wx.ALIGN_CENTER_VERTICAL)

        CenteringSizer.Add(useInspRowColumnSizer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        return CenteringSizer

    def MakeBindString(self) -> str:
        row = self.useInspRowColumnRow.GetSelection()+1
        col = self.useInspRowColumnCol.GetSelection()+1

        if row == 5:
            return f"inspexec_slot {col}"
        else:
            return f"inspexectray {col} {row}"

    def Serialize(self) -> dict:
        return {
            'col' : self.useInspRowColumnCol.GetSelection(),
            'row' : self.useInspRowColumnRow.GetSelection(),
        }

    def Deserialize(self, init) -> None:
        if init.get('col', ''): self.useInspRowColumnCol.SetSelection(init['col'])
        if init.get('row', ''): self.useInspRowColumnRow.SetSelection(init['row'])
