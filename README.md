# BindControl

<b>NEW!</b>  Check out the new work-in-progress [Getting Started with BindControl](https://github.com/emersonrp/bindcontrol/wiki/Getting-Started-With-BindControl) on the wiki!

<b>NEW!</b>  BindControl now has beta support for Rebirth!  Come set up keybinds for your Guardian!

<hr>

BindControl is a helper app for creating and maintaining keybinds and popmenus for City of Heroes.

It is an enhanced port of Konoko and Monorail's [CityBinder 0.76](http://sourceforge.net/projects/citybinder/), using Python and the WxWidgets UI toolkit.

During City of Heroes' original run, CityBinder was the go-to app for keybinds.  It's written in lua, using the IUP toolkit, and the required versions of those can be difficult to set up for development on modern OSes.  I wanted to add features and clean up the UI, so in a stunningly unwise act of hubris, I instead started work on BindControl.

I worked on it on-and-off for the remainder of the original run of the game, then shelved it, ostensibly forever.  Now here in the age of the SCORE, Homecoming, and other servers, it once again has value, so I've dusted it off and continued to add features and modernize it.

BindControl is and has been developed on Homecoming, and best supports that.  Recently, beta support for Rebirth has been added, supporting archetypes, powersets, the Genesis Incarnate slot, and more.  This support is solid but is a work in progress -- Rebirth players, check it out and file issues as you find bugs!

![image](https://github.com/user-attachments/assets/3faeee00-9ba5-42fd-bf1b-112f7f0a58ef)

## Features

* Runs on Windows, MacOS, and Linux
* Separate profiles for different characters, archetypes, or situations
* Controller support
* Basic Gameplay Binds
    * One-key next-teammate / previous-teammate selection, with support for setting team size and optionally skipping the player in the next/previous rotation
    * Rebind the keys for the in-game power tray buttons
    * Various helpful shortcut binds, "Quit to Desktop", "Invite Target", "Show FPS", "Show Netgraph" - more to come
    * Chat binds with optional 'typing' notifier

* Custom Binds
    * Create simple binds using PowerBinder, a flexible tool for stringing together arbitrary commands for keybinding
    * Complex binds, chains of PowerBinder actions that fire sequentially on multiple presses of a keybind
    * Buffer binds, allowing quick one-key buffing of each teammate and/or pet

* Movement / Speed-on-Demand
    * Speed-on-Demand based on [CityBinder](http://sourceforge.net/projects/citybinder/) and the original Gnarly's SoD keybinds
    * Supports all formal travel powers:  Fly, Mystic Flight, Group Fly, Super Jump, Mighty Leap, Super Speed, Speed of Sound, Teleport, and Team Teleport
    * Secondary / server tray travel powers like Super Jump's "Double Jump" and Mystic Flight's "Translocation" are starting to be better integrated
    * Homecoming's <code>powexec_location cursor</code> feature incorporated into Teleport binds, with "teleport immediately" and "teleport on key release" options available
    * Kheldian form toggles;  Kheldian movement powers incorporated into Speed-on-Demand
    * Simple Temporary Travel Power toggle keybind
    * One-key reset in case SoD binds get tangled up

* Inspiration Popper
    * By-type; dual and team inspirations supported
    * Option to use or skip "super" inspirations
    * Largest-first or smallest-first
    * Optional /say feedback with per-inspiration custom colors

* Mastermind / Pet Binds
    * Select pets by power level: all, minions, lieutenants, and boss
    * Orders for aggressive / defensive / passive stances; attack, follow, go to, and stay, for all or selected pets
    * Pets can give feedback on each order;  chattiness can be toggled via keybind
    * "Bodyguard mode" shortcut -- you can define which pets should be treated as bodyguards, and turn Bodyguard Mode on for them with a single keypress[^1]
    * By-name pet selection
    * Next-pet / previous-pet binds

* Popmenu Editor (beta)
    * Install, edit, and delete popmenus in the correct game folder
    * Easy GUI editing and testing of popmenus
    * Generate macros to make popmenu buttons in-game

## TODO

* It's gotten a lot better, but there are still some Homecoming-specific notions hard-coded into BindControl.  I'm working on finding and fixing these, but any bug reports and other feedback from Rebirth players would be very welcomed.
* The hope is to make every reasonable slash command in the game available in some way, typically via PowerBinder.  What qualifies as a "reasonable slash command" is yet to be determined.
* Access to MacOS for testing is via a MacOS VM several OS versions old.  I don't want to buy an actual Mac just for this wee vanity project, so mileage may vary on how it acts in an actual recent Mac environment.
* The Movement Powers page is a confusing forest of checkboxes, dating from the original CityBinder layout and needs some layout and documentation work <i>(WIP)</i>.
* "Bodyguard mode" as implemented in CityBinder doesn't work as intended, and might not be able to due to game restrictions.
* Investigate improvements to Mastermind binds to clarify and expand the behavior.
* The popmenu editor, on Windows, simply can't load pathologically large popmenus (tens of thousands of entries).  This is a hard limit on the wx toolkit imposed by Windows itself, and can't be worked around in any way I can see.  As there exist at least two menus this large "in the wild," further investigation is merited.
* More error detection and handling.
* More and better help text and documentation.
* Fix bugs as found.
* More internal work on initialization order of objects to speed up start time and avoid bootstrapping problems <i>(WIP)</i>.

## Using Binary Releases

Binary releases of Python applications are a bit finicky and fragile, but are provided on the [latest release page](https://github.com/emersonrp/bindcontrol/releases).  Feel free to try them, but if you have any trouble, skip down to [Running From Source](#running-from-source) below for an alternative, very deterministic, way of running BindControl.  Any feedback on your experience with the binary releases is welcome and encouraged.

*Windows users*:  Try the ZIP file.  If that works for you, it's the quickest path to victory.  ***If you receive malware warnings when downloading***, please read [my comments on that issue](Help/MalwareWarnings.md).

*MacOS users*:  An experimental binary release has been made available.  It is not signed and/or notarized, and might or might not work at all.

*Linux users*:  An experimental binary release is now available.  You should be able to unzip the zipfile anywhere, and run the "BindControl" binary from within it.  It's built using Github's "ubuntu-latest" environment, which may or may not be completely compatible with other distributions and versions.[^2]

## Running From Source

### Step 1 - Dependencies

1. [Python](https://www.python.org) version 3.13 or later
2. [wxPython](https://www.wxpython.org) version 4.2.2 or later

*Windows users*:  follow the instructions on the above sites' download pages to install Python and wxPython.

*MacOS users*:
* Pre-Catalina:  I recommend following the instructions in [this article at opensource.com](https://www.opensource.com/article/19/5/python-3-default-mac) to get Python 3 installed and working as the default Python.  Once Python 3 is working, you will want to run `pip3 install wxPython`.
* Catalina and later: follow the instructions on the above sites' download pages to install Python and wxPython.

*Linux users*:  install your distribution's packages for Python 3 and wxPython.

### Step 2 - Getting and running the code

* Clone this repo, or download the source as a ZIP file and unzip it somewhere[^3]

* Double-click `BindControl.py` in the top-level folder in your explorer / file manager / Finder / etc.  This should work if you have Python correctly installed.

* Alternatively: In a terminal, `cd` into the `bindcontrol` directory, then:
    + Windows: `py BindControl.py`
    + Linux: `./BindControl.py`
    + MacOS: `python3 BindControl.py`

## Credits

BindControl is in many places a direct port of [CityBinder](http://sourceforge.net/projects/citybinder/) code, and in most other places was extremely influenced by it.  Keybinding code drew from similar code in [PADRE](https://padre.perlide.org/).

Various newer functionality was added to [CityBinder for Homecoming](https://sourceforge.net/projects/citybinder-for-homecoming/) by Tailcoat, who kindly provided his source code and permission to adapt for use with BindControl, as well as offered suggestions and advice for improvements.

CityBinder's acknowledgements are reproduced below:
```
    Obviously, without Cryptic and NCSoft to have created/funded/published
    City of Heroes and City of Villains, there would be no point to this
    program.  Thanks to Gnarly and the numerous people who contributed to the
    creation of the Speed on Demand System.  Thanks to Sandolphan/Khaiba and
    the many people who posted Mastermind binds in the CoV Beta forums.
    Again thanks to Sandolphan for the Bodyguard mode binds.  Also thanks
    to the following people, who directly contributed to CityBinder, either
    with bug reports, feature suggestions, or contirbuted binds.
    PerezPersuader, Blue_Daze, Back_Blast, IronVulture, Darkelven,
    Shadowhand, Knight_Marshal, Nilt_, Psygon, DuskA, CyberKnight7, ErieFF,
    Darc_Reign, Beerninja, BarfBag, Oronis, TrystarMojo, Pyrobard,
    Ang_Rui_Shen, Konoko, Draznar, Local_Man, tyrose, Caustic, 80sboi,
    DarknessEternal, reiella, Robotech_Master, Ground_Zeroo, Stylina, and
    ShieldBearer.
```

The improved Inspiration Popper design was gratefully adapted from an unreleased version of [CityBinder for Homecoming](https://sourceforge.net/projects/citybinder-for-homecoming/) by Tailcoat.

Github Actions for automated building of binary releases provided by [JamzTheMan](https://github.com/JamzTheMan).

Additional feedback and suggestions provided in the [Homecoming Forums thread](https://forums.homecomingservers.com/topic/38674-bindcontrol-alternative-to-citybinder) and in [Github issues](https://github.com/emersonrp/bindcontrol/issues) by:<br>
DevoDog68, BlackSpectre, Premmy, kenlon, Lumenia, xizar, autobotpinto, jtoya85

Icons / graphics are from Microsoft's Fluent icons collection, by way of [Colton Griffith's Fluent Icons viewer](https://fluenticons.co/outlined/).


## License

BindControl is licensed under the [GPL version 3](LICENSE) or later.


emerson@hayseed.net

[^1]: Bodyguard Mode is based on CityBinder's original implementation, which no longer works exactly as intended in all circumstances.  It's not clear whether it ever did completely work.  It will be modified in a future release, and possibly removed, depending on what workarounds can be found.

[^2]: For instance, I run Manjaro, and have to install "libtiff5" from AUR to make the binary release work.

[^3]: If you are familiar at all with git or github, cloning the repo is the recommended action here -- this makes it easier and quicker to get new changes when they arrive, as well as allows access to incremental between-release changes and experimental branches.
