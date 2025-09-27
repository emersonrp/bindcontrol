import wx
import wx.lib.stattext as ST
import platform
from functools import partial

import Profile
from Util.Paths import GetAllProfileBindsDirs, CheckProfileForBindsDir, GetProfileFileForName


class BindDirsWindow(wx.MiniFrame):
    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        config = wx.ConfigBase.Get()

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

        for binddir in sorted(GetAllProfileBindsDirs(config), key = str.casefold):
            listsizer.Add(statictextclass(panel, label = binddir), 0, wx.ALL, 3)
            label = CheckProfileForBindsDir(config, binddir)
            dirname = statictextclass(panel, label = label or '')
            if not label:
                dirname.SetForegroundColour(wx.Colour(128,128,128))
                dirname.SetFont(unmgdFont)
                dirname.SetLabelMarkup('-unmanaged-')
                dirname.SetToolTip('No known profile is managing this directory.')
            else:
                file = GetProfileFileForName(config, label)
                if file.is_file():
                    dirname.SetFont(linkFont)
                    dirname.SetForegroundColour(wx.Colour(0,0,255))
                    dirname.SetToolTip(f'Click to load profile "{label}"')
                    dirname.SetCursor(wx.Cursor(wx.CURSOR_HAND))
                    # TODO Bind to a partial with 'file' in it
                    dirname.Bind(wx.EVT_LEFT_DOWN, partial(self.OnProfileClick, file = file, label = label))
                else:
                    dirname.SetForegroundColour(wx.Colour(255,0,0))
                    dirname.SetToolTip(f'The profile "{label}" isn\'t available to be loaded.')


            listsizer.Add(dirname, 0, wx.ALL, 3)

        listspacer.AddStretchSpacer(1)
        listspacer.Add(listsizer, 2, wx.EXPAND)
        listspacer.AddStretchSpacer(1)

        sizer.Add(listspacer, 1, wx.EXPAND|wx.ALL, 16)

        mainSizer.Add(panel, 1, wx.EXPAND)

        self.Fit()

        self.Bind(wx.EVT_SHOW, self.OnShow)

    def OnProfileClick(self, _, file, label) -> None:
        if self.Parent.CheckIfProfileNeedsSaving() == wx.CANCEL: return # pyright: ignore

        # Offer some feedback that we did anything.
        with wx.WindowDisabler():
            _ = wx.BusyInfo(wx.BusyInfoFlags().Parent(self).Text(f'Loading {label}...'))
            wx.GetApp().Yield()
            newProfile = Profile.Profile(self.Parent, filename = file)
            newProfile.buildUIFromData()

            self.Parent.InsertProfile(newProfile) # pyright: ignore

    # blow up the window when we hide it since we make a new one each time to keep the info fresh
    def OnShow(self, evt) -> None:
        if not evt.IsShown():
            self.Destroy()
