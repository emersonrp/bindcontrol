import wx
import UI
from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import KeySelectEventHandler
from UI.PowerBinderDialog import PowerBinderButton

### CustomBind subclasses for the individual bind types

class SimpleBindPane(CustomBindPaneParent):
    def __init__(self, page, bind = {}):
        CustomBindPaneParent.__init__(self, page, bind)

        if bind:
            self.Title = bind['Title']
            self.Key = bind['Key']
            self.Contents = bind['Contents']

    def Serialize(self):
        data = {
            'Type'     : 'SimpleBind',
            'Title'    : self.Title,
            'Contents' : self.Ctrls['BindContents'].GetValue(),
            'Key'      : self.Ctrls['BindKey'].GetValue(),
        }

    def BuildBindUI(self, page):

        self.SetLabel(self.Title)
        pane = self.GetPane()

        BindSizer = wx.BoxSizer(wx.HORIZONTAL)

        BindContentsCtrl = wx.TextCtrl(pane, -1, self.Contents)
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Contents:"), 0, wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(BindContentsCtrl, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(PowerBinderButton(pane, tgtTxtCtrl=BindContentsCtrl), 0)
        page.Ctrls[self.UniqueName('BindContents')] = BindContentsCtrl

        BindKeyCtrl = wx.Button(pane, -1, self.Key)
        BindKeyCtrl.CtlName = f"{self.bindclass}{self.unique_bind_id}BindKey"
        BindKeyCtrl.Page = page
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Key:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5)
        BindSizer.Add(BindKeyCtrl,                          0)
        BindKeyCtrl.Bind(wx.EVT_BUTTON, KeySelectEventHandler)
        page.Ctrls[self.UniqueName('BindKey')] = BindKeyCtrl
        UI.Labels[BindKeyCtrl.CtlName] = "Simple Bind " + self.unique_bind_id

        BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(BindSizer, 1, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)
