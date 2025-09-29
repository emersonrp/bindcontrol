#!/usr/bin/env python3
import re
import wx
import pytest
from pathlib import Path
from Util.Incarnate import Aliases
import GameData
import Util.Paths
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

count = 0
filecheck = set()
for filename in Path(icondir / "Archetypes").glob('**/*.png'):
    filecheck.add(str(filename))
for filename in Path(icondir / "Origins").glob('**/*.png'):
    filecheck.add(str(filename))
for filename in Path(icondir / "Powers").glob('**/*.png'):
    filecheck.add(str(filename))
for filename in Path(icondir / "Incarnate").glob('**/*.png'):
    if not re.search('Disable.png', str(filename)): # hmm
        filecheck.add(str(filename))
for filename in Path(icondir / "Inspirations").glob('**/*.png'):
    filecheck.add(str(filename))

def test_archetype_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Archetype, Primary, and Secondary
        for archname, archdata in GameData.Archetypes.items():
            archname = re.sub(r'\W+', '', archname)
            filename = icondir / "Archetypes" / f"{archname}.png"
            assert filename.exists(), f"Archetype icon missing: {filename}"
            if str(filename) in filecheck: filecheck.remove(str(filename))

            for category in ['Primary', 'Secondary', 'Epic']:
                for powerset, powers in archdata[category].items():
                    powerset = re.sub(r'\W+', '', powerset)
                    for power in powers:
                        if isinstance(power, dict):
                            [(power, items)] = power.items()
                            for p in items:
                                p = re.sub(r'\W+', '', p)
                                filename = icondir / "Powers" / powerset / f"{p}.png"
                                assert filename.exists(), f"Powers icon missing: {filename}"
                                if str(filename) in filecheck: filecheck.remove(str(filename))
                        power = re.sub(r'\W+', '', power)
                        filename = icondir / "Powers" / powerset / f"{power}.png"
                        assert filename.exists(), f"Powers icon missing: {filename}"
                        if str(filename) in filecheck: filecheck.remove(str(filename))

def test_origin_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Origins
        for origin in GameData.Origins:
            filename = icondir / "Origins" / f"{origin}.png"
            assert filename.exists(), f"Origins icon missing: {filename}"
            if str(filename) in filecheck: filecheck.remove(str(filename))

def test_pool_power_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Pool Powers
        for poolname, pool in GameData.PoolPowers.items():
            for power in pool:
                power = re.sub(r'\W+', '', power)
                poolname = re.sub(r'\W+', '', poolname)
                filename = icondir / "Powers" / poolname / f"{power}.png"
                assert filename.exists(), f"Pool power icon missing: {filename}"
                if str(filename) in filecheck: filecheck.remove(str(filename))

def test_incarnate_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Incarnate Powers
        for slot, slotdata in GameData.IncarnatePowers.items():
            for inc_type in slotdata['Types']:
                aliasedtype = Aliases.get(inc_type, inc_type)
                for rarity in ['Common', 'Uncommon', 'Rare', 'VeryRare']:
                    filename = icondir / "Incarnate" / f"Incarnate_{slot}_{aliasedtype}_{rarity}.png"
                    assert filename.exists(), f"Incarnate icon missing: {filename}"
                    if str(filename) in filecheck: filecheck.remove(str(filename))

def test_miscpowers_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        # Misc Powers
        # TODO generalize this more?


        miscpowerlist = RecurseMiscPowers(GameData.MiscPowers)
        for power in miscpowerlist:
            power = re.sub(r'[^\w|]+', '', power)
            _, icon = SplitNameAndIcon(power)
            icon = '_'.join(icon)
            filename = icondir / "Powers" / "Misc" / f"{icon}.png"
            assert filename.exists(), f"Misc Powers icon missing: {filename}"
            if str(filename) in filecheck: filecheck.remove(str(filename))

def test_temppowers_icons_exist():
    for server in ['Homecoming', 'Rebirth']:
        GameData.SetupGameData(server)
        for power in GameData.TempTravelPowers:
            power = re.sub(r'[^\w|]+', '', power)
            _, icon = SplitNameAndIcon(power)
            icon = '_'.join(icon)
            filename = icondir / "Powers" / "Temp" / f"{icon}.png"
            assert filename.exists(), f"Temp Powers icon missing: {filename}"
            if str(filename) in filecheck: filecheck.remove(str(filename))

def test_inspiration_icons_exist():
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

def test_no_extra_icons():
    assert not filecheck, f"{len(filecheck)} extra icons exist: {filecheck}"

def test_transparent_png():
    _ = wx.App()
    assert Icon.transparentPNG is not None

def test_icon_class():
    _ = wx.App()
    empty = Icon.Icon(wx.Bitmap.NewFromPNGData(Icon.transparentPNG, len(Icon.transparentPNG)), 'Empty')
    assert empty.Filename == 'Empty'
    assert isinstance(empty, wx.BitmapBundle)

def test_geticon():
    _ = wx.App()
    assert len(Icon.Icons) == 0
    empty = Icon.GetIcon('Empty')
    assert isinstance(empty, wx.BitmapBundle)
    assert len(Icon.Icons) == 1

def test_geticon_fromzip(monkeypatch):
    _ = wx.App()
    monkeypatch.setattr(Util.Paths, 'GetRootDirPath', fixturepathzip)
    archicon = Icon.GetIcon('Archetypes', 'Tanker')
    assert isinstance(archicon, Icon.Icon), 'Gets from ZIP file without extension'
    assert len(Icon.Icons) == 2, 'Caches from ZIP file without extension'

    alignicon = Icon.GetIcon('Alignments', 'Hero.png')
    assert isinstance(alignicon, Icon.Icon), 'Gets from ZIP file with extension'
    assert len(Icon.Icons) == 3, 'Caches from ZIP file with extension'

    monkeypatch.setattr(wx, 'LogError', raises_exception)
    with pytest.raises(Exception, match = 'RAISES: Loading icon'):
        Icon.GetIcon('Gibberish', 'Not', 'Here')

    monkeypatch.undo()

def test_geticon_fromfile(monkeypatch):
    _ = wx.App()
    monkeypatch.setattr(Util.Paths, 'GetRootDirPath', fixturepathfs)

    flyicon = Icon.GetIcon('Powers', 'Flight', 'Fly')
    assert isinstance(flyicon, Icon.Icon), 'Gets from filesystem'
    assert len(Icon.Icons) == 4, 'Caches from filesystem'

    frosticon = Icon.GetIcon('Powers', 'Icy Assault', 'Frost Breath')
    assert isinstance(frosticon, Icon.Icon), 'Gets with spaces in name'
    assert len(Icon.Icons) == 5, 'Caches with spaces'

    monkeypatch.setattr(wx, 'LogWarning', raises_exception)
    with pytest.raises(Exception, match = 'RAISES: Missing icon'):
        Icon.GetIcon('Gibberish', 'Not', 'Here')

    monkeypatch.undo()

def test_geticonbitmap(monkeypatch):
    monkeypatch.setattr(Util.Paths, 'GetRootDirPath', fixturepathfs)
    archbmp = Icon.GetIconBitmap('Archetypes', 'Tanker')
    assert isinstance(archbmp, wx.Bitmap)

#####
def fixturepathzip():
    return Path(__file__).resolve().parent / 'fixtures' / 'iconszip'

def fixturepathfs():
    return Path(__file__).resolve().parent / 'fixtures' / 'iconsfs'

def raises_exception(ex_input): raise(Exception(f"RAISES: {ex_input}"))
