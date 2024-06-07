import wx
from Icon import GetIcon

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
        MainSizer = wx.BoxSizer(wx.VERTICAL)

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
        self.PaneSizer     = wx.BoxSizer(wx.VERTICAL)
        self.scrolledPanel = wx.ScrolledWindow(self, -1, style = wx.VSCROLL)
        self.scrolledPanel.SetScrollRate(10,10) # necessary to enable scrolling at all.
        self.scrolledPanel.SetSizer(self.PaneSizer)

        # add the two parts of the layout, bottom one expandable
        MainSizer.Add( buttonSizer,       0, wx.EXPAND|wx.BOTTOM, 16)
        MainSizer.Add( self.scrolledPanel, 1, wx.EXPAND)

        # sizer around the whole thing to add padding
        paddingSizer = wx.BoxSizer(wx.VERTICAL)
        paddingSizer.Add(MainSizer, 1, flag = wx.ALL|wx.EXPAND, border = 16)

        self.SetSizerAndFit(paddingSizer)
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
            self.SetBindPaneLabel(None, bindpane, new = True)
            if not bindpane: # clicked 'Cancel'
                return

        self.Panes.append(bindpane)

        bindpane.BuildBindUI(self)

        for ctrlname, ctrl in bindpane.Ctrls.items():
            self.Ctrls[ctrlname] = ctrl

        # put it in a box with control buttons
        bindSizer = wx.BoxSizer(wx.HORIZONTAL)
        bindSizer.Add(bindpane, 1, wx.EXPAND, 5)

        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        deleteButton = wx.BitmapButton(self.scrolledPanel, -1, bitmap = GetIcon('UI/delete'))
        deleteButton.SetForegroundColour(wx.RED)
        setattr(deleteButton, "BindPane", bindpane)
        setattr(deleteButton, "BindSizer", bindSizer)
        setattr(bindpane,     "DelButton", deleteButton)
        deleteButton.SetToolTip(f'Delete bind "{bindpane.Title}"')
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDeleteButton)
        buttonSizer.Add(deleteButton)

        renameButton = wx.BitmapButton(self.scrolledPanel, -1, bitmap = GetIcon('UI/rename'))
        setattr(renameButton, "BindPane", bindpane)
        setattr(bindpane,     "RenButton", renameButton)
        renameButton.SetToolTip(f'Rename bind "{bindpane.Title}"')
        renameButton.Bind(wx.EVT_BUTTON, self.SetBindPaneLabel)
        buttonSizer.Add(renameButton)

        duplicateButton = wx.BitmapButton(self.scrolledPanel, -1, bitmap = GetIcon('UI/copy'))
        setattr(duplicateButton, "BindPane", bindpane)
        setattr(bindpane,        "DupButton", duplicateButton)
        duplicateButton.SetToolTip(f'Duplicate bind "{bindpane.Title}"')
        duplicateButton.Bind(wx.EVT_BUTTON, self.OnDuplicateButton)
        buttonSizer.Add(duplicateButton)

        bindSizer.Add(buttonSizer, 0, wx.LEFT, 10)

        self.PaneSizer.Insert(self.PaneSizer.GetItemCount(), bindSizer, 0, wx.ALL|wx.EXPAND, 10)
        bindpane.Expand()
        self.Layout()

    def SetBindPaneLabel(self, evt, bindpane = None, new = False):
        if not bindpane:
            bindpane = evt.GetEventObject().BindPane
        if not bindpane:
            wx.LogError("Tried to set a BindPane label without a bindpane!")
            return

        # freeze and thaw to jump thru some hoops to make the title display update on Windows
        bindpane.Freeze()
        try:
            dlg = wx.TextEntryDialog(self, 'Enter name for bind')
            if bindpane.Title:
                dlg.SetValue(bindpane.Title)
            if dlg.ShowModal() == wx.ID_OK:
                # check if we already have a bind named that.  Complex Binds use the name as
                # part of the bindfiles' filenames, so we can't have dupes
                title = dlg.GetValue()
                for pane in self.Panes:
                    if title == pane.Title:
                        # show an "oops" dialog, this might not be perfect
                        wx.MessageBox(f"A bind called {title} already exists!", "Error", wx.OK, self)
                        self.SetBindPaneLabel(evt, bindpane, new)
                        dlg.Destroy()
                        return

                bindpane.Title = title
                bindpane.SetLabel(bindpane.Title)
                if not new:
                    bindpane.DelButton.SetToolTip(f'Delete bind "{bindpane.Title}"')
                    bindpane.RenButton.SetToolTip(f'Rename bind "{bindpane.Title}"')
                    bindpane.DupButton.SetToolTip(f'Duplicate bind "{bindpane.Title}"')
            else:
                if new:
                    bindpane.Destroy()

            if bindpane:
                if bindpane.IsCollapsed():
                    bindpane.Expand()
                    bindpane.Collapse()
                else:
                    bindpane.Collapse()
                    bindpane.Expand()
        except Exception as e:
            raise e
        finally:
            if bindpane:
                bindpane.Parent.Layout()
                bindpane.Thaw()

        dlg.Destroy()

    def OnDeleteButton(self, evt):
        delButton = evt.EventObject
        bindname = delButton.BindPane.Title
        if wx.MessageBox(f'Delete Bind "{bindname}"?', 'Delete Bind', wx.YES_NO) == wx.NO: return
        sizer = delButton.BindSizer
        for ctrlname in delButton.BindPane.Ctrls:
            if self.Ctrls.get(ctrlname, None) : del self.Ctrls[ctrlname]
        self.PaneSizer.Hide(sizer)
        self.PaneSizer.Remove(sizer)
        self.Panes.remove(delButton.BindPane)
        delButton.BindPane.Destroy()
        self.Layout()
        evt.Skip()

    def OnDuplicateButton(self, evt):
        oldbindpane = evt.EventObject.BindPane
        init = oldbindpane.Serialize()
        newbindpane = None
        if   isinstance(oldbindpane, SimpleBindPane):
            newbindpane = SimpleBindPane(self, init)
        elif isinstance(oldbindpane, ComplexBindPane):
            newbindpane = ComplexBindPane(self, init)
        elif isinstance(oldbindpane, BufferBindPane):
            newbindpane = BufferBindPane(self, init)

        if not newbindpane:
            wx.LogError(f"Error duplicating bind {oldbindpane.Title}!")
            return

        # clear the title so we get to name it.
        # also clear the keybind itself.
        newbindpane.Title = None
        self.AddBindToPage(newbindpane)
        newbindpane.ClearKeyBinds()

    def PopulateBindFiles(self):
        for pane in self.Panes:
            pane.PopulateBindFiles()
