import re
import wx
import UI
from Icon import GetIcon
from BLF import BLF
from UI.PowerPicker import PowerPicker, EVT_POWER_CHANGED

from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED

class BufferBindPane(CustomBindPaneParent):
    def __init__(self, page, init = {}):
        CustomBindPaneParent.__init__(self, page, init)

        self.PassedInit = init
        self.Description = "Buffer Bind"

        self.Init = {
            'SelChatTgt'      : 'team',
            'BuffChat1Tgt'    : 'team',
            'BuffChat2Tgt'    : 'team',
            'BuffChat3Tgt'    : 'team',
            'SelChat'         : '',
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
        setattr(pane, 'Page', page)

        # Doing this UI here since we need Title to be set to get MakeCtlName right
        for i in (1,2,3,4,5,6,7,8):
            UI.Labels[self.MakeCtlName(f'Team{i}BuffKey')] = f'Team {i} Key'
        for i in (1,2,3,4,5,6):
            UI.Labels[self.MakeCtlName(f'Pet{i}BuffKey')] = f'Pet {i} Key'

        self.Init.update(self.PassedInit)

        # bind text controls
        BindSizer = wx.GridBagSizer(hgap=5, vgap=5)

        ChatTargets = ['team', 'target', 'local']

        # on-select chat/emote
        selChatTxt = wx.StaticText(pane, label = 'On select, tell:')
        selChatTgt = wx.Choice(pane, choices = ChatTargets)
        selChatTgt.SetSelection(selChatTgt.FindString(self.Init.get('SelChatTgt', '')))
        self.Ctrls[self.MakeCtlName('SelChatTgt')] = selChatTgt
        selChat = wx.TextCtrl(pane, -1, self.Init.get('SelChat', ''))
        selChat.SetHint('Chat contents; leave blank to skip')
        self.Ctrls[self.MakeCtlName('SelChat')]    = selChat
        BindSizer.Add(selChatTxt, (0, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(selChatTgt, (0, 1))
        BindSizer.Add(selChat,    (0, 2), (1, 3), flag = wx.EXPAND)

        # Power 1
        buffChatTxt1 = wx.StaticText(pane, label = 'On buff, tell:')
        BindSizer.Add(buffChatTxt1,                                  (1,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        buffChat1Tgt = wx.Choice(pane, choices = ChatTargets)
        buffChat1Tgt.SetSelection(buffChat1Tgt.FindString(self.Init.get('BuffChat1Tgt', '')))
        BindSizer.Add(buffChat1Tgt,                                  (1,1), flag=wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[self.MakeCtlName('BuffChat1Tgt')] = buffChat1Tgt
        buffChat1 = wx.TextCtrl(pane, -1, self.Init.get('BuffChat1', ''))
        buffChat1.SetHint('Chat contents; leave blank to skip')
        BindSizer.Add(buffChat1,                                     (1,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.Ctrls[self.MakeCtlName('BuffChat1')]    = buffChat1
        BindSizer.Add(wx.StaticText(pane, -1, "First Buff Power:"),  (1,3), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        buffPower1 = PowerPicker(pane)
        BindSizer.Add(buffPower1,                                    (1,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.Ctrls[self.MakeCtlName('BuffPower1')] = buffPower1
        if bp1 := self.Init.get('BuffPower1', {}):
            if bp1.get('pname', ''): buffPower1.SetLabel(bp1['pname'])
            if bp1.get('picon', ''):
                buffPower1.SetBitmap(GetIcon(bp1['picon']))
                buffPower1.IconFilename = bp1['picon']

        # Power 2
        buffChatTxt2 = wx.StaticText(pane, label = 'On buff, tell:')
        BindSizer.Add(buffChatTxt2,                                  (2,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        buffChat2Tgt = wx.Choice(pane, choices = ChatTargets)
        buffChat2Tgt.SetSelection(buffChat2Tgt.FindString(self.Init.get('BuffChat2Tgt', '')))
        BindSizer.Add(buffChat2Tgt,                                  (2,1), flag=wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[self.MakeCtlName('BuffChat2Tgt')] = buffChat2Tgt
        buffChat2 = wx.TextCtrl(pane, -1, self.Init.get('BuffChat2', ''))
        buffChat2.SetHint('Chat contents; leave blank to skip')
        BindSizer.Add(buffChat2,                                     (2,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.Ctrls[self.MakeCtlName('BuffChat2')   ] = buffChat2
        BindSizer.Add(wx.StaticText(pane, -1, "Second Buff Power:"), (2,3), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        buffPower2 = PowerPicker(pane)
        BindSizer.Add(buffPower2,                                    (2,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.Ctrls[self.MakeCtlName('BuffPower2')] = buffPower2
        if bp2 := self.Init.get('BuffPower2', {}):
            if bp2.get('pname', ''): buffPower2.SetLabel(bp2['pname'])
            if bp2.get('picon', ''):
                buffPower2.SetBitmap(GetIcon(bp2['picon']))
                buffPower2.IconFilename = bp2['picon']

        # Power 3
        buffChatTxt3 = wx.StaticText(pane, label = 'On buff, tell:')
        BindSizer.Add(buffChatTxt3,                                  (3,0), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        buffChat3Tgt = wx.Choice(pane, choices = ChatTargets)
        buffChat3Tgt.SetSelection(buffChat3Tgt.FindString(self.Init.get('BuffChat3Tgt', '')))
        BindSizer.Add(buffChat3Tgt,                                  (3,1), flag=wx.ALIGN_CENTER_VERTICAL)
        self.Ctrls[self.MakeCtlName('BuffChat3Tgt')] = buffChat3Tgt
        buffChat3 = wx.TextCtrl(pane, -1, self.Init.get('BuffChat3', ''))
        buffChat3.SetHint('Chat contents; leave blank to skip')
        BindSizer.Add(buffChat3,                                     (3,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.Ctrls[self.MakeCtlName('BuffChat3')]    = buffChat3
        BindSizer.Add(wx.StaticText(pane, -1, "Third Buff Power:"),  (3,3), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        buffPower3 = PowerPicker(pane)
        BindSizer.Add(buffPower3,                                    (3,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.Ctrls[self.MakeCtlName('BuffPower3')] = buffPower3
        if bp3 := self.Init.get('BuffPower3', {}):
            if bp3.get('pname', ''): buffPower3.SetLabel(bp3['pname'])
            if bp3.get('picon', ''):
                buffPower3.SetBitmap(GetIcon(bp3['picon']))
                buffPower3.IconFilename = bp3['picon']

        buffPower1.Bind(EVT_POWER_CHANGED, self.CheckAnyPowerPicked)
        buffPower2.Bind(EVT_POWER_CHANGED, self.CheckAnyPowerPicked)
        buffPower3.Bind(EVT_POWER_CHANGED, self.CheckAnyPowerPicked)

        # key picker controls
        TeamCtrls = wx.StaticBoxSizer(wx.HORIZONTAL, pane, label = "Buff Team Keybinds")
        TeamSB = TeamCtrls.GetStaticBox()
        TeamInner = wx.GridBagSizer(hgap = 5, vgap = 5)
        TeamCtrls.Add(TeamInner, 1, wx.ALL|wx.EXPAND, 10)
        PetCtrls  = wx.StaticBoxSizer(wx.HORIZONTAL, pane, label = "Buff Pets Keybinds")
        PetSB = PetCtrls.GetStaticBox()
        PetInner = wx.GridBagSizer(hgap = 5, vgap = 5)
        PetCtrls.Add(PetInner, 1, wx.ALL|wx.EXPAND, 10)

        self.Ctrls[self.MakeCtlName('BuffsAffectTeam')] = wx.CheckBox(TeamSB, -1, label = 'Enable')
        self.Ctrls[self.MakeCtlName('BuffsAffectTeam')].SetValue(self.Init['BuffsAffectTeam'])
        self.Ctrls[self.MakeCtlName('BuffsAffectTeam')].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        TeamInner.Add(self.Ctrls[self.MakeCtlName('BuffsAffectTeam')], (1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        for i in (1,2,3,4,5,6,7,8):
            button = bcKeyButton(TeamSB, -1, init = { 'CtlName' : self.MakeCtlName(f'Team{i}BuffKey'), })
            button.Key = self.Init[f'Team{i}BuffKey']
            button.SetLabel(button.Key)
            button.Bind(EVT_KEY_CHANGED, self.CheckAnyKeyPicked)
            label = wx.StaticText(TeamSB, label = f'Teammate {i}')
            button.CtlLabel = label
            TeamInner.Add(label, (0,i), flag = wx.EXPAND|wx.ALIGN_CENTER)
            TeamInner.Add(button, (1,i))
            self.Ctrls[self.MakeCtlName(f'Team{i}BuffKey')] = button

        self.Ctrls[self.MakeCtlName('BuffsAffectPets')] = wx.CheckBox(PetSB, -1, label = 'Enable')
        self.Ctrls[self.MakeCtlName('BuffsAffectPets')].SetValue(self.Init['BuffsAffectPets'])
        self.Ctrls[self.MakeCtlName('BuffsAffectPets')].Bind(wx.EVT_CHECKBOX, self.SynchronizeUI)
        PetInner.Add(self.Ctrls[self.MakeCtlName('BuffsAffectPets')], (1,0), flag=wx.ALIGN_CENTER_VERTICAL)
        for i in (1,2,3,4,5,6):
            button = bcKeyButton(PetSB, -1, init = { 'CtlName' : self.MakeCtlName(f'Pet{i}BuffKey'), })
            button.Key = self.Init[f'Pet{i}BuffKey']
            button.SetLabel(button.Key)
            button.Bind(EVT_KEY_CHANGED, self.CheckAnyKeyPicked)
            label = wx.StaticText(PetSB, label = f'Pet {i}')
            button.CtlLabel = label
            PetInner.Add(label , (0,i), flag = wx.EXPAND|wx.ALIGN_CENTER)
            PetInner.Add(button, (1,i))
            self.Ctrls[self.MakeCtlName(f'Pet{i}BuffKey')] = button

        BindSizer.AddGrowableCol(2)
        BindSizer.AddGrowableCol(4)
        BindSizer.Layout()

        # border around the addr box
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(BindSizer, 0, wx.EXPAND|wx.ALL, 10)
        border.Add(TeamCtrls, 0, wx.EXPAND|wx.ALL, 10)
        border.Add(PetCtrls,  0, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)
        self.SynchronizeUI()

    def PopulateBindFiles(self):
        if not self.checkIfWellFormed():
            wx.MessageBox(f"Custom Bind \"{self.Title}\" is not complete or has errors.  Not written to bindfile.")
            return

        profile = self.Profile
        ResetFile = profile.ResetFile()

        title = re.sub(r'\W+', '', self.Title)

        BuffChats = {}

        for chat in ['SelChat', 'BuffChat1', 'BuffChat2', 'BuffChat3']:
            ctl = self.Ctrls[self.MakeCtlName(f'{chat}Tgt')]
            tgt = ctl.GetString(ctl.GetSelection())

            if tgt == 'team':
                verb = "g "
            elif tgt == 'target':
                verb = "tell $target, "
            else:
                verb = "local "

            BuffChats[chat] = verb + self.Ctrls[self.MakeCtlName(chat)].GetValue()

        npow = 0
        if self.Ctrls[self.MakeCtlName('BuffPower1')].HasPowerPicked():
            npow = 1
            if self.Ctrls[self.MakeCtlName('BuffPower2')].HasPowerPicked():
                npow = 2
                if self.Ctrls[self.MakeCtlName('BuffPower3')].HasPowerPicked():
                    npow = 3

        if self.Ctrls[self.MakeCtlName('BuffsAffectTeam')].GetValue():
            for j in [1,2,3,4,5,6,7,8]:
                teamkey = self.Ctrls[self.MakeCtlName(f"Team{j}BuffKey")].Key
                if not teamkey: continue
                filebase = profile.BindsDir()     / 'buff' / f"{title}_t{j}"
                gamebase = profile.GameBindsDir() / 'buff' / f"{title}_t{j}"
                afile = profile.GetBindFile(f"{filebase}a.txt")
                bfile = profile.GetBindFile(f"{filebase}b.txt")
                afile.SetBind(    teamkey, self.Page, self.Title, [f'teamselect {j}', BuffChats['SelChat'], f'{BLF()} {gamebase}b.txt'])
                ResetFile.SetBind(teamkey, self.Page, self.Title, [f'teamselect {j}', BuffChats['SelChat'], f'{BLF()} {gamebase}b.txt'])
                if (npow == 1):
                    bfile.SetBind(teamkey, self.Page, self.Title, [BuffChats['BuffChat1'], f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower1")].GetLabel()}', f'{BLF()} {gamebase}a.txt'])
                else:
                    bfile.SetBind(teamkey, self.Page, self.Title, [BuffChats['BuffChat1'], f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower1")].GetLabel()}', f'{BLF()} {gamebase}c.txt'])
                    cfile = profile.GetBindFile(f"{filebase}c.txt")
                    if (npow == 2):
                        cfile.SetBind(teamkey,  self.Page, self.Title, [BuffChats['BuffChat2'], f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower2")].GetLabel()}', f'{BLF()} {gamebase}a.txt'])
                    else:
                        dfile = profile.GetBindFile(f"{filebase}d.txt")
                        cfile.SetBind(teamkey,  self.Page, self.Title, [BuffChats['BuffChat2'], f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower2")].GetLabel()}', f'{BLF()} {gamebase}d.txt'])
                        dfile.SetBind(teamkey,  self.Page, self.Title, [BuffChats['BuffChat3'], f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower3")].GetLabel()}', f'{BLF()} {gamebase}a.txt'])

        # NB:  Don't use the BuffChats for the pet ones.  They're spammy, nobody cares, and /tell $target breaks.
        if self.Ctrls[self.MakeCtlName("BuffsAffectPets")].GetValue():
            for j in [1,2,3,4,5,6]:
                petkey = self.Ctrls[self.MakeCtlName(f"Pet{j}BuffKey")].Key
                if not petkey: continue
                filebase = profile.BindsDir()     / 'buff' / f"{title}_p{j}"
                gamebase = profile.GameBindsDir() / 'buff' / f"{title}_p{j}"
                afile = profile.GetBindFile(f"{filebase}a.txt")
                bfile = profile.GetBindFile(f"{filebase}b.txt")
                afile.SetBind    (petkey, self.Page, self.Title, [f'petselect {j-1}', f'{BLF()} {gamebase}b.txt'])
                ResetFile.SetBind(petkey, self.Page, self.Title, [f'petselect {j}'  , f'{BLF()} {gamebase}b.txt'])
                if (npow == 1):
                    bfile.SetBind(petkey, self.Page, self.Title, [f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower1")].GetLabel()}', f'{BLF()} {gamebase}a.txt'])
                else:
                    bfile.SetBind(petkey, self.Page, self.Title, [f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower1")].GetLabel()}', f'{BLF()} {gamebase}c.txt'])
                    cfile = profile.GetBindFile(f"{filebase}c.txt")
                    if (npow == 2):
                        cfile.SetBind(petkey, self.Page, self.Title, [f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower2")].GetLabel()}', f'{BLF()} {gamebase}a.txt'])
                    else:
                        dfile = profile.GetBindFile(f"{filebase}d.txt")
                        cfile.SetBind(petkey, self.Page, self.Title, [f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower2")].GetLabel()}', f'{BLF()} {gamebase}d.txt'])
                        dfile.SetBind(petkey, self.Page, self.Title, [f'powexecname {self.Ctrls[self.MakeCtlName("BuffPower3")].GetLabel()}', f'{BLF()} {gamebase}a.txt'])

    def SynchronizeUI(self, _ = None):
        useteam = self.Ctrls[self.MakeCtlName("BuffsAffectTeam")].GetValue()
        for i in [1,2,3,4,5,6,7,8]:
            self.Ctrls[self.MakeCtlName(f'Team{i}BuffKey')].Enable(useteam)

        usepet = self.Ctrls[self.MakeCtlName("BuffsAffectPets")].GetValue()
        for i in [1,2,3,4,5,6]:
            self.Ctrls[self.MakeCtlName(f'Pet{i}BuffKey')].Enable(usepet)

        self.CheckAnyPowerPicked()
        self.CheckAnyKeyPicked()

    def Serialize(self):
        data = {
            'Type'            : 'BufferBind',
            'Title'           : self.Title,
            "SelChatTgt"      : self.Ctrls[self.MakeCtlName('SelChatTgt')].GetString(self.Ctrls[self.MakeCtlName('SelChatTgt')].GetSelection()),
            "SelChat"         : self.Ctrls[self.MakeCtlName("SelChat")].GetValue(),
            "BuffChat1Tgt"    : self.Ctrls[self.MakeCtlName("BuffChat1Tgt")].GetString(self.Ctrls[self.MakeCtlName('BuffChat1Tgt')].GetSelection()),
            "BuffChat1"       : self.Ctrls[self.MakeCtlName("BuffChat1")].GetValue(),
            "BuffChat2Tgt"    : self.Ctrls[self.MakeCtlName("BuffChat2Tgt")].GetString(self.Ctrls[self.MakeCtlName('BuffChat2Tgt')].GetSelection()),
            "BuffChat2"       : self.Ctrls[self.MakeCtlName("BuffChat2")].GetValue(),
            "BuffChat3Tgt"    : self.Ctrls[self.MakeCtlName("BuffChat3Tgt")].GetString(self.Ctrls[self.MakeCtlName('BuffChat3Tgt')].GetSelection()),
            "BuffChat3"       : self.Ctrls[self.MakeCtlName("BuffChat3")].GetValue(),
            "BuffsAffectTeam" : self.Ctrls[self.MakeCtlName("BuffsAffectTeam")].GetValue(),
            "BuffsAffectPets" : self.Ctrls[self.MakeCtlName("BuffsAffectPets")].GetValue(),
        }
        if self.Ctrls[self.MakeCtlName("BuffPower1")].HasPowerPicked():
            data['BuffPower1'] = {
                'pname' : self.Ctrls[self.MakeCtlName("BuffPower1")].GetLabel(),
                'picon' : self.Ctrls[self.MakeCtlName("BuffPower1")].IconFilename,
            }
        if self.Ctrls[self.MakeCtlName("BuffPower2")].HasPowerPicked():
            data['BuffPower2'] = {
                'pname' : self.Ctrls[self.MakeCtlName("BuffPower2")].GetLabel(),
                'picon' : self.Ctrls[self.MakeCtlName("BuffPower2")].IconFilename,
            }
        if self.Ctrls[self.MakeCtlName("BuffPower3")].HasPowerPicked():
            data['BuffPower3'] = {
                'pname' : self.Ctrls[self.MakeCtlName("BuffPower3")].GetLabel(),
                'picon' : self.Ctrls[self.MakeCtlName("BuffPower3")].IconFilename,
            }
        for i in (1,2,3,4,5,6,7,8):
            data[f'Team{i}BuffKey'] = self.Ctrls[self.MakeCtlName(f'Team{i}BuffKey')].Key
        for i in (1,2,3,4,5,6):
            data[f'Pet{i}BuffKey']  = self.Ctrls[self.MakeCtlName(f'Pet{i}BuffKey')].Key

        return data

    def AllBindFiles(self):
        files = []
        title = re.sub(r'\W+', '', self.Title)
        for j in [1,2,3,4,5,6,7,8]:
            filebase = self.Profile.BindsDir() / f"buff{title}" / f"bufft{j}"
            for k in ['a','b','c','d']:
                files.append(self.Profile.GetBindFile(f"{filebase}{k}.txt"))

        for j in [1,2,3,4,5,6]:
            filebase = self.Profile.BindsDir() / f"buff{title}" / f"buffp{j}"
            for k in ['a','b','c','d']:
                files.append(self.Profile.GetBindFile(f"{filebase}{k}.txt"))

        return {
            'files' : files,
            'dirs'  : [f"buff{title}"],
        }

    def checkIfWellFormed(self):
        return self.CheckAnyKeyPicked() and self.CheckAnyPowerPicked()

    def CheckAnyKeyPicked(self, _ = None):
        KeyIsPicked = False
        for i in (1,2,3,4,5,6,7,8):
            if self.Ctrls[self.MakeCtlName(f'Team{i}BuffKey')].Key:
                KeyIsPicked = True
        for i in (1,2,3,4,5,6):
            if self.Ctrls[self.MakeCtlName(f'Pet{i}BuffKey')].Key:
                KeyIsPicked = True

        Team1Button = self.Ctrls[self.MakeCtlName(f'Team1BuffKey')]
        if KeyIsPicked:
            Team1Button.RemoveError('undef')
        else:
            Team1Button.AddError('undef', 'At least one Team or Pet key must be selected.')

        return KeyIsPicked

    def CheckAnyPowerPicked(self, _ = None):
        bp1 = self.Ctrls[self.MakeCtlName("BuffPower1")]
        bp2 = self.Ctrls[self.MakeCtlName("BuffPower2")]
        bp3 = self.Ctrls[self.MakeCtlName("BuffPower3")]

        if (bp1.HasPowerPicked() or bp2.HasPowerPicked() or bp3.HasPowerPicked()):
            self.Ctrls[self.MakeCtlName("BuffPower1")].RemoveError('nopower')
            return True
        else:
            self.Ctrls[self.MakeCtlName("BuffPower1")].AddError('nopower', 'At least one power must be selected')
            return False
