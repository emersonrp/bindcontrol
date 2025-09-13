# UI / logic for the 'general' panel
import wx
import wx.adv
import wx.lib.stattext as ST
from typing import Dict, Any
import UI
import Profile
from Icon import GetIconBitmap
import GameData

from UI.ControlGroup import ControlGroup

from Page import Page

class General(Page):
    def __init__(self, parent):
        super().__init__(parent)

        self.Init : Dict[str, Any] = {
            'Alignment' : 'Hero',
            'Origin'    : "Magic",
            'Archetype' : 'Mastermind',
            'Primary'   : '',
            'Secondary' : '',
            'Epic'      : '',
            'Pool1'     : '',
            'Pool2'     : '',
            'Pool3'     : '',
            'Pool4'     : '',

            'ChatEnable' : False,
            'StartChat'  : 'ENTER',
            'SlashChat'  : '/',
            'StartEmote' : ';',
            'AutoReply'  : 'BACKSPACE',
            'TellLast'   : 'SHIFT+BACKSPACE',
            'TellTarget' : 'COMMA',
            'QuickChat'  : "'",

            'TypingNotifierEnable' : False,
            'TypingNotifier'       : 'typing',

            'QuitToDesktop'   : '',
            'QuitToLogin'     : '',
            'QuitToSelect'    : '',
            'Sync'            : '',

            'ToggleRP'        : '',
            'HelpHelpMe'      : '',
            'HelpMentor'      : '',
            'HelpOff'         : '',

            'InviteTarget'    : '',
            'SGInviteTarget'  : '',
            'FriendTarget'    : '',
            'GFriendTarget'   : '',
            'IgnoreTarget'    : '',
            'UnignoreTarget'  : '',
        }

    def BuildPage(self):

        self.bannerPanel = wx.Panel(self)
        bannerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bannerPanel.SetSizer(bannerSizer)

        alignPicker = wx.adv.BitmapComboBox(self.bannerPanel, style = wx.CB_READONLY, choices = [''])
        alignPicker.Clear()
        for a in GameData.Alignments:
            alignPicker.Append(a, GetIconBitmap('Alignments', a))
        self.Ctrls['Alignment'] = alignPicker
        alignPicker.SetSelection(alignPicker.FindString(self.Init['Alignment']))
        alignPicker.Bind(wx.EVT_COMBOBOX, self.OnPickAlignment)
        bannerSizer.Add(alignPicker, 1, wx.EXPAND|wx.ALL, 5)

        originPicker = wx.adv.BitmapComboBox(self.bannerPanel, style = wx.CB_READONLY, choices = [''])
        originPicker.Clear()
        for o in GameData.Origins:
            originPicker.Append(o, GetIconBitmap('Origins', o))
        self.Ctrls['Origin'] = originPicker
        originPicker.Bind(wx.EVT_COMBOBOX, self.OnPickOrigin)
        bannerSizer.Add(originPicker, 1, wx.EXPAND|wx.ALL, 5)

        self.nameBox = wx.Panel(self.bannerPanel)
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.nameBox.SetSizer(nameSizer)
        self.NameDisplay = ST.GenStaticText(self.nameBox, -1, "", style=wx.ALIGN_CENTER|wx.ST_NO_AUTORESIZE)
        self.NameDisplay.SetFont(wx.Font(wx.FontInfo().Bold()))
        nameSizer.Add(self.NameDisplay, 1, wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 6)
        bannerSizer.Add(self.nameBox, 1, wx.EXPAND|wx.ALL, 5)

        archetypePicker = wx.adv.BitmapComboBox(self.bannerPanel, style = wx.CB_READONLY, choices = [''])
        archetypePicker.Clear()
        for a in GameData.Archetypes:
            archetypePicker.Append(a, GetIconBitmap('Archetypes', a))
        self.Ctrls['Archetype'] = archetypePicker
        archetypePicker.Bind(wx.EVT_COMBOBOX, self.OnPickArchetype)
        bannerSizer.Add(archetypePicker, 1, wx.EXPAND|wx.ALL, 5)

        self.ServerPicker = wx.adv.BitmapComboBox(self.bannerPanel, style = wx.CB_READONLY, choices = [''])
        self.ServerPicker.Clear()
        for s in ['Homecoming', 'Rebirth']:
            self.ServerPicker.Append(s, GetIconBitmap('Servers', s))
        self.Ctrls['Server'] = self.ServerPicker
        self.ServerPicker.Bind(wx.EVT_COMBOBOX, self.OnServerChange)
        bannerSizer.Add(self.ServerPicker, 1, wx.EXPAND|wx.ALL, 5)

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        powersBox = ControlGroup(self, self, 'Powers')

        powersBox.AddControl(
            ctlName = 'Primary',
            ctlType = 'choice',
            callback = self.OnPickPrimaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Secondary',
            ctlType = 'choice',
            callback = self.OnPickSecondaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Epic',
            ctlType = 'choice',
            callback = self.OnPickEpicPowerSet,
        )
        poolcontents = sorted(GameData.PoolPowers)
        poolcontents.insert(0, '')
        powersBox.AddControl(
            ctlName = 'Pool1',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool2',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool3',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )
        powersBox.AddControl(
            ctlName = 'Pool4',
            ctlType = 'choice',
            contents = poolcontents,
            callback = self.OnPickPoolPower,
        )

        ## Typing Notifier
        TNPanel = wx.Panel(self)
        TNSizer = wx.BoxSizer(wx.HORIZONTAL)

        TNEnable = wx.CheckBox(TNPanel, -1, 'Use Typing Notifier')
        TNEnable.SetToolTip('Check this to enable a floating notifier when you are typing into the chat box')
        setattr(TNEnable, 'CtlName', 'TypingNotifierEnable')
        TNEnable.Bind(wx.EVT_CHECKBOX, self.OnTypeEnable)
        self.Ctrls['TypingNotifierEnable'] = TNEnable

        TN = wx.TextCtrl(TNPanel, value = self.Init['TypingNotifier'], style = wx.TE_CENTER)
        TN.SetToolTip('The contents of the notifier that will float over your head as you type')
        TN.SetHint('typing notifier contents')
        setattr(TN, 'CtlName', 'TypingNotifier')
        self.Ctrls['TypingNotifier'] = TN

        TNSizer.Add(TNEnable, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        TNSizer.Add(TN,       1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        TNPanel.SetSizer(TNSizer)

        ### Chat binds
        chatBindBox = ControlGroup(self, self, 'Chat Binds', topcontent = TNPanel)

        for b in (
                # ['StartChat',  'Activates the Chat bar with notifier and custom colors if selected'],
            ['StartChat',  'Activates the Chat bar with notifier if selected'],
            ['SlashChat',  'Activates the Chat bar with notifier and a slash already typed'],
            ['StartEmote', 'Activates the Chat bar with notifier and "/em" already typed'],
            ['AutoReply',  'AutoReplies to incoming tells with notifier'],
            ['TellLast',   'Starts a /tell to the last player you sent a /tell, with notifier'],
            ['TellTarget', 'Starts a /tell to your current target with notifier'],
            ['QuickChat',  'Pops up QuickChat menu, with notifier'],
        ):
            chatBindBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        ClientSizer = ControlGroup(self, self, 'Game Client Binds')
        for b in (
            ['QuitToSelect'    , 'Choose the key that will quit to the character select screen'],
            ['QuitToLogin'     , 'Choose the key that will quit to the login screen'],
            ['QuitToDesktop'   , 'Choose the key that will quit directly to the desktop']  ,
            ['Sync'            , 'Choose the key that will attempt to sync with the game server'],
        ):
            ClientSizer.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        StatusSizer = ControlGroup(self, self, 'Character Status Binds')
        for b in (
             ['ToggleRP'        , 'Choose the key that will toggle your "Roleplaying" status / tag / name block' ],
             ['HelpHelpMe'      , 'Choose the key that will set Help status to "Help Me"'],
             ['HelpMentor'      , 'Choose the key that will set Help status to "Mentor"'],
             ['HelpOff'         , 'Choose the key that will turn off Help status'],
        ):
            StatusSizer.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        SocialSizer = ControlGroup(self, self, 'Social Binds')
        for b in (
            ['InviteTarget'    , 'Choose the key that will invite your target to a group'] ,
            ['SGInviteTarget'  , 'Choose the key that will invite your target to your supergroup'] ,
            ['FriendTarget'    , 'Choose the key that will add your target to your friends list'],
            ['GFriendTarget'   , 'Choose the key that will add your target to your global friends list'],
            ['IgnoreTarget'    , 'Choose the key that will ignore your current target'],
            ['UnignoreTarget'  , 'Choose the key that will unignore your current target'],
        ):
            SocialSizer.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )

        topSizer.Add(powersBox, 1, wx.EXPAND|wx.RIGHT, 10)
        topSizer.Add(chatBindBox, 1, wx.EXPAND)

        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.Add(ClientSizer, 1, wx.EXPAND|wx.RIGHT, 10)
        bottomSizer.Add(StatusSizer, 1, wx.EXPAND|wx.RIGHT, 10)
        bottomSizer.Add(SocialSizer, 1, wx.EXPAND)

        centeringSizer  = wx.BoxSizer(wx.VERTICAL)
        centeringSizer.Add(self.bannerPanel, 0, wx.EXPAND|wx.BOTTOM, 10)
        centeringSizer.Add(topSizer,         0, wx.EXPAND)
        centeringSizer.Add(bottomSizer,      0, wx.EXPAND|wx.TOP, 10)

        self.MainSizer.Add(centeringSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0)

    def SynchronizeUI(self):
        self.OnPickAlignment()
        self.OnPickOrigin()
        self.OnPickArchetype()
        self.OnTypeEnable()
        self.ValidateServerPicker()

    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile()

        notifier = ''
        if self.GetState('TypingNotifierEnable'):
            notifier = 'afk ' + self.GetState('TypingNotifier')

        ResetFile.SetBind(self.Ctrls['StartChat'] .MakeBind([notifier, 'show chat', 'startchat']))
        ResetFile.SetBind(self.Ctrls['SlashChat'] .MakeBind([notifier, 'show chat', 'slashchat']))
        ResetFile.SetBind(self.Ctrls['StartEmote'].MakeBind([notifier, 'show chat', 'beginchat /em ']))
        ResetFile.SetBind(self.Ctrls['AutoReply'] .MakeBind([notifier, 'autoreply']))
        ResetFile.SetBind(self.Ctrls['TellLast']  .MakeBind([notifier, 'show chat', 'beginchat /tl ']))
        ResetFile.SetBind(self.Ctrls['TellTarget'].MakeBind([notifier, 'show chat', 'beginchat /tell $target, ']))
        ResetFile.SetBind(self.Ctrls['QuickChat'] .MakeBind([notifier, 'quickchat']))

        ### Helpful Binds
        ResetFile.SetBind(self.Ctrls['QuitToSelect'] .MakeBind('quittocharacterselect'))
        ResetFile.SetBind(self.Ctrls['QuitToLogin']  .MakeBind('quittologin'))
        ResetFile.SetBind(self.Ctrls['QuitToDesktop'].MakeBind('quit'))
        ResetFile.SetBind(self.Ctrls['Sync']         .MakeBind('sync'))

        ResetFile.SetBind(self.Ctrls['ToggleRP']  .MakeBind('roleplaying'))
        ResetFile.SetBind(self.Ctrls['HelpHelpMe'].MakeBind('sethelperstatus 1'))
        ResetFile.SetBind(self.Ctrls['HelpMentor'].MakeBind('sethelperstatus 2'))
        ResetFile.SetBind(self.Ctrls['HelpOff']   .MakeBind('sethelperstatus 3'))

        ResetFile.SetBind(self.Ctrls['InviteTarget']  .MakeBind('i $target'))
        ResetFile.SetBind(self.Ctrls['SGInviteTarget'].MakeBind('sgi $target'))
        ResetFile.SetBind(self.Ctrls['FriendTarget']  .MakeBind('friend $target'))
        ResetFile.SetBind(self.Ctrls['GFriendTarget'] .MakeBind('gfriend $target'))
        ResetFile.SetBind(self.Ctrls['IgnoreTarget']  .MakeBind('ignore $target'))
        ResetFile.SetBind(self.Ctrls['UnignoreTarget'].MakeBind('unignore $target'))

        return True

    # we only fiddle with ResetFile, which is already taken care of.
    def AllBindFiles(self):
        return {
            'files' : [],
            'dirs'  : [],
        }

    ### EVENT HANDLERS
    def OnPickAlignment(self, evt = None):
        alignment = self.GetState('Alignment')
        if not alignment:
            alignment = 'Hero'
            self.SetState('Alignment', 'Hero')

        # TODO put this in Gamedata?
        bgcolor = wx.Colour({
            'Hero'       : ( 35, 130, 212),
            'Villain'    : (225,  65,  65),
            'Vigilante'  : (241, 213, 114),
            'Rogue'      : (180, 180, 180),
            'Resistance' : ( 30, 240, 255),
            'Loyalist'   : (255, 226,  56),
        }[alignment])
        self.bannerPanel.SetBackgroundColour(bgcolor)
        self.NameDisplay.SetBackgroundColour(bgcolor)
        # Have to do this dance to make the colors refresh on Windows.  Ugh.
        self.nameBox.Show(False)
        self.nameBox.Show(True)
        self.bannerPanel.Show(False)
        self.bannerPanel.Show(True)

        if evt: evt.Skip()

    def OnPickArchetype(self, evt = None):
        arch = self.GetState('Archetype')

        if not arch:
            # We somehow have some code path that ends up here without arch set, so
            # default to "Blaster" instead of throwing an error.
            arch = 'Blaster'
            self.SetState('Archetype', arch)

        self.Ctrls['Primary'].Clear()
        self.Ctrls['Secondary'].Clear()
        self.Ctrls['Epic'].Clear()

        Primaries   = GameData.Archetypes[arch]['Primary']
        Secondaries = GameData.Archetypes[arch]['Secondary']
        Epix        = GameData.Archetypes[arch]['Epic']

        self.Ctrls['Epic'].Append('') # allow us to deselect epic pool

        for p in Primaries   : self.Ctrls['Primary'].Append(p)
        for s in Secondaries : self.Ctrls['Secondary'].Append(s)
        for e in Epix        : self.Ctrls['Epic'].Append(e)

        self.Ctrls['Primary'].SetSelection(0)
        self.Ctrls['Secondary'].SetSelection(0)
        self.Ctrls['Epic'].SetSelection(0)

        self.Ctrls['Epic'].Enable(arch != "Peacebringer" and arch != "Warshade")

        if arch == "Peacebringer" or arch == "Warshade":
            self.UpdatePoolPickers()

        if getattr(self.Profile, 'Mastermind', None):
            self.Profile.Mastermind.SynchronizeUI()
        if getattr(self.Profile, 'MovementPowers', None):
            self.Profile.MovementPowers.SynchronizeUI()

        if arch == "Mastermind":
            if self.Profile.GetPageText(5) != self.Profile.Mastermind.TabTitle:
                self.Profile.InsertPage(5, self.Profile.Mastermind, self.Profile.Mastermind.TabTitle)
        else:
            if self.Profile.GetPageText(5) == self.Profile.Mastermind.TabTitle:
                self.Profile.RemovePage(5)

        if evt: evt.Skip()

    def OnPickOrigin(self, evt = None):
        if not self.GetState('Origin'):
            self.SetState('Origin', 'Magic')
        if evt: evt.Skip()

    def OnPickPoolPower(self, evt):
        self.UpdatePoolPickers()
        self.Profile.MovementPowers.SynchronizeUI()
        self.Profile.CheckAllConflicts()
        evt.Skip()

    def UpdatePoolPickers(self):
        c = self.Ctrls
        pickedPools = []

        for pickername in ['Pool1', 'Pool2', 'Pool3', 'Pool4']:
            if val := self.GetState(pickername):
                pickedPools.append(val)

        for pickername in ['Pool1', 'Pool2', 'Pool3', 'Pool4']:
            curval = self.GetState(pickername)
            picker = c[pickername]
            # rebuild the base list
            poolcontents = sorted(GameData.PoolPowers)
            poolcontents.insert(0, '')
            # if we've already picked this pool, remove it (unless it's ours in the first place)
            for pp in pickedPools:
                if pp and pp != curval: poolcontents.remove(pp)

            # check the mutually-exclusive power pools.
            specializedPools = ['Experimentation', 'Force of Will', 'Gadgetry', 'Sorcery']
            for sp in specializedPools:
                # if we've selected one of these...
                if sp in pickedPools:
                    #...remove each of the other ones from poolcontents
                    for s in specializedPools:
                        if sp != s:
                            if s in poolcontents: poolcontents.remove(s)

            if self.Profile.Server() == 'Rebirth':
                arch = self.GetState('Archetype')
                if arch == 'Peacebringer' or arch == 'Warshade':
                    if 'Flight' in poolcontents: poolcontents.remove('Flight')
                    if 'Teleportation' in poolcontents: poolcontents.remove('Teleportation')

            picker.SetItems(poolcontents)
            picker.SetSelection(picker.FindString(curval))

    def OnPickPrimaryPowerSet(self, evt):
        self.Profile.Mastermind.SynchronizeUI()
        self.Profile.CheckAllConflicts()
        evt.Skip()

    def OnPickSecondaryPowerSet(self, evt):
        self.Profile.CheckAllConflicts()
        evt.Skip()

    def OnPickEpicPowerSet(self, evt):
        evt.Skip()

    def OnTypeEnable(self, evt = None):
        typeenabled = self.GetState('TypingNotifierEnable')
        self.EnableControls(typeenabled, ['TypingNotifier'])
        self.Layout()
        if evt: evt.Skip()

    def ValidateServerPicker(self):
        if not self.GetState('Server'): self.SetState('Server', 'Homecoming')

    def OnServerChange(self, evt):
        if evt: evt.Skip()
        server = self.Profile.Server()

        if self.GetState('Server') != server:
            if wx.MessageBox('Changing server requires saving and reloading the Profile.  Continue?', 'Changing Server', wx.YES_NO, self) == wx.YES:
                mainwindow = wx.App.Get().Main
                self.Profile.doSaveToFile()
                newProfile = Profile.Profile(mainwindow, filename = self.Profile.Filename)
                newProfile.buildFromData()
                mainwindow.InsertProfile(newProfile)
            else:
                self.ServerPicker.SetSelection(self.ServerPicker.FindString(server))

    UI.Labels.update({
        'Epic' : 'Epic / Patron',

        'Pool1'           : "Power Pool 1",
        'Pool2'           : "Power Pool 2",
        'Pool3'           : "Power Pool 3",
        'Pool4'           : "Power Pool 4",

        'StartChat'            : 'Start Chat',
        'SlashChat'            : 'Start Chat (with "/")',
        'StartEmote'           : 'Begin emote (types "/em")',
        'AutoReply'            : 'AutoReply to incoming /tell',
        'TellLast'             : 'Send /tell to the last player you sent a /tell',
        'TellTarget'           : 'Send /tell to current target',
        'QuickChat'            : 'Pop up QuickChat menu',

        'TypingNotifierEnable' : 'Enable Typing Notifier',
        'TypingNotifier'       : 'Typing Notifier',

        'QuitToDesktop'   : "Quit to Desktop",
        'QuitToSelect'    : "Quit to Character Select",
        'QuitToLogin'     : "Quit to Login",
        'Sync'            : "Synchronize with Game Server",

        'ToggleRP'        : "Toggle Roleplaying Status",
        'HelpHelpMe'      : 'Set "Help Me" Status',
        'HelpMentor'      : 'Set "Mentor" Status',
        'HelpOff'         : 'Disable Help Status',

        'InviteTarget'   : "Invite Target to Group",
        'SGInviteTarget' : "Invite Target to Supergroup",
        'FriendTarget'   : "Add Target to Friends",
        'GFriendTarget'  : "Add Target to Global Friends",
        'IgnoreTarget'   : "Ignore your Current Target",
        'UnignoreTarget' : "Unignore your Current Target",
    })
