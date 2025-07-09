# Slash Command List

This is the list of slash commands still to be implemented or deemed not worth implementing.

Anything not found on this list has been implemented, or is a longer alias to a shorter form listed here.  Some things on this list are implemented in places but not necessarily fully integrated.

## Still need "implement or don't" triage

| Bind | Description |
|------|-------------|
| /alt2tray [0-1] | Show and lock the tertiary (Alt2) tray slot into the raised position or unlock and hide it. |
| /altinvite name | Adds other characters in your account to your supergroup. |
| /alttray [0-1] | Show and lock the secondary (Alt) tray slot into the raised position or unlock and hide it. |
| /alttraysticky | Cycles through showing the secondary (Alt) and tertiary (Alt2) tray slots, and then hiding them. |
| /assist | Change your current target to selected ally's or enemy's target |
| /auc_loginupdate | Get status of auction inventory info to the player. Displays how many items were bought and sold in the Consignment House chat channel. |
| /boost_convert | Converts the specified enhancement into a different enhancement. |
| /build_save | Saves the current character build (Name, Level, Archetype, Origin, Powers and Slotted Enhancements) to build.txt |
| /build_save_file filename | Saves the current character build (Name, Level, Archetype, Origin, Powers and Slotted Enhancements) to a specified file |
| /chan_create channel | Create a new chat channel |
| /chan_desc channel description | Set the channel's description |
| /chan_invite channel username | Invite a player or chat handle to a chat channel. Alias: /ginvite |
| /chan_invite_gf channel | Invites your entire global friends list to a global chat channel |
| /chan_invite_sg channel rank | Invite your entire Supergroup to a global chat channel. Only leaders may use this command. The rank parameter may be any of the ranks listed below. Alias: /ginvite_sg |
| /chan_invite_team channel | Invites your entire team or Task Force to a Global chat channel |
| /chan_join channel | Join an existing chat channel |
| /chan_leave channel | Leave a chat channel |
| /chan_members channel | List all members of channel |
| /chan_mode channel options | Changes default access rights for new user who joins the channel. If you set -join, no one can join unless invited by an operator. |
| /chan_motd channel message | Set the channel's Message Of The Day, which is sent to everyone that joins or logs into the channel |
| /chan_send channel message | Send message to chat channel. You must be in the channel and have Send priviledges. Alias: /send |
| /chan_timeout <channel name> <days> | Sets the number of days a member of a global channel must go without logging in before being automatically kicked from the channel. |
| /chan_user_mode channel global options | Sets user permissions for the user with the handle global (without the @) on channel. You must have operator status to set permissions. |
| /chat_cycle | Cycles through the default chat channels |
| /chat_load | Reads a list of chat settings from chat.txt |
| /chat_load_file filename | Reads a list of chat settings from a file |
| /chatoptions [0-4] | Activates context menu for the chat windows. |
| /chat_save | Saves a list of chat settings to chat.txt |
| /chat_save_file filename | Saves a list of current chat settings to a file |
| /chat_set channel_name | Changes the default channel in the chat window. |
| /ci player | Alias for /coalition_invite |
| /citytime | Displays the current in-game time in the System chat channel. |
| /clearAttributeView | Clear a target's combat attributes from the Combat Attributes window. |
| /clearchat | Clear all chat buffers |
| /clear_petnames | Clear the names of all your named pets |
| /clearRewardChoice | Choose "no reward" in the current reward choice list. |
| /coalition_cancel supergroup | Cancel coalition with a supergroup. |
| /coalition_invite player | Invite player's supergroup to join coalition. Alias: /ci |
| /coalition_mintalkrank supergroup_ID [0-1] | Sets the Hear Leaders Only setting that prevents your supergroup members from hearing anyone other than the leader from the coalition supergroup. |
| /coalition_nosend supergroup_ID [0-1] | Stop your supergroup from sending coalition chat to an ally supergroup. |
| /coalition_sg_mintalkrank [0-1] | Sets the Leader Chat Only setting that restricts coalition chat to your supergroup's leader only. |
| /comment | Set or erase search comment. |
| /conprint string | Echo <string> to the console (System chat channel) |
| /contactfinder_selectcurrent | Selects the contact currently detailed in the Contact Finder window. |
| /contactfinder_showcurrent | Shows the current contact in the Contact Finder window. |
| /contactfinder_shownext | Shows the next contact in the Contact Finder window. |
| /contactfinder_showprevious | Shows the previous contact in the Contact Finder window. |
| /contactfinder_teleporttocurrent | Teleports you to the contact currently detailed in the Contact Finder window. |
| /contextmenu menu_num | Activate a context menu slot. |
| /controller_modifiers <first> <second> | Allows setting two controller buttons as modifiers on a gamepad |
| /controller_vmouse <LMB> <RMB> [MMB] [Snap] | Configures virtual mouse mode buttons on a gamepad |
| /cooldown_indicator [0-3] | Sets cooldown timer onto tray icons: Recharge indicator setting (0=off, 1=bottom, 2=top, 3=center) Alias: /recharge_indicator |
| /copychat tab | Copy the entire chat history from specified chat Tab into the clipboard |
| /ctm [0-1] | Alias for /clicktomove |
| /ctm_invert [0-1] | Alias for /clicktomove. |
| /ctmtoggle | Toggles click-to-move mode on or off. |
| /cursorcache | Enable cursor cache for smoother cursor changes |
| /custom_window name | Creates a custom window |
| /custom_window_toggle name | Opens or closes a custom window |
| /debug_disableautodismiss [0-1] | Enables you to turn on and off auto-dismissal of contacts. |
| /demodump | Alias for /demostop |
| /demodumptga [0-1] | dump frames to tga files |
| /demofps number | set demo playback frames per second |
| /demoframestats [0-1] | whether or not to log performance info for every frame of the demo |
| /demohideallentityui [0-1] | hides all ui in demo playback. |
| /demohidechat [0-1] | hides chat in demo playback. |
| /demohidedamage [0-1] | hides damage in demo playback. |
| /demohidenames [0-1] | hides names in demo playback. |
| /demoloop number | Number of times to loop demo before exiting |
| /demopause number | point to stop and loop same frame (in msec) |
| /demorecord filename | Record a demo to the given name |
| /demorecord_auto | Begin recording a demo with a game-generated filename |
| /demospeedscale number | speed multiple to play back demo at |
| /demostop | Stop demo record/play. Alias: /demodump |
| /demote character | Demote supergroup member one rank |
| /dialog_answer choice | Answer dialog with button matching the provided text choice (ok, yes, no, cancel, accept, decline, join, etc.) |
| /dialog_no | Answer OK, No, or Cancel to current dialog |
| /dialog_yes | Answer OK, Yes, or Accept to current dialog |
| /disable2d | Disables 2D sprite drawing |
| /debug_disableautodismiss [0-1] | Enables you to turn on and off auto-dismissal of contacts. |
| /emailheaders | Displays the number of local email messages in your inbox. |
| /enablevbos | turns on vertex buffer object extension |
| /enterbasefrompasscode passcode | Enter the Supergroup Base associated with the provided passcode. |
| /enter_base_from_sgid SGID number | When the Base Entry Selection window is open, enters the Supergroup Base associated with the provided supergroup ID number. |
| /enterdoor coordinates map_ID | Request a click on a door. |
| /exitlaunch FilePath | Set program to run when game exits |
| /face | Turn player to face target |
| /fl | Display friend list. Alias: /fl |
| /follow | Toggle follow mode (/cmdlist says that follow takes an argument (0 or 1), it does not) |
| /friend character | Add character to friend list |
| /fullRelight | Do not cap number of world object vertices to relight per frame |
| /fullscreen [0-1] | Sets video mode to fullscreen |
| /gamereturn | Close all dialogs and non-essential windows. |
| /getallarenastats | Get all your arena combat statistics, more comprehensive display. |
| /getarenastats | Get your arena stats. |
| /getglobalname localname | Given the name of a character, this command will tell you the player's global name |
| /get_local_invite globalname | Invite a player to your team using their global name |
| /get_local_league_invite globalname | Invite a player to your league using their global name |
| /getlocalname globalname | Given a global name, this command will tell you the name of a player's currently logged on character |
| /getpos | Alias for /loc |
| /gfriend name | Add a player to your global friends list. |
| /gfriends | Display all members of your global friends list |
| /gignore username | Alias for /ignore. |
| /gignoring | Alias for /ignorelist |
| /ginvite channel_name username | Alias for /chan_invite |
| /ginvite_sg channel_name rank | Alias for /chan_invite_sg |
| /gmotd | View the game's global message again. |
| /goto_tray number | Go to specified power tray number in the primary tray slot |
| /goto_tray_alt number | Go to specified power tray number in the secondary (Alt) tray slot |
| /goto_tray_alt2 number | Go to specified power tray number in the tertiary (Alt2) tray slot |
| /goto_trays_tray row tray | Go to specified tray slot (1-3) and power tray (1 to 9). |
| /graphfps number | Graph current framerate (1 = SWAP, 2 = GPU, 4 = CPU, 8 = SLI). |
| /gunfriend name | Remove player from global friends list. Alias: /gunfriend_player |
| /gunignore username | Removes a player from your global ignore list. |
| /hardconsts | Use hard shader constants instead of Cg to setup shader params |
| /hide | Opens the hide options dialog window. |
| /hide_all | Hides you completely from all other players, similar to the old /hide functionality |
| /hide_friends | Hide from server friends |
| /hide_gchannels | Hide from global chat channels |
| /hide_gfriends | Hide from global friends |
| /hide_invite | Block all invite requests |
| /hideprimarychat | Hide/unhide primary chat message windows. |
| /hide_search | Hide from searches |
| /hideset number | Hide from any combination of groups. |
| /hide_sg | Hide from SuperGroup |
| /hide_tell | Hide from tells (private messages) |
| /i character | Alias for /invite |
| /ignore character | Ignore character |
| /ignorelist | Displays a list of ignored characters |
| /ignore_spammer character | Ignore character and sends alert to customer service |
| /imageServer | Sets game to Image Server mode. |
| /incarnate_unequip slotName powername | Unequips the specified Incarnate Ability. |
| /incarnate_unequip_all | Unequips all equipped Incarnate Abilities. |
| /incarnate_unequip_by_slot slotName | Unequips whatever ability is in the specified Incarnate slot. |
| /info | Opens the info window for the current target (yourself if you have no target). |
| /info_self | Opens the info window for yourself |
| /info_self_tab tab_number | Opens the specified tab of the info window for yourself |
| /info_tab tab_number | Opens the specified tab of the info window for the current target (yourself if you have no target) |
| /insp_combine inspName inspName | Combine 3 inspirations into one of a different type. Alias: /MergeInsp |
| /insp_delete inspiration | Deletes an inspiration by name. |
| /inspexec_pet_name insp_name petname | Gives an inspiration to the named pet |
| /inspexec_pet_target insp_name | Gives an inspiration to the targeted pet |
| /interact | Interact with an object or entity in front of the player using a keyboard key (equivalent to left-click on object). |
| /invite character | Invite character to join team. Alias: /i |
| /k character | Alias for /kick |
| /keybind_reset | Alias for /unbind_all |
| /kick character | Remove character from team. Alias: /k |
| /kiosk number number | Pop up the kiosk info for the nearest kiosk. (Assuming you're close enough.) |
| /lc message | Alias for /league |
| /league message | Sends the specified message on the League chat channel. Aliases: /lc, /league_chat |
| /league_chat message | Alias for /league |
| /league_invite name | Invite a character to your league. Alias: /li |
| /league_kick name | Kick player name from league. Alias: /lk |
| /league_make_leader name | Change the league leader (must be league leader). Alias: /lml |
| /leagueToggleTeamLock | Lock your team so members can not be added, moved, or swapped (must be team leader). |
| /leagueWithdrawTeam | Withdraw you or your team from the current league without leaving the team |
| /leaveLeague | Leave your current team and league. |
| /leaveteam | Leave your current team |
| /lfg_event_response yes/no | Accept an invitation to join an event (trial, task force, story arc, or holiday event). |
| /lfg_remove_from_queue | Remove self or team from LFG queue. |
| /lfg_request_event_list | Get LFG system event list. |
| /lfgset number | Sets your "looking for group" status. |
| /lfgtoggle | Toggle looking for group status. |
| /li name | Alias for /league_invite |
| /link_channel ChannelName | Activates Context Menu for a channel name. |
| /link_info LinkName | Provides info window on matching power, inspiration, enhancement, recipe, or salvage item. |
| /link_interact name | Activates context menu for a character name. |
| /link_interact_global name string | Activates context menu for a player's global name. |
| /listen_range number | Set the maximum range of local chat and emotes that you want to listen to. |
| /lk name | Alias for /league_kick |
| /lml name | Alias for /league_make_leader |
| /loc | Get coordinates of current location on the map. Alias: /getpos |
| /localtime | Displays your local time (the time on your computer) in the System chat channel. |
| /logchat | Toggle chat logging |
| /loudstacking [0-1] | Enable old eardrum-busting sound stacking. |
| /ma message | Alias for /mission_architect |
| /macro name command | Add a macro to first empty slot |
| /macro_image icon tooltip command | Add a macro with an existing icon to the first empty slot |
| /macroslot macro-slot# name command | Add a macro to specified power tray slot |
| /mailview string | Sets which view to use (Inbox or Character Items) when on the Email window |
| /makeleader character | Change the team leader to targeted character, must have character targeted if no name is provided. Alias: /ml |
| /maxAniso | Shows the maximum anisotropic your card allows |
| /maxColorTrackerVerts number | Maximum number of world object vertices to relight per frame |
| /maxfps | Sets the maximum limit for frames per second that a player's client can utilize, whether the game is in focus or not. |
| /maximize | Maximizes the window |
| /maxInactiveFps | Limits max frames per second while the game is not in the foreground. |
| /maxrtframes number | How many frames ahead to allow buffering. |
| /maxtexunits | Limits number of textures used, set to 4 to emulate GF 4/5 path |
| /me | Alias for /emote |
| /menu | Opens the main menu. |
| /mergeInsp inspName inspName | Alias for /insp_combine. |
| /mission_architect message | Send message to the Architect Chat channel. Alias: /ma |
| /missionmake | Opens the Mission Architect to the My Creations tab while inside Architect Entertainment. Alias: /mmentry |
| /missionsearch | Alias for /architect |
| /ml character | Alias for /makeleader |
| /mmentry | Alias for /missionmake. |
| /mmscrollsettoggleregion [0-3] | Displays the specified editing screen while creating or editing a mission in the Mission Architect. Alias: /mmscrollsetviewlist |
| /mmscrollsetviewlist | Alias for /mmscrollsettoggleregion. |
| /mouse_invert | While using mouselook, makes the camera pitch down when the mouse moves down. |
| /mouse_speed | Scale factor for mouse look |
| /myhandle | Display your chat handle (global name) |
| /mypurchases | Show the list of purchases you have access to |
| /namecaptain name | Renames the 'Captain' supergroup rank |
| /namecommander name | Renames the 'Commander' supergroup rank |
| /nameenforcer name | Renames the 'Enforcer' supergroup rank |
| /nameflunky name | Renames the 'Flunky' supergroup rank |
| /nameleader name | Renames the 'Leader' supergroup rank |
| /namelieutenant name | Renames the 'Lieutenant' supergroup rank |
| /namemember name | Renames the 'Member' supergroup rank |
| /nameoverlord name | Renames the 'Overlord' supergroup rank |
| /nameringleader name | Renames the 'Ringleader' supergroup rank |
| /name_scale [0.5-9+] | Change size of name info over players, NPCs and objects. |
| /nametaskmaster name | Renames the 'Taskmaster' supergroup rank |
| /neterrorcorrection [0-2] | Adjusts network error correction limits. |
| /netgraph [0-2] | Displays network connection information. 0 = disable, 1 = enable, 2 = see a large version. |
| /next_trays_tray 1-3 | Go to next power tray located in the specified tray slot. |
| /noBump | disable bump maps by forcing unperturbed normal |
| /nojpg | Disables saving of .JPG files in image server mode ? |
| /nojumprepeat | Disable jump auto-repeat |
| /nop | Used to bind a keyboard key or button to do nothing. |
| /noparticles [0-1] | Turn off particle graphics. |
| /nosunflare | Disables sun flare for performance debugging |
| /notga [0-1] | Disables saving of .TGA files in image server mode |
| /option_list | Lists names allowed for /option_set and /option_toggle |
| /option_load | Reads a list of option settings from options.txt |
| /option_load_file filename | Reads a list of option settings from a file |
| /option_save | Saves a list of current option settings to options.txt |
| /option_save_file filename | Saves a list of current option settings to a file |
| /option_toggle optionname | Toggles an option setting on or off. |
| /petition message | Sends in-game user petition to customer support |
| /petoptions | Displays pet option context menu |
| /petrename name | Rename your current pet |
| /petrename_name name | Rename the named pet |
| /pet_select_name pet_name | Selects the named pet |
| /playernote globalname | Opens note window for a specified global name |
| /playernotelocal name | Opens note window for both character names and global names |
| /playerturn | Turn player to match camera |
| /popmenu name | Opens a custom pop-up menu at the cursor's location |
| /powers_togglealloff | Toggles off all currently active toggle powers |
| /powexec_abort | Cancels the auto-attack power and the queued power |
| /powexec_location power | One click automatic targeting of a ranged location area of effect |
| /powexec_server_slot slot | Executes the specified power slot in the server-controlled tray. |
| /powexec_slot slot | Executes the given power slot in the primary tray slot |
| /prevshaders | Use previous Cg shader set found in 'cgfx/prev' subfolder for comparison/debugging |
| /prev_trays_tray 1-3 | Go to previous power tray in the specified tray slot. |
| /profiler_record file | Record client profiler information to specified file. |
| /profiler_stop | Stop recording profiler information. |
| /profiling_memory | Set the number of MB of memory to use for profiling |
| /promote character | Promote supergroup member one rank |
| /quittocharacterselect | Quits to character select. |
| /quittologin | Quits to login screen. |
| /recharge_indicator [0-3] | Sets the position of the recharge timer on tray icons. Alias: /cooldown_indicator |
| /recharge_timer_color | Sets the Recharge Timer Color. |
| /recharge_timer_format | Sets the Recharge Timer Format. |
| /recharge_timer_opacity | Sets the Recharge Timer Opacity. |
| /recharge_timer_threshold | Enables the Power Recharge Timer and sets the threshold for when the timer will appear. |
| /reduce_mip | Reduces the resolution of textures to only use the reduced (mip-map) textures. Must pass as command line arg -reduce_mip or you need to subsequently run unloadgfx |
| /release | Activate medicom unit for emergency medical transport when defeated |
| /release_pets | Release your current pets |
| /renderscalex | Changes the horizontal scale at which the 3D world is rendered relative to your screen size |
| /renderscaley | Changes the vertical scale at which the 3D world is rendered relative to your screen size |
| /rendersize | Changes the size at which the 3D world is rendered |
| /requestexitmission number | Leave the mission once it is completed. It requires a number argument, but the number doesn't seem to do anything. |
| /respec | Go to the power respecification screen if you have a free respec |
| /respec_status | Find out how many respecs are available. |
| /roll parameter | Displays a random number within the specified range in the Emotes chat channel. |
| /salvage_open item | Opens the specified Super Pack salvage item. |
| /screen resolution | Sets X and Y screen dimensions. |
| /sea options | Find a character. |
| /select_build [1-3] | Select a Build from anywhere. |
| /send channel message | Alias for /chan_send |
| /servertime | Displays the current server's time in the System chat channel. |
| /set_difficulty_av | Sets whether or not you encounter archvillains while solo. See Notoriety |
| /set_difficulty_boss | Sets whether or not you encounter bosses while solo. See Notoriety |
| /set_difficulty_level level | Sets the level part of your Notoriety |
| /set_difficulty_team_size size | Sets the team size part of your Notoriety |
| /sethelperstatus [1-4] | Sets your helper status. 1 = help me, 2 = mentor, 3 = off, 4=roleplaying |
| /set_powerinfo_class | Brings up context menu for choosing archetype for power info display. |
| /set_title number | Set badge title by number, if you do not have the specified badge your current badge title will be cleared. |
| /sg_enter_passcode | When the Base Entry Selection window is open, opens a secondary window to enter a Supergroup Base Access Passcode. |
| /sgi character | Alias for /sginvite |
| /sginvite character | Invite character to join supergroup. Alias: /sgi |
| /sgk character | Alias for /sgkick |
| /sgkick character | Kick character from supergroup. Alias: /sgk |
| /sgkickyes name | Kick player from supergroup, without confirmation. |
| /sgleave | Leave the current supergroup. |
| /sgpasscode text | Creates a Base Access Passcode, used to enter a supergroup's base |
| /sgsetdemotetimeout seconds | Sets the number of days a leader in your supergroup has to go without logging in before the leader is demoted. |
| /sgsetdescription description | Sets your supergroup description. |
| /sgsetmotd message | Sets the supergroup's message of the day. |
| /sgsetmotto motto | Sets the supergroup's motto. |
| /sgwho | Lists basic information about your supergroup and generates a list of all member characters sorted by supergroup rank. The list is displayed in the System chat channel. |
| /shaderCache | Enable the shader cache |
| /sheathe | Immediately puts away all weapons. |
| /show_bind key | Shows bind attached to specified key |
| /show_bind_all | Prints a list of all apparent key bindings on a character |
| /show_bind_all_file filename | Prints a list of all apparent key bindings on a character |
| /showfps [0-3] | Show current framerate |
| /shownewtray | Opens an additional floating tray slot/power tray. |
| /show_petnames | Displays the names of all your named pets |
| /showtime [0-1] | Displays the in-game time of day on the screen. |
| /slashchat | Starts chat-entry mode with a forward slash. |
| /speak_range number | Set the maximum range that your local chat and emotes may carry. |
| /speed_turn number | Changes the speed that your character turns while using keyboard keys. |
| /startchat | Starts chat-entry mode |
| /stopinactivedisplay | Stops rendering when the game is not the foreground application. |
| /stopmonitorattribute string | Removes a display line from the combat Attribute Monitor. |
| /stuck | Try to get unstuck if you are stuck in the geometry. |
| /supporthardwarelights | Enable support for AlienFX/LightFX case lights. |
| /suppressCloseFx | Hide all personal FX when the camera is closer than the suppressCloseFxDist |
| /suppressCloseFxDist number | Within this camera distance, personal FX will be suppressed. |
| /sync | Try to resync with the game server. |
| /synch | Alias for /sync |
| /tabclose name | Close/delete chat tab |
| /tabcreate window pane name | Create new chat tab. Specify window (0-4), pane(0 top, 1 bottom) and tab name. |
| /tabglobalnext | Cycle forward through all chat tabs in all windows, will open the corresponding chat window if necessary |
| /tabglobalprev | Cycle backward through all chat tabs in all windows, will open the corresponding chat window if necessary |
| /tabnext 0-4 | Cycle forward through all chat tabs in specified chat window |
| /tabprev 0-4 | Cycle backward through all chat tabs in specified chat window |
| /tabselect tab_name | Select the given chat tab, will open the corresponding chat window if necessary |
| /tabtoggle | Toggle between the current chat tab and the previously active chat tab |
| /tailor_status | Find out how many free tailor sessions are available. |
| /target_distance [0-1] | Sets displaying the distance between you and your target in the Target window. |
| /target_name name | Targets next entity that matches the given name. |
| /teamMoveToLeague LeaderName | Create a new league with the whole team. Alias: /tmtl |
| /team_quit_internal | Quits a team without offering a confirmation dialog, even if in task force, flashback, or Architect modes. |
| /texaniso | Sets the amount of anisotropic filtering to use, reloads textures |
| /texLodBias | Reduces the texture LOD bias for better compatibility with anisotropic filtering (values from 0 - 2 are valid) |
| /title_change | Opens the Title selection menu. |
| /tll character_name, message | Send a message to a character's league leader. |
| /tmtl LeaderName | Alias for /teamMoveToLeague |
| /toggle_enemy | Cycles through targetable enemies starting with the closest |
| /toggle_enemy_prev | Cycles through targetable enemies in reverse order |
| /trade character | Invite character to trade, must have character targeted if no name is provided |
| /trade_accept | Recieves a trade accept (unfinished or internal command) |
| /tray_always_shrink | Shrink power icons when recharging. |
| /tray_animations | Power Tray Animations. |
| /tray_labels | Power Tray Labels. |
| /traysticky [1-2] [0-1] | Show or hide the secondary (Alt) or tertiary (Alt2) tray slot. |
| /traystickyalt2 | Toggles the tertiary (Alt2) tray slot (show/hide). |
| /ttl character_name, message | Send a message to a character's team leader. |
| /tut_votekick name | Start a vote kick request |
| /tut_votekick_opinion [yes, no] | Give your opinion on the vote kick. |
| /uiscale number | Enlarges or decreases the entire User Interface |
| /unbind keyname | Unbinds a bound key (resets it to default). |
| /unbind_all | Resets keybinds, returning all keys to their default bindings. |
| /unfriend character | Remove character from friends list. Alias: /estrange |
| /unhide_all | Stop hiding from all other players and allow them to see whether you are online |
| /unhide_friends | Stop hiding from server friends |
| /unhide_gchannels | Stop hiding from global chat channels |
| /unhide_gfriends | Stop hiding from global friends |
| /unhide_invite | Stop blocking invite requests |
| /unhide_search | Stop hiding from searches |
| /unhide_sg | Stop hiding from SuperGroup |
| /unhide_tell | Stop hiding from tells (private messages) |
| /unignore character | Unignore character |
| /unlevelingpact | Bring up the dialog for quitting a leveling pact. |
| /unloadgfx | unloads all textures (causing them to be reloaded dynamically). Alias: /reloadgfx |
| /usecelshader number | Enables or disables the cel shader graphics setting |
| /useCubemap number | Use cubemap |
| /usedof | Use Depth of Field effects if available |
| /usefp | Use a floating point render target for HDR lighting effects if available |
| /usehdr | Use HDR lighting effects (Bloom/tonemapping) if available |
| /useHQ number | Allow use of High Quality shader variants |
| /userenderscale | Enables/disables render scaling feature |
| /usewater | Use fancy water effects if available |
| /watching | List all members of all chat channels that you belong to |
| /wdw_load | Loads the default windows settings file wdw.txt onto your character. |
| /wdw_save | Saves a list of current window settings to wdw.txt |
| /whereami | Tells the names of your current Server, Zone, and map coordinates. |
| /who name | Searches for character name. |
| /whoall | List who's on the current map, in the System chat channel. |
| /window_names | Lists the names of most windows exposed to players. |
| /window_resetall | Resets all window locations, sizes, and visibility to their defaults. |
| /window_scale | Change a single window scale. |
| /zoomin +, ++, or [0-1] | Zoom camera in and lock. |
| /zoomout +, ++, or [0-1] | Zoom camera out and lock. |


## Not Likely to Implement

| Bind | Description |
|------|-------------|
| /ai player | Alias for /arena_invite |
| /angle_snap [0-359] | Sets the angle for snap drag rotation in degrees while editing a supergroup base. Default snap = 5, disable snap = 0 |
| /angle_snap_cycle | Cycles through 8 standard angles for snap drag rotation (Off - 45 degrees). (F2) |
| /architect | Activate the Mission Architect while inside Architect Entertainment. Alias: /missionsearch |
| /architect_claim_tickets # | Claims # Architect tickets |
| /architect_completemission | Complete the current mission while in Architect Test Mode |
| /architectexit | Return to the mission maker (opens the mission architect window) |
| /architectfixerrors | Fix Errors |
| /architect_invincible | Toggles Architect test mode invincibility on or off |
| /architect_invisible | Toggles Architect test mode invisibility on or off |
| /architect_killtarget | Defeats your currently selected target in the mission being tested |
| /architect_loginupdate | Shows amount of Architect tickets available to claim |
| /architect_nextcritter | Takes you to the next hostile entity in the mission being tested |
| /architect_nextobjective | Takes you to the next objective in the mission being tested |
| /architectrepublish | Republish mission |
| /architectsaveandexit | Save mission being edited and return to search window |
| /architectsaveandtest | Save mission being edited and test |
| /architect_save_compressed_costumes [0-1] | Toggle save file output to show compressed or uncompressed. |
| /arena_invite player | Invite player to join your arena event. Alias: /ai |
| /arena_local message | The Arena event window chat. |
| /arena_score | Open the arena score window if you are in an Arena match. |
| /assist_name player | Change your current target to specified ally's target |
| /attach_cycle | Toggle object placement attachment (Floor, Wall, Ceiling, Surface) while in the SG base editor. (F5) |
| /badgegrant BadgeGrantTag | Grants a character the specified badge (only works on Beta server) |
| /base_default_sky number | Sets SG base editing default sky setting to one of 16 preset values |
| /base_lighting_type number | Sets lighting type while in the supergroup base editor. 0 = Indoor, 1 = Outdoor sky lighting, 2 = Outdoor with shadows |
| /base_redo | Reverse your last Undo and/or repeat action while in the SG base editor. (Ctrl-Y) |
| /base_select | Select base object. |
| /base_undo | Reverse your last action while in the SG base editor. (Ctrl-Z) |
| /camdistadjust | Adjusts the camera distance relative to the current camera distance. |
| /center | While supergroup base editing, center alt on spot indicated. (Left-Doubleclick). |
| /centersel | Center on current selection (base editor). |
| /chan_invitedeny channel name_string | Chat channel invite denied message. Appears to be an internal command. |
| /change_handle new_global | Change your global user name, if allowed. |
| /clear_tray | Removes all power icons from all power trays; preserves macros |
| /cmdlist | Prints out most slash commands in the chat window |
| /compatiblecursors | Enables useage of basic Windows mouse cursors instead of graphical cursors (command line option) |
| /editbase [1/0] | Turns supergroup base editor on or off. |
| /extra_modifiers [mod1] [mod2] [mod3] [mod4] | Allows setting up to four extra modifiers on a controller/gamepad. |
| /grid_snap number | Sets item placement grid size while in the SG base editor. |
| /grid_snap_cycle | Cycles through object placement grid sizes while in the SG base editor. (F1) |
| /mousedrag | Enable dragging object while using the SG base editor. |
| /room_clip [0-1] | Enables or disables the room clipping option while in the SG base editor. Alias: /room_clip_cycle. (F3) |
| /room_clip_cycle | Toggle wall clipping on and off while in the SG base editor. Alias: /room_clip. (F3) |
| /rotate [0,1] | Rotate object 90 degrees while in the SG base editor. (R) or (Right-Click). |
| /see_everything [1/0] | See the boundary boxes and hidden markers for everything while in the SG base editor. |
| /select_last | Select previous object in series while in the SG base editor. (Shift+Tab) |
| /select_next | Select next present object in series while in the SG base editor. (Tab) |
| /sell (base editor) | Sells (deletes) a base item while editing a supergroup base. |
| /sg_music filename | Sets a sound file to play over the music channel in a supergroup base. |
| /thumbtack x y z | Adds a thumbtack to the map at the specified X/Y/Z coordinates |


## Slash Commands With Unknown Functionality

| Bind | Description |
|------|-------------|
| /badge_button_use <int> | Claim a badge button reward. (active but appears to do nothing) ? |
| /cgSaveShaderListing 0-1 | Save Cg shader listings in the current directory |
| /cgShaderPath path | Sets parent directory for "shaders/cgfx". If relative, path is resolved using the .exe root directory. |
| /client_pos_id | For letting the server know we got his position update command. (active but purpose/procedure unknown) ? |
| /createHero | Create a hero. (active but procedure unknown) ? |
| /createPraetorian | Create a Praetorian. (active but procedure unknown) ? |
| /createVillain | Create a villain. (active but procedure unknown) ? |
| /enterdoorteleport <string> <int> | request teleport to another map (active but procedure unknown) ? |
| /enterdoorvolume <string> | Request to enter a door via map volume. (unknown) ? |
| /enterscriptdoor <int> <string> <int> | enter a script controlled door. |
| /ignore_spammer_auth | Ignore As Spammer (GM/Admin command) |
| /linkAccountURL | URL for link account website (unknown functionality) ? |
| /markPowClosed <int> | Mark power closed (unknown functionality) ? |
| /markPowOpen <int> | Mark power open (unknown functionality - something to do with pets?) ? |
| /nagPraetorian | Explain the need to buy Going Rogue. ? |
| /newAccountURL | URL for new account creation website ? |
| /nohdr | Disable HDR lighting effects. ? |
| /nothread | Disables threaded texture loading |
| /petViewAttributes | View the attributes of the player's pet |
| /powers_cancel | Cancel all effects of specified power from the character if power is cancelable and target is you or your pet. |
| /redirect <int> | Internal command so smf can trigger the redirect menu |
| /reduce_min | Sets the minimum size that textures will be reduced to (requires -reduce_mip > 0) |
| /requestexitmissionalt | exit mission and teleport to another map ? |
| /runnerdebug | Enable limited debugging for a possible critter run-away bug |
| /selected_ent_server_index | send selected entity ? |
| /soundDebugName | name of sound to debug (will only play this sound name) ? |
| /splatShadowBias | Change how far from the camera to give people shadows. //scales distance to draw entitys' splat shadow. |
| /turnstile_invite_player_accept <dbID> <int> <int> | Invite player to the leaders instance ? |
| /useFBOs | Use FBOs, if supported, for off-screen rendering ? |
| /useMRTs | Use MRTs, for DoF effect debugging |
