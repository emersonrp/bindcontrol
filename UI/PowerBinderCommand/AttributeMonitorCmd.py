import wx
import wx.adv
from wx.adv import EditableListBox
from UI.PowerBinderCommand import PowerBinderCommand

####### Attribute Monitor
class AttributeMonitorCmd(PowerBinderCommand):
    Name = "Attribute Monitor"
    Menu = "Graphics / UI"

    def BuildUI(self, dialog):
        self.Page = dialog.Page
        self.AttributeTable = {
            'Base' : {
                'Current Hit Points'       : 'NT H',
                'Max Hit Points'           : 'X H',
                'Current Endurance'        : 'T E',
                'Max Endurance'            : 'X EN',
                'Regeneration Rate'        : 'N RAT',
                'Recovery Rate'            : 'Y RA',
                'Endurance Consumption'    : 'SU',
                'ToHit Bonus'              : 'T B',
                'Accuracy Bonus'           : 'CC',
                'Last Hit Chance'          : 'T C',
                'Damage Bonus'             : 'DA',
                'Healing Bonus'            : 'NG B',
                'Recharge Time Bonus'      : 'ME B',
                'Endurance Discount'       : 'CE DIS',
                'Stealth Radius (PvP)'     : 'PVP',
                'Stealth Radius (PvE)'     : 'PVE',
                'Perception Radius'        : 'RC',
                'Range Bonus'              : 'GE B',
                'Threat Level'             : 'AT L',
                'Experience to Next Level' : 'XT',
                'Experience Debt'          : 'XP',
                'Influence / Infamy'       : 'INF',
                'Inherent'                 : 'NH',
            },
            'Movement Speed' : {
                'Flying Speed'    : 'FL',
                'Jumping Speed'   : 'PI',
                'Max Jump Height' : 'X J',
                'Run Speed'       : 'RU',
            },
            'Damage Resistance' : {
                'Smashing Resistance'        : 'G R',
                'Lethal Resistance'          : 'L R',
                'Fire Resistance'            : 'RE R',
                'Cold Resistance'            : 'COLD R',
                'Energy Resistance'          : 'DamageType[4]',
                'Negative Energy Resistance' : 'GY R',
                'Psyonic Resistance'         : 'NIC R',
                'Toxic Resistance'           : 'XIC R',
            },
            'Defense' : {
                'Base Defense'            : 'BAS',
                'Ranged Defense'          : 'ED',
                'Melee Defense'           : 'MEL',
                'AoE Defense'             : '2',
                'Smashing Defense'        : '3',
                'Lethal Defense'          : '4',
                'Fire Defense'            : '5',
                'Cold Defense'            : '6',
                'Energy Defense'          : '7',
                'Negative Energy Defense' : '8',
                'Psionic Defense'         : '9',
                'Toxic Defense'           : '1',
            },
            'Debuff Resistance' : {
                'Regeneration Resistance' : 'ON R',
                'Recovery Resistance'     : 'RY R',
                'To Hit Resistance'       : 'IT R',
                'Defense Resistance'      : 'NSE RES',
            },
            'Status Effect Protection' : {
                'Hold Protection'          : 'D P',
                'Immobilize Protection'    : 'LIZE P',
                'Stun Protection'          : 'N P',
                'Sleep Protection'         : 'P P',
                'Knockback Protection'     : 'K P',
                'Confuse Protection'       : 'SE P',
                'Terrorize Protection'     : 'ZE P',
                'Repel Protection'         : 'EL P',
                'Teleport Protection'      : 'T P',
            },
            'Status Effect Resistance' : {
                'Hold Resistance'       : 'D R',
                'Immobilize Resistance' : 'LIZE R',
                'Stun Resistance'       : 'N R',
                'Sleep Resistance'      : 'P R',
                'Knockback Resistance'  : 'K R',
                'Confuse Resistance'    : 'SE R',
                'Terrorize Resistance'  : 'ZE R',
                'Placate Resistance'    : 'TE R',
                'Taunt Resistance'      : 'NT R',
            },
            'Miscellaneous' : {
                'Level Shift'              : 'L S',
            },
        }
        groupSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.AttributeMenu = wx.Menu()
        for group, controls in self.AttributeTable.items():
            submenu = wx.Menu()
            self.AttributeMenu.AppendSubMenu(submenu, group)
            for cb in controls:
                submenu.Append(wx.ID_ANY, cb)

        self.AttributeMenu.Bind(wx.EVT_MENU, self.OnMenuItem)

        self.editbox = EditableListBox(dialog, label = "Attributes", style = wx.adv.EL_ALLOW_NEW|wx.adv.EL_ALLOW_DELETE)
        groupSizer.Add(self.editbox)

        newButton = self.editbox.GetNewButton()
        newButton.Bind(wx.EVT_BUTTON, self.OnNewButton)

        return groupSizer

    def MakeBindString(self):
        map = {}
        bindstrings = []
        for _, controls in self.AttributeTable.items():
            for cb, data in controls.items():
                map[cb] = data

        for string in self.editbox.GetStrings():
            if string:
                bindstrings.append(f'monitorattribute {map[string]}')

        return '$$'.join(bindstrings)

    def Serialize(self):
        return {
            'attributes' : self.editbox.GetStrings()
        }

    def Deserialize(self, init):
        self.editbox.SetStrings(init.get('attributes', []))

    def OnNewButton(self, evt):
        evt.GetEventObject().PopupMenu(self.AttributeMenu)

    def OnMenuItem(self, evt):
        menuitem = evt.EventObject.FindItemById(evt.GetId())
        existingstrings = self.editbox.GetStrings()
        existingstrings.append(menuitem.GetItemLabel())
        self.editbox.SetStrings(existingstrings)
