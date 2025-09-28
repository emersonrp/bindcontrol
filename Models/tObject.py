from pathlib import Path, PureWindowsPath

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

        self.bl    :str = ''
        self.bla   :str = ''
        self.blaf  :str = ''
        self.blaj  :str = ''
        self.blan  :str = ''
        self.blas  :str = ''
        self.blat  :str = ''
        self.blf   :str = ''
        self.blff  :str = ''
        self.blfn  :str = ''
        self.blfj  :str = ''
        self.blfs  :str = ''
        self.blft  :str = ''
        self.blfr  :str = ''
        self.blgr  :str = ''
        self.blga  :str = ''
        self.blgaf :str = ''
        self.blgff :str = ''
        self.blj   :str = ''
        self.bln   :str = ''
        self.bls   :str = ''
        self.blt   :str = ''

        self.path    :Path = Path()
        self.patha   :Path = Path()
        self.pathaf  :Path = Path()
        self.pathaj  :Path = Path()
        self.pathan  :Path = Path()
        self.pathas  :Path = Path()
        self.pathat  :Path = Path()
        self.pathf   :Path = Path()
        self.pathff  :Path = Path()
        self.pathfn  :Path = Path()
        self.pathfj  :Path = Path()
        self.pathfs  :Path = Path()
        self.pathft  :Path = Path()
        self.pathfr  :Path = Path()
        self.pathga  :Path = Path()
        self.pathgaf :Path = Path()
        self.pathgff :Path = Path()
        self.pathgr  :Path = Path()
        self.pathj   :Path = Path()
        self.pathn   :Path = Path()
        self.paths   :Path = Path()
        self.patht   :Path = Path()

        self.gamepath   :PureWindowsPath = PureWindowsPath()
        self.gamepatha  :PureWindowsPath = PureWindowsPath()
        self.gamepathaf :PureWindowsPath = PureWindowsPath()
        self.gamepathaj :PureWindowsPath = PureWindowsPath()
        self.gamepathan :PureWindowsPath = PureWindowsPath()
        self.gamepathas :PureWindowsPath = PureWindowsPath()
        self.gamepathat :PureWindowsPath = PureWindowsPath()
        self.gamepathf  :PureWindowsPath = PureWindowsPath()
        self.gamepathff :PureWindowsPath = PureWindowsPath()
        self.gamepathfn :PureWindowsPath = PureWindowsPath()
        self.gamepathfj :PureWindowsPath = PureWindowsPath()
        self.gamepathfs :PureWindowsPath = PureWindowsPath()
        self.gamepathft :PureWindowsPath = PureWindowsPath()
        self.gamepathfr :PureWindowsPath = PureWindowsPath()
        self.gamepathga :PureWindowsPath = PureWindowsPath()
        self.gamepathgr :PureWindowsPath = PureWindowsPath()
        self.gamepathj  :PureWindowsPath = PureWindowsPath()
        self.gamepathn  :PureWindowsPath = PureWindowsPath()
        self.gamepaths  :PureWindowsPath = PureWindowsPath()
        self.gamepatht  :PureWindowsPath = PureWindowsPath()

        self.basepath     :Path = Path()
        self.gamebasepath :PureWindowsPath = PureWindowsPath()

        self.vertkeys  :int = 0
        self.horizkeys :int = 0
        self.jkeys     :int = 0
        self.totalkeys :int = 0

    # return binary "011010" string of which keys are "on";
    # optionally flipping one of them first.
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
