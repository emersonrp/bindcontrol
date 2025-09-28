# Constants and so forth for dealing with Incarnate stuff

import GameData
import Util.Incarnate

Rarities = ['Common', 'Uncommon', 'Uncommon', 'Rare', 'Rare', 'Rare', 'Rare', 'VeryRare', 'VeryRare']
Aliases = {
    "Banished Pantheon"   : "Banished",
    "Carnival of Shadows" : "Carnival",
    "Cimerorans"          : "Cimeroran",
    "Knives of Vengeance" : "Knives",
    "Phantom"             : "Phantoms",
    "Polar Lights"        : "Lights",
    "Robotic Drones"      : "Drones",
    "Storm Elementals"    : "Elementals",
    "Talons of Vengeance" : "Talons",
    "Warworks"            : "WarWorks",
}

SlotData = {}

# This builds the slotdata, which is basically a key->value for incarnate powers
# that contains HTML for the IncarnatePicker's use.  It could eventually expand to
# contain more info, with some work, possibly even hypothetical IncarnatePower()
# objects that could be kitted up to do interesting things.  Or this might be
# overengineered already.
#
# Call this from inside GameData.SetupGameData
def BuildSlotData() -> None:

    Util.Incarnate.SlotData.clear() # re-initialize this in case we change servers

    for slot, rawdata in GameData.IncarnatePowers.items():

        if slot == 'Lore':
            Util.Incarnate.SlotData['Lore'] = BuildLoreSlotData()
            continue

        slotdata = {}

        for typename, typedata in rawdata['Types'].items():
            slotdata[typename] = {}
            for i, levelname in enumerate(rawdata['Levels']):
                effecttext = ''
                for j, effectname in enumerate(typedata['Effects']):
                    effectdata = typedata['Levels'][i][j]
                    if isinstance(effectdata, int) and effectdata == 0:
                        continue
                    if isinstance(effectdata, list):
                        effectline = "<br>".join(effectdata)
                    elif isinstance(effectdata, str):
                        effectline = f"{effectdata}"
                    elif isinstance(effectdata, int) and effectdata == 1:
                        effectline = ''
                    else:
                        raise Exception(f'Something is terribly wrong with the incarnate data at {typename}, {i}, {j}: {effectdata}')
                    effecttext = effecttext + f"<dt><b>{effectname}</b></dt><dd>{effectline}</dd>"

                slotdata[typename][f'{typename} {levelname}'] = f"<dl>{effecttext}</dl>"

        Util.Incarnate.SlotData[slot] = slotdata

def BuildLoreSlotData():

    rawdata = GameData.IncarnatePowers['Lore']

    slotdata = {}

    for typename, typedata in rawdata['Types'].items():
        slotdata[typename] = {}
        for leveldata in rawdata['Levels']:
            effecttext = ''
            (levelname, mn, lt, bos, special, lvlshift) = leveldata

            if mn : effecttext = effecttext + f"Summon {typedata[0]}\n"
            if lt : effecttext = effecttext + f"Summon {typedata[1]}\n"
            if bos: effecttext = effecttext + f"Summon {typedata[2]}\n"
            if special:
                if special == "+DMG":
                    effecttext = effecttext + f"{special}\n"
                else:
                    effecttext = effecttext + f"{typedata[2]} {special}\n"
            if lvlshift: effecttext = effecttext + "Incarnate Level Shift\n"

            slotdata[typename][f'{typename} {levelname}'] = effecttext

    return slotdata
