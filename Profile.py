import wx
from pathlib import Path
import json

from BindFile import BindFile
from Page.BufferBinds import BufferBinds
#from Page.ComplexBinds
#from Page.CustomBinds
from Page.FPSDisplay import FPSDisplay
from Page.General import General
from Page.InspirationPopper import InspirationPopper
from Page.Mastermind import Mastermind
from Page.SimpleBinds import SimpleBinds
from Page.SoD import SoD
from Page.TeamPetSelect import TeamPetSelect
from Page.TypingMsg import TypingMsg

class Profile(wx.Notebook):

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, style = wx.NB_LEFT)

        self.BindFiles = {}
        self.Pages     = []

        # TODO -- here's where we'd load a profile from a file or something.

        # Add the individual tabs, in order.
        self.CreatePage(General(self))

        # Pluck some bits out of General that we'll want later
        self.BindsDir  = self.General.State['BindsDir']
        self.ResetFile = self.GetBindFile(self.BindsDir, "resetfile.txt")

        self.CreatePage(SoD(self))
        self.CreatePage(FPSDisplay(self))
        #self.CreatePage(InspirationPopper(self))
        self.CreatePage(Mastermind(self))
        #self.CreatePage(TeamPetSelect(self))
        #self.CreatePage(TypingMsg(self))
        self.CreatePage(SimpleBinds(self))
        self.CreatePage(BufferBinds(self))
        #self.CreatePage(ComplexBinds(self))
        #self.CreatePage(CustomBinds(self))

    def CreatePage(self, module):
        module.FillTab()
        page = self.AddPage(module, module.TabTitle)

        setattr(self, module.TabTitle, module)

        self.Pages.append(module.TabTitle)

        self.Layout()

    ###################
    # Profile Save/Load
    def ProfileFile(self):
        return Path(self.BindsDir, self.General.State['Name'] + ".bcp")


    def SaveToFile(self, event):

        savefile = Path(self.ProfileFile())

        savedata = {}
        for pagename in self.Pages:
            savedata[pagename] = {}
            page = getattr(self, pagename)
            for control in page.Controls:
                savedata[pagename][control] = page.Controls[control].GetValue()

        dumpstring = json.dumps(savedata, indent=0)
        try:
            savefile.touch() # make sure there's one there.
            savefile.write_text(dumpstring)
            wx.LogError(f"Wrote file {savefile}")
        except None:
            wx.LogError(f"Problem saving to file '{savefile}'")

    def LoadFromFile(self, event):

        with wx.FileDialog(self, "Open Profile file",
               wildcard="Bindcontrol Profiles (*.bcp)|*.bcp|All Files (*.*)|*.*",
               # wildcard="Bindcontrol and Citybinder Profiles (*.bcp;*.cbp)|*.bcp;*.cbp",
               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            with Path(pathname) as file:
                try:
                    datastring = file.read_text()
                    data = json.loads(datastring)

                    print(data)

                    for pagename in self.Pages:
                        page = getattr(self, pagename)
                        page.State = data[page]
                        page.SyncControlsFromState()

                except:
                    wx.LogError("Cannot open file '%s'." % file)

    #####################
    # Bind file functions
    def GetBindFile(self, *filename):
        # Store them internally as a simple string
        # but send BindFile the list of path parts
        filename_key = "!!".join(filename)

        if not self.BindFiles.get(filename_key, None):
            self.BindFiles[filename_key] = BindFile(self, *filename)

        return self.BindFiles[filename_key]


    def WriteBindFiles(self):
        for Page in self.Pages:
            print(Page.Name + "\n" + Page.PopulateBindFiles)

        for _, bindfile in self.BindFiles:
            bindfile.Write(self)
