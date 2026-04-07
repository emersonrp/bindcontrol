import re
import wx
import pytest
from pathlib import Path
from Util.Incarnate import Aliases
import GameData
import Util.Paths
from Util.SourceFileIcons import GetImageFromSourceFile, sourcemaps, SourceCache
import Icon

def RecurseMiscPowers(menustruct):
    powerlist = []

    for data in menustruct.values():
        if isinstance(data, dict):
            plist = RecurseMiscPowers(data)
            powerlist.extend(plist)
        elif isinstance(data, list):
            for item in data:
                powerlist.append(item)

    return powerlist

def SplitNameAndIcon(namestr):
    if re.search(r'\|', namestr):
        name, iconstr = re.split(r'\|', namestr)
        iconlist = re.split(r'_', iconstr)
        return [name, iconlist]
    else:
        return [namestr, [namestr]]

icondir = Util.Paths.GetRootDirPath() / 'icons'

def test_geticon(empty):
    _ = wx.App()
    assert isinstance(empty, wx.BitmapBundle)
    assert len(Icon.Icons) == 1

def test_source_files():

    for source in sourcemaps:

        powerlist  = list(sourcemaps[source]['list'])
        powercount = len(powerlist)
        GetImageFromSourceFile(source, powerlist[0]) # to cache the source file

        sourcefile = SourceCache[source]
        assert sourcefile is not None
        assert sourcefile.height == 32
        assert sourcefile.width  == (32 * powercount)

def test_archetype_icons(empty):
    archcheck = set()
    powcheck = set()

    # marshal set of existing Archetype icons
    for filename in Path(icondir / "Archetypes").glob('**/*.png'):
        archcheck.add(str(filename))

    # marshal set of existing Powers icons
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Archetype, Primary, and Secondary
        for archdata in GameData.Archetypes.values():
            for category in ['Primary', 'Secondary', 'Epic']:
                for powerset in archdata[category]:
                    for filename in Path(icondir / "Powers" / powerset).glob('**/*.png'):
                        powcheck.add(str(filename))

    # walk GameData, check if icons there, remove from "existing" sets
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Archetype, Primary, and Secondary
        for archname, archdata in GameData.Archetypes.items():
            archname = re.sub(r'\W+', '', archname)
            filename = icondir / "Archetypes" / f"{archname}.png"
            assert filename.exists(), f"Archetype icon missing: {filename}"
            if str(filename) in archcheck: archcheck.remove(str(filename))

            for category in ['Primary', 'Secondary', 'Epic']:
                for powerset, powers in archdata[category].items():
                    powerset = re.sub(r'\W+', '', powerset)
                    for power in powers:
                        if isinstance(power, dict):
                            [(power, items)] = power.items()
                            for p in items:
                                p = re.sub(r'\W+', '', p)
                                filename = icondir / "Powers" / f"{powerset}_{p}.png"
                                assert filename.exists(), f"Powers icon missing: {filename}"
                                if str(filename) in powcheck: powcheck.remove(str(filename))

                                sourceicon = GetImageFromSourceFile('Powers', f'{powerset}_{p}')
                                assert isinstance(sourceicon, wx.Image)
                                assert sourceicon != empty, f'{powerset}_{p}" in source file'
                        power = re.sub(r'\W+', '', power)
                        filename = icondir / "Powers" / f"{powerset}_{power}.png"
                        assert filename.exists(), f"Powers icon missing: {filename}"
                        if str(filename) in powcheck: powcheck.remove(str(filename))
    assert not archcheck, f"{len(archcheck)} extra Archetype icons exist: {archcheck}"
    assert not powcheck,  f"{len(powcheck)} extra Powerset icons exist: {powcheck}"

def test_pool_power_icons():
    filecheck = set()

    # marshal set of existing Pool Power icons
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Pool Powers
        for poolname, _ in GameData.PoolPowers.items():
            for filename in Path(icondir / "Powers" / poolname).glob('**/*.png'):
                filecheck.add(str(filename))

    # iterate GameData and check for icon files and source icons
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Pool Powers
        for poolname, pool in GameData.PoolPowers.items():
            for power in pool:
                power = re.sub(r'\W+', '', power)
                poolname = re.sub(r'\W+', '', poolname)
                filename = icondir / "Powers" / f"{poolname}_{power}.png"
                assert filename.exists(), f"Pool power icon missing: {filename}"
                if str(filename) in filecheck: filecheck.remove(str(filename))

                sourceicon = GetImageFromSourceFile('Powers', f'{poolname}_{power}')
                assert isinstance(sourceicon, wx.Image)
                assert sourceicon != empty, f'{poolname}_{power} in source file'

    assert not filecheck, f"{len(filecheck)} extra Powers icons exist: {filecheck}"

def test_incarnate_icons():
    filecheck = set()
    for filename in Path(icondir / "Incarnate").glob('**/*.png'):
        if not re.search('Disable.png', str(filename)): # hmm
            filecheck.add(str(filename))
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Incarnate Powers
        for slot, slotdata in GameData.IncarnatePowers.items():
            for inc_type in slotdata['Types']:
                aliasedtype = Aliases.get(inc_type, inc_type)
                for rarity in ['Common', 'Uncommon', 'Rare', 'VeryRare']:
                    filename = icondir / "Incarnate" / f"{slot}_{aliasedtype}_{rarity}.png"
                    assert filename.exists(), f"Incarnate icon missing: {filename}"
                    if str(filename) in filecheck: filecheck.remove(str(filename))
    assert not filecheck, f"{len(filecheck)} extra Incarnate icons exist: {filecheck}"

def test_miscpowers_icons(empty):
    filecheck = set()
    for filename in Path(icondir / "Powers").glob('Misc_*.png'):
        filecheck.add(str(filename))
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Misc Powers
        # TODO generalize this more?

        miscpowerlist = RecurseMiscPowers(GameData.MiscPowers)
        for power in miscpowerlist:
            power = re.sub(r'[^\w|]+', '', power)
            _, icon = SplitNameAndIcon(power)
            icon = '_'.join(icon)
            filename = icondir / "Powers" / f"Misc_{icon}.png"
            assert filename.exists(), f"Misc Powers icon missing: {filename}"
            if str(filename) in filecheck: filecheck.remove(str(filename))

            sourceicon = GetImageFromSourceFile('Powers', f'Misc_{icon}')
            assert isinstance(sourceicon, wx.Image)
            assert sourceicon != empty, f'Misc_{icon} in source file'

    assert not filecheck, f"{len(filecheck)} extra Misc Power icons exist: {filecheck}"

def test_temppowers_icons():
    filecheck = set()
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        for filename in Path(icondir / "Powers").glob('Temp_*.png'):
            filecheck.add(str(filename))
        for power in GameData.TempTravelPowers:
            power = re.sub(r'[^\w|]+', '', power)
            _, icon = SplitNameAndIcon(power)
            icon = '_'.join(icon)
            filename = icondir / "Powers" / f"Temp_{icon}.png"
            assert filename.exists(), f"Temp Powers icon missing: {filename}"
            if str(filename) in filecheck: filecheck.remove(str(filename))
    assert not filecheck, f"{len(filecheck)} extra Temp Power icons exist: {filecheck}"

def test_inspiration_icons():
    filecheck = set()
    for filename in Path(icondir / "Inspirations").glob('**/*.png'):
        filecheck.add(str(filename))
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Inspirations
        for _, insp_type in GameData.Inspirations.items():
            for _, data in insp_type.items():
                for insp in data['tiers']:
                    insp = re.sub(r'\W+', '',  insp)
                    filename = icondir / "Inspirations" / f"{insp}.png"
                    assert filename.exists(), f"Inspiration icon missing: {filename}"
                    if str(filename) in filecheck: filecheck.remove(str(filename))
    assert not filecheck, f"{len(filecheck)} extra Inspiration icons exist: {filecheck}"

def test_transparent_png():
    _ = wx.App()
    assert Icon.transparentPNG is not None

def test_icon_class():
    _ = wx.App()
    empty = Icon.Icon(wx.Bitmap.NewFromPNGData(Icon.transparentPNG, len(Icon.transparentPNG)), 'Empty')
    assert empty.Filename == 'Empty'
    assert isinstance(empty, wx.BitmapBundle)

def test_geticon_fromfile(monkeypatch, empty):
    _ = wx.App()
    monkeypatch.setattr(Util.Paths, 'GetRootDirPath', fixturepathfs)

    copyicon = Icon.GetIcon('UI', 'copy')
    assert isinstance(copyicon, Icon.Icon), 'Gets from filesystem'
    assert copyicon != empty, 'Gets the actual icon not the empty one'
    assert len(Icon.Icons) == 2, 'Caches from filesystem'

    monkeypatch.setattr(wx, 'LogWarning', raises_exception)
    with pytest.raises(Exception, match = 'RAISES: Missing icon'):
        Icon.GetIcon('Gibberish', 'Not', 'Here')

    monkeypatch.undo()

def test_geticonbitmap(monkeypatch):
    monkeypatch.setattr(Util.Paths, 'GetRootDirPath', fixturepathfs)
    archbmp = Icon.GetIconBitmap('Archetypes', 'Tanker')
    assert isinstance(archbmp, wx.Bitmap)

def test_splitnameandicon():
    assert Icon.SplitNameAndIcon('testone') == ['testone', ['testone']]
    assert Icon.SplitNameAndIcon('testtwo|moretest') == ['testtwo', ['moretest']]
    assert Icon.SplitNameAndIcon('testthree|longer_test_string') == ['testthree', ['longer', 'test', 'string']]

#####
def fixturepathfs():
    return Path(__file__).resolve().parent / 'fixtures' / 'iconsfs'

def raises_exception(ex_input): raise(Exception(f"RAISES: {ex_input}"))

@pytest.fixture
def empty():
    return Icon.GetIcon('Empty')
