import re
import wx
import UI
from Icon import GetIcon
from BLF import BLF
from UI.PowerPicker import PowerPicker

from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED
from UI.PowerBinderDialog import PowerBinderButton

class BufferBindPane(CustomBindPaneParent):
    def __init__(self, page, init = {}):
        CustomBindPaneParent.__init__(self, page, init)

        self.PassedInit = init

        self.Init = {
            'BuffChat1'       : '',
            'BuffChat2'       : '',
            'BuffChat3'       : '',
            'BuffPower1'      : {},
            'BuffPower2'      : {},
            'BuffPower3'      : {},
            'BuffsAffectTeam' : False,
            'BuffsAffectPets' : False,
        }
        for i in (1,2,3,4,5,6,7,8):
            self.Init[f'Team{i}BuffKey'] = ''
        for i in (1,2,3,4,5,6):
            self.Init[f'Pet{i}BuffKey'] = ''

    def BuildBindUI(self, page):
        pane = self.GetPane()
        pane.Page = page

        # Doing this UI here since we need Title to be set to get MakeCtlName right
        for i in (1,2,3,4,5,6,7,8):
            UI.Labels[self.MakeCtlName(f'Team{i}BuffKey')] = f'Team {i} Key'
        for i in (1,2,3,4,5,6):
            UI.Labels[self.MakeCtlName(f'Pet{i}BuffKey')] = f'Pet {i} Key'

        self.Init.update(self.PassedInit)

        # bind text controls
        BindSizer = wx.GridBagSizer(hgap=5, vgap=5)

        # on-select chat/emote
        selSizer = wx.BoxSizer(wx.HORIZONTAL)
        selchat = wx.TextCtrl(pane, -1, self.Init.get('SelectChat', ''))
        selchat.SetHint('Optional chat/emote command when selecting target')
        self.Ctrls[self.MakeCtlName('SelChat')] = selchat
        selSizer.Add(selchat, 1, wx.EXPAND|wx.RIGHT, 5)
        selSizer.Add(PowerBinderButton(pane, tgtTxtCtrl=selchat), 0, wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(selSizer, (0,0), (1,4), flag=wx.EXPAND)

        # Power 1
        buffChat1 = wx.TextCtrl(pane, -1, self.Init.get('BuffChat1', ''))
        buffChat1.SetHint('Optional chat/emote command when buffing')
        BindSizer.Add(buffChat1,                                     (1,0), flag=wx.EXPAND)
        BindSizer.Add(PowerBinderButton(pane, tgtTxtCtrl=buffChat1), (1,1), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[self.MakeCtlName('BuffChat1')] = buffChat1
        BindSizer.Add(wx.StaticText(pane, -1, "First Buff Power:"),  (1,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        buffPower1 = PowerPicker(pane)
        BindSizer.Add(buffPower1,                                    (1,3), flag=wx.EXPAND     |wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[self.MakeCtlName('BuffPower1')] = buffPower1
        bp1 = self.Init.get('BuffPower1', {})
        if bp1:
            if bp1['pname']: buffPower1.SetLabel(bp1['pname'])
            if bp1['picon']:
                buffPower1.SetBitmap(GetIcon(bp1['picon']))
                buffPower1.IconFilename = bp1['picon']

        # Power 2
        buffChat2 = wx.TextCtrl(pane, -1, self.Init.get('BuffChat2', ''))
        buffChat2.SetHint('Optional chat/emote command when buffing')
        BindSizer.Add(buffChat2,                                     (2,0), flag=wx.EXPAND)
        BindSizer.Add(PowerBinderButton(pane, tgtTxtCtrl=buffChat2), (2,1), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[self.MakeCtlName('BuffChat2')] = buffChat2
        BindSizer.Add(wx.StaticText(pane, -1, "Second Buff Power:"), (2,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        buffPower2 = PowerPicker(pane)
        bp2 = self.Init.get('BuffPower2', {})
        BindSizer.Add(buffPower2,                                    (2,3), flag=wx.EXPAND     |wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[self.MakeCtlName('BuffPower2')] = buffPower2
        if bp2:
            if bp2['pname']: buffPower2.SetLabel(bp2['pname'])
            if bp2['picon']:
                buffPower2.SetBitmap(GetIcon(bp2['picon']))
                buffPower2.IconFilename = bp2['picon']

        # Power 3
        buffChat3 = wx.TextCtrl(pane, -1, self.Init.get('BuffChat3', ''))
        buffChat3.SetHint('Optional chat/emote command when buffing')
        BindSizer.Add(buffChat3,                                     (3,0), flag=wx.EXPAND)
        BindSizer.Add(PowerBinderButton(pane, tgtTxtCtrl=buffChat3), (3,1), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[self.MakeCtlName('BuffChat3')] = buffChat3
        BindSizer.Add(wx.StaticText(pane, -1, "Third Buff Power:"),  (3,2), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        buffPower3 = PowerPicker(pane)
        bp3 = self.Init.get('BuffPower3', {})
        BindSizer.Add(buffPower3,                                    (3,3), flag=wx.EXPAND     |wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[self.MakeCtlName('BuffPower3')] = buffPower3
        if bp3:
            if bp3['pname']: buffPower3.SetLabel(bp3['pname'])
            if bp3['picon']:
                buffPower3.SetBitmap(GetIcon(bp3['picon']))
                buffPower3.IconFilename = bp3['picon']

        # key picker controls
        TeamCtrls = wx.StaticBoxSizer(wx.HORIZONTAL, pane, label = "Buff Team Keybinds")
        TeamInner = wx.GridBagSizer(hgap = 5, vgap = 5)
        TeamCtrls.Add(TeamInner, 1, wx.ALL|wx.EXPAND, 10)
        PetCtrls  = wx.StaticBoxSizer(wx.HORIZONTAL, pane, label = "Buff Pets Keybinds")
        PetInner = wx.GridBagSizer(hgap = 5, vgap = 5)
        PetCtrls.Add(PetInner, 1, wx.ALL|wx.EXPAND, 10)

        self.Ctrls[self.MakeCtlName('BuffsAffectTeam')] = wx.CheckBox(pane, -1, label = 'Enable')
        self.Ctrls[self.MakeCtlName('BuffsAffectTeam')].SetValue(self.Init['BuffsAffectTeam'])
        self.Ctrls[self.MakeCtlName('BuffsAffectTeam')].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        TeamInner.Add(self.Ctrls[self.MakeCtlName('BuffsAffectTeam')], (1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        for i in (1,2,3,4,5,6,7,8):
            button = bcKeyButton(pane, -1, init = { 'CtlName' : self.MakeCtlName(f'Team{i}BuffKey'), })
            button.Key = self.Init[f'Team{i}BuffKey']
            button.SetLabel(button.Key)
            label = wx.StaticText(pane, label = f'Teammate {i}')
            button.CtlLabel = label
            TeamInner.Add(label, (0,i), flag = wx.EXPAND|wx.ALIGN_CENTER)
            TeamInner.Add(button, (1,i))
            self.Ctrls[self.MakeCtlName(f'Team{i}BuffKey')] = button

        self.Ctrls[self.MakeCtlName('BuffsAffectPets')] = wx.CheckBox(pane, -1, label = 'Enable')
        self.Ctrls[self.MakeCtlName('BuffsAffectPets')].SetValue(self.Init['BuffsAffectPets'])
        self.Ctrls[self.MakeCtlName('BuffsAffectPets')].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        PetInner.Add(self.Ctrls[self.MakeCtlName('BuffsAffectPets')], (1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        for i in (1,2,3,4,5,6):
            button = bcKeyButton(pane, -1, init = { 'CtlName' : self.MakeCtlName(f'Pet{i}BuffKey'), })
            button.Key = self.Init[f'Pet{i}BuffKey']
            button.SetLabel(button.Key)
            label = wx.StaticText(pane, label = f'Pet {i}')
            button.CtlLabel = label
            PetInner.Add(label , (0,i), flag = wx.EXPAND|wx.ALIGN_CENTER)
            PetInner.Add(button, (1,i))
            self.Ctrls[self.MakeCtlName(f'Pet{i}BuffKey')] = button

        BindSizer.AddGrowableCol(0)
        BindSizer.AddGrowableCol(3)
        BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(BindSizer, 0, wx.EXPAND|wx.ALL, 10)
        border.Add(TeamCtrls, 0, wx.EXPAND|wx.ALL, 10)
        border.Add(PetCtrls,  0, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)
        self.SynchronizeUI()

    def PopulateBindFiles(self):
        profile = self.Profile
        ResetFile = profile.ResetFile()

        title = re.sub(r'\W+', '', self.Title)

        selchat = self.Ctrls[self.MakeCtlName('SelChat')]  .GetValue()
        chat1   = self.Ctrls[self.MakeCtlName('BuffChat1')].GetValue()
        chat2   = self.Ctrls[self.MakeCtlName('BuffChat2')].GetValue()
        chat3   = self.Ctrls[self.MakeCtlName('BuffChat3')].GetValue()

        npow = 1
        if self.Ctrls[self.MakeCtlName('BuffPower2')].GetLabel():
            npow = 2
            if self.Ctrls[self.MakeCtlName('BuffPower3')].GetLabel():
                npow = 3

        if self.Ctrls[self.MakeCtlName('BuffsAffectTeam')].GetValue():
            for j in [1,2,3,4,5,6,7,8]:
                teamkey = self.Ctrls[self.MakeCtlName(f"Team{j}BuffKey")].Key
                if not teamkey: continue
                filebase = profile.BindsDir()     / f"buff{title}" / f"bufft{j}"
                gamebase = profile.GameBindsDir() / f"buff{title}" / f"bufft{j}"
                afile = profile.GetBindFile(f"{filebase}a.txt")
                bfile = profile.GetBindFile(f"{filebase}b.txt")
                afile.SetBind(    teamkey, self.Page, self.Title, [f'teamselect {j}', selchat, f'{BLF()} {gamebase}b.txt'])
                ResetFile.SetBind(teamkey, self.Page, self.Title, [f'teamselect {j}', selchat, f'{BLF()} {gamebase}b.txt'])
                if (npow == 1):
                    bfile.SetBind(teamkey, self.Page, self.Title, [chat1, 'powexecname ', self.Ctrls[self.MakeCtlName("BuffPower1")].GetLabel(), f'{BLF()} {gamebase}a.txt'])
                else:
                    bfile.SetBind(teamkey, self.Page, self.Title, [chat1, f'powexecname ', self.Ctrls[self.MakeCtlName("BuffPower1")].GetLabel(), f'{BLF()} {gamebase}c.txt'])
                    cfile = profile.GetBindFile(f"{filebase}c.txt")
                    if (npow == 2):
                        cfile.SetBind(teamkey,  self.Page, self.Title, [chat2, f'powexecname ', self.Ctrls[self.MakeCtlName("BuffPower2")].GetLabel(), f'{BLF()} {gamebase}a.txt'])
                    else:
                        dfile = profile.GetBindFile(f"{filebase}d.txt")
                        cfile.SetBind(teamkey,  self.Page, self.Title, [chat2, f'powexecname ', self.Ctrls[self.MakeCtlName("BuffPower2")].GetLabel(), f'{BLF()} {gamebase}d.txt'])
                        dfile.SetBind(teamkey,  self.Page, self.Title, [chat3, f'powexecname ', self.Ctrls[self.MakeCtlName("BuffPower3")].GetLabel(), f'{BLF()} {gamebase}a.txt'])

        if self.Ctrls[self.MakeCtlName("BuffsAffectPets")].GetValue():
            for j in [1,2,3,4,5,6]:
                petkey = self.Ctrls[self.MakeCtlName(f"Pet{j}BuffKey")].Key
                if not petkey: continue
                filebase = profile.BindsDir()     / f"buff{title}" / f"buffp{j}"
                gamebase = profile.GameBindsDir() / f"buff{title}" / f"buffp{j}"
                afile = profile.GetBindFile(f"{filebase}a.txt")
                bfile = profile.GetBindFile(f"{filebase}b.txt")
                afile.SetBind    (petkey, self.Page, self.Title, [f'petselect {j-1}', selchat, f'{BLF()} {gamebase}b.txt'])
                ResetFile.SetBind(petkey, self.Page, self.Title, [f'petselect {j}'  , selchat, f'{BLF()} {gamebase}b.txt'])
                if (npow == 1):
                    bfile.SetBind(petkey, [chat1, f'powexecname ', self.Ctrls[self.MakeCtlName("BuffPower1")], f'{BLF()} {gamebase}a.txt'])
                else:
                    bfile.SetBind(petkey, [chat1, f'powexecname ', self.Ctrls[self.MakeCtlName("BuffPower1")], f'{BLF()} {gamebase}c.txt'])
                    cfile = profile.GetBindFile(f"{filebase}c.txt")
                    if (npow == 2):
                        cfile.SetBind(petkey, [f"{chat2}powexecname ", self.Ctrls[self.MakeCtlName("BuffPower2")], f"{BLF()} {gamebase}a.txt"])
                    else:
                        dfile = profile.GetBindFile(f"{filebase}d.txt")
                        cfile.SetBind(petkey, [chat2, f'powexecname ', self.Ctrls[self.MakeCtlName("BuffPower2")], f'{BLF()} {gamebase}d.txt'])
                        dfile.SetBind(petkey, [chat3, f'powexecname ', self.Ctrls[self.MakeCtlName("BuffPower3")], f'{BLF()} {gamebase}a.txt'])

    def SynchronizeUI(self, _ = None):
        useteam = self.Ctrls[self.MakeCtlName("BuffsAffectTeam")].GetValue()
        for i in [1,2,3,4,5,6,7,8]:
            self.Ctrls[self.MakeCtlName(f'Team{i}BuffKey')].Enable(useteam)
        usepet = self.Ctrls[self.MakeCtlName("BuffsAffectPets")].GetValue()
        for i in [1,2,3,4,5,6]:
            self.Ctrls[self.MakeCtlName(f'Pet{i}BuffKey')].Enable(usepet)

    def Serialize(self):
        data = {
            'Type'            : 'BufferBind',
            'Title'           : self.Title,
            "SelChat"         : self.Ctrls[self.MakeCtlName("SelChat")].GetValue(),
            "BuffChat1"       : self.Ctrls[self.MakeCtlName("BuffChat1")].GetValue(),
            "BuffChat2"       : self.Ctrls[self.MakeCtlName("BuffChat2")].GetValue(),
            "BuffChat3"       : self.Ctrls[self.MakeCtlName("BuffChat3")].GetValue(),
            "BuffsAffectTeam" : self.Ctrls[self.MakeCtlName("BuffsAffectTeam")].GetValue(),
            "BuffsAffectPets" : self.Ctrls[self.MakeCtlName("BuffsAffectPets")].GetValue(),
        }
        if self.Ctrls[self.MakeCtlName("BuffPower1")].GetLabel() != "...":
            data['BuffPower1'] = {
                'pname' : self.Ctrls[self.MakeCtlName("BuffPower1")].GetLabel(),
                'picon' : self.Ctrls[self.MakeCtlName("BuffPower1")].IconFilename,
            }
        if self.Ctrls[self.MakeCtlName("BuffPower2")].GetLabel() != "...":
            data['BuffPower2'] = {
                'pname' : self.Ctrls[self.MakeCtlName("BuffPower2")].GetLabel(),
                'picon' : self.Ctrls[self.MakeCtlName("BuffPower2")].IconFilename,
            }
        if self.Ctrls[self.MakeCtlName("BuffPower3")].GetLabel() != "...":
            data['BuffPower3'] = {
                'pname' : self.Ctrls[self.MakeCtlName("BuffPower3")].GetLabel(),
                'picon' : self.Ctrls[self.MakeCtlName("BuffPower3")].IconFilename,
            }
        for i in (1,2,3,4,5,6,7,8):
            data[f'Team{i}BuffKey'] = self.Ctrls[self.MakeCtlName(f'Team{i}BuffKey')].Key
        for i in (1,2,3,4,5,6):
            data[f'Pet{i}BuffKey']  = self.Ctrls[self.MakeCtlName(f'Pet{i}BuffKey')].Key

        return data
