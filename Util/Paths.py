import sys
from pathlib import Path

# Things related to paths for the app
#
# examine an arbitrary profile binds dir for its associated profile name
def CheckProfileForBindsDir(config, bindsdir, server = 'Homecoming') -> str:
    bindsloc = GetServerBindsPath(config, server) if config.ReadBool('RelativeBindsDir') else config.Read('BindPath')
    if bindsloc:
        if IDFile := Path(bindsloc) / bindsdir / 'bcprofileid.txt':
            # If the file is even there...
            if IDFile.exists():
                return IDFile.read_text().strip()
    return ''

# get a Path object given a profile name
def GetProfileFileForName(config, name) -> Path:
    return Path(config.Read('ProfilePath')) / f"{name}.bcp"

# get all profile binds dirs as a list of directory names (not full paths)
#
# Might want to case-mangle these in calling code if checking against them, but
# let's not do it inside here in case we want to touch them directly on Linux
# etc where changing the case inside here would be bad.
def GetAllProfileBindsDirs(config, server = 'Homecoming') -> list:
    alldirs = []
    bindsloc = GetServerBindsPath(config, server) if config.ReadBool('RelativeBindsDir') else config.Read('BindPath')

    if bindsloc:
        for bindsdir in Path(bindsloc).glob('*'):
            if bindsdir.is_dir():
                alldirs.append(bindsdir.name)
    return alldirs

# return the current Profile Path
def ProfilePath(config) -> Path: return Path(config.Read('ProfilePath'))

# This is for finding things like loadable modules for PowerBinder, icons, etc
# This relies on this file, Paths.py, staying exactly one level down, in /Util
def GetRootDirPath() -> Path:
    if base_path := getattr(sys, '_MEIPASS', ''):
        base_path = Path(base_path)
    else:
        base_path = Path(__file__).resolve().parent.parent

    return base_path

# returns the gamepath if it's valid, None otherwise
def GetValidGamePath(config, server:str) -> Path|None:
    pathvar = 'GamePath' if server == 'Homecoming' else 'GameRebirthPath'
    gamepath = Path(config.Read(pathvar))
    if server == 'Homecoming':
        binpath   = gamepath / 'bin'
        assetpath = gamepath / 'assets'
        if gamepath.is_dir() and gamepath.is_absolute() and binpath.is_dir() and assetpath.is_dir():
            return gamepath
    elif server == 'Rebirth':
        exepath = gamepath / 'Rebirth.exe'
        if gamepath.is_dir() and gamepath.is_absolute() and exepath.is_file():
            return gamepath
    else:
        raise Exception('GetValidGamePath got an unknown "server" passed in.  This is a bug')

def GetServerBindsPath(config, server: str) -> Path|None:
    if not GetValidGamePath(config, server): return None
    if server == 'Rebirth':
        return Path(config.Read('GameRebirthPath')) / 'piggs'
    else:
        return Path(config.Read('GamePath')) / 'settings' / 'live'

# returns the popmenu path for the server, regardless of whether it's there
def GetPopmenuPath(config, server) -> Path|None:
    menupath = GetValidGamePath(config, server)
    if not menupath: return

    gamelang = config.Read('GameLang')
    pathparts = ['data', 'Texts', gamelang, 'Menus']
    # Here's a wacky thing we do for Linux / Mac users:
    while pathparts:
        # walk through the parts and find them non-case-sensitively
        pathpart = pathparts.pop(0)
        pathglob = sorted(menupath.glob(pathpart, case_sensitive = False))
        # if we found it, add it in as found, otherwise as written
        menupath = pathglob[0] if pathglob else (menupath / pathpart)

    return menupath
