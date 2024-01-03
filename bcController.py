# Utility class for querying joystick/controller
import wx
import wx.adv

class bcController(wx.adv.Joystick):

    def __init__(self):
        wx.adv.Joystick.__init__(self)
        self.CurrentAxis = ''
        self.SetCodeTable()

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
                amin, amax = self.GetRudderMin(), self.GetRudderMax()
                # normalize this to 0 - 65535 on Linux.  Find a better way if needed
                if wx.Platform == "__WXGTK__":
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
                # normalize this to 0 - 65535 on Linux.  Find a better way if needed
                if wx.Platform == "__WXGTK__":
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

    def SetCurrentAxis(self):
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

            current_axis = self.CurrentAxisPercents.index(max(self.CurrentAxisPercents, key=abs))

            current_dir = None

            if self.CurrentAxisPercents[current_axis] < -50:
                current_dir = 0
            elif self.CurrentAxisPercents[current_axis] > 50:
                current_dir = 1

            if current_dir != None:
                code = self.CodeTable[current_axis][current_dir]

        if code:
            self.CurrentAxis = code

    def StickIsNearCenter(self):
        return abs(max(self.CurrentAxisPercents, key=abs)) < 50

    def AxisPercent(self, amin, amax, apos):
        center = amin + ((amax - amin) / 2)
        # (apos - center) is the distance, positive or negative, from the center
        # (amax - center) is the (positive) total throw on one side of center
        return int((apos - center) / (amax - center) * 100)

    def SetCodeTable(self):
        # sets the Code table, which is a list, indexed by axis number,
        # of lists of [negative direction, positive direction] codes
        if wx.Platform == '__WXMSW__':
            self.CodeTable =  [
                    ['J1_L', 'J1_R'],
                    ['J1_U', 'J1_D'],
                    ['J2_L', 'J2_R'],
                    ['J3_U', 'J3_D'],
                    ['J3_L', 'J3_R'],
                    ['J2_L', 'J2_R'],
                    ['JP_L', 'JP_R'],
                    ['JP_U', 'JP_D'],
            ]

        elif wx.Platform == '__WXGTK__':
            self.CodeTable =  [
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
        elif wx.Platform == '__WXMAC__':
            self.CodeTable =  [
                    ['J1_L', 'J1_R'],
                    ['J1_U', 'J1_D'],
                    ['J2_L', 'J2_R'],
                    ['J3_L', 'J3_R'],
                    ['J3_U', 'J3_D'],
                    ['J2_L', 'J2_R'],
                    ['JP_L', 'JP_R'],
                    ['JP_U', 'JP_D'],
            ]
