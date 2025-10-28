from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from pathlib import Path, PureWindowsPath
from BLF import BLF

class tObject(dict):
    def __init__(self, profile):
        self.togon   = "px_tgon" if profile.Server() == "Rebirth" else "powexectoggleon"
        self.togoff  = "px_tgof" if profile.Server() == "Rebirth" else "powexectoggleoff"

        self.profile             = profile
        self.ini           :str  = ''
        self.sprint        :str  = ''
        self.speed         :str  = ''
        self.hover         :str  = ''
        self.fly           :str  = ''
        self.gfly          :str  = ''
        self.flyx          :str  = ''
        self.jump          :str  = ''
        self.cjmp          :str  = ''
        self.canhov        :bool = False
        self.canfly        :bool = False
        self.cancj         :bool = False
        self.canjmp        :bool = False
        self.tphover       :str  = ''
        self.ttpgfly       :str  = ''
        self.on            :str  = f'$${self.togon} '
        self.off           :str  = f'$${self.togoff} '
        self.playerturn    :str  = ''
        self.mouselookon   :str  = ''
        self.mouselookoff  :str  = ''
        self.runcamdist    :str  = ''
        self.flycamdist    :str  = ''
        self.detailhi      :str  = ''
        self.detaillo      :str  = ''
        self.NonSoDModeKey :str  = ''
        self.SprintModeKey :str  = ''
        self.FlyModeKey    :str  = ''
        self.JumpModeKey   :str  = ''
        self.SpeedModeKey  :str  = ''
        self.GFlyModeKey   :str  = ''
        self.jumpifnocj    :str  = ''

        self.space:int = 0
        self.X    :int = 0
        self.W    :int = 0
        self.S    :int = 0
        self.A    :int = 0
        self.D    :int = 0
        self.up   :str = ''
        self.dow  :str = ''
        self.forw :str = ''
        self.bac  :str = ''
        self.lef  :str = ''
        self.rig  :str = ''
        self.upx  :str = ''
        self.dowx :str = ''
        self.forx :str = ''
        self.bacx :str = ''
        self.lefx :str = ''
        self.rigx :str = ''

        self.basepath     : Path            = profile.BindsDir()
        self.gamebasepath : PureWindowsPath = profile.GameBindsDir()

        self.horizkeys :int = 0
        self.jkeys     :int = 0
        self.totalkeys :int = 0

    def path(self, code):
        return self.basepath / code.upper() / code.upper()

    def gamepath(self, code):
        return self.gamebasepath / code.upper() / code.upper()

    def bl(self, code):
        return f"$${BLF()} {self.gamepath(code)}"

    def bfpath(self, code, suffix):
        return str(self.path(code)) + self.KeyState() + suffix + '.txt'

    # return binary "011010" string of which keys are "on";
    # optionally flipping one of them firsself.
    def KeyState(self, toggle: Literal['space', 'X', 'W', 'S', 'A', 'D', ''] = ''):

        ret = ''
        for key in ('space','X','W','S','A','D'):
            retthing = int(getattr(self, key))
            ret = ret + (str(1 - retthing) if key == toggle else str(retthing))

        return ret

    def dirs(self, dirs):
        dirdict = { 'U': 'up', "D": 'dow', "F": 'forw', "B": 'bac', "L": 'lef', "R": 'rig' }
        ret = ''
        for d in list(dirs):
           ret += getattr(self, dirdict[d])

        return ret

    # This will return "${BLF()} C:\path\CODE\CODE101010<suffix>.txt"
    def BLF(self, code, suffix = ''):
        return self.profile.BLF(code.upper(), code.upper() + self.KeyState() + suffix + '.txt')
