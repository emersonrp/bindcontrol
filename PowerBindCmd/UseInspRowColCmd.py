from PowerBindCmd import PowerBindCmd
import wx


####### Use Insp From Row / Column
class UseInspRowColCmd(PowerBindCmd):
    def BuildUI(self, dialog):
        useInspRowColumnSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Row:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.useInspRowColumnRow = wx.Choice(dialog, -1, choices=['1','2','3','4'], style=wx.ALIGN_CENTER_VERTICAL)
        self.useInspRowColumnRow.SetSelection(0)
        useInspRowColumnSizer.Add(self.useInspRowColumnRow, 1)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Column:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        self.useInspRowColumnCol = wx.Choice(dialog, -1, choices=['1','2','3','4','5'], style=wx.ALIGN_CENTER_VERTICAL)
        self.useInspRowColumnCol.SetSelection(0)
        useInspRowColumnSizer.Add(self.useInspRowColumnCol, 1)

        return useInspRowColumnSizer

    def MakeBindString(self, dialog):
        row = self.useInspRowColumnRow.GetSelection()+1
        col = self.useInspRowColumnCol.GetSelection()+1

        return f"inspexectray {col} {row}"

