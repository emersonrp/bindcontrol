# parent class for various custom bindpane types
import wx

class CustomBindPaneParent(wx.CollapsiblePane):
    def __init__(self, page, bind = None):
        wx.CollapsiblePane.__init__(self, page.scrolledPane,
                style = wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        # TODO - simplebind just have the one key<->contents,
        # but buffer binds have a whole set of them.
        self.Key            = ''
        self.Name           = ''
        self.Contents       = ''
        self.Page           = page
        self.bindclass      = type(self).__name__
        self.unique_bind_id = str(wx.NewIdRef().GetId())

        if bind:
            if bind.get('key',      None): self.Key      = bind['key']
            if bind.get('name',     None): self.Title    = bind['title']
            if bind.get('contents', None): self.Contents = bind['contents']

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)

    # This is so we can have multiple controls of the "same name" on the
    # Custom Binds page, if we have, say, several Simple binds.
    # TODO - still need to work out saving and especially loading
    # in Profile.  The "@@" below is so we can separate unique from
    # name for purposes of repopulating the UI on load.
    def UniqueName(self, name = ''):
        return self.bindclass + self.unique_bind_id + "@@" + name

    def BuildBindUI(self, parent):
        # build the UI needed to edit/create this bind, and shim
        # it into 'parent'
        pass

    def PopulateBindFiles(self):
        print(f"Inside {self.bindclass} PopulateBindFiles")
        # for overriding on child classes this will be called in the course of
        # the Custom Binds page doing its own PopulateBindFiles, iteratively
        # over all of its kids

    def OnPaneChanged(self, evt):
        self.Page.Layout()

