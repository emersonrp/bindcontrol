import wx

from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.ControlGroup import ControlGroup
from UI.PowerBinderDialog import PowerBinderButton

class BufferBindPane(CustomBindPaneParent):
    def __init__(self, page, bind):
        CustomBindPaneParent.__init__(self, page, bind)
        self.Page = page
        self.Init = {
            'BuffPetsByName' : True,
            'BuffsAffectTeam': True,
            'BuffsAffectPets': True,
        }

        for i in (1,2,3,4,5,6,7,8):
            self.Init[f"Team{i}BuffKey"] = "UNBOUND"

        for i in (1,2,3,4,5,6):
            self.Init[f"Pet{i}BuffKey"] = "UNBOUND"

    def BuildBindUI(self, BindCP, page):

        BindCP.SetLabel("This is a test label")
        pane = BindCP.GetPane()

        # bind text controls
        BindSizer = wx.GridBagSizer(hgap=5, vgap=5)
        BindSizer.Add(wx.StaticText(pane, -1, "Bind Name:"),     (0,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.TextCtrl  (pane, -1, ""),               (0,1), span=(1,4), flag=wx.EXPAND)

        BindSizer.Add(wx.StaticText(pane, -1, "First Buff Power"),  (1,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(self.BuffPowerPicker(pane),                   (1,1), flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.StaticText(pane, -1, "Extra"),             (1,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        buffPower1 = wx.TextCtrl  (pane, -1, "")
        BindSizer.Add(buffPower1,                                   (1,3), flag=wx.EXPAND)
        BindSizer.Add(PowerBinderButton(pane, targetTextCtrl=buffPower1), (1,4), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        BindSizer.Add(wx.StaticText(pane, -1, "Second Buff Power"), (2,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(self.BuffPowerPicker(pane),                   (2,1), flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.StaticText(pane, -1, "Extra"),             (2,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        buffPower2 = wx.TextCtrl  (pane, -1, "")
        BindSizer.Add(buffPower2,                                   (2,3), flag=wx.EXPAND)
        BindSizer.Add(PowerBinderButton(pane, targetTextCtrl=buffPower2), (2,4), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        BindSizer.Add(wx.StaticText(pane, -1, "Third Buff Power"),  (3,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(self.BuffPowerPicker(pane),                   (3,1), flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.StaticText(pane, -1, "Extra"),             (3,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        buffPower3 = wx.TextCtrl  (pane, -1, "")
        BindSizer.Add(buffPower3,                                   (3,3), flag=wx.EXPAND)
        testbutton = PowerBinderButton(pane, targetTextCtrl=buffPower3)
        print(testbutton)
        BindSizer.Add(PowerBinderButton(pane, targetTextCtrl=buffPower3), (3,4), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        BindSizer.Add(wx.StaticText(pane, -1, ""),                 (4,0))


        # key picker controls
        KeySizer = wx.BoxSizer(wx.HORIZONTAL)
        TeamCtrls = ControlGroup(pane, self.Page, "Buff Team Keybinds")
        PetCtrls  = ControlGroup(pane, self.Page, "Buff Pet Keybinds")

        TeamCtrls.AddLabeledControl(ctlType = 'checkbox', ctlName = "BuffsAffectTeam")
        for i in (1,2,3,4,5,6,7,8):
            TeamCtrls.AddLabeledControl(ctlType = "keybutton", ctlName = f"Team{i}BuffKey", contents = "UNBOUND")


        PetCtrls.AddLabeledControl(ctlType = 'checkbox', ctlName = "BuffsAffectPets")
        PetCtrls.AddLabeledControl(ctlType = "checkbox", ctlName = "BuffPetsByName")
        for i in (1,2,3,4,5,6):
            PetCtrls.AddLabeledControl(ctlType = "keybutton", ctlName = f"Pet{i}BuffKey", contents = "UNBOUND")

        KeySizer.Add(TeamCtrls, 0, flag = wx.LEFT|wx.RIGHT, border = 5)
        KeySizer.Add(PetCtrls,  0, flag = wx.LEFT|wx.RIGHT, border = 5)

        BindSizer.AddGrowableCol(1)
        BindSizer.AddGrowableCol(3)
        BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(BindSizer, 0, wx.EXPAND|wx.ALL, 10)
        border.Add(KeySizer,  0, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)


    def BuffPowerPicker(self, pane):
        picker = wx.Choice(pane, -1)
        return picker
