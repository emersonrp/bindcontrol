import wx
import Profile

class BindDirsWindow(wx.MiniFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(sizer)

        bindpath = wx.ConfigBase.Get().Read('BindPath')
        sizer.Add(mainlabel := wx.StaticText(panel), 0, wx.TOP|wx.ALIGN_CENTER, 16)
        mainlabel.SetLabelMarkup(f"In your bind path: <b>{bindpath}</b>\n"+
                                 "the following binds directories were found,\n" +
                                 "and are managed by the following profiles:")

        listspacer = wx.BoxSizer(wx.HORIZONTAL)
        listsizer = wx.FlexGridSizer(2, -1, 5)

        headerFont = wx.Font(wx.FontInfo().Bold().Underlined())
        listsizer.Add(dirlabel := wx.StaticText(panel))
        dirlabel.SetFont(headerFont)
        dirlabel.SetLabelMarkup('Directory')
        listsizer.Add(proflabel := wx.StaticText(panel))
        proflabel.SetFont(headerFont)
        proflabel.SetLabelMarkup('Managing Profile')

        for binddir in sorted(Profile.GetAllProfileBindsDirs(), key = str.casefold):
            listsizer.Add(wx.StaticText(panel, label = binddir), 0, wx.ALL, 3)
            label = Profile.CheckProfileForBindsDir(binddir)
            dirname = wx.StaticText(panel, label = label or '')
            if not label:
                dirname.SetForegroundColour((128,128,128))
                dirname.SetLabelMarkup('<i>-unmanaged-</i>')
            listsizer.Add(dirname, 0, wx.ALL, 3)

        listspacer.AddStretchSpacer(1)
        listspacer.Add(listsizer, 2, wx.EXPAND)
        listspacer.AddStretchSpacer(1)

        sizer.Add(listspacer, 1, wx.EXPAND|wx.ALL, 16)

        mainSizer.Add(panel, 1, wx.EXPAND)

        self.Fit()
