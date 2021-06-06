#!/usr/bin/env python3


import wx

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
        wx.Notebook.__init__(self, parent)

        self.BindFiles = {}
        self.Pages     = {}

        # TODO -- here's where we'd load a profile from a file or something.

        # Add the individual tabs, in order.
        self.CreatePage(General(self))
        self.CreatePage(SoD(self))
        self.CreatePage(FPSDisplay(self))
        self.CreatePage(InspirationPopper(self))
        self.CreatePage(Mastermind(self))
        self.CreatePage(TeamPetSelect(self))
        self.CreatePage(TypingMsg(self))
        self.CreatePage(SimpleBinds(self))
        self.CreatePage(BufferBinds(self))
        #self.CreatePage(ComplexBinds(self))
        #self.CreatePage(CustomBinds(self))

    def CreatePage(self, module):
        module.InitKeys()
        module.FillTab()
        page = self.AddPage(module, module.TabTitle)

        self.Layout()

    def GetBindFile(self, filename):
        if not self.BindFiles.get(filename):
            self.BindFiles[filename] = BindFile(filename)

    def WriteBindFiles(self):
        for Page in self.Pages:
            print(Page.Name + "\n" + Page.PopulateBindFiles)

        for _, bindfile in self.BindFiles:
            bindfile.Write(self)
