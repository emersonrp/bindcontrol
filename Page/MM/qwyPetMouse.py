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
            ['2'               ,'Attack'         ,'Attack'         ,'Attack'    ,'Attack']    ,
            ['ALT+LBUTTON'     ,'Target Next Pet','Target Next Pet','Go To'     ,'Go To']     ,
            [''                ,'Go To'          ,'Go To'          ,''                    ,'']                    ,
            ['ALT+RBUTTON'     ,'Stay'           ,'Stay'           ,'Stay'      ,'Stay']      ,
            ['RightDoubleClick','Follow'         ,'Follow'         ,'Follow'    ,'Follow']    ,
            ['ALT+RightDC'     ,'Defensive'      ,'Defensive'      ,'Defensive' ,'Defensive'] ,
            ['SHIFT+RightDC'   ,'Aggressive'     ,'Aggressive'     ,'Aggressive','Aggressive'],
            ['CTRL+RightDC'    ,'Passive'        ,'Passive'        ,'Passive'   ,'Passive ']  ,
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

        centeringSizer.Add(self.ButtonGrid, 1, wx.ALL, 15)

        qwyMouseSizer.Add(centeringSizer, 0, wx.ALIGN_CENTER)

        self.Fit()
        self.Layout()

    def GetKeyBinds(self):
        return [
            ['Attack'         , '2'                     ],
            ['Target Next Pet', 'ALT+LBUTTON'           ],
            ['Stay'           , 'ALT+RBUTTON'           ],
            ['Follow'         , 'RIGHTDOUBLECLICK'      ],
            ['Defensive'      , 'ALT+RIGHTDOUBLECLICK'  ],
            ['Aggressive'     , 'SHIFT+RIGHTDOUBLECLICK'],
            ['Passive'        , 'CTRL+RIGHTDOUBLECLICK' ],
        ]

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
