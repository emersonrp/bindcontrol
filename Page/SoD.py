#!/usr/bin/perl

use strict;

package Page::SoD;
use parent "Page::Page";

use File::Spec;

use Utility qw(id);
use Wx qw();

our $PageName = 'SoD';

sub InitKeys {

	my $self = shift;

	$self->Profile->SoD ||= {
		Up => "SPACE",
		Down => "X",
		Forward => "W",
		Back => "S",
		Left => "A",
		Right => "D",
		TurnLeft => "Q",
		TurnRight => "E",
		AutoRun => "R",
		Follow => "TILDE",
		DefaultMode => '',
		MousechordSoD => 1,
		AutoMouseLook => 0,

		SprintPower => 'Sprint',

		ChangeCamera => 1,
		CamdistBase => 15,
		CamdistTravelling => 60,

		ChangeDetail => 1,
		DetailBase => 100,
		DetailTravelling => 50,

		NonSoDMode => 1,
		ToggleSoD => 'CTRL-M',
		JumpMode => "T",
		SimpleSJCJ => 1,

		RunMode => "C",
		SSOnlyWhenMoving => 0,
		SSSJModeEnable => 1,

		FlyMode => "F",
		GFlyMode => "G",

		SelfTellOnChange => 1,

		TPMode => 'SHIFT-LBUTTON',
		TPCombo => 'SHIFT',
		TPReset => 'CTRL-T',

		TTPMode => 'SHIFT-CTRL-LBUTTON',
		TTPCombo => 'SHIFT-CTRL',
		TTPReset => 'SHIFT-CTRL-T',

		TPHideWindows => 0,

		RunPrimary => "Super Speed",
		RunPrimaryNumber => 2,
		RunSecondary => "Sprint",
		RunSecondaryNumber => 1,
		FlyHover => 1,
		FlyFly => '',
		FlyGFly => '',
		Unqueue => 1,
		ToggleSoD => "CTRL+M",
		Enable => undef,
	};

	my $SoD = $self->Profile->SoD;

	$SoD->{'TPHideWindows'} ||= 1;

	$SoD->{'NovaMode'} ||= "T";
	$SoD->{'NovaTray'} ||= "4";

	$SoD->{'DwarfMode'} ||= "G";
	$SoD->{'DwarfTray'} ||= "5";

	if ($self->Profile->General->{'Archetype'} eq "Peacebringer") {
		$SoD->{'NovaNova'} = "Bright Nova";
		$SoD->{'DwarfDwarf'} = "White Dwarf";
		$SoD->{'HumanFormShield'} ||= "Shining Shield";

	} elsif ($self->Profile->General->{'Archetype'} eq "Warshade") {
		$SoD->{'NovaNova'} = "Dark Nova";
		$SoD->{'DwarfDwarf'} = "Black Dwarf";
		$SoD->{'HumanFormShield'} ||= "Gravity Shield";
	}

	$SoD->{'HumanMode'}    ||= "UNBOUND";
	$SoD->{'HumanTray'}    ||= "1";
	$SoD->{'HumanHumanPBind'} ||= "nop";
	$SoD->{'HumanNovaPBind'}  ||= "nop";
	$SoD->{'HumanDwarfPBind'} ||= "nop";

	#  Temp Travel Powers
	$SoD->{'TempTray'} ||= "6";
	$SoD->{'TempTraySwitch'} ||= "UNBOUND";
	$SoD->{'TempMode'} ||= "UNBOUND";
}

sub FillTab {

	my $self = shift;

	my $SoD = $self->Profile->SoD;

	my $topSizer = Wx::FlexGridSizer->new(0,2,10,10);

	$topSizer->Add( Wx::CheckBox->new( $self, id('USE_SOD'), "Enable Speed On Demand Binds" ), 0, Wx::wxTOP|Wx::wxLEFT, 10);
	$topSizer->AddSpacer(1);

	my $leftColumn = Wx::BoxSizer->new(Wx::wxVERTICAL);
	my $rightColumn = Wx::BoxSizer->new(Wx::wxVERTICAL);

	my %SoDDefaults = ( parent => $self, module => $SoD );

	##### MOVEMENT KEYS
	my $movementSizer = UI::ControlGroup->new($self, 'Movement Keys');

	for ( qw(Up Down Forward Back Left Right TurnLeft TurnRight) ){
		$movementSizer->AddLabeledControl({
			value => $_,
			type => 'keybutton',
			%SoDDefaults,
		});
	}
	# TODO!  fill this picker with only the appropriate bits.
	$movementSizer->AddLabeledControl({
		value => 'DefaultMode',
		type => 'combo',
		contents => ['No SoD','Sprint','Super Speed','Jump','Fly'],
		%SoDDefaults,
	});
	$movementSizer->AddLabeledControl({
		value => 'MousechordSoD',
		type => 'checkbox',
		%SoDDefaults,
	});
	$leftColumn->Add($movementSizer, 0, Wx::wxEXPAND);


	##### GENERAL SETTINGS
	my $generalSizer = UI::ControlGroup->new($self, 'General Settings');

	$generalSizer->AddLabeledControl({
		value => 'AutoMouselook',
		type => 'checkbox',
		tooltip => 'Automatically Mouselook when moving',
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'SprintPower',
		type => 'combo',
		contents => [@GameData::SprintPowers],
		%SoDDefaults,
	});

	# TODO -- decide what to do with this.
	# $generalSizer->Add( Wx::CheckBox->new($self, SPRINT_UNQUEUE, "Exec powexecunqueue"));

	for ( qw(AutoRun Follow NonSoDMode) ){ # TODO - lost "Sprint-Only SoD Mode" b/c couldn't find the name in %$Labels
		$generalSizer->AddLabeledControl({
			value => $_,
			type => 'keybutton',
			%SoDDefaults,
		});
	}
	$generalSizer->AddLabeledControl({
		value => 'ToggleSoD',
		type => 'keybutton',
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'SprintSoD',
		type => 'checkbox',
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'ChangeCamera',
		type => 'checkbox',
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'CamdistBase',
		type => 'spinbox',
		contents => [1, 100],
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'CamdistTravelling',
		type => 'spinbox',
		contents => [1, 100],
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'ChangeDetail',
		type => 'checkbox',
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'DetailBase',
		type => 'spinbox',
		contents => [1, 100],
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'DetailTravelling',
		type => 'spinbox',
		contents => [1, 100],
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'HideWinsDuringTP',
		type => 'checkbox',
		%SoDDefaults,
	});
	$generalSizer->AddLabeledControl({
		value => 'SelfTellOnChange',
		type => 'checkbox',
		%SoDDefaults,
	});
	$leftColumn->Add($generalSizer, 0, Wx::wxEXPAND);


	##### SUPER SPEED
	my $superSpeedSizer = UI::ControlGroup->new($self, 'Super Speed');
	$superSpeedSizer->AddLabeledControl({
		value => 'RunMode',
		type => 'keybutton',
		%SoDDefaults,
	});
	$superSpeedSizer->AddLabeledControl({
		value => 'SSOnlyWhenMoving',
		type => 'checkbox',
		%SoDDefaults,
	});
	$superSpeedSizer->AddLabeledControl({
		value => 'SSSJModeEnable',
		type => 'checkbox',
		%SoDDefaults,
	});
	$rightColumn->Add($superSpeedSizer, 0, Wx::wxEXPAND);

	##### SUPER JUMP
	my $superJumpSizer = UI::ControlGroup->new($self, 'Super Jump');
	$superJumpSizer->AddLabeledControl({
		value => 'JumpMode',
		type => 'keybutton',
		%SoDDefaults,
	});
	$superJumpSizer->AddLabeledControl({
		value => 'SimpleSJCJ',
		type => 'checkbox',
		%SoDDefaults,
	});
	$rightColumn->Add($superJumpSizer, 0, Wx::wxEXPAND);


	##### FLY
	my $flySizer = UI::ControlGroup->new($self, 'Flight');

	$flySizer->AddLabeledControl({
		value => 'FlyMode',
		type => 'keybutton',
		%SoDDefaults,
	});
	$flySizer->AddLabeledControl({
		value => 'GFlyMode',
		type => 'keybutton',
		%SoDDefaults,
	});
	$rightColumn->Add($flySizer, 0, Wx::wxEXPAND);

	##### TELEPORT
	my $teleportSizer = UI::ControlGroup->new($self, 'Teleport');

	# if (at == peacebringer) "Dwarf Step"
	# if (at == warshade) "Shadow Step / Dwarf Step"

	$teleportSizer->AddLabeledControl({
		value => "TPMode",
		type => 'keybutton',
		%SoDDefaults,
	});
	$teleportSizer->AddLabeledControl({
		value => "TPCombo",
		type => 'keybutton',
		%SoDDefaults,
	});
	$teleportSizer->AddLabeledControl({
		value => "TPReset",
		type => 'keybutton',
		%SoDDefaults,
	});

	# if (player has hover): {
		$teleportSizer->AddLabeledControl({
			value => 'AutoHoverTP',
			type => 'checkbox',
			%SoDDefaults,
		});
	# }

	# if (player has team-tp) {
		$teleportSizer->AddLabeledControl({
			value => "TTPMode",
			type => 'keybutton',
			%SoDDefaults,
		});
		$teleportSizer->AddLabeledControl({
			value => "TTPCombo",
			type => 'keybutton',
			%SoDDefaults,
		});
		$teleportSizer->AddLabeledControl({
			value => "TTPReset",
			type => 'keybutton',
			%SoDDefaults,
		});

		# if (player has group fly) {
			$teleportSizer->AddLabeledControl({
				value => 'AutoGFlyTTP',
				type => 'checkbox',
				%SoDDefaults,
			});
		# }
	# }
	$rightColumn->Add($teleportSizer, 0, Wx::wxEXPAND);

	##### TEMP TRAVEL POWERS
	my $tempSizer = UI::ControlGroup->new($self, 'Temp Travel Powers');
	# if (temp travel powers exist)?  Should this be "custom"?
	$tempSizer->AddLabeledControl({
		value => 'TempMode',
		type => 'keybutton',
		%SoDDefaults,
	});
	$tempSizer->AddLabeledControl({
		value => 'TempTray',
		type => 'spinbox',
		contents => [1, 8],
		%SoDDefaults,
	});
	$rightColumn->Add($tempSizer, 0, Wx::wxEXPAND);

	##### KHELDIAN TRAVEL POWERS
	my $kheldianSizer = UI::ControlGroup->new($self, 'Nova / Dwarf Travel Powers');

	$kheldianSizer->AddLabeledControl({
		value => 'NovaMode',
		type => 'keybutton',
		%SoDDefaults,
	});
	$kheldianSizer->AddLabeledControl({
		value => 'NovaTray',
		type => 'spinbox',
		contents => [1, 8],
		%SoDDefaults,
	});
	$kheldianSizer->AddLabeledControl({
		value => 'DwarfMode',
		type => 'keybutton',
		%SoDDefaults,
	});
	$kheldianSizer->AddLabeledControl({
		value => 'DwarfTray',
		type => 'spinbox',
		contents => [1, 8],
		%SoDDefaults,
	});

	# do we want a key to change directly to human form, instead of toggles?
	$kheldianSizer->AddLabeledControl({
		value => 'HumanMode',
		type => 'keybutton',
		%SoDDefaults,
	});
	$kheldianSizer->AddLabeledControl({
		value => 'HumanTray',
		type => 'spinbox',
		contents => [1, 8],
		%SoDDefaults,
	});

	$rightColumn->Add($kheldianSizer, 0, Wx::wxEXPAND);

	$topSizer->Add($leftColumn);
	$topSizer->Add($rightColumn);

	$self->SetSizer($topSizer);

	$self->TabTitle = "Speed On Demand";

	return $self;
}


sub makeSoDFile {
	my $p = shift;

	my $t = $p->{'t'};

	my $profile = $t->{'profile'};

	my $bl   = defined $p->{'bl'}   ? $t->bl($p->{'bl'})   : '';
	my $bla  = defined $p->{'bla'}  ? $t->bl($p->{'bla'})  : '';
	my $blf  = defined $p->{'blf'}  ? $t->bl($p->{'blf'})  : '';
	my $blbo = defined $p->{'blbo'} ? $t->bl($p->{'blbo'}) : '';
	my $blsd = defined $p->{'blsd'} ? $t->bl($p->{'blsd'}) : '';

	my $path   = defined $p->{'path'}   ? $t->path($p->{'path'})   : '';
	my $pathr  = defined $p->{'pathr'}  ? $t->path($p->{'pathr'})  : '';
	my $pathf  = defined $p->{'pathf'}  ? $t->path($p->{'pathf'})  : '';
	my $pathbo = defined $p->{'pathbo'} ? $t->path($p->{'pathbo'}) : '';
	my $pathsd = defined $p->{'pathsd'} ? $t->path($p->{'pathsd'}) : '';

	my $mobile     = $p->{'mobile'}     || '';
	my $stationary = $p->{'stationary'} || '';
	my $modestr    = $p->{'modestr'}    || '';
	my $flight     = $p->{'flight'}     || '';
	my $fix        = $p->{'fix'}        || '';
	my $turnoff    = $p->{'turnoff'}    || '';
	my $sssj       = $p->{'sssj'}       || '';

	my $SoD = $profile->SoD;
	my $curfile;

	# this wants to be $turnoff ||= $mobile, $stationary once we know what those are.  arrays?  hashes?
	$turnoff ||= {$mobile,$stationary};

	if (($SoD->{'Default'} eq $modestr) and ($t->{'totalkeys'} == 0)) {

		$curfile = $profile->General->{'ResetFile'};
		sodDefaultResetKey($mobile,$stationary);

		sodUpKey     ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
		sodDownKey   ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
		sodForwardKey($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
		sodBackKey   ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
		sodLeftKey   ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
		sodRightKey  ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);

		if ($modestr eq "NonSoD") { makeNonSoDModeKey($profile,$t,"r", $curfile,{$mobile,$stationary}); }
		if ($modestr eq "Base")   { makeBaseModeKey  ($profile,$t,"r", $curfile,$turnoff,$fix); }
		if ($modestr eq "Fly")    { makeFlyModeKey   ($profile,$t,"bo",$curfile,$turnoff,$fix); }
		if ($modestr eq "GFly")   { makeGFlyModeKey  ($profile,$t,"gf",$curfile,$turnoff,$fix); }
		if ($modestr eq "Run")    { makeSpeedModeKey ($profile,$t,"s", $curfile,$turnoff,$fix); }
		if ($modestr eq "Jump")   { makeJumpModeKey  ($profile,$t,"j", $curfile,$turnoff,$path); }
		if ($modestr eq "Temp")   { makeTempModeKey  ($profile,$t,"r", $curfile,$turnoff,$path); }
		if ($modestr eq "QFly")   { makeQFlyModeKey  ($profile,$t,"r", $curfile,$turnoff,$modestr); }
	
		sodAutoRunKey($t,$bla,$curfile,$SoD,$mobile,$sssj);
	
		sodFollowKey($t,$blf,$curfile,$SoD,$mobile);
	}

	if ($flight and ($flight eq "Fly") and $pathbo) {
		#  blast off
		$curfile = $profile->GetBindFile($pathbo);
		sodResetKey($curfile,$profile,$path,actPower_toggle(undef,1,$stationary,$mobile),'');

		sodUpKey     ($t,$blbo,$curfile,$SoD,$mobile,$stationary,$flight,'','',"bo",$sssj);
		sodDownKey   ($t,$blbo,$curfile,$SoD,$mobile,$stationary,$flight,'','',"bo",$sssj);
		sodForwardKey($t,$blbo,$curfile,$SoD,$mobile,$stationary,$flight,'','',"bo",$sssj);
		sodBackKey   ($t,$blbo,$curfile,$SoD,$mobile,$stationary,$flight,'','',"bo",$sssj);
		sodLeftKey   ($t,$blbo,$curfile,$SoD,$mobile,$stationary,$flight,'','',"bo",$sssj);
		sodRightKey  ($t,$blbo,$curfile,$SoD,$mobile,$stationary,$flight,'','',"bo",$sssj);

		# if ($modestr eq "Base") { makeBaseModeKey($profile,$t,"r",$curfile,$turnoff,$fix); }
		$t->{'ini'} = '-down$$';

		if ($SoD->{'Default'} eq "Fly") {

			if ($SoD->{'NonSoD'}) {
				$t->{'FlyMode'} = $t->{'NonSoDMode'};
				makeFlyModeKey($profile,$t,"a",$curfile,$turnoff,$fix);
			}
			if ($SoD->{'Base'}) {
				$t->{'FlyMode'} = $t->{'BaseMode'};
				makeFlyModeKey($profile,$t,"a",$curfile,$turnoff,$fix);
			}
			if ($t->{'canss'}) {
				$t->{'FlyMode'} = $t->{'RunMode'};
				makeFlyModeKey($profile,$t,"a",$curfile,$turnoff,$fix);
			}
			if ($t->{'canjmp'}) {
				$t->{'FlyMode'} = $t->{'JumpMode'};
				makeFlyModeKey($profile,$t,"a",$curfile,$turnoff,$fix);
			}
			if ($SoD->{'Temp'} and $SoD->{'TempEnable'}) {
				$t->{'FlyMode'} = $t->{'TempMode'};
				makeFlyModeKey($profile,$t,"a",$curfile,$turnoff,$fix);
			}
		} else {
			makeFlyModeKey($profile,$t,"a",$curfile,$turnoff,$fix);
		}

		$t->{'ini'} = '';
		# if ($modestr eq "GFly") { makeGFlyModeKey($profile,$t,"gbo",$curfile,$turnoff,$fix); }
		# if ($modestr eq "Run") { makeSpeedModeKey ($profile,$t,"s",$curfile,$turnoff,$fix); }
		# if ($modestr eq "Jump") { makeJumpModeKey($profile,$t,"j",$curfile,$turnoff,$path); }

		sodAutoRunKey($t,$bla,$curfile,$SoD,$mobile,$sssj);

		sodFollowKey($t,$blf,$curfile,$SoD,$mobile);

		# $curfile = $profile->GetBindFile($pathsd);

		sodResetKey($curfile,$profile,$path,actPower_toggle(undef,1,$stationary,$mobile),'');

		sodUpKey     ($t,$blsd,$curfile,$SoD,$mobile,$stationary,$flight,'','',"sd",$sssj);
		sodDownKey   ($t,$blsd,$curfile,$SoD,$mobile,$stationary,$flight,'','',"sd",$sssj);
		sodForwardKey($t,$blsd,$curfile,$SoD,$mobile,$stationary,$flight,'','',"sd",$sssj);
		sodBackKey   ($t,$blsd,$curfile,$SoD,$mobile,$stationary,$flight,'','',"sd",$sssj);
		sodLeftKey   ($t,$blsd,$curfile,$SoD,$mobile,$stationary,$flight,'','',"sd",$sssj);
		sodRightKey  ($t,$blsd,$curfile,$SoD,$mobile,$stationary,$flight,'','',"sd",$sssj);

		$t->{'ini'} = '-down$$';
		# if ($modestr eq "Base") { makeBaseModeKey($profile,$t,"r",$curfile,$turnoff,$fix); }
		# if ($modestr eq "Fly") { makeFlyModeKey($profile,$t,"a",$curfile,$turnoff,$fix); }
		# if ($modestr eq "GFly") { makeGFlyModeKey($profile,$t,"gbo",$curfile,$turnoff,$fix); }
		$t->{'ini'} = '';
		# if ($modestr eq "Jump") { makeJumpModeKey($profile,$t,"j",$curfile,$turnoff,$path); }

		sodAutoRunKey($t,$bla,$curfile,$SoD,$mobile,$sssj);
		sodFollowKey($t,$blf,$curfile,$SoD,$mobile);
	}

	$curfile = $profile->GetBindFile($path);

	sodResetKey($curfile,$profile,$path,actPower_toggle(undef,1,$stationary,$mobile),'');

	sodUpKey     ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
	sodDownKey   ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
	sodForwardKey($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
	sodBackKey   ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
	sodLeftKey   ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);
	sodRightKey  ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,'','','',$sssj);

	if (($flight eq "Fly") and $pathbo) {
		#  Base to set down
		if ($modestr eq "NonSoD") { makeNonSoDModeKey($profile,$t,"r",$curfile,{$mobile,$stationary},\&sodSetDownFix); }
		if ($modestr eq "Base")   { makeBaseModeKey  ($profile,$t,"r",$curfile,$turnoff,\&sodSetDownFix); }
		# if ($t->{'BaseMode'}) {
			# $curfile->SetBind($t->{'BaseMode'},"+down$$down 1" . actPower_name(undef,1,$mobile) . $t->{'detailhi'} . $t->{'runcamdist'} . $t->{'blsd'})
		#}
		if ($modestr eq "Run")     { makeSpeedModeKey ($profile,$t,"s", $curfile,$turnoff,\&sodSetDownFix); }
		if ($modestr eq "Fly")     { makeFlyModeKey   ($profile,$t,"bo",$curfile,$turnoff,$fix); }
		if ($modestr eq "Jump")    { makeJumpModeKey  ($profile,$t,"j", $curfile,$turnoff,$path); }
		if ($modestr eq "Temp")    { makeTempModeKey  ($profile,$t,"r", $curfile,$turnoff,$path); }
		if ($modestr eq "QFly")    { makeQFlyModeKey  ($profile,$t,"r", $curfile,$turnoff,$modestr); }
	} else {
		if ($modestr eq "NonSoD")  { makeNonSoDModeKey($profile,$t,"r", $curfile,{$mobile,$stationary}); }
		if ($modestr eq "Base")    { makeBaseModeKey  ($profile,$t,"r", $curfile,$turnoff,$fix); }
		if ($flight eq "Jump") {
			if ($modestr eq "Fly") { makeFlyModeKey   ($profile,$t,"a", $curfile,$turnoff,$fix,undef,1); }
		} else {
			if ($modestr eq "Fly") { makeFlyModeKey   ($profile,$t,"bo",$curfile,$turnoff,$fix); }
		}
		if ($modestr eq "Run")    { makeSpeedModeKey  ($profile,$t,"s", $curfile,$turnoff,$fix); }
		if ($modestr eq "Jump")   { makeJumpModeKey   ($profile,$t,"j", $curfile,$turnoff,$path); }
		if ($modestr eq "Temp")   { makeTempModeKey   ($profile,$t,"r", $curfile,$turnoff,$path); }
		if ($modestr eq "QFly")   { makeQFlyModeKey   ($profile,$t,"r", $curfile,$turnoff,$modestr); }
	}

	sodAutoRunKey($t,$bla,$curfile,$SoD,$mobile,$sssj);

	sodFollowKey($t,$blf,$curfile,$SoD,$mobile);

# AutoRun Binds
	$curfile = $profile->GetBindFile($pathr);

	sodResetKey($curfile,$profile,$path,actPower_toggle(undef,1,$stationary,$mobile),'');

	sodUpKey     ($t,$bla,$curfile,$SoD,$mobile,$stationary,$flight,1,'','',$sssj);
	sodDownKey   ($t,$bla,$curfile,$SoD,$mobile,$stationary,$flight,1,'','',$sssj);
	sodForwardKey($t,$bla,$curfile,$SoD,$mobile,$stationary,$flight,$bl, '','',$sssj);
	sodBackKey   ($t,$bla,$curfile,$SoD,$mobile,$stationary,$flight,$bl, '','',$sssj);
	sodLeftKey   ($t,$bla,$curfile,$SoD,$mobile,$stationary,$flight,1,'','',$sssj);
	sodRightKey  ($t,$bla,$curfile,$SoD,$mobile,$stationary,$flight,1,'','',$sssj);

	if (($flight eq "Fly") and $pathbo) {
		if ($modestr eq "NonSoD") { makeNonSoDModeKey($profile,$t,"ar",$curfile,{$mobile,$stationary},\&sodSetDownFix); }
		if ($modestr eq "Base")   { makeBaseModeKey  ($profile,$t,"gr",$curfile,$turnoff,\&sodSetDownFix); }
		if ($modestr eq "Run")    { makeSpeedModeKey ($profile,$t,"as",$curfile,$turnoff,\&sodSetDownFix); }
	} else {
		if ($modestr eq "NonSoD") { makeNonSoDModeKey($profile,$t,"ar",$curfile,{$mobile,$stationary}); }
		if ($modestr eq "Base")   { makeBaseModeKey  ($profile,$t,"gr",$curfile,$turnoff,$fix); }
		if ($modestr eq "Run")    { makeSpeedModeKey ($profile,$t,"as",$curfile,$turnoff,$fix); }
	}
	if ($modestr eq "Fly")        { makeFlyModeKey   ($profile,$t,"af",$curfile,$turnoff,$fix); }
	if ($modestr eq "Jump")       { makeJumpModeKey  ($profile,$t,"aj",$curfile,$turnoff,$pathr); }
	if ($modestr eq "Temp")       { makeTempModeKey  ($profile,$t,"ar",$curfile,$turnoff,$path); }
	if ($modestr eq "QFly")       { makeQFlyModeKey  ($profile,$t,"ar",$curfile,$turnoff,$modestr); }

	sodAutoRunOffKey($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight);

	$curfile->SetBind($SoD->{'Follow'},'nop');

# FollowRun Binds
	$curfile = $profile->GetBindFile($pathf);

   	sodResetKey($curfile,$profile,$path,actPower_toggle(undef,1,$stationary,$mobile),'');
   
   	sodUpKey     ($t,$blf,$curfile,$SoD,$mobile,$stationary,$flight,'',$bl,'',$sssj);
   	sodDownKey   ($t,$blf,$curfile,$SoD,$mobile,$stationary,$flight,'',$bl,'',$sssj);
   	sodForwardKey($t,$blf,$curfile,$SoD,$mobile,$stationary,$flight,'',$bl,'',$sssj);
   	sodBackKey   ($t,$blf,$curfile,$SoD,$mobile,$stationary,$flight,'',$bl,'',$sssj);
   	sodLeftKey   ($t,$blf,$curfile,$SoD,$mobile,$stationary,$flight,'',$bl,'',$sssj);
   	sodRightKey  ($t,$blf,$curfile,$SoD,$mobile,$stationary,$flight,'',$bl,'',$sssj);
   
   	if (($flight eq "Fly") and $pathbo) {
   		if ($modestr eq "NonSoD") { makeNonSoDModeKey($profile,$t,"fr",$curfile,{$mobile,$stationary},\&sodSetDownFix); }
   		if ($modestr eq "Base")   { makeBaseModeKey  ($profile,$t,"fr",$curfile,$turnoff,\&sodSetDownFix); }
   		if ($modestr eq "Run")    { makeSpeedModeKey ($profile,$t,"fs",$curfile,$turnoff,\&sodSetDownFix); }
   	} else {
   		if ($modestr eq "NonSoD") { makeNonSoDModeKey($profile,$t,"fr",$curfile,{$mobile,$stationary}); }
   		if ($modestr eq "Base")   { makeBaseModeKey  ($profile,$t,"fr",$curfile,$turnoff,$fix); }
   		if ($modestr eq "Run")    { makeSpeedModeKey ($profile,$t,"fs",$curfile,$turnoff,$fix); }
   	}
   	if ($modestr eq "Fly")        { makeFlyModeKey   ($profile,$t,"ff",$curfile,$turnoff,$fix); }
   	if ($modestr eq "Jump")       { makeJumpModeKey  ($profile,$t,"fj",$curfile,$turnoff,$pathf); }
   	if ($modestr eq "Temp")       { makeTempModeKey  ($profile,$t,"fr",$curfile,$turnoff,$path); }
   	if ($modestr eq "QFly")       { makeQFlyModeKey  ($profile,$t,"fr",$curfile,$turnoff,$modestr); }

   	$curfile->SetBind($SoD->{'AutoRun'},'nop');

   	sodFollowOffKey($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight);
}

# TODO -- seems like these subs could get consolidated but stab one at that was feeble
sub makeNonSoDModeKey{
	my ($p,$t,$bl,$cur,$toff,$fix, $fb) = @_;
	my $key = $t->{'NonSoDMode'};
	return if (not $key or $key eq 'UNBOUND');

	my $feedback = $p->SoD->{'Feedback'} ? ($fb or '$$t $name, Non-SoD Mode') : '';
	$t->{'ini'} ||= '';
	if ($bl eq "r") {
		my $bindload = $t->bl('n');
		if ($fix) {
			&$fix($p,$t,$key, \&makeNonSoDModeKey,"n",$bl,$cur,$toff,'',$feedback)
		} else {
			$cur->SetBind($key, $t->{'ini'} . actPower_toggle(undef,1,undef,$toff) . $t->dirs('UDFBLR') . $t->{'detailhi'} . $t->{'runcamdist'} . $feedback . $bindload)
		}
	} elsif ($bl eq "ar") {
		my $bindload = $t->bl('an');
		if ($fix) {
			&$fix($p,$t,$key, \&makeNonSoDModeKey,"n",$bl,$cur,$toff,"a",$feedback)
		} else {
			$cur->SetBind($key, $t->{'ini'} . actPower_toggle(undef,1,undef,$toff)..$t->{'detailhi'} . $t->{'runcamdist'} . '$$up 0' . $t->dirs('DLR') . $feedback . $bindload);
		}
	} else {
		if ($fix) {
			&$fix($p,$t,$key, \&makeNonSoDModeKey,"n",$bl,$cur,$toff,"f",$feedback)
		} else {
			$cur->SetBind($key, $t->{'ini'} . actPower_toggle(undef,1,undef,$toff)..$t->{'detailhi'} . $t->{'runcamdist'} . '$$up 0' . $feedback . $t->bl('fn'));
		}
	}
	$t->{'ini'} = '';
}

# ODO -- seems like these subs could get consolidated but stab one at that was feeble
sub makeTempModeKey  {
	my ($p,$t,$bl,$cur,$toff) = @_;
	my $key = $t->{'TempMode'};
	return if (not $key or $key eq "UNBOUND");

	my $feedback = $p->SoD->{'Feedback'} ? '$$t $name, Temp Mode' : '';
	$t->{'ini'} ||= '';
	my $trayslot = "1 $p->SoD->{'TempTray'}";

	if ($bl eq "r") {
		my $bindload = $t->bl('t');
		$cur->SetBind($key, $t->{'ini'} . actPower(undef,1,$trayslot,$toff) . $t->dirs('UDFBLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $bindload);
	} elsif ($bl eq "ar") {
		my $bindload  = $t->bl('at');
		my $bindload2 = $t->bl('at','_t');
		my $tgl = $p->GetBindFile($bindload2);
		$cur->SetBind($key, $t->{'in'} . actPower(undef,1,$trayslot,$toff) . $t->{'detaillo'} . $t->{'flycamdist'} . '$$up 0' . $t->dirs('DLR') . $feedback . $bindload2);
		$tgl->SetBind($key, $t->{'in'} . actPower(undef,1,$trayslot,$toff) . $t->{'detaillo'} . $t->{'flycamdist'} . '$$up 0' . $t->dirs('DLR') . $feedback . $bindload);
	} else {
		$cur->SetBind($key, $t->{'ini'} . actPower(undef,1,$trayslot,$toff) . $t->{'detaillo'} . $t->{'flycamdist'} . '$$up 0' . $feedback . $t->bl('ft'));
	}
	$t->{'ini'} = '';
}


# TODO -- seems like these subs could get consolidated but stab one at that was feeble
sub makeQFlyModeKey  {
	my ($p,$t,$bl,$cur,$toff,$modestr) = @_;
	my $key = $t->{'QFlyMode'};
	return if (not $key or $key eq "UNBOUND");

	if ($modestr eq "NonSoD") { $cur->SetBind($key, "powexecname Quantum Flight") && return; }

	my $feedback = $p->SoD->{'Feedback'} ? '$$t $name, QFlight Mode' : '';
	$t->{'ini'} ||= '';

	if ($bl eq "r") {
		my $bindload  = $t->bl('n');
		my $bindload2 = $t->bl('n'.'_q');
		my $tgl = $p->GetBindFile($bindload2);

		my $tray = ($modestr eq 'Nova' or $modestr eq 'Dwarf') ? '$$gototray 1' : '';

		$cur->SetBind($key, $t->{'ini'} . actPower(undef,1,'Quantum Flight', $toff) . $tray . $t->dirs('UDFBLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $bindload2);
		$tgl->SetBind($key, $t->{'ini'} . actPower(undef,1,'Quantum Flight', $toff) . $tray . $t->dirs('UDFBLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $bindload);

	} elsif ($bl eq "ar") {
		my $bindload  = $t->bl('an');
		my $bindload2 = $t->bl('an','_t');
		my $tgl = $p->GetBindFile($bindload2);
		$cur->SetBind($key, $t->{'in'} . actPower(undef,1,'Quantum Flight', $toff) . $t->{'detaillo'} . $t->{'flycamdist'} . '$$up 0' . $t->dirs('DLR') . $feedback . $bindload2);
		$tgl->SetBind($key, $t->{'in'} . actPower(undef,1,'Quantum Flight', $toff) . $t->{'detaillo'} . $t->{'flycamdist'} . '$$up 0' . $t->dirs('DLR') . $feedback . $bindload);
	} else {
		$cur->SetBind($key, $t->{'ini'} . actPower(undef,1,'Quantum Flight', $toff) . $t->{'detaillo'} . $t->{'flycamdist'} . '$$up 0' . $feedback . $t->bl('fn'));
	}
	$t->{'ini'} = '';
}

# TODO -- seems like these subs could get consolidated but stab one at that was feeble
sub makeBaseModeKey  {
	my ($p,$t,$bl,$cur,$toff,$fix,$fb) = @_;
	my $key = $t->{'BaseMode'};
	return if (not $key or $key eq "UNBOUND");

	my $feedback = $p->SoD->{'Feedback'} ? ($fb or '$$t $name, Sprint-SoD Mode') : '';
	$t->{'ini'} ||= '';

	if ($bl eq "r") {
		my $bindload  = $t->bl();

		my $ton = actPower_toggle(1, 1, ($t->{'horizkeys'} ? $t->{'sprint'} : ''), $toff);

		if ($fix) {
			&$fix($p,$t,$key, \&makeBaseModeKey,"r",$bl,$cur,$toff,'',$feedback)
		} else {
			$cur->SetBind($key, $t->{'ini'} . $ton . $t->dirs('UDFBLR') . $t->{'detailhi'} . $t->{'runcamdist'} . $feedback . $bindload);
		}

	} elsif ($bl eq "ar") {
		my $bindload  = $t->bl('gr');

		if ($fix) {
			&$fix($p,$t,$key, \&makeBaseModeKey,"r",$bl,$cur,$toff,"a",$feedback)
		} else {
			$cur->SetBind($key, $t->{'ini'} . actPower_toggle(1,1,$t->{'sprint'},$toff) . $t->{'detailhi'} .  $t->{'runcamdist'} . '$$up 0' . $t->dirs('DLR') . $feedback . $bindload);
		}
	} else {
		if ($fix) {
			&$fix($p,$t,$key, \&makeBaseModeKey,"r",$bl,$cur,$toff,"f",$feedback)
		} else {
			$cur->SetBind($key, $t->{'ini'} . actPower_toggle(1,1,$t->{'sprint'}, $toff) . $t->{'detailhi'} . $t->{'runcamdist'} . '$$up 0' . $fb . $t->bl('fr'));
		}
	}
	$t->{'ini'} = '';
}

# TODO -- seems like these subs could get consolidated but stab one at that was feeble
sub makeSpeedModeKey   {
	my ($p,$t,$bl,$cur,$toff,$fix,$fb) = @_;
	my $key = $t->{'RunMode'};
	my $feedback = $p->SoD->{'Feedback'} ? ($fb or '$$t $name, Superspeed Mode') : '';
	$t->{'ini'} ||= '';
	if ($t->{'canss'}) {
		if ($bl eq 's') {
			my $bindload = $t->bl('s');
			if ($fix) {
				&$fix($p,$t,$key,\&makeSpeedModeKey,"s",$bl,$cur,$toff,'',$feedback)
			} else {
				$cur->SetBind($key,$t->{'ini'} . actPower_toggle(1,1,$t->{'speed'},$toff) . $t->dirs('UDFBLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $bindload);
			}
		} elsif ($bl eq "as") {
			my $bindload = $t->bl('as');
			if ($fix) {
				&$fix($p,$t,$key,\&makeSpeedModeKey,"s",$bl,$cur,$toff,"a",$feedback)
			} elsif (not $feedback) {
				$cur->SetBind($key,$t->{'ini'} . actPower_toggle(1,1,$t->{'speed'},$toff) . $t->dirs('UDLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $bindload);
			} else {
				my $bindload  = $t->bl('as');
				my $bindload2 = $t->bl('as','_s');
				my $tgl = $p->GetBindFile($bindload2);
				$cur->SetBind($key,$t->{'ini'} . actPower_toggle(1,1,$t->{'speed'},$toff) . $t->dirs('UDLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $bindload2);
				$tgl->SetBind($key,$t->{'ini'} . actPower_toggle(1,1,$t->{'speed'},$toff) . $t->dirs('UDLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $bindload);
			}
		} else {
			if ($fix) {
				&$fix($p,$t,$key,\&makeSpeedModeKey,"s",$bl,$cur,$toff,"f",$feedback)
			} else {
				$cur->SetBind($key, $t->{'ini'} . actPower_toggle(1,1,$t->{'speed'},$toff) . '$$up 0' .  $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $t->bl('fs'));
			}
		}
	}

	$t->{'ini'} = '';
}

# TODO -- seems like these subs could get consolidated but stab one at that was feeble
sub makeJumpModeKey  {
	my ($p,$t,$bl,$cur,$toff,$fbl) = @_;
	my $key = $t->{'JumpMode'};
	if ($t->{'canjmp'} and not $p->SoD->{'JumpSimple'}) {

		my $feedback = $p->SoD->{'Feedback'} ? '$$t $name, Superjump Mode' : '';
		my $tgl = $p->GetBindFile($fbl);

		if ($bl eq "j") {
			my $a;
			if ($t->{'horizkeys'} + $t->{'space'} > 0) {
				$a = actPower(undef,1,$t->{'jump'},$toff) . '$$up 1';
			} else {
				$a = actPower(undef,1,$t->{'cjmp'},$toff);
			}
			my $bindload = $t->bl('j');
			$tgl->SetBind($key, '-down' . $a . $t->{'detaillo'} . $t->{'flycamdist'} . $bindload);
			$cur->SetBind($key, '+down' . $feedback . BindFile::BLF($p, $fbl));
		} elsif ($bl eq "aj") {
			my $bindload = $t->bl('aj');
			$tgl->SetBind($key, '-down' . actPower(undef,1,$t->{'jump'},$toff) . '$$up 1' . $t->{'detaillo'} . $t->{'flycamdist'} . $t->dirs('DLR') . $bindload);
			$cur->SetBind($key, '+down' . $feedback . BindFile::BLF($p, $fbl));
		} else {
			$tgl->SetBind($key, '-down' . actPower(undef,1,$t->{'jump'},$toff) . '$$up 1' . $t->{'detaillo'} . $t->{'flycamdist'} . $t->bl('fj'));
			$cur->SetBind($key, '+down' . $feedback . BindFile::BLF($p, $fbl));
		}
	}
	$t->{'ini'} = '';
}

# TODO -- seems like these subs could get consolidated but stab one at that was feeble
sub makeFlyModeKey   {
	my ($p,$t,$bl,$cur,$toff,$fix,$fb,$fb_on_a) = @_;
	my $key = $t->{'FlyMode'};
	return if (not $key or $key eq "UNBOUND");
	my $feedback = $p->SoD->{'Feedback'} ? ($fb or '$$t $name, Flight Mode') : '';

	$t->{'ini'} ||= '';
	if ($t->{'canhov'} + $t->{'canfly'} > 0) {
		if ($bl eq "bo") {
			my $bindload = $t->bl('bo');
			if ($fix) {
				&$fix($p,$t,$key,\&makeFlyModeKey,"f",$bl,$cur,$toff,'',$feedback);
			} else {
				$cur->SetBind($key,'+down$$' . actPower_toggle(1,1,$t->{'flyx'},$toff) . '$$up 1$$down 0' . $t->dirs('FBLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $bindload);
			}
		} elsif ($bl eq "a") {
			if (not $fb_on_a) { $feedback = ''; }
			my $bindload = $t->bl('a');
			my $ton = $t->{'tkeys'} ? $t->{'flyx'} : $t->{'hover'};
			if ($fix) {
				&$fix($p,$t,$key,\&makeFlyModeKey,"f",$bl,$cur,$toff,'',$feedback);
			} else {
				$cur->SetBind($t-{'FlyMode'}, $t->{'ini'} . actPower_toggle(1,1,$ton ,$toff) . $t->dirs('UDLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $bindload)
			}
		} elsif ($bl eq "af") {
			my $bindload = $t->bl('af');
			if ($fix) {
				&$fix($p,$t,$key,\&makeFlyModeKey,"f",$bl,$cur,$toff,"a",$feedback);
			} else {
				$cur->SetBind($key, $t->{'ini'} . actPower_toggle(1,1,$t->{'flyx'},$toff) . $t->{'detaillo'} . $t->{'flycamdist'} . $t->dirs('DLR') . $feedback . $bindload)
			}
		} else {
			if ($fix) {
				&$fix($p,$t,$key,\&makeFlyModeKey,"f",$bl,$cur,$toff,"f",$feedback);
			} else {
				$cur->SetBind($key, $t->{'ini'} . actPower_toggle(1,1,$t->{'flyx'},$toff) . $t->dirs('UDFBLR') . $t->{'detaillo'} . $t->{'flycamdist'} . $feedback . $t->bl('ff'));
			}
		}
	}

	$t->{'ini'} = '';
}

# TODO -- seems like these subs could get consolidated but stab one at that was feeble
sub makeGFlyModeKey  {
	my ($p,$t,$bl,$cur,$toff,$fix) = @_;
	my $key = $t->{'GFlyMode'};

	$t->{'ini'} ||= '';
	if ($t->{'cangfly'} > 0) {
		if ($bl eq "gbo") {
			my $bindload = $t->bl('gbo');
			if ($fix) {
				&$fix($p,$t,$key,\&makeGFlyModeKey,"gf",$bl,$cur,$toff,'','');
			} else {
				$cur->SetBind($key,$t->{'ini'} . '$$up 1$$down 0' . actPower_toggle(undef,1,$t->{'gfly'},$toff) . $t->dirs('FBLR') . $t->{'detaillo'} . $t->{'flycamdist'} .$bindload);
			}
		} elsif ($bl eq "gaf") {
			my $bindload = $t->bl('gaf');
			if ($fix) {
				&$fix($p,$t,$key,\&makeGFlyModeKey,"gf",$bl,$cur,$toff,"a")
			} else {
				$cur->SetBind($key,$t->{'ini'} . $t->{'detaillo'} . $t->{'flycamdist'} . $t->dirs('UDLR') . $bindload);
			}
		} else {
			if ($fix) {
				&$fix($p,$t,$key,\&makeGFlyModeKey,"gf",$bl,$cur,$toff,"f")
			} else {
				if ($bl eq "gf") {
					$cur->SetBind($key,$t->{'ini'} . actPower_toggle(1,1,$t->{'gfly'},$toff) . $t->{'detaillo'} . $t->{'flycamdist'} . $t->bl('gff'));
				} else {
					$cur->SetBind($key,$t->{'ini'} . $t->{'detaillo'} . $t->{'flycamdist'} . $t->bl('gff'));
				}
			}
		}
	}
	$t->{'ini'} = '';
}

sub iupMessage { print STDERR "ZOMG SOMEBODY IMPLEMENT A WARNING DIALOG!!!\n"; }

sub PopulateBindFiles {

	my $profile = shift->Profile;

	my $ResetFile = $profile->General->{'ResetFile'};
	my $SoD = $profile->SoD;

	# $ResetFile->SetBind(petselec$t->{'sel5'} . ' "petselect 5')
	if ($SoD->{'Default'} eq "NonSoD") {
		if (not $SoD->{'NonSoD'}) { iupMessage("Notice","Enabling NonSoD mode, since it is set as your default mode.") }
		$SoD->{'NonSoD'} = 1;
	}
	if ($SoD->{'Default'} eq "Base" and not $SoD->{'Base'}) {
		iupMessage("Notice","Enabling NonSoD mode and making it the default, since Sprint SoD, your previous Default mode, is not enabled.");
		$SoD->{'NonSoD'} = 1;
		$SoD->{'Default'} = "NonSoD";
	}
	if ($SoD->{'Default'} eq "Fly" and not ($SoD->{'FlyHover'} or $SoD->{'FlyFly'})) {
		iupMessage("Notice","Enabling NonSoD mode and making it the default, since Flight SoD, your previous Default mode, is not enabled.");
		$SoD->{'NonSoD'} = 1;
		$SoD->{'Default'} = "NonSoD";
	}
	if ($SoD->{'Default'} eq "Jump" and not ($SoD->{'JumpCJ'} or $SoD->{'JumpSJ'})) {
		iupMessage("Notice","Enabling NonSoD mode and making it the default, since Superjump SoD, your previous Default mode, is not enabled.");
		$SoD->{'NonSoD'} = 1;
		$SoD->{'Default'} = "NonSoD";
	}
	if ($SoD->{'Default'} eq "Run" and $SoD->{'RunPrimaryNumber'} == 1) {
		iupMessage("Notice","Enabling NonSoD mode and making it the default, since Superspeed SoD, your previous Default mode, is not enabled.");
		$SoD->{'NonSoD'} = 1;
		$SoD->{'Default'} = "NonSoD";
	}

	my $t = Page::SoD::Table->new({
		profile => $profile,
		sprint => '',
		speed => '',
		hover => '',
		fly => '',
		flyx => '',
		jump => '',
		cjmp => '',
		canhov => 0,
		canfly => 0,
		canqfly => 0,
		cangfly => 0,
		cancj => 0,
		canjmp => 0,
		canss => 0,
		tphover => '',
		ttpgrpfly => '',
		on => '$$powexectoggleon ',
		# on => '$$powexecname ',
		off => '$$powexectoggleoff ',
		mlon => '',
		mloff => '',
		runcamdist => '',
		flycamdist => '',
		detailhi => '',
		detaillo => '',
	});

	if ($SoD->{'JumpCJ'} and not $SoD->{'JumpSJ'}) {
		$t->{'cancj'} = 1;
		$t->{'cjmp'} = "Combat Jumping";
		$t->{'jump'} = "Combat Jumping";
	}
	if (not $SoD->{'JumpCJ'} and $SoD->{'JumpSJ'}) {
		$t->{'canjmp'} = 1;
		$t->{'jump'} = "Super Jump";
		$t->{'jumpifnocj'} = "Super Jump";
	}
	if ($SoD->{'JumpCJ'} and $SoD->{'JumpSJ'}) {
		$t->{'cancj'} = 1;
		$t->{'canjmp'} = 1;
		$t->{'cjmp'} = "Combat Jumping";
		$t->{'jump'} = "Super Jump";
	}

	if ($profile->General->{'Archetype'} eq "Peacebringer") {
		if ($SoD->{'FlyHover'}) {
			$t->{'canhov'} = 1;
			$t->{'canfly'} = 1;
			$t->{'hover'} = "Combat Flight";
			$t->{'fly'} = "Energy Flight";
			$t->{'flyx'} = "Energy Flight";
		 } else {
			$t->{'canfly'} = 1;
			$t->{'hover'} = "Energy Flight";
			$t->{'flyx'} = "Energy Flight";
		}
	 } elsif (not ($profile->General->{'Archetype'} eq "Warshade")) {
		if ($SoD->{'FlyHover'} and not $SoD->{'FlyFly'}) {
			$t->{'canhov'} = 1;
			$t->{'hover'} = "Hover";
			$t->{'flyx'} = "Hover";
			if ($SoD->{'TPTPHover'}) { $t->{'tphover'} = '$$powexectoggleon Hover' }
		}
		if (not $SoD->{'FlyHover'} and $SoD->{'FlyFly'}) {
			$t->{'canfly'} = 1;
			$t->{'hover'} = "Fly";
			$t->{'flyx'} = "Fly";
		}
		if ($SoD->{'FlyHover'} and $SoD->{'FlyFly'}) {
			$t->{'canhov'} = 1;
			$t->{'canfly'} = 1;
			$t->{'hover'} = "Hover";
			$t->{'fly'} = "Fly";
			$t->{'flyx'} = "Fly";
			if ($SoD->{'TPTPHover'}) { $t->{'tphover'} = '$$powexectoggleon Hover' }
		}
	}
	if (($profile->General->{'Archetype'} eq "Peacebringer") and $SoD->{'FlyQFly'}) {
		$t->{'canqfly'} = 1;
	}
	if ($SoD->{'FlyGFly'}) {
		$t->{'cangfly'} = 1;
		$t->{'gfly'} = "Group Fly";
		if ($SoD->{'TTPTPGFly'}) { $t->{'ttpgfly'} = '$$powexectoggleon Group Fly' }
	}
	if ($SoD->{'RunPrimaryNumber'} == 1) {
		$t->{'sprint'} = $SoD->{'RunSecondary'};
		$t->{'speed'}  = $SoD->{'RunSecondary'};
	} else {
		$t->{'sprint'} = $SoD->{'RunSecondary'};
		$t->{'speed'}  = $SoD->{'RunPrimary'};
		$t->{'canss'} = 1;
	}
	$t->{'unqueue'} = $SoD->{'Unqueue'} ? '$$powexecunqueue' : '';
	if ($SoD->{'AutoMouseLook'}) {
		$t->{'mlon'}  = '$$mouselook 1';
		$t->{'mloff'} = '$$mouselook 0';
	}
	if ($SoD->{'RunUseCamdist'}) {
		$t->{'runcamdist'} = '$$camdist ' . $SoD->{'RunCamdist'};
	}
	if ($SoD->{'FlyUseCamdist'}) {
		$t->{'flycamdist'} = '$$camdist ' . $SoD->{'FlyCamdist'};
	}
	if ($SoD->{'Detail'} and $SoD->{'DetailEnable'}) {
		$t->{'detailhi'} = '$$visscale ' . $SoD->{'DetailNormalAmt'} . '$$shadowvol 0$$ss 0';
		$t->{'detaillo'} = '$$visscale ' . $SoD->{'DetailMovingAmt'} . '$$shadowvol 0$$ss 0';
	}

	my $windowhide = $SoD->{'TPHideWindows'} ? '$$windowhide health$$windowhide chat$$windowhide target$$windowhide tray' : '';
	my $windowshow = $SoD->{'TPHideWindows'} ? '$$show health$$show chat$$show target$$show tray' : '';

	# my $turn = "+zoomin$$-zoomin"  # a non functioning bind used only to activate the keydown/keyup functions of +commands;
	$t->{'turn'} = "+down";  # a non functioning bind used only to activate the keydown/keyup functions of +commands;
	
	#  temporarily set $SoD->{'Default'} to "NonSoD"
	# $SoD->{'Default'} = "Base"
	#  set up the keys to be used.
	if ($SoD->{'Default'} eq "NonSoD") { $t->{'NonSoDMode'} = $SoD->{'NonSoDMode'} }
	if ($SoD->{'Default'} eq "Base") { $t->{'BaseMode'} = $SoD->{'BaseMode'} }
	if ($SoD->{'Default'} eq "Fly") { $t->{'FlyMode'} = $SoD->{'FlyMode'} }
	if ($SoD->{'Default'} eq "Jump") { $t->{'JumpMode'} = $SoD->{'JumpMode'} }
	if ($SoD->{'Default'} eq "Run") { $t->{'RunMode'} = $SoD->{'RunMode'} }
# 	if ($SoD->{'Default'} eq "GFly") { $t->{'GFlyMode'} = $SoD->{'GFlyMode'} }
	$t->{'TempMode'} = $SoD->{'TempMode'};
	$t->{'QFlyMode'} = $SoD->{'QFlyMode'};

	for my $space (0..1) {
		$t->{'space'} = $space;
		$t->{'up'} = '$$up ' . $space;
		$t->{'upx'} = '$$up ' . (1-$space);

		for my $X (0..1) {
			$t->{'X'} = $X;
			$t->{'dow'} = '$$down ' . $X;
			$t->{'dowx'} = '$$down ' . (1-$X);

			for my $W (0..1) {
				$t->{'W'} = $W;
				$t->{'forw'} = '$$forward ' . $W;
				$t->{'forx'} = '$$forward ' . (1-$W);

				for my $S (0..1) {
					$t->{'S'} = $S;
					$t->{'bac'} = '$$backward ' . $S;
					$t->{'bacx'} = '$$backward ' . (1-$S);

					for my $A (0..1) {
						$t->{'A'} = $A;
						$t->{'lef'} = '$$left ' . $A;
						$t->{'lefx'} = '$$left ' . (1-$A);

						for my $D (0..1) {
							$t->{'D'} = $D;
							$t->{'rig'} = '$$right ' . $D;
							$t->{'rigx'} = '$$right ' . (1-$D);

							$t->{'totalkeys'} = $space+$X+$W+$S+$A+$D;	# total number of keys down
							$t->{'horizkeys'} = $W+$S+$A+$D;	# total # of horizontal move keys.	So Sprint isn't turned on when jumping
							$t->{'vertkeys'} = $space+$X;
							$t->{'jkeys'} = $t->{'horizkeys'}+$t->{'space'};

							if ($SoD->{'NonSoD'} or $t->{'canqfly'}) {
								$t->{$SoD->{'Default'} . "Mode"} = $t->{'NonSoDMode'};
								makeSoDFile({
									t => $t,
									bl => 'n',
									bla => 'an',
									blf => 'fn',
									path => 'n',
									pathr => 'an',
									pathf => 'fn',
									mobile => '',
									stationary => '',
									modestr => "NonSoD",
								});
								undef $t->{$SoD->{'Default'} . "Mode"};
							}
							if ($SoD->{'Base'}) {
								$t->{$SoD->{'Default'} . "Mode"} = $t->{'BaseMode'};
								makeSoDFile({
									t => $t,
									bl => 'r',
									bla => 'gr',
									blf => 'fr',
									path => 'r',
									pathr => 'ar',
									pathf => 'fr',
									mobile => $t->{'sprint'},
									stationary => '',
									modestr => "Base",
								});
								undef $t->{$SoD->{'Default'} . "Mode"};
							}
							if ($t->{'canss'}) {
								$t->{$SoD->{'Default'} . "Mode"} = $t->{'RunMode'};
								my $sssj;
								if ($SoD->{'SSSSSJModeEnable'}) { $sssj = $t->{'jump'} }
								if ($SoD->{'SSMobileOnly'}) {
									makeSoDFile({
										t => $t,
										bl => 's',
										bla => 'as',
										blf => 'fs',
										path => 's',
										pathr => 'as',
										pathf => 'fs',
										mobile => $t->{'speed'},
										stationary => '',
										modestr => "Run",
										sssj => $sssj,
									});
								 } else {
									makeSoDFile({
										t => $t,
										bl => 's',
										bla => 'as',
										blf => 'fs',
										path => 's',
										pathr => 'as',
										pathf => 'fs',
										mobile => $t->{'speed'},
										stationary => $t->{'speed'},
										modestr => "Run",
										sssj => $sssj,
									});
								}
								undef $t->{$SoD->{'Default'} . "Mode"};
							}
							if ($t->{'canjmp'}>0 and not ($SoD->{'JumpSimple'})) {
								$t->{$SoD->{'Default'} . "Mode"} = $t->{'JumpMode'};
								my $jturnoff;
								if ($t->{'jump'} eq $t->{'cjmp'}) { $jturnoff = $t->{'jumpifnocj'} }
								makeSoDFile({
									t => $t,
									bl => 'j',
									bla => 'aj',
									blf => 'fj',
									path => 'j',
									pathr => 'aj',
									pathf => 'fj',
									mobile => $t->{'jump'},
									stationary => $t->{'cjmp'},
									modestr => "Jump",
									flight => "Jump",
									fix => \&sodJumpFix,
									turnoff => $jturnoff,
								});
								undef $t->{$SoD->{'Default'} . "Mode"};
							}
							if ($t->{'canhov'}+$t->{'canfly'}>0) {
								$t->{$SoD->{'Default'} . "Mode"} = $t->{'FlyMode'};
								makeSoDFile({
									t => $t,
									bl => 'r',
									bla => 'af',
									blf => 'ff',
									path => 'r',
									pathr => 'af',
									pathf => 'ff',
									mobile => $t->{'flyx'},
									stationary => $t->{'hover'},
									modestr => "Fly",
									flight => "Fly",
									pathbo => 'bo',
									pathsd => 'sd',
									blbo => 'bo',
									blsd => 'sd',
								});
								undef $t->{$SoD->{'Default'} . "Mode"};
							}
							if ($t->{'canqfly'}>0) {
								$t->{$SoD->{'Default'} . "Mode"} = $t->{'QFlyMode'};
								makeSoDFile({
									t => $t,
									bl => 'q',
									bla => 'aq',
									blf => 'fq',
									path => 'q',
									pathr => 'aq',
									pathf => 'fq',
									mobile => "Quantum Flight",
									stationary => "Quantum Flight",
									modestr => "QFly",
									flight => "Fly",
								});
								undef $t->{$SoD->{'Default'} . "Mode"};
							}
							if ($t->{'cangfly'}) {
								$t->{$SoD->{'Default'} . "Mode"} = $t->{'GFlyMode'};
								makeSoDFile({
									t => $t,
									bl => 'a',
									bla => 'af',
									blf => 'ff',
									path => 'ga',
									pathr => 'gaf',
									pathf => 'gff',
									mobile => $t->{'gfly'},
									stationary => $t->{'gfly'},
									modestr => "GFly",
									flight => "GFly",
									pathbo => 'gbo',
									pathsd => 'gsd',
									blbo => 'gbo',
									blsd => 'gsd',
								});
								undef $t->{$SoD->{'Default'} . "Mode"};
							}
							if ($SoD->{'Temp'} and $SoD->{'TempEnable'}) {
								my $trayslot = "1 " . $SoD->{'TempTray'};
								$t->{$SoD->{'Default'} . "Mode"} = $t->{'TempMode'};
								makeSoDFile({
									t => $t,
									bl => 't',
									bla => 'at',
									blf => 'ft',
									path => 't',
									pathr => 'at',
									pathf => 'ft',
									mobile => $trayslot,
									stationary => $trayslot,
									modestr => "Temp",
									flight => "Fly",
								});
								undef $t->{$SoD->{'Default'} . "Mode"};
							}
						}
					}
				}
			}
		}
	}
	$t->{'space'} = $t->{'X'} = $t->{'W'} = $t->{'S'} = $t->{'A'} = $t->{'D'} = 0;

	$t->{'up'}   = '$$up '       .    $t->{'space'};
	$t->{'upx'}  = '$$up '       . (1-$t->{'space'});
	$t->{'dow'}  = '$$down '     .    $t->{'X'};
	$t->{'dowx'} = '$$down '     . (1-$t->{'X'});
	$t->{'forw'} = '$$forward '  .    $t->{'W'};
	$t->{'forx'} = '$$forward '  . (1-$t->{'W'});
	$t->{'bac'}  = '$$backward ' .    $t->{'S'};
	$t->{'bacx'} = '$$backward ' . (1-$t->{'S'});
	$t->{'lef'}  = '$$left '     .    $t->{'A'};
	$t->{'lefx'} = '$$left '     . (1-$t->{'A'});
	$t->{'rig'}  = '$$right '    .    $t->{'D'};
	$t->{'rigx'} = '$$right '    . (1-$t->{'D'});
	
	if ($SoD->{'TLeft'}  and uc $SoD->{'TLeft'}  eq "UNBOUND") { $ResetFile->SetBind($SoD->{'TLeft'}, "+turnleft") }
	if ($SoD->{'TRight'} and uc $SoD->{'TRight'} eq "UNBOUND") { $ResetFile->SetBind($SoD->{'TRight'},"+turnright") }
	
	if ($SoD->{'Temp'} and $SoD->{'TempEnable'}) {
		my $temptogglefile1 = $profile->GetBindFile("temptoggle1.txt");
		my $temptogglefile2 = $profile->GetBindFile("temptoggle2.txt");
		$temptogglefile2->SetBind($SoD->{'TempTraySwitch'},'-down$$gototray 1'                     . BindFile::BLF($profile, 'temptoggle1.txt'));
		$temptogglefile1->SetBind($SoD->{'TempTraySwitch'},'+down$$gototray ' . $SoD->{'TempTray'} . BindFile::BLF($profile, 'temptoggle2.txt'));
		$ResetFile->      SetBind($SoD->{'TempTraySwitch'},'+down$$gototray ' . $SoD->{'TempTray'} . BindFile::BLF($profile, 'temptoggle2.txt'));
	}

	my ($dwarfTPPower, $normalTPPower, $teamTPPower);
	if ($profile->General->{'Archetype'} eq "Warshade") {
		$dwarfTPPower  = "powexecname Black Dwarf Step";
		$normalTPPower = "powexecname Shadow Step";
	 } elsif ($profile->General->{'Archetype'} eq "Peacebringer") {
		$dwarfTPPower = "powexecname White Dwarf Step";
	 } else {
		$normalTPPower = "powexecname Teleport";
		$teamTPPower   = "powexecname Team Teleport";
	}

	my ($dwarfpbind, $novapbind, $humanpbind, $humanBindKey);
	if ($SoD->{'Human'} and $SoD->{'HumanEnable'}) {
		$humanBindKey = $SoD->{'HumanMode'};
		$humanpbind = cbPBindToString($SoD->{'HumanHumanPBind'},$profile);
		$novapbind  = cbPBindToString($SoD->{'HumanNovaPBind'}, $profile);
		$dwarfpbind = cbPBindToString($SoD->{'HumanDwarfPBind'},$profile);
	}
	if (($profile->General->{'Archetype'} eq "Peacebringer") or ($profile->General->{'Archetype'} eq "Warshade")) {
		if ($humanBindKey) {
			$ResetFile->SetBind($humanBindKey,$humanpbind);
		}
	}

	#  kheldian form support
	#  create the Nova and Dwarf form support files if enabled.
	my $Nova =  $SoD->{'Nova'};
	my $Dwarf = $SoD->{'Dwarf'};

	my $fullstop = q|$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0|;

	if ($Nova and $Nova->{'Enable'}) {
		$ResetFile->SetBind($Nova->{'Mode'},"t \$name, Changing to Nova->{'Nova'} Form$fullstop$t->{'on'}$Nova->{'Nova'}\$\$gototray $Nova->{'Tray'}" . BindFile::BLF($profile, 'nova.txt'));

		my $novafile = $profile->GetBindFile("nova.txt");

		if ($Dwarf and $Dwarf->{'Enable'}) {
			$novafile->SetBind($Dwarf->{'Mode'},"t \$name, Changing to $Dwarf->{'Dwarf'} Form$fullstop$t->{'off'}$Nova->{'Nova'}$t->{'on'}$Dwarf->{'Dwarf'}\$\$gototray $Dwarf->{'Tray'}" . BindFile::BLF($profile, 'dwarf.txt'));
		}
		$humanBindKey ||= $Nova->{'Mode'};

		my $humpower = $SoD->{'UseHumanFormPower'} ? '$$powexectoggleon ' . $SoD->{'HumanFormShield'} : '';

		$novafile->SetBind($humanBindKey,"t \$name, Changing to Human Form, SoD Mode$fullstop\$\$powexectoggleoff $Nova->{'Nova'} $humpower \$\$gototray 1" . BindFile::BLF($profile, 'reset.txt'));

		undef $humanBindKey if ($humanBindKey eq $Nova->{'Mode'});

		$novafile->SetBind($Nova->{'Mode'},$novapbind) if $novapbind;

		makeQFlyModeKey($profile,$t,"r",$novafile,$Nova->{'Nova'},"Nova") if ($t->{'canqfly'});

		$novafile->SetBind($SoD->{'Forward'},"+forward");
		$novafile->SetBind($SoD->{'Left'},"+left");
		$novafile->SetBind($SoD->{'Right'},"+right");
		$novafile->SetBind($SoD->{'Back'},"+backward");
		$novafile->SetBind($SoD->{'Up'},"+up");
		$novafile->SetBind($SoD->{'Down'},"+down");
		$novafile->SetBind($SoD->{'AutoRun'},"++forward");
		$novafile->SetBind($SoD->{'FlyMode'},'nop');
		$novafile->SetBind($SoD->{'RunMode'},'nop')          if ($SoD->{'FlyMode'} ne $SoD->{'RunMode'});
		$novafile->SetBind('mousechord "' . "+down$$+forward")    if ($SoD->{'MouseChord'});

		if ($SoD->{'TP'} and $SoD->{'TPEnable'}) {
			$novafile->SetBind($SoD->{'TPComboKey'},'nop');
			$novafile->SetBind($SoD->{'TPBindKey'},'nop');
			$novafile->SetBind($SoD->{'TPResetKey'},'nop');
		}
		$novafile->SetBind($SoD->{'Follow'},"follow");
		# $novafile->SetBind($SoD->{'ToggleKey'},'t $name, Changing to Human Form, Normal Mode$$up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0$$powexectoggleoff ' . $Nova->{'Nova'} . '$$gototray 1' . BindFile::BLF($profile, 'reset.txt'));
	}

	if ($Dwarf and $Dwarf->{'Enable'}) {
		$ResetFile->SetBind($Dwarf->{'Mode'},"t \$name, Changing to $Dwarf->{'Dwarf'} Form$fullstop\$\$powexectoggleon $Dwarf->{'Dwarf'}\$\$gototray $Dwarf->{'Tray'}" . BindFile::BLF($profile, 'dwarf.txt'));
		my $dwrffile = $profile->GetBindFile("dwarf.txt");
		if ($Nova and $Nova->{'Enable'}) {
			$dwrffile->SetBind($Nova->{'Mode'},"t \$name, Changing to $Nova->{'Nova'} Form$fullstop\$\$powexectoggleoff $Dwarf->{'Dwarf'}\$\$powexectoggleon $Nova->{'Nova'}\$\$gototray $Nova->{'Tray'}" . BindFile::BLF($profile, 'nova.txt'));
		}

		$humanBindKey ||= $Dwarf->{'Mode'};
		my $humpower = $SoD->{'UseHumanFormPower'} ? '$$powexectoggleon ' . $SoD->{'HumanFormShield'} : '';

		$dwrffile->SetBind($humanBindKey,"t \$name, Changing to Human Form, SoD Mode$fullstop\$\$powexectoggleoff $Dwarf->{'Dwarf'}$humpower\$\$gototray 1" . BindFile::BLF($profile, 'reset.txt'));

		$dwrffile->SetBind($Dwarf->{'Mode'},$dwarfpbind) if ($dwarfpbind);
		makeQFlyModeKey($profile,$t,"r",$dwrffile,$Dwarf->{'Dwarf'},"Dwarf") if ($t->{'canqfly'});

		$dwrffile->SetBind($SoD->{'Forward'},"+forward");
		$dwrffile->SetBind($SoD->{'Left'},"+left");
		$dwrffile->SetBind($SoD->{'Right'},"+right");
		$dwrffile->SetBind($SoD->{'Back'},"+backward");
		$dwrffile->SetBind($SoD->{'Up'},"+up");
		$dwrffile->SetBind($SoD->{'Down'},"+down");
		$dwrffile->SetBind($SoD->{'AutoRun'},"++forward");
		$dwrffile->SetBind($SoD->{'FlyMode'},'nop');
		$dwrffile->SetBind($SoD->{'Follow'},"follow");
		$dwrffile->SetBind($SoD->{'RunMode'},'nop')          if ($SoD->{'FlyMode'} ne $SoD->{'RunMode'});
		$dwrffile->SetBind('mousechord "' . "+down$$+forward")    if ($SoD->{'MouseChord'});

		if ($SoD->{'TP'} and $SoD->{'TPEnable'}) {
			$dwrffile->SetBind($SoD->{'TPComboKey'},'+down$$' . $dwarfTPPower . $t->{'detaillo'} . $t->{'flycamdist'} . $windowhide . BindFile::BLF($profile, 'dtp','tp_on1.txt'));
			$dwrffile->SetBind($SoD->{'TPBindKey'},'nop');
			$dwrffile->SetBind($SoD->{'TPResetKey'},substr($t->{'detailhi'},2) . $t->{'runcamdist'} . $windowshow . BindFile::BLF($profile, 'dtp','tp_off.txt'));
			#  Create tp_off file
			my $tp_off = $profile->GetBindFile("dtp","tp_off.txt");
			$tp_off->SetBind($SoD->{'TPComboKey'},'+down$$' . $dwarfTPPower . $t->{'detaillo'} . $t->{'flycamdist'} . $windowhide . BindFile::BLF($profile, 'dtp','tp_on1.txt'));
			$tp_off->SetBind($SoD->{'TPBindKey'},'nop');

			my $tp_on1 = $profile->GetBindFile("dtp","tp_on1.txt");
			$tp_on1->SetBind($SoD->{'TPComboKey'},'-down$$powexecunqueue' . $t->{'detailhi'} . $t->{'runcamdist'} . $windowshow . BindFile::BLF($profile, 'dtp','tp_off.txt'));
			$tp_on1->SetBind($SoD->{'TPBindKey'},'+down' . BindFile::BLF($profile, 'dtp','tp_on2.txt'));

			my $tp_on2 = $profile->GetBindFile("dtp","tp_on2.txt");
			$tp_on2->SetBind($SoD->{'TPBindKey'},'-down$$' . $dwarfTPPower . BindFile::BLF($profile, 'dtp','tp_on1.txt'));
		}
		# $dwrffile->SetBind($SoD->{'ToggleKey'},"t \$name, Changing to Human Form, Normal Mode$fullstop\$\$powexectoggleoff $Dwarf->{'Dwarf'}\$\$gototray 1" . BindFile::BLF($profile, 'reset.txt'));
	}

	if ($SoD->{'JumpSimple'}) {
		if ($SoD->{'JumpCJ'} and $SoD->{'JumpSJ'}) {
			$ResetFile->SetBind($SoD->{'JumpMode'},'powexecname Super Jump$$powexecname Combat Jumping');
		 } elsif ($SoD->{'JumpSJ'}) {
			$ResetFile->SetBind($SoD->{'JumpMode'},'powexecname Super Jump');
		 } elsif ($SoD->{'JumpCJ'}) {
			$ResetFile->SetBind($SoD->{'JumpMode'},'powexecname Combat Jumping');
		}
	}

	if ($SoD->{'TP'} and $SoD->{'TPEnable'} and not $normalTPPower) {
		$ResetFile->SetBind($SoD->{'TPComboKey'},'nop');
		$ResetFile->SetBind($SoD->{'TPBindKey'},'nop');
		$ResetFile->SetBind($SoD->{'TPResetKey'},'nop');
	}
	if ($SoD->{'TP'} and $SoD->{'TPEnable'} and not ($profile->General->{'Archetype'} eq "Peacebringer") and $normalTPPower) {
		my $tphovermodeswitch = '';
		if ($t->{'tphover'} eq '') {
			# TODO hmm can't get this from ->KeyState directly?
			#$tphovermodeswitch = $t->bl('r') . "000000.txt";
			($tphovermodeswitch = $t->bl('r')) =~ s/\d\d\d\d\d\d/000000/;
		}
		$ResetFile->SetBind($SoD->{'TPComboKey'},'+down$$' . $normalTPPower . $t->{'detaillo'} . $t->{'flycamdist'} . $windowhide . BindFile::BLF($profile, 'tp','tp_on1.txt'));
		$ResetFile->SetBind($SoD->{'TPBindKey'},'nop');
		$ResetFile->SetBind($SoD->{'TPResetKey'},substr($t->{'detailhi'},2) . $t->{'runcamdist'} . $windowshow . BindFile::BLF($profile, 'tp','tp_off.txt') . $tphovermodeswitch);
		#  Create tp_off file
		my $tp_off = $profile->GetBindFile("tp","tp_off.txt");
		$tp_off->SetBind($SoD->{'TPComboKey'},'+down$$' . $normalTPPower . $t->{'detaillo'} . $t->{'flycamdist'} . $windowhide . BindFile::BLF($profile, 'tp','tp_on1.txt'));
		$tp_off->SetBind($SoD->{'TPBindKey'},'nop');

		my $tp_on1 = $profile->GetBindFile("tp","tp_on1.txt");
		my $zoomin = $t->{'detailhi'} . $t->{'runcamdist'};
		if ($t->{'tphover'}) { $zoomin = '' }
		$tp_on1->SetBind($SoD->{'TPComboKey'},'-down$$powexecunqueue' . $zoomin . $windowshow . BindFile::BLF($profile, 'tp','tp_off.txt') . $tphovermodeswitch);
		$tp_on1->SetBind($SoD->{'TPBindKey'},'+down' . $t->{'tphover'} . BindFile::BLF($profile, 'tp','tp_on2.txt'));

		my $tp_on2 = $profile->GetBindFile("tp","tp_on2.txt");
		$tp_on2->SetBind($SoD->{'TPBindKey'},'-down$$' . $normalTPPower . BindFile::BLF($profile, 'tp','tp_on1.txt'));
	}
	if ($SoD->{'TTP'} and $SoD->{'TTPEnable'} and not ($profile->General->{'Archetype'} eq "Peacebringer") and $teamTPPower) {
		my $tphovermodeswitch = '';
		$ResetFile->SetBind($SoD->{'TTPComboKey'},'+down$$' . $teamTPPower . $t->{'detaillo'} . $t->{'flycamdist'} . $windowhide . BindFile::BLF($profile, 'ttp','ttp_on1.txt'));
		$ResetFile->SetBind($SoD->{'TTPBindKey'},'nop');
		$ResetFile->SetBind($SoD->{'TTPResetKey'},substr($t->{'detailhi'},2) . $t->{'runcamdist'} . $windowshow . BindFile::BLF($profile, 'ttp','ttp_off') . $tphovermodeswitch);
		#  Create tp_off file
		my $ttp_off = $profile->GetBindFile("ttp","ttp_off.txt");
		$ttp_off->SetBind($SoD->{'TTPComboKey'},'+down$$' . $teamTPPower . $t->{'detaillo'} . $t->{'flycamdist'} . $windowhide . BindFile::BLF($profile, 'ttp','ttp_on1.txt'));
		$ttp_off->SetBind($SoD->{'TTPBindKey'},'nop');

		my $ttp_on1 = $profile->GetBindFile("ttp","ttp_on1.txt");
		$ttp_on1->SetBind($SoD->{'TTPComboKey'},'-down$$powexecunqueue' . $t->{'detailhi'} . $t->{'runcamdist'} . $windowshow . BindFile::BLF($profile, 'ttp','ttp_off') . $tphovermodeswitch);
		$ttp_on1->SetBind($SoD->{'TTPBindKey'},'+down' . BindFile::BLF($profile, 'ttp','ttp_on2.txt'));

		my $ttp_on2 = $profile->GetBindFile("ttp","ttp_on2.txt");
		$ttp_on2->SetBind($SoD->{'TTPBindKey'},'-down$$' . $teamTPPower . BindFile::BLF($profile, 'ttp','ttp_on1.txt'));
	}
}


sub sodResetKey {
	my ($curfile,$p,$path,$turnoff,$moddir) = @_;

	$path =~ s/\d\d\d\d\d\d/000000/;  # ick ick ick

	my ($u, $d) = (0, 0);
	if ($moddir eq 'up')   { $u = 1; }
	if ($moddir eq 'down') { $d = 1; }
	$curfile->SetBind($p->General->{'Reset Key'},
			'up ' . $u . '$$down ' . $d . '$$forward 0$$backward 0$$left 0$$right 0' .
			$turnoff . '$$t $name, SoD Binds Reset' . BindFile::BaseReset($p) . BindFile::BLF($p, $path)
	);
}

sub sodDefaultResetKey {
	my ($mobile,$stationary) = @_;
	# TODO -- decide where to keep 'resetstring' and make this sub update it.
	#cbAddReset('up 0$$down 0$$forward 0$$backward 0$$left 0$$right 0'.actPower_name(undef,1,$stationary,$mobile) . '$$t $name, SoD Binds Reset')
}


# TODO TODO TODO -- the s/\d\d\d\d\d\d/$newbits/ scheme in the following six subs is a vile evil (live veil ilve vlie) hack.
sub sodUpKey {
	my ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,$autorun,$followbl,$bo,$sssj) = @_;

	my ($upx, $dow, $forw, $bac, $lef, $rig) = ($t->{'upx'}, $t->D, $t->F, $t->B, $t->L, $t->R);

	my ($ml, $toggle, $toggleon, $toggleoff, $toggleoff2) = ('','','','','');

	my $actkeys = $t->{'totalkeys'};

	if (not $flight and not $sssj) { undef $mobile; undef $stationary; }

	if ($bo eq "bo") { $upx = '$$up 1'; $dow = '$$down 0'; }
	if ($bo eq "sd") { $upx = '$$up 0'; $dow = '$$down 1'; }
	
	undef $mobile     if $mobile     and $mobile     eq "Group Fly";
	undef $stationary if $stationary and $stationary eq "Group Fly";

	if ($flight eq "Jump") {
		$dow = '$$down 0';
		$actkeys = $t->{'jkeys'};
		if ($t->{'totalkeys'} == 1 and $t->{'space'} == 1) { $upx = '$$up 0' } else { $upx = '$$up 1' }
		if ($t->{'X'} == 1)                                { $upx = '$$up 0' }
	}

	$toggleon = $mobile;
	if ($actkeys == 0) {
		$ml = $t->{'mlon'};
		$toggleon = $mobile;
		if (not ($mobile and ($mobile eq $stationary))) { $toggleoff = $stationary; }
	} else {
		undef $toggleon;
	}

	if ($t->{'totalkeys'} == 1 and $t->{'space'} == 1) {
		$ml = $t->{'mloff'};
		if (not ($stationary and ($mobile eq $stationary))) { $toggleoff = $mobile; }
		$toggleon = $stationary;
	} else {
		undef $toggleoff;
	}
	
	if ($sssj) {
		if ($t->{'space'} == 0) { #  if we are hitting the space bar rather than releasing its..
			$toggleon = $sssj;
			$toggleoff = $mobile;
			if ($stationary and $stationary eq $mobile) { $toggleoff2 = $stationary; }
		} elsif ($t->{'space'} == 1) { #  if we are releasing the space bar ..
			$toggleoff = $sssj;
			if ($t->{'horizkeys'} > 0 or $autorun) { #  and we are moving laterally, or in autorun..
				$toggleon = $mobile;
			} else { #  otherwise turn on the stationary power..
				$toggleon = $stationary;
			}
		}
	}
	
	if ($toggleon or $toggleoff) {
		$toggle = actPower_name(undef,1,$toggleon,$toggleoff,$toggleoff2);
	}

	my $newbits = $t->KeyState({toggle => 'space'});
	$bl =~ s/\d\d\d\d\d\d/$newbits/;

	my $ini = ($t->{'space'} == 1) ? '-down' : '+down';

	if ($followbl) {
		my $move = '';
		if ($t->{'space'} != 1) {
			($bl = $followbl) =~ s/\d\d\d\d\d\d/$newbits/;
			$move = $upx . $dow . $forw . $bac . $lef . $rig;
		}
		$curfile->SetBind($SoD->{'Up'},$ini . $move . $bl);
	} elsif (not $autorun) {
		$curfile->SetBind($SoD->{'Up'},$ini . $upx . $dow . $forw . $bac . $lef . $rig . $ml . $toggle . $bl);
	} else {
		if (not $sssj) { $toggle = '' } #  returns the following line to the way it was before $sssj
		$curfile->SetBind($SoD->{'Up'},$ini . $upx . $dow . '$$backward 0' . $lef . $rig . $toggle . $t->{'mlon'} . $bl);
	}
}

sub sodDownKey {
	my ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,$autorun,$followbl,$bo,$sssj) = @_;
	my ($up, $dowx, $forw, $bac, $lef, $rig) = ($t->U, $t->{'dowx'}, $t->F, $t->B, $t->L, $t->R);

	my ($ml, $toggle, $toggleon, $toggleoff) = ('','','','');
	my $actkeys = $t->{'totalkeys'};

	if (not $flight) { undef $mobile; undef $stationary; }
	if ($bo eq 'bo') { $up = '$$up 1'; $dowx = '$$down 0'; }
	if ($bo eq 'sd') { $up = '$$up 0'; $dowx = '$$down 1'; }

	if ($mobile     and $mobile     eq 'Group Fly') { undef $mobile; }
	if ($stationary and $stationary eq 'Group Fly') { undef $stationary; }

	if ($flight eq 'Jump') {
		$dowx = '$$down 0';
		# if ($t->{'cancj'}  == 1) { $aj = $t->{'cjmp'}; }
		# if ($t->{'canjmp'} == 1) { $aj = $t->{'jump'}; }
		$actkeys = $t->{'jkeys'};
		if ($t->{'X'} == 1 and $t->{'totalkeys'} > 1) { $up = '$$up 1' } else { $up = '$$up 0'; }
	}

	$toggleon = $mobile;
	if ($actkeys == 0) {
		$ml = $t->{'mlon'};
		$toggleon = $mobile;
		if (not ($mobile and $mobile eq $stationary)) { $toggleoff = $stationary; }
	} else {
		undef $toggleon;
	}

	if ($t->{'totalkeys'} == 1 and $t->{'X'} == 1) {
		$ml = $t->{'mloff'};
		if (not ($stationary and $mobile eq $stationary)) { $toggleoff = $mobile; }
		$toggleon = $stationary;
	} else {
		undef $toggleoff;
	}
	
	if ($toggleon or $toggleoff) {
		$toggle = actPower_name(undef,1,$toggleon,$toggleoff)
	}

	my $newbits = $t->KeyState({toggle => 'X'});
	$bl =~ s/\d\d\d\d\d\d/$newbits/;

	my $ini = ($t->{'X'} == 1) ? '-down' : '+down';

	if ($followbl) {
		my $move = '';
		if ($t->{'X'} != 1) {
			($bl = $followbl) =~ s/\d\d\d\d\d\d/$newbits/;
			$move = $up . $dowx . $forw . $bac . $lef . $rig;
		}
		$curfile->SetBind($SoD->{'Down'},$ini . $move . $bl);
	} elsif (not $autorun) {
		$curfile->SetBind($SoD->{'Down'},$ini . $up . $dowx . $forw . $bac . $lef . $rig . $ml . $toggle . $bl);
	} else {
		$curfile->SetBind($SoD->{'Down'},$ini . $up . $dowx . '$$backward 0' . $lef . $rig . $t->{'mlon'} . $bl);
	}
}
###### HERE!


sub sodForwardKey {
	my ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,$autorunbl,$followbl,$bo,$sssj) = @_;
	my ($up, $dow, $forx, $bac, $lef, $rig) = ($t->U, $t->D, $t->{'forx'}, $t->B, $t->L, $t->R);
	my ($ml, $toggle, $toggleon, $toggleoff) = ('','','','');
	my $actkeys = $t->{'totalkeys'};
	if ($bo eq "bo") { $up = '$$up 1'; $dow = '$$down 0' }
	if ($bo eq "sd") { $up = '$$up 0'; $dow = '$$down 1' }

	if ($mobile     eq 'Group Fly') { undef $mobile; }
	if ($stationary eq 'Group Fly') { undef $stationary; }

	if ($flight eq "Jump") { 
		$dow = '$$down 0';
		$actkeys = $t->{'jkeys'};
		if (
			($t->{'totalkeys'} == 1 and $t->{'W'} == 1)
				or
			($t->{'X'} == 1)
			)
		 { $up = '$$up 0'; } else { $up = '$$up 1'; }
	}

	$toggleon = $mobile;
	if ($t->{'totalkeys'} == 0) { 
		$ml = $t->{'mlon'};
		if (not ($mobile and $mobile eq $stationary)) { 
			$toggleoff = $stationary;
		}
	}
		
	if ($t->{'totalkeys'} == 1 and $t->{'W'} == 1) { 
		$ml = $t->{'mloff'};
	}

	my $testKeys = $flight ? $t->{'totalkeys'} : $t->{'horizkeys'};
	if ($testKeys == 1 and $t->{'W'} == 1) { 
		if (not ($stationary and $mobile eq $stationary)) {
			$toggleoff = $mobile;
		}
		$toggleon = $stationary;
	}

	if ($sssj and $t->{'space'} == 1) { #  if (we are jumping with SS+SJ mode enabled
		$toggleon = $sssj;
		$toggleoff = $mobile;
	}
	
	if ($toggleon or $toggleoff) { 
		$toggle = actPower_name(undef,1,$toggleon,$toggleoff);
	}

	my $newbits = $t->KeyState({toggle => 'W'});
	$bl =~ s/\d\d\d\d\d\d/$newbits/;

	my $ini = ($t->{'W'} == 1) ? '-down' : '+down';

	if ($followbl) { 
		my $move;
		if ($t->{'W'} == 1) { 
			$move = $ini;
		} else {
			($bl = $followbl) =~ s/\d\d\d\d\d\d/$newbits/;
			$move = $ini . $up . $dow . $forx . $bac . $lef . $rig;
		}
		$curfile->SetBind($SoD->{'Forward'},$move . $bl);
		if ($SoD->{'MouseChord'}) { 
			if ($t->{'W'} == 1) { $move = $ini . $up . $dow . $forx . $bac . $rig . $lef }
			$curfile->SetBind('mousechord',$move . $bl);
		}
	} elsif (not $autorunbl) { 
		$curfile->SetBind($SoD->{'Forward'},$ini . $up . $dow . $forx . $bac . $lef . $rig . $ml . $toggle . $bl);
		if ($SoD->{'MouseChord'}) { 
			$curfile->SetBind('mousechord',$ini . $up . $dow . $forx . $bac . $rig . $lef . $ml . $toggle . $bl);
		}
	} else {
		if ($t->{'W'} == 1) { 
			($bl = $autorunbl) =~ s/\d\d\d\d\d\d/$newbits/;
		}
		$curfile->SetBind($SoD->{'Forward'},$ini . $up . $dow . '$$forward 1$$backward 0' . $lef . $rig . $t->{'mlon'} . $bl);
		if ($SoD->{'MouseChord'}) { 
			$curfile->SetBind('mousechord',$ini . $up . $dow . '$$forward 1$$backward 0' . $rig . $lef . $t->{'mlon'} . $bl);
		}
	}
}

sub sodBackKey {
	my ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,$autorunbl,$followbl,$bo,$sssj) = @_;
	my ($up, $dow, $forw, $bacx, $lef, $rig) = ($t->U, $t->D, $t->F, $t->{'bacx'}, $t->L, $t->R);

	my ($ml, $toggle, $toggleon, $toggleoff) = ('','','','');

	my $actkeys = $t->{'totalkeys'};
	if ($bo eq "bo") { $up = '$$up 1'; $dow = '$$down 0' }
	if ($bo eq "sd") { $up = '$$up 0'; $dow = '$$down 1' }

	if ($mobile     eq 'Group Fly') { undef $mobile; }
	if ($stationary eq 'Group Fly') { undef $stationary; }

	if ($flight eq "Jump") { 
		$dow = '$$down 0';
		$actkeys = $t->{'jkeys'};
		if ($t->{'totalkeys'} == 1 and $t->{'S'} == 1) { $up = '$$up 0' } else { $up = '$$up 1' }
		if ($t->{'X'} == 1) { $up = '$$up 0' }
	}

	$toggleon = $mobile;
	if ($t->{'totalkeys'} == 0) { 
		$ml = $t->{'mlon'};
		$toggleon = $mobile;
		if (not ($mobile and $mobile eq $stationary)) {
			$toggleoff = $stationary;
		}
	}
		
	if ($t->{'totalkeys'} == 1 and $t->{'S'} == 1) { 
		$ml = $t->{'mloff'};
	}

	my $testKeys = $flight ? $t->{'totalkeys'} : $t->{'horizkeys'};
	if ($testKeys == 1 and $t->{'S'} == 1) { 
		if (not ($stationary and $mobile eq $stationary)) {
			$toggleoff = $mobile;
		}
		$toggleon = $stationary;
	}

	if ($sssj and $t->{'space'} == 1) { #  if (we are jumping with SS+SJ mode enabled
		$toggleon = $sssj;
		$toggleoff = $mobile;
	}
	
	if ($toggleon or $toggleoff) { 
		$toggle = actPower_name(undef,1,$toggleon,$toggleoff);
	}

	my $newbits = $t->KeyState({toggle => 'S'});
	$bl =~ s/\d\d\d\d\d\d/$newbits/;

	my $ini = ($t->{'S'} == 1) ? "-down" : "+down";

	my $move;
	if ($followbl) { 
		if ($t->{'S'} == 1) { 
			$move = $ini;
		} else {
			($bl = $followbl) =~ s/\d\d\d\d\d\d/$newbits/;
			$move = $ini . $up . $dow . $forw . $bacx . $lef . $rig;
		}
		$curfile->SetBind($SoD->{'Back'},$move . $bl);
	} elsif (not $autorunbl) { 
		$curfile->SetBind($SoD->{'Back'},$ini . $up . $dow . $forw . $bacx . $lef . $rig . $ml . $toggle . $bl);
	} else {
		if ($t->{'S'} == 1) { 
			$move = '$$forward 1$$backward 0';
		} else {
			$move = '$$forward 0$$backward 1';
			($bl = $autorunbl) =~ s/\d\d\d\d\d\d/$newbits/;
		}
		$curfile->SetBind($SoD->{'Back'},$ini . $up . $dow . $move . $lef . $rig . $t->{'mlon'} . $bl);
	}
}

sub sodLeftKey {
	my ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,$autorun,$followbl,$bo,$sssj) = @_;
	my ($up, $dow, $forw, $bac, $lefx, $rig) = ($t->U, $t->D, $t->F, $t->B, $t->{'lefx'}, $t->R);

	my ($ml, $toggle, $toggleon, $toggleoff) = ('','','','');

	my $actkeys = $t->{'totalkeys'};
	if ($bo eq "bo") { $up = '$$up 1'; $dow = '$$down 0' }
	if ($bo eq "sd") { $up = '$$up 0'; $dow = '$$down 1' }

	if ($mobile     eq 'Group Fly') { undef $mobile; }
	if ($stationary eq 'Group Fly') { undef $stationary; }

	if ($flight eq "Jump") { 
		$dow = '$$down 0';
		$actkeys = $t->{'jkeys'};
		if ($t->{'totalkeys'} == 1 and $t->{'A'} == 1) { $up = '$$up 0' } else { $up = '$$up 1' }
		if ($t->{'X'} == 1) { $up = '$$up 0' }
	}

	$toggleon = $mobile;
	if ($t->{'totalkeys'} == 0) { 
		$ml = $t->{'mlon'};
		$toggleon = $mobile;
		if (not ($mobile and $mobile eq $stationary)) { 
			$toggleoff = $stationary;
		}
	}
		
	if ($t->{'totalkeys'} == 1 and $t->{'A'} == 1) { 
		$ml = $t->{'mloff'};
	}

	my $testKeys = $flight ? $t->{'totalkeys'} : $t->{'horizkeys'};
	if ($testKeys == 1 and $t->{'A'} == 1) { 
		if (not ($stationary and $mobile eq $stationary)) {
			$toggleoff = $mobile;
		}
		$toggleon = $stationary;
	}

	if ($sssj and $t->{'space'} == 1) { #  if (we are jumping with SS+SJ mode enabled
		$toggleon = $sssj;
		$toggleoff = $mobile;
	}
	
	if ($toggleon or $toggleoff) { 
		$toggle = actPower_name(undef,1,$toggleon,$toggleoff);
	}

	my $newbits = $t->KeyState({toggle => 'A'});
	$bl =~ s/\d\d\d\d\d\d/$newbits/;

	my $ini = ($t->{'A'} == 1) ? '-down' : '+down';

	my $move;
	if ($followbl) { 
		if ($t->{'A'} == 1) { 
			$move = $ini;
		} else {
			($bl = $followbl) =~ s/\d\d\d\d\d\d/$newbits/;
			$move = $ini . $up . $dow . $forw . $bac . $lefx . $rig;
		}
		$curfile->SetBind($SoD->{'Left'},$move . $bl);
	} elsif (not $autorun) { 
		$curfile->SetBind($SoD->{'Left'},$ini . $up . $dow . $forw . $bac . $lefx . $rig . $ml . $toggle . $bl);
	} else {
		$curfile->SetBind($SoD->{'Left'},$ini . $up . $dow . '$$backward 0' . $lefx . $rig . $t->{'mlon'} . $bl);
	}
}

sub sodRightKey {
	my ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,$autorun,$followbl,$bo,$sssj) = @_;
	my ($up, $dow, $forw, $bac, $lef, $rigx) = ($t->U, $t->D, $t->F, $t->B, $t->L, $t->{'rigx'});

	my ($ml, $toggle, $toggleon, $toggleoff) = ('','','','');

	my $actkeys = $t->{'totalkeys'};
	if ($bo eq "bo") { $up = '$$up 1'; $dow = '$$down 0' }
	if ($bo eq "sd") { $up = '$$up 0'; $dow = '$$down 1' }

	if ($mobile     eq 'Group Fly') { undef $mobile; }
	if ($stationary eq 'Group Fly') { undef $stationary; }

	if ($flight eq "Jump") { 
		$dow = '$$down 0';
		$actkeys = $t->{'jkeys'};
		if ($t->{'totalkeys'} == 1 and $t->{'D'} == 1) { $up = '$$up 0' } else { $up = '$$up 1' }
		if ($t->{'X'} == 1) { $up = '$$up 0' }
	}

	$toggleon = $mobile;
	if ($t->{'totalkeys'} == 0) { 
		$ml = $t->{'mlon'};
		$toggleon = $mobile;
		if (not ($mobile and $mobile eq $stationary)) { 
			$toggleoff = $stationary;
		}
	}
		
	if ($t->{'totalkeys'} == 1 and $t->{'D'} == 1) { 
		$ml = $t->{'mloff'};
	}

	my $testKeys = $flight ? $t->{'totalkeys'} : $t->{'horizkeys'};
	if ($testKeys == 1 and $t->{'D'} == 1) { 
		if (not ($stationary and $mobile eq $stationary)) {
			$toggleoff = $mobile;
		}
		$toggleon = $stationary;
	}

	if ($sssj and $t->{'space'} == 1) { #  if (we are jumping with SS+SJ mode enabled
		$toggleon = $sssj;
		$toggleoff = $mobile;
	}
	
	if ($toggleon or $toggleoff) { 
		$toggle = actPower_name(undef,1,$toggleon,$toggleoff);
	}

	my $newbits = $t->KeyState({toggle => 'D'});
	$bl =~ s/\d\d\d\d\d\d/$newbits/;

	my $ini = ($t->{'D'} == 1) ? '-down' : '+down';

	if ($followbl) { 
		my $move;
		if ($t->{'D'} == 1) { 
			$move = $ini;
		} else {
			($bl = $followbl) =~ s/\d\d\d\d\d\d/$newbits/;
			$move = $ini . $up . $dow . $forw . $bac . $lef . $rigx;
		}
		$curfile->SetBind($SoD->{'Right'},$move . $bl);
	} elsif (not $autorun) { 
		$curfile->SetBind($SoD->{'Right'},$ini . $up . $dow . $forw . $bac . $lef . $rigx . $ml . $toggle . $bl);
	} else {
		$curfile->SetBind($SoD->{'Right'},$ini . $up . $dow . '$$forward 1$$backward 0' . $lef . $rigx . $t->{'mlon'} . $bl);
	}
}

sub sodAutoRunKey {
	my ($t,$bl,$curfile,$SoD,$mobile,$sssj) = @_;
	if ($sssj and $t->{'space'} == 1) { 
		$curfile->SetBind($SoD->{'AutoRun'},'forward 1$$backward 0' . $t->dirs('UDLR') . $t->{'mlon'} . actPower_name(undef,1,$sssj,$mobile) . $bl);
	} else {
		$curfile->SetBind($SoD->{'AutoRun'},'forward 1$$backward 0' . $t->dirs('UDLR') . $t->{'mlon'} . actPower_name(undef,1,$mobile) . $bl);
	}
}

sub sodAutoRunOffKey {
	my ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight,$sssj) = @_;
	my ($toggle, $toggleon, $toggleoff);
	if (not $flight and not $sssj) { 
		if ($t->{'horizkeys'} > 0) { 
			$toggleon = $t->{'mlon'} . actPower_name(undef,1,$mobile);
		} else {
			$toggleon = $t->{'mloff'} . actPower_name(undef,1,$stationary,$mobile);
		}
	} elsif ($sssj) { 
		if ($t->{'horizkeys'} > 0 or $t->{'space'} == 1) { 
			$toggleon = $t->{'mlon'} . actPower_name(undef,1,$mobile,$toggleoff);
		} else {
			$toggleon = $t->{'mloff'} . actPower_name(undef,1,$stationary,$mobile,$toggleoff);
		}
	} else {
		if ($t->{'totalkeys'} > 0) { 
			$toggleon = $t->{'mlon'} . actPower_name(undef,1,$mobile);
		} else {
			$toggleon = $t->{'mloff'} . actPower_name(undef,1,$stationary,$mobile);
		}
	}
	my $bindload = $bl . $t->KeyState . '.txt';
	$curfile->SetBind($SoD->{'AutoRun'},$t->dirs('UDFBLR') . $toggleon . $bindload);
}

sub sodFollowKey {
	my ($t,$bl,$curfile,$SoD,$mobile) = @_;
	$curfile->SetBind($SoD->{'Follow'},'follow' . actPower_name(undef,1,$mobile) . $bl . $t->KeyState . '.txt');
}

sub sodFollowOffKey {
	my ($t,$bl,$curfile,$SoD,$mobile,$stationary,$flight) = @_;
	my ($toggle) = '';
	if (not $flight) { 
		if ($t->{'horizkeys'} == 0) { 
			if ($stationary eq $mobile) { 
				$toggle = actPower_name(undef,1,$stationary,$mobile);
			} else {
				$toggle = actPower_name(undef,1,$stationary);
			}
		}
	} else {
		if ($t->{'totalkeys'} == 0) { 
			if ($stationary eq $mobile) { 
				$toggle = actPower_name(undef,1,$stationary,$mobile);
			} else {
				$toggle = actPower_name(undef,1,$stationary);
			}
		}
	}
	$curfile->SetBind($SoD->{'Follow'},"follow" . $toggle . $t->U . $t->{'dow'} . $t->F . $t->B . $t->L . $t->R . $bl . $t->KeyState . '.txt');
}

sub bindisused { 
	my ($profile) = @_;
	return if not defined $profile->SoD;
	my $SoD = $profile->SoD;
	return $profile->{$SoD->{'Enable'}};
}

sub findconflicts {
	my ($profile) = @_;
	my $SoD = $profile->SoD;
	Utility::CheckConflict($SoD,"Up","Up Key");
	Utility::CheckConflict($SoD,"Down","Down Key");
	Utility::CheckConflict($SoD,"Forward","Forward Key");
	Utility::CheckConflict($SoD,"Back","Back Key");
	Utility::CheckConflict($SoD,"Left","Strafe Left Key");
	Utility::CheckConflict($SoD,"Right","Strafe Right Key");
	Utility::CheckConflict($SoD,"TLeft","Turn Left Key");
	Utility::CheckConflict($SoD,"TRight","Turn Right Key");
	Utility::CheckConflict($SoD,"AutoRun","AutoRun Key");
	Utility::CheckConflict($SoD,"Follow","Follow Key");

	if ($SoD->{'NonSoD'})          { Utility::CheckConflict($SoD,"NonSoDMode","NonSoD Key") }
	if ($SoD->{'Base'})            { Utility::CheckConflict($SoD,"BaseMode","Sprint Mode Key") }
	if ($SoD->{'SSSS'})      { Utility::CheckConflict($SoD,"RunMode","Speed Mode Key") }
	if ($SoD->{'JumpCJ'}
		or $SoD->{'JumpSJ'}) { Utility::CheckConflict($SoD,"JumpMode","Jump Mode Key") }
	if ($SoD->{'FlyHover'}
		or $SoD->{'FlyFly'}) { Utility::CheckConflict($SoD,"FlyMode","Fly Mode Key") }
	if ($SoD->{'FlyQFly'}
		and ($profile->General->{'Archetype'} eq "Peacebringer")) { Utility::CheckConflict($SoD,"QFlyMode","Q.Fly Mode Key") }
	if ($SoD->{'TP'} and $SoD->{'TPEnable'}) {
		Utility::CheckConflict($SoD->{'TP'},"ComboKey","TP ComboKey");
		Utility::CheckConflict($SoD->{'TP'},"ResetKey","TP ResetKey");

		my $TPQuestion = "Teleport Bind";
		if ($profile->General->{'Archetype'} eq "Peacebringer") {
			$TPQuestion = "Dwarf Step Bind"
		 } elsif ($profile->General->{'Archetype'} eq "Warshade") {
			$TPQuestion = "Shd/Dwf Step Bind"
		}
		Utility::CheckConflict($SoD->{'TP'},"BindKey",$TPQuestion)
	}
	if ($SoD->{'FlyGFly'}) { Utility::CheckConflict($SoD,"GFlyMode","Group Fly Key"); }
	if ($SoD->{'TTP'} and $SoD->{'TTPEnable'}) {
		Utility::CheckConflict($SoD->{'TTP'},"ComboKey","TTP ComboKey");
		Utility::CheckConflict($SoD->{'TTP'},"ResetKey","TTP ResetKey");
		Utility::CheckConflict($SoD->{'TTP'},"BindKey","Team TP Bind");
	}
	if ($SoD->{'Temp'} and $SoD->{'TempEnable'}) {
		Utility::CheckConflict($SoD,"TempMode","Temp Mode Key");
		Utility::CheckConflict($SoD->{'Temp'},"TraySwitch","Tray Toggle Key");
	}

	if (($profile->General->{'Archetype'} eq "Peacebringer") or ($profile->General->{'Archetype'} eq "Warshade")) {
		if ($SoD->{'Nova'}  and $SoD->{'NovaEnable'}) { Utility::CheckConflict($SoD->{'Nova'}, "Mode","Nova Form Bind") }
		if ($SoD->{'Dwarf'} and $SoD->{'DwarfEnable'}) { Utility::CheckConflict($SoD->{'Dwarf'},"Mode","Dwarf Form Bind") }
	}
}

#  toggleon variation
sub actPower_toggle {
	my ($start,$unq,$on,@rest) = @_;
	my ($s, $traytest) = ('','');
	if (ref $on) {
		#  deal with power slot stuff..
		$traytest = $on->{'trayslot'};
	}
	my $offpower = {};
	for my $v (@rest) {
		if (ref $v) {
			while (my ($j, $w) = each %$v) {
				if ($w and $w ne 'on' and not $offpower->{$w}) {
					if (ref $w) {
						if ($w->{'trayslot'} eq $traytest) {
							$s .= '$$powexectray ' . $w->{'trayslot'};
							$unq = 1
						}
					} else {
						$offpower->{'w'} = 1;
						$s .= '$$powexectoggleoff ' . $w
					}
				}
			}
			if ($v->{'trayslo'} and $v->{'trayslot'} eq $traytest) {
				$s = $s . '$$powexectray ' . $v->{'trayslot'};
				$unq = 1;
			}
		} else {
			if ($v and ($v ne 'on') and not $offpower->{$v}) {
				$offpower->{$v} = 1;
				$s .= '$$powexectoggleoff ' . $v;
			}
		}
	}
	if ($unq and $s) {
		$s .= '$$powexecunqueue';
	}
	# if start then s = string.sub(s,3,string.len(s)) end
	if ($on) {
		if (ref $on) {
			#  deal with power slot stuff..
			$s .= '$$powexectray '.$on->{'trayslot'} . '$$powexectray ' . $on->{'trayslot'};
		} else {
			$s .= '$$powexectoggleon ' . $on;
		}
	}
	return $s;
}

sub actPower { goto &actPower_name }
sub actPower_name {
	my ($start,$unq,$on,@rest) = @_;
	my ($s, $traytest) = ('','');
	if (ref $on) {
		#  deal with power slot stuff..
		$traytest = $on->{'trayslot'};
	}
	for my $v (@rest) {
		if (!ref $v) {
			if ($v and $v ne 'on') {
				$s .= '$$powexecname ' . $v;
			}
		} else { # $v is a ref
			while (my (undef, $w) = each %$v) {
				if ($w and $w ne 'on') {
					if (ref $w) {
						if ($w->{'trayslot'} eq $traytest) {
							$s .= '$$powexectray ' . $w->{'trayslot'};
						}
					} else {
						$s .= '$$powexecname ' . $w;
					}
				}
			}
			if ($v->{'trayslot'} and $v->{'trayslot'} eq $traytest) {
				$s .= '$$powexectray ' . $v->{'trayslot'};
			}
		}
	}
	if ($unq and $s) {
		$s .= '$$powexecunqueue';
	}

	if ($on and $on ne '') {
		if (ref $on) {
			#  deal with power slot stuff..
			$s .= '$$powexectray ' . $on->{'trayslot'} . '$$powexectray ' . $on->{'trayslot'};
		} else {
			$s .= '$$powexecname ' . $on . '$$powexecname ' . $on;
		}
	}
	if ($start) { $s = substr $s, 2; }
	return $s;
}

# TODO - this isn't used anywhere, is it useful?
#  updated hybrid binds can reduce the space used in SoD Bindfiles by more than 40KB per SoD mode generated
sub actPower_hybrid {
	my ($start,$unq,$on,@rest) = @_;
	my ($s, $traytest) = ('','');
	if (ref $on) { $traytest = $on->{'trayslot'}; }

	for my $v (@rest) {
		if (!ref $v) {
			if ($v eq 'on') { $s .= '$$powexecname ' . $v; }
		 } else {
			while (my (undef, $w) = each %$v) {
				if ($w and $w ne 'on') {
					if (ref $w) {
						if ($w->{'trayslot'} eq $traytest) {
							$s .= '$$powexectray ' . $w->{'trayslot'};
						}
					 } else {
						$s .= '$$powexecname ' . $w;
					}
				}
			}
			if ($v->{'trayslot'} eq $traytest) {
				$s .= '$$powexectray ' . $v->{'trayslot'};
			}
		}
	}
	if ($unq and $s) { $s .= '$$powexecunqueue'; }

	if ($on) {
		if (ref $on) {
			#  deal with power slot stuff..
			$s .= '$$powexectray ' . $on->{'trayslot'} . '$$powexectray ' . $on->{'trayslot'};
		 } else {
			$s .= '$$powexectoggleon ' . $on;
		}
	}
	if ($start) { $s = substr $s, 2; }
	return $s;
}

# local actPower = actPower_name;
# # local actPower = actPower_toggle
sub sodJumpFix {
	my ($profile,$t,$key,$makeModeKey,$suffix,$bl,$curfile,$turnoff,$autofollowmode,$feedback) = @_;

	my $filename = $t->path("${autofollowmode}j", $suffix);
	my $tglfile = $profile->GetBindFile($filename);
	$t->{'ini'} = '-down$$';
	&$makeModeKey($profile,$t,$bl,$tglfile,$turnoff,undef,1);
	$curfile->SetBind($key,"+down" . $feedback . actPower_name(undef,1,$t->{'cjmp'}) . BindFile::BLF($profile, $filename));
}

sub sodSetDownFix {
	my ($profile,$t,$key,$makeModeKey,$suffix,$bl,$curfile,$turnoff,$autofollowmode,$feedback) = @_;
	my $pathsuffix = $autofollowmode ? 'f' : 'a';
	my $filename = $t->path("$autofollowmode$pathsuffix", $suffix);
	my $tglfile = $profile->GetBindFile($filename);
	$t->{'ini'} = '-down$$';
	&$makeModeKey($profile,$t,$bl,$tglfile,$turnoff,undef,1);
	$curfile->SetBind($key,'+down' . $feedback . BindFile::BLF($profile, $filename));
}


UI::Labels::Add( {
	Up => 'Up',
	Down => 'Down',
	Forward => 'Forward',
	Back => 'Back',
	Left => 'Strafe Left',
	Right => 'Strafe Right',
	TurnLeft => 'Turn Left',
	TurnRight => 'Turn Right',
	AutoRun => 'Auto Run',
	Follow => 'Follow Target',

	DefaultMode => 'Default SoD Mode',
	MousechordSoD => 'Mousechord is SoD Forward',
	AutoMouselook => 'Automatically Mouselook when moving',

	SprintPower => 'Power to use for Sprint',

	ChangeCamera => 'Change camera distance when moving',
	CamdistBase => 'Base Camera Distance',
	CamdistTravelling => 'Travelling Camera Distance',

	ChangeDetail => 'Change graphics detail level when moving',
	DetailBase => 'Base Detail Level',
	DetailTravelling => 'Travelling Detail Level',

	NonSoDMode => 'Non-SoD Mode',
	ToggleSoD => 'SoD Mode Toggle',
	JumpMode => 'Toggle Jump Mode',
	SimpleSJCJ => 'Simple Combat Jumping / Super Jump Toggle',

	RunMode => 'Toggle Super Speed Mode',
	SSOnlyWhenMoving => 'SuperSpeed only when moving',
	SSSJModeEnable => 'Enable Super Speed / Super Jump Mode',

	FlyMode => 'Toggle Fly Mode',
	GFlyMode => 'Toggle Group Fly Mode',

	SelfTellOnChange => 'Self-/tell when changing mode',

	TPMode  => 'Teleport Bind',
	TPCombo => 'Teleport Combo Key',
	TPReset => 'Teleport Reset Key',
	HideWinsDuringTP => 'Hide Windows when Teleporting',
	AutoHoverTP => 'Automatically use Hover when Teleporting',

	TTPMode  => 'Team Teleport Bind',
	TTPCombo => 'Team Teleport Combo Key',
	TTPReset => 'Team Teleport Reset Key',
	AutoGFlyTTP => 'Automatically use Group Fly when Team Teleporting',

	TempMode => 'Toggle Temp Mode',
	TempTray => 'Temporary Travel Power Tray',

	NovaMode => 'Toggle Nova Form',
	NovaTray => 'Nova Travel Power Tray',
	DwarfMode => 'Toggle Dwarf Form',
	DwarfTray => 'Dwarf Travel Power Tray',
	HumanMode => 'Human Form',
	HumanTray => 'Human Travel Power Tray',

	SprintSoD => 'Enable Sprint SoD',
});

package Page::SoD::Table;

sub new {
	my ($class, $init) = @_;

	my $self = $init;

	bless ($self, $class);

	return $self;
}

sub KeyState {
	my $t = shift;
	my $p = shift;
	my $togglebit = $p->{'toggle'} || '';

	my $ret;
	for (qw(space X W S A D)) {
		$ret .= ($_ eq $togglebit) ? not $t->{$_} : $t->{$_};
	}
	return $ret;
}

# These next two subs are terrible.  This stuff should all be squirreled away in BindFile.

# This will return "$$bindloadfilesilent C:\path\CODE\CODE1010101<suffix>.txt"
sub bl {
	my $self = shift;
	my $code = shift;
	my $suffix = shift || '';
	my $p = $self->{'profile'};
	return BindFile::BLF($p, uc($code), uc($code) . $self->KeyState . $suffix . '.txt');
}

# This will return "CODE\CODE1010101<suffix>.txt"
sub path {
	my $self = shift;
	my $code = shift;
	my $suffix = shift || '';
	return File::Spec->catpath(undef, uc($code), uc($code) . $self->KeyState . $suffix . '.txt');
}

sub dirs {
	my $self = shift;
	my $ret;
	for (split '', shift) {
		$ret .= $self->{ { U => 'up', D => 'dow', F => 'forw', B => 'bac', L => 'lef', R => 'rig' }->{$_} };
	}
	return $ret;
}
sub U { shift()->{'up'} }
sub D { shift()->{'dow'} }
sub F { shift()->{'forw'} }
sub B { shift()->{'bac'} }
sub L { shift()->{'lef'} }
sub R { shift()->{'rig'} }

1;
