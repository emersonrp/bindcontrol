import wx
import Utility
import UI

from Page import Page
from Bind.BufferBind import BufferBind

class BufferBinds(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Binds = {}
        self.TabTitle = "Buffer Binds"

        # TODO - This init belongs in the actual bind class, but "self.Page.Init"
        # is hardwired into the innards of ControlGroup.  Hmmm.
        self.Init = {
            'BuffPetsByName' : True,
            'BuffsAffectTeam': True,
            'BuffsAffectPets': True,
        }
        for i in (1,2,3,4,5,6,7,8):
            self.Init[f"Team{i}BuffKey"] = "UNBOUND"
        for i in (1,2,3,4,5,6):
            self.Init[f"Pet{i}BuffKey"] = "UNBOUND"

    def BuildPage(self):
        profile = self.Profile

        self.MainSizer = wx.BoxSizer(wx.VERTICAL) # overall sizer
        self.PaneSizer = wx.BoxSizer(wx.VERTICAL) # sizer for collapsable panes
        buttonSizer    = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item button

        # Stick a button in the bottom sizer
        newBindButton = wx.Button(self, -1, "New Buffer Bind")
        newBindButton.Bind(wx.EVT_BUTTON, self.AddBindToPage)
        buttonSizer.Add(newBindButton, wx.ALIGN_CENTER)

        # Put blank space into PaneSizer so it expands self.PaneSizer.AddStretchSpacer()

        # add the two sub-sizers, top one expandable
        self.MainSizer.Add( self.PaneSizer, 1, wx.EXPAND|wx.ALL)
        self.MainSizer.Add( buttonSizer, 0, wx.EXPAND|wx.ALL)

        # sizer around the whole thing to add padding
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(self.MainSizer, 1, flag = wx.ALL|wx.EXPAND, border = 16)

        # Add any binds that came from a savefile
        for bind in self.Binds:
            bindCP = self.AddBindToPage(bind)

        self.SetSizerAndFit(paddingSizer)
        self.Layout()

    def AddBindToPage(self, _, bindinit = {}):

        bind = BufferBind(self, bindinit)

        # TODO - if bind is already in there, just scroll to it and pop it open
        bindCP = wx.CollapsiblePane(self, style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, bindCP)

        bind.BuildBindUI(bindCP)

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount() - 1, bindCP, 0, wx.ALL|wx.EXPAND, 10)
        self.Layout()

    def OnPaneChanged(self, event):
        self.Layout()

    def PopulateBindFiles(self):
        profile = self.Profile
        ResetFile = profile.ResetFile

        buffer = self.GetState('buffer')

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

    def findconflicts(self, profile):
        for bbind in self.GetState('bufferbinds'):
            title = bbind.get('title', "unknown")
            if ((bbind['target'] == 1) or (bbind['target'] == 3)):
                for j in range(1,9):
                    Utility.CheckConflict(bbind,"team"+j, f"Buff bind {title}: Team {j} Key")

            if ((bbind['target'] == 2) or (bbind['target'] == 3)):
                for j in range(1,7):
                    Utility.CheckConflict(bbind,"pet"+j, f"Buff bind {title}: Pet {j} Key")

    def bindisused(self, profile):
        return bool(len(self.buffer.keys()))

    for i in (1,2,3,4,5,6,7,8):
        UI.Labels[f'Team{i}BuffKey'] = f"Team {i} Key"

    for i in (1,2,3,4,5,6):
        UI.Labels[f'Pet{i}BuffKey'] = f"Pet {i} Key"

    UI.Labels.update( {
        'BuffPetsByName' : "Buff Pets using Pet Names",
        'BuffsAffectTeam' : "Buffs Affect Team Members",
        'BuffsAffectPets' : "Buffs Affect Pets",
    })

