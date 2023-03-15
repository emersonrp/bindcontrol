# UI / logic for the 'general' panel
import re
import wx
import UI
from Icon import GetIcon
from GameData import Archetypes, Origins, MiscPowers

from UI.ControlGroup import ControlGroup
from UI.IncarnateBox import IncarnateBox
from UI.ChatColorPicker import ChatColorPicker, ChatColors

from Page import Page

class General(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.Init = {
            'Name': 'Profile',
            'Origin': "Magic",
            'Archetype': 'Mastermind',
            'Primary': '',
            'Secondary': '',
            'Epic': '',
            'Pool1': '',
            'Pool2': '',
            'Pool3': '',
            'Pool4': '',

            'ChatEnable' : True,
            'StartChat'  : 'ENTER',
            'SlashChat'  : '/',
            'StartEmote' : ';',
            'AutoReply'  : 'BACKSPACE',
            'TellTarget' : 'COMMA',
            'QuickChat'  : "'",

            'TypingNotifierEnable' : 1,
            'TypingNotifier'       : 'typing',
        }

    def BuildPage(self):

        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        powersBox = ControlGroup(self, self, 'Powers and Info')
        self.NameCtrl = powersBox.AddControl(
            ctlName = 'Name',
            ctlType = 'text',
        )
        self.NameCtrl.Bind(wx.EVT_TEXT, self.OnNameCtrlChanged)

        originchoices = []
        for Origin in Origins:
            originchoices.append([Origin, GetIcon(Origin)])
        originpicker = powersBox.AddControl(
            ctlName = 'Origin',
            ctlType = 'bmcombo',
            contents = originchoices,
            callback = self.OnPickOrigin,
        )
        originpicker.SetMinSize([200,-1])

        archchoices = []
        for Arch in sorted(Archetypes):
            archchoices.append([Arch, GetIcon(Arch)])
        archpicker = powersBox.AddControl(
            ctlName = 'Archetype',
            ctlType = 'bmcombo',
            contents = archchoices,
            callback = self.OnPickArchetype,
        )
        archpicker.SetMinSize([200,-1])

        powersBox.AddControl(
            ctlName = 'Primary',
            ctlType = 'choice',
            # contents = sorted(ArchData['Primary']),
            callback = self.OnPickPrimaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Secondary',
            ctlType = 'choice',
            # contents = sorted(ArchData['Secondary']),
            callback = self.OnPickSecondaryPowerSet,
        )
        powersBox.AddControl(
            ctlName = 'Epic',
            ctlType = 'choice',
            # contents = sorted(ArchData['Epic']),
            callback = self.OnPickEpicPowerSet,
        )
        poolcontents = sorted(MiscPowers['Pool'])
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

        ChatSizer = wx.BoxSizer(wx.VERTICAL)

        ### Chat Color Picker
        ChatColorSizer = wx.StaticBoxSizer(wx.VERTICAL, self, "Chat Colors")
        ChatColorEnable = wx.CheckBox(ChatColorSizer.GetStaticBox(), -1, 'Use Custom Chat Colors')
        ChatColorEnable.SetToolTip( wx.ToolTip('Check this to select custom colors for your chat messages'))
        ChatColorEnable.CtlName = "ChatColorEnable"
        self.Ctrls['ChatColorEnable'] = ChatColorEnable
        ChatColorEnable.Bind(wx.EVT_CHECKBOX, self.OnColorEnable)
        ChatColors = ChatColorPicker(ChatColorSizer.GetStaticBox(), self, 'Chat', {
            'border'     : wx.BLACK,
            'background' : wx.WHITE,
            'text'       : wx.BLACK,
        })
        ChatColorSizer.Add(ChatColorEnable, 0, wx.ALL, 6)
        ChatColorSizer.Add(ChatColors, 0, wx.ALL, 10)
        ChatSizer.Add(ChatColorSizer, 0)

        ## Typing Notifier
        TNSizer = wx.StaticBoxSizer(wx.VERTICAL, self, "Typing Notifier")
        TNEnable = wx.CheckBox(TNSizer.GetStaticBox(), -1, 'Use Typing Notifier')
        TNEnable.SetToolTip(
                wx.ToolTip('Check this to enable a floating "typing" notifier when you are typing into the chat box'))
        TNEnable.CtlName = 'TypingNotifierEnable'
        TNEnable.Bind(wx.EVT_CHECKBOX, self.OnTypeEnable)
        self.Ctrls['TypingNotifierEnable'] = TNEnable
        TNCtrlSizer = wx.BoxSizer(wx.HORIZONTAL)
        TNLabel = wx.StaticText(TNSizer.GetStaticBox(), label = "Typing Notifier:", style=wx.ALIGN_RIGHT)
        TN = wx.TextCtrl(TNSizer.GetStaticBox(), value = self.Init['TypingNotifier'], style=wx.TE_CENTER)
        TN.CtlName = 'TypingNotifier'
        TN.CtlLabel = TNLabel
        self.Ctrls['TypingNotifier'] = TN
        TNCtrlSizer.Add(TNLabel, 1, wx.ALL|wx.ALIGN_CENTER, 6)
        TNCtrlSizer.Add(TN,      1, wx.ALL, 6)

        TNSizer.Add(TNEnable,    0, wx.ALL, 5)
        TNSizer.Add(TNCtrlSizer, 0, wx.ALL|wx.EXPAND, 5)

        ChatSizer.Add(TNSizer, 0, wx.TOP|wx.EXPAND, 6)

        ### Chat binds
        chatBindBox = ControlGroup(self, self, 'Chat Binds')

        for b in (
            ['StartChat',  'Activates the Chat bar with notifier and custom colors if selected'],
            ['SlashChat',  'Activates the Chat bar with notifier and a slash already typed'],
            ['StartEmote', 'Activates the Chat bar with notifier and "/em" already typed'],
            ['AutoReply',  'AutoReplies to incoming tells with notifier'],
            ['TellTarget', 'Starts a /tell to your current target with notifier'],
            ['QuickChat',  'Pops up QuickChat menu, with notifier'],
        ):
            chatBindBox.AddControl(
                ctlName = b[0],
                ctlType = 'keybutton',
                tooltip = b[1],
            )
        ChatSizer.Add(chatBindBox, 1, wx.EXPAND)

        ### Incarnate interface
        self.IncarnateBox = IncarnateBox(self)

        topSizer.Add(powersBox, 0, wx.RIGHT|wx.EXPAND, 10)
        topSizer.Add(ChatSizer, 0,          wx.EXPAND, 0)

        centeringSizer  = wx.BoxSizer(wx.VERTICAL)
        centeringSizer.Add(topSizer,           0, wx.TOP|wx.EXPAND, 10)
        centeringSizer.Add(self.IncarnateBox,  0, wx.TOP|wx.EXPAND, 6)

        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(centeringSizer, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0)

        # testPowerPicker = PowerPicker(self)
        # paddingSizer.Add(testPowerPicker, flag=wx.ALL|wx.EXPAND, border = 20)

        self.SynchronizeUI()

        self.SetSizerAndFit(paddingSizer)

    def SynchronizeUI(self):
        self.OnPickArchetype()
        self.OnTypeEnable()
        self.OnColorEnable()

    def PopulateBindFiles(self):
        ResetFile = self.Profile.ResetFile()

        colorstring = ''
        if self.GetState('ChatColorEnable'):
            colorstring = ChatColors(
                self.GetState('ChatForeground'),
                self.GetState('ChatBackground'),
                self.GetState('ChatBorder'),
            )

        notifier = ''
        if self.GetState('TypingNotifierEnable'):
            notifier = 'afk ' + self.GetState('TypingNotifier')

        ResetFile.SetBind(self.Ctrls['StartChat'] .MakeFileKeyBind([notifier, 'show chat', 'beginchat ' + colorstring]))
        ResetFile.SetBind(self.Ctrls['SlashChat'] .MakeFileKeyBind([notifier, 'show chat', 'slashchat']))
        ResetFile.SetBind(self.Ctrls['StartEmote'].MakeFileKeyBind([notifier, 'show chatem ' + notifier]))
        ResetFile.SetBind(self.Ctrls['AutoReply'] .MakeFileKeyBind([notifier, 'autoreply']))
        ResetFile.SetBind(self.Ctrls['TellTarget'].MakeFileKeyBind([notifier, 'show chat', 'beginchat /tell $target, ']))
        ResetFile.SetBind(self.Ctrls['QuickChat'] .MakeFileKeyBind([notifier, 'quickchat']))

        return

    ### EVENT HANDLERS
    def OnPickArchetype(self, evt = {}):
        arch = self.GetState('Archetype')

        if not arch:
            wx.LogError("Got into OnPickArchetype with arch not set, bailing.")
            return

        self.Ctrls['Primary'].Clear()
        self.Ctrls['Secondary'].Clear()
        self.Ctrls['Epic'].Clear()

        Primaries   = Archetypes[arch]['Primary']
        Secondaries = Archetypes[arch]['Secondary']
        Epix        = Archetypes[arch]['Epic']

        self.Ctrls['Epic'].Append('') # allow us to deselect epic pool

        for p in Primaries   : self.Ctrls['Primary'].Append(p)
        for s in Secondaries : self.Ctrls['Secondary'].Append(s)
        for e in Epix        : self.Ctrls['Epic'].Append(e)

        self.Ctrls['Primary'].SetSelection(0)
        self.Ctrls['Secondary'].SetSelection(0)
        self.Ctrls['Epic'].SetSelection(0)

        self.Ctrls['Epic']         .Enable(arch != "Peacebringer" and arch != "Warshade")
        self.Ctrls['Epic'].CtlLabel.Enable(arch != "Peacebringer" and arch != "Warshade")

        if getattr(self.Profile, 'Mastermind', None):
            self.Profile.Mastermind.SynchronizeUI()
        if getattr(self.Profile, 'MovementPowers', None):
            self.Profile.MovementPowers.SynchronizeUI()

        self.Fit()
        if evt: evt.Skip()


    # Event handlers
    def OnNameCtrlChanged(self, evt):
        nc = self.NameCtrl
        text = nc.GetValue()
        if len(text) == 0 or re.search(" ", text):
            nc.SetBackgroundColour((255,200,200))
            if len(text) == 0:
                nc.SetToolTip("The profile name cannot be empty.")
            else:
                nc.SetToolTip("The profile name cannot contain spaces.")
        else:
            nc.SetBackgroundColour(wx.NullColour)
            nc.SetToolTip(None)
        evt.Skip()


    def OnPickOrigin(self, evt):
        evt.Skip()

    def OnPickPoolPower(self, evt):
        self.Profile.MovementPowers.SynchronizeUI()
        evt.Skip()

    def OnPickPrimaryPowerSet(self, evt):
        self.Profile.Mastermind.SynchronizeUI()
        evt.Skip()

    def OnPickSecondaryPowerSet(self, evt):
        evt.Skip()

    def OnPickEpicPowerSet(self, evt):
        evt.Skip()

    def OnColorEnable(self, evt = None):
        colorsenabled = self.GetState('ChatColorEnable')
        self.DisableControls(colorsenabled, ['ChatBorder', 'ChatBackground', 'ChatForeground'])
        if evt: evt.Skip()

    def OnTypeEnable(self, evt = None):
        typeenabled = self.GetState('TypingNotifierEnable')
        self.DisableControls(typeenabled, ['TypingNotifier'])
        if evt: evt.Skip()

    UI.Labels.update({
        'Pool1'           : "Power Pool 1",
        'Pool2'           : "Power Pool 2",
        'Pool3'           : "Power Pool 3",
        'Pool4'           : "Power Pool 4",

        'StartChat'            : 'Start Chat',
        'SlashChat'            : 'Start Chat (with "/")',
        'StartEmote'           : 'Begin emote (types "/em")',
        'AutoReply'            : 'AutoReply to incoming /tell',
        'TellTarget'           : 'Send /tell to current target',
        'QuickChat'            : 'Pop up QuickChat menu',

        'TypingNotifierEnable' : 'Enable Typing Notifier',
        'TypingNotifier'       : 'Typing Notifier',
    })
