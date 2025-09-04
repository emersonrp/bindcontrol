import wx
import wx.lib.agw.ultimatelistctrl as ulc
from Help import HelpButton

import GameData

class qwyPetMouse(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        qwyMouseSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(qwyMouseSizer)

        centeringSizer = wx.BoxSizer(wx.VERTICAL)

        self.ButtonGrid = ulc.UltimateListCtrl(self,
                    agwStyle = ulc.ULC_VRULES|ulc.ULC_HRULES|ulc.ULC_NO_HIGHLIGHT|ulc.ULC_REPORT)

        # column headers
        for i, name in enumerate(['Key', 'Minions', 'Lieutenants', 'Boss', 'All']):
            self.ButtonGrid.InsertColumn(i, name)

        for row in [
            ['2'               ,'PetCom attack'         ,'PetCom attack'         ,'PetComPow attack'    ,'PetComAll attack']    ,
            ['ALT+LBUTTON'     ,'TargetCustomNext mypet','TargetCustomNext mypet','PetComPow go to'     ,'PetComAll go to']     ,
            [''                ,'PetCom go to'          ,'PetCom go to'          ,''                    ,'']                    ,
            ['ALT+RBUTTON'     ,'PetCom stay'           ,'PetCom stay'           ,'PetComPow stay'      ,'PetComAll stay']      ,
            ['RightDoubleClick','PetCom follow'         ,'PetCom follow'         ,'PetComPow follow'    ,'PetComAll follow']    ,
            ['ALT+RightDC'     ,'PetCom defensive'      ,'PetCom defensive'      ,'PetComPow defensive' ,'PetComAll defensive'] ,
            ['SHIFT+RightDC'   ,'PetCom aggressive'     ,'PetCom aggressive'     ,'PetComPow aggressive','PetComAll aggressive'],
            ['CTRL+RightDC'    ,'PetCom passive'        ,'PetCom passive'        ,'PetComPow passive'   ,'PetComAll passive ']  ,
        ]:
            self.ButtonGrid.Append(row)

        for i in (0,1,2,3,4):
            self.ButtonGrid.SetColumnWidth(i, wx.LIST_AUTOSIZE)

        # This is awful
        rect = self.ButtonGrid.GetItemRect(0)
        height = rect.height * (self.ButtonGrid.GetItemCount()+2)
        width = rect.width
        self.ButtonGrid.SetMinSize((wx.Size(width, height)))
        self.ButtonGrid.SetAutoLayout(True)

        centeringSizer.Add(self.ButtonGrid, 1)

        qwyMouseSizer.Add(centeringSizer, 0, wx.ALIGN_CENTER)

        self.Fit()
        self.Layout()

    def PopulateBindFiles(self):
        # This is going to be complicated and tangly - there are like 14 files with many entries.
        profile = wx.App.Get().Main.Profile
        page    = profile.Mastermind
        primary = profile.GetState('Primary')
        pabb = GameData.MMPowerSets[primary]['abbrs']
        pnam = GameData.MMPowerSets[primary]['names']
        heal = GameData.MMPowerSets[primary]['heal']
        upgr = GameData.MMPowerSets[primary]['upgrade']
        uniq = page.uniqueNames
