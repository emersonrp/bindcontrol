import wx
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeyBindDialog import KeyPickerEventHandler

### CustomBind subclasses for the individual bind types

class SimpleBindPane(CustomBindPaneParent):
    def __init__(self, page, bind = {}):
        CustomBindPaneParent.__init__(self, page, bind)

    def BuildBindUI(self, page):

        self.CPane.SetLabel("This is a test label")
        pane = self.CPane.GetPane()

        # TODO - get 'bindclass' (Simple, Buffer, etc) and 'unique-bind-id' scheme
        bindclass = ''
        unique_bind_id = ''

        BindSizer = wx.GridBagSizer(hgap=5, vgap=5)

        BindNameCtrl = wx.TextCtrl(pane, -1, self.Name)
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Name:"), (0,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(BindNameCtrl,                          (0,1), flag=wx.EXPAND)
        page.Controls["BindName"] = BindNameCtrl

        BindKeyCtrl = wx.Button(pane, -1, self.Key)
        BindKeyCtrl.CtlName = f"{bindclass}{unique_bind_id}BindKey"
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Key:"), (0,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(BindKeyCtrl,                          (0,3), flag=wx.EXPAND)
        BindKeyCtrl.Bind(wx.EVT_BUTTON, KeyPickerEventHandler)
        page.Controls['BindKey'] = BindKeyCtrl

        BindContentsCtrl = wx.TextCtrl(pane, -1, self.Contents)
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Contents:"), (1,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(BindContentsCtrl,                          (1,1), span=(1,3), flag=wx.ALL|wx.EXPAND)
        page.Controls['BindContents'] = BindContentsCtrl

        BindSizer.AddGrowableCol(1)
        BindSizer.AddGrowableCol(3)

        BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(BindSizer, 1, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)
