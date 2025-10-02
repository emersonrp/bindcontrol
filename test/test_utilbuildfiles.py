import Util.BuildFiles
from pathlib import Path

def test_ParseBuildFiles(tmp_path):
    badfile = tmp_path / 'nothere.txt'
    badfile.touch()
    assert Util.BuildFiles.ParseBuildFile(badfile) == {}

    badfile.write_text('This is not a valid build file.')
    assert Util.BuildFiles.ParseBuildFile(badfile) == {}
    badfile.unlink()

    fixture = Path(__file__).resolve().parent / 'fixtures' / 'buildfile.txt'

    data = Util.BuildFiles.ParseBuildFile(fixture)

    assert data['Name'] == 'Fixture'
    assert data['Archetype'] == 'Tanker'
    assert data['Origin'] == 'Magic'
    assert data['Server'] == 'Homecoming'
    assert data['Primary'] == 'Fiery Aura'
    assert data['Secondary'] == 'War Mace'
    assert data['Pool1'] == 'Flight'
    assert data['Pool2'] == 'Fighting'
    assert data['Pool3'] == 'Leadership'
    assert data['Epic'] == 'Soul Mastery'
    assert data['Fiery Aura'] == ['Fire Shield', 'Healing Flames', 'Blazing Aura', 'Plasma Shield', 'Burn', 'Temperature Protection']
    assert data['War Mace'] == ['Bash', 'Pulverize', 'Taunt', 'Whirling Mace', 'Clobber', 'Crowd Control', 'Build Up']
    assert data['Flight'] == ['Combat Flight', 'Fly', 'Fly Boost']
    assert data['Fighting'] == ['Boxing', 'Tough', 'Weave']
    assert data['Leadership'] == ['Defense', 'Tactics', 'Assault', 'Vengeance']
    assert data['Soul Mastery'] == ['Gloom', 'Darkest Night']
