from PowerBindCmd import PowerBindCmd
import wx


####### Use Insp From Row / Column
class UseInspRowColCmd(PowerBindCmd):
    def __init__(self, dialog):
        PowerBindCmd.__init__(self, dialog)

    def BuildUI(self, dialog):
        useInspRowColumnSizer = wx.BoxSizer(wx.HORIZONTAL)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Row:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        useInspRowColumnRow = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS|wx.ALIGN_CENTER_VERTICAL)
        useInspRowColumnRow.SetRange(1, 4)
        useInspRowColumnSizer.Add(useInspRowColumnRow, 1)
        useInspRowColumnSizer.Add(wx.StaticText(dialog, -1, "Column:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 4)
        useInspRowColumnCol = wx.SpinCtrl(dialog, -1, style=wx.SP_ARROW_KEYS|wx.ALIGN_CENTER_VERTICAL)
        useInspRowColumnCol.SetRange(1, 5)
        useInspRowColumnSizer.Add(useInspRowColumnCol, 1)

        return useInspRowColumnSizer

