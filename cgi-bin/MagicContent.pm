#!E:/Program Files/perl/bin/perl.exe
###############################################################################
#	MagicContent.pm
#------------------------------------------------------------------------------
#	Generated content for Wiki pages, requested by the page text itself
#	Syntax in wiki pages:
#	#MAGIC ModuleName param1=value1 param2=value2 ...
{
	package MagicContentMaker;
 
	our @registered;
	
	sub register {
		# borrowed from Mych's Wookee.pm - thanks Mych :-)
		# fills the @registered array with the names of the packages
 
		my $class = shift;	$class = (ref $class or $class);
 
		push @registered, $class
			unless grep /^\Q$class\E$/, @registered;
	}
	sub GenerateContent	{ '' }
	sub CommandParameters { () }
	sub ListParameters {
		my $class = shift;
		my $text;
		my @parameters = $class->CommandParameters;
		
		return '' if scalar @parameters == 0;
		
		$text .= "\n<h6>Parameters for this command</h6>";
		$text .= "\n<ul class='disabled'>";
		$text .= join '', map { "\n<li>$_</li>" } @parameters ;
		$text .= "\n</ul>";
		
		return $text;
	}
 
	# call this from UseModWiki
	sub MakeSection {
		my $class			= shift;
		my $page			= shift; # the page being browsed
		my $magicmodule = shift; # the requested magicmodule	
		my %params = map { s/^"|"$//g; $_ } (shift =~ m[(\w+)\s*=\s*("[^"]*"?|\S+)]g); #"
		
		$params{'thispage'} = $page; # add the page to the parameters hash
		
		foreach ( values %params ) {
			# escape HTML. keys are fine since grabbed as "\w+"
			s[&][&]g;
			s[<][<]g;
		}
		
		my $text;
		
		# ... make an opener
		$text .= qq[<div class="magic" id="$magicmodule">\n];
		if( grep /^\Q$magicmodule\E$/ , @registered ){
			# if one of our packages matches the name of the wiki page, run the script
			$text .= $magicmodule->GenerateContent(%params);
			$text .= $magicmodule->ListParameters;
		}
		else {
			# ...or complain
			$magicmodule =~ s[&][&]g;
			$magicmodule =~ s[<][<]g;
			$text .= qq[#MAGIC module "<b>$magicmodule</b>" cannot be found. 
			Use "#MAGIC ListCommands" to see available modules.];
		}
		
		# ... make a closer
		$text .= qq[</div>\n];
		
		return $text;
	}
}
 
###############################################################################
# command: Foobar
#------------------------------------------------------------------------------
# this is just a template
{
	package Foobar;
	@ISA = qw(MagicContentMaker);
	Foobar->register();
#------------------------------------------------------------------------------
	sub CommandParameters { () } 
		# auto-documentation: list the params this module requires here.
		# safe to delete if no parameters
	###########################
		
	sub GenerateContent {
		my ( $class, %params ) = @_;
		# put the script for the page here
		# access parameters thus: $params{'threshold'}
		# page being browsed is:	$params{'thispage'}
		return "Generating... FooBar<br/>";	
	}
 }
###############################################################################
# command: Discuss
#------------------------------------------------------------------------------
# ASSUMES that wiki engine code will present link to Discuss page.
# ASSUMES that $DiscussDir is defined; usually /wiki/discuss-data
# REQUIRES $DiscussDir/OpenPageName to exist.
#------------------------------------------------------------------------------
# #MAGIC Discuss
{
	package Discuss;	
	@ISA = qw(MagicContentMaker);
	Discuss->register();
	my ( $class, %params ) = @_;
#------------------------------------------------------------------------------
	sub CommandParameters { } 	
	sub GenerateContent {
		my ( $class, %params ) = @_;
		my ( $text, $fpath, $pageId, $directory, $folder, $file, $comments, $targetFile, $entryCount, $errorMessage);

		# GATHER options
		##my $isNumbered = $params{'numbered'};
		##my $isThumbed = $params{'numbered'};
		##my $isThreaded = $params{'threaded'};
		##my $feedbackClass = $params{'class'};
						
		# SETUP variables
		my $ext = "\.df";
		my $delimItem = $UseModWiki::FS1;
		my $delimEntry = $UseModWiki::FS3;
			
		$fpath = $UseModWiki::DiscussDir;
		$pageId = $UseModWiki::OpenPageName;
		$directory = uc(substr($pageId, 0, 1));
		$folder = &UseModWiki::ExtractFolder($pageId);
		$file = &UseModWiki::ExtractName($pageId);
		
		if ($pageId =~ /\//){ $pageId =~ tr/\//\./; }
		else { $file = ""; }
		
		unless (uc($UseModWiki::q->param('post')) =~ /preview/ig){
			unless (lc($params{'locked'})){ 
				$errorMessage = &AppendComment($fpath, $directory, $folder, $pageId, $ext); 
			}
		}
		
		$targetFile = "$fpath/$directory/$folder/$pageId$ext";		
		if ( -f $targetFile ) {
			local $/ = undef;      # Read complete files
			open( INFILE, "<$targetFile" ) or die "Can't find file [ $targetFile ] $!";
			$comments = <INFILE>;
			close INFILE;
		}
		
		my @entries = split ($delimEntry, $comments);
		my $numEntries = scalar(@entries);
		
		$text .= "\n<div id='feedback'><span class='title'>$numEntries Comments</span>";
		if (lc($params{'locked'})){ $text .= "\n<br/><i>This comments section is locked until further notice.</i><br/><br/>"; }
		else { $text .= "&nbsp;&nbsp;<a href='#feedbackForm' title='Click to jump to feedback form.'>[ form ]</a><br/>"; }
		
		foreach my $entry (@entries){
			$entryCount++;
			my @items = split ($delimItem, $entry);
			$text .= &ShowResults($items[0], $items[1], $items[2], $items[3], $entryCount, $numEntries, "");		
		}
		
		unless ($params{'locked'}){
			if (uc($UseModWiki::q->param('post')) =~ /preview/ig){ 
				my ($errorMessage, $result) = &ShowPreview($numEntries);
				
				if ($result){ $text .= $result; }
				$text .= &ShowForm($errorMessage);
			}
			else { $text .= &ShowForm($errorMessage); }	
		}
		
		$text .= "\n</div>";
		
		return $text;
	}
	
	sub AppendComment {		
		my ($fpath, $directory, $folder, $pageId, $ext) = @_;

		unless ($UseModWiki::q->param('tokenId')){ return ""; }
		unless (&UseModWiki::CheckTokenList($UseModWiki::DiscussDir)){ return ""; }
			
		my ($errorMessage, $commentBy, $commentTitle, $commentDateTime, $commentText) = &GetFeedbackEntry();

		if ($errorMessage){ return $errorMessage; }        
        if ($commentTitle eq "" || $commentText eq ""){ return ""; }      

		my $delimItem = $UseModWiki::FS1;
		my $delimEntry = $UseModWiki::FS3;		
		my $string = $commentBy . $delimItem . $commentTitle . $delimItem . $commentDateTime .  $delimItem . $commentText . $delimEntry;
		my $targetFile = "$fpath/$directory/$folder/$pageId$ext";	
						
		&UseModWiki::CreateDir("$fpath/$directory");
		&UseModWiki::CreateDir("$fpath/$directory/$folder");
		
		&UseModWiki::RequestLock() or die( "Could not get maintain-lock" );
		open( OUT, ">>$targetFile" ) or die( "Can't write to file $!" );
		print OUT $string;
		close(OUT);
		&UseModWiki::ReleaseLock();
			
		return "";
	}

	sub GetFeedbackEntry {
		my ($maxBy, $maxTitle, $maxText);
		
		$maxBy = 64;
		$maxTitle = 200;
		$maxText = 4000;
		
		my $errorMessage = "";
		my $action = lc($UseModWiki::q->param('action'));
		my $commentBy = $UseModWiki::q->param('commentby');
		my $commentTitle = $UseModWiki::q->param('commentTitle');
		my $commentText = $UseModWiki::q->param('commenttext');
		my $commentDateTime = $UseModWiki::Now;
		
		if ($commentTitle eq "" && $commentText eq ""){ $errorMessage = ""; }
		elsif ($action ne 'discuss'){ $errorMessage = "The action parameter [ $action ] is not valid for the Feedback append process."; }		
		elsif ($commentBy eq ""){ $errorMessage = "The author ID provided is not valid"; }
		elsif ($commentTitle eq ""){ $commentTitle = "$commentBy";  }
		elsif ($commentText eq ""){ $errorMessage = "The feedback comment text provided is not valid."; }		
		
		if (length($commentBy) > $maxBy){ $commentBy = substr ($commentBy, 0, $maxBy); $errorMessage = "Truncated author name to $maxBy characters."; }
		if (length($commentTitle) > $maxTitle){ $commentTitle = substr ($commentTitle, 0, $maxTitle); $errorMessage = "Truncated title to $maxTitle characters."; }
		if (length($commentText) > $maxText){ $commentText = substr ($commentText, 0, $maxText); $errorMessage = "Truncated comment text to $maxText characters."; }
		
		return ($errorMessage, $commentBy, $commentTitle, $commentDateTime, $commentText);
	}
	
	sub ShowForm {
		my ( $commentBy, $commentTitle, $commentDateTime, $commentText );
		my ( $text, $username, $isPriviledged, $pageId, $homePage, $date, $tokenId, $showForm, $scriptName );
		my ( $errorMessage ) = @_;	
		my ($maxBy, $maxTitle, $maxText);
		
		$maxBy = 64;
		$maxTitle = 200;
		$maxText = 4000;
			
		
		$scriptName = $UseModWiki::scriptName;
		$tokenId = $UseModWiki::Now;
		$pageId = $UseModWiki::OpenPageName;
		$username = $UseModWiki::UserData{'username'};
		$isPriviledged = &UseModWiki::UserIsEditorOrAdmin();
		$homePage = "$UseModWiki::HomePagePrefix$username";
		
		if ($username){ if ($isPriviledged){ $showForm = 1; }}
						
		$text .= "\n<!--- FEEDBACK FORM //-->";
		$text .= "\n<form id='feedbackForm' name='feedbackForm' method='post' class='wikiform feedbackForm' action='$scriptName?$pageId#lastEntry'>";
		$text .= "\n<h3>Provide Feedback</h3>";
		
		if ($showForm){
				$text .= "\n<div class='info'>";
				$text .= "Use BBCode for mark-up.";
				$text .= "All fields are required.  Limited to $maxText characters per message entry. ";
				$text .= "Visit the <a href='$scriptName?BulletinBoardCode' title='Click to get help' target='_blank'><u>BBCode</u></a> page for help.";
				$text .= "</div>";
		}
		
		if ($errorMessage){ $text .= "<p class='warning'>$errorMessage</p>"; }		
		if (uc($UseModWiki::q->param('post')) =~ /preview/ig || $errorMessage){
			($errorMessage, $commentBy, $commentTitle, $commentDateTime, $commentText) = &GetFeedbackEntry();
		}
		
		unless ($showForm){
			$text .= "\n<i>You must be signed in to add a comment. Use the <a class='wikilinkorurl' href='?action=editprefs' title='Click to set your preferences'>Preferences</a> link to set your username. </a></i>";
		}
		if ($showForm){		
			$text .= "\n<br/><b>Title</b> &nbsp;[ required ]";
			$text .= "\n<input type='text' name='commentTitle' value='$commentTitle' class='wide'/>";
			$text .= "\n<br/><br/><b>Message from [ $username ]</b>:";
			$text .= "\n<br/><div class='outline'><textarea name='commenttext' id='commentText' class='wide' style='width: 100%;' wrap='virtual' cols='80' rows='20'>$commentText</textarea></div>";
			$text .= "\n<br/><p align='right'>";
			$text .= "\n<input type='hidden' name='commentby' value='$username'/>";
			$text .= "\n<input type='hidden' name='tokenId' value='$tokenId'/>";
			$text .= "\n<input type='hidden' name='id' value='$pageId'/>";
			$text .= "\n<input type='hidden' name='action' value='discuss'/>";
			$text .= "\n<input type='hidden' name='magic' value='solo'/>";
			$text .= "\n<input type='text' id='showcount' value='0' class='showHand floatleft' title='Number of characters.  Limit is $maxText.' readonly='readonly'/>";	
			$text .= "\n<input type='submit' name='post' value='Preview' title='Click to preview this comment'/>";	
			$text .= "\n<input type='submit' name='post' value='Submit Comment' title='Click to post this comment'/>";			
		}
		
		$text .= "\n</p>";
		$text .= "\n</form>";	
	
		return $text;	
	}
	
	sub ShowPreview {
		my ($numEntries) = @_;		
		my ($errorMessage, $commentBy, $commentTitle, $commentDateTime, $commentText) = &GetFeedbackEntry();

		if ($errorMessage){ return $errorMessage; }        
        if ($commentTitle eq "" || $commentText eq ""){ return ""; }   
		
		my $text = &ShowResults($commentBy, $commentTitle, $commentDateTime, $commentText, $numEntries + 1, $numEntries + 1, "preview");

		return ("", $text);			
	}
		
	sub ShowResults {
		my ($commentBy, $commentTitle, $commentDateTime, $commentText, $entryNum, $numEntries, $isPreview) = @_;
		my ($username, $homePage, $oddEntry, $authorEntry, $localDateTime, $commentId, $text);
		
		$commentId = "comment$entryNum";
		$username = $UseModWiki::UserData{'username'};
		$homePage = "$UseModWiki::HomePagePrefix$username";
		$authorEntry = ($username eq $commentBy) ? "-author" : "";
		$oddEntry = $entryNum % 2 ? "-odd" : "-even";
		
		$localDateTime = &UseModWiki::TimeToText($commentDateTime);
		$commentTitle = &UseModWiki::StripHTML($commentTitle);
		$commentText = &UseModWiki::GetBBCode($commentText);
				
		$text .= "\n<!--- FEEDBACK RESULT //-->";			
		$text .= "\n<div id='$commentId' class='feedbackComment$authorEntry$oddEntry'>";
		
		if ($numEntries == $entryNum){ $text .= "\n<a name='lastEntry'></a>"; }
		if ($isPreview){ $text .= "\n<div class='$isPreview'>[ preview ]<br/>";	}		
		$text .= "\n	<div class='commentId'><div class='commentNumber'>$entryNum</div></div>";
		
					
		$text .= "\n	<div class='commentText'>";
		$text .= "\n		<div class='commentTitle'>$commentTitle</div>";	
		$text .= "\n		<p>$commentText</p>";	
		$text .= "\n	</div>";
		$text .= "\n	<div class='commentDateTime'>Posted on <a href='\#$commentId' title='Click to view linkback URL for bookmarking.'>$localDateTime</a>";
		$text .= "\n		<span class='commentBy'> by <a href='?$homePage$commentBy' target='_blank' title='Click to visit this page.'>$commentBy</a>&nbsp;</span>";
		$text .= "\n		</div><div class='clearright'>";	
		$text .= "\n	</div>";	
		
		if ($isPreview){ $text .= "\n</div>"; }
		
		$text .= "\n</div>";
		
		return $text;
	}
}
###############################################################################
# command: Flash
#------------------------------------------------------------------------------
# ASSUMES UFO.js loaded
# ASSUMES GetFlash.png in /img/ufodirectory
# ASSUMES .ufoFlash has been defined in the wiki.css
# REQUIRES JavaScript is enabled in the browser
#------------------------------------------------------------------------------
# #MAGIC Flash name=ufo.swf height=300 width=300
{
	package Flash;	
	@ISA = qw(MagicContentMaker);
	Flash->register();
	my ( $class, %params ) = @_;	
#------------------------------------------------------------------------------
	sub CommandParameters { } 	
	sub GenerateContent {
		my ( $class, %params ) = @_;	
		my $text = "";				
		# put the script for the page here
		# access parameters thus: $params{'threshold'}
		# page being browsed is:	$params{'thispage'}	

		my $fpath = "$UseModWiki::UploadUrl/";
		my $defaultSWF = 'ufo.swf';
			
		my $fname;
		my $fwidth;
		my $fheight;
		my $idDiv = "ufoDivmagic";
		my $idFO = "FOmagic";

		if ($params{'name'}){ $fname = $params{'name'}; } else { $fname = $defaultSWF; }
		if ($params{'width'}){ $fwidth = $params{'width'}; } else { $fwidth = 400; }
		if ($params{'height'}){ $fheight = $params{'height'}; } else { $fheight = 300; }
				
		unless (-e "$UseModWiki::UploadDir/$fname"){ $fname = $defaultSWF; }
		
		$text .= "\n<div id='$idDiv' class='ufoFlash'>";
		$text .= "\n	<script type='text/javascript'>";
		$text .= "\n		var enlarged = false;";		
		$text .= "\n		var fpath = '$fpath';";
		$text .= "\n		var fname = '$fname';";
		$text .= "\n		var fwidth = $fwidth;";
		$text .= "\n		var fheight = $fheight;";
		$text .= "\n		var enlargedHeight = Math.ceil((800/$fwidth) * $fheight);";	
		$text .= "\n		var $idFO = { 'movie': fpath + fname, 'width':fwidth, 'height':fheight, 'majorversion':'8', 'build':'0', 'xi':'true', 'id': '$idFO' };";
		$text .= "\n		\$(window).load(function () {";
		$text .= "\n			UFO.create($idFO, '$idDiv');";					
		$text .= "\n			document.getElementById('$idDiv').style.width = fwidth;";
		$text .= "\n			document.getElementById('$idDiv').style.height= fheight;";
		$text .= "\n		});";
		$text .= "\n";
		$text .= "\n		function resizeFlash(){";
		$text .= "\n			if (enlarged){;";
		$text .= "\n				enlarged = false;";					
		$text .= "\n				document.getElementById('$idFO').style.width = fwidth;";
		$text .= "\n				document.getElementById('$idFO').style.height= fheight;";
		$text .= "\n				document.getElementById('$idDiv').style.width = fwidth;";
		$text .= "\n				document.getElementById('$idDiv').style.height= fheight;";
		$text .= "\n			}";
		$text .= "\n			else {";
		$text .= "\n				enlarged = true;";	
		$text .= "\n				document.getElementById('$idFO').style.width = 800;";
		$text .= "\n				document.getElementById('$idFO').style.height= enlargedHeight;";
		$text .= "\n				document.getElementById('$idDiv').style.width = 800;";
		$text .= "\n				document.getElementById('$idDiv').style.height= enlargedHeight;";
		$text .= "\n			}";
		$text .= "\n		}";
		$text .= "\n	</script>";		
		$text .= "\n	<p style='margin-top: 0px;'>[ <i><b>$fname</b></i> ]<br> is unavailable for viewing.	Please enable JavaScript and/or download the latest <a href='http://www.macromedia.com/go/getflashplayer'>Flash Player</a>.</p>";
		$text .= "\n	<p><a href='http://www.macromedia.com/go/getflashplayer'><img src='http://wiki.kurcina.org/plugins/ufo/img/get_flash_player.gif' alt='Get macromedia Flash Player' style='border: none; float: right; margin-right:10px;' /></a></p>";
		$text .= "\n	<p style='clear: both;'></p>";
		$text .= "\n</div>";
		$text .= "\n<a onclick='resizeFlash();' title='Click to resize'><img src='/plugins/ufo/img/icon.expand.gif'></a>";	

		return $text;	
	}
}
 
###############################################################################
# command: Params
#------------------------------------------------------------------------------
# this lists all the parameters the page has passed to the command, just for testing
{
	package Params;
	@ISA = qw(MagicContentMaker);
	Params->register();
#------------------------------------------------------------------------------
	sub GenerateContent {
		my ( $class, %params ) = @_;
		my $text;
		
		$text .= '<h4>Parameters</h4><dl>';
		
		while (($key, $value) = each %params) {
			$text .= qq[<dt><b>$key</b> = $value</dt>];
		}
		$text .= '</dl>';
		
		return $text;	
	}
}
###############################################################################
# command: ListCommands
#------------------------------------------------------------------------------
# this returns all the available commands in this perl module
{
	package ListCommands;
	@ISA = qw(MagicContentMaker);
	ListCommands->register();
#------------------------------------------------------------------------------
	sub GenerateContent {
		my ( $class, %params ) = @_;
		my $text;
		
		$text .= '<h4>Commands</h4><ul>';
		$text .= join '', map { "<li>$_</li>" } @MagicContentMaker::registered;
		$text .= '</ul>';
		
		return $text;	
	}
}
###############################################################################
# command: AllPages
#------------------------------------------------------------------------------
# lists all the pages of the wiki
{
	package AllPages;
	@ISA = qw(MagicContentMaker);
	AllPages->register();
#------------------------------------------------------------------------------
	sub CommandParameters {'list = ol|ul'}	
	sub GenerateContent {
		my ( $class, %params ) = @_;
		my $text;
		my $listTag = $params{'list'};
		
		$listTag = 'ul' unless defined $params{list};
		
		if( $listTag !~ m/^(ul|ol)$/i ){ 
			$listTag = 'ul';
			$text .= qq[parameter "$params{'list'}" not recognized, defaulting to OL.];
		}
		
		$text .= "\n<h4>List of all pages on this wiki:</h4><$listTag>";
		$text .= join '', map { '<li>' . UseModWiki::GetPageLink($_) . '</li>' } UseModWiki::AllPagesList();
		$text .= "</$listTag>";
		
		return $text;	
	}
}

###############################################################################
# command: WantedPages
#------------------------------------------------------------------------------
# lists wanted pages. refactored & better UseMod call
{
	package WantedPages;
	@ISA = qw(MagicContentMaker);
	WantedPages->register();
#------------------------------------------------------------------------------
	sub CommandParameters {'threshold = 0,1,2 ... : show only pages with more than this number of requests.' }
	sub SortItems {
		my ( $a , $b , $numA , $numB ) = @_; 
	}
	sub GenerateContent {
		my ( $class, %params ) = @_;
		my ($text, @links);
		
		$params{threshold} = 0 unless defined $params{threshold};
		
		if( $params{'threshold'} !~ /^\d+$/ ) {
			return q[Invalid value in parameter 'threshold'.];
		}
		
		# grab the list of links from UseModWiki::GetFullLinkList which spits out an array
		# on the way, kill any items which are just one pagename: ie pages that make no requests
		@links = grep { !/^\w+\s*$/ } UseModWiki::GetFullLinkList(1,1,1,0,0,0,0,'',1);

		#reset currently open page, so the referrer is correct in the edit links made below
		$UseModWiki::OpenPageName = $params{'thispage'};
		
		#------------------------------------------------------------------------------
		# Data extraction
		# what we have so far: multiple lines like:
		# {Existing page} {list of wanted link plain text}\n
		#------------------------------------------------------------------------------
		my %requesters; # hash of arrays to store who wants the pages
		
		foreach (@links) {
			# we are chomping through each line at a time
			
			my $head;
			s[^(\S+)\s*]{
			 $head = $1;
			 '';
			 }eg; # strip link tags and put the head name somewhere else
			# now $_ is the list of links wanted by page $head	
			
			while( m[(\S+)\s*]g ) {
			 push @{ $requesters{$1} }, $head;
			}
		}	 
		# now we have a hash of arrays. Keys are wanted pages, value is array of requesters
		#------------------------------------------------------------------------------
		# Data output
		#------------------------------------------------------------------------------
		my $wantedpage;
		my $rowNum;
		my $thresholdmessage = ( $params{'threshold'} == 0 ) ? '' : 'May be further pages. ';
		
		# sort { SortList( $a, $b, @{$requesters{$a}}, @{$requesters{$b}} } ( grep ... )
		
		$text  = "";
		$text .= "\n<div style='_width: 90%;'>";
   		$text .= "\n<h2>Wanted Pages found:</h2>";
   		$text .= "\n<table id='tablesorter-998' class='wikilargelist tablesorter'>";
    	$text .= "\n<thead><tr><th>#</th><th>Page Name</th><th>Requests</th><th>Requested By</th></tr></thead>";
   		$text .= "\n<tbody>";
   		
		foreach $wantedpage 
			(sort { @{$requesters{$b}} <=> @{$requesters{$a}}	|| $a cmp $b }
			(grep { @{$requesters{$_}} > $params{'threshold'} } keys %requesters ) ) {

			#------------------------------------------------------------------------------
			# run through the hash keys
			# BUT sort them by size of the associated array, 
			# AND only let through the arrays > threshold parameter
			#------------------------------------------------------------------------------
			
			$rowNum++;
	        $text .= "\n<tr><td>$rowNum</td>";
	        $text .= "\n<td class='first'>" . &UseModWiki::GetPageOrEditLink($wantedpage, $wantedpage) . "</td>";
	        $text .= "\n<td>" . @{$requesters{$wantedpage}} . "</td>";
	        $text .= "\n<td>" . join(', ', map {UseModWiki::GetPageLink($_)} @{$requesters{$wantedpage}} ) ."</tr>\n";
        
		}
				
		$text .= "\n</tbody></table>";
		$text .= "\n</div>";
		$text .= $thresholdmessage;
		$text .= "Threshold is $params{'threshold'}";
		
		$text .= "\n<script>\$(document).ready(function(){ \$('\#tablesorter\-998').tablesorter({widgets: ['zebra']}); });<\/script>";
		
		return $text;
	}
 }
 
###############################################################################
 1;