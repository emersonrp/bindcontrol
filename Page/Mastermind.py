#!/usr/bin/perl

use strict;

package Page::Mastermind;
use parent "Page::Page";

use BindFile;

use Wx qw();

our $PageName = 'MastermindPets';

sub InitKeys {

	my $self = shift;

	$self->Profile->MastermindPets ||= {
		Enable => undef,

		PetSelectAll => 'ALT-V',
		PetSelectAllResponse => 'Orders?',
		PetSelectAllResponseMethod => 'Petsay',

		PetSelectMinions => 'ALT-Z',
		PetSelectMinionsResponse => 'Orders?',
		PetSelectMinionsResponseMethod => 'Petsay',

		PetSelectLieutenants => 'ALT-X',
		PetSelectLieutenantsResponse => 'Orders?',
		PetSelectLieutenantsResponseMethod => 'Petsay',

		PetSelectBoss => 'ALT-C',
		PetSelectBossResponse => 'Orders?',
		PetSelectBossResponseMethod => 'Petsay',

		PetBodyguard => 'ALT-G',
		PetBodyguardResponse => 'Bodyguarding.',
		PetBodyguardResponseMethod => 'Petsay',

		PetAggressive => 'ALT-A',
		PetAggressiveResponse => 'Kill On Sight.',
		PetAggressiveResponseMethod => 'Petsay',

		PetDefensive => 'ALT-S',
		PetDefensiveResponse => 'Return Fire Only.',
		PetDefensiveResponseMethod => 'Petsay',

		PetPassive => 'ALT-D',
		PetPassiveResponse => 'At Ease.',
		PetPassiveResponseMethod => 'Petsay',

		PetAttack => 'ALT-Q',
		PetAttackResponse => 'Open Fire!',
		PetAttackResponseMethod => 'Petsay',

		PetFollow => 'ALT-W',
		PetFollowResponse => 'Falling In.',
		PetFollowResponseMethod => 'Petsay',

		PetStay => 'ALT-E',
		PetStayResponse => 'Holding This Position',
		PetStayResponseMethod => 'Petsay',

		PetGoto => 'ALT-LBUTTON',
		PetGotoResponse => 'Moving To Checkpoint.',
		PetGotoResponseMethod => 'Petsay',

		PetBodyguardMode => 1,
		PetBodyguardAttack => '',
		PetBodyguardGoto => '',

		PetBackgroundAttack => 'UNBOUND',  # TODO -- need UI for this
		PetBackgroundGoto => 'UNBOUND',  # TODO -- need UI for this
		PetBackgroundAttackEnabled => 0,  # TODO -- need UI for this
		PetBackgroundGotoEnabled => 0,  # TODO -- need UI for this


		PetChatToggle => 'ALT-M',
		PetSelect1 => 'F1',
		PetSelect2 => 'F2',
		PetSelect3 => 'F3',
		PetSelect4 => 'F4',
		PetSelect5 => 'F5',
		PetSelect6 => 'F6',

		Pet1Name => 'Crow T Robot',
		Pet2Name => 'Tom Servo',
		Pet3Name => 'Cambot',
		Pet4Name => 'Gypsy',
		Pet5Name => 'Mike',
		Pet6Name => 'Joel',

		Pet1Bodyguard => 0,
		Pet2Bodyguard => 1,
		Pet3Bodyguard => 0,
		Pet4Bodyguard => 0,
		Pet5Bodyguard => 1,
		Pet6Bodyguard => 0,

	};
}

sub FillTab {

	my $self = shift;

	$self->TabTitle = 'Mastermind / Pet Binds';

	my $MMP = $self->Profile->MastermindPets;

	my $sizer = Wx::BoxSizer->new(Wx::wxVERTICAL);

	my $useCB = Wx::CheckBox->new( $self, -1, 'Enable Mastermind Pet Binds');
	$useCB->SetToolTip(Wx::ToolTip->new('Check this to enable the Mastermind Pet Action Binds'));
	$sizer->Add($useCB, 0, Wx::wxALL, 10);

# TODO - add checkbox handler to hide/show (enable/disable?) the bodyguard options
# TODO -- actually, automagically enable/disable these depending on whether any pets have their
# individual "Bodyguard" checkboxes checked.
	my $bgCB = Wx::CheckBox->new( $self, -1, 'Enable Bodyguard Mode Binds');
	$bgCB->SetToolTip(Wx::ToolTip->new('Check this to enable the Bodyguard Mode Binds'));
	$bgCB->SetValue($MMP->{'PetBodyguardMode'});
	$sizer->Add($bgCB, 0, Wx::wxALL, 10);

	$sizer->AddSpacer(10);

	# Iterate the data structure at the bottom and make the grid of controls for the basic pet binds
	my $ChatOptions = [ qw( Local Self-Tell Petsay None ) ];
	my $PetCommandKeyRows = Wx::FlexGridSizer->new(0,5,2,2);
	for my $k (petCommandKeyDefinitions()) {

		my $basename = $k->{'basename'};  # all of the fieldnames we look up in the MMP are based on this value

		my $al = Wx::StaticText->new($self, -1, $k->{'label'});
		my $ab = Wx::Button->    new($self, Utility::id($basename), $MMP->{$basename});

		my $cl = Wx::StaticText->new($self, -1, "Respond via:");
		my $cm = Wx::ComboBox->  new($self, Utility::id("${basename}ResponseMethod"), $MMP->{"${basename}ResponseMethod"},
				Wx::wxDefaultPosition, Wx::wxDefaultSize, $ChatOptions, Wx::wxCB_READONLY);
		my $cr = Wx::TextCtrl->  new($self, Utility::id("${basename}Response"),   $MMP->{"${basename}Response"});

		my $tip = $k->{'tooltipdetail'};
		$ab->SetToolTip( Wx::ToolTip->new("Choose the key combo that will $tip"));
		$cm->SetToolTip( Wx::ToolTip->new("Choose the method your pets will use to respond when they are in chatty mode and you $tip"));
		$cr->SetToolTip( Wx::ToolTip->new("Choose the chat response your pets will give when you $tip"));
		$cr->SetMinSize( [250, -1] );

		$PetCommandKeyRows->Add($al, 0, Wx::wxALIGN_RIGHT|Wx::wxALIGN_CENTER_VERTICAL);
		$PetCommandKeyRows->Add($ab, 0, Wx::wxEXPAND);
		$PetCommandKeyRows->Add($cl, 0, Wx::wxALIGN_RIGHT|Wx::wxALIGN_CENTER_VERTICAL);
		$PetCommandKeyRows->Add($cm);
		$PetCommandKeyRows->Add($cr, 0, Wx::wxEXPAND);

	}
	$sizer->Add($PetCommandKeyRows);

	$sizer->AddSpacer(15);

	# get the pet names, whether they're bodyguards, and binds to select them directly
	# TODO -- probably want to enable/disable various bits of this based on whether bodyguard is
	# active, or whether we have names, or whatever
	my $PetNames = Wx::FlexGridSizer->new(0,5,5,5);
	for my $PetID (1..6) {

		my $pn = Wx::TextCtrl->new($self,  Utility::id("Pet${PetID}Name"), $MMP->{"Pet${PetID}Name"});
		$pn->SetToolTip( Wx::ToolTip->new("Specify Pet ${PetID}'s Name for individual selection") );

		my $cb = Wx::CheckBox->new($self, Utility::id("Pet${PetID}Bodyguard"), "Bodyguard" );
		$cb->SetValue($MMP->{"Pet${PetID}Bodyguard"});
		$cb->SetToolTip( Wx::ToolTip->new("Select whether pet $PetID acts as Bodyguard") );

		my $bn = Wx::Button->    new($self, Utility::id("PetSelect$PetID"), $MMP->{"PetSelect$PetID"});
		$bn->SetToolTip( Wx::ToolTip->new("Choose the Key Combo to Select Pet $PetID"));

		$PetNames->Add( Wx::StaticText->new($self, -1, "Pet ${PetID}'s Name"), 0, Wx::wxALIGN_CENTER_VERTICAL);
		$PetNames->Add( $pn );
		$PetNames->Add( $cb, 0, Wx::wxALIGN_CENTER_VERTICAL);
		$PetNames->Add( Wx::StaticText->new($self, -1, "Select Pet $PetID"), 0, Wx::wxALIGN_CENTER_VERTICAL);
		$PetNames->Add( $bn );
	}
	$sizer->Add($PetNames);

	$self->SetSizerAndFit($sizer);

	return $self;
}

sub HelpText { qq|
	The Original Mastermind Control Binds
	were created in CoV Beta by Khaiba
	a.k.a. Sandolphan
	Bodyguard code inspired directly from
	Sandolphan's Bodyguard binds.
	Thugs added by Konoko!
|;}

sub mmBGSelBind {
	my ($profile,$file,$PetBodyguardResponse,$powers) = @_;
	my $MMP = $profile->MastermindPets;
	if ($MMP->{'bg_enable'}) {
		my ($bgsay, $bgset, $tier1bg, $tier2bg, $tier3bg);
		#  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
		#  first check if any full tier groups are bodyguards.  full tier groups are either All BG or all NBG.
		if ($MMP->{'Pet1Bodyguard'}) { $tier1bg++; }
		if ($MMP->{'Pet2Bodyguard'}) { $tier1bg++; }
		if ($MMP->{'Pet3Bodyguard'}) { $tier1bg++; }
		if ($MMP->{'Pet4Bodyguard'}) { $tier2bg++; }
		if ($MMP->{'Pet5Bodyguard'}) { $tier2bg++; }
		if ($MMP->{'Pet6Bodyguard'}) { $tier3bg++; }
		#  if $tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
		#  if $tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
		#  $tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
		#  so, add all fullgroups into the bgsay command.
		#  first check if $tier1bg + $tier2bg + $tier3bg == 6, if so, we can get away with petsayall.
		if ((($tier1bg + $tier2bg + $tier3bg) == 6) or ($MMP->{'PetBodyguardResponseMethod'} != 3)) {
			my @saymethall = ("local ",'tell, $name ',"petsayall ","");
			$bgsay = $MMP->{'PetBodyguardResponseMethod'} . $PetBodyguardResponse;
		} else {
			if ($tier1bg == 3) {
				$bgsay .= '$$petsaypow ' . "$powers->{'min'} $PetBodyguardResponse";
			} else {
				#  use petsayname commands for those $tier1s that are bodyguards.
				$bgsay .= '$$petsayname ' . "$MMP->{'Pet1Name'} $PetBodyguardResponse" if ($MMP->{'Pet1Bodyguard'});
				$bgsay .= '$$petsayname ' . "$MMP->{'Pet2Name'} $PetBodyguardResponse" if ($MMP->{'Pet2Bodyguard'});
				$bgsay .= '$$petsayname ' . "$MMP->{'Pet3Name'} $PetBodyguardResponse" if ($MMP->{'Pet3Bodyguard'});
			}
			if ($tier2bg == 2) {
				$bgsay .= '$$petsaypow ' . "ltspow $PetBodyguardResponse";
			} else {
				$bgsay .= '$$petsayname ' . "$MMP->{'Pet4Name'} $PetBodyguardResponse" if ($MMP->{'Pet4Bodyguard'});
				$bgsay .= '$$petsayname ' . "$MMP->{'Pet5Name'} $PetBodyguardResponse" if ($MMP->{'Pet5Bodyguard'});
			}
			if ($tier3bg == 1) {
				$bgsay .= '$$petsaypow ' . "$powers->{'bos'} $PetBodyguardResponse";
			}
		}
		if (($tier1bg + $tier2bg + $tier3bg) == 6) {
			$bgset = '$$petcomall def fol';
		} else {
			if ($tier1bg == 3) {
				$bgset .= '$$petcompow ' . "$powers->{'min'} def fol";
			} else {
				#  use petsayname commands for those $tier1s that are bodyguards.
				$bgset .= '$$petcomname ' . "$MMP->{'Pet1Name'} def fol" if ($MMP->{'Pet1Bodyguard'});
				$bgset .= '$$petcomname ' . "$MMP->{'Pet2Name'} def fol" if ($MMP->{'Pet2Bodyguard'});
				$bgset .= '$$petcomname ' . "$MMP->{'Pet3Name'} def fol" if ($MMP->{'Pet3Bodyguard'});
			}
			if ($tier2bg == 2) {
				$bgset .= '$$petcompow ' . "$powers->{'lts'} def fol";
			} else {
				$bgset .= '$$petcomname ' . "$MMP->{'Pet4Name'} def fol" if ($MMP->{'Pet4Bodyguard'});
				$bgset .= '$$petcomname ' . "$MMP->{'Pet5Name'} def fol" if ($MMP->{'Pet5Bodyguard'});
			}
			if ($tier3bg == 1) {
				$bgset .= '$$petcompow ' . "$powers->{'bos'} def fol";
			}
		}
		$file->SetBind($MMP->{'selbgm'}, $bgsay . $bgset . BindFile::BLF($profile, 'mmbinds','\cbguarda.txt'));
	}
}

sub mmBGActBind {
	my ($profile,$filedn,$fileup,$action,$say,$powers) = @_;

	my $MMP    = $profile->MastermindPets;
	my $key    = $MMP->{"Pet$action"};
	my $method = $MMP->{"Pet${action}ResponseMethod"};

	my ($bgact, $bgsay, $tier1bg, $tier2bg, $tier3bg);
	#  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
	#  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
	if ($MMP->{'Pet1Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet2Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet3Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet4Bodyguard'}) { $tier2bg++; }
	if ($MMP->{'Pet5Bodyguard'}) { $tier2bg++; }
	if ($MMP->{'Pet6Bodyguard'}) { $tier3bg++; }
	#  if $tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
	#  if $tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
	#  $tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
	#  so, add all fullgroups into the bgsay command.
	#  first check if $tier1bg + $tier2bg + $tier3bg == 6, if so, we can get away with petsayall.
	if ((($tier1bg + $tier2bg + $tier3bg) == 0) or ($method != 3)) {
		my @saymethall = ("local ",'tell, $name ',"petsayall ","");
		$bgsay = $method . $say;
	} else {
		if ($tier1bg == 0) {
			$bgsay .= '$$petsaypow ' . "$powers->{'min'} $say";
		} else {
			#  use petsayname commands for those $tier1s that are bodyguards.
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet1Name'} $say" if (not $MMP->{'Pet1Bodyguard'});
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet2Name'} $say" if (not $MMP->{'Pet2Bodyguard'});
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet3Name'} $say" if (not $MMP->{'Pet3Bodyguard'});
		}
		if ($tier2bg == 0) {
			$bgsay .= '$$petsaypow ' . "$powers->{'lts'} $say";
		} else {
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet4Name'} $say" if (not $MMP->{'Pet4Bodyguard'});
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet5Name'} $say" if (not $MMP->{'Pet5Bodyguard'});
		}
		if ($tier3bg == 0) {
			$bgsay .= '$$petsaypow ' . "$powers->{'bos'} $say";
		}
	}
	if (($tier1bg + $tier2bg + $tier3bg) == 0) {
		$bgact = '$$petcomall ' . $action;
	} else {
		if ($tier1bg == 0) {
			$bgact .= '$$petcompow ' . "$powers->{'min'} $action";
		} else {
			#  use petsayname commands for those $tier1s that are bodyguards.
			$bgact .= '$$petcomname ' . "$MMP->{'Pet1Name'} $action" if (not $MMP->{'Pet1Bodyguard'});
			$bgact .= '$$petcomname ' . "$MMP->{'Pet2Name'} $action" if (not $MMP->{'Pet2Bodyguard'});
			$bgact .= '$$petcomname ' . "$MMP->{'Pet3Name'} $action" if (not $MMP->{'Pet3Bodyguard'});
		}
		if ($tier2bg == 0) {
			$bgact .= '$$petcompow ' . "$powers->{'lts'} $action";
		} else {
			$bgact .= '$$petcomname ' . "$MMP->{'Pet4Name'} $action" if (not $MMP->{'Pet4Bodyguard'});
			$bgact .= '$$petcomname ' . "$MMP->{'Pet5Name'} $action" if (not $MMP->{'Pet5Bodyguard'});
		}
		if ($tier3bg == 0) {
			$bgact .= '$$petcompow ' . "$powers->{'bos'} $action";
		}
	}
	cbWriteToggleBind($filedn,$fileup,$key,$bgsay,$bgact,$filedn->BLFPath,$fileup->BLFPath);
}

sub mmBGActBGBind {
	my ($profile,$filedn,$fileup,$action,$say,$powers) = @_;

	my $MMP =    $profile->MastermindPets;
	my $key =    $MMP->{"PetBackground$action"};
	my $method = $MMP->{"Pet${action}ResponseMethod"};

	my ($bgact, $bgsay, $tier1bg, $tier2bg, $tier3bg);
	#  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
	#  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
	if ($MMP->{'Pet1Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet2Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet3Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet4Bodyguard'}) { $tier2bg++; }
	if ($MMP->{'Pet5Bodyguard'}) { $tier2bg++; }
	if ($MMP->{'Pet6Bodyguard'}) { $tier3bg++; }
	#  if $tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
	#  if $tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
	#  $tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
	#  so, add all fullgroups into the bgsay command.
	#  first check if $tier1bg + $tier2bg + $tier3bg == 6, if so, we can get away with petsayall.
	if ((($tier1bg + $tier2bg + $tier3bg) == 6) or ($method != 3)) {
		my @saymethall = ("local ",'tell, $name ',"petsayall ","");
		$bgsay = $method . $say;
	} else {
		if ($tier1bg == 3) {
			$bgsay .= '$$petsaypow ' . "$powers->{'min'} $say";
		} else {
			#  use petsayname commands for those $tier1s that are bodyguards.
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet1Name'} $say" if ($MMP->{'Pet1Bodyguard'});
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet2Name'} $say" if ($MMP->{'Pet2Bodyguard'});
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet3Name'} $say" if ($MMP->{'Pet3Bodyguard'});
		}
		if ($tier2bg == 2) {
			$bgsay .= '$$petsaypow ' / "$powers->{'lts'} $say";
		} else {
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet4Name'} $say" if ($MMP->{'Pet4Bodyguard'});
			$bgsay .= '$$petsayname ' . "$MMP->{'Pet5Name'} $say" if ($MMP->{'Pet5Bodyguard'});
		}
		if ($tier3bg == 1) {
			$bgsay .= '$$petsaypow ' . "$powers->{'bos'} $say";
		}
	}
	if (($tier1bg + $tier2bg + $tier3bg) == 6) {
		$bgact = '$$petcomall ' . $action;
	} else {
		if ($tier1bg == 3) {
			$bgact .= '$$petcompow ' . "$powers->{'min'} $action";
		} else {
			#  use petsayname commands for those $tier1s that are bodyguards.
			$bgact .= '$$petcomname ' . "$MMP->{'Pet1Name'} $action" if ($MMP->{'Pet1Bodyguard'});
			$bgact .= '$$petcomname ' . "$MMP->{'Pet2Name'} $action" if ($MMP->{'Pet2Bodyguard'});
			$bgact .= '$$petcomname ' . "$MMP->{'Pet3Name'} $action" if ($MMP->{'Pet3Bodyguard'});
		}
		if ($tier2bg == 2) {
			$bgact .= '$$petcompow ' . "$powers->{'lts'} $action";
		} else {
			$bgact .= '$$petcomname ' . "$MMP->{'Pet4Name'} $action" if ($MMP->{'Pet4Bodyguard'});
			$bgact .= '$$petcomname ' . "$MMP->{'Pet5Name'} $action" if ($MMP->{'Pet5Bodyguard'});
		}
		if ($tier3bg == 1) {
			$bgact .= '$$petcompow ' . "$powers->{'bos'} $action";
		}
	}
	# file->SetBind($MMP->{'selbgm'},bgsay.$bgset.BindFile::BLF($profile, 'mmbinds','\mmbinds\\cbguarda.txt'));
	cbWriteToggleBind($filedn,$fileup,$key,$bgsay,$bgact,$filedn->BLFPath,$fileup->BLFPath);
}

sub mmQuietBGSelBind {
	my ($profile,$file,$powers) = @_;
	my $MMP = $profile->MastermindPets;
	if ($MMP->{'bg_enable'}) {
		my ($bgset, $tier1bg, $tier2bg, $tier3bg);
		#  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
		#  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
		if ($MMP->{'Pet1Bodyguard'}) { $tier1bg++; }
		if ($MMP->{'Pet2Bodyguard'}) { $tier1bg++; }
		if ($MMP->{'Pet3Bodyguard'}) { $tier1bg++; }
		if ($MMP->{'Pet4Bodyguard'}) { $tier2bg++; }
		if ($MMP->{'Pet5Bodyguard'}) { $tier2bg++; }
		if ($MMP->{'Pet6Bodyguard'}) { $tier3bg++; }
		#  if $tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
		#  if $tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
		#  $tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
		#  so, add all fullgroups into the bgsay command.
		#  first check if $tier1bg + $tier2bg + $tier3bg == 6, if so, we can get away with petsayall.
		if (($tier1bg + $tier2bg + $tier3bg) == 6) {
			$bgset = "petcomall def fol";
		} else {
			if ($tier1bg == 3) {
				$bgset .= '$$petcompow ' . "$powers->{'min'} def fol";
			} else {
				#  use petsayname commands for those $tier1s that are bodyguards.
				$bgset .= '$$petcomname ' . "$MMP->{'Pet1Name'} def fol" if ($MMP->{'Pet1Bodyguard'});
				$bgset .= '$$petcomname ' . "$MMP->{'Pet2Name'} def fol" if ($MMP->{'Pet2Bodyguard'});
				$bgset .= '$$petcomname ' . "$MMP->{'Pet3Name'} def fol" if ($MMP->{'Pet3Bodyguard'});
			}
			if ($tier2bg == 2) {
				$bgset .= '$$petcompow ' . "$powers->{'lts'} def fol";
			} else {
				$bgset .= '$$petcomname ' . "$MMP->{'Pet4Name'} def fol" if ($MMP->{'Pet4Bodyguard'});
				$bgset .= '$$petcomname ' . "$MMP->{'Pet5Name'} def fol" if ($MMP->{'Pet5Bodyguard'});
			}
			if ($tier3bg == 1) {
				$bgset .= '$$petcompow ' . "$powers->{'bos'} def fol";
			}
		}
		$file->SetBind($MMP->{'selbgm'},$bgset . BindFile::BLF($profile, 'mmbinds','\mmbinds\\bguarda.txt'));
	}
}

sub mmQuietBGActBind {
	my ($profile,$filedn,$fileup,$action,$powers) = @_;

	my $MMP = $profile->MastermindPets;
	my $key = $MMP->{"PetBackground$action"};

	my ($bgact, $tier1bg, $tier2bg, $tier3bg);
	#  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
	#  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
	if ($MMP->{'Pet1Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet2Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet3Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet4Bodyguard'}) { $tier2bg++; }
	if ($MMP->{'Pet5Bodyguard'}) { $tier2bg++; }
	if ($MMP->{'Pet6Bodyguard'}) { $tier3bg++; }
	#  if $tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
	#  if $tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
	#  $tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
	#  so, add all fullgroups into the bgsay command.
	#  first check if $tier1bg + $tier2bg + $tier3bg == 6, if so, we can get away with petsayall.
	if (($tier1bg + $tier2bg + $tier3bg) == 0) {
		$bgact = "petcomall $action";
	} else {
		if ($tier1bg == 0) {
			$bgact .= '$$petcompow ' . "$powers->{'min'} $action";
		} else {
			#  use petsayname commands for those $tier1s that are bodyguards.
			if (not $MMP->{'Pet1Bodyguard'}) {
				$bgact .= '$$petcomname ' . "$MMP->{'Pet1Name'} $action";
			}
			if (not $MMP->{'Pet2Bodyguard'}) {
				$bgact .= '$$petcomname ' . "$MMP->{'Pet2Name'} $action";
			}
			if (not $MMP->{'Pet3Bodyguard'}) {
				$bgact .= '$$petcomname ' . "$MMP->{'Pet3Name'} $action";
			}
		}
		if ($tier2bg == 0) {
			$bgact .= '$$petcompow ' . "$powers->{'lts'} $action";
		} else {
			if (not $MMP->{'Pet4Bodyguard'}) {
				$bgact .= '$$petcomname ' . "$MMP->{'Pet4Name'} $action";
			}
			if (not $MMP->{'Pet5Bodyguard'}) {
				$bgact .= '$$petcomname ' . "$MMP->{'Pet5Name'} $action";
			}
		}
		if ($tier3bg == 0) {
			$bgact .= '$$petcompow ' . "$powers->{'bos'} $action";
		}
	}
	# 'petcompow ',,grp.' Stay'
	$filedn->SetBind($key,$bgact);
}

sub mmQuietBGActBGBind {
	my ($profile,$filedn,$fileup,$action,$powers) = @_;

	my $MMP    = $profile->MastermindPets;
	my $key    = $MMP->{"PetBackground$action"};
	my $method = $MMP->{"Pet${action}ResponseMethod"};

	my ($bgact, $tier1bg, $tier2bg, $tier3bg);
	#  fill bgsay with the right commands to have bodyguards say PetBodyguardResponse
	#  first check if any full tier groups are bodyguards.  full tier groups are eaither All BG or all NBG.
	if ($MMP->{'Pet1Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet2Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet3Bodyguard'}) { $tier1bg++; }
	if ($MMP->{'Pet4Bodyguard'}) { $tier2bg++; }
	if ($MMP->{'Pet5Bodyguard'}) { $tier2bg++; }
	if ($MMP->{'Pet6Bodyguard'}) { $tier3bg++; }
	#  if $tier1bg is 3 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
	#  if $tier2bg is 2 or 0 then it is a full bg or full nbg group.  otherwise we have to call them by name.
	#  $tier3bg is ALWAYS a full group, with only one member, he is either BG or NBG
	#  so, add all fullgroups into the bgsay command.
	#  first check if $tier1bg + $tier2bg + $tier3bg == 6, if so, we can get away with petsayall.
	if (($tier1bg + $tier2bg + $tier3bg) == 6) {
		$bgact = "petcomall $action";
	} else {
		if ($tier1bg == 3) {
			$bgact .= '$$petcompow ' . "$powers->{'min'} $action";
		} else {
			#  use petsayname commands for those $tier1s that are bodyguards.
			$bgact .= '$$petcomname ' . "$MMP->{'Pet1Name'} $action" if ($MMP->{'Pet1Bodyguard'});
			$bgact .= '$$petcomname ' . "$MMP->{'Pet2Name'} $action" if ($MMP->{'Pet2Bodyguard'});
			$bgact .= '$$petcomname ' . "$MMP->{'Pet3Name'} $action" if ($MMP->{'Pet3Bodyguard'});
		}
		if ($tier2bg == 2) {
			$bgact .= '$$petcompow ' . "$powers->{'lts'} $action";
		} else {
			$bgact .= '$$petcomname ' . "$MMP->{'Pet4Name'} $action" if ($MMP->{'Pet4Bodyguard'});
			$bgact .= '$$petcomname ' . "$MMP->{'Pet5Name'} $action" if ($MMP->{'Pet5Bodyguard'});
		}
		if ($tier3bg == 1) {
			$bgact .= '$$petcompow ' . "$powers->{'bos'} $action";
		}
	}
	# 'petcompow ',,grp.' Stay'
	$filedn->SetBind($key,$bgact);
}

sub mmSubBind {
	my ($profile,$file,$fn,$grp,$powers) = @_;
	my $MMP = $profile->MastermindPets;
	my %PetResponses;
	for my $cmd (qw(SelectAll SelectMinions SelectLieutenants SelectBoss Bodyguard Aggressive Defensive Passive Attack Follow Stay Goto) ) {
		if ($MMP->{"Pet${cmd}ResponseMethod"} ne 'None') { $PetResponses{$cmd} = $MMP->{"Pet${cmd}Response"} }
	}

	$file->SetBind($MMP->{'PetSelectAll'},        $MMP->{'PetSelectAllResponseMethod'}         . " $PetResponses{'SelectAll'}"         . BindFile::BLF($profile, 'mmbinds','call.txt'));
	$file->SetBind($MMP->{'PetSelectMinions'},    $MMP->{'PetSelectMinionsResponseMethod'}     . " $PetResponses{'SelectMinions'}"     . BindFile::BLF($profile, 'mmbinds','ctier1.txt'));
	$file->SetBind($MMP->{'PetSelectLieutenants'},$MMP->{'PetSelectLieutenantsResponseMethod'} . " $PetResponses{'SelectLieutenants'}" . BindFile::BLF($profile, 'mmbinds','ctier2.txt'));
	$file->SetBind($MMP->{'PetSelectBoss'},       $MMP->{'PetSelectBossResponseMethod'}        . " $PetResponses{'SelectBoss'}"        . BindFile::BLF($profile, 'mmbinds','ctier3.txt'));

	mmBGSelBind($profile,$file,$PetResponses{'Bodyguard'},$powers);

	my $petcom = ($grp) ? "\$\$petcompow$grp" : '$$petcomall';
	for my $cmd (qw(Aggressive Defensive Attack Follow Stay Goto)) {
		$file->SetBind($MMP->{"Pet$cmd"},$MMP->{"Pet${cmd}ResponseMethod"} . " $PetResponses{$cmd}$petcom $cmd");
	}
	if ($MMP->{'PetBackgroundAttackEnabled'})  { $file->SetBind($MMP->{'PetBackgroundAttack'},'nop'); }
	if ($MMP->{'PetBackgroundGotoenabled'}) { $file->SetBind($MMP->{'PetBackgroundGoto'},'nop'); }
	$file->SetBind($MMP->{'chattykey'},'tell $name, Non-Chatty Mode' . BindFile::BLF($profile, 'mmbinds',"$fn.txt"));
}

sub mmBGSubBind {
	my ($profile,$filedn,$fileup,$fn,$powers) = @_;
	my $MMP = $profile->MastermindPets;
	my %PetResponses;
	for my $cmd (qw(SelectAll SelectMinions SelectLieutenants SelectBoss Bodyguard Aggressive Defensive Passive Attack Follow Stay Goto) ) {
		if ($MMP->{'Pet${cmd}ResponseMethod'} ne 'None') { $PetResponses{$cmd} = $MMP->{'Pet${cmd}Response'} }
	}

	$filedn->SetBind($MMP->{'PetSelectAll'},        $MMP->{'PetSelectAllResponseMethod'}         .  " $PetResponses{'SelectAll'}"         . BindFile::BLF($profile, 'mmbinds','call.txt'));
	$filedn->SetBind($MMP->{'PetSelectMinions'},    $MMP->{'PetSelectMinionsResponseMethod'}     .  " $PetResponses{'SelectMinions'}"     . BindFile::BLF($profile, 'mmbinds','ctier1.txt'));
	$filedn->SetBind($MMP->{'PetSelectLieutenants'},$MMP->{'PetSelectLieutenantsResponseMethod'} .  " $PetResponses{'SelectLieutenants'}" . BindFile::BLF($profile, 'mmbinds','ctier2.txt'));
	$filedn->SetBind($MMP->{'PetSelectBoss'},       $MMP->{'PetSelectBossResponseMethod'}        .  " $PetResponses{'SelectBoss'}"        . BindFile::BLF($profile, 'mmbinds','ctier3.txt'));
	mmBGSelBind($profile,$filedn,$PetResponses{'Bodyguard'},$powers);

	for my $cmd (qw(Aggressive Defensive Attack Follow Stay Goto)) {
		mmBGActBind($profile,$filedn,$fileup,$cmd,$PetResponses{$cmd},$powers);
	}
	if ($MMP->{'PetBackgroundAttackenabled'}) {
		mmBGActBGBind($profile,$filedn,$fileup,'Attack',$PetResponses{'Attack'},$powers);
	}
	if ($MMP->{'PetBackgroundGotoenabled'}) {
		mmBGActBGBind($profile,$filedn,$fileup,'Goto',$PetResponses{'Goto'},$powers);
	}
	$filedn->SetBind($MMP->{'chattykey'},'tell $name, Non-Chatty Mode' . BindFile::BLF($profile, 'mmbinds',"${fn}a.txt"));
}

sub mmQuietSubBind {
	my ($profile,$file,$fn,$grp,$powers) = @_;
	my $MMP = $profile->MastermindPets;
	$file->SetBind($MMP->{'PetSelectAll'},        BindFile::BLFs($profile, 'mmbinds','all.txt'));
	$file->SetBind($MMP->{'PetSelectMinions'},    BindFile::BLFs($profile, 'mmbinds','tier1.txt'));
	$file->SetBind($MMP->{'PetSelectLieutenants'},BindFile::BLFs($profile, 'mmbinds','tier2.txt'));
	$file->SetBind($MMP->{'PetSelectBoss'},       BindFile::BLFs($profile, 'mmbinds','tier3.txt'));
	mmQuietBGSelBind($profile,$file,$powers);

	my $petcom = ($grp) ? "\$\$petcompow$grp" : '$$petcomall';
	for my $cmd (qw(Aggressive Defensive Attack Follow Stay Goto)) {
		$file->SetBind($MMP->{"Pet$cmd"},"$petcom $cmd");
	}
	if ($MMP->{'PetBackgroundAttackenabled'})  { $file->SetBind($MMP->{'PetBackgroundAttack'} ,'nop'); }
	if ($MMP->{'PetBackgroundGotoenabled'}) { $file->SetBind($MMP->{'PetBackgroundGoto'},'nop'); }

	$file->SetBind($MMP->{'chattykey'},'tell $name, Chatty Mode' . BindFile::BLF($profile, 'mmbinds','c' . $fn . '.txt'));
}

sub mmQuietBGSubBind {
	my ($profile,$filedn,$fileup,$fn,$powers) = @_;
	my $MMP = $profile->MastermindPets;
	$filedn->SetBind($MMP->{'PetSelectAll'},        BindFile::BLFs($profile, 'mmbinds','all.txt'));
	$filedn->SetBind($MMP->{'PetSelectMinions'},    BindFile::BLFs($profile, 'mmbinds','tier1.txt'));
	$filedn->SetBind($MMP->{'PetSelectLieutenants'},BindFile::BLFs($profile, 'mmbinds','tier2.txt'));
	$filedn->SetBind($MMP->{'PetSelectBoss'},       BindFile::BLFs($profile, 'mmbinds','tier3.txt'));
	mmQuietBGSelBind($profile,$filedn,$powers);
	for my $cmd (qw(Aggressive Defensive Passive Attack Follow Stay Goto)) {
		mmQuietBGActBind($profile,$filedn,$fileup,$cmd,$powers);
	}
	if ($MMP->{'PetBackgroundAttackenabled'}) {
		mmQuietBGActBGBind($profile,$filedn,$fileup,'Attack',$powers);
	}
	if ($MMP->{'PetBackgroundGotoenabled'}) {
		mmQuietBGActBGBind($profile,$filedn,$fileup,'Goto',$powers);
	}
	$filedn->SetBind($MMP->{'chattykey'},'tell $name, Chatty Mode' . BindFile::BLF($profile, 'mmbinds','c' . $fn . 'a.txt'));
}

sub PopulateBindFiles {
	my $profile = shift->Profile;
	my $ResetFile = $profile->General->{'ResetFile'};
	my $MMP = $profile->MastermindPets;
	if ($MMP->{'petselenable'}) {
		$ResetFile->SetBind($MMP->{'sel0'},"petselectname  $MMP->{'Pet1Name'}") if ($MMP->{'Pet1Nameenabled'});
		$ResetFile->SetBind($MMP->{'sel1'},"petselectname  $MMP->{'Pet2Name'}") if ($MMP->{'Pet2Nameenabled'});
		$ResetFile->SetBind($MMP->{'sel2'},"petselectname  $MMP->{'Pet3Name'}") if ($MMP->{'Pet3Nameenabled'});
		$ResetFile->SetBind($MMP->{'sel3'},"petselectname  $MMP->{'Pet4Name'}") if ($MMP->{'Pet4Nameenabled'});
		$ResetFile->SetBind($MMP->{'sel4'},"petselectname  $MMP->{'Pet5Name'}") if ($MMP->{'Pet5Nameenabled'});
		$ResetFile->SetBind($MMP->{'sel5'},"petselectname  $MMP->{'Pet6Name'}") if ($MMP->{'Pet6Nameenabled'});
	}
	my $allfile = $profile->GetBindFile('mmbinds','all.txt');
	my $minfile = $profile->GetBindFile('mmbinds','tier1.txt');
	my $ltsfile = $profile->GetBindFile('mmbinds','tier2.txt');
	my $bosfile = $profile->GetBindFile('mmbinds','tier3.txt');
	my $bgfiledn;
	my $bgfileup;
	if ($MMP->{'bg_enable'}) {
		$bgfiledn = $profile->GetBindFile('mmbinds','bguarda.txt');
		#  since we never need to split lines up in this fashion
		#  comment the next line out so an empty file is not created.
		# bgfileup = $profile->GetBindFile($profile->{'base'} . "\\mmbinds\\bguardb.txt")
	}
	my $callfile = $profile->GetBindFile('mmbinds','call.txt');
	my $cminfile = $profile->GetBindFile('mmbinds','ctier1.txt');
	my $cltsfile = $profile->GetBindFile('mmbinds','ctier2.txt');
	my $cbosfile = $profile->GetBindFile('mmbinds','ctier3.txt');
	my $cbgfiledn;
	my $cbgfileup;
	if ($MMP->{'bg_enable'}) {
		$cbgfiledn = $profile->GetBindFile('mmbinds','cbguarda.txt');
		$cbgfileup = $profile->GetBindFile('mmbinds','cbguardb.txt');
	}
	# TODO!!!  get this into / from GameData
	my $powers = {
		Mercenaries => { min => "sol",  lts => "spec", bos => "com", },
		Ninjas      => { min => "gen",  lts => "joun", bos => "oni", },
		Robotics    => { min => "dron", lts => "prot", bos => "ass", },
		Necromancy  => { min => "zom",  lts => "grav", bos => "lich", },
		Thugs       => { min => "thu",  lts => "enf",  bos => "bru", },
	}->{ $profile->General->{'Primary'} };
	# "Local","Self-Tell","Petsay","None";
	mmSubBind($profile,$ResetFile,"all",undef,$powers);
	mmQuietSubBind($profile,$allfile,"all",undef,$powers);
	mmQuietSubBind($profile,$minfile,"tier1",$powers->{'min'},$powers);
	mmQuietSubBind($profile,$ltsfile,"tier2",$powers->{'lts'},$powers);
	mmQuietSubBind($profile,$bosfile,"tier3",$powers->{'bos'},$powers);
	if ($MMP->{'bg_enable'}) {
		mmQuietBGSubBind($profile,$bgfiledn,$bgfileup,"bguard",$powers);
	}
	mmSubBind($profile,$callfile,"all",undef,$powers);
	mmSubBind($profile,$cminfile,"tier1",$powers->{'min'},$powers);
	mmSubBind($profile,$cltsfile,"tier2",$powers->{'lts'},$powers);
	mmSubBind($profile,$cbosfile,"tier3",$powers->{'bos'},$powers);
	if ($MMP->{'bg_enable'}) {
		mmBGSubBind($profile,$cbgfiledn,$cbgfileup,"bguard",$powers);
	}
}

sub findconflicts {
	my ($profile) = @_;
	my $MMP = $profile->MastermindPets;
	if ($MMP->{'petselenable'}) {
		for my $i (1..6) {
			if ($MMP->{'pet'.$i.'nameenabled'}) {
				cbCheckConflict($MMP,"sel".($i-1),"Select Pet ".$i)
			}
		}
	}
	cbCheckConflict($MMP,"PetSelectAll","Select All Pets");
	cbCheckConflict($MMP,"PetSelectMinions","Select Minions");
	cbCheckConflict($MMP,"PetSelectLieutenants","Select Lieutenants");
	cbCheckConflict($MMP,"PetSelectBoss","Select Boss Pet");
	cbCheckConflict($MMP,"PetAggressive","Set Pets Aggressive");
	cbCheckConflict($MMP,"PetDefensive","Set Pets Defensive");
	cbCheckConflict($MMP,"PetPassive","Set Pets Passive");
	cbCheckConflict($MMP,"PetAttack","Pet Order: Attack");
	cbCheckConflict($MMP,"PetFollow","Pet Order: Follow");
	cbCheckConflict($MMP,"PetStay","Pet Order: Stay");
	cbCheckConflict($MMP,"PetGoto","Pet Order: Goto");
	cbCheckConflict($MMP,"chattykey","Pet Action Bind Chatty Mode Toggle");
	if ($MMP->{'bg_enable'}) {
		cbCheckConflict($MMP,"selbgm","Bodyguard Mode");
		if ($MMP->{'PetBackgroundAttackenabled'})  { cbCheckConflict($MMP,"PetBackgroundAttack","Pet Order: BG Attack"); }
		if ($MMP->{'PetBackgroundGotoenabled'}) { cbCheckConflict($MMP,"PetBackgroundGoto","Pet Order: BG Goto"); }
	}
}

sub bindisused { shift->MastermindPets->{'Enable'} }


sub petCommandKeyDefinitions {
	(
		{
			label      => 'Select All',
			basename      => 'PetSelectAll',
			tooltipdetail => 'select all of your pets',
		},
		{
			label      => 'Select Minions',
			basename      => 'PetSelectMinions',
			tooltipdetail => 'select your "minion" pets',
		},
		{
			label      => 'Select Lieutenants',
			basename      => 'PetSelectLieutenants',
			tooltipdetail => 'select your "lieutenant" pets',
		},
		{
			label      => 'Select Boss',
			basename      => 'PetSelectBoss',
			tooltipdetail => 'select your "boss" pet',
		},
		{
			label      => 'Bodyguard',
			basename      => 'PetBodyguard',
			tooltipdetail => 'put your selected pets into Bodyguard mode',
		},
		{
			label      => 'Aggressive',
			basename      => 'PetAggressive',
			tooltipdetail => 'set your selected pets to "Aggressive" mode',
		},
		{
			label      => 'Defensive',
			basename      => 'PetDefensive',
			tooltipdetail => 'set your selected pets to "Defensive" mode',
		},
		{
			label      => 'Passive',
			basename      => 'PetPassive',
			tooltipdetail => 'set your selected pets to "Passive" mode',
		},
		{
			label      => 'Attack',
			basename      => 'PetAttack',
			tooltipdetail => 'order your selected pets to Attack your target',
		},
		{
			label      => 'Follow',
			basename      => 'PetFollow',
			tooltipdetail => 'order your selected pets to Follow you',
		},
		{
			label      => 'Stay',
			basename      => 'PetStay',
			tooltipdetail => 'order your selected pets to Stay at their current location',
		},
		{
			label      => 'Go To',
			basename      => 'PetGoto',
			tooltipdetail => 'order your selected pets to Go To a targeted location',
		},
	);
}

1;
