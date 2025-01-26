import PyInstaller.__main__
import platform, subprocess
from pathlib import Path

version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip('\r\n')
versionfile = Path('version.txt')
versionfile.write_text(version)

params = [
    'BindControl.py',
    '--noconfirm',
    '--clean',
    '--add-data=icons;icons',
    '--add-data=Help;Help',
    '--add-data=version.txt;.',
    '--add-data=UI/PowerBinderCommand;PowerBinderCommand',
    '--exclude-module=_bz2',
    '--exclude-module=_ctypes',
    '--exclude-module=_decimal',
    '--exclude-module=_hashlib',
    '--exclude-module=_lzma',
    '--exclude-module=_socket',
    '--exclude-module=_ssl',
]

if platform.system() == "Darwin":
    params.append('-i=tools/bcicon/BindControl.icns')
else:
    params.append('-i=icons/BindControl.ico')


path = Path('UI/PowerBinderCommand')
for package_file in sorted(path.glob('*.py')):
    if package_file.stem == '__init__': continue
    modstr = "UI.PowerBinderCommand." + package_file.stem
    params.append(f'--hidden-import={modstr}')

PyInstaller.__main__.run(params)

