import wx
import UI

from Page import Page
from UI.BufferBindPane  import BufferBindPane
from UI.SimpleBindPane  import SimpleBindPane
from UI.ComplexBindPane import ComplexBindPane

class CustomBinds(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)

        self.TabTitle = "Custom Binds"
        self.Panes    = []
        self.Init     = {}

    def BuildPage(self):

        # Overall sizer for 'self'
        MainSizer = wx.BoxSizer(wx.VERTICAL) # overall sizer

        # bottom sizer for the buttons
        buttonSizer         = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item buttons
        newSimpleBindButton = wx.Button(self, -1, "New Simple Bind")
        newSimpleBindButton.Bind(wx.EVT_BUTTON, self.OnNewSimpleBindButton)
        buttonSizer.Add(newSimpleBindButton, wx.ALIGN_CENTER)
        newComplexBindButton = wx.Button(self, -1, "New Complex Bind")
        newComplexBindButton.Bind(wx.EVT_BUTTON, self.OnNewComplexBindButton)
        buttonSizer.Add(newComplexBindButton, wx.ALIGN_CENTER)
        newBufferBindButton = wx.Button(self, -1, "New Buffer Bind")
        newBufferBindButton.Bind(wx.EVT_BUTTON, self.OnNewBufferBindButton)
        buttonSizer.Add(newBufferBindButton, wx.ALIGN_CENTER)

        # a scrollable window and sizer for the collection of collapsable panes
        self.PaneSizer      = wx.BoxSizer(wx.VERTICAL)
        self.scrolledPane   = wx.ScrolledWindow(self, -1, style = wx.VSCROLL)
        self.scrolledPane.SetScrollRate(10,10) # necessary to enable scrolling at all.
        self.scrolledPane.SetSizer(self.PaneSizer)

        # add the two parts of the layout, bottom one expandable
        MainSizer.Add( buttonSizer,       0, wx.EXPAND)
        MainSizer.Add( self.scrolledPane, 1, wx.EXPAND)

        # sizer around the whole thing to add padding
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(MainSizer, 1, flag = wx.ALL|wx.EXPAND, border = 16)

        self.SetSizerAndFit(paddingSizer)
        #self.SetSizerAndFit(MainSizer)
        self.Layout()

    def OnNewSimpleBindButton(self, evt):
        self.AddBindToPage(bindpane = SimpleBindPane(self))
        evt.Skip()

    def OnNewComplexBindButton(self, evt):
        self.AddBindToPage(bindpane = ComplexBindPane(self))
        evt.Skip()

    def OnNewBufferBindButton(self, evt):
        self.AddBindToPage(bindpane = BufferBindPane(self))
        evt.Skip()

    def AddBindToPage(self, bindpane = None):

        if not bindpane:
            wx.LogError("Something tried to add an empty bindpane to the page")
            return

        if not bindpane.Title: # this is from a "New Bind" button
            dlg = wx.TextEntryDialog(self, 'Enter name for new bind')
            if dlg.ShowModal() == wx.ID_OK:
                bindpane.Title = dlg.GetValue()
                bindpane.SetLabel(bindpane.Title)
            else:
                bindpane.Destroy()
                return

            dlg.Destroy()

        self.Panes.append(bindpane)

        bindpane.BuildBindUI(self)

        # put it in a box with a 'delete' button
        deleteSizer = wx.BoxSizer(wx.HORIZONTAL)
        deleteSizer.Add(bindpane, 1, wx.EXPAND, 5)
        deleteButton = wx.Button(self.scrolledPane, -1, "X", size = [40, -1])
        deleteButton.SetForegroundColour(wx.RED)
        setattr(deleteButton, "BindPane", bindpane)
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDeleteButton)
        deleteSizer.Add(deleteButton, 0, wx.LEFT, 10)

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount(), deleteSizer, 0, wx.ALL|wx.EXPAND, 10)
        bindpane.Expand()
        self.Layout()

    def OnDeleteButton(self, evt):
        delButton = evt.EventObject
        bindname = delButton.BindPane.Title
        if wx.MessageBox(f'Delete Bind "{bindname}"?', 'Delete Bind', wx.YES_NO) == wx.NO: return
        sizer = delButton.GetContainingSizer()
        self.PaneSizer.Hide(sizer)
        self.PaneSizer.Remove(sizer)
        self.Panes.remove(delButton.BindPane)
        delButton.BindPane.Destroy()
        self.Layout()
        evt.Skip()

    def PopulateBindFiles(self):
        for pane in self.Panes:
            pane.PopulateBindFiles()
