# Utility class for querying joystick/controller
import platform
import wx.adv
from typing import List

class bcController(wx.adv.Joystick):

    def __init__(self):
        wx.adv.Joystick.__init__(self)
        self.CodeTable = self.SetCodeTable()

        self.CurrentAxisPercents = []

        # Don't even poll axes if we're not joysticking
        if self.IsOk():
            self.CurrentAxisPercents = [0] * self.GetNumberAxes()

    def SetCurrentAxisPercents(self):
        for axis in range(len(self.CurrentAxisPercents)):

            # TODO - this code makes assumptions about the range/location of the dpad.
            # This works for my Logitech 310 but possibly nothing else.
            # This will take some third-party testing
            apos = self.GetPosition(axis)
            if axis == 0:
                amin, amax = self.GetXMin(), self.GetXMax()
                self.CurrentAxisPercents[axis]= self.AxisPercent(amin, amax, apos)
                # Joystick1_LEFT, Joystick1_RIGHT
            elif axis == 1:
                amin, amax = self.GetYMin(), self.GetYMax()
                self.CurrentAxisPercents[axis]= self.AxisPercent(amin, amax, apos)
                # Joystick1_UP, Joystick1_DOWN
            elif axis == 2:
                # So far, looks like on MacOS, axis 2 is Z
                if platform.system() == "Darwin":
                    amin, amax = self.GetZMin(), self.GetZMax()
                else:
                    amin, amax = self.GetRudderMin(), self.GetRudderMax()
                # normalize this on Linux and Mac.  Find a better way if needed
                if platform.system() == "Linux" or platform.system() == "Darwin":
                    corr = (amax - amin) / 2
                    apos = apos + corr
                    amin = amin - corr
                    amax = amax + corr
                self.CurrentAxisPercents[axis]= self.AxisPercent(amin, amax, apos)
                # Joystick2_LEFT
            elif axis == 3:
                amin, amax = self.GetZMin(), self.GetZMax()
                self.CurrentAxisPercents[axis]= self.AxisPercent(amin, amax, apos)
                # Joystick3_LEFT, Joystick3_RIGHT
            elif axis == 4:
                amin, amax = self.GetUMin(), self.GetUMax()
                self.CurrentAxisPercents[axis]= self.AxisPercent(amin, amax, apos)
                # Joystick3_UP, Joystick3_DOWN
            elif axis == 5:
                amin, amax = self.GetVMin(), self.GetVMax()
                # normalize this on Linux and Mac.  Find a better way if needed
                if platform.system() == "Linux" or platform.system() == "Darwin":
                    corr = (amax - amin) / 2
                    apos = apos + corr
                    amin = amin - corr
                    amax = amax + corr
                self.CurrentAxisPercents[axis]= self.AxisPercent(amin, amax, apos)
                # Joystick2_LEFT
            elif axis in [6,7]:
                amin, amax = -32767, 32767
                self.CurrentAxisPercents[axis]= self.AxisPercent(amin, amax, apos)
                # JOYPAD_*

    def GetCurrentAxis(self):
        povpos = code = None
        if self.HasPOV4Dir():
            povpos = self.GetPOVPosition()

            if povpos != None and povpos < 60000: # 65535 seems to mean "at center"
                if   povpos == 0     : code = "JP_U"
                elif povpos == 9000  : code = "JP_R"
                elif povpos == 18000 : code = "JP_D"
                elif povpos == 27000 : code = "JP_L"

        else:
            self.SetCurrentAxisPercents()

            if self.CurrentAxisPercents: # might be empty list if we have no controller.
                current_axis = self.CurrentAxisPercents.index(max(self.CurrentAxisPercents, key=abs))

                current_dir = None

                if self.CurrentAxisPercents[current_axis] < -50:
                    current_dir = 0
                elif self.CurrentAxisPercents[current_axis] > 50:
                    current_dir = 1

                if current_dir != None:
                    code = self.CodeTable[current_axis][current_dir]

        return code

    def StickIsNearCenter(self):
        return abs(max(self.CurrentAxisPercents, key=abs)) < 50

    def AxisPercent(self, amin, amax, apos):
        center = amin + ((amax - amin) / 2)
        # (apos - center) is the distance, positive or negative, from the center
        # (amax - center) is the (positive) total throw on one side of center
        return int((apos - center) / (amax - center) * 100)

    def ListOfPossibleMods(self):
        # return a list of strings of controls that might be used as controller_modifiers
        # or extra_modifiers
        if not self.IsOk(): return []

        possible_mods = ["", "LTrigger", "RTrigger"] # assume everybody has triggers

        for bnum in range(1, self.GetNumberButtons()):
            bname = "JOY" + str(bnum)
            # TODO - should keep these mappings in this class somewhere
            if bnum == 5: bname = "LeftBumper"
            if bnum == 6: bname = "RightBumper"
            possible_mods.append(bname)

        # windows vs linux treatment of dpad
        if self.HasPOV4Dir() or self.GetMaxAxes() > 6:
            possible_mods = possible_mods + ["Joypad_Up", "Joypad_Down", "Joypad_Left", "Joypad_Right"]

        return possible_mods


    def SetCodeTable(self):
        # sets the Code table, which is a list, indexed by axis number,
        # of lists of [negative direction, positive direction] codes
        CodeTable : List[List] = []
        if platform.system() == 'Windows':
            CodeTable =  [
                    ['J1_L', 'J1_R'],
                    ['J1_U', 'J1_D'],
                    ['J2_L', 'J2_R'],
                    ['J3_U', 'J3_D'],
                    ['J3_L', 'J3_R'],
                    ['J2_L', 'J2_R'],
                    ['JP_L', 'JP_R'],
                    ['JP_U', 'JP_D'],
            ]

        elif platform.system() == 'Linux':
            CodeTable =  [
                    ['J1_L', 'J1_R'],
                    ['J1_U', 'J1_D'],
                    [''    , 'J2_R'],
                    ['J3_L', 'J3_R'],
                    ['J3_U', 'J3_D'],
                    [''    , 'J2_L'],
                    ['JP_L', 'JP_R'],
                    ['JP_U', 'JP_D'],
            ]

        # TODO this is utterly untested
        elif platform.system() == 'Darwin':
            CodeTable =  [
                    ['J1_L', 'J1_R'],
                    ['J1_U', 'J1_D'],
                    ['J3_L', 'J3_R'],
                    # Currently no way to test more than three axes on Mac
#                    ['J3_L', 'J3_R'],
#                    ['J3_U', 'J3_D'],
#                    ['J2_L', 'J2_R'],
#                    ['JP_L', 'JP_R'],
#                    ['JP_U', 'JP_D'],
            ]
        return CodeTable
