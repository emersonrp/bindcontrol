# BindControl

<b>NEW!</b>  Check out the new work-in-progress [Getting Started with BindControl](https://github.com/emersonrp/bindcontrol/wiki/Getting-Started-With-BindControl) on the wiki!

<hr>

BindControl is a helper app for creating and maintaining keybinds and popmenus for City of Heroes.

It is an enhanced port of Konoko and Monorail's [CityBinder 0.76](http://sourceforge.net/projects/citybinder/), using Python and the WxWidgets UI toolkit.

During City of Heroes' original run, CityBinder was the go-to app for keybinds.  It's written in lua, using the IUP toolkit, and the required versions of those can be difficult to set up for development on modern OSes.  I wanted to add features and clean up the UI, so in a stunningly unwise act of hubris, I instead started work on BindControl.

I worked on it on-and-off for the remainder of the original run of the game, then shelved it, ostensibly forever.  Now here in the age of the SCORE, Homecoming, and other servers, it once again has value, so I've dusted it off and continued to add features and modernize it.

With Homecoming recently [securing the licensing](https://forums.homecomingservers.com/topic/47223-ncsoft-homecoming-license-announcement/) for City of Heroes from NCSoft, development of the game and its ecosystem, BindControl included, is likely to remain very Homecoming-centric in the near to medium term.  Recent updates to BindControl's Speed on Demand code incorporate [changes made in Homecoming Issue 27, Page 2](https://homecoming.wiki/wiki/Issue_27_Page_2#Travel_Power_Updates), and while BindControl will continue to work on non-Homecoming servers to a greater or lesser degree, I don't currently have a presence on these other servers to test and validate.  Please feel free to open issues for non-Homecoming servers, but know that they might not receive as much attention as Homecoming-specific ones do.

![BindControl](https://github.com/user-attachments/assets/3761cd12-0620-4c61-a436-4e5d32770e79)

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

* Attempt to make every reasonable slash command in the game available in some way, typically via PowerBinder.  What qualifies as a "reasonable slash command" is yet to be determined.
* Access to MacOS for testing is via a MacOS VM several OS versions old.  I don't want to buy an actual Mac just for this wee vanity project, so mileage may vary on how it acts in an actual recent Mac environment.
* The Movement Powers page is a confusing forest of checkboxes, dating from the original CityBinder layout and needs some layout and documentation work.
* "Bodyguard mode" as implemented in CityBinder doesn't work as intended, and might not be able to due to game restrictions.
* Investigate improvements to Mastermind binds to clarify and expand the behavior.
* The popmenu editor, on Windows, simply can't load pathologically large popmenus (tens of thousands of entries).  This is a hard limit on the wx toolkit imposed by Windows itself, and can't be worked around in any way I can see.  As there exist at least two menus this large "in the wild," further investigation is merited.
* More error detection and handling.
* Temporary powers in speed-on-demand.
* More and better help text and documentation.
* Fix bugs as found.
* More internal work on initialization order of objects to speed up start time and avoid bootstrapping problems.

## Using Binary Releases

Binary releases of Python applications are a bit finicky and fragile, but are provided on the [latest release page](https://github.com/emersonrp/bindcontrol/releases).  Feel free to try them, but if you have any trouble, skip down to [Running From Source](#running-from-source) below for an alternative, very deterministic, way of running BindControl.

*Windows users*:  try the ZIP file and give feedback.  If that works for you, it's the quickest path to victory.  <b>If you receive malware warnings when downloading</b>, please read [my comments on that issue](Help/MalwareWarnings.md).

*MacOS users*:  an experimental binary release has been made available.  It is not signed and/or notarized, and might or might not work at all.  Any feedback is encouraged.

*Linux users*:  an experimental binary release is now available.  You should be able to unzip the zipfile anywhere, and run the "BindControl" binary from within it.  It's built using Github's "ubuntu-latest" environment, which may or may not be completely compatible with other distributions and versions.[^2]

## Running From Source

### Step 1 - Dependencies

1. [Python](https://www.python.org) version 3.12 or later
2. [wxPython](https://www.wxpython.org) version 4.2 or later

*Windows users*:  follow the instructions on the above sites' download pages to install Python and wxPython.

*MacOS users*:  I recommend following the instructions in [this article at opensource.com](https://www.opensource.com/article/19/5/python-3-default-mac) to get Python 3 installed and working by default.  Once everything is working, you will want to run `pip3 install wxPython`.

*Linux users*:  install your distribution's packages for Python 3 and wxPython.

### Step 2 - Getting and running the code

* Clone this repo, or download the source as a ZIP file and unzip it somewhere[^3]

* Windows (and possibly Mac) users:  Double-click `BindControl.py` in the top-level folder

* Mac / Linux users: In a terminal, `cd` to where you put the BindControl source, then `python BindControl.py`.  Some distributions might need `python3` instead of `python`.

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
