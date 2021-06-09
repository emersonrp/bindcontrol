import json 
import requests
import pprint

# TODO - save cached version, touch it back up every once in a while.
# TODO - or make it a menu item, "Refresh Game Data"

def GetDataFromWeb():


    Archetypes = {}

    # we start at the top
    topr = requests.get("https://coh.tips/powers/v2/")
    toplvldata = topr.json()

    # iterate all the power categories and sort them by archetype
    for cat in toplvldata['power_categories']:
        atinfo = cat.get('archetype', None)
        if atinfo: # might be Epic or other, will do those down below
            if not Archetypes.get(atinfo['name'], None):
                Archetypes[atinfo['name']] = {}
            Archetypes[atinfo['name']][atinfo['primary_or_secondary']] = {}

            # go get at's powerset data
            psr = requests.get(cat['url'])
            powerset_data = psr.json()

            for powercat in powerset_data['power_sets']:
                Archetypes[atinfo['name']][atinfo['primary_or_secondary']][powercat['display_name']] = []

                # go get powerset's details
                psr = requests.get(powercat['url'])
                powercat_data = psr.json()

                for powerset in powercat_data['powers']:
                    Archetypes[atinfo['name']][atinfo['primary_or_secondary']][powercat['display_name']].append(powerset['display_name'])

    Output_Archetypes = { 'Archetypes' : Archetypes }
    pp = pprint.PrettyPrinter(indent=1, width=132)
    pp.pprint(Output_Archetypes)



GetDataFromWeb()
