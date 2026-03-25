# BindControl

### Find the latest release of BindControl on its [releases page](https://github.com/emersonrp/bindcontrol/releases).

## About BindControl

BindControl is a helper app for creating and maintaining keybinds, macros, and popmenus for City of Heroes.

It began as a direct port of Konoko and Monorail's [CityBinder 0.76](http://sourceforge.net/projects/citybinder/), using Python and the WxWidgets UI toolkit.  It has since come into its own, adding many original features, UI improvements, and quality-of-life upgrades.

During City of Heroes' original run, CityBinder was the go-to app for keybinds.  It's written in lua, using the IUP toolkit, and the required versions of those can be difficult to set up for development on modern OSes.  I wanted to add features and clean up the UI, so in a stunningly unwise act of hubris, I instead started work on BindControl.

I worked on it on-and-off for the remainder of the original run of City of Heroes, then shelved it, ostensibly forever, when NCSoft shut down the game.  Then, of course, everything changed, the game lives again, and BindControl has a reason to exist.

BindControl is and has been developed on Homecoming, and best supports that.  Recently, beta support for Rebirth has been added, supporting the Guardian archetype, new powersets, the Genesis Incarnate slot, and more.  This support is solid but is a work in progress -- Rebirth players, check it out and file issues as you find bugs!

![BindControl_ Tinker 3_17_2026 11_47_23 PM](https://github.com/user-attachments/assets/cba3d81c-4939-4004-91ba-4a4411deb947)

## Features

* Runs on Windows, MacOS, and Linux
* Separate profiles for different characters, archetypes, or situations
* Supports Homecoming and Rebirth servers
* Controller support

* Basic Gameplay Binds
    * Chat binds with optional 'typing' notifier
    * One-key next-teammate / previous-teammate selection, with support for setting team size and optionally skipping the player in the next/previous rotation
    * Rebind the keys for the in-game power tray buttons
    * Many helpful binds directly supported - "Quit to Desktop," "Assist Target," "Show Coordinates," "Toggle Roleplaying Status," many many more

* Custom Binds
    + Simple Binds, multiple slash commands bound to a single keypress
    + Complex Binds, essentially series of Simple Binds that execute in rotation with repeated presses of a single key
    + Buffer Binds, quick one-key selection and buffing for each teammate and/or pet
    * "Bind Wizards" - simple processes guiding you through creating elaborate or complicated bind schemes that would be difficult and/or fiddly to create and maintain by hand
    + PowerBinder is a flexible tool offering an easy way to assemble and maintain possibly-complicated configurations of slash commands, and is used in Simple, Complex, and Buffer Binds

* Movement / Speed-on-Demand
    * Speed-on-Demand keybinds based on CityBinder and the original Gnarly's SoD keybinds, with many clarifications and improvements
    * Updates to Speed-on-Demand to accommodate the various [travel power changes introduced by Homecoming](https://homecoming.wiki/wiki/Issue_27_Page_2#Travel_Power_Updates)
    * Simple Power Toggle keybinds that can activate individual travel powers or toggle between related powers like Fly and Hover
    * Support for all formal travel powers:  Fly, Mystic Flight, Group Fly, Super Jump, Mighty Leap, Super Speed, Speed of Sound, Teleport, and Team Teleport
    * Secondary / server tray travel powers like Super Jump's "Double Jump" and Mystic Flight's "Translocation" integrated
    * With Homecoming profiles, <code>powexec_location cursor</code> used for Teleport binds, with "teleport immediately" and "teleport on key release" options available
    * Kheldian form toggles with power tray changing;  Kheldian movement powers incorporated into Speed-on-Demand and Power Toggle
    * Simple Temporary Travel Power toggle keybind
    * One-key reset in case SoD binds get tangled up

* Inspiration Popper
    * By-type; dual and team inspirations supported
    * Option to use or skip "super" inspirations
    * Largest-first or smallest-first
    * Optional /say feedback with per-inspiration-type custom colors

* Mastermind / Pet Binds
    * Features to help name pets uniquely, required for most of BindControl's Mastermind bind styles
        * BindControl will detect and warn if names are inadequately different / unique for by-name use
        * BindControl can create a keybind to rename your pets to match BindControl's config instead of doing it manually in-game
    * By-name pet selection - <i>requires uniquely-named pets</i>
    * Support for multiple alternate Mastermind binds styles:
        + [Classic "Sandolphan" binds](https://wiki.homecomingservers.com/wiki/Mastermind_Numpad_Pet_Controls):
            + Select pets by power level: all, minions, lieutenants, and boss
            + Select next-pet / previous-pet binds for quick buffing etc
            + Orders for aggressive / defensive / passive stances; attack, follow, go to, and stay, for all or selected pets
            + Pets can give feedback on each order;  chattiness can be toggled via keybind
            + "Bodyguard mode" shortcut -- you can define which pets should be treated as bodyguards, and turn Bodyguard Mode on for them with a single keypress - <i>requires uniquely-named pets</i>
        + [qwy's Numpad Controls](https://forums.homecomingservers.com/topic/20650-i26-expanded-mastermind-numpad-controls/):
            + Simple but comprehensive scheme using the number pad and modifier keys to select, control, heal, and buff pets
            + Mod keys select Defensive, Aggressive, Passive versions of the same commands
            + Select individual pets or by power level
            + Follow, Go To, Attack, Stay commands
            + One-key upgrade bind, applying both possible upgrades on key press and release
            + Heal targeted pet
            + Cycle target through all pets or per power level
        + [qwy's PetMouse Controls](https://forums.homecomingservers.com/topic/20788-i26-the-masterminds-petmouse-new-menu/):
            + Mouse-centric keybind scheme that uses mod keys with the mouse to give orders to pets individually or by power level
            + Alt+Click (by default) will command current pet to "go to" the click location and will target the next pet for orders, making it trivial to send each of your pets to a precise location with a minimum of interaction
            + Most key commands available from the WASD "home" position by default
            + Optional popmenu allowing more detailed commands using just a few home position keystrokes
            + Numpad commands to select all pets or by-power
            + Mouse controls can cover 90% of moment-to-moment interactions with henchmen, while the popmenu covers all other needed functionality

* Macro Composer (beta)
    * Create complex macros using PowerBinder
    * Icon picker containing (basically) all available in-game icons
    * Import and export macros for ease of moving from one Profile to another or sharing with other BindControl users

* Popmenu Editor (beta)
    * Create, install, edit, and delete popmenus in the game folder
        + Requires telling BindControl where the game is installed
        + BindControl can create the necessary folders in the game install folder for popmenus
    * Easy GUI editing and testing of popmenus
    * Generate macros to make popmenu buttons in-game

## TODO

* There are still some Homecoming-specific notions hard-coded into BindControl.  I'm working on finding and fixing these, but any bug reports and other feedback from Rebirth players would be very welcomed.
* There are a growing number of places where bits of BindControl want to trigger changes in other far-flung bits, for instance, reworking some of the UI in response to changes in the Preferences Dialog.  This is currently done haphazardly and in an ugly tightly-coupled fashion.  The time will come when I buckle down and rewrite most of these cases using [pubsub](https://pypi.org/project/Pypubsub/) which I've mostly been avoiding just to keep from adding extra dependencies.
* I hope to make every reasonable slash command available, typically via PowerBinder.  What counts as a "reasonable slash command" is yet to be determined.  Check [the SlashCommands.md file](SlashCommands.md) for the current status.
* I have ideas for a few more BindWizards.  Rolling those up from scratch is always a process, so they'll arrive whenever they do.
* Access to MacOS for testing is via a VM several OS versions old.  I don't want to buy an actual Mac just for this wee vanity project, so mileage may vary on how it acts in an actual recent Mac environment.
* Similarly, notarizing MacOS software involves having a $99/year Apple Developer Account, which is not something I find remotely interesting just for making life a few clicks easier for BindControl's MacOS users, of which I suspect there are approximately zero....
* The popmenu editor, on Windows, can't load pathologically large popmenus (tens of thousands of entries).  This is a hard limit on the wx toolkit imposed by Windows itself, and can't be worked around in any way I can see.  As there exist at least two menus this large "in the wild," further investigation is merited.
* More error detection and better / cleaner error handling.
* More and better help text and documentation.  <i>(WIP - check [the wiki](https://github.com/emersonrp/bindcontrol/wiki/Getting-Started-With-BindControl))</i>
* More internal work on initialization order of objects to speed up start time and avoid bootstrapping problems.  <i>(WIP)</i>
* Fix bugs as found.

## Using Binary Releases

Binary releases of Python applications are a bit finicky and fragile, but are provided on the [latest release page](https://github.com/emersonrp/bindcontrol/releases).  Feel free to try them, but if you have any trouble, skip down to [Running From Source](#running-from-source) below for an alternative, very deterministic, way of running BindControl.  Any feedback on your experience with the binary releases is welcome and encouraged.

*Windows users*:  Try the ZIP file.  If that works for you, it's the quickest path to victory.  ***If you receive malware warnings when downloading***, please read [my comments on that issue](Help/MalwareWarnings.md).

*MacOS users*:  Experimental binary releases for Intel and Arm64 have been made available.  They are not signed and/or notarized, and might or might not work at all.  Any feedback from MacOS users is welcome and appreciated.

*Linux users*:  Two experimental binary releases are now available:
* ZIP file:  you should be able to unzip the ZIP file anywhere, and run the "BindControl" binary from within it.  It's built using Github's "ubuntu-24.04" environment, which may or may not be completely compatible with other distributions and versions.[^1]  If this works for you, it's probably the simplest solution
* AppImage:  a full-on AppImage is also available.  You should be able to download it, `chmod +x` the downloaded file, and run it directly.  It's a big download, as AppImages tend to be, but github supports using tools like [AppImageUpdate](https://github.com/AppImageCommunity/AppImageUpdate) and [appimage-updater](https://royw.github.io/appimage-updater/), so it's possible to update BindControl incrementally instead of downloading nearly 200MB of AppImage over and over.  Check the various tools' sites for more information.

## Running From Source

### Step 1 - Dependencies

1. [Python](https://www.python.org) version 3.13 or later
2. [wxPython](https://www.wxpython.org) version 4.2.2 or later
3. [Pillow](https://pypi.org/project/pillow/)

*Windows users*:
* follow the instructions on the above sites' download pages to install Python and wxPython.
* From a command line, `pip3 install pillow`

*MacOS users*:
* *Pre-Catalina*:  I recommend following the instructions in [this article at opensource.com](https://www.opensource.com/article/19/5/python-3-default-mac) to get Python 3 installed and working as the default Python.  Once Python 3 is working, you will want to run `pip3 install wxPython`.
* *Catalina and later*: follow the instructions on the above sites' download pages to install Python and wxPython.
* *All versions*: from a command line, `pip3 install pillow`

*Linux users*:  install your distribution's packages for Python 3 and wxPython, and "python-pillow" or whatever your distribution calls it.


### Step 2 - Getting and running the code

* Clone this repo, or download the source as a ZIP file and unzip it somewhere[^2].

* Double-click `BindControl.py` in the top-level folder in your explorer / file manager / Finder / etc.  This should work if you have Python correctly installed.

* Alternatively: In a terminal, `cd` into the `bindcontrol` directory, then:
    + Windows: `py BindControl.py`
    + Linux: `./BindControl.py`
    + MacOS: `python3 BindControl.py`

## Developing BindControl

BindControl is being developed on Manjaro Linux.  It gets feature-tested on Windows 10 and 11 VMs, and occasionally on a MacOS Catalina VM.

While developing, I make sure the code passes both `pyright` and `ruff` with a large subset of the possible ruff rules included.

There is a small but growing `pytest` test suite.  It only runs on Linux (and possibly MacOS) because it uses `pytest-forked` which is not supported on Windows.  To run the test suite, you'll need to install the following plugins and their dependencies:
* `pytest-forked`
* `pytest-xdist`
* `pytest-ruff`
* `pytest-cov`

I make liberal use of `typing` in parameters, attributes, and return values, and continue to add this into new and existing code as I go.  This has proven to be a bit of a hassle since BindControl was originally a direct port of CityBinder, and inherited many of its original questionable design decisions, as well as having introduced any number of its own over the years.  Enforcing more strict typing is an ongoing process, but has resulted in cleaner and better code, as well as having surfaced any number of potential and actual bugs.

Any submitted patches or pull requests should pass the test suite and `pyright` at the very least.  Adding new tests is encouraged.

## Credits

BindControl was originally a direct port of [CityBinder](http://sourceforge.net/projects/citybinder/) code, and in many places is still extremely influenced by it.  Keybinding code drew from similar code in [PADRE](https://padre.perlide.org/).

Various newer functionality was added to [CityBinder for Homecoming](https://sourceforge.net/projects/citybinder-for-homecoming/) by Tailcoat, who kindly provided his source code and permission to adapt for use with BindControl, as well as offered suggestions and advice for improvements.  The Inspiration Popper in particular was incorporated wholesale from a design of Tailcoat's in an unreleased version of CityBinder for Homecoming.

The [CoH/CoV Technical Reference Guide](https://web.archive.org/web/20251212024327/http://shenanigunner.com/CoX-Technical-Guide-v4-16.pdf) from [Shenanigunner](https://web.archive.org/web/20250318031408/http://shenanigunner.com/)[^5] has been, and continues to be, a crucial resource and is highly recommended for those wishing to dig deeper into keybinds, popmenus, and macros.

The Sandolphan Mastermind bind schemes were originally developed by Sandolphan during the City of Villains beta in 2006 and [posted to the official forums](http://web.archive.org/web/20120904222729/http://boards.cityofheroes.com/showthread.php?t=117256) at that time.  The version in BindControl is an adaptation and expansion of the original binds.

The qwy Mastermind bind schemes are adapted from qwy's posts on the Homecoming forums[^3] [^4], and are used with their gracious permission.

The Github Actions for automated building of binary releases were provided by [JamzTheMan](https://github.com/JamzTheMan).

Additional feedback and suggestions have been provided in the [Homecoming Forums thread](https://forums.homecomingservers.com/topic/38674-bindcontrol-alternative-to-citybinder) and in [Github issues](https://github.com/emersonrp/bindcontrol/issues) by:<br>
DevoDog68, BlackSpectre, Premmy, kenlon, Lumenia, xizar, autobotpinto, jtoya85

Most of the UI Icons / graphics are from Microsoft's [Fluent icons](https://github.com/microsoft/fluentui-system-icons) collection, by way of [Colton Griffith's Fluent Icons viewer](https://fluenticons.co/outlined/).

CityBinder's original acknowledgements are reproduced below:
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


## License

BindControl is licensed under the [GPL version 3](LICENSE) or later.


emerson@hayseed.net

[^1]: For instance, I run Manjaro, and have to install "libtiff5" from AUR to make the binary release work.

[^2]: If you are familiar at all with git or github, cloning the repo is the recommended action here -- this makes it easier and quicker to get new changes when they arrive, as well as allows access to incremental between-release changes and experimental branches.

[^3]: [i26 Expanded Mastermind NumPad Controls+](https://forums.homecomingservers.com/topic/20650-i26-expanded-mastermind-numpad-controls/)

[^4]: [i26 The Mastermind's PetMouse](https://forums.homecomingservers.com/topic/20788-i26-the-masterminds-petmouse-new-menu/)

[^5]: [Shenanigunner passed away in April 2025](https://forums.homecomingservers.com/topic/59721-shenanigunner-ave-atque-vale/) and his site has gone dark since then.  The links in the Credits section point to the latest available captures of his site at the Internet Archive.  Shenanigunner was an iconic and tireless member of the City of Heroes community, and his presence is deeply missed.
