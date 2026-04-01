# vim: ft=python
import sys
from pathlib import Path

from PyInstaller.building.api import EXE, COLLECT, PYZ
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.osx import BUNDLE

# Add extra files in the PyInstaller-spec
extra_pyinstaller_files = [
    ('Fonts/', 'Fonts/'),
    ('icons/*.png', 'icons/'),
    ('icons/UI/', 'icons/UI/'),
    ('icons/Servers', 'icons/Servers/'),
    ('icons/BindControl.ico', 'icons/'),
    ('Help/', 'Help/'),
    ('UI/PowerBinderCommand/', 'UI/PowerBinderCommand/'),
    ('UI/BindWizard/', 'UI/BindWizard/'),
    ('popmenus/qwyPetMouse.mnu', 'popmenus/')
]

# first, extract the varsion from version.txt
version = 'no version found'
if versfile := Path('version.txt'):
    if versfile.exists():
        version = versfile.read_text()
        extra_pyinstaller_files.append(('version.txt', '.'))

extra_hidden_imports = ['PIL']

# go find our powerbinder commands
path = Path('UI/PowerBinderCommand')
for package_file in sorted(path.glob('*.py')):
    if package_file.stem == '__init__': continue
    extra_hidden_imports.append("UI.PowerBinderCommand." + package_file.stem)

# and our bindwizards
path = Path('UI/BindWizard')
for package_file in sorted(path.glob('*.py')):
    if package_file.stem == '__init__': continue
    extra_hidden_imports.append("UI.BindWizard." + package_file.stem)


if sys.platform == 'darwin':
    extra_pyinstaller_files.append(('tools/bcicon/BindControl.icns', '.'))
    version_info = None
elif sys.platform == 'windows':
    ...
else: # linux
    ...

a = Analysis(
    ['BindControl.py'],
    datas=extra_pyinstaller_files,
    hiddenimports=extra_hidden_imports,
    excludes=['_bz2', '_ctypes', '_decimal', '_hashlib', '_lzma', '_ssl'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BindControl',
    debug=False,
    bootloader_ignore_signals=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons/BindControl.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='BindControl',
)
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name="BindControl.app",
        icon="tools/bcicon/BindControl.icns",
        bundle_identifier="net.hayseed.bindcontrol",
        info_plist={
            "NSPrincipalClass": "NSApplication",
            "CFBundleShortVersionString": version,
            "NSHumanReadableCopyright": "emerson@hayseed.net",
            "CFBundleIdentifier": "net.hayseed.bindcontrol",
            "CFBundleDocumentTypes": [
                {
                    "CFBundleTypeExtensions": ["bcp"],
                    "CFBundleTypeIconFile": "tools/bcicon/BindControl.icns",
                    "CFBundleTypeMIMETypes": ["text/bcp"],
                    "CFBundleTypeName": "BindControl Profile",
                    "CFBundleTypeRole": "Viewer",
                    "LSTypeIsPackage": 0,
                }
            ],
            "LSEnvironment": {"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"},
            'ATSApplicationFontsPath': 'Fonts',
        },
    )
