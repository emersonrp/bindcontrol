import wx
import UI
from UI.PowerPicker import PowerPicker

from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.ControlGroup import ControlGroup
from UI.PowerBinderDialog import PowerBinderButton

class BufferBindPane(CustomBindPaneParent):
    def __init__(self, page):
        CustomBindPaneParent.__init__(self, page)
        self.Page = page
        page.Init = {
            'BuffPetsByName' : True,
            'BuffsAffectTeam': True,
            'BuffsAffectPets': True,
        }

        UI.Labels.update({
            "BuffsAffectTeam" : "Buffs Affect Team",
            "BuffsAffectPets" : "Buffs Affect Pets",
            "BuffPetsByName"  : "Buff Pets By Name",
        })

        for i in (1,2,3,4,5,6,7,8):
            ctrlName = f"Team{i}BuffKey"
            page.Init[ctrlName] = ""
            UI.Labels[ctrlName] = f'Team {i} Key'

        for i in (1,2,3,4,5,6):
            ctrlName = f"Pet{i}BuffKey"
            page.Init[ctrlName] = ""
            UI.Labels[ctrlName] = f'Pet {i} Key'

    def BuildBindUI(self, page):

        self.SetLabel(self.Title)
        pane = self.GetPane()

        # bind text controls
        BindSizer = wx.GridBagSizer(hgap=5, vgap=5)

        BindSizer.Add(wx.StaticText(pane, -1, "First Buff Power:"),    (0,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(PowerPicker(pane),                               (0,1), flag=wx.EXPAND     |wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.StaticText(pane, -1, "Extra:"),               (0,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        buffPower1 = wx.TextCtrl  (pane, -1, "")
        BindSizer.Add(buffPower1,                                      (0,3), flag=wx.EXPAND)
        BindSizer.Add(PowerBinderButton(pane, tgtTxtCtrl=buffPower1),  (0,4), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        page.Ctrls['BuffPower1'] = buffPower1

        BindSizer.Add(wx.StaticText(pane, -1, "Second Buff Power:"),   (1,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(PowerPicker(pane),                               (1,1), flag=wx.EXPAND     |wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.StaticText(pane, -1, "Extra:"),               (1,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        buffPower2 = wx.TextCtrl  (pane, -1, "")
        BindSizer.Add(buffPower2,                                      (1,3), flag=wx.EXPAND)
        BindSizer.Add(PowerBinderButton(pane, tgtTxtCtrl=buffPower2),  (1,4), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        page.Ctrls['BuffPower2'] = buffPower2

        BindSizer.Add(wx.StaticText(pane, -1, "Third Buff Power:"),    (2,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(PowerPicker(pane),                               (2,1), flag=wx.EXPAND     |wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(wx.StaticText(pane, -1, "Extra:"),               (2,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        buffPower3 = wx.TextCtrl  (pane, -1, "")
        BindSizer.Add(buffPower3,                                      (2,3), flag=wx.EXPAND)
        BindSizer.Add(PowerBinderButton(pane, tgtTxtCtrl=buffPower3),  (2,4), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        page.Ctrls['BuffPower3'] = buffPower3

        BindSizer.Add(wx.StaticText(pane, -1, ""),                    (3,0))


        # key picker controls
        KeySizer = wx.BoxSizer(wx.HORIZONTAL)
        TeamCtrls = ControlGroup(pane, self.Page, "Buff Team Keybinds")
        PetCtrls  = ControlGroup(pane, self.Page, "Buff Pet Keybinds")

        TeamCtrls.AddControl(ctlType = 'checkbox', ctlName = "BuffsAffectTeam")
        for i in (1,2,3,4,5,6,7,8):
            TeamCtrls.AddControl(
                ctlType = "keybutton",
                ctlName = f"Team{i}BuffKey",
                contents = ""
            )

        PetCtrls.AddControl(ctlType = 'checkbox', ctlName = "BuffsAffectPets")
        PetCtrls.AddControl(ctlType = "checkbox", ctlName = "BuffPetsByName")
        for i in (1,2,3,4,5,6):
            PetCtrls.AddControl(ctlType = "keybutton", ctlName = f"Pet{i}BuffKey", contents = "")

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



# This is the old lua logic for stuffing buffer binds, mashed to python but not reviewed at all
"""
        profile = self.Profile
        ResetFile = profile.ResetFile()

        buffer = self.GetState('buffer') or []

        for key in buffer:
            bbind = buffer['key']

            if bbind.get('selchatenabled', None):
                chat1 = cbPBindToString(bbind['chat1'])
                chat2 = cbPBindToString(bbind['chat2'])
                chat3 = cbPBindToString(bbind['chat3'])

            npow = 1
            if bbind.get('power2enabled', None):
                npow = 2
                if (bbind.get('power3enabled')): npow = 3

            if ((bbind['target'] == 1) or (bbind['target'] == 3)):
                for j in range(1,9):
                    teamid = "team"+j
                    filebase = f"{profile['base']}\\buff{i}\\bufft{j}"
                    afile = profile.GetBindFile(f"{filebase}a.txt")
                    bfile = profile.GetBindFile(f"{filebase}b.txt")
                    afile.SetBind(    teamid, f'+down$$teamselect {j}$${selchat}bindloadfile {filebase}b.txt')
                    ResetFile.SetBind(teamid, f'+down$$teamselect {j}$${selchat}bindloadfile {filebase}b.txt')
                    if (npow == 1):
                        bfile.SetBind(teamid,f'-down$${chat1}powexecname {bbind["power1"]}$$bindloadfile {filebase}a.txt')
                    else:
                        bfile.SetBind(teamid,f'-down$${chat1}powexecname {bbind["power1"]}$$bindloadfile {filebase}c.txt')
                        cfile = profile.GetBindFile(f"{filebase}c.txt")
                        if (npow == 2):
                            cfile.SetBind(teamid, f'{chat2}powexecname {bbind["power2"]}$$bindloadfile {filebase}a.txt')
                        else:
                            dfile = profile.GetBindFile(f"{filebase}d.txt")
                            cfile.SetBind(teamid, f'+down$${chat2}powexecname {bbind["power2"]}$$bindloadfile {filebase}d.txt')
                            dfile.SetBind(teamid, f'-down$${chat3}powexecname {bbind["power3"]}$$bindloadfile {filebase}a.txt')

            if ((bbind['target'] == 2) or (bbind['target'] == 3)):
                for j in range(1.7):
                    petid = "pet" + j
                    filebase = f"{profile['base']}\\buff{i}\\buffp{j}"
                    if (bbind['usepetnames']):
                        ResetFile.SetBind(petid, f'+down$$petselectname {profile["petaction"]}pet{j}name$${selchat}bindloadfile {filebase}b.txt')
                    else:
                        ResetFile.SetBind(petid, f'+down$$petselect {j-1}$${selchat}bindloadfile {filebase}b.txt')

                    afile = profile.GetBindFile(f"{filebase}a.txt")
                    bfile = profile.GetBindFile(f"{filebase}b.txt")
                    if (bbind['usepetnames']):
                        afile.SetBind(petid, f'+down$$petselectname {profile["petaction"]}pet{j}name$${selchat}bindloadfile {filebase}b.txt')
                    else:
                        afile.SetBind(petid, f'+down$$petselect {j-1}$${selchat}bindloadfile {filebase}b.txt')

                    if (npow == 1):
                        bfile.SetBind(petid, f'-down$${chat1}powexecname {bbind["power1"]}$$bindloadfile {filebase}a.txt')
                    else:
                        bfile.SetBind(petid, f'-down$${chat1}powexecname {bbind["power1"]}$$bindloadfile {filebase}c.txt')
                        cfile = profile.GetBindFile(f"{filebase}c.txt")
                        if (npow == 2):
                            cfile.SetBind(petid, f"{chat2}powexecname {bbind['power2']}$$bindloadfile {filebase}a.txt")
                        else:
                            dfile = profile.GetBindFile(f"{filebase}d.txt")
                            cfile.SetBind(petid, f'+down$${chat2}powexecname {bbind["power2"]}$$bindloadfile {filebase}d.txt')
                            dfile.SetBind(petid, f'-down$${chat3}powexecname {bbind["power3"]}$$bindloadfile {filebase}a.txt')
"""
