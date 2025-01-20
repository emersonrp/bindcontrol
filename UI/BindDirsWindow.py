import wx
import wx.lib.stattext as ST
import platform
from functools import partial

import Profile

class BindDirsWindow(wx.MiniFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        statictextclass = wx.StaticText if platform.system() == "Windows" else ST.GenStaticText

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

        bindpath = wx.ConfigBase.Get().Read('BindPath')
        sizer.Add(mainlabel := statictextclass(panel), 0, wx.TOP|wx.ALIGN_CENTER, 16)
        mainlabel.SetLabelMarkup(f"In your bind path: <b>{bindpath}</b>\n"+
                                 "the following binds directories were found,\n" +
                                 "and are managed by the following profiles:")

        listspacer = wx.BoxSizer(wx.HORIZONTAL)
        listsizer = wx.FlexGridSizer(2, -1, 5)

        headerFont = wx.Font(wx.FontInfo().Bold().Underlined())
        unmgdFont  = wx.Font(wx.FontInfo().Italic())
        linkFont   = wx.Font(wx.FontInfo().Underlined())

        listsizer.Add(dirlabel := statictextclass(panel))
        dirlabel.SetFont(headerFont)
        dirlabel.SetLabelMarkup('Directory')
        listsizer.Add(proflabel := statictextclass(panel))
        proflabel.SetFont(headerFont)
        proflabel.SetLabelMarkup('Managing Profile')

        for binddir in sorted(Profile.GetAllProfileBindsDirs(), key = str.casefold):
            listsizer.Add(statictextclass(panel, label = binddir), 0, wx.ALL, 3)
            label = Profile.CheckProfileForBindsDir(binddir)
            dirname = statictextclass(panel, label = label or '')
            dirname.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            if not label:
                dirname.SetForegroundColour((128,128,128))
                dirname.SetFont(unmgdFont)
                dirname.SetLabelMarkup('-unmanaged-')
                dirname.SetToolTip(f'No known Profile is managing this directory.  Click to select an existing Profile to manage it.')
                dirname.SetCursor(wx.Cursor(wx.CURSOR_HAND))
                dirname.Bind(wx.EVT_LEFT_DOWN, partial(self.OnPickProfileClick, dirname = binddir))
            else:
                if file := Profile.GetProfileFileForName(label):
                    dirname.SetFont(linkFont)
                    dirname.SetForegroundColour((0,0,255))
                    dirname.SetToolTip(f'Click to load Profile "{label}"')
                    dirname.SetCursor(wx.Cursor(wx.CURSOR_HAND))
                    dirname.Bind(wx.EVT_LEFT_DOWN, partial(self.OnProfileClick, file = file))
                else:
                    dirname.SetForegroundColour((255,0,0))
                    dirname.SetToolTip(f'The managing Profile "{label}" isn\'t available to be loaded.')

            listsizer.Add(dirname, 0, wx.ALL, 3)

        listspacer.AddStretchSpacer(1)
        listspacer.Add(listsizer, 2, wx.EXPAND)
        listspacer.AddStretchSpacer(1)

        sizer.Add(listspacer, 1, wx.EXPAND|wx.ALL, 16)

        mainSizer.Add(panel, 1, wx.EXPAND)

        self.Fit()

        self.Bind(wx.EVT_SHOW, self.OnShow)

    def OnPickProfileClick(self, _, dirname):
        message = f'Select a BindControl Profile to manage the "{dirname}" directory'
        defaultdir = wx.ConfigBase.Get().Read('ProfilePath')
        if not defaultdir:
            return
        wildcard = "BindControl Profiles (*.bcp)|*.bcp"
        dlg = wx.FileDialog(self, message, defaultdir, wildcard = wildcard, style = wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            profilename = dlg.GetFilename()[:-4]
            confirmdlg = wx.MessageDialog(self, f'Assign the Profile "{profilename}" to manage the "{dirname}" directory?', style = wx.OK|wx.CANCEL)
            if confirmdlg.ShowModal() == wx.ID_OK:
                # create BindsDir / dirname / bcprofileid.txt with profilename in it
                # somehow update the contents of self to reflect the new reality, maybe just twiddle the one label that was clicked.
                # Oh God somehow open up the profile and set its ProfileBindsDir, without loading the whole thing.
                ...

    def OnProfileClick(self, _, file):
        if self.Parent.CheckIfProfileNeedsSaving() == wx.CANCEL: return

        # Offer some feedback that we did anything.
        with wx.WindowDisabler():
            _ = wx.BusyInfo('Loading...')
            wx.GetApp().Yield()
            newProfile = Profile.Profile(self.Parent)

            newProfile.doLoadFromFile(file)

            self.Parent.InsertProfile(newProfile)

    # blow up the window when we hide it since we make a new one each time to keep the info fresh
    def OnShow(self, evt):
        if not evt.IsShown():
            self.Destroy()
