import wx
import UI

from Page import Page
from UI.BufferBindPane import BufferBindPane
from UI.SimpleBindPane import SimpleBindPane

class CustomBinds(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Custom Binds"
        self.Panes    = []

    def BuildPage(self):

        # Overall sizer for 'self'
        MainSizer = wx.BoxSizer(wx.VERTICAL) # overall sizer

        # a scrollable window and sizer for the collection of collapsable panes
        self.PaneSizer      = wx.BoxSizer(wx.VERTICAL)
        self.scrolledPane   = wx.ScrolledWindow(self, -1, style = wx.VSCROLL)
        self.scrolledPane.SetScrollRate(10,10) # necessary to enable scrolling at all.
        self.scrolledPane.SetSizer(self.PaneSizer)

        # bottom sizer for the buttons
        buttonSizer         = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item buttons
        newSimpleBindButton = wx.Button(self, -1, "New Simple Bind")
        newSimpleBindButton.Bind(wx.EVT_BUTTON, self.OnNewSimpleBindButton)
        buttonSizer.Add(newSimpleBindButton, wx.ALIGN_CENTER)
        #newBufferBindButton = wx.Button(self, -1, "New Buffer Bind")
        #newBufferBindButton.Bind(wx.EVT_BUTTON, self.OnNewBufferBindButton)
        #buttonSizer.Add(newBufferBindButton, wx.ALIGN_CENTER)

        # add the two parts of the layout, top one expandable
        MainSizer.Add( self.scrolledPane, 1, wx.EXPAND)
        MainSizer.Add( buttonSizer,       0, wx.EXPAND)

        # sizer around the whole thing to add padding
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(MainSizer, 1, flag = wx.ALL|wx.EXPAND, border = 16)

        self.SetSizerAndFit(paddingSizer)
        #self.SetSizerAndFit(MainSizer)
        self.Layout()

    def OnNewSimpleBindButton(self, _):
        self.AddBindToPage(bindpane = SimpleBindPane(self))

    def OnNewBufferBindButton(self, _):
        self.AddBindToPage(bindpane = BufferBindPane(self))

    def AddBindToPage(self, bindinit = {}, bindpane = None):

        if not bindpane:
            wx.LogError("Something tried to add an empty bindpane to the page")
            return

        if bindinit:
            # TODO - this is for initializing one of these from a saved profile
            pass
        else:
            bindname = ''
            dlg = wx.TextEntryDialog(self, 'Enter name for new bind')
            if dlg.ShowModal() == wx.ID_OK:
                bindname = dlg.GetValue()
            else:
                bindpane.Destroy()
                return

            dlg.Destroy()

        self.Panes.append(bindpane)


        bindpane.Title = bindname
        bindpane.BuildBindUI(self)
        bindpane.SetBackgroundColour([240,240,240])

        # put it in a box with a 'delete' button
        deleteSizer = wx.BoxSizer(wx.HORIZONTAL)
        deleteSizer.Add(bindpane, 1, wx.EXPAND, 5)
        deleteButton = wx.Button(self.scrolledPane, -1, "Delete")
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDeleteButton)
        deleteSizer.Add(deleteButton, 0, wx.LEFT|wx.RIGHT, 15)

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount(), deleteSizer, 0, wx.ALL|wx.EXPAND, 10)
        bindpane.Expand()
        self.Layout()

    def OnDeleteButton(self, _):
        pass

    def PopulateBindFiles(self):

        for pane in self.Panes:
            pane.PopulateBindFiles()

        ### TODO
        return
        ### TODO

    for i in (1,2,3,4,5,6,7,8):
        UI.Labels[f'Team{i}BuffKey'] = f"Team {i} Key"

    for i in (1,2,3,4,5,6):
        UI.Labels[f'Pet{i}BuffKey'] = f"Pet {i} Key"

    UI.Labels.update( {
        'BuffPetsByName' : "Buff Pets using Pet Names",
        'BuffsAffectTeam' : "Buffs Affect Team Members",
        'BuffsAffectPets' : "Buffs Affect Pets",
    })

