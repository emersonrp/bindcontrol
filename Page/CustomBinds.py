import wx
from Icon import GetIcon

from Page import Page
from Help import HelpButton
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

        # sizer for the buttons
        buttonSizer         = wx.BoxSizer(wx.HORIZONTAL) # sizer for new-item buttons
        newSimpleBindButton = wx.Button(self, -1, "New Simple Bind")
        newSimpleBindButton.Bind(wx.EVT_BUTTON, self.OnNewSimpleBindButton)
        buttonSizer.Add(newSimpleBindButton, wx.ALIGN_CENTER)
        buttonSizer.Add(HelpButton(self, 'SimpleBinds.html'), 0, wx.ALIGN_CENTER|wx.RIGHT, 5)
        newComplexBindButton = wx.Button(self, -1, "New Complex Bind")
        newComplexBindButton.Bind(wx.EVT_BUTTON, self.OnNewComplexBindButton)
        buttonSizer.Add(newComplexBindButton, wx.ALIGN_CENTER)
        buttonSizer.Add(HelpButton(self, 'ComplexBinds.html'), 0, wx.ALIGN_CENTER|wx.RIGHT, 5)
        newBufferBindButton = wx.Button(self, -1, "New Buffer Bind")
        newBufferBindButton.Bind(wx.EVT_BUTTON, self.OnNewBufferBindButton)
        buttonSizer.Add(newBufferBindButton, wx.ALIGN_CENTER)
        buttonSizer.Add(HelpButton(self, 'BufferBinds.html'), 0, wx.ALIGN_CENTER)

        # a scrollable window and sizer for the collection of collapsible panes
        self.PaneSizer     = wx.BoxSizer(wx.VERTICAL)
        self.scrolledPanel = wx.ScrolledWindow(self, -1, style = wx.VSCROLL)
        self.scrolledPanel.SetScrollRate(10,10) # necessary to enable scrolling at all.
        self.scrolledPanel.SetSizer(self.PaneSizer)

        # add the two parts of the layout, bottom one expandable
        self.MainSizer.Add(buttonSizer,        0, wx.EXPAND|wx.BOTTOM, 16)
        self.MainSizer.Add(self.scrolledPanel, 1, wx.EXPAND)

        # disable scrolling on the main page's ScrolledWindow.
        # This is black magic, and may still act squirrely.
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)

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
            wx.LogError("Something tried to add an empty bindpane to the page.  This is a bug.")
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
        deleteButton = wx.BitmapButton(self.scrolledPanel, -1, bitmap = GetIcon('UI', 'delete'))
        deleteButton.SetForegroundColour(wx.RED)
        setattr(deleteButton, "BindPane", bindpane)
        setattr(deleteButton, "BindSizer", bindSizer)
        setattr(bindpane,     "DelButton", deleteButton)
        deleteButton.SetToolTip(f'Delete bind "{bindpane.Title}"')
        deleteButton.Bind(wx.EVT_BUTTON, self.OnDeleteButton)
        buttonSizer.Add(deleteButton)

        renameButton = wx.BitmapButton(self.scrolledPanel, -1, bitmap = GetIcon('UI', 'rename'))
        setattr(renameButton, "BindPane", bindpane)
        setattr(bindpane,     "RenButton", renameButton)
        renameButton.SetToolTip(f'Rename bind "{bindpane.Title}"')
        renameButton.Bind(wx.EVT_BUTTON, self.SetBindPaneLabel)
        buttonSizer.Add(renameButton)

        duplicateButton = wx.BitmapButton(self.scrolledPanel, -1, bitmap = GetIcon('UI', 'copy'))
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
            wx.LogError("Tried to set a BindPane label without a bindpane.  This is a bug.")
            return

        # freeze and thaw to jump thru some hoops to make the title display update on Windows
        bindpane.Freeze()
        oldtitle = bindpane.Title
        # marshal up the files to delete, before we change the name
        deletefiles = None if new else bindpane.AllBindFiles()
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
                        # TODO if we don't change the name, but click "OK" it errors because
                        # we already have ourselves named that.
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
                    bindpane.RenameCtrlsFrom(oldtitle)
                    # if we have files to delete (we do, if not new) then delete them.
                    if deletefiles:
                        self.Profile.doDeleteBindFiles(deletefiles)
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
        bindpane = delButton.BindPane
        with BindDeletionDialog(self, bindpane) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            if dlg.DeleteFilesCB and dlg.DeleteFilesCB.GetValue():
                # do the delete of the files
                files = bindpane.AllBindFiles()
                self.Profile.doDeleteBindFiles(files)
        sizer = delButton.BindSizer
        for ctrlname in delButton.BindPane.Ctrls:
            if self.Ctrls.get(ctrlname, None) : del self.Ctrls[ctrlname]
        self.PaneSizer.Hide(sizer)
        self.PaneSizer.Remove(sizer)
        self.Panes.remove(delButton.BindPane)
        delButton.BindPane.Destroy()
        self.Profile.CheckAllConflicts()
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
        return True

    def AllBindFiles(self):
        files = []
        dirs  = []
        for pane in self.Panes:
            bfs = pane.AllBindFiles()
            if bfs:
                files.extend(bfs['files'])
                dirs .extend(bfs['dirs'])

        return {
            'files' : files,
            'dirs'  : dirs,
        }

class BindDeletionDialog(wx.Dialog):
    def __init__(self, parent, bindpane):
        wx.Dialog.__init__(self, parent, title = "Delete Bind")

        self.DeleteFilesCB = None

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(wx.StaticText(self, label = f'Delete Custom Bind "{bindpane.Title}"?'), 0, wx.ALL, 20)

        if isinstance(bindpane, ComplexBindPane) or isinstance(bindpane, BufferBindPane):
            self.DeleteFilesCB = wx.CheckBox(self, label = "Delete all associated bindfiles")
            self.DeleteFilesCB.SetValue(True)
            mainSizer.Add(self.DeleteFilesCB, 0, wx.ALL|wx.ALIGN_CENTER, 10)

        mainSizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL), 0, wx.ALL|wx.ALIGN_CENTER, 20)

        self.SetSizerAndFit(mainSizer)

