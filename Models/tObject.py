from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pathlib import Path, PureWindowsPath
from BLF import BLF

class tObject(dict):
    def __init__(self, profile):
        self.togon   = "px_tgon" if profile.Server() == "Rebirth" else "powexectoggleon"
        self.togoff  = "px_tgof" if profile.Server() == "Rebirth" else "powexectoggleoff"

        self.profile            = profile
        self.ini          :str  = ''
        self.sprint       :str  = ''
        self.speed        :str  = ''
        self.hover        :str  = ''
        self.fly          :str  = ''
        self.gfly         :str  = ''
        self.flyx         :str  = ''
        self.jump         :str  = ''
        self.cjmp         :str  = ''
        self.canhov       :bool = False
        self.canfly       :bool = False
        self.canqfly      :bool = False
        self.cangfly      :bool = False
        self.cancj        :bool = False
        self.canjmp       :bool = False
        self.tphover      :str  = ''
        self.ttpgfly      :str  = ''
        self.on           :str  = f'$${self.togon} '
        self.off          :str  = f'$${self.togoff} '
        self.playerturn   :str  = ''
        self.mouselookon  :str  = ''
        self.mouselookoff :str  = ''
        self.runcamdist   :str  = ''
        self.flycamdist   :str  = ''
        self.detailhi     :str  = ''
        self.detaillo     :str  = ''
        self.NonSoDMode   :str  = ''
        self.SprintMode   :str  = ''
        self.FlyMode      :str  = ''
        self.JumpMode     :str  = ''
        self.SpeedMode    :str  = ''
        self.GFlyMode     :str  = ''
        self.jumpifnocj   :str  = ''

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

        # I am very close to making these into methods instead of static definitions
        self.pathr       : Path            = self.basepath     / 'R' / 'R' # run
        self.gamepathr   : PureWindowsPath = self.gamebasepath / 'R' / 'R'
        self.blr         : str             = f"$${BLF()} {self.gamepathr}"

        self.pathf       : Path            = self.basepath     / 'F' / 'F' # fly
        self.gamepathf   : PureWindowsPath = self.gamebasepath / 'F' / 'F'
        self.blf         : str             = f"$${BLF()} {self.gamepathf}"

        self.pathj       : Path            = self.basepath     / 'J' / 'J' # jump
        self.gamepathj   : PureWindowsPath = self.gamebasepath / 'J' / 'J'
        self.blj         : str             = f"$${BLF()} {self.gamepathj}"

        self.paths       : Path            = self.basepath     / 'S' / 'S' # speed
        self.gamepaths   : PureWindowsPath = self.gamebasepath / 'S' / 'S'
        self.bls         : str             = f"$${BLF()} {self.gamepaths}"

        self.pathgf      : Path            = self.basepath     / 'GF' / 'GF' # group fly
        self.gamepathgf  : PureWindowsPath = self.gamebasepath / 'GF' / 'GF'
        self.blgf        : str             = f"$${BLF()} {self.gamepathgf}"

        self.pathn       : Path            = self.basepath     / 'N' / 'N' # normal / non-sod
        self.gamepathn   : PureWindowsPath = self.gamebasepath / 'N' / 'N'
        self.bln         : str             = f"$${BLF()} {self.gamepathn}"

        self.pathar      : Path            = self.basepath     / 'AR' / 'AR'  # autorun ground
        self.gamepathar  : PureWindowsPath = self.gamebasepath / 'AR' / 'AR'
        self.blar        : str             = f"$${BLF()} {self.gamepathar}"

        self.pathaf      : Path            = self.basepath     / 'AF' / 'AF'  # autorun flight
        self.gamepathaf  : PureWindowsPath = self.gamebasepath / 'AF' / 'AF'
        self.blaf        : str             = f"$${BLF()} {self.gamepathaf}"

        self.pathaj      : Path            = self.basepath     / 'AJ' / 'AJ'  # autorun jump
        self.gamepathaj  : PureWindowsPath = self.gamebasepath / 'AJ' / 'AJ'
        self.blaj        : str             = f"$${BLF()} {self.gamepathaj}"

        self.pathas      : Path            = self.basepath     / 'AS' / 'AS'  # autorun speed
        self.gamepathas  : PureWindowsPath = self.gamebasepath / 'AS' / 'AS'
        self.blas        : str             = f"$${BLF()} {self.gamepathas}"

        self.pathagf     : Path            = self.basepath     / 'AGF' / 'AGF'  # autorun group fly
        self.gamepathagf : PureWindowsPath = self.gamebasepath / 'AGF' / 'AGF'
        self.blagf       : str             = f"$${BLF()} {self.gamepathagf}"

        self.pathan      : Path            = self.basepath     / 'AN' / 'AN' # autorun normal / non-sod
        self.gamepathan  : PureWindowsPath = self.gamebasepath / 'AN' / 'AN'
        self.blan        : str             = f"$${BLF()} {self.gamepathan}"

        self.pathfr      : Path            = self.basepath     / 'FR' / 'FR'  # Follow Run
        self.gamepathfr  : PureWindowsPath = self.gamebasepath / 'FR' / 'FR'
        self.blfr        : str             = f"$${BLF()} {self.gamepathfr}"

        self.pathff      : Path            = self.basepath     / 'FF' / 'FF'  # Follow Fly
        self.gamepathff  : PureWindowsPath = self.gamebasepath / 'FF' / 'FF'
        self.blff        : str             = f"$${BLF()} {self.gamepathff}"

        self.pathfj      : Path            = self.basepath     / 'FJ' / 'FJ'  # Follow Jump
        self.gamepathfj  : PureWindowsPath = self.gamebasepath / 'FJ' / 'FJ'
        self.blfj        : str             = f"$${BLF()} {self.gamepathfj}"

        self.pathfs      : Path            = self.basepath     / 'FS' / 'FS'  # Follow Speed
        self.gamepathfs  : PureWindowsPath = self.gamebasepath / 'FS' / 'FS'
        self.blfs        : str             = f"$${BLF()} {self.gamepathfs}"

        self.pathfgf     : Path            = self.basepath     / 'FGF' / 'FGF'  # Follow Group Fly
        self.gamepathfgf : PureWindowsPath = self.gamebasepath / 'FGF' / 'FGF'
        self.blfgf       : str             = f"$${BLF()} {self.gamepathfgf}"

        self.pathfn      : Path            = self.basepath     / 'FN' / 'FN' # Follow normal / non-sod
        self.gamepathfn  : PureWindowsPath = self.gamebasepath / 'FN' / 'FN'
        self.blfn        : str             = f"$${BLF()} {self.gamepathfn}"

        self.vertkeys  :int = 0
        self.horizkeys :int = 0
        self.jkeys     :int = 0
        self.totalkeys :int = 0

    # return binary "011010" string of which keys are "on";
    # optionally flipping one of them firsself.
    def KeyState(self, p : dict|None = None):
        p = p or {}
        togglebit = p.get('toggle', '')

        ret = ''
        for key in ('space','X','W','S','A','D'):
            retthing = int(getattr(self, key))
            if key == togglebit:
                ret = ret + str(1 - retthing)
            else:
                ret = ret + str(retthing)
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
