import re
import wx
import UI
from BLF import BLF
from Icon import GetIcon
from UI.PowerPicker import PowerPicker, EVT_POWER_CHANGED

from UI.CustomBindPaneParent import CustomBindPaneParent
from UI.KeySelectDialog import bcKeyButton, EVT_KEY_CHANGED

ChatTargets = ['team', 'target', 'local']

class BufferBindPane(CustomBindPaneParent):
    def __init__(self, page, init = {}):
        CustomBindPaneParent.__init__(self, page, init)

        self.PassedInit = init
        self.Description = "Buffer Bind"

        self.Buffs = []

        self.Init = {
            'SelChatTgt'      : 'team',
            'SelChat'         : '',
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

        # TODO:  why do I do this here instead of in __init__?  Must have been a reason.
        self.Init.update(self.PassedInit)

        # bind text controls
        # TODO this doesn't need to be a Gridbag any more.  Just BoxSizer it.
        BindSizer = wx.GridBagSizer(hgap=5, vgap=5)

        # on-select chat/emote
        selChatTxt = wx.StaticText(pane, label = 'On select, tell:')

        self.SelChatTgt = wx.Choice(pane, choices = ChatTargets)
        self.SelChatTgt.SetSelection(self.SelChatTgt.FindString(self.Init.get('SelChatTgt', '')))
        self.Ctrls[self.MakeCtlName('SelChatTgt')] = self.SelChatTgt

        self.SelChat = wx.TextCtrl(pane, -1, self.Init.get('SelChat', ''))
        self.SelChat.SetHint('/tell contents; leave blank to skip')
        self.Ctrls[self.MakeCtlName('SelChat')] = self.SelChat

        BindSizer.Add(selChatTxt,      (0, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        BindSizer.Add(self.SelChatTgt, (0, 1))
        BindSizer.Add(self.SelChat,    (0, 2), (1, 3), flag = wx.EXPAND)

        self.BuffSizer = wx.BoxSizer(wx.VERTICAL)
        if self.Init.get('Buffs', ''):
            for buff in self.Init['Buffs']:
                self.OnAddBuffButton(None, buff)
        else:
            self.OnAddBuffButton()

        AddBindsButton = wx.Button(pane, label = "Add Buff")
        AddBindsButton.Bind(wx.EVT_BUTTON, self.OnAddBuffButton)

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
        border.Add(BindSizer     , 0, wx.EXPAND|wx.ALL, 10)
        border.Add(self.BuffSizer, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 10)
        border.Add(AddBindsButton, 0, wx.ALL, 5)
        border.Add(TeamCtrls     , 0, wx.EXPAND|wx.ALL, 10)
        border.Add(PetCtrls      , 0, wx.EXPAND|wx.ALL, 10)
        pane.SetSizer(border)
        self.SynchronizeUI()

    def OnAddBuffButton(self, evt = None, buff = {}):
        if evt: evt.Skip()
        newBuff = Buff(self, buff)
        self.Buffs.append(newBuff)
        self.BuffSizer.Add(newBuff, flag=wx.EXPAND)
        # don't SynchronizeUI in here, as we do this before the full page is built
        self.Page.Layout()

    def OnDelBuffButton(self, evt):
        evt.Skip()
        button = evt.GetEventObject()
        buff = button.GetParent()
        self.Buffs.remove(buff)
        buff.GetContainingSizer().Detach(buff)
        buff.DestroyLater()
        self.Profile.SetModified()
        self.Parent.Layout()
        wx.CallAfter(self.Page.SynchronizeUI)

    def PopulateBindFiles(self):
        if not self.checkIfWellFormed():
            wx.MessageBox(f'Buffer Bind "{self.Title}" is not complete or has errors.  Not written to bindfile.')
            return

        profile = self.Profile
        ResetFile = profile.ResetFile()

        title = re.sub(r'\W+', '', self.Title)

        BuffChats = {}

        # TODO:  DRY up the next two bits eventually
        ctl = self.SelChatTgt
        tgt = ctl.GetString(ctl.GetSelection())

        if tgt == 'team':
            verb = "g "
        elif tgt == 'target':
            verb = "tell $target, "
        else:
            verb = "local "

        BuffChats['SelChat'] = verb + self.SelChat.GetValue()

        for i, b in enumerate(self.Buffs, start = 2): # select is step i, buffs 2..x
            tgt = b.ChatTgt.GetString(b.ChatTgt.GetSelection())
            if tgt == 'team':
                verb = "g "
            elif tgt == 'target':
                verb = "tell $target, "
            else:
                verb = "local "

            BuffChats[f'Buff{i}'] = verb + b.Chat.GetValue()

        if self.Ctrls[self.MakeCtlName('BuffsAffectTeam')].GetValue():
            for j in [1,2,3,4,5,6,7,8]:
                teamkey = self.Ctrls[self.MakeCtlName(f"Team{j}BuffKey")].Key
                if not teamkey: continue
                filebase = profile.BindsDir()     / 'buff' / f"{title}_t{j}"
                gamebase = profile.GameBindsDir() / 'buff' / f"{title}_t{j}"

                outfiles = {}
                outfiles[1] = profile.GetBindFile(f"{filebase}1.txt")

                outfiles[1].SetBind(teamkey, self.Page, self.Title, [f'teamselect {j}', BuffChats['SelChat'], f'{BLF()} {gamebase}2.txt'])
                ResetFile  .SetBind(teamkey, self.Page, self.Title, [f'teamselect {j}', BuffChats['SelChat'], f'{BLF()} {gamebase}2.txt'])

                for i, b in enumerate(self.Buffs, start = 2): # number the binds as steps 2..x
                    outfiles[i] = profile.GetBindFile(f"{filebase}{i}.txt")
                    if i == len(self.Buffs)+1:  # on the last one, back to step 1
                        outfiles[i].SetBind(teamkey, self.Page, self.Title, [BuffChats[f'Buff{i}'], f'powexecname {b.BuffPower.GetLabel()}', f'{BLF()} {gamebase}1.txt'])
                    else:
                        outfiles[i].SetBind(teamkey, self.Page, self.Title, [BuffChats[f'Buff{i}'], f'powexecname {b.BuffPower.GetLabel()}', f'{BLF()} {gamebase}{i+1}.txt'])

        # NB:  Don't use the BuffChats for the pet ones.  They're spammy, nobody cares, and /tell $target breaks.
        if self.Ctrls[self.MakeCtlName("BuffsAffectPets")].GetValue():
            for j in [1,2,3,4,5,6]:
                petkey = self.Ctrls[self.MakeCtlName(f"Pet{j}BuffKey")].Key
                if not petkey: continue
                filebase = profile.BindsDir()     / 'buff' / f"{title}_p{j}"
                gamebase = profile.GameBindsDir() / 'buff' / f"{title}_p{j}"

                outfiles = {}
                outfiles[1] = profile.GetBindFile(f"{filebase}1.txt")

                outfiles[1].SetBind(petkey, self.Page, self.Title, [f'petselect 1', f'{BLF()} {gamebase}2.txt'])
                ResetFile  .SetBind(petkey, self.Page, self.Title, [f'petselect 1', f'{BLF()} {gamebase}2.txt'])

                for i, b in enumerate(self.Buffs, start = 2): # number the binds as steps 2..x
                    outfiles[i] = profile.GetBindFile(f"{filebase}{i}.txt")
                    if i == len(self.Buffs)+1:  # on the last one, back to step 1
                        outfiles[i].SetBind(petkey, self.Page, self.Title, [f'powexecname {b.BuffPower.GetLabel()}', f'{BLF()} {gamebase}1.txt'])
                    else:
                        outfiles[i].SetBind(petkey, self.Page, self.Title, [f'powexecname {b.BuffPower.GetLabel()}', f'{BLF()} {gamebase}{i+i}.txt'])

    def SynchronizeUI(self, _ = None):

        for i, b in enumerate(self.Buffs):
            b.delButton.Show(i > 0)

        useteam = self.Ctrls[self.MakeCtlName("BuffsAffectTeam")].GetValue()
        for i in [1,2,3,4,5,6,7,8]:
            self.Ctrls[self.MakeCtlName(f'Team{i}BuffKey')].Enable(useteam)

        usepet = self.Ctrls[self.MakeCtlName("BuffsAffectPets")].GetValue()
        for i in [1,2,3,4,5,6]:
            self.Ctrls[self.MakeCtlName(f'Pet{i}BuffKey')].Enable(usepet)

        self.CheckAnyKeyPicked()
        self.Page.Layout()

    def Serialize(self):
        data = {
            'Type'            : 'BufferBind',
            'Title'           : self.Title,
            "SelChatTgt"      : self.SelChatTgt.GetString(self.SelChatTgt.GetSelection()),
            "SelChat"         : self.SelChat.GetValue(),
            "BuffsAffectTeam" : self.Ctrls[self.MakeCtlName('BuffsAffectTeam')].GetValue(),
            "BuffsAffectPets" : self.Ctrls[self.MakeCtlName('BuffsAffectPets')].GetValue(),
        }
        buffs = []
        for b in self.Buffs:
            buffs.append({
                'ChatTgt' : b.ChatTgt.GetString(b.ChatTgt.GetSelection()),
                'Chat'    : b.Chat.GetValue(),
                'Power'   : {
                    'pname' : b.BuffPower.GetLabel(),
                    'picon' : b.BuffPower.IconFilename,
                },
            })
        data['Buffs'] = buffs

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
        return self.CheckAnyKeyPicked()

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

class Buff(wx.Panel):
    def __init__(self, parent, buff = {}):
        self.Page = parent.Page
        pane = parent.GetPane()

        super().__init__(pane)

        buffSizer = wx.BoxSizer(wx.HORIZONTAL)
        buffChatTxt = wx.StaticText(self, label = 'On buff, tell:')
        buffSizer.Add(buffChatTxt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.ChatTgt = wx.Choice(self, choices = ChatTargets)
        self.ChatTgt.SetSelection(self.ChatTgt.FindString(buff.get('ChatTgt', 'team')))
        buffSizer.Add(self.ChatTgt, 0, wx.ALIGN_CENTER_VERTICAL)
        self.Chat = wx.TextCtrl(self, value = buff.get('Chat', ''))
        self.Chat.SetHint('/tell contents; leave blank to skip')
        buffSizer.Add(self.Chat, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        buffSizer.Add(wx.StaticText(self, label = "Buff Power:"), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.BuffPower = PowerPicker(self)
        buffSizer.Add(self.BuffPower, 1, wx.ALIGN_CENTER_VERTICAL)
        self.BuffPower.SetLabel(buff.get('Power', {}).get('pname', ''))
        if icon := buff.get('Power', {}).get('picon', ''):
            self.BuffPower.SetBitmap(GetIcon(icon))
            self.BuffPower.IconFilename = icon
        self.BuffPower.Bind(EVT_POWER_CHANGED, self.OnPowerPicked)

        self.delButton = wx.Button(self, -1, "X", size = wx.Size(40,-1))
        self.delButton.SetForegroundColour(wx.RED)
        self.delButton.Bind(wx.EVT_BUTTON, parent.OnDelBuffButton)
        buffSizer.Add(self.delButton, 0, flag = wx.RESERVE_SPACE_EVEN_IF_HIDDEN|wx.ALIGN_CENTER_VERTICAL)

        self.OnPowerPicked()
        self.SetSizerAndFit(buffSizer)

    def OnPowerPicked(self, _ = None):
        if self.BuffPower.HasPowerPicked():
            self.BuffPower.RemoveError("nopick")
        else:
            self.BuffPower.AddError("nopick", "No power has been picked")

