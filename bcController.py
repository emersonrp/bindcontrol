# Utility class for querying joystick/controller
import wx
import wx.adv

class bcController(wx.adv.Joystick):

    def __init__(self):
        wx.adv.Joystick.__init__(self)
        self.AxisStates = [None] * self.GetNumberAxes() # ["JOYSTICK1_UP", None, None, etc etc]
        self.CurrentAxis = ''

    def SetCurrentAxis(self):
        # TODO - matrix of platform / controller options call out to versions of SetCurrentAxis_*
        self.SetCurrentAxis_Linux_X360()

    def SetCurrentAxis_Linux_X360(self):
        current_axis_percents = [0] * self.GetNumberAxes() # ["JOYSTICK1_UP", None, None, etc etc]

        for axis in range(0, self.GetNumberAxes()):

            # TODO - this code makes assumptions about which axes are "centered" and "uncentered"
            # and about the range of the dpad.  This works for my Logitech 310 but possibly nothing
            # else.  This will take some third-party testing
            apos = self.GetPosition(axis)
            if axis == 0:
                amin, amax = self.GetXMin(), self.GetXMax()
                current_axis_percents[axis]= self.CenteredAxisPercent(amin, amax, apos)
                # Joystick1_LEFT, Joystick1_RIGHT
            elif axis == 1:
                amin, amax = self.GetYMin(), self.GetYMax()
                current_axis_percents[axis]= self.CenteredAxisPercent(amin, amax, apos)
                # Joystick1_UP, Joystick1_DOWN
            elif axis == 2: # rudder is uncentered
                amin, amax = self.GetRudderMin(), self.GetRudderMax()
                current_axis_percents[axis]= self.UncenteredAxisPercent(amin, amax, apos)
                # Joystick3_LEFT, Joystick3_RIGHT
            elif axis == 3:
                amin, amax = self.GetZMin(), self.GetZMax()
                current_axis_percents[axis]= self.CenteredAxisPercent(amin, amax, apos)
                # Joystick3_UP, Joystick3_DOWN
            elif axis == 4:
                amin, amax = self.GetUMin(), self.GetUMax()
                current_axis_percents[axis]= self.CenteredAxisPercent(amin, amax, apos)
                # Joystick2_RIGHT
            elif axis == 5: # v is uncentered
                amin, amax = self.GetVMin(), self.GetVMax()
                current_axis_percents[axis]= self.UncenteredAxisPercent(amin, amax, apos)
                # Joystick2_LEFT
            elif axis in [6,7]:
                amin, amax = -32767, 32767
                current_axis_percents[axis]= self.CenteredAxisPercent(amin, amax, apos)
                # JOYPAD_*

        current_axis = current_axis_percents.index(max(current_axis_percents, key=abs))

        code = ''
        if current_axis == 0:
            if current_axis_percents[current_axis] < -50:
                code = "J1_L"
            elif current_axis_percents[current_axis] > 50:
                code = "J1_R"
        elif current_axis == 1:
            if current_axis_percents[current_axis] < -50:
                code = "J1_U"
            elif current_axis_percents[current_axis] > 50:
                code = "J1_D"
        elif current_axis == 2:
            if current_axis_percents[current_axis] > 50:
                code = "J2_R"
        elif current_axis == 3:
            if current_axis_percents[current_axis] < -50:
                code = "J3_L"
            elif current_axis_percents[current_axis] > 50:
                code = "J3_R"
        elif current_axis == 4:
            if current_axis_percents[current_axis] < -50:
                code = "J3_U"
            elif current_axis_percents[current_axis] > 50:
                code = "J3_D"
        elif current_axis == 5:
            if current_axis_percents[current_axis] > 50:
                code = "J2_L"
        elif current_axis == 6:
            if current_axis_percents[current_axis] < -50:
                code = "JP_L"
            elif current_axis_percents[current_axis] > 50:
                code = "JP_R"
        elif current_axis == 7:
            if current_axis_percents[current_axis] < -50:
                code = "JP_U"
            elif current_axis_percents[current_axis] > 50:
                code = "JP_D"

        if code:
            self.CurrentAxis = code


    def CenteredAxisPercent(self, amin, amax, apos):
        center = amin + ((amax - amin) / 2)
        if apos > center:
            return int(apos / (amax - center) * 100)
        else:
            return int(apos / (center - amin) * 100)

    def UncenteredAxisPercent(self, amin, amax, apos):
        # uncentered axes, on XBox 360 controllers, start at
        # -50% and go to 50%, so mash these values so they 0-100
        apos = apos + amax; amin = amin + amax;  amax = amax + amax
        return int(apos / (amax - amin) * 100)