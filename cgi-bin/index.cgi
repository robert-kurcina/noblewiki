#!E:/Program Files/perl/bin/perl.exe
#==============================================================================
# NobleWiki version 1.0.0 (2008.10.03)
#     Copyright (C) 2008 Robert Kurcina <kitrok@yahoo.com>
#------------------------------------------------------------------------------
# Based on the UseModWiki version 1.0.4 (December 1, 2007)
#     Copyright (C) 2000-2003 Clifford A. Adams  <caadams@usemod.com>
#     Copyright (C) 2002-2003 Sunir Shah  <sunir@sunir.org>
#
# ...which was based on
#    the GPLed AtisWiki 0.3  (C) 1998 Markus Denker
#    <marcus@ira.uka.de>
#
# ...which was based on
#    the LGPLed CVWiki CVS-patches (C) 1997 Peter Merel
#    and The Original WikiWikiWeb  (C) Ward Cunningham
#        <ward@c2.com> (code reused with permission)
#------------------------------------------------------------------------------
# Email and ThinLine options by Jim Mahoney <mahoney@marlboro.edu>
#------------------------------------------------------------------------------
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
#    Free Software Foundation, Inc.
#    59 Temple Place, Suite 330
#    Boston, MA 02111-1307 USA
#==============================================================================

use Diff;
use MagicContent;
use Image::Size;

package UseModWiki;
use strict;
local $| = 1;    # Do not buffer output (localized for mod_perl)

#------------------------------------------------------------------------------
# Global variables:
#------------------------------------------------------------------------------
use vars qw(@RcDays @HtmlPairs @HtmlSingle @WikiFarmNames
  $TempDir $LockDir $DataDir $HtmlDir $UserDir $KeepDir $PageDir
  $InterFile $RcFile $RcOldFile $IndexFile $FullUrl $SiteName $HomePage
  $LogoUrl $RcDefault $IndentLimit $RecentTop $EditAllowed $UseDiff
  $UseSubpage $UseCache $RawHtml $SimpleLinks $NonEnglish
  $KeepDays $HtmlTags $HtmlLinks $UseDiffLog $KeepMajor $KeepAuthor
  $FreeUpper $EmailNotify $SendMail $EmailFrom $FastGlob $EmbedWiki
  $ScriptTZ $BracketText $UseAmPm $UseConfig $UseIndex $UseLookup
  $RedirType $AdminPass $EditPass $UseHeadings $NetworkFile $BracketWiki
  $FreeLinks $WikiLinks $AdminDelete $FreeLinkPattern $RCName $RunCGI
  $ShowEdits $ThinLine $LinkPattern $InterLinkPattern $InterSitePattern
  $UrlProtocols $UrlPattern $ImageExtensions $RFCPattern $ISBNPattern
  $FS $FS1 $FS2 $FS3 $CookieName $SiteBase $StyleSheet $NotFoundPage
  $FooterNote $EditNote $MaxPostSizeKB $NewText $NotifyDefault $HttpCharset
  $UserGotoBar $DeletedPage $AllowReplaceFiles @ReplaceableFiles $TableSyntax
  $MetaKeywords $NamedAnchors $InterWikiMoniker $SiteDescription $RssLogoUrl
  $NumberDates $EarlyRules $LateRules $NewFS $KeepSize $SlashLinks $BGColor
  $UpperFirst $AdminBar $RepInterMap $DiffColor1 $DiffColor2 $ConfirmDel
  $MaskHosts $LockCrash $ConfigFile $HistoryEdit $OldThinLine
  @IsbnNames @IsbnPre @IsbnPost $EmailFile $FavIcon $RssDays $UserHeader
  $UserBody $StartUID $ParseParas $AuthorFooter $UseUpload $AllUpload
  $UploadDir $UploadUrl $LimitFileUrl $MaintTrimRc $SearchButton $UserPagePrefix
  $EditNameLink @ImageSites $BracketImg $DisabledDir $DeletedDir $ReplaceDir
  $AllowInclusion $InclusionDir $NumberDatesDelim
);

#------------------------------------------------------------------------------
# Other global variables:
#------------------------------------------------------------------------------  
use vars qw(%Page %Section %Text %InterSite %SaveUrl %SaveNumUrl
  %KeptRevisions %UserCookie %SetCookie %UserData %IndexHash %Translate
  %LinkIndex $InterSiteInit $SaveUrlIndex $SaveNumUrlIndex $MainPage
  $OpenPageName @KeptList @IndexList $IndexInit $TableMode
  $q $Now $UserID $TimeZoneOffset $ScriptName $BrowseCode $OtherCode
  $AnchoredLinkPattern @HeadingNumbers $TableOfContents $QuotedFullUrl
  $ConfigError $UploadPattern $WikiLineHeader $WikiLineHeaderPreview $WikiLineFooter $WikiLineDiff
  $WikiLine $WikiLine1 $WikiLine2 $WikiLinePref $AutoMailto $SiteUrl $NewTable $UserFooter
  $WikiLeftNav %TableCellDefaults $DownloadExtensions $DocsDir $CssDir $HomeDir $ImageDir $CGIBIN $Windows
  
  $DiscussDir $CurrentUserName $HelpPage $InfoPage $ContactUsPage $SandBoxPage
  $CategoriesPage $FeaturedPage $NotesSuffix $UseNotesPages $AuthErrorPage
  %SaveNumHeadings
  $GLOBAL_footnoteCounter $FootNotes @Footnotes %SaveNumFootnote
  $GLOBAL_imageCount $GLOBAL_flashCount $GLOBAL_galleryCount $GLOBAL_tableCount
  $GLOBAL_codeboxCount $GLOBAL_sectionCount
);

#==============================================================================
# BEGIN CONFIGURATION
#------------------------------------------------------------------------------
$HomeDir          = "F:/ASSETS - Development/export/www/http/content/wiki.kurcina.org";
$CGIBIN           = $HomeDir . "/cgi-bin";              # Main directory for wiki perl script and associated perl modules
$DataDir          = $HomeDir . "/data";                 # Main directory for storing pages and other wiki generated information
$DocsDir          = $HomeDir . "/docs";                 # Main directory for browser-accessible assets like images, javascript, and CSS files
$CssDir           = $DocsDir . "/css";                  # Location of CSS files required by the wiki engine
$ImageDir         = $DocsDir . "/img";                  # Location of images files required by the wiki engine
$UploadDir        = $DocsDir . "/attachments";          # Location of uploaded files

$SiteUrl          = "http://wiki.kurcina.org";          # Used for access to /img, /js, /css, and /attachments directories; set this if the auto-detected URL is wrong
$FullUrl          = $SiteUrl . "/cgi-bin/index.cgi";    # Full URL (like http://foo.com/uploads)
$UploadUrl        = $SiteUrl . "/attachments";          # Full path (like /foo/www/uploads) for files     


#------------------------------------------------------------------------------
# Global configurations
#------------------------------------------------------------------------------
@WikiFarmNames    = ();                                 # List of all WikiFarms to be created; will create $DataDir/<farm name>/
$UseConfig        = 0;                                  # 1 = use config file,    0 = do not look for config
$ConfigFile       = "$DataDir/config";                  # Configuration file location; if using WikiFarms will look inside $DataDir/<farm name>/config

$ENV{PATH}        = "/usr/bin/";                        # Path used to find "diff"
$SendMail         = "/usr/sbin/sendmail";               # Full path to sendmail executable
$AutoMailto       = 1;                                  # 0 = off; 1 = convert email address automatically to mailTo:<address>
$HttpCharset      = "UTF-8";                            # Charset for pages, like "iso-8859-2"
$CookieName       = "NobleWiki";                        # Name for this wiki; WikiFarms will append their instance name as in NobleWiki.<farm name>
@RcDays           = qw(1 3 7 30 90 180 365);            # Days for links on RecentChanges
$RcDefault        = 30;                                 # Default number of RecentChanges days
$RssDays          = 7;                                  # Default number of days in RSS feed
$KeepDays         = 365;                                # Days to keep old revisions
$KeepSize         = 0;                                  # If non-zero, maximum size of keep file
$ScriptTZ         = "PST";                              # Local time zone ("" means do not print)                       
$Windows          = 1;                                  # 0 = No; probably *NIX, 1 = Yes; this is a Microsoft Windows deployment
$MaxPostSizeKB    = 1024 * 5000;                        # Maximum page size and file-upload posts (~200K for pages) 
$RedirType        = 1;                                  # 1 = CGI.pm, 2 = script, 3 = no redirect
$StartUID         = 1001;                               # Starting number for user IDs

@ImageSites       = qw();                               # URL prefixes of good image sites: () if left empty allows all sites
@HtmlSingle       = qw(br);      						# Single tags (that do not require a closing /tag).
@HtmlPairs        =                                     # HTML tag lists, enabled if $HtmlTags is set. . Tags that must be in <tag> ... </tag> pairs:
	qw(
	b i u big small sub em s strike strong tt
	sup h1 h2 h3 h4 h5 h6 code
	blockquote caption cite 
);
@HtmlPairs        = ( @HtmlPairs, @HtmlSingle );        # All singles can also be pairs

@IsbnNames        = (                                   # Names of sites.  (The first entry is used for the number link.)
	'bn.com', 'amazon.com', 'search' 
);      
@IsbnPre          = (                                   # Full URL of each site before the ISBN
    "http://search.barnesandnoble.com/booksearch/isbninquiry.asp?isbn=",
    "http://www.amazon.com/exec/obidos/ISBN=",
    "http://www.pricescan.com/books/BookDetail.asp?isbn="
);
@IsbnPost         = ( "", "", "" );                     # Rest of URL of each site after the ISBN (usually '')


#------------------------------------------------------------------------------
# BEGIN WikiFarm site configurations
#------------------------------------------------------------------------------
$SiteName         = "Noble Pursuit Games Wiki";         # Name of site (used for titles)
$SiteDescription  = $SiteName;                          # Description of this wiki. (for RSS)
$SiteBase         = "";                                 # Full URL for <BASE> tag to be used in all page headers 
$InterWikiMoniker = "NobleWiki";                        # InterWiki moniker for this wiki. (for RSS)
$EmailFrom        = "Noble Wiki";                       # Text for "From: " field of email notes.

$RssLogoUrl       = "";                                 # URL for optional site logo used as image for RSS feed
$LogoUrl          = "";                                 # URL for site logo ("" for no logo) that will be added to the left of each page title
$FavIcon          = "";                                 # URL of bookmark/favorites icon, or ''
$StyleSheet       = "/css/wiki/default.css";            # URL for CSS stylesheet (like "/wiki/default.css")

$HomePage         = "HomePage";                         # Name of Home page
$UserPagePrefix   = "UserNexus/";                       # Which page will be linked when a valid $username is clicked in the RC history; end with slash if using Sub pages
$RCName           = "RecentChanges";                    # Name of changes page ("" to remove from menu)
$HelpPage         = "Help";                             # Name of Help page ("" to remove from menu)
$InfoPage         = "About";                            # Name of About page ("" to remove from menu)
$CategoriesPage   = "CategoryCategory";                 # Name of Index page ("" to remove from menu)
$FeaturedPage     = "Featured";                         # Name of Featured content page ("" to remove from menu)
$SandBoxPage      = "SandBox";                          # Name of SandBox page ("" to remove from menu)
$ContactUsPage    = "WikiContacts";                     # Name of Contacts page ("" to remove from menu)
$NotFoundPage     = "PageNotFound";                     # Page for not-found links ("" for blank page)
$AuthErrorPage    = "AuthError";						# Page for not-found links ("" for blank page)
$DeletedPage      = "WikiDelete";                       # 0 = disable, 'PageName' = tag to delete page

$NotesSuffix      = "_Notes";                           # Name of suffix for notes page ("" to remove from menu; also set $UseNotesPages to 0)
$AdminPass        = "linhson";                          # Set to non-blank to enable password(s)
$EditPass         = "emerald";                          # Like AdminPass, but for editing only

@ReplaceableFiles = ();                                 # List of allowed server files to replace via {{replace:/path/to/file/system/item}}

#------------------------------------------------------------------------------
# WikiFarm rendered HTML page modifications
#------------------------------------------------------------------------------
$EditNote         = "";                                 # HTML notice above buttons on edit page      
$NewText          = "[Describe the new page here]";     # New page text ("" for default message)


$EarlyRules       = "";                                 # Local syntax rules for wiki->html (evaled)
$LateRules        = "";                                 # Local syntax rules for wiki->html (evaled)

$UserGotoBar      = "";                                 # HTML added to end of goto bar
$UserGotoBar     .= "";

$UserHeader       = "";                                 # Optional HTML header additional content
$UserHeader      .= "\n<link type='text/css' rel='stylesheet' media='print' href='/css/printer.friendly.css'/>";
$UserHeader      .= "\n<link type='text/css' rel='stylesheet' media='screen' href='/plugins/jquery/lightbox/lightbox.css'/>";
$UserHeader      .= "\n<link type='text/css' rel='stylesheet' media='screen' href='/plugins/markitup/skins/markitup/style.css' />";
#$UserHeader      .= "\n<link type='text/css' rel='stylesheet' media='screen' href='/plugins/markitup/sets/default/style.css' />";
#$UserHeader      .= "\n<link type='text/css' rel='stylesheet' media='screen' href='/plugins/markitup/sets/wiki/style.css' />";
$UserHeader      .= "\n<link type='text/css' rel='stylesheet' media='screen' href='/plugins/markitup/sets/bbcode/style.css' />";

$UserHeader      .= "\n<script type='text/javascript' src='/plugins/jquery/jquery.js'></script>";
$UserHeader      .= "\n<script type='text/javascript' src='/plugins/jquery/lightbox/lightbox.js'></script>";
$UserHeader      .= "\n<script type='text/javascript' src='/plugins/jquery/tablesorter/tablesorter.js'></script>";
$UserHeader      .= "\n<script type='text/javascript' src='/plugins/codepress/codepress.js'></script>";
$UserHeader      .= "\n<script type='text/javascript' src='/plugins/markitup/jquery.markitup.js'></script>";
$UserHeader      .= "\n<script type='text/javascript' src='/plugins/markitup/sets/default/set.js'></script>";
$UserHeader      .= "\n<script type='text/javascript' src='/plugins/markitup/sets/wiki/set.js'></script>";
$UserHeader      .= "\n<script type='text/javascript' src='/plugins/markitup/sets/bbcode/set.js'></script>";
$UserHeader      .= "\n<script type='text/javascript' src='/plugins/ufo/ufo.js'></script>";
$UserHeader      .= "\n<script type='text/javascript' src='/js/wiki/NPG.js'></script>";

$UserBody         = "";                                 # Optional <BODY> tag additional content
$UserFooter       = "";                                 # Optional HTML or text to append to the end of each rendered footer

$FooterNote       = "";                                 # HTML for bottom of every page
$FooterNote      .= "<a href='?action=editprefs'>";
$FooterNote      .= "<div id='anylogo' title='access username'>&nbsp;</div>";
$FooterNote      .= "</a><div style='clear: both;'></div>";       

#------------------------------------------------------------------------------
# Major options
#------------------------------------------------------------------------------
$UseNotesPages    = 1;								    # 1 = use _Notes pages,   0 = do not use _Notes pages
$UseSubpage       = 1;                                  # 1 = use subpages,       0 = do not use subpages
$UseCache         = 0;                                  # 1 = cache HTML pages,   0 = generate every page
$EditAllowed      = 1;                                  # 1 = editing allowed,    0 = read-only
$RawHtml          = 0;                                  # 1 = allow <HTML> tag,   0 = no raw HTML in pages
$HtmlTags         = 1;                                  # 1 = "unsafe" HTML tags, 0 = only minimal tags
$UseDiff          = 1;                                  # 1 = use diff features,  0 = do not use diff
$FreeLinks        = 1;                                  # 1 = use [[word]] links, 0 = LinkPattern only
$WikiLinks        = 1;                                  # 1 = use LinkPattern,    0 = use [[word]] only
$AdminDelete      = 1;                                  # 1 = Admin only deletes, 0 = Editor can delete
$RunCGI           = 1;                                  # 1 = Run script as CGI,  0 = Load but do not run
$EmailNotify      = 1;                                  # 1 = use email notices,  0 = no email on changes
$EmbedWiki        = 0;                                  # 1 = no headers/footers, 0 = normal wiki pages
$TableSyntax      = 1;                                  # 1 = wiki syntax tables, 0 = no table syntax
$NewFS            = 1;                                  # 1 = new multibyte $FS,  0 = old $FS
$UseUpload        = 1;                                  # 1 = allow uploads,      0 = no uploads
$AllowInclusion   = 1;                                  # 1 = files (*.txt,*.html) may be included by {{include:$InclusionDir/somefile.html}}, 0 = files will not be included
$AllowReplaceFiles= 0;                                  # 1 = system files may be over-written by content of pages using {{replace:/filesystem/path/somefile}}, 0 = files will not be replaced


#------------------------------------------------------------------------------
# Minor options
#------------------------------------------------------------------------------
$RecentTop        = 1;                                  # 1 = recent on top,      0 = recent on bottom
$UseDiffLog       = 1;                                  # 1 = save diffs to log,  0 = do not save diffs
$KeepMajor        = 1;                                  # 1 = keep major rev,     0 = expire all revisions
$KeepAuthor       = 1;                                  # 1 = keep author rev,    0 = expire all revisions
$ShowEdits        = 0;                                  # 1 = show minor edits,   0 = hide edits by default
$HtmlLinks        = 1;                                  # 1 = allow A HREF links, 0 = no raw HTML links
$SimpleLinks      = 0;                                  # 1 = only letters,       0 = allow _ and numbers
$NonEnglish       = 0;                                  # 1 = extra link chars,   0 = only A-Za-z chars
$ThinLine         = 0;                                  # 1 = fancy <hr> tags,    0 = classic wiki <hr>
$BracketText      = 1;                                  # 1 = allow [URL text],   0 = no link descriptions
$UseAmPm          = 0;                                  # 1 = use am/pm in times, 0 = use 24-hour times
$UseIndex         = 0;                                  # 1 = use index file,     0 = slow/reliable method
$UseHeadings      = 1;                                  # 1 = allow = h1 text =,  0 = no header formatting
$NetworkFile      = 1;                                  # 1 = allow remote file:, 0 = no file:// links
$BracketWiki      = 1;                                  # 1 = [WikiLnk txt] link, 0 = no local descriptions
$UseLookup        = 1;                                  # 1 = lookup host names,  0 = skip lookup (IP only)
$FreeUpper        = 1;                                  # 1 = force upper case,   0 = do not force case
$FastGlob         = 1;                                  # 1 = new faster code,    0 = old compatible code
$MetaKeywords     = 1;                                  # 1 = Google-friendly,    0 = search-engine averse
$NamedAnchors     = 1;                                  # 0 = no anchors, 1 = enable anchors, 2 = enable but suppress display
$SlashLinks       = 0;                                  # 1 = use script/action links, 0 = script?action
$UpperFirst       = 1;                                  # 1 = free links start uppercase, 0 = no ucfirst
$AdminBar         = 1;                                  # 1 = admins see admin links, 0 = no admin bar
$RepInterMap      = 0;                                  # 1 = intermap is replacable, 0 = not replacable
$ConfirmDel       = 1;                                  # 1 = delete link confirm page, 0 = immediate delete
$MaskHosts        = 0;                                  # 1 = mask hosts/IPs,      0 = no masking
$LockCrash        = 0;                                  # 1 = crash if lock stuck, 0 = auto clear locks
$HistoryEdit      = 0;                                  # 1 = edit links on history page, 0 = no edit links
$OldThinLine      = 0;                                  # 1 = old ==== thick line, 0 = ------ for thick line
$NumberDates      = 1;                                  # 1 = 2003-6-17 dates,     0 = June 17, 2003 dates
$NumberDatesDelim = ".";                                # 1 = this character separates the values for year, month, day
$ParseParas       = 1;                                  # 1 = new paragraph markup, 0 = old markup
$AuthorFooter     = 1;                                  # 1 = show last author in footer, 0 = do not show
$AllUpload        = 0;                                  # 1 = anyone can upload,   0 = only editor/admins
$LimitFileUrl     = 1;                                  # 1 = limited use of file: URLs, 0 = no limits
$MaintTrimRc      = 1;                                  # 1 = maintain action trims RC, 0 = only maintainrc
$SearchButton     = 1;                                  # 1 = search button on page, 0 = old behavior
$EditNameLink     = 0;                                  # 1 = edit links use name (CSS), 0 = '?' links
$BracketImg       = 1;                                  # 1 = [url url.gif] becomes image link, 0 = no img

#------------------------------------------------------------------------------
# END WikiFarm site configurations
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Various horizontal rules for delimiting visual blocks of content
#------------------------------------------------------------------------------
$WikiLineHeader   = "\n<div class='wikilineheader'></div>";
$WikiLineHeaderPreview = "\n<div class='wikilineheaderpreview'></div>";
$WikiLineFooter   = "\n<div class='wikilinefooter'></div>";
$WikiLineDiff     = "\n<div class='wikilinediff'></div>";
$WikiLinePref     = "\n<div class='wikilinepref'></div>";
$WikiLine         = "\n<div class='wikiline'>&nbsp;</div>";
$WikiLine1        = "\n<div class='wikiline1'></div>";
$WikiLine2        = "\n<div class='wikiline2'></div>";
$BGColor          = "";                                 # Background color ('' to disable)
$DiffColor1       = "#ffffaf";                          # Background color of old/deleted text
$DiffColor2       = "#cfffcf";                          # Background color of new/added text

#------------------------------------------------------------------------------
# You should not have to change anything below this line.
#==============================================================================
$IndentLimit      = 20;                                 # Maximum depth of nested lists
$TempDir          = "$DataDir/temp-files";              # Temporary files and locks
$LockDir          = "$TempDir/lock-dir";                # DB is locked if this exists
$HtmlDir          = "$DataDir/html-version";            # Stores HTML versions
$PageDir          = "$DataDir/page-data";               # Stores page data
$UserDir          = "$DataDir/user-data";               # Stores user data
$KeepDir          = "$DataDir/keep-data";               # Stores kept (old) page data
$DiscussDir       = "$DataDir/discuss-data";            # Stores discussions for a page
$InclusionDir     = "$DataDir/includes-data";           # Store HTML fragments here for inclusion into a Wiki page via {{include}} directive 
$ReplaceDir       = "$DataDir/replace-data";            # Store HTML fragments here for replace entire Wiki pages via {{replace}} directive 
$DisabledDir      = "$DataDir/disabled-assets";         # Stores disabled uploads; assets can be re-enabled
$DeletedDir       = "$DataDir/deleted-assets";          # Stores deleted disabled assets; will clear out once each week.
$RcFile           = "$DataDir/recent-log";              # New RecentChanges logfile
$RcOldFile        = "$DataDir/oldrecent-log";           # Old RecentChanges logfile
$IndexFile        = "$DataDir/page-index";              # List of all pages
$EmailFile        = "$DataDir/email-list";              # Email notification lists
$InterFile        = "$DataDir/intermap";                # Interwiki site->url map

#------------------------------------------------------------------------------
# END CONFIGURATION
#------------------------------------------------------------------------------

if ($RepInterMap) { push @ReplaceableFiles, $InterFile; }

#==============================================================================
# The "main" program, called at the end of this script file.
#------------------------------------------------------------------------------
sub DoWikiRequest {
    if ( $UseConfig && ( -f $ConfigFile ) ) {
        $ConfigError = "";
        
        if ( !do $ConfigFile ) {               # Some error occurred
            $ConfigError = $@;
            if ( $ConfigError eq "" ) {

              # Unfortunately, if the last expr returns 0, one will get a false
              # error above.  To remain compatible with existing installs the
              # wiki must not report an error unless there is error text in $@.
              # (Errors in "use strict" may not have error text.)
              # Uncomment the line below if you want to catch use strict errors.
              #       $ConfigError = "Unknown Error (no error text)";
            }
        }
    }
    
    &InitLinkPatterns();
    
    if ( !&DoCacheBrowse() ) {
        eval $BrowseCode;
        &InitRequest() or return;
        
        if ( !&DoBrowseRequest() ) {
            eval $OtherCode;
            &DoOtherRequest();
        }
    }
}

#------------------------------------------------------------------------------
# Common and cache-browsing code
#------------------------------------------------------------------------------
sub InitLinkPatterns {
    my ( $UpperLetter, $LowerLetter, $AnyLetter, $LpA, $LpB, $QDelim );

    # Field separators are used in the URL-style patterns below.
    if ($NewFS) {
        $FS = "\x1e\xff\xfe\x1e";    # An unlikely sequence for any charset
    }
    else {
        $FS = "\xb3";                # The FS character is a superscript "3"
    }
    
    $FS1         = $FS . "1";  # The FS values are used to separate fields
    $FS2         = $FS . "2";  # in stored hashtables and other data structures.
    $FS3         = $FS . "3";  # The FS character is not allowed in user data.
    
    $UpperLetter = "[A-Z";
    $LowerLetter = "[a-z";
    $AnyLetter   = "[A-Za-z";
    
    if ($NonEnglish) {
        $UpperLetter .= "\xc0-\xde";
        $LowerLetter .= "\xdf-\xff";
        
        if ($NewFS) { $AnyLetter .= "\x80-\xff"; }
        else { $AnyLetter .= "\xc0-\xff"; }
    }
    
    if ( !$SimpleLinks ) { 
        $LowerLetter .= "_";
        $AnyLetter .= "_0-9"; 
    }
    
    $UpperLetter .= "]";
    $LowerLetter .= "]";
    $AnyLetter   .= "]";

    # Main link pattern: lowercase between uppercase, then anything
    $LpA = $UpperLetter . "+" . $LowerLetter . "+" . $UpperLetter . $AnyLetter . "*";

    # Optional subpage link pattern: uppercase, lowercase, then anything
    $LpB = $UpperLetter . "+" . $LowerLetter . "+" . $AnyLetter . "*";
    
    if ($UseSubpage) {
        # Loose pattern: If subpage is used, subpage may be simple name
        $LinkPattern = "((?:(?:$LpA)?\\/$LpB)|$LpA)";

        # Strict pattern: both sides must be the main LinkPattern
        #$LinkPattern = "((?:(?:$LpA)?\\/)?$LpA)";
    }
    else {
        $LinkPattern = "($LpA)";
    }
    
    $QDelim = '(?:"")?';    # Optional quote delimiter (not in output)
    $AnchoredLinkPattern = $LinkPattern . '#(\\w+)' . $QDelim if $NamedAnchors;
    $LinkPattern .= $QDelim;

    # Inter-site convention: sites must start with uppercase letter
    # (Uppercase letter avoids confusion with URLs)
    $InterSitePattern = $UpperLetter . $AnyLetter . "+";
    $InterLinkPattern = "((?:$InterSitePattern:[^\\]\\s\"<>$FS]+)$QDelim)";
    
    if ($FreeLinks) {

        # Note: the - character must be first in $AnyLetter definition
        if ($NonEnglish) {
            if ($NewFS) {
                $AnyLetter = "[-,.()' _0-9A-Za-z\x80-\xff]";
            }
            else {
                $AnyLetter = "[-,.()' _0-9A-Za-z\xc0-\xff]";
            }
        }
        else {
            $AnyLetter = "[-,.()' _0-9A-Za-z]";
        }
    }
    $FreeLinkPattern = "($AnyLetter+";
    
    if ($UseSubpage) {
        $FreeLinkPattern = "((?:(?:$AnyLetter+)?\\/)?$AnyLetter+";
    }
    
    if ($NamedAnchors){
        $FreeLinkPattern .= "(?:#(?:\\w+))?)";
    }
    else {
        $FreeLinkPattern .= ")";
    }
    
    $FreeLinkPattern .= $QDelim;

    # Url-style links are delimited by one of:
    #   1.  Whitespace                           (kept in output)
    #   2.  Left or right angle-bracket (< or >) (kept in output)
    #   3.  Right square-bracket (])             (kept in output)
    #   4.  A single double-quote (")            (kept in output)
    #   5.  A $FS (field separator) character    (kept in output)
    #   6.  A double double-quote ("")           (removed from output)
    $UrlProtocols    = "http|https|ftp|afs|news|nntp|mid|cid|mailto|wais|prospero|telnet|gopher";
    $UrlProtocols   .= '|file' if ( $NetworkFile || !$LimitFileUrl );
    
    $UrlPattern      = "((?:(?:$UrlProtocols):[^\\]\\s\"<>$FS]+)$QDelim)";
    $ImageExtensions = "(gif|jpg|png|bmp|jpeg|ico|tiff)";
    $DownloadExtensions = "(pdf|psd|ai|xls|xml|ppt|js|css|doc|txt|swf|fla|fh9|fh11|blend|java|zip)";
    $RFCPattern      = "RFC\\s?(\\d+)";
    $ISBNPattern     = "ISBN:?([0-9- xX]{10,})";
    $UploadPattern   = "upload:([^\\]\\s\"<>$FS]+)$QDelim";
}

#------------------------------------------------------------------------------
# Simple HTML cache
#------------------------------------------------------------------------------
sub DoCacheBrowse {
    my ( $query, $idFile, $text );
    
    return 0 if ( !$UseCache );
    $query = $ENV{'QUERY_STRING'};
    
    if ( ( $query eq "" ) && ( $ENV{'REQUEST_METHOD'} eq "GET" ) ) {
        $query = $HomePage;    # Allow caching of home page.
    }
    
    if ( !( $query =~ /^$LinkPattern$/ ) ) {
        if ( !( $FreeLinks && ( $query =~ /^$FreeLinkPattern$/ ) ) ) {
            return 0;          # Only use cache for simple links
        }
    }
    
    $idFile = &GetHtmlCacheFile($query);
    if ( -f $idFile ) {
        local $/ = undef;      # Read complete files
        
        open( INFILE, "<$idFile" ) or return 0;
        $text = <INFILE>;
        close INFILE;
        
        print $text;
        
        return 1;
    }
    
    return 0;
}

sub GetHtmlCacheFile {
    my ($id) = @_;
    return $HtmlDir . "/" . &GetPageDirectory($id) . "/$id.htm";
}

sub GetPageDirectory {
    my ($id) = @_;
    
    if ( $id =~ /^([a-zA-Z])/ ) {
        return uc($1);
    }
    
    return "other";
}

sub T {
    my ($text) = @_;
    
    if (defined($Translate{$text}) && ($Translate{$text} ne ''))  {
        return $Translate{$text};
    }
    
    return $text;
}

sub Ts {
    my ($text, $string, $noquote) = @_;
    
    $string = &QuoteHtml($string) unless $noquote;
    $text = T($text);
    $text =~ s/\%s/$string/;
    
    return $text;
}

sub Tss {
    my $text = $_[0];
    my @args = @_;
    
    @args = map { $_ = &QuoteHtml($_); } @args;
    $text = T($text);
    $text =~ s/\%([1-9])/$args[$1]/ge;
    
    return $text;
}

#------------------------------------------------------------------------------
# Normal page-browsing and RecentChanges code
#------------------------------------------------------------------------------
$BrowseCode = "";    # Comment next line to always compile (slower)
#$BrowseCode = <<'# END_OF_BROWSE_CODE';

#------------------------------------------------------------------------------
use CGI;
use CGI::Carp qw(fatalsToBrowser);

sub InitRequest {
    my @ScriptPath = split( '/', "$ENV{SCRIPT_NAME}" );
    $CGI::POST_MAX = $MaxPostSizeKB;
    
    if ($UseUpload) { $CGI::DISABLE_UPLOADS = 0; }   # allow uploads    
    else { $CGI::DISABLE_UPLOADS = 1; }   # no uploads    
    
    if ($SlashLinks && length($ENV{'PATH_INFO'}>1)){
        $ENV{'QUERY_STRING'} .= '&' if($ENV{'QUERY_STRING'});
        $ENV{'QUERY_STRING'} .= substr($ENV{'PATH_INFO'},1);
    }
        
    $q = new CGI();
    
    if ($SlashLinks){
        my $numberOfSlashes = ($ENV{'PATH_INFO'} = tr[/][/]);
        $ScriptName = ('../' x $numberOfSlashes) . $ScriptName;
    }

    # Fix some issues with editing UTF8 pages (if charset specified)
    if ( $HttpCharset ne "" ) {
        $q->charset($HttpCharset);
    }
    
    $Now           = time;                # Reset in case script is persistent
    $ScriptName    = pop(@ScriptPath);    # Name used in links
    $IndexInit     = 0;                   # Must be reset for each request
    $InterSiteInit = 0;
    %InterSite     = ();
    $MainPage     = ".";    # For subpages only, the name of the top-level page
    $OpenPageName = "";     # Currently open page
    
    &CreateDir($DataDir);   # Create directory if it doesn't exist

    if ( !-d $DataDir ) {
        &ReportError( "Could not create $DataDir : $!" );
        return 0;
    }
    
    &InitCookie();          # Reads in user data
    
    return 1;
}

sub InitCookie {
    %SetCookie      = ();
    $TimeZoneOffset = 0;
    
    undef $q->{'.cookies'};    # Clear cache if it exists (for SpeedyCGI)
    
    %UserData   = ();                        # Fix for persistent environments.
    %UserCookie = $q->cookie($CookieName);
    $UserID     = $UserCookie{'id'};
    $UserID =~ s/\D//g;                      # Numeric only
    
    if ( $UserID < 200 ) { $UserID = 111; }
    else { &LoadUserData($UserID); }
    
    if ( $UserID > 199 ) {
        if (( $UserData{'id'} != $UserCookie{'id'}) || ($UserData{'randkey'} != $UserCookie{'randkey'})) {
            # Invalid.  Consider warning message.
            $UserID   = 113;
            %UserData = ();    
        }
    }
    
    if ( $UserData{'tzoffset'} != 0 ) { $TimeZoneOffset = $UserData{'tzoffset'} * ( 60 * 60 ); }
}

sub DoBrowseRequest {
    my ( $id, $action, $text );
    
    if ( !$q->param ) { &BrowsePage($HomePage); return 1; } # No parameter
        $id = &GetParam( 'keywords', "" );
    
    if ($id) {                 
        # Just script?PageName
        if ( $FreeLinks && ( !-f &GetPageFile($id) )) { $id = &FreeToNormal($id); }
        if (( $NotFoundPage  ne "" ) && ( !-f &GetPageFile($id) )) { 
			$id = $NotFoundPage;
		}
		
        &BrowsePage($id) if &ValidIdOrDie($id);
        
        return 1;
    }
    
    $action = lc( &GetParam( 'action', "" ) );
    $id = &GetParam( 'id', "" );

    if ( $action eq 'browse' || $action eq 'discuss') {
        
        if ( $FreeLinks && ( !-f &GetPageFile($id) )) { $id = &FreeToNormal($id); }
        if (( $NotFoundPage ne "" ) && ( !-f &GetPageFile($id) )) { 
			$id = $NotFoundPage;
		}
        
        &BrowsePage($id) if &ValidIdOrDie($id);
        
        return 1;
    }
    elsif ( $action eq 'rc'     ) { &BrowsePage($RCName); return 1; }
    elsif ( $action eq 'random' ) { &DoRandom(); return 1; }
    elsif ( $action eq 'orphans') { &DoOrphanList(); return 1; } 
    elsif ( $action eq 'history') { &DoHistory($id) if &ValidIdOrDie($id); return 1; }
	elsif ( $action eq 'editreferer'){ 
		my $referer = $ENV{HTTP_REFERER};
		my @destination = split(/\?/, $referer);
		$destination[1] =~ s/browse/edit/;
		print &GetRedirectPage($destination[1], $id, 1);
	}
    
    return 0;    # Request not handled
}

sub BrowsePage {
    my ($id) = @_;
    my ( $fullHtml, $oldId, $allDiff, $showDiff, $openKept );
    my ( $revision, $goodRevision, $diffRevision, $newText );
    my ( $fragHtml, $diffHtml );    
    
    # GET PAGE contents
    &OpenPage($id);
    &OpenDefaultText();
    
    $openKept = 0;
    $revision = &GetParam( 'revision', "" );
    $revision =~ s/\D//g;    # Remove non-numeric chars
    $goodRevision = $revision;    # Non-blank only if exists
        
    if ( $revision ne "" ) {
        &OpenKeptRevisions('text_default');
        $openKept = 1;
        
        if (!defined( $KeptRevisions{$revision} )) { $goodRevision = ""; }
        else { &OpenKeptRevision($revision); }
    }

    # RAW MODE: just untranslated wiki text
    if ( &GetParam( 'raw', 0 ) ) {
        print &GetHttpHeader('text/plain');
        print $Text{'text'};
        
        return;
    }
    
    # REDIRECT processing of page
    $newText = $Text{'text'};              # For differences                                           
    $oldId   = &GetParam( 'oldid', "" );   # Handle a single-level redirect    
    if (( $oldId eq "" ) && ( substr( $Text{'text'}, 0, 11) eq '{{redirect:' ) )
    {
        $oldId = $id;
        if ( ($FreeLinks) && ( $Text{'text'} =~ /^\s*{{redirect:\s?\[\[.+\]\]}}/ ) ) {
            ($id) = ( $Text{'text'} =~ /^\s*{{redirect:\s?\[\[(.+)\]\]\}}/ );
            $id = &FreeToNormal($id);
        }
        else {
            ($id) = ( $Text{'text'} =~ /^\s*{{redirect:\s?(\S+)}}/ );
        }
        
        if ( &ValidId($id) eq "" ) {
            # Consider revision in rebrowse?
            &ReBrowsePage( $id, $oldId, 0 );
            return;
        }
        else {    # Not a valid target, so continue as normal page
            $id    = $oldId;
            $oldId = "";
        }
    }
	elsif ($Text{'text'} =~ /\s*{{delete}}/ )  {
		&ReBrowsePage($DeletedPage, $id, 0 );
		return;	
	}
    
    # NORMAL processing top of page
    $MainPage = $id;
    $MainPage =~ s|/.*||;    # Only the main page name (remove subpage)    
    $fullHtml = &GetHeader($id, &QuoteHtml($id), $oldId, 1);
    
    unless( $id eq $RCName ){ $fullHtml .= &GetLeftNav(); }
    
    if ( $UseDiff && $showDiff ) {
        $fullHtml .= "\n<div class='wikiadmin'>";
    }
    else {
        unless ($id eq $RCName){ $fullHtml .= "\n<div class='wikitext'>"; }
        else { $fullHtml .= "\n<div class='wikiadmin'>"; }
    }
    
    if ( $revision ne "" ) {
        if ( ( $revision eq $Page{'revision'} ) || ( $goodRevision ne "" ) ) {
            $fragHtml = "\n<div class='wikidifftexttitle'>Showing revision $revision. ";
					
			if ( &UserCanEdit( $id, 0 )) {
				$fragHtml .= &GetOldPageLink( 'edit', $id, $revision, Ts( '[edit]', $revision ) );
			}
			else {
				$fragHtml .= T( '[locked] ');
			}
			$fragHtml .= "</div>";
        }
        else {
            $fragHtml = "\n<div class='wikidifftexttitle'>Revision $revision not available, showing current revision instead.</div>";
        }
    }
    $fullHtml .= $fragHtml;    
    
    # REVISIONED content processing    
    $allDiff = &GetParam( 'alldiff', 0 );
    if ( $allDiff != 0 ) { $allDiff = &GetParam( 'defaultdiff', 1 ); }
    
    if (
        (
            ( $id eq $RCName ) || ( $RCName eq $id ) || ( $id eq $RCName )
        )
        && &GetParam( 'norcdiff', 1 )
      )
    {
        $allDiff = 0;    # Only show if specifically requested
    }
    
    $showDiff = &GetParam( 'diff', $allDiff );
    
    if ( $UseDiff && $showDiff ) {
        $diffRevision = $goodRevision;
        $diffRevision = &GetParam( 'diffrevision', $diffRevision );

        # Eventually try to avoid the following keep-loading if possible?
        &OpenKeptRevisions('text_default') if ( !$openKept );
        $diffHtml .= &GetDiffHTML( $showDiff, $id, $diffRevision, $revision, $newText );
        $diffHtml .= $fragHtml;
    }

    # GET MagicContent [ tarquin ]
    # Refactored and added position functionality --DavidClaughton.
    my ($magiccommand, $magicpos, $magicparams, $checkParm);
    my ($magicHTML, $wikiHTML, $noMagic);    

    # DON'T DISPLAY if this is a revision page view
    if ($q->param('diffrevision')){ $noMagic = 1; }
    if ($q->param('revision')){ $noMagic = 1; }
    if ($q->param('diff')){ $noMagic = 1; }
    
    if ( ($magicpos, $magiccommand, $magicparams) = $Text{'text'} =~ m[^\s*{{magic:\s?(?:\@(top|bottom|solo|check))?\s*(\w*)\s*(.*)}}] ){
        if ($noMagic){
            $fullHtml .= $diffHtml . &WikiToHTML($Text{'text'});
        }
        else {
            $Text{'text'} =~ s/^\s*{{magic:\s?.*\}}//; # kill the magic command line in source
            $wikiHTML = &WikiToHTML($Text{'text'});
                
            # call: MakeSection( current page, magic module, line of parameters)
            $magicpos = lc $magicpos;
            $magicHTML .= (MagicContentMaker->MakeSection( $id, $magiccommand, $magicparams ) || "");
            
            if ($magicpos eq "check"){ 
                $checkParm = $q->param('magic');
                
                if ($checkParm =~ /(top|bottom|solo)/){ $magicpos = $checkParm; }
                if ($magicpos eq "solo"){ $fullHtml .= $magicHTML; }
                elsif ($magicpos eq "top"){ $fullHtml .= $diffHtml . $magicHTML . $wikiHTML; }
                elsif ($magicpos eq "bottom"){ $fullHtml .= $diffHtml . $wikiHTML . $magicHTML; }
                else { $fullHtml .= $diffHtml . &WikiToHTML($Text{'text'}); }
            }
            else {                
                if ($magicpos eq "solo"){ $fullHtml .= $magicHTML; }
                elsif ($magicpos eq "top"){ $fullHtml .= $diffHtml . $magicHTML . $wikiHTML; }
                else { $fullHtml .= $diffHtml . $wikiHTML . $magicHTML; }
            }
        }        
    }
    else {
        $fullHtml .= $diffHtml . &WikiToHTML($Text{'text'});
    }
	
    $fullHtml .= &GetFooterReferences();	
    $fullHtml .= "</div>";

    # RECENT CHANGES processing
    if ( ( $id eq $RCName ) || ( $RCName eq $id ) || ( $id eq $RCName ) ){
        print $fullHtml;
        print $WikiLineDiff;
        print &GetLeftNav();
        print "\n<div class='wikidiff'>";
        &DoRc(1);
        print "\n</div>";        
        print &GetFooterText( $id, $goodRevision );
        print "\n</div></div></div></div></body></html>";
        
        return;
    }    

    # FOOTER section
    $fullHtml .= &GetFooterText( $id, $goodRevision );
    $fullHtml .= &InsertTableSorter();
    $fullHtml .= "</div></div></div></div></body></html>";    

    print $fullHtml;
    
    return
    
    if ( $showDiff || ( $revision ne "" ) );    # Don't cache special version
    &UpdateHtmlCache( $id, $fullHtml ) if ( $UseCache && ( $oldId eq "" ) );
}

sub ReBrowsePage {
    my ( $id, $oldId, $isEdit ) = @_;
    
    if ( $oldId ne "" ) {    
        # Target of {{redirect:NNNN}} (loop breaking safety code)
        print &GetRedirectPage( "action=browse&id=$id&oldid=$oldId", $id, $isEdit );
    }
    else {
        print &GetRedirectPage( $id, $id, $isEdit );
    }
}

sub DoRc {
    my ($rcType) = @_;       # 0 = RSS, 1 = HTML
    my ( $fileData, $rcline, $i, $daysago, $lastTs, $ts, $idOnly, $userid, $authorLink );
    my ( @fullrc, $status, $oldFileData, $firstTs, $errorText, $showHTML, $showUserId, $title );
	
    my $starttime = 0;
    my $showbar   = 0;
	
	$userid 	= GetParam( "userid", "" );
	$starttime 	= &GetParam( "from", 0 );
    $daysago 	= &GetParam( "days", 0 );
    $daysago 	= &GetParam( "rcdays", 0 ) if ( $daysago == 0 );
	$title 		= "Updates since " . &TimeToText($starttime);
	
	if ($daysago) { $starttime = $Now - ( ( 24 * 60 * 60 ) * $daysago ); }			
    if ( 0 == $rcType ) { $showHTML = 0; }
    else { $showHTML = 1; }

	if ($userid eq ""){
		$title = Ts( 'Updates in the last %s day' . ( ( $daysago != 1 ) ? "s" : "" ), $daysago );
	}
	else {
		$authorLink = $userid;
		$showUserId = "&userid=$userid";

		if (-f &GetPageFile("$UserPagePrefix$userid") ){
			$authorLink = &GetPageLinkText("$UserPagePrefix$userid", $userid);
		}
		
		$title = Ts( 'Updates in the last %s day' . ( ( $daysago != 1 ) ? "s" : "" ), $daysago ) . " by [ $authorLink ]";
	}
			
    if ( $starttime == 0 ) {
        if ( 0 == $rcType ) { $starttime = $Now - ( ( 24 * 60 * 60 ) * $RssDays ); }
        else { $starttime = $Now - ( ( 24 * 60 * 60 ) * $RcDefault ); }
        
         $title =  Ts('Updates in the last %s day'. ( ( $RcDefault != 1 ) ? "s" : "" ),$RcDefault );
    }
	
	if ($showHTML) { 
		print "\n<h2>$title</h2>"; 

		# Note: must have two translations (for "day" and "days")
		# Following comment line is for translation helper script
		# Ts('Updates in the last %s days', '');
	}
	
    # Read rclog data (and oldrclog data if needed)
    ( $status, $fileData ) = &ReadFile($RcFile);
    $errorText = "";
	
    if ( !$status ) {
        # Save error text if needed.
        $errorText = "\n<p><strong>";
        $errorText .= "Could not open $RCName log file";
        $errorText .= ":</strong> $RcFile</p>";
        $errorText .= "Error was ";
        $errorText .= ":<pre>$!</pre><p>";
        $errorText .= "Note: This error is normal if no changes have been made.";
    }
    
    @fullrc = split( /\n/, $fileData );
    $firstTs = 0;
    
    # Only false if no lines in file
    if ( @fullrc > 0 ) { ($firstTs) = split( /$FS3/, $fullrc[0] ); }
    if (( $firstTs == 0 ) || ( $starttime <= $firstTs )) {
        ( $status, $oldFileData ) = &ReadFile($RcOldFile);
        
        if ($status) { @fullrc = split( /\n/, $oldFileData . $fileData ); }
        else {
            if ( $errorText ne "" ) {                
                # could not open either rclog file
                print $errorText;
                print "\n<p><strong>";
                print "\nCould not open old $RCName log file";
                print "\n:</strong> $RcOldFile</p>";
                print "\nError was";
                print "\n:<pre>$!</pre>";
                
                return;
            }
        }
    }
    
    $lastTs = 0;
    
    # Only false if no lines in file
    if ( @fullrc > 0 ) { ($lastTs) = split( /$FS3/, $fullrc[$#fullrc] ); }
    
    $lastTs++  if (($Now - $lastTs) > 5);  # Skip last unless very recent
    $idOnly = &GetParam("rcidonly", "");
    
    if ($idOnly && $showHTML) { print '<b>(' . Ts('for %s only', &ScriptLink($idOnly, &QuoteHtml($idOnly)), 1) . ')</b><br/>'; }    
    if ($showHTML) {
        foreach $i (@RcDays) {
            print "\n | " if $showbar;
            $showbar = 1;
            print &ScriptLinkTitle( "action=rc&days=$i$showUserId", Ts( '%s day' . ( ( $i != 1 ) ? 's' : '' ), $i ), T('click to view updates since') );

            # Note: must have two translations (for "day" and "days") Following comment line is for translation helper script
            # Ts('%s days', '');
        }
        
        print "\n<br/><br/>";
        print &ScriptLinkTitle( "action=rc&from=$lastTs$showUserId", T('List new changes starting from'), T('click to set') );
        print "\n " . &TimeToText($lastTs);
        print "\n<br/><br/>";
    }
    
    $i = 0;
    while ( $i < @fullrc ) {    
        # Optimization: skip old entries quickly
        ($ts) = split( /\W/, $fullrc[$i] );
        if ( $ts >= $starttime ) {
            $i -= 1000 if ( $i > 0 );
            last;
        }
        $i += 1000;
    }
    
    $i -= 1000 if ( ( $i > 0 ) && ( $i >= @fullrc ) );
    for ( ; $i < @fullrc ; $i++ ) {
        ($ts) = split( /\W/, $fullrc[$i] );
        last if ( $ts >= $starttime );
    }
    
    if ( $i == @fullrc && $showHTML ) {
        print "\n<br/><strong>";
        print "\nNo updates since ";
        print &TimeToText($starttime);
        print "\n</strong><br/>";
    }
    else {
        splice( @fullrc, 0, $i );    # Remove items before index $i
        
        # Consider an end-time limit (items older than X)
        if ( 0 == $rcType ) { print &GetRcRss(@fullrc); }
        else { print &GetRcHtml(@fullrc); }
    }
    
    if ($showHTML) {
        print "\n<i>Page generated ";
        print &TimeToText($Now);
        print "\n</i><br/>";
    }
}

sub GetRc {
    my $rcType = shift;
    my @outrc  = @_;
    my ( $rcline,   $date, $newtop, $author, $inlist,   $result, $userid );
    my ( $showedit, $link, $all,    $idOnly, $headItem, $item );
    my ( $ts, $pagename, $summary, $isEdit, $host, $kind, $extraTemp );
    my ( $rcchangehist, $tEdit, $tChanges, $tDiff );
    my ( $headList, $pagePrefix, $historyPrefix, $diffPrefix);
    my %extra      = ();
    my %changetime = ();
    my %pagecount  = ();

    # Slice minor edits
    $showedit = &GetParam( "rcshowedit", $ShowEdits );
    $showedit = &GetParam( "showedit",   $showedit );
    
    if ( $showedit != 1 ) {
        my @temprc = ();
        
        foreach $rcline (@outrc) {
            ( $ts, $pagename, $summary, $isEdit, $host ) = split( /$FS3/, $rcline );
            
            if ( $showedit == 0 ) {    # 0 = No edits
                push( @temprc, $rcline ) if ( !$isEdit );
            }
            else {                     # 2 = Only edits
                push( @temprc, $rcline ) if ($isEdit);
            }
        }
        @outrc = @temprc;
    }

    # Optimize param fetches out of main loop
    $rcchangehist = &GetParam( "rcchangehist", 1 );

    # Optimize translations out of main loop
    $tEdit         = "(edit)";
    $tDiff         = "(diff)";
    $tChanges      = "changes";
    
    $pagePrefix = $QuotedFullUrl . &ScriptLinkChar();
    $diffPrefix = $pagePrefix . &QuoteHtml("action=browse&diff=4&id=");
    $historyPrefix = $pagePrefix . &QuoteHtml("action=history&id=");

    foreach $rcline (@outrc) {
        ( $ts, $pagename ) = split( /$FS3/, $rcline );
        $pagecount{$pagename}++;
        $changetime{$pagename} = $ts;
    }
    
    $date     = "";
	$userid   = &GetParam( "userid", "" );
    $all      = &GetParam( "rcall", 0 );
    $all      = &GetParam( "all", $all );
    $newtop   = &GetParam( "rcnewtop", $RecentTop );
    $newtop   = &GetParam( "newtop", $newtop );
    $idOnly   = &GetParam( "rcidonly", "" );
    $inlist   = 0;
    $headList = "";
    $result = "\n<div class='wikirc'>";
    @outrc    = reverse @outrc if ($newtop);


    foreach $rcline (@outrc) {
        ( $ts, $pagename, $summary, $isEdit, $host, $kind, $extraTemp ) = split( /$FS3/, $rcline );
        
        next if ( ( !$all ) && ( $ts < $changetime{$pagename} ) );
        next if ( ( $idOnly ne "" ) && ( $idOnly ne $pagename ) );		
		        
        %extra = split( /$FS2/, $extraTemp, -1 );

		if ($userid ne ""){ next unless ( $extra{'name'} eq $userid); }
        
        if ( $date ne &CalcDay($ts) ) {
            $date = &CalcDay($ts);
            
            if ( 1 == $rcType ) {    # HTML
                                     # add date, properly closing lists first
                if ($inlist) {
                    $result .= "</ul>";
                    $inlist = 0;
                }
                
                $result .= "\n<h6>" . $date . "</h6>";
                
                if ( !$inlist ) {
                    $result .= "\n<ul>";
                    $inlist = 1;
                }
            }
        }

        if ( 0 == $rcType ) {        # RSS
            ( $headItem, $item ) = &GetRssRcLine(
                $pagename,          $ts,
                $host,              $extra{'name'},
                $extra{'id'},       $summary,
                $isEdit,            $pagecount{$pagename},
                $extra{'revision'}, $diffPrefix, $historyPrefix, $pagePrefix
            );
            
            $headList .= $headItem;
            $result   .= $item;
        }
        else {                       # HTML
            $result .= &GetHtmlRcLine(
                $pagename,          $ts,
                $host,              $extra{'name'},
                $extra{'id'},       $summary,
                $isEdit,            $pagecount{$pagename},
                $extra{'revision'}, $tEdit,
                $tDiff,             $tChanges,
                $all,               $rcchangehist
            );
        }
    }
    
    if ( 1 == $rcType ) {
        $result .= "</ul>" if ($inlist);    # Close final tag
    }
    
	$result .= "\n</div>";
    return ( $headList, $result );            # Just ignore headList for HTML
}

sub GetRcHtml {
    my ( $html, $extra );
    
    ( $extra, $html ) = &GetRc( 1, @_ );
    
    return $html;
}

sub GetHtmlRcLine {
    my (
        $pagename, $timestamp, $host,      $userName, $userID,
        $summary,  $isEdit,    $pagecount, $revision, $tEdit,
        $tDiff,    $tChanges,  $all,       $rcchangehist
      )
      = @_;
      
    my ( $author, $sum, $edit, $count, $link, $html );
    
    $html = "";
    $host = &QuoteHtml($host);
    
    if ( defined($userName) && defined($userID) ) { $author = &GetAuthorLink( $host, $userName, $userID ); }
    else { $author = &GetAuthorLink( $host, "", 0 ); }
    
    $sum = "";
    
    if ( ( $summary ne "" ) && ( $summary ne "*" ) ) {
        $summary = &QuoteHtml($summary);
        $sum     = "$summary ";
    }
    
    $edit  = "";
    $edit  = "<em>$tEdit</em> " if ($isEdit);
    $count = "";
        
    if ( ( !$all ) && ( $pagecount > 1 ) ) {
        $count = "($pagecount ";
        
        if ($rcchangehist) { $count .= &GetHistoryLink( $pagename, $tChanges, "click to view revision history" ); }
        else { $count .= $tChanges; }
        
        $count .= ") ";
    }
    
    $link = "<i>" . &CalcTime($timestamp) . "</i>";
    if ( $UseDiff && &GetParam( "diffrclink", 1 ) ) { $link .= "&nbsp;" . &ScriptLinkDiff( 4, $pagename, $tDiff, "" ) . "&nbsp;"; }
    
    $link .= "<b>" . &GetPageLink($pagename) . "</b>";
    $html .= "\n<li>$link $count$edit &rarr; ";
    $html .= "<i>$author</i>";
	
	if ($userName ne "" && &GetParam ("userid", "") eq ""){		
		$html .= &ScriptLinkTitle("action=rc&days=999&userid=$userName", " (contrib)", Ts('View all contributions by this user'));
	}
	
	if ($sum ne ""){ $html .= ". . . . . . . . . . $sum"; }

		
    return $html;
}

sub GetRcRss {
  my ($rssHeader, $headList, $items);

  # Normally get URL from script, but allow override
  $FullUrl = $q->url(-full=>1)  if ($FullUrl eq "");
  $QuotedFullUrl = &QuoteHtml($FullUrl);
  $SiteDescription = &QuoteHtml($SiteDescription);

  my $ChannelAbout = &QuoteHtml($FullUrl . &ScriptLinkChar()
                                . $ENV{QUERY_STRING});
  $rssHeader = <<RSS ;
<?xml version="1.0" encoding="$HttpCharset"?>
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns="http://purl.org/rss/1.0/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wiki="http://purl.org/rss/1.0/modules/wiki/"
>
    <channel rdf:about="$ChannelAbout">
        <title>${\(&QuoteHtml($SiteName))}</title>
        <link>${\($QuotedFullUrl . &ScriptLinkChar() . &QuoteHtml("$RCName"))}</link>
        <description>${\(&QuoteHtml($SiteDescription))}</description>
        <wiki:interwiki>
            <rdf:Description link="$QuotedFullUrl">
                <rdf:value>$InterWikiMoniker</rdf:value>
            </rdf:Description>
        </wiki:interwiki>
        <items>
            <rdf:Seq>
RSS
  ($headList, $items) = &GetRc(0, @_);
  $rssHeader .= $headList;
  return <<RSS ;
$rssHeader
            </rdf:Seq>
        </items>
    </channel>
    <image rdf:about="${\(&QuoteHtml($RssLogoUrl))}">
        <title>${\(&QuoteHtml($SiteName))}</title>
        <url>$RssLogoUrl</url>
        <link>$QuotedFullUrl</link>
    </image>
$items
</rdf:RDF>
RSS
}

sub GetRssRcLine{
    my ($pagename, $timestamp, $host, $userName, $userID, $summary, $isEdit, $pagecount, $revision, $diffPrefix, $historyPrefix, $pagePrefix) = @_;    
    my ($pagenameEsc, $itemID, $description, $authorLink, $author, $status, $importance, $date, $item, $headItem);
    
    $pagenameEsc = CGI::escape($pagename);
    
    # Add to list of items in the <channel/>
    $itemID = $FullUrl . &ScriptLinkChar() . &GetOldPageParameters('browse', $pagenameEsc, $revision);
    $itemID = &QuoteHtml($itemID);
    
    $headItem = "                <rdf:li rdf:resource=\"$itemID\"/>\n";
    
    # Add to list of items proper.
    if (($summary ne "") && ($summary ne "*")) {
        $description = &QuoteHtml($summary);
    }
    
    $host = &QuoteHtml($host);
    
    if ($userName) {
        $author = &QuoteHtml($userName);
        $authorLink = 'link="' . $QuotedFullUrl . &ScriptLinkChar() . $author . '"';
    } 
    else {
        $author = $host;
    }
    
    $status = (1 == $revision) ? 'new' : 'updated';
    $importance = $isEdit ? 'minor' : 'major';
    $timestamp += $TimeZoneOffset;
    
    my ($sec, $min, $hour, $mday, $mon, $year) = localtime($timestamp);
    $year += 1900;
    
    $date = sprintf("%4d-%02d-%02dT%02d:%02d:%02d+%02d:00", $year, $mon+1, $mday, $hour, $min, $sec, $TimeZoneOffset/(60*60));
    $pagename = &QuoteHtml($pagename);
  
  # Write it out longhand
  $item = <<RSS ;
    <item rdf:about="$itemID">
        <title>$pagename</title>
        <link>$pagePrefix$pagenameEsc</link>
        <description>$description</description>
        <dc:date>$date</dc:date>
        <dc:contributor>
            <rdf:Description wiki:host="$host" $authorLink>
                <rdf:value>$author</rdf:value>
            </rdf:Description>
        </dc:contributor>
        <wiki:status>$status</wiki:status>
        <wiki:importance>$importance</wiki:importance>
        <wiki:diff>$diffPrefix$pagenameEsc</wiki:diff>
        <wiki:version>$revision</wiki:version>
        <wiki:history>$historyPrefix$pagenameEsc</wiki:history>
    </item>
RSS
    return ($headItem, $item);
}

sub DoRss {
    print "Content-type: text/xml\n\n";
    &DoRc(0);
}

sub DoRandom {
    my ( $id, @pageList );
    
    @pageList = &AllPagesList();
    $id       = $pageList[ int( rand( $#pageList + 1 ) ) ];
    
    &ReBrowsePage( $id, "", 0 );
}
   
sub DoHistory {
    my ($id) = @_;
    my ( $html, $canEdit, $row, $newText );

    print &GetHeader( "", Ts('History of ') . &GetPageLink($id), ""  );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    
    &OpenPage($id);
    &OpenDefaultText();
    
    $newText = $Text{'text'};
    $canEdit = 0;
    $canEdit = &UserCanEdit($id) if ($HistoryEdit);
        
    if ($UseDiff) {
      print "\n<form id='wikiform' action='$ScriptName' method='get'>";
      print "\n<input type='hidden' name='action' value='browse'/>";
      print "\n<input type='hidden' name='diff' value='1'/>";
      print "\n<input type='hidden' name='id' value='$id'/>";
      print "\n<table class='wikihistory' border='0'>";
    }
    
	print "\n<thead><tr><th></th><th>Version</th><th>Date</th><th>Author</th><th>Summary</th<th>Description</th></tr></thead>";
	print "<tbody>";
    $html = &GetHistoryLine( $id, $Page{'text_default'}, $canEdit, $row++ );
    &OpenKeptRevisions('text_default');
    
    foreach ( reverse sort { $a <=> $b } keys %KeptRevisions ) {
        next if ( $_ eq "" );    # (needed?)
        $html .= &GetHistoryLine( $id, $KeptRevisions{$_}, $canEdit, $row++ );
    }
    
    print $html;
    
    if ($UseDiff) {
        my $label = "Compare";
        
        print "\n<tr><td colspan='6' align='left'><br/>";
        print "\n<input type='submit' value='$label'/>&nbsp;&nbsp;</td></tr></tbody></table></form>";
        print &GetDiffHTML( &GetParam( 'defaultdiff', 1 ), $id, "", "", $newText );
    }
    
    print "\n</div>";
    print &GetFooterText();

    print "\n</div></div></div></div></body></html>";    
}

sub GetMaskedHost {
    my ($text) = @_;
    my ($logText);
    
    if ( !$MaskHosts ) {
        return $text;
    }
    
    $logText = "(logged)";
    
    if ( !( $text =~ s/\d+$/$logText/ ) ) { # IP address (ending numbers masked)
        $text =~ s/^[^\.\(]+/$logText/;     # Host name: mask until first .
    }
    
    return $text;
}

sub GetDateTime {
    my ($timestamp) = @_;
    
    unless ($timestamp) { $timestamp = $Now + $TimeZoneOffset; }    
    my ($sec, $min, $hour, $mday, $mon, $year) = localtime($timestamp);
    
    $year += 1900;
    my $date = sprintf("%4d-%02d-%02dT%02d:%02d:%02d+%02d:00", $year, $mon+1, $mday, $hour, $min, $sec, $TimeZoneOffset/(60*60));

    return $date;    
}

sub GetHistoryLine {
    my ( $id, $section, $canEdit, $row ) = @_;
    my ( $html, $expirets, $rev, $summary, $host, $user, $uid, $ts, $minor, $description );
    my ( %sect, %revtext );
    
    %sect 			= split( /$FS2/, $section, -1 );
    %revtext 		= split( /$FS3/, $sect{'data'} );
	
    $rev     		= $sect{'revision'};
    $summary 		= $revtext{'summary'};
	$description 	= $revtext{'description'};
    
    if ( ( defined( $sect{'host'} ) ) && ( $sect{'host'} ne "" ) ) {
        $host = $sect{'host'};
    }
    else {
        $host = $sect{'ip'};
    }
    
    $host     = &GetMaskedHost($host);
    $user     = $sect{'username'};
    $uid      = $sect{'id'};
    $ts       = $sect{'ts'};
    $minor    = "";
    $minor    = "<i>(edited) </i>" if ( $revtext{'minor'} );
    $expirets = $Now - ( $KeepDays * 24 * 60 * 60 );

    if ($UseDiff) {
        my ( $c1, $c2 );
        
        $c1 = "checked='checked'" if 1 == $row;
        $c2 = "checked='checked'" if 0 == $row;
		
        $html .= "\n<tr>";
        $html .= "\n<td style='width: 50px; text-align: center;' nowrap valign='top'>";
        $html .= "\n<input style='_margin-right: -10px;' type='radio' name='diffrevision' value='$rev' $c1/>";
        $html .= "\n<input type='radio' name='revision' value='$rev' $c2/>";
        $html .= "</td>";
        $html .= "\n<td  valign='top' style='width: 120px;'>";
    }
    
    if ( 0 == $row ) {    
        # current revision
        $html .= &GetPageLinkText( $id, Ts( 'RevisionB %s', $rev ) ) . ' ';
        
        if ($canEdit) {
            $html .= &GetEditLink( $id, "Edit" ) . ' ';
        }
    }
    else {
        $html .= &GetOldPageLink( 'browse', $id, $rev, Ts( 'RevisionA %s', $rev ) ) . ' ';
        
        if ($canEdit) {
            $html .= &GetOldPageLink( 'edit', $id, $rev, "Edit" ) . ' ';
        }
    }
	
    $html .= "\n<td valign='top' style='width: 150px' nowrap><i>" . &TimeToText($ts) . "</i></td>";
    $html .= "\n<td valign='top' style='width: 100px' nowrap>&nbsp;" . &GetAuthorLink( $host, $user, $uid ) . "&nbsp;$minor</td>";
    
	if ( defined($summary) && ( $summary ne "" ) && ( $summary ne "*" ) ) { $summary = &QuoteHtml($summary); } else { $summary = "&nbsp;_"; }
	if ( defined($description) && ( $description ne "" ) && ( $description ne "*" ) ){ $description = &QuoteHtml($description); } else { $description = "&nbsp;_"; }   
	
	$html .= "\n<td valign='top'>$summary &nbsp;&nbsp;</td><td valign='top'>$description</td>";
    $html .= $UseDiff ? "</tr>" : "\n<br/>";
    
    return $html;
}

#------------------------------------------------------------------------------
# HTML and page-oriented functions
#------------------------------------------------------------------------------
sub ScriptLinkChar {
    if ($SlashLinks) {
        return '/';
    }
    
    return '?';
}

sub ScriptLink {
  my ($action, $text) = @_;

  return "<a class='wikiscriptlink' title='click to visit page' href='" . $ScriptName . &ScriptLinkChar() . &UriEscape($action) . "'>$text</a>";
}

sub ScriptLinkClass {
  my ($action, $text, $class) = @_;

  return "<a href='" . $ScriptName . &ScriptLinkChar() . &UriEscape($action) . "' class='" . $class . "'>$text</a>";
}

sub ScriptLinkTitle {
    my ( $action, $text, $title ) = @_;
    
    if ($FreeLinks) { $action =~ s/ /_/g; }
    
    return "<a href='" . $ScriptName . &ScriptLinkChar() . &UriEscape($action) . "' title='$title' class='wikiscriptlinktitle'>$text</a>";
}

sub ScriptLinkLeftNav {
    my ($id, $action, $target, $label, $type) = @_;
    my $html;
    my $title;
    my $class;
    my $oldid = &GetParam('oldid');
    
    if ($type eq "1"){
        if ($target eq $action){ $html .= "\n<li class='selected'><a class='wikipagelink' title='click to visit this page.' href='\?action=$target'>$label</a></li>"; }
        elsif ($target =~ "listfiles" && ($action eq "listdisabled" or $action eq "listfiles")){ $html .= "\n<li class='selected'><a class='wikipagelink' title='click to visit this page.' href='\?action=$target'>$label</a></li>"; } 
        else { $html .= "\n<li><a class='wikipagelink' title='click to visit this page.' href='\?action=$target'>$label</a></li>"; }
    }
    else {
        my $authtype = &CheckIsAuthUser($target);
        
        if ($authtype eq ""){
            $title = "This page is private.";
            $class = "wikipagelink private";
            $label .= "!";
        }
        elsif ( $authtype eq "1"){
            $title = "click to visit this locked page.";
            $class = "wikipagelink locked";
            $label .= "&not;";
        }
        else {
            $title = "click to visit this page.";
            $class = "wikipagelink";        
        }
        
        if ($id eq $target or $oldid eq $target){ $html .= "\n<li class='selected'><a class='$class' title='$title' href='\?$target'>$label</a></li>"; }
        else { $html .= "\n<li><a class='$class' title='$title' href='\?$target'>$label</a></li>"; }        
    }
}

sub GetOrphanLink {
    return &ScriptLink("action=orphans", T('Orphans'));
}

sub DoOrphanList {
    print &GetHeader("", &QuoteHtml(T('Full Orphan List')), "");
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    print &PrintPageList( "", "", &GetOrphanList() );
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

#--------------------------------------------------------------------------
# Orphan pages have no back-links; no pages link to them
#--------------------------------------------------------------------------
sub GetOrphanList {
    my @found;    
    my %seen = ();
    my @pglist = &AllPagesList();
    
    foreach my $name (@pglist) {
		if ($UseNotesPages){
			# _Notes pages are not orphans
			if ($name =~ /_Notes$/){ $seen{$name} = 1; next; }
		}
		
		if ($UseSubpage){
			# Sub-pages are not orphans
			if ($name =~ /\//){ $seen{$name} = 1; next; }
		}
		
        $seen{$name} = 0;
    }

    # pages linked from menu bar aren't orphans
    $seen{$HomePage} = 1;
    $seen{$RCName} = 1;
	$seen{$HelpPage} = 1;
	
	$seen{'WikiContacts'} = 1;
	$seen{'SandBox'} = 1;
	$seen{'CategoryCategory'} = 1;
	$seen{'NobleWiki'} = 1;
    
    foreach my $name (@pglist) {
        my @links = &GetPageLinks($name, 1, 0, 0, 0);
        
        foreach my $link (@links) {
            #don't include self links
            unless ($link eq $name) {
                $seen{$link}++ if exists $seen{$link};
            }
        }
    }
    
    foreach my $name (sort keys %seen) {
        push(@found, $name) if $seen{$name} < 1;
    }
    
    return @found;
}

sub GetPageDescription {
	my ( $id ) = @_;
	my ( $fname, $data, %temp, $description, $html);
	
	$fname   = &GetPageFile($id);
	$description = "";
    
    if ( -f $fname ) {
        $data = &ReadFileOrDie($fname);
        %temp = split( /$FS1/, $data, -1 );    # -1 keeps trailing null fields
		
		$description = $temp{'description'};
    }
	
	if ( defined($description) && ( $description ne "" ) && ( $description ne "*" ) ){
		$html = "<span class='pagedescription'>&there4;<i>$description</i></span>";
	}
	else { $html = ""; }
	
	return $html;
}

sub GetPageLinkText {
    my ( $id, $name ) = @_;
    $id =~ s|^/|$MainPage/|;
    
    if ($FreeLinks) {
        $id = &FreeToNormal($id);
        $name =~ s/_/ /g;
    }
    
    my $authtype = &CheckIsAuthUser($id);

    if ($authtype eq ""){
        return &ScriptLinkClass( $id, "$name!", 'wikipagelink private', T('this page is private.') );
    }
        
    if ( -f &GetLockedPageFile($id) || $authtype eq "1"){
        return &ScriptLinkClass( $id, "$name&not;", 'wikipagelink locked', T('click to visit this locked page') );
    }
    
    return &ScriptLinkClass( $id, $name, 'wikipagelink', T('click to visit page') );
}

sub GetPageLink {
    my ($id) = @_;
    return &GetPageLinkText( $id, $id );
}

sub GetEditLink {
    my ( $id, $name ) = @_;
    
    if ($FreeLinks) {
        $id = &FreeToNormal($id);
        $name =~ s/_/ /g;
    }
    return &ScriptLinkClass( "action=edit&id=$id", $name, 'wikipageedit', 'click to edit page' );
}

sub GetCreateNewLink {
    my ( $id, $name ) = @_;
    my ( $html );
    
    if ($FreeLinks) {
        $id = &FreeToNormal($id);
        $name =~ s/_/ /g;
    }
    
    $html  = "<a href='$ScriptName";
    $html .= &ScriptLinkChar();
    $html .= "action=edit&id=$id' class='wikicreatepagelink' title='create this entry'>";
    $html .= $name;
    $html .= "<span class='wikilinkicon'>&nbsp;</span>";
    $html .= "</a>";
    
    return $html;
}

sub GetDeleteLink {
    my ( $id, $name, $confirm ) = @_;
    
    if ($FreeLinks) {
        $id = &FreeToNormal($id);
        $name =~ s/_/ /g;
    }
    
    return &ScriptLink( "action=delete&id=$id&confirm=$confirm", $name );
}

sub GetOldPageParameters {
    my ( $kind, $id, $revision ) = @_;
    
    $id = &FreeToNormal($id) if $FreeLinks;
    return "action=$kind&id=$id&revision=$revision";
}

sub GetOldPageLink {
    my ( $kind, $id, $revision, $name ) = @_;
    
    $name =~ s/_/ /g if $FreeLinks;
    
    return &ScriptLink( &GetOldPageParameters( $kind, $id, $revision ), $name );
}

sub GetPageOrEditAnchoredLink {
    my ( $id, $anchor, $name ) = @_;
    my ( @temp, $exists );
    my $NamedFreeLink = 0;
    
    if ( $name eq "" ) {
        $name = $id;
        if ($FreeLinks) { $name =~ s/_/ /g; }
    }
    else { $NamedFreeLink = 1; }
    
    $id =~ s|^/|$MainPage/|;
    
    if ($FreeLinks) { $id = &FreeToNormal($id); }
    $exists = 0;
    
    if ($UseIndex) {
        if ( !$IndexInit ) {
            @temp = &AllPagesList();    # Also initializes hash
        }
        $exists = 1 if ( $IndexHash{$id} );
    }
    elsif ( -f &GetPageFile($id) ) {    # Page file exists
        $exists = 1;
    }
    
    if ($exists) {
        $id = "$id#$anchor" if $anchor;
        $name = "$name#$anchor"  if $anchor && $NamedAnchors != 2 && !$NamedFreeLink;
        
        return &GetPageLinkText( $id, $name );
    }
    if ( $FreeLinks && !$EditNameLink ) {
        if ( $name =~ m| | ) {          # Not a single word
            $name = "[$name]";          # Add brackets so boundaries are obvious
        }
    }
    
    if ($EditNameLink) { return &GetEditLink( $id, $name ); }
    else { return &GetCreateNewLink( $id, $name ); }
}

sub GetPageOrEditLink {
    my ( $id, $name ) = @_;
    my ($link, $anchor) = split( /#/, $id, 2);
    
    return &GetPageOrEditAnchoredLink($link, $anchor, $name);
}

sub GetBackLinksSearchLink {
    my ($id) = @_;
    my $name = $id;
	
    $id =~ s|.+/|/|;    # Subpage match: search for just /SubName
    
    if ($FreeLinks) {
        $name =~ s/_/ /g;    # Display with spaces
        $id   =~ s/_/+/g;    # Search for url-escaped spaces
    }
    
    return &ScriptLinkTitle( "back=$id", $name, "click to see which pages link to this one" );
}

sub GetPrefsLink {
    return &ScriptLink( "action=editprefs", "Preferences" );
}

sub GetRandomLink {
    return &ScriptLink( "action=random", "Random Page" );
}

sub ScriptLinkDiff {
    my ( $diff, $id, $text, $rev ) = @_;
    
    $rev = "&revision=$rev" if ( $rev ne "" );
    $diff = &GetParam( "defaultdiff", 1 ) if ( $diff == 4 );
    
    return &ScriptLinkTitle( "action=browse&diff=$diff&id=$id$rev", $text, "click to view last revision" );
}

sub GetUploadLink {
    return &ScriptLink( 'action=upload', "Upload" );
}


sub GetAuthorLink {
    my ( $host, $userName, $uid ) = @_;
    my ( $html, $title, $userNameShow );
    
    $userNameShow = $userName;
    
    if ($FreeLinks) {
        $userName     =~ s/ /_/g;
        $userNameShow =~ s/_/ /g;
    }
    
    if ( &ValidId($userName) ne "" ) {    # Invalid under current rules
        $userName = "";                   # Just pretend it isn't there.
    }
    
	# CREATE a link to the default homepage if it exists for this user
    if ( ( $uid > 0 ) && ( $userName ne "" ) ) {		
		if (-f &GetPageFile("$UserPagePrefix$userName") ){
			$html = &ScriptLinkTitle( "$UserPagePrefix$userName", $userNameShow, Ts( 'ID %s', $uid ) . ' ' . Ts( 'from %s', $host ) );
		}	
        else { $html = $userName; }
	}
    else {
        $html = $host;
    }
    
    return $html;
}

sub GetHistoryLink {
    my ( $id, $text, $title ) = @_;
    
    if ($FreeLinks) { $id =~ s/ /_/g; }
    
    return &ScriptLinkTitle( "action=history&id=$id", $text, $title );
}

sub GetHeader {
    my ($id, $title, $oldId, $backlinks) = @_;
    my ( $html, $header, $logoImage, $result, $embed, $altText, $temp );

    $embed     	= &GetParam( 'embed', $EmbedWiki );
    $altText   	= "[Home]";    
    $result 	= &GetHttpHeader("");
        
    # DISPLAY underscores as spaces
    if ($FreeLinks) { $title =~ s/_/ /g; }
    
    $result .= &GetHtmlHeader("$SiteName: $title", $id);
    
    return $result if ($embed);
    $result .= "\n<a name='wikiheader'></a><div class='wikiheader'>";
    
    if ($oldId ne '') { $result .= $q->h3('(' . Ts('redirected from %s',  &GetEditLink($oldId, &QuoteHtml($oldId)), 1) . ')'); }
    else { $result .= "<h3>&nbsp;</h3>"; }
    
    if ( ( !$embed ) && ( $LogoUrl ne "" ) ) {
        $logoImage = "img class='wikilogo' src='$LogoUrl' alt='$altText'";        
        $header = &ScriptLink( $HomePage, "\n<$logoImage>" );
    }
    
    if ($id and $backlinks) {
        my $authtype = &CheckIsAuthUser($id);
        
        if (&PageIsLocked($id, 1) || $authtype eq "1"){
            $temp = "<span class='wikilockicon' title='this page is locked.'>&nbsp;</span>";
        }
        else {    
            if ( -f &GetLockedPageFile($id) ) {
                $temp = "<a href='$ScriptName?action=edit&id=$id' title='this page locked for others. click to edit page'><span class='wikiprotectedicon'>&nbsp;</span></a>";
            }
            else {
                $temp = "<a href='$ScriptName?action=edit&id=$id' title='click to edit this page'><span class='wikiediticon'>&nbsp;</span></a>";
            }
        }        
        $result .= $q->h1( $header . &GetBackLinksSearchLink($id) . $temp );
    }
    else {
        $result .= $q->h1( $header . $title );
    }    
	
    if ( &GetParam( "toplinkbar", 1 ) ) {        
        $result .= &GetGotoBar("footer");
        $result .= $WikiLineHeader;
    }
	
    $result .= "</div>";
        
    return $result;
}

sub GetHttpHeader {
    my ($type) = @_;
    my $cookie;
    
    $type = "text/html" if ( $type eq "" );
    
    if ( defined( $SetCookie{'id'} ) ) {
        $cookie =
           "$CookieName=" . "rev&"
          . $SetCookie{'rev'} . "&id&"
          . $SetCookie{'id'}
          . "&randkey&"
          . $SetCookie{'randkey'};
        $cookie .= ";expires=Fri, 08-Sep-2013 19:48:23 GMT";
        
        if ( $HttpCharset ne "" ) {
            return $q->header(
                -cookie => $cookie,
                -type   => "$type; charset=$HttpCharset"
            );
        }
        
        return $q->header( -cookie => $cookie );
    }
    
    if ( $HttpCharset ne "" ) { return $q->header( -type => "$type; charset=$HttpCharset" ); }
    
    return $q->header( -type => $type );
}

sub GetHtmlHeader {
    my ($title, $id) = @_;
    my ( $dtd, $html, $bodyExtra, $stylesheet, $keywords );
    
    $dtd   = "-//IETF//DTD HTML//EN";
	
	# FIX for scriptlink in title
	if ($title =~ /\>(.*)</ && (&GetParam('action', "") eq "history") ){ $title = "History of $1"; }
	else { $title = $q->escapeHTML($title); }
	
	$html  = "";	
    $html  = qq(<!DOCTYPE HTML PUBLIC "$dtd">);    
    $html .= "\n<html>";
    $html .= "\n<head>";
    $html .= "\n<title>$title</title>";
    
    if ( $FavIcon ne "" ) { $html .= "\n<link rel='shortcut icon' href='$FavIcon'>"; }    
    if ($MetaKeywords) {
        $keywords = $OpenPageName;
        $keywords =~ s/([a-z])([A-Z])/$1, $2/g;
        $html .= "\n<meta name='keywords' content='$keywords'/>" if $keywords;
    }
    
    #--------------------------------------------------------------------------
    # UNSURE ABOUT THIS ONE; we don't want robots indexing our history or other admin pages
    #--------------------------------------------------------------------------
    my $action = lc(&GetParam('action', ''));
    
    unless (!$action or $action eq "rc" or $action eq "index") { 
        $html .= "\n<meta name='robots' content='noindex,nofollow'>";    
    }
    
	$html .= "\n<meta http-equiv='Content-Type' content='text/html;$HttpCharset' >";
	$html .= "\n<meta name='robots' content='noindex,nofollow'>";    
	$html .= "\n<meta http-equiv='Pragma' content='no-cache'>";
	$html .= "\n<meta http-equiv='Expires' content='-1'>";
		
    if ( $SiteBase ne "" ) { $html .= qq(<base href="$SiteBase">); }
    
    $stylesheet = &GetParam( 'stylesheet', $StyleSheet );
    $stylesheet = $StyleSheet if ( $stylesheet eq "" );
    $stylesheet = "" if ( $stylesheet eq '*' );    # Allow removing override
    
    if ( $stylesheet ne "" ) { $html .= qq(<link rel="stylesheet" href="$stylesheet">); }

    my $bots = "";
    
    # actions and non-existant page views don't get indexed or followed by robots
    if ( ($id eq "") || ( $id && !-f &GetPageFile($id) ) ) { $bots = "no"; }
    
    $bots = $bots . 'index,' . $bots . 'follow';
    $html .= qq(<meta name="robots" content="$bots" />\n);
    
    $html .= $UserHeader;
    $bodyExtra = "";
    
    if ( $UserBody ne "" ) { $bodyExtra = " $UserBody"; }    
    if ( $BGColor ne "" ) { $bodyExtra .= "BGCOLOR='$BGColor'"; }
    
    $html .= "\n</head>";
    $html .= "\n<body$bodyExtra>";
    $html .= "\n<div id='wikicontainer-outer'>";
    $html .= "\n<div id='wikicontainer-inner'>";
	
	if ( &GetParam( 'embed', $EmbedWiki ) ) { $html .= "\n<div id='wikicontainer-embed'>"; }
	else { $html .= "\n<div id='wikicontainer'>"; }
    
    return $html;
}

sub GetLeftNav {
    my ($id, $action, $diff, $html, $hasFeedback, $notesPage, $username, $notValid);
	
    if ( &GetParam( 'embed', $EmbedWiki ) ) { return ""; } 
    if ($Text{'text'} =~ /^\s*{{magic:\s?.*\}}/i){ $hasFeedback = 1; }

	$id = $OpenPageName;
	$username = &GetParam("username", "");
    $action = &GetParam( "action", "" );
    $diff = &GetParam( "diff", "" );
	
	$notValid = $id =~ /^\d*$/;
	
    $html = "";    
    $html .= "\n<div class='wikileftnav'>";
    $html .= "\n    <div class='wikileftnavbox'>";
    $html .= "\n        <ul>";
    
    $html .= &ScriptLinkLeftNav($id, $action, $HomePage, 'Main', "") if $HomePage;
    $html .= &ScriptLinkLeftNav($id, $action, $InfoPage, 'About', "") if $InfoPage;
    $html .= &ScriptLinkLeftNav($id, $action, $CategoriesPage, 'Contents', "") if $CategoriesPage;
    $html .= &ScriptLinkLeftNav($id, $action, $FeaturedPage, 'Featured', "") if $FeaturedPage;
	$html .= &ScriptLinkLeftNav($id, $action, 'random', 'Random Article', "1") if &GetParam( "linkrandom", 0 );	
    $html .= &ScriptLinkLeftNav($id, $action, $SandBoxPage, 'SandBox', "") if $SandBoxPage;
    $html .= &ScriptLinkLeftNav($id, $action, $ContactUsPage, 'Contact Us', "") if $ContactUsPage;
    $html .= &ScriptLinkLeftNav($id, $action, $HelpPage, 'Help', "") if $HelpPage;
    
    $html .= "\n        </ul>";
    $html .= "\n    </div>    ";    
    $html .= "\n    <div class='wikileftnavbox'>";
    $html .= "\n        <ul>";
	
	if ($username ne ""){ $html .= &ScriptLinkLeftNav($id, $action, 'editprefs', 'Preferences', "1"); }
	else { $html .= &ScriptLinkLeftNav($id, $action, 'newlogin', 'Login', "1"); }
    
    if ( &UserCanUpload() ){ $html .= &ScriptLinkLeftNav($id, $action, 'upload', 'Upload', "1"); }
    if (&UserIsEditorOrAdmin()){ $html .= &ScriptLinkLeftNav($id, $action, 'listfiles&filter=!/', 'Manage Assets', "1"); }
    else { $html .= &ScriptLinkLeftNav($id, $action, 'listfiles&filter=!/', 'List Assets', "1"); }

    $html .= &ScriptLinkLeftNav($id, $action, 'RecentChanges', 'Recent changes', "");
    $html .= &ScriptLinkLeftNav($id, $action, 'ListOfWantedPages', 'Wanted Pages', "");
	$html .= &ScriptLinkLeftNav($id, $action, 'version', 'System Info', "1");
	
    $html .= "\n        </ul>";
    $html .= "\n    </div>";

	if (&UserIsAdmin()){
        $html .= "\n    <div class='wikileftnavbox'>";
        $html .= "\n        <ul>";
				
        $html .= &ScriptLinkLeftNav($id, $action, 'links', 'All Links', "1");
        $html .= &ScriptLinkLeftNav($id, $action, 'editbanned', 'Banned List', "1");    
        $html .= &ScriptLinkLeftNav($id, $action, 'maintain', 'Maintenance', "1");
        $html .= &ScriptLinkLeftNav($id, $action, 'maintainrc', 'Trim History', "1");       
        $html .= &ScriptLinkLeftNav($id, $action, 'editlinks', 'Manage Pages', "1");    
        $html .= &ScriptLinkLeftNav($id, $action, 'orphans', 'List Orphans', "1");
        $html .= &ScriptLinkLeftNav($id, $action, 'version', 'Wiki Version', "1");
		
		$html .= "<li>";
		if ($id eq "" || $notValid){ $html .= "<span class='disabled'>Lock Page</span>"; }
	    else {
	        if ( -f &GetLockedPageFile($id) ) { $html .= &GetPageLockLink( $id, 0, "Unlock Page" ); }
	        else { $html .= &GetPageLockLink( $id, 1, "Lock Page" ); }
	    } 
		$html .= "</li>";
		$html .= "<li>";
		
	    if ( -f "$DataDir/noedit" ) { $html .= &ScriptLink( "action=editlock&set=0", "Unlock site" ); }
	    else { $html .= &ScriptLink( "action=editlock&set=1", "Lock site" ); }	
		
		$html .= "\n</li>";				
        $html .= "\n        </ul>";
        $html .= "\n    </div>";
    }
	
    $html .= "\n    <div class='wikileftnavbox'>";
    $html .= "\n        <ul>";
                        
    if ($id ne ""){
        unless ($action eq 'history' or $id eq 'ListOfWantedPages' or $id eq 'RecentChanges' or $id =~ /^\d/){
            if (&UserCanEdit( $id, 0 )){ $html .= "\n<li><a href='$ScriptName?action=edit&id=$id'>Edit Page</a></li>"; }
            else { $html .= "\n<li><a href='$ScriptName?action=edit&id=$id'>Source</a></li>"; }                           
            
            if ($hasFeedback){ 
                if ($action eq 'discuss'){ $html .= "\n<li class='selected'><a href='$ScriptName?action=browse&id=$id' title='click to browse page'>Discuss Page</a></li>"; }
                else { $html .= "\n<li><a href='$ScriptName?action=discuss&id=$id&magic=solo' title='click to discuss this page'>Discuss Page</a></li>" }
            }
            else {
                $html .= "\n<li class='disabled'>Discuss Page</li>";
            }
			
			if ($UseNotesPages){
				#BUILD link for Notes page; GivenPage becomes GivenPage_Notes
				if ($id !~ /$NotesSuffix$/ && $action ne 'discuss'){			
					if (!-f &GetPageFile("$id$NotesSuffix")) { $html .= "\n<li><a href='$ScriptName?action=edit&id=$id$NotesSuffix' title='click to create notes for this page'>Notes Page</a></li>"; }
					else { $html .= "\n<li><a href='$ScriptName?action=browse&id=$id$NotesSuffix' title='click to view notes for this page'>Notes Page</a></li>"; }
				}
				else {
					$html .= "\n<li class='disabled'>Notes Page</li>";
				}
			}
			
			if ($action eq 'history' or $diff ne ""){ $html .= "\n<li class='selected'>Version History</li>"; }
            else { $html .= "\n<li><a href='$ScriptName?action=history&id=$id'>Version History</a></li>"; }
        }
        else {            
            $html .= "\n<li class='disabled'>Edit Page</li>"; 
            $html .= "\n<li class='disabled'>Version History</li>";
            $html .= "\n<li class='disabled'>Discuss Page</li>";
			$html .= "\n<li class='disabled'>Notes Page</li>" if $UseNotesPages;
        }
    }
    else {
        if ($action eq 'edit'){ $html .= "\n<li class='selected'>Edit Page</li>"; }
        else { $html .= "\n<li class='disabled'>Edit</li>"; }        
        
        $html .= "\n<li class='disabled'>Version History</li>";
        $html .= "\n<li class='disabled'>Discuss Page</li>";
		$html .= "\n<li class='disabled'>Notes Page</li>" if $UseNotesPages;
    }
    
    $html .= "\n    </ul></div>";
    
    $html .= "\n    <div class='wikileftnavsearch' style='text-align:right;'>";
    $html .= "\n        <form>";
    $html .= "\n            <div class='wikisearchlabel' style='text-align:left;'><b>Search</b></div>";
    $html .= "\n            <input type='text' title='Enter ! before search term for exclusion' name='search' class='searchterm' />";
    $html .= "\n            <span><input type='checkbox' value='1' name='regex' title='click to enable searches using Regular Expressions'/>regex&nbsp;</span>";
    $html .= "\n			<span><input type='checkbox' value='1' checked='checked' name='titlesonly' title='click to restrict results to page titles'/>titles</span>";
	$html .= "\n            <input id='btnGo' type='submit' value='Go!' name='dosearch' title='click to perform your search request.'/>";
    $html .= "\n        </form><div style='clear: both;'></div></div>";
    $html .= "\n</div>";
    
    return $html;    
}

sub GetFooterText {
    my ( $id, $rev ) = @_;
    my ( $action, $diff, $result, $canEdit );

    if ( &GetParam( 'embed', $EmbedWiki ) ) { return ""; }
    unless ($id){ $id = &GetParam( "id", "" ); }

    $action = &GetParam( "action", "" );
    $diff = &GetParam( "diff", "" );
        
    if ($id ne ""){ if ($id =~ s/^\d*//g){ if ($action ne "delete"){ $canEdit = 1; }}}
    
    $result = "\n$WikiLineFooter" if ( !&GetParam( 'embed', $EmbedWiki ) );
    $result .= "\n<a name='wikifooter'></a><div class='wikifooter'>";
	
	if (&GetParam('bottomlinkbar', "")){ $result .= &GetGotoBar("header"); }
    
    if ($id ne ""){ 
        if ( $Section{'revision'} > 0 ) {
            $result .= "\n<div class='wikirevision'>";        
            $result .= "Created " . &TimeToText($Page{'tscreate'});
            
            if ($Page{'authorcreate'}) { $result .= " by " . $Page{'authorcreate'}; } 
            
            $result .= " | ";
            
            if ( $rev eq "" ) { $result .= "Last edited"; }
            else { $result .= "Edited"; }
            
            $result .= " " . &TimeToText( $Section{ts} );
            
            if ($AuthorFooter) { $result .= ' ' . Ts('by %s', &GetAuthorLink($Section{'host'}, $Section{'username'}, $Section{'id'}), 1); }
        }
        
        if ($canEdit){ if ($UseDiff) { $result .= " " . &ScriptLinkDiff( 4, $id, "(diff)", $rev ); }}
    }
    
    $result .= $UserFooter;
        
    $result .= "\n<form id='wikifooterform' action='$ScriptName' enctype='application/x-www-form-urlencoded' method='POST'>";
    if (&GetParam('extrasearchform', "")){ $result .= &GetSearchForm(); }
        
    if ( $DataDir =~ m|/tmp/| ) {
        $result .= "\n<br/><b>";
        $result .= "Warning";
        $result .= ":</b> ";
        $result .= "Database is stored in temporary directory $DataDir";
        $result .= "\n<br/>";
    }
    
    if ( $ConfigError ne "" ) {
        $result .= "\n<br/>";
        $result .= "\n<b>Config file error:</b>";
        $result .= "$ConfigError <br/>";
    }
    
    $result .= "</form>";
    $result .= &GetFooterNote();    
    $result .= "</div>";
        
    return $result;
}

sub GetSimpleFooterText {
	my $html;
	
	$html  = "\n<div class='wikifooter'>";
	
	if (&GetParam('bottomlinkbar', "")){
		$html .= &GetGotoBar("header");
	}
	
	$html .= &GetFooterNote;
	$html .= "\n</div>";
	
	return $html;
}

sub GetFooterNote {
    my $html;
    my $userid = &GetParam("username", "");
    my $access = "Guest ";
    my $username = "Anonymous";

    if (UserIsAdmin()){ $access = "Admin "; }
    elsif (UserIsEditor()){ $access = "Editor "; }
    
    if ($userid ne ""){ $username = $userid; }
    
    if ($FooterNote ne ""){
        $html = $FooterNote;
        $html =~ s/access/$access/;
        $html =~ s/username/$userid/;
    }
    
    return $html;
}

sub StoreFootNotes {
	my ($note) = @_;
	my ($html, $number, $text);
	
	$GLOBAL_footnoteCounter++;
	
	$text = $note; # TODO; use CommonMarkUp subroutine to allow footnotes to have wikimarkup; currently breaks
	$number = "<a class='footnote-item' name='fn_$GLOBAL_footnoteCounter' href='#fnr_$GLOBAL_footnoteCounter'>$GLOBAL_footnoteCounter</a>";

	if (defined $SaveNumFootnote{$note}) {
		$Footnotes[$SaveNumFootnote{$note}] =~ s/_MARK_/$number _MARK_/;
	} 
	else { 
		push @Footnotes, "$number _MARK_<span class='footnote-entry'>$note</span><br>\n";
		$SaveNumFootnote{$note} = $#Footnotes;
	}

	$html = "<sup><a class='footnote-note' name='fnr_$GLOBAL_footnoteCounter' href='#fn_$GLOBAL_footnoteCounter'>[$GLOBAL_footnoteCounter]</a></sup>";
	
	return $html;
}

sub GetFooterReferences {
	my ($html);
	
	if ($GLOBAL_footnoteCounter > 0) {
		map { s/_MARK_// } @Footnotes;
		
		$html .= "<div class='footnotes'><h6>" . T('References:') . "</h6>\n" . (join (('', @Footnotes))) . "</div>";
	}
	
	return $html;
}

sub GetGotoBar {
    my ($position) = @_;
    my ( $canEdit, $main, $html, $icon, $action, $diff, $rev, $diffrev, $newfile, $id, $oldid, $actionpage, $validId, $appendRev );
    
	$id = $OpenPageName;
	
	if ($id eq ""){ $id = &GetParam('id'); }
	
	$action = &GetParam('action');
	$actionpage = &GetIsAnActionPage();
	
	$oldid = &GetParam('oldid');
	$diff = &GetParam('diff');
	$rev = &GetParam('revision');
	$diffrev = &GetParam('diffrevision');
	$canEdit = &UserCanEdit($id) && !$actionpage;
	
	$validId = 0;
	$appendRev = "";
	
	if ($rev){ $appendRev = "&revision=$rev"; }
	if ($id =~ /$LinkPattern/ || $id =~ /$FreeLinkPattern/){ $validId = 1; }	
	if ($Section{'revision'} == 0){ $newfile = "1"; }
	
    $html = "\n<div class='wikigotobar'>";
    if ( $id =~ m|/| ) {
        $main = $id;
        $main =~ s|/.*||;    # Only the main page name (remove subpage)
        
        unless ($main eq $HomePage){ $html .= &GetPageLink($main); }
    }

	if ($validId){
		if ($action eq 'edit'){
			if (-f &GetPageFile($id) ){
				$html .= "\n<a href='$ScriptName?action=browse&id=$id'>View</a>"; 
			}
			else {
				$html .= "\n<a href='$ScriptName?action=browse&id=$id' class='selected'>View</a>"; 
			}
			
			if ($canEdit){
				$html .= "\n<a href='$ScriptName?action=edit&id=$id' class='selected'>Edit</a>"; 
			}
			else {
				$html .= "\n<a href='$ScriptName?action=edit&id=$id' class='selected'>Source</a>"; 
			}
		}
		else {
			if ($id eq $RCName){ 
				$html .= "\n<a class='disabled'>View</a>"; 
			}
			else {
				if ($id eq "$RCName$NotesSuffix"){
					$html .= "\n<a href='$ScriptName?action=browse&id=$id'>View</a>"; 
				}
				else {
					if ($actionpage){ 
						$html .= "\n<a class='selected'>View</a>"; 
					}
					else {
						$html .= "\n<a href='$ScriptName?action=browse&id=$id' class='selected'>View</a>"; 
					}
				}
			}
			
			if ($canEdit){
				$html .= "\n<a href='$ScriptName?action=edit&id=$id'>Edit</a>"; 
			}
			else {
				if($actionpage &&  $action ne 'history'){
					$html .= "\n<a class='disabled'>Edit</a>"; 
				}
				else {				
					$html .= "\n<a href='$ScriptName?action=edit&id=$id$appendRev'>Source</a>"; 
				}
			}
		}
	}
	else { 		
		unless ($validId and $canEdit){ 
			if ($actionpage){ 
				$html .= "\n<a class='disabled'>View</a>"; 
			}
			else {
				$html .= "\n<a href='$ScriptName?action=browse&id=$id' class='selected'>View</a>"; 
			}
			
			$html .= "\n<a class='disabled'>Edit</a>"; 
		}
		else {			
			$html .= "\n<a href='$ScriptName?action=browse&id=$id'>View</a>"; 
			$html .= "\n<a href='$ScriptName?action=edit&id=$id'>Edit4</a>"; 
		}
	}	
	
	if ($UseNotesPages){
		if ($id =~ /_Notes$/){ 
			if ($id eq "$RCName$NotesSuffix"){
				if (-f &GetPageFile("$id$NotesSuffix") ){
					$html .= "\n<a href='$ScriptName?action=browse&id=$id'>Notes</a>"; 
				}
				else {
					$html .= "\n<a href='$ScriptName?action=browse&id=$id' class='notfound'>Notes</a>"; 
				}
			}
			else {
				if ($action eq 'history'){ 
					$html .= "\n<a href='$ScriptName?action=browse&id=$id'>Notes</a>"; 
				}
				else {
					$html .= "\n<a href='#' class='selected'>Notes</a>";
				}
			}
		}
		else { 
			if ($action ne 'listfiles' and ($id eq $RCName and $newfile eq "") or $newfile eq ""){ 
				if (-f &GetPageFile("$id$NotesSuffix") ){
					$html .= "\n<a href='$ScriptName?action=browse&id=$id$NotesSuffix'>Notes</a>";
				}
				else {
					if ($id eq $NotFoundPage){
						$html .= "\n<a class='disabled'>Notes</a>";
					}
					else {
						$html .= "\n<a href='$ScriptName?action=browse&id=$id$NotesSuffix' class='notfound'>Notes</a>";
					}
				}
			}
			else { $html .= "\n<a class='disabled'>Notes</a>"; }
		}
	}
	
	if ($action eq 'history' or $diff ne "" or $rev ne "" or $diffrev){ $html .= "\n<a href='$ScriptName?action=history&id=$id' class='selected'>Version History</a>"; }
	else { 
		if ($validId and $action ne 'listfiles' and $newfile eq ""){ $html .= "\n<a href='$ScriptName?action=history&id=$id'>Version History</a>"; }
		else { $html .= "\n<a class='disabled'>Version History</a>"; }
	}

    if ($id eq $RCName){ 
		if ($action eq 'history' or $diff ne "" or $rev ne "" or $diffrev){
			$html .= "\n<a href='$ScriptName?$RCName'>Recent Changes</a>";
		}
		else {
			$html .= "\n<a href='$ScriptName?$RCName' class='selected'>Recent Changes</a>"; }
		}
	else { $html .= "\n<a href='$ScriptName?$RCName'>Recent Changes</a>"; }
	
    if ( &GetParam( "linkrandom", 0 ) ) { $html .= &GetRandomLink(); } 
	
    if ($id =~ /$HelpPage/ or $oldid =~ /$HelpPage/){ $html .= "\n<a href='$ScriptName?$HelpPage' class='selected'>Help</a>"; }	
	else { $html .= "\n<a href='$ScriptName?$HelpPage'>Help</a>"; }
	
	if ( $UserGotoBar ne "" ) { $html .= $UserGotoBar; }
	
	unless ( &GetParam( 'embed', $EmbedWiki ) ) {
		if ($position eq "footer"){ $icon = "&darr;"; }
		else { $icon = "&uarr;"; }
		$html .= "<a href='#wiki$position' class='wikiscriptlink' title='click to jump to $position'>$icon</a>"; 
	}
	    
    $html .= "</div>";
    
    return $html;
}

sub GetSearchForm {
    my ($html);
    
    $html =  "\n<div class='wikisearch'>";    
    $html .= "\n<input type='text' class='searchterm' name='search' title='Enter ! before search term for exclusion'>";
        
    if ($SearchButton) {
		$html .= "<input type='submit' value='Go!' name='dosearch' title='click to perform your search request.'/>";
        $html .= "\n<input type='checkbox' value='1' name='regex' title='click to enable searches using Regular Expressions'/><span>regex</span>";
		$html .= "\n<input type='checkbox' value='1' checked='checked' name='titlesonly' title='click to restrict results to page titles'/><span>titles</span>";
    }
    else { $html .= &GetHiddenValue( "dosearch", 1 ); }
    
    $html .= "</div>";
    
    return $html;
}

sub GetRedirectPage {
    my ( $newid, $name, $isEdit ) = @_;
    my ( $url, $html );
    my ($nameLink);

    # Normally get URL from script, but allow override.
    $FullUrl  = $q->url( -full => 1 ) if ( $FullUrl eq "" );
    $url      = $FullUrl . &ScriptLinkChar() . $newid;
    $nameLink = "<a href='$url' class='wikiredirect'>$name</a>";
    
    if ( $RedirType < 3 ) {
        if ( $RedirType == 1 ) {    # Use CGI.pm
            # NOTE: do NOT use -method (does not work with old CGI.pm versions)
            # Thanks to Daniel Neri for fixing this problem.
            $html = $q->redirect( -uri => $url );
        }
        else {    
        	# Minimal header
            $html = "Status: 302 Moved\n";
            $html .= "Location: $url\n";
            $html .= "Content-Type: text/html; charset=$HttpCharset\n\n";   # Needed for browser failure
        }
        $html .= " Your browser should go to the $newid page.";
        $html .= " If it does not, click $nameLink to continue.";
    }
    else {
        if ($isEdit) {
            $html  = &GetHeader( "", "Thanks for editing...", "" );
            $html .= &GetLeftNav();
            $html .= "\n<div class='wikiadmin'>";
             $html .= "Thank you for editing $nameLink ";
        }
        else {
            $html = &GetHeader( "", "Link to another page...", "" );
            $html .= &GetLeftNav();
            $html .= "\n<div class='wikiadmin'>";
        }
        
        $html .= "Follow the $nameLink link to continue.";
        $html .= "</div>";
        $html .= "</div></div></div></div></body></html>";    
    }
    
    return $html;
}

sub GetIsAnActionPage {
	my $action = &GetParam('action');
	my $search = &GetParam('dosearch');
	
	
	if ($action eq 'history'){ return 1; }
	if ($action eq 'editbanned'){ return 1; }
	if ($action eq 'banlist'){ return 1; }
	if ($action eq 'orphans'){ return 1; }
	if ($action eq 'version'){ return 1; }
	if ($action eq 'maintain'){ return 1; }
	if ($action eq 'links'){ return 1; }
	if ($action eq 'editlinks'){ return 1; }
	if ($action eq 'maintainrc'){ return 1; }
	if ($action eq 'listfiles'){ return 1; }
	if ($action eq 'upload'){ return 1; }
	if ($action eq 'editprefs'){ return 1; }
	if ($action eq 'newlogin'){ return 1; }
	if ($action eq 'login'){ return 1; }
	if ($action eq 'editlock'){ return 1; }
	if ($action eq 'pagelock'){ return 1; }
	if ($search ne ''){ return 1; }
	
	return 0;
}

#------------------------------------------------------------------------------
# Common wiki markup
#------------------------------------------------------------------------------
sub RestoreSavedText {
    my ($text) = @_;
    
    1 while $text =~ s/$FS(\d+)$FS/$SaveUrl{$1}/ge;    # Restore saved text
    
    return $text;
}

sub RemoveFS {
    my ($text) = @_;

    # Note: must remove all $FS, and $FS may be multi-byte/char separator
    $text =~ s/($FS)+(\d)/$2/g;
    
    return $text;
}

sub WikiToHTML {
    my ($pageText) = @_;
    
    $TableMode       = 0;
    %SaveUrl         = ();
    %SaveNumUrl      = ();
    $SaveUrlIndex    = 0;
    $SaveNumUrlIndex = 0;
    $pageText        = &RemoveFS($pageText);
    
    if ($RawHtml) {
        $pageText =~ s/<html>((.|\n)*?)<\/html>/&StoreRaw($1)/ige;
    }
    
    $pageText = &QuoteHtml($pageText);
    $pageText =~ s/\\ *\r?\n/ /g;    # Join lines with backslash at end
	$pageText =~ s/(\r?\n)+$//g;     # Remove extra blank lines
        
    if ($ParseParas) {
        # Note: The following 3 rules may span paragraphs, so they are copied from CommonMarkup
        $pageText =~ s/\&lt;nowiki\&gt;((.|\n)*?)\&lt;\/nowiki\&gt;/&StoreRaw($1)/ige;
        $pageText =~ s/\&lt;pre\&gt;((.|\n)*?)\&lt;\/pre\&gt;/&StorePre($1, "pre")/ige;
        $pageText =~ s/\&lt;code\&gt;((.|\n)*?)\&lt;\/code\&gt;/&StorePre($1, "code")/ige;
		
		# Note: These are the various custom markup that use at the start of a given line the pattern {{namespace:key=value|key=value|...}}
        $pageText =~ s/\s*\{{color:\s*(.*?)}}/&StoreRaw(&GetColor($1))/iges;
		$pageText =~ s/\s*\{{template:(\w+\s*.*?)}}/&StoreTemplate($1)/iges;
		$pageText =~ s/\s*\{{flash:\s*(.*?)}}/&StoreRaw(&GetFlash($1))/iges;
        $pageText =~ s/\s*\{{bbcode:\s*(.*?)}}/&StoreRaw(&GetBBCode($1))/iges;        
        $pageText =~ s/\s*\{{data:(\w+\s*.*?)}}/&StoreRaw(&GetJSON($1))/iges;
        $pageText =~ s/\s*\{{gallery:\s*(.*?)}}/&StoreRaw(&GetGallery($1))/iges;
        $pageText =~ s/\s*\{{code(:\s*\w+)?(.*?)?\r?\n(.*?)\r?\n?}}/&StoreRaw(&GetCodeBox($1, $2, $3))/iges;
		$pageText =~ s/\s*\{{box:\s*(\w+)?(.*?)?\r?\n?}}/&StoreRaw(&GetBox($1, $2))/iges; 
    }

	$pageText = &WikiLinesToHtml($pageText);         # Line-oriented markup
	$pageText =~ s/((.|\n)+?\n)\s*\n/&ParseParagraph($1)/geo;
    $pageText =~ s/(.*)<\/p>(.+)$/$1.&ParseParagraph($2)/seo;
    
    while (@HeadingNumbers) {
        pop @HeadingNumbers;
        $TableOfContents .= "</dd></dl>";
    }
	
    $pageText =~ s/\s*{{toc}}/<div class='wikitoc'><div class='wikitoctitle'>Table of Contents<\/div>$TableOfContents<\/div>/gi;
    $pageText =~ s/\s*{{toc:\s?(\d+)?}}/<div style='width: $1;' class='wikitoc'><div class='wikitoctitle'>Table of Contents<\/div>$TableOfContents<\/div>/gi;
	
    $pageText =~ s/\s*\{{subpages:\s+(\w+.*?)}}/&StoreRaw("\n<h6>" . Ts('Subpages of: %s', &QuoteHtml($1)) . "<\/h6>" . &GetPageList(&GetSubpages($1)))/ige;
    $pageText =~ s/\s*\{{subpages}}/&StoreRaw("\n<h6>" . Ts('Sub-pages for %s', $MainPage) . "<\/h6>" . &GetPageList(&GetSubpages($MainPage)))/ige;
    
    if ( $LateRules ne "" ) {
        $pageText = &EvalLocalRules( $LateRules, $pageText, 0 );
    }
    
    return &RestoreSavedText($pageText);
}

sub CommonMarkup {
    my ( $text, $useImage, $doLines ) = @_;
    local $_ = $text;
    
    if ( $doLines < 2 ) {    # 2 = do line-oriented only
        
        while ( m!\s*{{include:\s*((\w+\.?\w*|/)+)}}!gi and $AllowInclusion ) {        
            my $FileName = $1;
            
            open FILE, "$InclusionDir/$FileName"
            or &ReportError(T("Cannot open $FileName: $!"));
            
            local $/;            
            my $FileContent = <FILE>;
            
            close FILE
            or &ReportError(T("Cannot close '$FileName': $!"));
            s!\s*{{include:\s*$FileName}}!$FileContent!i unless $FileName !~ /(html?|txt)$/i;
        }
		
		# AUTO-SIGNATURE
		my $signature = &GetParam("username", "");       
		my $idLink = "<b>$UserPagePrefix$signature</b>";
		my $timestamp = "<i>" . &TimeToText($Now) . "</i>";
		my $sigNorm = "";
		my $sigTime = "";
		
		$signature =~ s/ /_/g;
		$sigNorm = "[[$idLink $signature]]";
		$sigTime = "[[$idLink $signature] $timestamp]";
		
		unless ($signature){ $signature = "<b>Guest</b>"; $idLink = &GetRemoteHost(); $sigNorm = "[$signature\@$idLink]"; $sigTime = "[$signature\@$idLink $timestamp]"; }   
		s/\~\~\~\~/\ $sigNorm/gi;
		s/\$\$\$\$/\ $sigTime/gi;
		
		# non-HTML word decoration
		
        # The <nowiki> tag stores text with no markup (except quoting HTML)
        s/\&lt;nowiki\&gt;((.|\n)*?)\&lt;\/nowiki\&gt;/&StoreRaw($1)/ige;

        # The <pre> tag wraps the stored text with the HTML <pre> tag
        s/\&lt;pre\&gt;((.|\n)*?)\&lt;\/pre\&gt;/&StorePre($1, "pre")/ige;
        s/\&lt;code\&gt;((.|\n)*?)\&lt;\/code\&gt;/&StorePre($1, "code")/ige;
		        
        if ( $EarlyRules ne "" ) {
            $_ = &EvalLocalRules( $EarlyRules, $_, !$useImage );
        }
        
        s/\[\#(\w+)\]/&StoreHref(" name='$1'")/ge if $NamedAnchors;
        
        if ($HtmlTags) {
            my ($t);
			
            foreach $t (@HtmlPairs) {
                s/\&lt;$t(\s[^<>]+?)?\&gt;(.*?)\&lt;\/$t\&gt;/<$t$1>$2<\/$t>/gis;
            }
            foreach $t (@HtmlSingle) {
                s/\&lt;$t(\s[^<>]+?)?\&gt;/<$t$1>/gi;
            }
        }
        else {

            # Note that these tags are restricted to a single line
            s/\&lt;b\&gt;(.*?)\&lt;\/b\&gt;/<b>$1<\/b>/gi;
            s/\&lt;i\&gt;(.*?)\&lt;\/i\&gt;/<i>$1<\/i>/gi;
            s/\&lt;strong\&gt;(.*?)\&lt;\/strong\&gt;/<strong>$1<\/strong>/gi;
            s/\&lt;em\&gt;(.*?)\&lt;\/em\&gt;/<em>$1<\/em>/gi;
        }

		s/(\[\[\[([^\n]+?)\]\]\])/&StoreRaw(&StoreFootNotes($2))/ige;
		        
		# <tt> (MeatBall)
        s/\&lt;tt\&gt;(.*?)\&lt;\/tt\&gt;/<tt>$1<\/tt>/gis; 
        s/\&lt;br\/?\&gt;/<br\/>/gi;    	# Allow simple line break anywhere
		s/([\w|\W]?)\\\\/$1<br\/>/gi;		# Allow Creole line break anywhere
        
        if ($HtmlLinks) {
            s/\&lt;A(\s[^<>]+?)\&gt;(.*?)\&lt;\/a\&gt;/&StoreHref($1, $2)/gise;
        }
        
        if ($FreeLinks) {
            # Consider: should local free-link descriptions be conditional?
            # Also, consider that one could write [[Bad Page|Good Page]]?
            s/\[\[$FreeLinkPattern\|([^\]]+)\]\]/&StorePageOrEditLink($1, $2)/geo;
            s/\[\[$FreeLinkPattern\]\]/&StorePageOrEditLink($1, "")/geo;
        }
        
        if ($BracketText) {        
            # Links like [URL text of link]
            s/\[$UrlPattern\s+([^\]]+?)(\|(.*))?\]/&StoreBracketUrl($1, $2, $useImage, $3)/geos;
            s/\[$InterLinkPattern\s+([^\]]+?)(\|(.*))?\]/&StoreBracketInterPage($1, $2, $useImage, $3)/geos;
            
            if ( $WikiLinks && $BracketWiki ) {    # Local bracket-links
                s/\[$LinkPattern\s+([^\]]+?)\]/&StoreBracketLink($1, $2)/geos;
                s/\[$AnchoredLinkPattern\s+([^\]]+?)\]/&StoreBracketAnchoredLink($1, $2, $3)/geos if $NamedAnchors;
            }
        }
        
        if ($UseUpload) { s/$UploadPattern/&StoreUpload($1)/geo; }
    
        s/\[$UrlPattern(\|(.*))?\]/&StoreBracketUrl($1, "", 0, "")/geo;
        s/\[$InterLinkPattern\]/&StoreBracketInterPage($1, "", 0, "")/geo;
        s/\b$UrlPattern/&StoreUrl($1, $useImage)/geo;
        s/\b$InterLinkPattern/&StoreInterPage($1, $useImage)/geo;
        
        if ($WikiLinks) {
            s/$AnchoredLinkPattern/&StoreRaw(&GetPageOrEditAnchoredLink($1, $2, ""))/geo if $NamedAnchors;

            # CAA: Putting \b in front of $LinkPattern breaks /SubPage links (subpage links without the main page)
            s/$LinkPattern/&GetPageOrEditLink($1, "")/geo;
        }
        
        s/\b$RFCPattern/&StoreRFC($1)/geo;
        s/\b$ISBNPattern/&StoreISBN($1)/geo;		
        
        if ($ThinLine) {
            if ($OldThinLine) {   
                # Backwards compatible, conflicts with headers
                s/====+/$WikiLine2/g;
            }
            else {                
                # New behavior--no conflict
                s/------+/$WikiLine2/g;
            }
            s/----+/$WikiLine1/g;
        }
        else {
            s/----+/$WikiLine/g;
        }
        
        if ($AutoMailto) {
            s/([A-z0-9-_]+(?:\.[A-z0-9-_]+)*)\@([A-z0-9-_]+(?:\.[A-z0-9-_]+)*(?:\.[A-z]{2,})+)/<a href="mailto:$1\@$2">$1\@$2<\/a>/g;
        }
    }
    
    if ($doLines) {    
		# 0 = no line-oriented, 1 or 2 = do line-oriented
		# The quote markup patterns avoid overlapping tags (with 5 quotes)
		# by matching the inner quotes for the strong pattern.
        s/('*)'''(.*?)'''/$1<strong>$2<\/strong>/g; #'REMARK
        s/''(.*?)''/<em>$1<\/em>/g;
        		
        if ($UseHeadings) {
            s/(^|\n)\s*(\=+)\s*(#)?\s+([^\n]+)\s+\=+/&StoreRaw(&WikiHeading($1, $2, $4, $3))/geo;
        }
        
        if ($TableMode == 1) {
            my @cells = split(/\|\|/);
            my $cellIndex = 0;
            
            while (/(\|\|)+([^\|<]+)/) {    
                my $switches = @cells->[++$cellIndex];
                my ($class, $style, $width, $align, $DUMMY) = &GetTableCellModifiers($switches, "", $cellIndex);
                my $cellOptions = "$class $style $width $align";
                
                s/((\|\|)+)/"<\/td><td $cellOptions colspan='" . (length($1)\/2) . "'>"/e;
            }
            
            s/(\|\w*=\w*)+([^\|<]+)//g;   
        }
        elsif  ($TableMode == 2) {
            my @cells = split(/\!\!/);
            my $cellIndex = 0;
            
            while (/(\!\!)+([^\!<]+)/) {            
                my $switches = @cells->[++$cellIndex];
                my ($class, $style, $width, $align, $DUMMY) = &GetTableCellModifiers($switches, "", $cellIndex);
                my $cellOptions = "$class $style $width $align";
                
                s/((\!\!)+)/"<\/th><th $cellOptions colspan='" . (length($1)\/2) . "'>"/e;                
            }
            
            s/(\|\w*=\w*)+([^\!<]+)//g;
        }
    }
    
    return $_;
}

sub GetTableCellModifiers {
    my ($given, $initialCell, $cellIndex) = @_;    
    my ($options) = $given;

    /^(\s*(\w+)\s*)\|/;
    my $align = $2;
    
    if ($initialCell ne ""){ $align = $initialCell; }
        
    $align = $align =~ /^  / ? ($align =~ /  $/ ? 'center' : 'right') : 'left';
    $align = "align='$align'";
    
    my ($options) = $options =~ /(\|\S*=\S*)+/g;
    my %options = &GetOptions($options);

    my $class;
    my $style;
    my $width;    
    my $rowclass;
    my $rowstyle;
    my $rowalign;
    my $tablewidth;
    my $tableclass;
    my $tablestyle;
    my $tablesort;
        
    if ($TableCellDefaults{"rowclass"} =~ /clear/){ $TableCellDefaults{"rowclass"} = ""; }
    if ($TableCellDefaults{"rowstyle"} =~ /clear/){ $TableCellDefaults{"rowstyle"} = ""; }
    if ($TableCellDefaults{"rowalign"} =~ /clear/){ $TableCellDefaults{"rowalign"} = ""; }
                
    if ($TableCellDefaults{"rowclass"}){ $rowclass = $TableCellDefaults{"rowclass"}; }
    if ($TableCellDefaults{"rowstyle"}){ $rowstyle = $TableCellDefaults{"rowstyle"}; }
    if ($TableCellDefaults{"rowalign"}){ $rowalign = $TableCellDefaults{"rowalign"}; }
        
    if ($options{'rowclass'}){ $rowclass = "class='" . $options{'rowclass'} . "'"; $TableCellDefaults{"rowclass"} = $rowclass; }
    if ($options{'rowstyle'}){ $rowstyle = "style='" . $options{'rowstyle'} . "'"; $TableCellDefaults{"rowstyle"} = $rowstyle; }
    if ($options{'rowalign'}){ $rowalign = "align='" . $options{'rowalign'} . "'"; $TableCellDefaults{"rowalign"} = $rowalign; }
    
    if ($rowclass){ $class = $rowclass; }
    if ($rowstyle){ $style = $rowstyle; }
    if ($rowalign){ $align = $rowalign; }

    if ($TableCellDefaults{"class$cellIndex"} =~ /clear/){ $TableCellDefaults{"class$cellIndex"} = ""; }
    if ($TableCellDefaults{"style$cellIndex"} =~ /clear/){ $TableCellDefaults{"style$cellIndex"} = ""; }
    if ($TableCellDefaults{"align$cellIndex"} =~ /clear/){ $TableCellDefaults{"align$cellIndex"} = ""; }
            
    if ($TableCellDefaults{"class$cellIndex"}){ $class = $TableCellDefaults{"class$cellIndex"}; }
    if ($TableCellDefaults{"style$cellIndex"}){ $style = $TableCellDefaults{"style$cellIndex"}; }
    if ($TableCellDefaults{"align$cellIndex"}){ $align = $TableCellDefaults{"align$cellIndex"}; }

    if ($options{'class'}){ $class = "class='" . $options{'class'} . "'"; $TableCellDefaults{"class$cellIndex"} = $class; }
    if ($options{'style'}){ $style = "style='" . $options{'style'} . "'"; $TableCellDefaults{"style$cellIndex"} = $style; }
    if ($options{'align'}){ $align = "align='" . $options{'align'} . "'"; $TableCellDefaults{"align$cellIndex"} = $align; }
    if ($options{'width'}){ $width = "width='" . $options{'width'} . "'"; }
    if ($options{'tablewidth'}){ $tablewidth = "width='" . $options{'tablewidth'} . "'"; }
    if ($options{'tablestyle'}){ $tablestyle = "style='" . $options{'tablestyle'} . "'"; }
    if ($options{'tableclass'}){ $tableclass = "class='" . $options{'tableclass'} . "'"; } else { $tableclass = "class='wikilargelist'"; }
    if ($options{'tablesort'}){ $tablesort = "class='" . $options{'tablesort'} . "'"; }
                    
    return ($class, $style, $width, $align, $tablewidth, $tablestyle, $tableclass, $tablesort);                
}

sub EmptyCellsToNbsp {
  my ($row) = @_;

  $row =~ s/(?<=\|\|)\s+(?=\|\|)/&nbsp;/g;
  $row =~ s/^\s+(?=\|\|)/&nbsp;/;
  $row =~ s/(?<=\|\|)\s+$/&nbsp;/;
  
  return $row;
}

sub InsertTableSorter {
    my ($numTables, $html, $count);
            
    if ($GLOBAL_tableCount){        
        for ($count = 1; $count < ($GLOBAL_tableCount + 1); $count++){
            $html .= "\n<script>\$(document).ready(function(){ \$('\#tablesorter\-$count').tablesorter({widgets: ['zebra']}); });<\/script>";
        }
    }
    return $html;    
}

sub WikiLinesToHtml {
    my ($pageText) = @_;
    my ( $pageHtml, @htmlStack, $code, $codeAttributes, $depth, $oldCode );
    
    @htmlStack = ();
    $depth     = 0;
    $pageHtml  = "";
    
    foreach ( split( /\r?\n/, $pageText ) ) {    # Process lines one-at-a-time
        $code           = "";
        $codeAttributes = "";
        $TableMode      = 0;
        $_ .= "\n";
        
        if (s/^(\;+)([^:]+\:?)\:/<dt>$2<dd>/) {
            $code  = "dl";
            $depth = length $1;
        }
        elsif (s/^(\:+)/<dt><dd>/) {
            $code  = "dl";
            $depth = length $1;
        }
        elsif (s/^(\*+)/<li>/) {
            $code  = "ul";
            $depth = length $1;
        }
        elsif (s/^(\#+)/<li>/) {
            $code  = "ol";
            $depth = length $1;
        }
        elsif ($TableSyntax && /^(\!\!)+.*\!\!\s*$/) {
            /^(\!\!)+([^\!]+)/;
            
            %TableCellDefaults = {};
            
            my $switches = $2;
            my ($class, $style, $width, $align, $tablewidth, $tablestyle, $tableclass, $tablesort) = &GetTableCellModifiers($switches, "", 0);
            my $cellOptions = "$class $style $width $align";
            my $insert1;
            my $insert2;
            my $tableid;
            
            unless ($tablesort){
                
                    $insert1 = "<thead>"; 
                    $insert2 = "<\/thead>"; 
                    $NewTable = 1;
                    $GLOBAL_tableCount++;
                    $tableid = "id='tablesorter-$GLOBAL_tableCount'";
                    $tableclass =~ s/class\=\'/class\=\'tablesorter /;    #'REMARK
              
            }
            
            s/^((\!\!)+)(.*)\!\!\s*$/"$insert1<tr><th $cellOptions colspan='" . (length($1)\/2) . "'>" . EmptyCellsToNbsp($3) . "<\/th><\/tr>$insert2\n"/e;
            
            $code = "table";
            $codeAttributes = "$tableid $tablewidth $tablestyle $tableclass";
            $TableMode = 2;
            $depth = 1;
        }
        elsif ($TableSyntax && /^(\|\|)+.*\|\|\s*$/) {
            /^((\|\|)+)(.*?)\|\|/;    
    
            my ($alignInitial) = $3;
            my $switches = $3;
            
            ($alignInitial) = $alignInitial =~ /(.*)\|/;    

            my ($class, $style, $width, $align, $tablewidth, $tablestyle, $tableclass, $tablesort) = &GetTableCellModifiers($switches, $alignInitial, 0);
            my $cellOptions = "$class $style $width $align";
            my $insert1;
            if ($NewTable == 1){ 
                $insert1 = "<tbody>";
                $NewTable = 2;
            }
            
            unless ($NewTable){ $NewTable = 3; }

            s/^((\|\|)+)(.*)\|\|\s*$/"$insert1<tr><td $cellOptions colspan='" . (length($1)\/2) . "'>" . EmptyCellsToNbsp($3) . "<\/td><\/tr>\n"/e;
            
            $code = "table";
            $codeAttributes = "$tablewidth  $tablestyle  $tableclass";
            $TableMode = 1;
            $depth = 1;
        }
        elsif (/^[ \t].*\S/) {
            $code  = "pre";
            $depth = 1;
        }
        else {
            $depth = 0;
        }
        
        while ( @htmlStack > $depth ) {    
            # Close tags as needed
            $pageHtml .= "</" . pop(@htmlStack) . ">";
        }
        
        if ( $depth > 0 ) {
            $depth = $IndentLimit if ( $depth > $IndentLimit );
            if (@htmlStack) {              
                # Non-empty stack
                $oldCode = pop(@htmlStack);
                
                if ( $oldCode ne $code ) {
                    my $insert2;
                    
                    if ($code eq "table"){ 
                        if ($NewTable == 2){ 
                            $insert2 = "<\/tbody>";
                            $NewTable = 0;
                        }
                    }
                    $pageHtml .= "</$oldCode>$insert2<$code>";
                }
                push( @htmlStack, $code );
            }
            
            while ( @htmlStack < $depth ) {
                push( @htmlStack, $code );
                $pageHtml .= "\n<$code $codeAttributes>";
            }
        }
        
        if ( !$ParseParas ) {
            s/^\s*$/<p>\n/;    # Blank lines become <p> tags
        }
		
        $pageHtml .= &CommonMarkup( $_, 1, 2 );    # Line-oriented common markup
    }
    
    while ( @htmlStack > 0 ) {                     
        # Clear stack
        my $insert2;

        if ($NewTable == 2){ 
            $insert2 = "<\/tbody>";
            $NewTable = 0;
        }
        
        $pageHtml .= "$insert2</" . pop(@htmlStack) . ">";
    }
    
    $NewTable = 0;
    %TableCellDefaults = {};
    
    return $pageHtml;
}

sub EvalLocalRules {
    my ( $rules, $origText, $isDiff ) = @_;
    my ( $text, $reportError, $errorText );
    
    $text        = $origText;
    $reportError = 1;

    # Basic idea: the $rules should change $text, possibly with different behavior if $isDiff is true (no images or color changes?)
    # Note: for fun, the $rules could also change $reportError and $origText
    if ( !eval $rules ) {
        $errorText = $@;
        
        if ( $errorText eq "" ) {

          # Search for "Unknown Error" for the reason the next line is commented
          #     $errorText = "Unknown Error (no error text)";
        }
        if ( $errorText ne "" ) {
            $text = $origText;    # Consider: should partial results be kept?
            
            if ($reportError) {
                $text .= "\n<hr>";
                $text .= "<b>Local rule error:</b><br/>";
                $text .= &QuoteHtml($errorText);
            }
        }
    }
    
    return $text;
}
sub UriEscape {
    my ($uri) = @_;
    
    $uri =~ s/([\x00-\x1f\x7f-\xff])/sprintf("%%%02X", ord($1))/ge;
    $uri =~ s/\&/\&amp;/g;
    
    return $uri;
}


sub QuoteHtml {
    my ($html) = @_;
    
    $html =~ s/&/&amp;/g;
    $html =~ s/</&lt;/g;
    $html =~ s/>/&gt;/g;
    $html =~ s/&amp;([#a-zA-Z0-9]+);/&$1;/g;    # Allow character references
    
    return $html;
}

sub ParseParagraph {
    my ($text) = @_;
    
	$text = &CommonMarkup( $text, 1, 0 );    # Multi-line markup
    if ($text =~ /^\<h[1|2|3|4|5|6]>.*<\\h[1|2|3|4|5|6]>$/){ return "<nowiki>$text</nowiki>"; }
	
    return "\n<p>$text</p>";
}

sub StoreInterPage {
    my ( $id, $useImage ) = @_;
    my ( $link, $extra );
    
    ( $link, $extra ) = &InterPageLink( $id, $useImage );

    # Next line ensures no empty links are stored
    $link = &StoreRaw($link) if ( $link ne "" );
    
    return $link . $extra;
}

sub InterPageLink {
    my ( $id, $useImage ) = @_;
    my ( $name, $site, $remotePage, $url, $punct );
    
    ( $id, $punct ) = &SplitUrlPunct($id);
    $name = $id;
    ( $site, $remotePage ) = split( /:/, $id, 2 );
    $url = &GetSiteUrl($site);
    
    return ( "", $id . $punct ) if ( $url eq "" );
    
    $remotePage =~ s/&amp;/&/g;    # Unquote common URL HTML
    $url .= $remotePage;
    
    return ( &UrlLinkOrImage( $url, $name, $useImage ), $punct );
}

sub StoreBracketInterPage {
    my ( $id, $text, $useImage, $options ) = @_;
    my ( $site, $remotePage, $url, $index );
    
    ( $site, $remotePage ) = split( /:/, $id, 2 );
    $remotePage =~ s/&amp;/&/g;    # Unquote common URL HTML
    $url = &GetSiteUrl($site);
    
    if ( $text ne "" ) {
        return "[$id $text]" if ( $url eq "" );
    }
    else {
        return "[$id]" if ( $url eq "" );
        $text = &GetBracketUrlIndex($id);
    }
    
    $url .= $remotePage;
    
    $text = StoreBracketUrl( $url, $text, $useImage, $options);
    
    return $text;
}

sub GetBracketUrlIndex {
    my ($id) = @_;
    my ( $index, $key );

    # Consider plain array?
    if ( $SaveNumUrl{$id} > 0 ) { return $SaveNumUrl{$id}; }
    
    $SaveNumUrlIndex++;    # Start with 1
    $SaveNumUrl{$id} = $SaveNumUrlIndex;
    
    return $SaveNumUrlIndex;
}

sub GetSiteUrl {
    my ($site) = @_;
    my ( $data, $status );
    
    if ( !$InterSiteInit ) {
        ( $status, $data ) = &ReadFile($InterFile);
        
        if ($status) {
            %InterSite = split( /\s+/, $data );    # Consider defensive code
        }

        # Check for definitions to allow file to override automatic settings
        if ( !defined( $InterSite{'LocalWiki'} ) ) {
            $InterSite{'LocalWiki'} = $ScriptName . &ScriptLinkChar();
        }
        
        if ( !defined( $InterSite{'Local'} ) ) {
            $InterSite{'Local'} = $ScriptName . &ScriptLinkChar();
        }
        
        $InterSiteInit = 1;                        # Init only once per request
    }
    
    return $InterSite{$site} if ( defined( $InterSite{$site} ) );
    return "";
}

sub StoreRaw {
    my ($html) = @_;
    
    $SaveUrl{$SaveUrlIndex} = $html;
    
    return $FS . $SaveUrlIndex++ . $FS;
}

sub StorePre {
    my ( $html, $tag ) = @_;
    
    return &StoreRaw( "<$tag>" . $html . "</$tag>" );
}

sub ReadWikiFile {
    my ($fileName) = @_;
    my ($fileData, %tempPage, %tempSection, %tempText);
    
    return unless -f $fileName;
    
    $fileData = &ReadFileOrDie($fileName);
    %tempPage = split(/$FS1/, $fileData, -1);
    %tempSection = split(/$FS2/, $tempPage{'text_default'}, -1);
    %tempText = split(/$FS3/, $tempSection{'data'}, -1);
    
    return $tempText{'text'};
}

sub WikiFileToHTML {
    my ($text) = @_;
    my ($output);
    my ($mySaveUrlIndex, $mySaveNumUrlIndex, $myTableMode, %mySaveUrl, %mySaveNumUrl);
    
    return unless $text;
    
    # Global variables do not help this code. Nasty, but easiest solution.
    %mySaveUrl= %SaveUrl;
    %mySaveNumUrl= %SaveNumUrl;
    $mySaveUrlIndex= $SaveUrlIndex;
    $mySaveNumUrlIndex = $SaveNumUrlIndex;
    $myTableMode= $TableMode;
    
    $output = &WikiToHTML($text);
    
    %SaveUrl = %mySaveUrl;
    %SaveNumUrl = %mySaveNumUrl;
    $SaveUrlIndex = $mySaveUrlIndex;
    $SaveNumUrlIndex = $mySaveNumUrlIndex;
    $TableMode = $myTableMode;
    
    return $output;
}

sub StoreTemplate {
    my ($params) = @_;    
    my $id = &GetParam( "id",     "" );
    my ($templateId, $templateFile, $templateText, $output, %substitutes);
    
    $params =~ s/^\s*(\S+)\s*/$templateId=$1,''/e;
    return &StoreRaw(T('No template name')) unless $templateId;
    
    $templateFile = &GetPageFile($templateId);
    return &StoreRaw(Ts('Template %s not found', $templateId)) unless -f $templateFile;
    
    while ($params =~ /^(\S+)\s*=(.*)$/gm) {
        $substitutes{$1} = $2;
    }
    
    $templateText = &ReadWikiFile($templateFile);
    $templateText =~ s/\$(\S+)\$/$substitutes{$1}/gi;
    $templateText =~ s/\s*{{//g; # Avoid nesting.
    $output = &WikiFileToHTML($templateText);
    
    return &StoreRaw($output);
}

sub StoreHref {
    my ( $anchor, $text ) = @_;
    return "<a" . &StoreRaw($anchor) . ">$text</a>";
}

sub StoreUrl {
    my ( $name, $useImage ) = @_;
    my ( $link, $extra );
    
    ( $link, $extra ) = &UrlLink( $name, $useImage );

    # Next line ensures no empty links are stored
    $link = &StoreRaw($link) if ( $link ne "" );
    
    return $link . $extra;
}

sub UrlLink {
    my ( $rawname, $useImage ) = @_;
    my ( $name, $punct );
    
    ( $name, $punct ) = &SplitUrlPunct($rawname);
    
    if ( $LimitFileUrl && ( $NetworkFile && $name =~ m|^file:| ) ) {

        # Only do remote file:// links. No file:///c|/windows.
        if ( $name =~ m|^file://[^/]| ) {
            return ( "<a href='$name' class='wikiurllink'>$name</a>", $punct );
        }
        
        return ( $rawname, "" );
    }
    
    return ( &UrlLinkOrImage( $name, $name, $useImage ), $punct );
}

sub UrlLinkOrImage {
    my ( $url, $name, $useImage ) = @_;
	my $css = "wikiurlorimage";
	my $target = "_top";
    
	if (!($url !~ /http:\/\// || $url =~ /wiki.kurcina.org/)){ $css .= " external"; $target='_blank'; }
	
    # Restricted image URLs so that mailto:foo@bar.gif is not an image
    if ( $useImage && &ImageAllowed($url) ) {
        return "<a href='$url' class='wikiurlorimage' target='_blank'><img class='$css' src='$url'></a>";
    }
    
    return "<a href='$url' target='$target' class='$css'>$name</a>";
}

sub ImageAllowed {
    my ($url) = @_;
    my ( $site, $imagePrefixes );
    
    $imagePrefixes = 'http:|https:|ftp:|upload:';
    $imagePrefixes .= '|file:' if ( !$LimitFileUrl );
    
    return 0 unless ( $url =~ /^($imagePrefixes).+\.$ImageExtensions$/i );
    return 0 if ( $url =~ /"/ );    #" No HTML-breaking quotes allowed
    return 1 if ( @ImageSites < 1 );             # Most common case: () means all allowed
    return 0 if ( $ImageSites[0] eq 'none' );    # Special case: none allowed

    foreach $site (@ImageSites) {
        return 1
          if ( $site eq substr( $url, 0, length($site) ) );    # Match prefix
    }
    
    return 0;
}

sub ExtensionAllowed {
    my ($file) = @_;

    return 1 if ( $file =~ /$ImageExtensions$/ );
    return 1 if ( $file =~ /$DownloadExtensions$/ );
        
    return 0;    
}

sub GetUploadUrl {
    my ($url) = @_;
    
    &StoreRaw($url);
}

sub GetOptions {
    my ($text) = @_;
    my %options;
    
    foreach my $pair (split(/\|/, $text)){
        my @keyvalues = split (/=/, $pair);
        $options{$keyvalues[0]} = $keyvalues[1];
    }
    
    return %options;    
}

sub StripBBCode {
    my ($text)= @_;
    
    $text =~ s/\[/&#91;/g;
    $text =~ s/\]/&#93;/g;
    
    return "<pre>$text<\/pre>";    
}

sub StripJavaScript {
    my ($tag, $url, $text) = @_;
    
    $url =~ s/eval//g;
    $url =~ s/alert//g;
    $url =~ s/javascript://g;
    $url =~ s/\{//g;
    $url =~ s/\}//g;
    
    if ($tag eq "email"){ return "<a href='mailto:$url'>$text<\/a>"; }
    if ($tag eq "url"){ return "<a href='$url'>$text<\/a>"; }
    if ($tag eq "img"){ return "<img src='$url' title='$text'\/>"; }
    if ($tag eq "upload"){ 
        if (&ExtensionAllowed($url)){ return  "<img src='$UploadUrl/$url' title='$text'\/>"; }
        return "<img src='DISALLOWED_EXTENSION' title='$text'\/>";    
    }
    
    return $text;
}

sub StripHTML {
    my ($text) = @_;
    
    $text =~ s/\</&lt;/g;
    $text =~ s/\>/&gt;/g;

    $text =~ s/^\s+//; #remove leading spaces
    $text =~ s/\s+$//; #remove trailing spaces
    
    return $text;
}

sub GetBBList {
    my ($type, $text) = @_;
    my ($count) = 0;
    
    $text =~ s/\[\*\](.*?)(\n|$)/<li>$1<\/li>/ig;    

    if ($type eq '1'){ return "<ol style='list-style-type:numeric;'>$text<\/ol>"; }
    if ($type eq 'a'){ return "<ol style='list-style-type:lower-alpha;'>$text</ol>"; }
    if ($type eq 'A'){ return "<ol style='list-style-type:upper-alpha;'>$text</ol>"; }
        
    return "<ol style='list-style-type:square;'>$text<\/ol>";
}

sub GetBBCode {
    my ($text) = @_;
    
    $text = &StripHTML($text);

    $text =~ s/\[code\]\s*?((.*?\s*?)*?)\s*?\[\/code\]/&StripBBCode($1)/ige;    
    $text =~ s/\[b\](.*?)\[\/b\]/<b>$1<\/b>/ig;
    $text =~ s/\[i\](.*?)\[\/i\]/<i>$1<\/i>/ig;
    $text =~ s/\[u\](.*?)\[\/u\]/<u>$1<\/u>/ig;

    # ALLOW 3 levels of nested lists
    $text =~ s/\[list=(\w?)\]\s*?((.*?\s*?)*?)\s*?\[\/list\]$/&GetBBList($1, $2)/ige;
    $text =~ s/\[list\]\s*?((.*?\s*?)*?)\s*?\[\/list\]$/&GetBBList($1, $1)/ige;
    $text =~ s/\[list=(\w?)\]\s*?((.*?\s*?)*?)\s*?\[\/list\]/&GetBBList($1, $2)/ige;
    $text =~ s/\[list\]\s*?((.*?\s*?)*?)\s*?\[\/list\]/&GetBBList($1, $1)/ige;
    $text =~ s/\[list=(\w?)\]\s*?((.*?\s*?)*?)\s*?\[\/list\]/&GetBBList($1, $2)/ige;
    $text =~ s/\[list\]\s*?((.*?\s*?)*?)\s*?\[\/list\]/&GetBBList($1, $1)/ige;    
    
    $text =~ s/\[email\](.*?)\[\/email\]/&StripJavaScript("email", $1, $1)/ige;
    $text =~ s/\[email=(.*?)\](.*?)\[\/email\]/&StripJavaScript("email", $1, $2)/ige;
    $text =~ s/\[url\](.*?)\[\/url\]/&StripJavaScript("url", $1, $1)/ige;
    $text =~ s/\[url=(.*?)\](.*?)\[\/url\]/&StripJavaScript("url", $1, $2)/ige;
    $text =~ s/\[upload\](.*?)\[\/upload]/&StripJavaScript("upload", $1, $1)/ige;
    $text =~ s/\[upload=(.*?)\](.*?)\[\/upload]/&StripJavaScript("upload", $1, $2)/ige;
    $text =~ s/\[img\](.*?)\[\/img\]/&StripJavaScript("img", $1, $1)/ige;
    $text =~ s/\[img=(.*?)\](.*?)\[\/img\]/&StripJavaScript("img", $1, $2)/ige;
    $text =~ s/\[br\]/<br\/>/ig;
    $text =~ s/\[quote\]\s*?/\quote:<blockquote>/ig;    
    $text =~ s/\[quote=(.+?)\]\s*?/QUOTE:<blockquote><cite>$1 said:<\/cite><br\/>/ig;
    $text =~ s/\s*?\[\/quote\]/<\/blockquote>/ig;

    return $text;
}

sub ComputeImageRatio {
    my ($imageName, $desiredWidth, $desiredHeight, $okayLarger) = @_;
    my $filepath = &NoDirSlash($UploadDir) . "/$imageName";
    my ($imageWidth, $imageHeight) = Image::Size::imgsize($filepath);
    
    my $ratioWidth = 1;
    my $ratioHeight = 1;
    my $ratioFinal = 1;
    
    if ($imageWidth <= 0){ $imageWidth = 100; }
    if ($imageHeight <= 0){ $imageHeight = 100; }
    
    if ($desiredWidth){ $ratioWidth = $desiredWidth/$imageWidth; }
    if ($desiredHeight){ $ratioHeight = $desiredHeight/$imageHeight; }
    
    if ($okayLarger){
        if ($ratioWidth > $ratioHeight){ $ratioFinal = $ratioWidth; }
        else { $ratioFinal = $ratioHeight; }
    }
    else {
        if ($ratioWidth > $ratioHeight){ $ratioFinal = $ratioHeight; }
        else { $ratioFinal = $ratioWidth; }
    
    }
    
    my $finalWidth = int($ratioFinal * $imageWidth);
    my $finalHeight = int($ratioFinal * $imageHeight);
    
    return ($finalWidth, $finalHeight);
}

sub StoreBracketUrl {
    my ( $url, $text, $useImage, $options ) = @_;
    my %options = &GetOptions($options);
    my $targetUrl = &NoDirSlash($UploadUrl) . "/";
    my $imageFloat;
    my $imageClear = "\n<br class='clear$options{clear}'/>";
    my $boxFloat = " float" . $options{'boxfloat'};
    my $boxClear = "\n<br class='clear$options{boxclear}'/>";
    my $width;
    my $height;
    my $title;
    my $caption;
    my $description;
    my $imageLink;
    my $boxWidth = "style='width: 300px !important;'";
	my $css = "";

    if ( $text eq "" ) { $text = &GetBracketUrlIndex($url); }
    elsif ($text =~ /^$InterLinkPattern$/) {
        my @interlink = split(/:/, $text, 2);
        $text = &GetSiteUrl($interlink[0]) . $interlink[1];
    }

    if ($options{'float'}){ $imageFloat = "float" . $options{'float'}; }
    if ($options{'clear'}){ $imageClear = "\n<br class='clear$options{clear}'/>"; }
    if ($options{'title'}){ $title = $options{title}; } else { $title = $text; }
    if ($options{'width'}){ $width = $options{'width'}; }
    if ($options{'height'}){ $height = $options{'height'}; }
            
    if ($options{'boxfloat'}){ $boxFloat = "float" . $options{'boxfloat'}; }
    if ($options{'boxclear'}){ $boxClear = "\n<br class='clear$options{boxclear}'/>"; }
    if ($options{'boxwidth'}){ $boxWidth = "style='width: $options{boxwidth} !important;'"; }
    if ($options{'caption'}){ 
        if ($options{'description'}){ $description = $options{description}; } 
        else { $description = "FIGURE " . (++$GLOBAL_imageCount); }
        
        $caption =  "\n<div class='wikibracketboxtitle image$imageFloat clearfix'>$description</div><div class='wikibracketboxdescription clearfix'>$options{caption}</div>"; 
    }
    
    if ($url =~ /$UploadPattern/){ $url = $targetUrl . $1; }    
    if ( $BracketImg && $useImage && &ImageAllowed($text) ) {        
        if ($text =~ /$UploadPattern/){
            my $imageName = $1;
            my ($imageWidth, $imageHeight) = &ComputeImageRatio($imageName, $width, $height, "");
            my $imageStyle = "style='width: $imageWidth; height: $imageHeight;'";
            
            $imageLink = $targetUrl . &GetUploadUrl($1);            
            $text = "<a href='$url' title='$title' class='wikibracketurl'><img class='wikibracketurl $imageFloat' $imageStyle src='$imageLink'></a>";
        }
        else {
            $imageLink = $text;
            $text = "<a href='$url' title='$title' class='wikibracketurl'><img class='wikibracketurl $imageFloat' src='$imageLink'></a>";
        }
        
        my $expandlink =  "<a target='_blank' class='wikiexpandimageicon' href='$imageLink' title='View source image'>&nbsp;</a>";
        
        if ($options{'caption'}){ 
            if ($options{'description'}){ $description = $options{description}; } 
            else { $description = "FIGURE " . (++$GLOBAL_imageCount); }
            
            $caption =  "\n<div class='wikibracketboxtitle image$imageFloat clearfix'>$description</div>$expandlink<div class='wikibracketboxdescription clearfix'>$options{caption}</div>"; 
        }
            
        if ($imageClear){ $text .= $imageClear; }        
                    
        if ($caption){
            $text = "\n<div title='$title' class='wikibracketbox $boxFloat' $boxWidth>$text$caption</div>";        
        }
        else {
            $text = "\n<div title='$title' class='$boxFloat'>$text</div>";    
        }
        
        if ($boxClear){ $text .= $boxClear; }
    }
    else {
		if ($text =~ /^\d+$/){ $text = "{$text}"; $css = "footnote-note"; }
		if ($url =~ /http:\/\// && $url !~ /wiki.kurcina.org/){ $text = "<a href='$url' target='_blank' title='$title' class='wikibracketurl external $css'>$text</a>"; }
		else { $text = "<a href='$url' title='$title' class='wikibracketurl $css'>$text</a>"; }

    }
    
    return &StoreRaw($text);
}

sub StoreBracketLink {
    my ( $name, $text ) = @_;
    
    return &StoreRaw( &GetPageLinkText( $name, "$text" ) );
}

sub StoreBracketAnchoredLink {
    my ( $name, $anchor, $text ) = @_;
    
    return &StoreRaw( &GetPageLinkText( "$name#$anchor", "$text" ) );
}

sub StorePageOrEditLink {
    my ( $page, $name ) = @_;
    
    if ($FreeLinks) {
        $page =~ s/^\s+//;        # Trim extra spaces
        $page =~ s/\s+$//;
        $page =~ s|\s*/\s*|/|;    # ...also before/after subpages
    }
    
    $name =~ s/^\s+//;
    $name =~ s/\s+$//;
    
    return &StoreRaw( &GetPageOrEditLink( $page, $name ) );
}

sub StoreRFC {
    my ($num) = @_;
    
    return &StoreRaw( &RFCLink($num) );
}

sub RFCLink {
    my ($num) = @_;
    
    return "<a href='http://www.faqs.org/rfcs/rfc${num}.html' class='wikirfclink'>RFC $num</a>";
}

sub StoreUpload {
    my ($url) = @_;
    
    return &StoreRaw( &UploadLink($url) );
}

sub UploadLink {
    my ($filename) = @_;
    my ( $html, $url );
    
    return $filename if ( $UploadUrl eq "" );    # No bad links if misconfigured
    
    $url  = &NoDirSlash($UploadUrl) . "/$filename";
    $html = "<a href='$url' class='wikiuploadlink' target='_blank'>";
    
    if ( &ImageAllowed($url) ) { $html .= "<img class='wikiuploadlink' src='$url' alt='upload:$filename'>"; }
    else { $html .= &GetDownloadsBox(&ExtractName($filename), $filename); }    
    
    $html .= "</a>";
    
    return $html;
}

sub StoreISBN {
    my ($num) = @_;
    
    return &StoreRaw( &ISBNLink($num) );
}

sub ISBNALink {
    my ( $num, $pre, $post, $text ) = @_;
    
    return "<a href='$pre$num$post' class='wikiisbnalink'>$text</a>";
}

sub ISBNLink {
    my ($rawnum) = @_;
    my ( $rawprint, $html, $num, $numSites, $i );
    
    $num      = $rawnum;
    $rawprint = $rawnum;
    $rawprint =~ s/ +$//;
    $num      =~ s/[- ]//g;
    $numSites = scalar @IsbnNames;    # Number of entries
    
    if ( ( length($num) != 10 ) || ( $numSites < 1 ) ) {
        return "ISBN $rawnum";
    }
    
    $html = &ISBNALink( $num, $IsbnPre[0], $IsbnPost[0], 'ISBN ' . $rawprint );
    
    if ( $numSites > 1 ) {
        $html .= " (";
        $i = 1;
        while ( $i < $numSites ) {
            $html .=
              &ISBNALink( $num, $IsbnPre[$i], $IsbnPost[$i], $IsbnNames[$i] );
            if ( $i < ( $numSites - 1 ) ) {    # Not the last site
                $html .= ", ";
            }
            $i++;
        }
        $html .= ")";
    }
    
    $html .= " " if ( $rawnum =~ / $/ );    # Add space if old ISBN had space.
    
    return $html;
}

sub SplitUrlPunct {
    my ($url) = @_;
    my ($punct);
    
    if ( $url =~ s/\"\"$// ) {  #"REMARK
        return ( $url, "" );    # Delete double-quote delimiters here
    }
    
    $punct = "";
    
    if ($NewFS) {
        ($punct) = ( $url =~ /([^a-zA-Z0-9\/\x80-\xff]+)$/ );
        $url =~ s/([^a-zA-Z0-9\/\xc0-\xff]+)$//;
    }
    else {
        ($punct) = ( $url =~ /([^a-zA-Z0-9\/\xc0-\xff]+)$/ );
        $url =~ s/([^a-zA-Z0-9\/\xc0-\xff]+)$//;
    }
    
    return ( $url, $punct );
}

sub StripUrlPunct {
    my ($url) = @_;
    my ($junk);
    
    ( $url, $junk ) = &SplitUrlPunct($url);
    
    return $url;
}

sub WikiHeadingNumber {
    my ( $depth, $text, $useNumber) = @_;
    my ( $number, $anchor );
    
    if ( --$depth > 0){

	    while ( scalar @HeadingNumbers < ( $depth - 1 ) ) {
	        push @HeadingNumbers, 1;
	        $TableOfContents .= "\n<dl><dt></dt><dd>";
	    }
	    
	    if ( scalar @HeadingNumbers < $depth ) {
	        push @HeadingNumbers, 0;
	        $TableOfContents .= "\n<dl><dt></dt><dd>";
	    }
	    
	    while ( scalar @HeadingNumbers > $depth ) {
	        pop @HeadingNumbers;
	        $TableOfContents .= "</dd></dl>";
	    }
	    
	    $HeadingNumbers[$#HeadingNumbers]++;
	    $number = ( join '.', @HeadingNumbers ) . '. ';

	    # Remove embedded links. THIS IS FRAGILE!
	    $text = &RestoreSavedText($text);	
		
		if ($text =~ /^\[\#(\w+)\]/){ 
			m/\[\#(\w+)\]\s?(.+)+\s?\=/;
			$anchor = $1;
			$text = $2;
		}
		else {
			$anchor = $text;
		}
		
		$text =~ s/\<a\s[^\>]*?\>\?\<\/a\>//si;        # No such page syntax
		$text =~ s/\<a\s[^\>]*?\>(.*?)\<\/a\>/$1/si;

		# Cook anchor by canonicalizing $text.
		$anchor =~ s/\<.*?\>//g;
		$anchor =~ s/\W/_/g;
		$anchor =~ s/__+/_/g;
		$anchor =~ s/^_//;
		$anchor =~ s/_$//;
		
	    # Last ditch effort    
	    $TableOfContents .= ('&nbsp;' x (2 * $depth)) . $number;
	    $TableOfContents .= &ScriptLink( "$OpenPageName#$anchor", $text );
	    $TableOfContents .= "</dd><dt>";
	    $TableOfContents .= "</dt><dd>";	
	}
      
    if ($useNumber) { return &StoreHref(" name='$anchor'") . $number  . $text; } 
	else { return &StoreHref(" name='$anchor'") . $text; }
}

sub WikiHeading {
    my ($pre, $depth, $text, $useNumber) = @_;
	my ( $html, $result, $sectionId, $action, $locked, $authtype, $heading, $anchor, $revised );

	if ( !defined( $SaveNumHeadings{$text} ) ){
		$GLOBAL_sectionCount++;
		$SaveNumHeadings{$text} = $GLOBAL_sectionCount;
	}
	
	$action = &GetParam("rcsource", "");
	$authtype = &CheckIsAuthUser($OpenPageName);
	$locked = (&PageIsLocked($OpenPageName, 1) || $authtype eq "1");
	$sectionId = $SaveNumHeadings{$text};

    $depth = length($depth);
    $depth = 6 if ( $depth > 6 );
	
    if ($useNumber) { $result = &WikiHeadingNumber($depth, $text, 1); } 
    else { $result = &WikiHeadingNumber($depth, $text, 0); }

	# REVISED HEADER with edit section link
	$html = $pre;
	if ($action eq "doedit" || $locked){
		$html .= "<h$depth>$result</h$depth>";
	}
	else {	
		$html .= "<h$depth>";
		$html .= "<span class='editsection'>";
		$html .= "[<a title='click to edit this section' href='$ScriptName?action=edit&id=$OpenPageName&section=$sectionId'>edit</a>]";
		$html .= "</span>";
		$html .= "<span class='headline'>$result</span>";
		$html .= "</h$depth>";
	}
	
    return $html;
}


# ==== Difference markup and HTML ====
sub GetDiffHTML {
    my ( $diffType, $id, $revOld, $revNew, $newText ) = @_;
    my ( $html, $diffText, $diffTextTwo, $priorName, $links, $usecomma );
    my ( $major, $minor, $author, $useMajor, $useMinor, $useAuthor, $cacheName );
    
    $links     = " (";
    $usecomma  = 0;
    $major     = &ScriptLinkDiff( 1, $id, "major diff", "" );
    $minor     = &ScriptLinkDiff( 2, $id, "minor diff", "" );
    $author    = &ScriptLinkDiff( 3, $id, "author diff", "" );
    $useMajor  = 1;
    $useMinor  = 1;
    $useAuthor = 1;
    $diffType  = &GetParam( "defaultdiff", 1 ) if ( $diffType == 4 );
    
    if ( $diffType == 1 ) {
        $priorName = "major";
        $cacheName = "major";
        $useMajor  = 0;
    }
    elsif ( $diffType == 2 ) {
        $priorName = "minor";
        $cacheName = "minor";
        $useMinor  = 0;
    }
    elsif ( $diffType == 3 ) {
        $priorName = "author";
        $cacheName = "author";
        $useAuthor = 0;
    }
    
    if ( $revOld ne "" ) {

        # Note: OpenKeptRevisions must have been done by caller.
        # Eventually optimize if same as cached revision
        $diffText = &GetKeptDiff( $newText, $revOld, 1 );    # 1 = get lock
        
        if ( $diffText eq "" ) {
            $diffText = "(The revisions are identical or unavailable.)";
        }
    }
    else {
        $diffText = &GetCacheDiff($cacheName);
    }
    
    $useMajor = 0 if ( $useMajor && ( $diffText eq &GetCacheDiff("major") ) );
    $useMinor = 0 if ( $useMinor && ( $diffText eq &GetCacheDiff("minor") ) );
    $useAuthor = 0 if ( $useAuthor && ( $diffText eq &GetCacheDiff("author") ) );
    $useMajor = 0 if ( ( !defined( &GetPageCache('oldmajor') ) ) || ( &GetPageCache("oldmajor") < 1 ) );
    $useAuthor = 0 if ( ( !defined( &GetPageCache('oldauthor') ) ) || ( &GetPageCache("oldauthor") < 1 ) );
    
    if ($useMajor) {
        $links .= $major;
        $usecomma = 1;
    }
    
    if ($useMinor) {
        $links .= ", " if ($usecomma);
        $links .= $minor;
        $usecomma = 1;
    }
    
    if ($useAuthor) {
        $links .= ", " if ($usecomma);
        $links .= $author;
    }
    
    if ( !( $useMajor || $useMinor || $useAuthor ) ) {
        $links .= "no other diffs";
    }
    $links .= ")";
    
    if ( ( !defined($diffText) ) || ( $diffText eq "" ) ) {
        $diffText = "<h4>No diff available</h4>";
    }
    
    if ( $revOld ne "" ) {
        my $currentRevision = "current revision";
        
        $currentRevision = "revision $revNew " if $revNew;
        $html .= "<h4>Difference (from revision $revOld to $currentRevision)</h4>";
        $html .= "$links<br/><br/>";
        $html .= &DiffToHTML($diffText);
    }
    else {
        if (
            ( $diffType != 2 )
            && (   ( !defined( &GetPageCache("old$cacheName") ) )
                || ( &GetPageCache("old$cacheName") < 1 ) )
          )
        {
            $html .= "<h4>No diff available -- this is the first $priorName revision.</h4>";
            $html .= "$links<br/><br/>";
        }
        else {
            $html .= "<h4>Difference from prior $priorName revision</h4>";
            $html .= "$links<br/><br/>";
            $html .= &DiffToHTML($diffText);
        }
    }
    @HeadingNumbers  = ();
    $TableOfContents = "";
        
    return $html;
}

sub GetCacheDiff {
    my ($type) = @_;
    my ($diffText);
    $diffText = &GetPageCache("diff_default_$type");
    $diffText = &GetCacheDiff('minor') if ( $diffText eq "1" );
    $diffText = &GetCacheDiff('major') if ( $diffText eq "2" );
    return $diffText;
}

# Must be done after minor diff is set and OpenKeptRevisions called
sub GetKeptDiff {
    my ( $newText, $oldRevision, $lock ) = @_;
    my ( %sect, %data, $oldText );
    
    $oldText = "";
    if ( defined( $KeptRevisions{$oldRevision} ) ) {
        %sect = split( /$FS2/, $KeptRevisions{$oldRevision}, -1 );
        %data = split( /$FS3/, $sect{'data'}, -1 );
        $oldText = $data{'text'};
    }
    
    return "" if ( $oldText eq "" );    # Old revision not found
    return &GetDiff( $oldText, $newText, $lock );
}

sub GetDiff {
  my $textOld = shift;
  my $textNew = shift;

  my %format = (
    paraIdent     => '<tr valign=top><td class="diff-para-ident">%text%</td><td class="diff-vertical"></td><td class="diff-para-ident">%text%</td></tr>',
    paraAdded     => '<tr valign=top><td class="diff-para-ident"></td><td class="diff-vertical"></td><td class="diff-para-added">%text%</td></tr>',
    paraDeleted   => '<tr valign=top><td class="diff-para-deleted">%text%</td><td class="diff-vertical"></td><td class="diff-para-ident"></td></tr>',
    paraChanged   => '<tr valign=top><td class="diff-para-changed-old">%text%</td><td class="diff-vertical"></td><td class="diff-para-changed-new">%text%</td></tr>',
    paraReplaced  => '<tr valign=top><td class="diff-para-deleted">%textDeleted%</td><td class="diff-vertical"></td><td class="diff-para-added">%textAdded%</td></tr>',
  
    changeContext => 1,
    changeHeader  => '<tr valign=top><td class="diff-header">Paragraph %oldFrom%</td><td class="diff-vertical">&nbsp;</td><td class="diff-header">Paragraph %newFrom%</td></tr>',
  
    spanIdent     => '<span class="diff-span-ident">%text%</span>',
    spanAdded     => '<span class="diff-span-added">%text%</span>',
    spanDeleted   => '<span class="diff-span-deleted">%text%</span>',

    processText => sub {

      my $text = shift;

      $text =~ s[&]               [&amp;]g;
      $text =~ s[<]               [&lt;]g;
      $text =~ s[>]               [&gt;]g;
      $text =~ s[\n]              [<br>\n]g;
      $text =~ s[\r]              []g;
      $text =~ s[([\t ]+)([\t ])] [('&nbsp;' x length($1)) . $2]ge;
      $text =~ s[^[\t ]]          [&nbsp;];

      return $text;
    }
  );

  my $diff = Diff::diffText($textOld, $textNew, %format);
  
  if ($diff ne "") {
    $diff =~ s[<td class="diff-para-changed-old">(.*?)</td>] [
      my $textChanged = $1;
      $textChanged =~ s[<span class="diff-span-added">.*?</span>] []gs;
      qq[<td class="diff-para-changed">$textChanged</td>];
    ]ges;
    
    $diff =~ s[<td class="diff-para-changed-new">(.*?)</td>] [
      my $textChanged = $1;
      $textChanged =~ s[<span class="diff-span-deleted">.*?</span>] []gs;
      qq[<td class="diff-para-changed">$textChanged</td>];
    ]ges;
  
    $diff = qq[<div id=wikidiffdiv><table id=wikidifftable>$diff</table></div>];
  }

  return $diff;
}

sub DiffToHTML { shift }


#------------------------------------------------------------------------------
# Database (Page, Section, Text, Kept, User) functions
#------------------------------------------------------------------------------
sub OpenNewPage {
    my ($id) = @_;
    
    %Page             = ();
    $Page{'version'}  = 3;       # Data format version
    $Page{'revision'} = 0;       # Number of edited times
    $Page{'tscreate'} = $Now;    # Set once at creation
    $Page{'ts'}       = $Now;    # Updated every edit
    $Page{'authorcreate'} = &GetParam('username',"") unless $Page{'authorcreate'} or $Page{revision}; # Set once at creation
	$Page{'description'} = &GetParam('description',"") unless $Page{'description'};
}

sub OpenNewSection {
    my ( $name, $data ) = @_;
    
    %Section             = ();
    $Section{'name'}     = $name;
    $Section{'version'}  = 1;                   # Data format version
    $Section{'revision'} = 0;                   # Number of edited times
    $Section{'tscreate'} = $Now;                # Set once at creation
    $Section{'ts'}       = $Now;                # Updated every edit    
    $Section{'host'}     = "";        			# Updated only for real edits (can be slow)    
    $Section{'data'}     = $data;
	$Section{'id'}       = $UserID;    
	$Section{'username'} = &GetParam( "username", "" );
	$Section{'ip'}       = $ENV{REMOTE_ADDR};
	
    $Page{$name}         = join( $FS2, %Section );    # Replace with save?
    $Page{'authorcreate'}= &GetParam('username',"") unless $Page{'authorcreate'} or $Page{revision}; # Set once at creation
	$Page{'description'} = &GetParam('description',"") unless $Page{'description'};
}

sub OpenNewText {
    my ($name) = @_;                          		# Name of text (usually "default")
    
    %Text = ();
    
    if ( $NewText ne "" ) { $Text{'text'} = $NewText; }
    else { $Text{'text'} = "Describe the new page here."; }
    
    $Text{'text'} 	   		.= "\n" if ( substr( $Text{'text'}, -1, 1 ) ne "\n" );
    $Text{'minor'}     		 = 0;                   # Default as major edit
    $Text{'newauthor'} 	 	 = 1;                   # Default as new author
    $Text{'summary'}   		 = "";
	$Text{'description'}   	 = "";
    
    &OpenNewSection( "text_$name", join( $FS3, %Text ) );
}

sub GetPageFile {
    my ($id) = @_;
    
    return $PageDir . "/" . &GetPageDirectory($id) . "/$id.db";
}

sub OpenPage {
    my ($id) = @_;
    my ( $fname, $data );
    
    if (!CheckIsAuthUser($id)) { $id = $AuthErrorPage; } #auth patch
	if ( $id eq ""){ return $HomePage; }
    if ( $OpenPageName eq $id ) { return; }    
        
    %Section = ();
    %Text    = ();
    $fname   = &GetPageFile($id);
    
    if ( -f $fname ) {
        $data = &ReadFileOrDie($fname);
        %Page = split( /$FS1/, $data, -1 );    # -1 keeps trailing null fields
    }
    else {
        &OpenNewPage($id);
    }
    
    if ( $Page{'version'} != 3 ) {
        &UpdatePageVersion();
    }
    
    $OpenPageName = $id;
}

sub OpenSection {
    my ($name) = @_;
    
    if ( !defined( $Page{$name} ) ) {
        &OpenNewSection( $name, "" );
    }
    else {
        %Section = split( /$FS2/, $Page{$name}, -1 );
    }
}

sub OpenText {
    my ($name) = @_;
    
    if ( !defined( $Page{"text_$name"} ) ) {
        &OpenNewText($name);
    }
    else {
        &OpenSection("text_$name");
        %Text = split( /$FS3/, $Section{'data'}, -1 );
    }
}

sub OpenDefaultText {
    &OpenText('default');
}

# Called after OpenKeptRevisions
sub OpenKeptRevision {
    my ($revision) = @_;
    
    %Section = split( /$FS2/, $KeptRevisions{$revision}, -1 );
    %Text = split( /$FS3/, $Section{'data'}, -1 );
}

sub GetPageCache {
    my ($name) = @_;
    return $Page{"cache_$name"};
}

# Always call SavePage within a lock.
sub SavePage {
    my $file = &GetPageFile($OpenPageName);
    
    $Page{'revision'} += 1;    # Number of edited times
    $Page{'ts'} = $Now;        # Updated every edit
    
    &CreatePageDir( $PageDir, $OpenPageName );
    &WriteStringToFile( $file, join( $FS1, %Page ) );
}

sub SaveSection {
    my ( $name, $data ) = @_;
    
    $Section{'revision'}   += 1;    # Number of edited times
    $Section{'ts'}       	= $Now;                          # Updated every edit
    $Section{'ip'}       	= $ENV{REMOTE_ADDR};
    $Section{'id'}       	= $UserID;
    $Section{'username'} 	= &GetParam( "username", "" );
    $Section{'data'}     	= $data;
    $Page{$name} 		 	= join( $FS2, %Section );
}

sub SaveText {
    my ($name) = @_;
    
    &SaveSection( "text_$name", join( $FS3, %Text ) );
}

sub SaveDefaultText {
    &SaveText('default');
}

sub SetPageCache {
    my ( $name, $data ) = @_;
    
    $Page{"cache_$name"} = $data;
}

sub UpdatePageVersion {
    &ReportError( "Bad page version (or corrupt page)." );
}

sub KeepFileName {
    return $KeepDir . "/"
      . &GetPageDirectory($OpenPageName)
      . "/$OpenPageName.kp";
}

sub SaveKeepSection {
    my $file = &KeepFileName();
    my $data;
    
    return if ( $Section{'revision'} < 1 );    # Don't keep "empty" revision
    $Section{'keepts'} = $Now;
    $data = $FS1 . join( $FS2, %Section );
    
    &CreatePageDir( $KeepDir, $OpenPageName );
    &AppendStringToFileLimited( $file, $data, $KeepSize );
}

sub ExpireKeepFile {
    my ( $fname, $data, @kplist, %tempSection, $expirets );
    my ( $anyExpire, $anyKeep, $expire, %keepFlag, $sectName, $sectRev );
    my ( $oldMajor, $oldAuthor );
    
    $fname = &KeepFileName();
    return if ( !( -f $fname ) );
    
    $data = &ReadFileOrDie($fname);
    @kplist = split( /$FS1/, $data, -1 );    # -1 keeps trailing null fields
    return if ( length(@kplist) < 1 );    # Also empty
    
    shift(@kplist) if ( $kplist[0] eq "" );    # First can be empty
    return if ( length(@kplist) < 1 );         # Also empty
    
    %tempSection = split( /$FS2/, $kplist[0], -1 );

    if ( !defined( $tempSection{'keepts'} ) ) {
        return;                                # Bad keep file
    }
    
    $expirets = $Now - ( $KeepDays * 24 * 60 * 60 );
    return if ( $tempSection{'keepts'} >= $expirets );    # Nothing old enough
    
    $anyExpire = 0;
    $anyKeep   = 0;
    %keepFlag  = ();
    $oldMajor  = &GetPageCache('oldmajor');
    $oldAuthor = &GetPageCache('oldauthor');
    
    foreach ( reverse @kplist ) {
        %tempSection = split( /$FS2/, $_, -1 );
        $sectName    = $tempSection{'name'};
        $sectRev     = $tempSection{'revision'};
        $expire      = 0;
        
        if ( $sectName eq "text_default" ) {
            if (   ( $KeepMajor && ( $sectRev == $oldMajor ) )
                || ( $KeepAuthor && ( $sectRev == $oldAuthor ) ) )
            {
                $expire = 0;
            }
            elsif ( $tempSection{'keepts'} < $expirets ) {
                $expire = 1;
            }
        }
        else {
            if ( $tempSection{'keepts'} < $expirets ) {
                $expire = 1;
            }
        }
        
        if ( !$expire ) {
            $keepFlag{ $sectRev . "," . $sectName } = 1;
            $anyKeep = 1;
        }
        else {
            $anyExpire = 1;
        }
    }
    
    if ( !$anyKeep ) {    # Empty, so remove file
        unlink($fname);
        return;
    }
    return if ( !$anyExpire );    # No sections expired
    
    open( OUT, ">$fname" ) or die( Ts( 'cant write %s', $fname ) . ": $!" );
    
    foreach (@kplist) {
        %tempSection = split( /$FS2/, $_, -1 );
        $sectName    = $tempSection{'name'};
        $sectRev     = $tempSection{'revision'};
        
        if ( $keepFlag{ $sectRev . "," . $sectName } ) {
            print OUT $FS1, $_;
        }
    }
    close(OUT);
}

sub OpenKeptList {
    my ( $fname, $data );
    
    @KeptList = ();
    $fname    = &KeepFileName();
    return if ( !( -f $fname ) );
    
    $data = &ReadFileOrDie($fname);
    @KeptList = split( /$FS1/, $data, -1 );    # -1 keeps trailing null fields
}

sub OpenKeptRevisions {
    my ($name) = @_;    # Name of section
    my ( $fname, $data, %tempSection );
    
    %KeptRevisions = ();
    &OpenKeptList();
    
    foreach (@KeptList) {
        %tempSection = split( /$FS2/, $_, -1 );
        next if ( $tempSection{'name'} ne $name );
        $KeptRevisions{ $tempSection{'revision'} } = $_;
    }
}

sub LoadUserData {
    my ( $data, $status );
    
    %UserData = ();
    ( $status, $data ) = &ReadFile( &UserDataFilename($UserID) );
    
    if ( !$status ) {
        $UserID = 112;    # Could not open file.  Consider warning message?
        return;
    }
    
    %UserData = split( /$FS1/, $data, -1 );    # -1 keeps trailing null fields
}

sub UserDataFilename {
    my ($id) = @_;
    
    if ($id =~ /(\d+)/){ $id = $1; }
    else { die "The userid must be a positive integer"; }
    
    return "" if ( $id < 1 );
    return $UserDir . "/" . ( $id % 10 ) . "/$id.db";
}

# ==== Misc. functions ====
sub ReportError {
    my ($errmsg) = @_;
    
    print &GetHeader( "", "ERROR!", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    print "\n<h2>$errmsg</h2>";
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub ValidId {
    my ($id) = @_;
    
    if ( length($id) > 120 ) {
        return Ts( 'Invalid Page %s (name is too long)', $id );
    }
    
    if ( $id =~ m| | ) {
        return Ts( 'Invalid Page %s (name may not contain space characters)', $id );
    }
    
    if ($UseSubpage) {
        if ( $id =~ m|.*/.*/| ) {
            return Ts( 'Invalid Page %s (too many / characters in page)', $id );
        }
        
        if ( $id =~ /^\// ) {
            return Ts( 'Invalid Page %s (subpage without main page)', $id );
        }
        
        if ( $id =~ /\/$/ ) {
            return Ts( 'Invalid Page %s (missing subpage name)', $id );
        }
    }
    
    if ($FreeLinks) {
        $id =~ s/ /_/g;
        
        if ( !$UseSubpage ) {
            if ( $id =~ /\// ) {
                return Ts( 'Invalid Page %s (/ not allowed in free-link pattern)', $id );
            }
        }
        
        if ( !( $id =~ m|^$FreeLinkPattern$| ) ) {
            return Ts( 'Invalid Page %s (improper free-link pattern)', $id );
        }
        
        if ( $id =~ m|\.db$| ) {
            return Ts( 'Invalid Page %s (free-link must not end with .db)', $id );
        }
        
        if ( $id =~ m|\.lck$| ) {
            return Ts( 'Invalid Page %s (free-link must not end with .lck)', $id );
        }
        
        return "";
    }
    else {
        if ( !( $id =~ /^$LinkPattern$/ ) ) {
            return Ts( 'Invalid Page %s (improper name pattern)', $id );
        }
    }
    
    return "";
}

sub ValidIdOrDie {
    my ($id) = @_;
    my $error;
    
    $error = &ValidId($id);
    
    if ( $error ne "" ) {
        &ReportError($error);
        return 0;
    }
    
    return 1;
}

sub UserCanEdit {
    my ( $id, $deepCheck ) = @_;
    my $authtype = &CheckIsAuthUser($id);
    
    # Optimized for the "everyone can edit" case (don't check passwords)
    if ( ( $id ne "" ) && ( -f &GetLockedPageFile($id) ) ) {
        return 1 if ( &UserIsAdmin() );    # Requires more privledges
             # Consider option for editor-level to edit these pages?
        return 0;
    }
    
    if ( !$EditAllowed ) {
        return 1 if ( $authtype eq "2" || $authtype eq "3");
        return 1 if ( &UserIsEditor() );
        return 0;
    }
    
    if ( -f "$DataDir/noedit" ) {
        return 1 if ( $authtype eq "2" || $authtype eq "3");
        return 1 if ( &UserIsEditor() );
        return 0;
    }
    
    if ($deepCheck) {    # Deeper but slower checks (not every page)
        return 1 if ( $authtype eq "2" || $authtype eq "3");
        return 1 if ( &UserIsEditor() );
        return 0 if ( &UserIsBanned() );
    }
    
    return 1;
}

sub UserIsBanned {
    my ( $host, $ip, $data, $status );
    
    ( $status, $data ) = &ReadFile("$DataDir/banlist");
    return 0 if ( !$status );    # No file exists, so no ban
    
    $data =~ s/\r//g;
    $ip   = $ENV{'REMOTE_ADDR'};
    $host = &GetRemoteHost(0);
    
    foreach ( split( /\n/, $data ) ) {
        next if ( (/^\s*$/) || (/^#/) );    # Skip empty, spaces, or comments
        return 1 if ( $ip   =~ /$_/i );
        return 1 if ( $host =~ /$_/i );
    }
    
    return 0;
}

sub UserIsAdmin {
    my ( @pwlist, $userPassword );
    
    return 0 if ( $AdminPass eq "" );
    $userPassword = &GetParam( "adminpw", "" );
    return 0 if ( $userPassword eq "" );
    
    foreach ( split( /\s+/, $AdminPass ) ) {
        next     if ( $_            eq "" );
        return 1 if ( $userPassword eq $_ );
    }
    
    return 0;
}

sub UserIsEditor {
    my ( @pwlist, $userPassword );
    
    return 1 if ( &UserIsAdmin() );    # Admin includes editor
    return 0 if ( $EditPass eq "" );
    $userPassword = &GetParam( "password", "" );    # Used for both
    return 0 if ( $userPassword eq "" );
    
    foreach ( split( /\s+/, $EditPass ) ) {
        next     if ( $_            eq "" );
        return 1 if ( $userPassword eq $_ );
    }
    
    return 0;
}

sub UserIsEditorOrAdmin {
    return (UserIsEditor || UserIsAdmin);    
}

sub UserCanUpload {
    return 1 if ( &UserIsEditor() );
    return $AllUpload;
}

sub GetLockedPageFile {
    my ($id) = @_;
    return $PageDir . "/" . &GetPageDirectory($id) . "/$id.lck";
}

sub RequestLockDir {
    my ( $name, $tries, $wait, $errorDie ) = @_;
    my ( $lockName, $n );
    
    &CreateDir($TempDir);
    $lockName = $LockDir . $name;
    $n        = 0;
    
    while ( mkdir( $lockName, 0555 ) == 0 ) {
        if ( $! != 17 ) {
            die( Ts( 'can not make %s', $LockDir ) . ": $!\n" ) if $errorDie;
            return 0;
        }
        return 0 if ( $n++ >= $tries );
        sleep($wait);
    }
    return 1;
}

sub ReleaseLockDir {
    my ($name) = @_;
    rmdir( $LockDir . $name );
}

sub RequestLock {

    # 10 tries, 3 second wait, possibly die on error
    return &RequestLockDir( "main", 10, 3, $LockCrash );
}

sub ReleaseLock {
    &ReleaseLockDir('main');
}

sub ForceReleaseLock {
    my ($name) = @_;
    my $forced;

    # First try to obtain lock (in case of normal edit lock)
    # 5 tries, 3 second wait, do not die on error
    $forced = !&RequestLockDir( $name, 5, 3, 0 );
    &ReleaseLockDir($name);    # Release the lock, even if we didn't get it.
    return $forced;
}

sub RequestCacheLock {

    # 4 tries, 2 second wait, do not die on error
    return &RequestLockDir( 'cache', 4, 2, 0 );
}

sub ReleaseCacheLock {
    &ReleaseLockDir('cache');
}

sub RequestDiffLock {

    # 4 tries, 2 second wait, do not die on error
    return &RequestLockDir( 'diff', 4, 2, 0 );
}

sub ReleaseDiffLock {
    &ReleaseLockDir('diff');
}

# Index lock is not very important--just return error if not available
sub RequestIndexLock {

    # 1 try, 2 second wait, do not die on error
    return &RequestLockDir( 'index', 1, 2, 0 );
}

sub ReleaseIndexLock {
    &ReleaseLockDir('index');
}

sub ReadFile {
    my ($fileName) = @_;
    my ($data);
    
    local $/ = undef;    # Read complete files
    if ( open( IN, "<$fileName" ) ) {
        $data = <IN>;
        close IN;
        return ( 1, $data );
    }
    return ( 0, "" );
}

sub ReadFileOrDie {
    my ($fileName) = @_;
    my ( $status, $data );
    
    ( $status, $data ) = &ReadFile($fileName);
    if ( !$status ) {
        die( Ts( 'Can not open %s', $fileName ) . ": $!" );
    }
    return $data;
}

sub WriteStringToFile {
    my ( $file, $string ) = @_;
    
    open( OUT, ">$file" ) or die( Ts( 'cant write %s', $file ) . ": $!" );
    print OUT $string;
    close(OUT);
}

sub AppendStringToFile {
    my ( $file, $string ) = @_;
    
    open( OUT, ">>$file" ) or die( Ts( 'cant write %s', $file ) . ": $!" );
    print OUT $string;
    close(OUT);
}

sub AppendStringToFileLimited {
    my ( $file, $string, $limit ) = @_;
    
    if ( ( $limit < 1 ) || ( ( ( -s $file ) + length($string) ) <= $limit ) ) {
        &AppendStringToFile( $file, $string );
    }
}

sub CreateDir {
    my ($newdir) = @_;
    mkdir( $newdir, 0775 ) if ( !( -d $newdir ) );
}

sub CreatePageDir {
    my ( $dir, $id ) = @_;
    my $subdir;
    
    &CreateDir($dir);    # Make sure main page exists
    $subdir = $dir . "/" . &GetPageDirectory($id);
    &CreateDir($subdir);
    
    if ( $id =~ m|([^/]+)/| ) {
        $subdir = $subdir . "/" . $1;
        &CreateDir($subdir);
    }
}

sub UpdateHtmlCache {
    my ( $id, $html ) = @_;
    my $idFile;
    
    $idFile = &GetHtmlCacheFile($id);
    &CreatePageDir( $HtmlDir, $id );
    
    if ( &RequestCacheLock() ) {
        &WriteStringToFile( $idFile, $html );
        &ReleaseCacheLock();
    }
}

sub GenerateAllPagesList {
    my ( @pages, @dirs, $id, $dir, @pageFiles, @subpageFiles, $subId );
    
    @pages = ();
    if ($FastGlob) {
        # The following was inspired by the FastGlob code by Marc W. Mengel.
        # Thanks to Bob Showalter for pointing out the improvement.
        opendir( PAGELIST, $PageDir );
        @dirs = readdir(PAGELIST);
        closedir(PAGELIST);
        @dirs = sort(@dirs);
        
        foreach $dir (@dirs) {
            next if ( substr( $dir, 0, 1 ) eq '.' );  # No ., .., or .dirs or files
            
            opendir( PAGELIST, "$PageDir/$dir" );
            @pageFiles = readdir(PAGELIST);
            closedir(PAGELIST);
            
            foreach $id (@pageFiles) {
                next if ( ( $id eq '.' ) || ( $id eq '..' ) );
                
                if (substr( $id, -3 ) eq '.db') {
                    push( @pages, substr( $id, 0, -3 ) );
                }
                elsif ( substr( $id, -4 ) ne '.lck' ) {
                    opendir( PAGELIST, "$PageDir/$dir/$id" );
                    @subpageFiles = readdir(PAGELIST);
                    closedir(PAGELIST);
                    
                    foreach $subId (@subpageFiles) {
                        if ( substr( $subId, -3 ) eq '.db' ) {
                            push( @pages, "$id/" . substr( $subId, 0, -3 ) );
                        }
                    }
                }
            }
        }
    }
    else {
        # Old slow/compatible method.
        @dirs = qw(A B C D E F G H I J K L M N O P Q R S T U V W X Y Z other);
        
        foreach $dir (@dirs) {
            if ( -e "$PageDir/$dir" ) {    # Thanks to Tim Holt
                while (<$PageDir/$dir/*.db $PageDir/$dir/*/*.db>) {
                    s|^$PageDir/||;
                    m|^[^/]+/(\S*).db|;
                    $id = $1;
                    push( @pages, $id );
                }
            }
        }
    }
    
    return sort(@pages);
}

sub AllPagesList {
    my ( $rawIndex, $refresh, $status, $stale );
    
	$refresh = &GetParam("refresh", 0 );	
	$stale = &CalcIsStaleFile($IndexFile);
	
	if ($stale){ $refresh = 1; }
    if ( !$UseIndex ) { return &GenerateAllPagesList(); }
    
    $refresh = &GetParam( "refresh", 0 );
    if ( $IndexInit && !$refresh ) {

        # Note for mod_perl: $IndexInit is reset for each query
        # Eventually consider some timestamp-solution to keep cache?
        return @IndexList;
    }
    
    if ( ( !$refresh ) && ( -f $IndexFile ) ) {
        ( $status, $rawIndex ) = &ReadFile($IndexFile);
        
        if ($status) {
            %IndexHash = split( /\s+/, $rawIndex );
            @IndexList = sort( keys %IndexHash );
            $IndexInit = 1;
            
            return @IndexList;
        }

        # If open fails just refresh the index
    }
    
    @IndexList = ();
    %IndexHash = ();
    @IndexList = &GenerateAllPagesList();
    
    foreach (@IndexList) { $IndexHash{$_} = 1; }
    
    $IndexInit = 1;    # Initialized for this run of the script
                       # Try to write out the list for future runs
    &RequestIndexLock() or return @IndexList;
    &WriteStringToFile( $IndexFile, join( " ", %IndexHash ) );
    &ReleaseIndexLock();
    
    return @IndexList;
}

sub AllSubPagesList {
    my $GivenPage = shift;
    my @PageList = &AllPagesList();
    my @Results;
    
    foreach (@PageList){
        if (/^$GivenPage\//i){
            push @Results, $_;    
        }
    }
    
    return @Results;
}

sub CalcIsStaleFile {
	my ($filename) = @_;
	my ($dev, $ino, $mode, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks) = stat($filename);
	
	my $currentTime = time();
	my $maxSec = 30;
	my $diffSec = $currentTime - $mtime;
	
	if ($diffSec > $maxSec){ return 1; }
	else { return 0; }	
}

sub CalcDay {
    my ($ts) = @_;
    
    $ts += $TimeZoneOffset;
    my ( $sec, $min, $hour, $mday, $mon, $year ) = localtime($ts);
    
    if ($NumberDates) {
        $year = $year + 1900;
        $mon = $mon + 1;
        if ($mon < 10){ $mon = "0$mon"; }
        if ($mday < 10){ $mday = "0$mday"; }
        
        return "$year$NumberDatesDelim$mon$NumberDatesDelim$mday";
    }
    
    return (
        "January",   "February", "March",    "April",
        "May",       "June",     "July",     "August",
        "September", "October",  "November", "December"
      )[$mon]
      . " "
      . $mday . ", "
      . ( $year + 1900 );
}

sub CalcTime {
    my ($ts) = @_;
    my ( $ampm, $mytz );
    
    $ts += $TimeZoneOffset;
    
    my ( $sec, $min, $hour, $mday, $mon, $year ) = localtime($ts);
    $mytz = "";
    
    if ( ( $TimeZoneOffset == 0 ) && ( $ScriptTZ ne "" ) ) {
        $mytz = " " . $ScriptTZ;
    }
    $ampm = "";
    
    if ($UseAmPm) {
        $ampm = " am";
        if ( $hour > 11 ) {
            $ampm = " pm";
            $hour = $hour - 12;
        }
        $hour = 12 if ( $hour == 0 );
    }
	else {
		$hour = "0" . $hour if ( $hour < 10 );
	}
    
    $min = "0" . $min if ( $min < 10 );
    
    return $hour . ":" . $min . $ampm . $mytz;
}

sub TimeToText {
    my ($t) = @_;
    
    return &CalcDay($t) . " " . &CalcTime($t);
}

sub GetParam {
    my ( $name, $default ) = @_;
    my $result;
    
    $result = $q->param($name);
    
    if ( !defined($result) ) {
        if ( defined( $UserData{$name} ) ) {
            $result = $UserData{$name};
        }
        else {
            $result = $default;
        }
    }
    
    return $result;
}

sub GetHiddenValue {
    my ( $name, $value ) = @_;
    
    $q->param( $name, $value );
    
    return $q->hidden($name);
}

sub GetRemoteHost {
    my ($doMask) = @_;
    my ( $rhost, $iaddr );
    
    $rhost = $ENV{REMOTE_HOST};
    
    if ( $UseLookup && ( $rhost eq "" ) ) {

        # Catch errors (including bad input) without aborting the script
        eval 'use Socket; $iaddr = inet_aton($ENV{REMOTE_ADDR});'
          . '$rhost = gethostbyaddr($iaddr, AF_INET)';
    }
    
    if ( $rhost eq "" ) {
        $rhost = $ENV{REMOTE_ADDR};
    }
    
    $rhost = &GetMaskedHost($rhost) if ($doMask);
    
    return $rhost;
}

sub FreeToNormal {
    my ($id) = @_;
    
    $id =~ s/ /_/g;
    $id = ucfirst($id) if ( $UpperFirst || $FreeUpper );
    
    if ( index( $id, '_' ) > -1 ) {    # Quick check for any space/underscores
        $id =~ s/__+/_/g;
        $id =~ s/^_//;
        $id =~ s/_$//;
        
        if ($UseSubpage) {
            $id =~ s|_/|/|g;
            $id =~ s|/_|/|g;
        }
    }
    
    if ($FreeUpper) {
        # Note that letters after ' are *not* capitalized
        if ( $id =~ m|[-_.,\(\)/][a-z]| ) { # Quick check for non-canonical case
            $id =~ s|([-_.,\(\)/])([a-z])|$1 . uc($2)|ge;
        }
    }
    
    return $id;
}
#------------------------------------------------------------------------------
# END_OF_BROWSE_CODE
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Page-editing and other special-action code
#------------------------------------------------------------------------------
$OtherCode = "";    # Comment next line to always compile (slower)
#$OtherCode = <<'# END_OF_OTHER_CODE';

#------------------------------------------------------------------------------
sub DoOtherRequest {
    my ( $id, $action, $filter, $text, $search );
    
    $action = &GetParam( "action", "" );
    $id     = &GetParam( "id",     "" );
    $filter = &GetParam( "filter", "" );
    
    if ( $action ne "" ) {
        $action = lc($action);
        
        if ( $action eq "edit" ) { &DoEdit( $id, 0, 0, "", 0 ) if &ValidIdOrDie($id); }
        elsif ( $action eq "unlock" ) { &DoUnlock(); }
        elsif ( $action eq "index" ) { &DoIndex(); }
        elsif ( $action eq "links" ) { &DoLinks(); }
        elsif ( $action eq "maintain" ) { &DoMaintain(); }
        elsif ( $action eq "pagelock" ) { &DoPageLock(); }
        elsif ( $action eq "editlock" ) { &DoEditLock(); }
        elsif ( $action eq "editprefs" ) { &DoEditPrefs(); }
        elsif ( $action eq "editbanned" ) { &DoEditBanned(); }
        elsif ( $action eq "editlinks" ) { &DoEditLinks(); }
        elsif ( $action eq "login" ) { &DoEnterLogin(); }
        elsif ( $action eq "newlogin" ) { $UserID = 0; &DoEditPrefs(); }
        elsif ( $action eq "version" ) { &DoShowVersion(); }
        elsif ( $action eq "rss" ) { &DoRss(); }
        elsif ( $action eq "delete" ) { &DoDeletePage($id); }
        elsif ( $action eq "maintainrc" ) { &DoMaintainRc(); }
        elsif ( $action eq "convert" ) { &DoConvert(); }
        elsif ( $action eq "trimusers" ) { &DoTrimUsers(); }
        elsif ( $action eq "listfiles" ) { &DoListFiles($id, $filter, 0); }
        elsif ( $action eq "listdisabled" ) { &DoListFiles($id, $filter, 1); }
        
        elsif ( $UseUpload && ( $action eq "upload" ) ) { &DoUpload(""); }
        else { &ReportError( Ts( 'Invalid action parameter %s', $action ) ); }
        
        return;
    }
    
    if ( &GetParam( "edit_prefs", 0 ) ) {
        &DoUpdatePrefs();
        return;
    }
    
    if ( &GetParam( "edit_ban", 0 ) ) {
        &DoUpdateBanned(); return;
    }
    
    if ( &GetParam( "enter_login", 0 ) ) {
        &DoLogin(); return;
    }
    
    if ( &GetParam( "edit_links", 0 ) ) {
        &DoUpdateLinks(); return;
    }
    
    if ( $UseUpload && ( &GetParam( "upload", 0 ) ) ) {
        &SaveUpload();
        return;
    }
    
    $search = &GetParam( "search", "" );
    
    if ( ( $search ne "" ) || ( &GetParam( "dosearch", "" ) ne "" ) ) {
        &DoSearch($search, $filter);
        return;
    }
    else {
        $search = &GetParam( "back", "" );
        
        if ( $search ne "" ) {
            &DoBackLinks($search, $filter);
            
            return;
        }
    }

    # Handle posted pages
    if ( &GetParam( "oldtime", "" ) ne "" ) {
        $id = &GetParam( "title", "" );
        &DoPost() if &ValidIdOrDie($id);
        
        return;
    }
    
    &ReportError( "Invalid URL." );
}

sub PageIsLocked {
    my ($id, $deepedit) = @_;
    my ($result) = 0;
    
    if ( !&UserCanEdit( $id, $deepedit ) ) {
            $result = 1;
        if ( &UserIsBanned() ) {
            $result = 2;
        }
        else {
            $result = 3;
        }
    }
    
    return $result;
}

sub DoEdit {
    my ( $id, $isConflict, $oldTime, $newText, $preview ) = @_;
    my ( $header, $editRows, $userName, $revision, $oldText, $html, $description, $descriptionHtml );
    my ( $summary, $isEdit, $pageTime, $isLocked, $newfile, $appendRev );
    
    my $authtype = &CheckIsAuthUser($id);
    if (!$authtype) { $id = $AuthErrorPage; } 
	if ($id eq ""){ return $HomePage; }
    if ($FreeLinks) { $id = &FreeToNormal($id); }  
    
	$isLocked = &PageIsLocked( $id, 1 );
	$newfile = 0;
		
    # Consider sending a new user-ID cookie if user does not have one
    &OpenPage($id);
    &OpenDefaultText();
	
	$oldText = $Text{'text'};
	$description 	= &GetParam("description", $Page{'description'});
	
	$descriptionHtml = "\n<br/><b>" . T('Description of this page:') . "</b>";
    $descriptionHtml .=
      $q->textfield(
        -name      => 'description',
        -id        => 'descriptiontext',
        -default   => $description,
        -override  => 1,
        -size      => 60,
        -maxlength => 200
      );
	$descriptionHtml .= "<br/>\n";	
	
	if ($Section{'revision'} == 0 && ( !-f &GetPageFile($id) )){ $newfile = 1; }    
    if ( $preview && !$isConflict ) { $oldText = $newText; }
    
    $editRows = &GetParam("editrows", 20 );
	$editRows = 20 if ( $editRows > 20 );
	
    $revision = &GetParam('revision', "" );
    $revision =~ s/\D//g;    # Remove non-numeric chars
	
    $pageTime = $Section{'ts'};
    $header   = Ts( 'Editing %s', $id );
	
	$html = "";

	if ($revision){ $appendRev = " [ version $revision ]"; }	
    if ( $isLocked > 0 or $authtype eq "" || $authtype eq "1") {        
        if ( $isLocked == 2 ) {
		    $html .= &GetHeader( "", "Editing Denied", "" );
			$html .= &GetLeftNav();
			$html .= "\n<div class='wikiadmin'>";
            $html .= "\n<h2>Editing not allowed: user, ip, or network is blocked.</h2>";
            $html .= "\nContact the wiki administrator for more information.";
        }
        else {
		    $html .= &GetHeader( "", "Viewing $id", "" );
	        $html .= &GetLeftNav();
	        $html .= "\n<div class='wikiadmin'>";
            $html .= "\n<h2>Editing not allowed: $id $appendRev is read-only.</h2>";
			$html .= "You'll need to sign in as either an Editor to modify this page.<br/><br/>";			
			$html .= &GetTextArea( 'text', $oldText, $editRows, 1 );
			$html .= $descriptionHtml;
        }
        
        $html .= "\n</div>";
        $html .= &GetFooterText();
        $html .= "\n</div></div></div></div></body></html>";
		
		print $html;
            
        return;
    }
    
    if ( $revision ne "" ) {
        &OpenKeptRevisions('text_default');
        
        if ( !defined( $KeptRevisions{$revision} ) ) {
            $revision = "";
        }
        else {
            &OpenKeptRevision($revision);
            $header = Ts( 'Editing revision %s of ', $revision ) . $id;
        }
    }
	
	if ($newfile){
		if ($id =~ /^$LinkPattern$/){ $header   = Ts( 'Creating %s', $id ); }
		elsif (&UserIsEditorOrAdmin()){ $header   = Ts( 'Creating %s', $id ); }
		else {
	        $html .= &GetHeader( "", "Page Creation Denied", "" );
	        $html .= &GetLeftNav();
	        $html .= "\n<div class='wikiadmin'>";
			$html .= "\n<h2>Creating the page '$id' is disallowed for Guests.</h2>";
			$html .= "\nYou must sign in as an " . &ScriptLink("EditorRole", "editor") . " or ";
			$html .= "\n" . &ScriptLink("AdminRole", "administrator") . " to create pages that are not named as " . &ScriptLink("WikiWord", "WikiWords") . ". ";
			$html .= "\nPlease visit the " . &ScriptLink( "action=editprefs", "Preferences" ) . " page to set your username and password.";	        
	        $html .= "\n</div>";
			
			$html .= &GetSimpleFooterText();
			
	        $html .= "\n</div></div></div></div></body></html>";
			
			print $html;
	            
	        return;			
		}
	}
    
    $oldText = $Text{'text'};
    
    if ( $preview && !$isConflict ) { $oldText = $newText; }
    
    $editRows = &GetParam( "editrows", 20 );
	
    $html .= &GetHeader($id, &QuoteHtml($header), "");
    $html .= &GetLeftNav();
    $html .= "\n<div class='wikiadmin'>";
    
    if ( $revision ne "" ) {
        $html .= "\n<div class='warning'><b>Editing old revision $revision. Saving this page will replace the latest revision with this text.</b></div><br/>";
    }
    
    if ($isConflict) {
        $editRows = 25 if ( $editRows > 25 );
        $html .= "\n<H1>Edit Conflict!</H1>";
        
        if ( $isConflict > 1 ) {

            # The main purpose of a new warning is to display more text
            # and move the save button down from its old location.
            $html .= "\n<h2>(This is a new conflict)</h2>";
        }
        
        $html .= "\n<p><strong>";
        $html .= "\nSomeone saved this page after you started editing. ";
        $html .= "\nThe top textbox contains the saved text. ";
        $html .= "\nOnly the text in the top textbox will be saved.";
        $html .= "\n</strong></p><br/>";
        $html .= "\nScroll down to see your edited text.";
        $html .= "\n<br/>";
        $html .= "\nLast save time: ";
        $html .= &TimeToText($oldTime);
        $html .= "\n(Current time is: ";
        $html .= &TimeToText($Now);
        $html .= "\n)<br/>";
    }

    $html .= &GetEditBar();
    $html .= "\n<form id='wikiform' action='$ScriptName#preview-anchor' enctype='application/x-www-form-urlencoded' method='POST'>";
    $html .= &GetHiddenValue( "title",   $id );
    $html .= &GetHiddenValue( "oldtime",     $pageTime );
    $html .= &GetHiddenValue( "oldconflict", $isConflict );
    $html .= &GetHiddenValue( "rcsource", "doedit" );
      
    if ( $revision ne "" ) {
        $html .= &GetHiddenValue( "revision", $revision );
    }
        
	$html .= &GetTextArea( 'text', $oldText, $editRows, 0 );
	$html .= $descriptionHtml;
    if ($newfile){ $summary = &GetParam( "summary", T('Initial draft.') ); }
	else { $summary = &GetParam( "summary", "*" ); }
    
    $html .= "\n<div id='wikisaveedit'>";
	$html .= "<b>" . T('Summary of changes:') . "</b>";
    $html .=
      $q->textfield(
        -name      => 'summary',
        -id        => 'summarytext',
        -default   => $summary,
        -override  => 1,
        -size      => 60,
        -maxlength => 200
      );

    # ALLOW minor edits to Editors and Admins
    if (&UserIsEditorOrAdmin() && $newfile == 0){
        if ( &GetParam("recent_edit") eq "on" ) {
            $html .= "\n<br/>" . $q->checkbox(
                -name    => 'recent_edit',
                -checked => 1,
                -label   => T('This change is a minor edit.')
              );
            $html .= "\n<br/>";
        }
        else {
            $html .= "\n<br/>" . $q->checkbox(
                -name  => 'recent_edit',
                -checked => 0,
                -label => T('This change is a minor edit.')
              );
            $html .= "\n<br/>";
        }
    }
    
    if ($EmailNotify) {
		if ($newfile){
			$html .= "\n" . $q->checkbox(
	            -name  => 'do_email_notify',
	            -label => Ts( 'Send email notification that %s has been created.', $id )
			);
		}
		else {
			$html .= "\n" . $q->checkbox(
	            -name  => 'do_email_notify',
	            -label => Ts( 'Send email notification that %s has been changed.', $id )
			);
		}
    }
    
    $html .= "\n<br/><br/>";
    
    if ( $EditNote ne "" ) { $html .= $EditNote . '<br/>'; }
    $userName = &GetParam( "username", "" );
    
    $html .= $q->submit( -name => 'Preview', -value => 'Preview' );
    $html .= $q->button( -name => 'Cancel', -value => 'Cancel', -onclick => 'window.location="' . $ScriptName . '?' . $id . '";' );
    $html .= "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" . $q->submit( -name => 'Save', -value => "Save" );  
    
    if ( $userName ne "" ) {
        $html .= "\n (Your user name is ";
        $html .= &GetPageLinkText("$UserPagePrefix$userName", $userName);
        $html .= "\n )";
    }
    else {
        $html .= ' (' . Ts('Visit %s to set your user name.', &GetPrefsLink(), 1) . ') ';
    }

    if ($isConflict) {
        $html .= "\n<br/><hr><p><strong>";
        $html .= "\nThis is the text you submitted:";
        $html .=  "</strong><p>";
        
		$html .= &GetTextArea( 'newtext', $newText, $editRows, 0 );
		$html .= $descriptionHtml;
    }
    
    $html .= "\n</div>";
    $html .= "\n</form>";
    $html .= "<a name='preview-anchor'></a>";
    $html .= "\n</div>";            
    $html .= "\n$WikiLineFooter";
    
    if ($preview) {
        $html .= "\n<div class='wikipreviewtitle'>Preview only, not yet saved <a href='#top' title='click to jump to top of page'>[top]</a></div>";
        $html .= $WikiLineHeaderPreview;
        $html .= "\n<div id='wikipreview' class='wikipreview'>";    
                    
        if ($isConflict) {
            $html .= "\n<b>NOTE: This preview shows the revision of the other author.</b><hr>";
        }
        
        $MainPage = $id;
        $MainPage =~ s|/.*||;    # Only the main page name (remove subpage)
        
        $html .= &WikiToHTML($oldText);        
		$html .= &GetFooterReferences();
        $html .= "\n</div>";
        $html .= "\n$WikiLineFooter";
        $html .= "\n<div class='wikipreviewtitle'>Preview only, not yet saved <a href='#top' title='click to jump to top of page'>[top]</a></div>";
        $html .= "\n<div id='wikibar'>&nbsp</div>";
    }

	if ($newfile){  $html .= &GetSimpleFooterText(); }
	else { $html .= &GetFooterText(); }
	
    $html .= "\n</div></div></div></body></html>";

	print $html;
}

sub GetTextArea {
    my ( $name, $text, $rows, $readOnly ) = @_;
    my ( $html );
    
    $html = "\n<div style='width: 100%;'>";

	if ($readOnly){
		$html .= $q->textarea(
			-name     => $name,
			-default  => $text,
			-id       => 'wikitextarea' . $name,
			-rows     => $rows,
			-columns  => 80,
			-override => 1,
			-style    => 'width:100%; color: #777777; border: 1px solid #ff0000;',
			-wrap     => 'virtual',
			-readonly => $readOnly
		);
	}
	else {
		$html .= $q->textarea(
			-name     => $name,
			-default  => $text,
			-id       => 'wikitextarea' . $name,
			-rows     => $rows,
			-columns  => 80,
			-override => 1,
			-style    => 'width:100%',
			-wrap     => 'virtual'
		);  
	}
	
    $html .= "</div>";
    
    return $html;
}

sub DoEditPrefs {
    my ( $check, $recentName, $lastUrl, %labels, $action, $html );
    
	$action = &GetParam ("action", "");
	$html = "";

    $recentName = $RCName;
    $recentName =~ s/_/ /g;
    
    &DoNewLogin() if ( $UserID < 400 );
	
    if ($action ne "newlogin"){ $html .= &GetHeader( "", "Editing Preferences", "" ); }
	else { $html .= &GetHeader( "", "Session Login", "" ); }
    
    $html .= &GetLeftNav();
    $html .= "\n<div class='wikiadmin'>";
    $html .= "\n<h2>Access Controls</h2>";
    $html .= "\n<form id='wikiform' action='$ScriptName' enctype='application/x-www-form-urlencoded' method='POST'>";
    $html .= &GetHiddenValue( "previous_url", $ENV{HTTP_REFERER} );
    $html .= &GetHiddenValue( "edit_prefs", 1 );
    $html .= "\n<table class='wikilargelist'>";
    $html .= "\n<tr><th colspan='2'><b>User Information </b></th></tr>";
    $html .= "\n<tr><td class='first'>Your User ID number </td><td>$UserID</td></tr>";
    $html .= "\n<tr><td class='first'>UserName</td>";
    $html .= "\n<td>" . &GetFormText( 'username', "", 30, 50 );
    $html .= "\n<br/>(blank to remove, or valid page name)</td></tr>";
    $html .= "\n<tr><td class='first'>Set Password </td>";
    $html .= "\n<td>";
    
    $html .=
      $q->password_field(
        -name      => 'p_password',
        -value     => '*',
        -size      => 30,
        -maxlength => 50
      );
     $html .= "\n<br/>(blank to remove password)";
     $html .= "\n<br/>Passwords allow sharing preferences between multiple systems. Passwords are completely optional. ";
     $html .= "\n</td></tr>";

    if ( ( $AdminPass ne "" ) || ( $EditPass ne "" ) ) {
        $html .= "\n<tr><td class='first'>Administrator Password </td>";
        $html .= "\n<td>";
		$html .=
          $q->password_field(
            -name      => 'p_adminpw',
            -value     => '*',
            -size      => 30,
            -maxlength => 50
          );
        $html .= "\n<br/>(blank to remove password)";
        $html .= "\n<br/>(Administrator passwords are used for special maintenance.)";
        $html .= "\n</td></tr>";
    }
    
    if ($EmailNotify) {
        $html .= "\n<tr><td class='first'>Email Address</td>";
        $html .= "\n<td>" . &GetFormText( 'email', "", 30, 60 );
        $html .= "\n<br/>" . &GetFormCheck( 'notify', 1, T('Include this address in the site email list.') );
        $html .= "\n<br/>(Uncheck the box to remove the address.) ";
        
        $html .= "\n</td></tr>";
    }
    
    $html .= "\n</table>";
    
    
    $html .= "<fieldset>";
    $html .= "<legend><b>$recentName</b></legend>";    
    $html .= "\nDefault days to display: " . &GetFormText( 'rcdays', $RcDefault, 4, 9 );
    $html .= "\n<br/><br/>" . &GetFormCheck( 'rcchangehist', 1, T('Use &quot;changes&quot; as link to history') );
    $html .= "\n<br/>" . &GetFormCheck( 'rcnewtop', $RecentTop, T('Most recent changes on top') );
    $html .= "\n<br/>" . &GetFormCheck( 'rcall', 0, T('Show all changes (not just most recent)') );
    
    %labels = (
        0 => "Hide minor edits",
        1 => "Show minor edits",
        2 => "Show only minor edits"
    );
    
    $html .= "\n<br/><br/>Minor edit display: ";
    $html .= $q->popup_menu(
        -name   => 'p_rcshowedit',
        -values => [ 0, 1, 2 ],
        -labels => \%labels,
        -default => &GetParam( "rcshowedit", $ShowEdits )
    );
    $html .= "</fieldset>";

    if ($UseDiff) {
        $html .= "<br/><fieldset>";
        $html .= "<legend><b>Differences</b></legend>"; 

		%labels = ( 1 => "Major", 2 => "Minor", 3 => "Author" );
        
        $html .= "\nDefault difference type: ";
        $html .= $q->popup_menu(
            -name   => 'p_defaultdiff',
            -values => [ 1, 2, 3 ],
            -labels => \%labels,
            -default => &GetParam( "defaultdiff", 1 )
        );
		
        $html .= "<br/><br/>\n" . &GetFormCheck( 'diffrclink', 1, "Show (diff) links on $recentName " );
        $html .= "\n<br/>" . &GetFormCheck( 'alldiff', 0, "Show differences on all pages" );
        $html .= "\n<br/>" . &GetFormCheck( 'norcdiff', 1, "No differences on $recentName " );
        
        
        $html .= "</fieldset>";
    }
    
    $html .= "<br/><fieldset>";
    $html .= "<legend><b>Misc</b></legend>";
    
    # Note: TZ offset is added by TimeToText, so pre-subtract to cancel.
    $html .= "\nServer time: ";
    $html .= &TimeToText( $Now - $TimeZoneOffset );
    $html .= "\n ";
	$html .= GetFormText( 'tzoffset', 0, 4, 9 );
	$html .= " GMT";
    
    $html .= "\n<br/><br/>Edit area rows: ";
	$html .= &GetFormText( 'editrows', 20, 4, 4 );
    $html .= "\n<br/>" . &GetFormCheck( 'toplinkbar', 1, "Show link bar on top" );
	$html .= "\n<br/>" . &GetFormCheck( 'bottomlinkbar', 0, "Show link bar on bottom" );
	$html .= "\n<br/>" . &GetFormCheck( 'extrasearchform', 0, "Show additional search form" );
    $html .= "\n<br/>" . &GetFormCheck( 'linkrandom', 0, "Add 'Random Page' link to link bar" );

    $html .= "\n<br/><br/>StyleSheet URL: ";

    $html .= &GetCssChoices();
    $html .= "</fieldset>";
    
    $html .= "\n<br/><br/><input type='button' name='Cancel' value='Cancel' onclick='history.go(-1);'>";
    $html .= "\n<input type='reset' name='Reset' style='margin-right: 20px;'>";    
    $html .= $q->submit( -name => 'Save', -value => "Save" );
    
    $html .= "\n</form>";
    $html .= "\n</div>";
    $html .= &GetFooterText();
    
    $html .= "\n</div></div></div></body></html>";

	print $html;
}

sub GetFormText {
    my ( $name, $default, $size, $max ) = @_;
    my $text = &GetParam( $name, $default );
    
    return $q->textfield(
        -name      => "p_$name",
        -default   => $text,
        -override  => 1,
        -size      => $size,
        -maxlength => $max
    );
}

sub GetFormCheck {
    my ( $name, $default, $label ) = @_;
    my $checked = ( &GetParam( $name, $default ) > 0 );
    
    return $q->checkbox(
        -name     => "p_$name",
        -override => 1,
        -checked  => $checked,
        -label    => $label
    );
}

sub DoUpdatePrefs {
    my ( $username, $password, $stylesheet, $lastUrl );

    $stylesheet = &GetParam( 'p_stylesheet', "" );

    if ( $stylesheet eq "" ) {
        undef $UserData{'stylesheet'};
    }
    else {
        $stylesheet =~ s/[">]//g;  # Remove characters that would cause problems"
        $UserData{'stylesheet'} = $stylesheet;
    }
    
    # All link bar settings should be updated before printing the header
	&UpdatePrefCheckbox("toplinkbar");
	&UpdatePrefCheckbox("bottomlinkbar");
    &UpdatePrefCheckbox("extrasearchform");
    &UpdatePrefCheckbox("linkrandom");
    
    print &GetHeader( "", "Saving Preferences" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    
    if ( $UserID < 1001 ) {
        print "\n<h2>Invalid UserID $UserID, preferences not saved.</h2>";
        
        if ( $UserID == 111 ) {
            print "\n<br/>(Preferences require cookies, but no cookie was sent.)";
        }
        
        print "\n</div>";
        print &GetFooterText();
        print "\n</div></div></div></div></body></html>";
        
        return;
    }
    
    $username = &GetParam( "p_username", "" );
    
    if ($FreeLinks) {
        $username =~ s/^\[\[(.+)\]\]/$1/;    # Remove [[ and ]] if added
        $username = &FreeToNormal($username);
        $username =~ s/_/ /g;
    }
    
    if ( $username eq "" ) {
        print "\n<h2>UserName removed.</h2>";
        undef $UserData{'username'};
    }
    elsif ( ( !$FreeLinks ) && ( !( $username =~ /^$LinkPattern$/ ) ) ) {
        print Ts( '<h2>Invalid UserName %s: not saved.', $username ), "</h2>";
    }
    elsif ( $FreeLinks && ( !( $username =~ /^$FreeLinkPattern$/ ) ) ) {
        print Ts( '<h2>Invalid UserName %s: not saved.', $username ), "</h2>";
    }
    elsif ( length($username) > 50 ) {    # Too long
        print "\n<h2>UserName must be 50 characters or less. (not saved)</h2>";
    }
    else {
        print "\n<h2>UserName $username saved.</h2>";
        print "\nUserID is $UserID\.<br/>";
        $UserData{'username'} = $username;
    }
    
    $password = &GetParam( "p_password", "" );
    
    if ( $password eq "" ) {
        print "\nPassword removed.<br/>";
        undef $UserData{'password'};
    }
    elsif ( $password ne "*" ) {
        print "\nPassword changed.<br/>";
        $UserData{'password'} = $password;
    }
    
    if ( ( $AdminPass ne "" ) || ( $EditPass ne "" ) ) {
        $password = &GetParam( "p_adminpw", "" );
        
        if ( $password eq "" ) {
            print "\nAdministrator password removed.<br/>";
            undef $UserData{'adminpw'};
        }
        elsif ( $password ne "*" ) {
            print "\nAdministrator password changed.<br/>";
            $UserData{'adminpw'} = $password;
            
            if ( &UserIsAdmin() ) {
                print "\nUser has administrative abilities.<br/>";
            }
            elsif ( &UserIsEditor() ) {
                print "\nUser has editor abilities.<br/>";
            }
            else {
                print "\nUser does not have administrative abilities. (Password does not match administrative password(s).) <br/>";
            }
        }
    }
    
    if ($EmailNotify) {
        &UpdatePrefCheckbox("notify");
        &UpdateEmailList();
    }
    
    &UpdatePrefNumber( "rcdays", 0, 0, 999999 );
    &UpdatePrefCheckbox("rcnewtop");
    &UpdatePrefCheckbox("rcall");
    &UpdatePrefCheckbox("rcchangehist");
    
    if ($UseDiff) {
        &UpdatePrefCheckbox("norcdiff");
        &UpdatePrefCheckbox("diffrclink");
        &UpdatePrefCheckbox("alldiff");
        &UpdatePrefNumber( "defaultdiff", 1, 1, 3 );
    }
    
    &UpdatePrefNumber( "rcshowedit", 1, 0,    2 );
    &UpdatePrefNumber( "tzoffset",   0, -999, 999 );
    &UpdatePrefNumber( "editrows",   1, 1,    999 );
    
    print "\nServer time: ";
    print &TimeToText( $Now - $TimeZoneOffset );
    print "\n<br/>";
    
    $TimeZoneOffset = &GetParam( "tzoffset", 0 ) * ( 60 * 60 );
    
    print"Local time: ";
    print &TimeToText($Now);
    print "\n<br/>";

    if ( $stylesheet eq "" ) {
        if ( &GetParam( 'stylesheet', "" ) ne "" ) {
            print "\nStyleSheet URL removed.<br/>";
        }
    }
    else {
        print "\nStyleSheet setting saved.<br/>";
    }
    
    &SaveUserData();
    
    print "\nPreferences saved.<br/>";
    print "\n<br/>click <a href='" . &GetParam("previous_url") . "' title='jumps two pages back via the browser history list'>here</a> to continue to prior page.";    
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

#------------------------------------------------------------------------------ 
# add or remove email address from preferences to $EmailFile
#------------------------------------------------------------------------------
sub UpdateEmailList {
    my (@old_emails);
    local $/ = "\n";               # don't slurp whole files in this sub.
    
    if ( my $new_email = $UserData{'email'} = &GetParam( "p_email", "" ) ) {
        my $notify = $UserData{'notify'};
        
        if ( -f $EmailFile ) {
            open( NOTIFY, $EmailFile ) or die( Ts( 'Could not read from %s:', $EmailFile ) . " $!\n" );
            @old_emails = <NOTIFY>;
            close(NOTIFY);
        }
        else {
            @old_emails = ();
        }
        
        my $already_in_list = grep /$new_email/, @old_emails;
        
        if ( $notify and ( not $already_in_list ) ) {
            &RequestLock() or die( "Could not get mail lock" );
            
            if ( !open( NOTIFY, ">>$EmailFile" ) ) {
                &ReleaseLock();    # Don't leave hangling locks
                die( "Could not append to $EmailFile : $!\n" );
            }
            
            print NOTIFY $new_email, "\n";
            close(NOTIFY);
            
            &ReleaseLock();
        }
        elsif ( ( not $notify ) and $already_in_list ) {
            &RequestLock() or die( "Could not get mail lock" );
            
            if ( !open( NOTIFY, ">$EmailFile" ) ) {
                &ReleaseLock();
                die( "Could not overwrite $EmailFile : $!\n" );
            }
            foreach (@old_emails) {
                print NOTIFY "$_" unless /$new_email/;
            }
            
            close(NOTIFY);
            &ReleaseLock();
        }
    }
}

sub UpdatePrefCheckbox {
    my ($param) = @_;
    my $temp = &GetParam( "p_$param", "*" );
    
    $UserData{$param} = 1 if ( $temp eq "on" );
    $UserData{$param} = 0 if ( $temp eq "*" );

    # It is possible to skip updating by using another value, like "2"
}

sub UpdatePrefNumber {
    my ( $param, $integer, $min, $max ) = @_;
    my $temp = &GetParam( "p_$param", "*" );
    
    return if ( $temp eq "*" );
    
    $temp =~ s/[^-\d\.]//g;
    $temp =~ s/\..*// if ($integer);
    
    return if ( $temp eq "" );
    return if ( ( $temp < $min ) || ( $temp > $max ) );
    
    $UserData{$param} = $temp;
}

sub DoIndex {
    print &GetHeader( "", "Index of all pages", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    print PrintPageList( "", "", &AllPagesList() );
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

#------------------------------------------------------------------------------
# Create a new user file/cookie pair
#------------------------------------------------------------------------------
sub DoNewLogin {
    # Consider warning if cookie already exists (maybe use "replace=1" parameter)
    &CreateUserDir();
    $SetCookie{'id'}      = &GetNewUserId();
    $SetCookie{'randkey'} = int( rand(1000000000) );
    $SetCookie{'rev'}     = 1;
	$SetCookie{'stylesheet'} = &GetParam ('stylesheet');
    %UserCookie           = %SetCookie;
    $UserID               = $SetCookie{'id'};

    # The cookie will be transmitted in the next header
    %UserData               = %UserCookie;
    $UserData{'createtime'} = $Now;
    $UserData{'createip'}   = $ENV{REMOTE_ADDR};
    &SaveUserData();
}

sub DoEnterLogin {
    print &GetHeader( "", "Login", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    print "\n<h2>Enter UserID</h2>";
    print "\n<form id='wikiform' action='$ScriptName' enctype='application/x-www-form-urlencoded' method='POST'>";
    
    print &GetHiddenValue( 'enter_login', 1 );
    
    print "\n<table><tr>";
    print "\n<td>User ID number &nbsp;</td>";
    print "\n<td>";
    print
      $q->textfield(
        -name      => 'p_userid',
        -value     => "",
        -size      => 15,
        -maxlength => 50
      );
    print "\n</td>";
    print "\n<tr>";
    print "\n<td>Password  &nbsp;</td>";
    print "\n<td>";
    print
      $q->password_field(
        -name      => 'p_password',
        -value     => "",
        -size      => 15,
        -maxlength => 50
      );
    print "\n</td>";
    print "\n</tr></table><br/>";
    print $q->submit( -name => 'Login', -value => 'Login' );
    print "\n<br/></form></div>";
    print &GetFooterText();
    print "\n</div></div></div></body></html>";    
}

sub DoLogin {
    my ( $uid, $password, $success );
    
    $success = 0;
    $uid = &GetParam( "p_userid", "" );
    $uid =~ s/\D//g;
    $password = &GetParam( "p_password", "" );
    
    print &GetHeader( "", "Login Results", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    
    if ( ( $uid > 199 ) && ( $password ne "" ) && ( $password ne "*" ) ) {
        $UserID = $uid;

        &LoadUserData();

        if ( $UserID > 199 ) {
            if ( defined( $UserData{'password'} ) && ( $UserData{'password'} eq $password ) ) {
                $SetCookie{'id'}      = $uid;
                $SetCookie{'randkey'} = $UserData{'randkey'};
                $SetCookie{'rev'}     = 1;
                $success              = 1;
            }
            else {
                print "\nUserID Account Undefined<br/>";
            }
        }
        else {
        	if ( $UserID == 112 ){ print "Could not locate data file for UserID $uid.  It is likely that it was trimmed from the database." }
        	else { print "\nUserID must be above 199<br/>"; }
        }
    }
    
    
    if ($success) {
        print "\n<h2>Login for user ID $uid complete.</h2>";
    }
    else {
        print "\n<h2>Login for user ID $uid failed.</h2>";
    }
    
    print "\n</div>";
    print &GetFooterText;
    print "\n</div></div></div></body></html>";    
}

sub GetNewUserId {
    my ($id);
    
    $id = $StartUID;
    
    while ( -f &UserDataFilename( $id + 1000 ) ) {
        $id += 1000;
    }
    
    while ( -f &UserDataFilename( $id + 100 ) ) {
        $id += 100;
    }
    
    while ( -f &UserDataFilename( $id + 10 ) ) {
        $id += 10;
    }
    
    &RequestLock() or die( "Could not get user-ID lock" );
    
    while ( -f &UserDataFilename($id) ) {
        $id++;
    }
    
    &WriteStringToFile( &UserDataFilename($id), "lock" );    # reserve the ID
    &ReleaseLock();
    
    return $id;
}

# Consider user-level lock?
sub SaveUserData {
    my ( $userFile, $data );
    
    &CreateUserDir();
    $userFile = &UserDataFilename($UserID);
    $data = join( $FS1, %UserData );
    &WriteStringToFile( $userFile, $data );
}

sub CreateUserDir {
    my ( $n, $subdir );
    
    if ( !( -d "$UserDir/0" ) ) {
        &CreateDir($UserDir);
        
        foreach $n ( 0 .. 9 ) {
            $subdir = "$UserDir/$n";
            &CreateDir($subdir);
        }
    }
}

sub DoSearch {
    my ($string, $filter) = @_;
    my ( $title, $titlesOnly, $useRegex, $constraint, $originalString );
    
    if ( $string eq "" ) {
        &DoIndex();
        return;
    }
    
	my @results = &SearchTitleAndBody($string, $filter, "");
	$titlesOnly = $q->param('titlesonly');
	$useRegex = $q->param('regex');

	if (scalar(@results) == 0){ 
		$originalString = $string;
		$originalString =~ s/ //g;
		@results = &SearchTitleAndBody($originalString, $filter, ""); 
	}

	if (scalar(@results) == 1 && $titlesOnly ne "" && $results[0] eq $string){ &ReBrowsePage( $results[0], "", 0 ); }
	
	$constraint = "Search for";
	if ($useRegex ne ""){ $constraint .= " via RegEx"; }
	if ($titlesOnly ne ""){ $constraint .= " titles"; }
	
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	$filter =~ s/^\s+//;
	$filter =~ s/\s+$//;
	
    print &GetHeader( "", &QuoteHtml( "$constraint: $title " . Ts( '%s', $string ) ), "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
	print PrintPageList( $filter, $string, @results );
	
	if (scalar(@results) > 0){
	    print "\n<form id='wikiform' action='$ScriptName' method='POST'>";
	    print "\n<br/>Naming filter:<br/><input type='text' name='filter' value='$filter' title='Enter ! before search term for exclusion'>&nbsp;";
	    print "\n<input type='hidden' name='search' value='$string'>";
	    print "\n<input type='hidden' name='dosearch' value='1'>";
		print "\n<input type='hidden' name='regex' value='$useRegex'>";  
		print "\n<input type='hidden' name='titlesonly' value='$titlesOnly'>";  	
	    print "\n<input type='submit' value='Apply Filter'>";    
	    print "\n</form>";
	}
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub DoBackLinks {
    my ($string, $filter) = @_;
    my ($title, @results);
    
    $title = $string;

    # At this time the backlinks are mostly a renamed search.
    # An initial attempt to match links only failed on subpages and free links.
    # Escape some possibly problematic characters:
    
    # $string =~ s/([_ ])/( |_)/g; # APPARENTLY makes underscores become spaces, and spaces become underscores; weird.
    $string =~ s/([-'(),])/\\$1/g; #'REMARK
    $string =~ m,/, ? "\\b$string\\b" : "$string\\b";
    
	@results =  grep($_ !~ $title, $filter, &SearchTitleAndBody($string, $filter, 0));
	
    print &GetHeader( "", &QuoteHtml( T( 'Backlinks for ')) . $title, ""  );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";    
    print PrintPageList( "", "", @results);
	
	if (scalar(@results) > 0){
	    print "\n<form id='wikiform' action='$ScriptName' method='POST'>";
	    print "\n<br/>Naming filter:<br/><input type='text' name='filter' value='$filter' title='Enter ! before search term for exclusion'>&nbsp;";
	    print "\n<input type='hidden' name='back' value='$string'>";
	    print "\n<input type='submit' value='Apply Filter'>";    
	    print "\n</form>";
	}
	
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub PrintPageList {
    my ($filter, $pageId, @results) = @_;
    my $term;
    my $pagename;
    my $html = "";
    my $pagecount = scalar(@results);
    my $currentInitial = "";
    my $thisInitial;
    my $lastInitial;
    my $letterGrouping = "";
    my $currentParent = "";
    my $linktext = "";
    my $notFirst;
	my $letterCount = 0;
	my $letterIndexCount = 0;
	my $newColumn = 0;
	my $letterIndex = 0;
	my $showDescriptions = 0;
	my $totalFound = scalar(@results);
	my $isBackLink = &GetParam("back", "");

    if ($filter ne ""){ $term = ": using filter '<em>$filter</em>'"; }
	
	if ($totalFound == 0){ $html .= "<h2>" . T('Page Not Found') . "$term</h2>"; }
	else { 
		if ( $isBackLink){ $html .= "<h2>" . ($totalFound - 1) . " pages found $term</h2>"; }
		else { $html .= "<h2>$totalFound pages found $term</h2>"; }
	}
	
	if ($totalFound == 0 && ($pageId =~ /$LinkPattern/ )){
		unless (-f &GetPageFile($pageId) or $filter ne ""){
			$html .= "The page <b>$pageId</b> doesn't yet exist.  Click " . &ScriptLink( "action=edit&id=$pageId", "here" ) . " to create this page.";
		}
	}
	else {
		if ($totalFound == 0) { $html .= "The search term <b>$pageId</b> returned no query results."; }
		else { $html .= "The search term <b>$pageId</b> returned these results."; }
	}

	
	foreach $pagename (@results) {
		$thisInitial = substr($pagename,0,1);
		
		if ($thisInitial ne $lastInitial) {
			$lastInitial = $thisInitial;
			$letterCount++;
		}
	}
	
	$letterGrouping = ($pagecount > 25);
	$showDescriptions = ($pagecount <= 25);
	
    if ($letterGrouping) {
        $html .= "<h4 class='lettergroup'>";
		$lastInitial = "";
		
        foreach $pagename (@results) {
            $thisInitial = substr($pagename,0,1);
			
            if ($thisInitial ne $lastInitial) {
				$html .= "<a href='#letter".$thisInitial."'>$thisInitial</a> ";
				$lastInitial = $thisInitial;
            }
        }
		
        $html .= "</h4><br/><br/>";
    }
    
	$html .= "<table class='wikipagesfound'><tr valign='top'><td>";
    for ($letterIndex = 0; $letterIndex < scalar(@results); $letterIndex++){
		$pagename = $results[$letterIndex];
		
        if ($letterGrouping) {
            $thisInitial = substr($pagename,0,1);
			
            if ($currentInitial ne $thisInitial) {
			
				if ($letterIndexCount >= ($letterCount /2 )){
					unless ($newColumn){
						$newColumn = 1;
						$html .= "</td><td>"; 
					}
				}
				
				$html .= "\n<h3 class='lettergroup'><a name='letter$thisInitial'> $thisInitial </h3>$WikiLine";
                
                $currentInitial = $thisInitial; 
                $notFirst = 0;
				$letterIndexCount++;
            }
        }
		
        $html .= "   ";
        if (not($pagename =~ m|(.*)/(.*)|)) {
            $currentParent = $pagename;
            $linktext = $pagename;
        } 
        else {
            if ($1 eq $currentParent) {
                if ($letterGrouping){  $linktext = "$currentParent/$2";}
                else { $html .= "... "; $linktext = "/$2";}                
            } 
            else {
                $linktext = $pagename;
            }
        }
		
        if ($notFirst){ $notFirst = 1; $linktext = ", $linktext"; }
        $html .= &GetPageLinkText($pagename,$linktext);

		if ($showDescriptions){ $html .= &GetPageDescription($pagename); }
        if ($letterGrouping){ $html .= ", "; }
        else { $html .= "\n<br/>"; }	
    }

    $html .= "</td></tr></table>";
    $html .= "\n<br/>";
    
    return $html;
}

sub DoLinks {    
    print &GetHeader( "", &QuoteHtml( "Full Link List" ), "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    print "\n<h2>Links found:</h2>";

    print &PrintLinkList(&GetFullLinkList(
        &GetParam("unique", 1),
        &GetParam("sort", 1),
        &GetParam("page", 1),
        &GetParam("inter", 0),
        &GetParam("url", 0),
        &GetParam("exists", 2),
        &GetParam("empty", 0),
        &GetParam("search", "")
    ));
    
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub PrintLinkList {
    my ( $pagelines, $page,  $names, $editlink, $isLocked );
    my ( $link, $text, $extra, @links, %pgExists, $rowNum );
    
    %pgExists = ();
    
    foreach $page (&AllPagesList()) {
        $pgExists{$page} = 1;
    }
    
    $names    = &GetParam( "names",    1 );
    $editlink = &GetParam( "editlink", 0 );

    $text .= "\n<table id='tablesorter-997' class='wikilargelist tablesorter'>";
    $text .= "\n<thead><tr><th>#</th><th>Page Name</th><th>Locked&nbsp;</th><th>Links</th></tr></thead>";
    $text .= "\n<tbody>";
    
    foreach $pagelines (@_) {
        @links = ();
        
        foreach $page ( split( ' ', $pagelines ) ) {
            if ( $page =~ /\:/ ) {    # URL or InterWiki form
            
                # DISALLOW images
                if ( $page =~ /$UrlPattern/ ) { ( $link, $extra ) = &UrlLink( $page, 0 ); }
                else { ( $link, $extra ) = &InterPageLink( $page, 0 ); }
            }
            else {
                if ( $pgExists{$page} ) {
                    $link = &GetPageLink($page);
                }
                else {
                    $link = $page;
                    
                    if ($editlink) { $link = &GetEditLink( $page, "?" ); }
                    else { $link = &GetCreateNewLink( $page, $page ); }
                }
            }
            
            push( @links, $link );
        }
        
        if ( !$names ) { shift(@links); }
		
		$page = shift(@links);
        if ( $page =~ /locked/ ) { $isLocked = "Y"; }
		else { $isLocked = "-"; }
		
        $rowNum++;
        $text .= "\n<tr><td>$rowNum</td>";
		$text .= "\n<td class='first'>$page</td>";
		$text .= "\n<td align='center'>$isLocked</td>"; 
        $text .= "\n<td>" . join(', ', @links) . "</td></tr>\n";
    }
    
    $text .= "\n</tbody></table>";
    $text .= "\n<script>\$(document).ready(function(){ \$('\#tablesorter\-997').tablesorter({widgets: ['zebra']}); });<\/script>";
    
    return $text;
}

sub GetFullLinkList {
    my ($unique, $sort, $pagelink, $interlink, $urllink, $exists, $empty, $search, $listWantedPages )= @_ ;
    my ($name, $link );
    my (@found, @links, @newlinks, @pglist, %pgExists, %seen, $main);
    
    if ( ( $interlink == 2 ) || ( $urllink == 2 ) ) { $pagelink = 0; }
    
    %pgExists = ();
    @pglist   = &AllPagesList();
    
    foreach $name (@pglist) { $pgExists{$name} = 1; }
    %seen = ();
    
    foreach $name (@pglist) {
        @newlinks = ();
        
        if ( $unique != 2 ) { %seen = (); }
        
        @links = &GetPageLinks($name, $pagelink, $interlink, $urllink, $listWantedPages);
        
        foreach $link (@links) {      
            if ($link =~ m/^\//){
                $name =~ m/(.*)\//;
                
                if ($1){ $link = $1 . $link; }
                else { $link = $name . $link; }
            }
            
            $seen{$link}++;
            
            if ( ( $unique > 0 ) && ( $seen{$link} != 1 ) ) { next; }            
            if ( ( $exists == 0 ) && ( $pgExists{$link} == 1 ) ) { next; }            
            if ( ( $exists == 1 ) && ( $pgExists{$link} != 1 ) ) { next; }            
            if ( ( $search ne "" ) && !( $link =~ /$search/ ) ) { next; }
            
            push( @newlinks, $link );
        }
        
        @links = @newlinks;
        if ($sort) { @links = sort(@links); }
        
        unshift( @links, $name );
        
        if ( $empty || ( $#links > 0 ) ) {    # If only one item, list is empty.
            push( @found, join( ' ', @links ) );
        }
    }
    
    return @found;
}

sub GetEditBar {
    my $html = "";

    $html .= "\n<div id='wikieditbar'>";
	$html .= "<a href='$ScriptName?WikiMarkup' target='_blank'>WikiMarkup</a> | ";
    $html .= "<a href='$ScriptName?WikiStyleGuide' target='_blank'>WikiStyleGuide</a> | ";
    $html .= "<a href='$ScriptName?WikiHeadings' target='_blank'>WikiHeadings</a> | ";
    $html .= "<a href='$ScriptName?WikiTOCs' target='_blank'>WikiTOCs</a> | ";
    $html .= "<a href='$ScriptName?WikiURLs' target='_blank'>WikiURLs</a> | ";
    $html .= "<a href='$ScriptName?WikiImages' target='_blank'>WikiImages</a> | ";
    $html .= "<a href='$ScriptName?WikiTables' target='_blank'>WikiTables</a> | ";
    $html .= "<a href='$ScriptName?WikiLists' target='_blank'>WikiLists</a> | ";
    $html .= "<a href='$ScriptName?WikiGallery' target='_blank'>WikiGallery</a> | ";
    $html .= "<a href='$ScriptName?WikiFlash' target='_blank'>WikiFlash</a> | ";
    $html .= "<a href='$ScriptName?WikiTemplates' target='_blank'>WikiTemplates</a> | ";
    $html .= "<a href='$ScriptName?WikiUploads' target='_blank'>WikiUploads</a> | ";
    $html .= "<a href='$ScriptName?WikiCodeBox' target='_blank'>WikiCodeBox</a> | ";
	$html .= "<a href='$ScriptName?WikiCommands' target='_blank'>WikiCommands</a>";
    $html .= "\n</div>";
    
    return $html;    
}
sub GetSubpages {
    my ($parentPage) = @_;
    my ($dir, @subpageFiles, @pages, $subId);
    
    return "" unless $parentPage;
    $dir = GetPageDirectory($parentPage);
    
    opendir(PAGELIST, "$PageDir/$dir/$parentPage") or return "";
    @subpageFiles = readdir(PAGELIST);
    closedir(PAGELIST);
    
    foreach $subId (@subpageFiles) {
        if (substr($subId, -3) eq '.db') {
          push(@pages, "$parentPage/" . substr($subId, 0, -3));
        }
    }
    return @pages;
}

sub GetPageList {
    my ($pagename, $retval);
    my (@list) = @_;

    foreach $pagename (@list) {
    ##    $retval .= ".... " if ($pagename =~ m|/|);
        $retval .= "&nbsp;" . &GetPageLink($pagename) . "<br/>";
    }

    return $retval;
}

sub GetPageLinks {
    my ( $name, $pagelink, $interlink, $urllink, $listWantedPages ) = @_;
    my ( $text, @links );
    
    @links = ();
    &OpenPage($name);
    &OpenDefaultText();
    
    $text = $Text{'text'};
    $text =~ s/<html>((.|\n)*?)<\/html>/ /ig;
    $text =~ s/<nowiki>(.|\n)*?\<\/nowiki>/ /ig;
    $text =~ s/<pre>(.|\n)*?\<\/pre>/ /ig;
    $text =~ s/<tt>(.|\n)*?\<\/tt>/ /ig;
    
    if ($interlink) {
        $text =~ s/''+/ /g;    # Quotes can adjacent to inter-site links
        $text =~ s/$InterLinkPattern/push(@links, &StripUrlPunct($1)), ' '/ge;
    }
    else {
        $text =~ s/$InterLinkPattern/ /g;
    }
    
    if ($urllink) {
        $text =~ s/''+/ /g;    # Quotes can adjacent to URLs
        $text =~ s/$UrlPattern/push(@links, &StripUrlPunct($1)), ' '/ge;
    }
    else {
        $text =~ s/$UrlPattern/ /g;
    }
    
    if ($pagelink) {
        if ($FreeLinks) {
            my $f2 = $FreeLinkPattern;
            
            $text =~ s/\[\[$f2\|[^\]]+\]\]/push(@links, &FreeToNormal($1)), ' '/ge;
            $text =~ s/\[\[$f2\]\]/push(@links, &FreeToNormal($1)), ' '/ge;
        }
        
        if ($listWantedPages){ $text =~ s/\[((.|\n)*?)\]/ /ig; }
            
        if ($WikiLinks) {
            $text =~ s/$LinkPattern/push(@links, &StripUrlPunct($1)), ' '/ge;
        }
    }
    
    return @links;
}

sub DoPost {
    my ( $editDiff, $old, $newAuthor, $pgtime, $oldrev, $preview, $user, $newfile, $oldDescription, $summaryDescription );
	
    my $string      = &GetParam( "text",     undef );
    my $id          = &GetParam( "title",       "" );
    my $summary     = &GetParam( "summary",     "" );
    my $oldtime     = &GetParam( "oldtime",     "" );
    my $oldconflict = &GetParam( "oldconflict", "" );
	my $description = &GetParam( "description", "" );
	
    my $isEdit      = 0;
    my $editTime    = $Now;
    my $authorAddr  = $ENV{REMOTE_ADDR};
	
	if ($Section{'revision'} == 0 && ( !-f &GetPageFile($id) )){ $newfile = 1; }    
	if ($FreeLinks){ $id = &FreeToNormal($id); }
    if ($id =~ /($LinkPattern)/){ $id = $1; }    
    
    if ( !&UserCanEdit( $id, 1 ) ) {
        # This is an internal interface--we don't need to explain
        &ReportError( Ts( 'Editing not allowed for %s.', $id ) );
        return;
    }
    
    if (($id eq   'SampleUndefinedPage')    ||
        ($id eq T('SampleUndefinedPage'))   ||
        ($id eq   'Sample_Undefined_Page')  ||
        ($id eq T('Sample_Undefined_Page'))){
		
		&ReportError(Ts('%s cannot be defined.', $id));
		return;
    }

	# SUMMARY FIELD
    $summary = &RemoveFS($summary);
    $summary =~ s/[\r\n]//g;
    if ( length($summary) > 300 ) {  $summary = substr( $summary, 0, 300 ); }
	
	# DESCRIPTION FIELD
    $description = &RemoveFS($description);
    $description =~ s/[\r\n]//g;
    if ( length($description) > 300 ) {  $description = substr( $description, 0, 300 ); }
	
	# TRIM WHITE-SPACE and BLANK LINES
	$string  = &RemoveFS($string);
	$string =~ s/\s*(\r?\n)+$//g;
	$string =~ s/(\r?\n){2,}(\S)/$1$1$2/g;
    
    # Add a newline to the end of the string (if it doesn't have one)
    $string .= "\n" if ( !( $string =~ /\n$/ ) );
	
	# AUTO-SIGNATURE; cooks signature into saved file unless preview mode
	unless ($preview){
		my $signature = &GetParam("username", "");       
		my $idLink = "<b>$UserPagePrefix$signature</b>";
		my $timestamp = "<i>" . &TimeToText($Now) . "</i>";
		my $sigNorm = "";
		my $sigTime = "";
		
		$signature =~ s/ /_/g;
		$sigNorm = "[[$idLink $signature]]";
		$sigTime = "[[$idLink $signature] $timestamp]";
		
		unless ($signature){ $signature = "<b>Guest</b>"; $idLink = &GetRemoteHost(); $sigNorm = "[$signature\@$idLink]"; $sigTime = "[$signature\@$idLink $timestamp]"; }   
		$string =~ s/\~\~\~\~/\ $sigNorm/gi;
		$string =~ s/\$\$\$\$/\ $sigTime/gi;
	}
	
    # Lock before getting old page to prevent races Consider extracting lock section into sub, and eval-wrap it?
    # (A few called routines can die, leaving locks.)
    if ($LockCrash) { &RequestLock() or die( "Could not get editing lock" ); }
    else {
        if ( !&RequestLock() ) { &ForceReleaseLock('main'); }

        # Clear all other locks.
        &ForceReleaseLock('cache');
        &ForceReleaseLock('diff');
        &ForceReleaseLock('index');
    }
    
    &OpenPage($id);
    &OpenDefaultText();
    $old     = $Text{'text'};
    $oldrev  = $Section{'revision'};
    $pgtime  = $Section{'ts'};
    $preview = 0;
    $preview = 1 if ( &GetParam( "Preview", "" ) ne "" );
    
    if ( !$preview && ( $old eq $string ) ) {    # No changes (ok for preview)
        &ReleaseLock();
        &ReBrowsePage( $id, "", 1 );
        return;
    }
    
    if ( ( $UserID > 399 ) || ( $Section{'id'} > 399 ) ) {
        $newAuthor = ( $UserID ne $Section{'id'} );    # known user(s)
    }
    else {
        $newAuthor = ( $Section{'ip'} ne $authorAddr );    # hostname fallback
    }
	
    $newAuthor = 1 if ( $oldrev == 0 );    # New page
    $newAuthor = 0 if ( !$newAuthor );     # Standard flag form, not empty                                           
										   
    # Detect editing conflicts and resubmit edit                                           
    if ( ( $oldrev > 0 ) && ( $newAuthor && ( $oldtime != $pgtime ) ) ) {
        &ReleaseLock();
         # IF Conflict again...
        if ( $oldconflict > 0 ) { &DoEdit( $id, 2, $pgtime, $string, $preview ); }
        else { &DoEdit( $id, 1, $pgtime, $string, $preview ); }
        
        return;
    }
    
    if ($preview) {
        &ReleaseLock();
        &DoEdit( $id, 0, $pgtime, $string, 1 );
        return;
    }
    
    $user = &GetParam( "username", "" );

    # If the person doing editing chooses, send out email notification
    if ($EmailNotify) {
        &EmailNotify( $id, $user )
          if &GetParam( "do_email_notify", "" ) eq 'on';
    }
    
    # ALLOW minor edits to Editors and Admins
    if ( &GetParam( "recent_edit", "" ) eq 'on' ) {
        if (&UserIsEditorOrAdmin()){ $isEdit = 1; }
    }
    
    if ( !$isEdit ) { &SetPageCache( 'oldmajor', $Section{'revision'} );  }    
    if ($newAuthor) { &SetPageCache( 'oldauthor', $Section{'revision'} ); }
    
    &SaveKeepSection();
    &ExpireKeepFile();
    
    if ($UseDiff) { &UpdateDiffs( $id, $editTime, $old, $string, $isEdit, $newAuthor ); }
    $oldDescription = $Text{'description'};
	
	if ($description eq $oldDescription){ $description = ""; }
	else { $Page{'description'} = $description; }
	
    $Text{'text'}      		= $string;
    $Text{'minor'}     		= $isEdit;
    $Text{'newauthor'} 		= $newAuthor;
    $Text{'summary'}   		= $summary;	
	$Text{'description'} 	= $description;
    $Section{'host'}  		= &GetRemoteHost(1);
    
	if ($description ne ""){
		if ($newfile) { $summaryDescription = "CREATED $summary :: $description"; }
		else { $summaryDescription = "$summary :: $description"; }
	}
	else {
		if ($newfile) { $summaryDescription = "CREATED $summary"; }
		elsif ($oldDescription ne ""){ $summaryDescription = "$summary"; }
		else { $summaryDescription = "$summary"; }
	}
	
    &SaveDefaultText();
    &SavePage();
    &WriteRcLog( $id, $summaryDescription, $isEdit, $editTime, $Section{'revision'}, $user, $Section{'host'} );

    if ($UseCache) {
        &UnlinkHtmlCache($id);    # Old cached copy is invalid
		
        if ( $Page{'revision'} < 2 ) {    # If this is a new page...
            &NewPageCacheClear($id);      # ...uncache pages linked to this one.
        }
    }
    
    # Regenerate index on next request
    if ( $UseIndex && ( $Page{'revision'} == 1 ) ) { unlink($IndexFile); }
    &ReleaseLock();
    &ReBrowsePage( $id, "", 1 );
}

sub UpdateDiffs {
    my ( $id, $editTime, $old, $new, $isEdit, $newAuthor ) = @_;
    my ( $editDiff, $oldMajor, $oldAuthor );
    
    $editDiff  = &GetDiff( $old, $new, 0 );    # 0 = already in lock
    $oldMajor  = &GetPageCache('oldmajor');
    $oldAuthor = &GetPageCache('oldauthor');
    
    if ($UseDiffLog) {
          my $editDiff = Diff::diffClassic($old, $new);  # add this line
          &WriteDiff($id, $editTime, $editDiff);
    }
    
    &SetPageCache( 'diff_default_minor', $editDiff );
    if ( $isEdit || !$newAuthor ) { &OpenKeptRevisions('text_default'); }
    
    if ( !$isEdit ) { &SetPageCache( 'diff_default_major', "1" ); }    
    else { &SetPageCache( 'diff_default_major', &GetKeptDiff( $new, $oldMajor, 0 ) ); }
    
    if ($newAuthor) { &SetPageCache( 'diff_default_author', "1" ); }    
    elsif ( $oldMajor == $oldAuthor ) { &SetPageCache( 'diff_default_author', "2" ); }
    else { &SetPageCache( 'diff_default_author', &GetKeptDiff( $new, $oldAuthor, 0 ) ); }
}

#------------------------------------------------------------------------------
# Translation note: the email messages are still sent in English Send an email message.
#------------------------------------------------------------------------------
sub SendEmail {
  my ($to, $from, $reply, $subject, $message) = @_;

  # sendmail options:
  #    -odq : send mail to queue (i.e. later when convenient)
  #    -oi  : do not wait for "." line to exit
  #    -t   : headers determine recipient.
  open (SENDMAIL, "| $SendMail -odq -t ") or die "Can't send email: $!\n";
  print SENDMAIL <<"EOF";
From: $from
To: $to
Reply-to: $reply
Subject: $subject\n
$message
EOF
  close(SENDMAIL) or warn "sendmail didn't close nicely";
}

#------------------------------------------------------------------------------
# Email folks who want to know a note that a page has been modified. - JimM.
#------------------------------------------------------------------------------
sub EmailNotify {
  local $/ = "\n";   # don't slurp whole files in this sub.

  if ($EmailNotify) {
    my ($id, $user) = @_;
    my $address;
	
    if ($user) { $user = " by $user"; }   
    
    return  if (!-f $EmailFile);  # No notifications yet
    open(EMAIL, $EmailFile) or die "Can't open $EmailFile: $!\n";
	
    $address = join ",", <EMAIL>;
    $address =~ s/\n//g;
	
    close(EMAIL);
    
    my $home_url = $q->url();
    my $page_url = $home_url . &ScriptLinkChar() . &UriEscape($id);
    my $pref_url = $home_url . &ScriptLinkChar() . "action=editprefs";
    
    my $editors_summary = $q->param("summary");
    if (($editors_summary eq "*") or ($editors_summary eq "")){
      $editors_summary = "";
    }
    else {
      $editors_summary = "\n Summary: $editors_summary";
    }
    my $content = <<"END_MAIL_CONTENT";

 The $SiteName page $id at $page_url has been changed$user to revision $Page{revision}. 
 $editors_summary

 (Replying to this notification will send email to the entire mailing list, so only do that if you mean to. To remove yourself from this list, visit $pref_url .)
END_MAIL_CONTENT
    my $subject = "The $id page at $SiteName has been changed.";
    # I'm setting the "reply-to" field to be the same as the "to:" field
    # which seems appropriate for a mailing list, especially since the $EmailFrom string needn't be a real email address.
    &SendEmail($address, $EmailFrom, $address, $subject, $content);
  }
}

sub ConsiderRegex {
    my ($term, $text, $useRegex) = @_;
    
    unless ($term =~ /[\.|\*|\?]/){ return 1; }
    unless ($useRegex){ if (index (lc($$text), lc($term)) == -1){ return 0; }}
    
    return 1;
}

sub SearchTitleAndBody {
    my ($term, $filter, $allowRegex) = @_;
    my ( $name, $freeName, @found, $excludeTerm, $excludeFilter, $useRegex, $titlesOnly );
    
    $useRegex = $q->param('regex');
    unless ($useRegex){ $useRegex = $allowRegex; }
	
	$titlesOnly = $q->param('titlesonly');
    
    #If the search term has a !preceding it, strip it and set the exclusion flag
    if ($term =~ m/^\!/){ 
        $excludeTerm = 1;
        $term = substr($term, 1);    
    }
	
    #If the filter string has a !preceding it, strip it and set the exclusion flag    
    if ($filter =~ m/^\!/){ 
        $excludeFilter = 1;
        $filter = substr($filter, 1);    
    }

    foreach $name ( &AllPagesList() ) {
        if ($excludeFilter){
            if ($filter) { next if ($name =~ m/$filter/); }
        }
        else {
            if ($filter) { next unless ($name =~ m/$filter/); }
        }
        
		unless ($titlesOnly){
	        &OpenPage($name);
	        &OpenDefaultText();
		}
        
        if (!$excludeTerm){  
            if ( ( $Text{'text'} =~ /$term/ig ) || ( $name =~ /$term/i ) ) {
                if (&ConsiderRegex($term, \$Text{'text'}, $useRegex)){ push( @found, $name ); }
            }
            elsif ( $FreeLinks && ( $name =~ m/_/ ) ) {
                $freeName = $name;
                $freeName =~ s/_/ /g;
                
                if ( $freeName =~ /$term/i ) {
                    if (&ConsiderRegex($term, \$Text{'text'}, $useRegex)){ push( @found, $name ); }
                }
            }
        }
        else { 
            if ( ! (( $Text{'text'} =~ /$term/i ) || ( $name =~ /$term/i )) ) {
                if (&ConsiderRegex($term, \$Text{'text'}, $useRegex)){ push( @found, $name ); }
            }
            elsif ( $FreeLinks && ( $name =~ m/_/ ) ) {
                $freeName = $name;
                $freeName =~ s/_/ /g;
                
                if ( ! ($freeName =~ /$term/i) ) {
                    if (&ConsiderRegex($term, \$Text{'text'}, $useRegex)){ push( @found, $name ); }
                }
            }            
        }
    }
    
    return @found;
}

sub SearchBody {
    my ($string) = @_;
    my ( $name, @found );
    
    foreach $name ( &AllPagesList() ) {
        &OpenPage($name);
        &OpenDefaultText();
        
        if ( $Text{'text'} =~ /$string/i ) {
            push( @found, $name );
        }
    }
    
    return @found;
}

sub UnlinkHtmlCache {
    my ($id) = @_;
    my $idFile;
    
    $idFile = &GetHtmlCacheFile($id);
    
    if ( -f $idFile ) {
        unlink($idFile);
    }
}

sub NewPageCacheClear {
    my ($id) = @_;
    my $name;
    
    return if ( !$UseCache );
    
	# If subpage, search for just the subpage
    $id =~ s|.+/|/|;    
    
	# The following code used to search the body for the $id
    foreach $name ( &AllPagesList() ) {    # Remove all to be safe
        &UnlinkHtmlCache($name);
    }
}

#------------------------------------------------------------------------------
# Note: all diff and recent-list operations should be done within locks.
#------------------------------------------------------------------------------
sub DoUnlock {
    my $LockMessage = "Normal Unlock.";
    
    print &GetHeader( "", "Removing edit lock", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    print "\n<h2>This operation may take several seconds...</h2>\n";
    
    if ( &ForceReleaseLock('main') ) {
        $LockMessage = "Forced Unlock.";
    }
    
    &ForceReleaseLock('cache');
    &ForceReleaseLock('diff');
    &ForceReleaseLock('index');
    
    print "\n<br/><h2>$LockMessage</h2>";
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

#------------------------------------------------------------------------------
# Note: all diff and recent-list operations should be done within locks.
#------------------------------------------------------------------------------
sub WriteRcLog {
    my ( $id, $summary, $isEdit, $editTime, $revision, $name, $rhost ) = @_;
    my ( $extraTemp, %extra );
    
    %extra = ();
    $extra{'id'}       = $UserID   if ( $UserID > 0 );
    $extra{'name'}     = $name     if ( $name ne "" );
    $extra{'revision'} = $revision if ( $revision ne "" );
    $extraTemp = join( $FS2, %extra );

    # The two fields at the end of a line are kind and extension-hash
    my $rc_line = join( $FS3, $editTime, $id, $summary, $isEdit, $rhost, "0", $extraTemp );
    
    if ( !open( OUT, ">>$RcFile" ) ) {
        die( Ts( '%s log error:', $RCName ) . " $!" );
    }
    
    print OUT $rc_line . "\n";
    close(OUT);
}

sub WriteDiff {
    my ( $id, $editTime, $diffString ) = @_;
    
    open( OUT, ">>$DataDir/diff_log" ) or die( "can not write diff_log" );
    print OUT "------\n" . $id . "|" . $editTime . "\n";
    print OUT $diffString;
    close(OUT);
}

#------------------------------------------------------------------------------
# Actions are vetoable if someone edits the page before the keep expiry time. For example, page deletion. If
# no one edits the page by the time the keep expiry time elapses, then no one has vetoed the last action, and the
# action is accepted.  See http://www.usemod.com/cgi-bin/mb.pl?PageDeletion
#------------------------------------------------------------------------------
sub ProcessVetos {
    my ($expirets);
    
    $expirets = $Now - ( $KeepDays * 24 * 60 * 60 );
    
    return ( 0, "(done)" ) unless $Page{'ts'} < $expirets;
    
    if ( $DeletedPage && $Text{'text'} =~ /^\s*{{delete}}\W*?(\n|$)/o ) {
        &DeletePage( $OpenPageName, 1, 1 );
        return ( 1, "(deleted)" );
    }
    
	## see http://www.usemod.com/cgi-bin/wiki.pl?WikiPatches/FileReplacement
    if ( $AllowReplaceFiles && $Text{'text'} =~ /^\s*{{replace\:\s*(\S+)}}/o ) {
        my $fname = $1;

        # Only replace an allowed, existing file. 
        if ( ( grep { $_ eq $fname } @ReplaceableFiles ) && -e $fname ) {
            if ( $Text{'text'} =~ /.*<pre>.*?\n(.*?)\s*<\/pre>/ims ) {
                my $string = $1;
                
                $string =~ s/\r\n/\n/gms;
                open( OUT, ">$fname" ) or return 0;
                print OUT $string;
                close OUT;
                
                return ( 0, "(replaced)" );
            }
        }
    }
    return ( 0, "(done)" );
}

sub DoMaintain {
    my ( $name, $fname, $data, $message, $status );
    
    print &GetHeader( "", "Maintenance on all pages", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    $fname = "$DataDir/maintain";
    
    if ( !&UserIsAdmin() ) {
        if ( ( -f $fname ) && ( ( -M $fname ) < 0.5 ) ) {
            print "\n<h2>Warning</h2>";
            print "\nMaintenance not done. ";
            print "\n(Maintenance can only be done once every 12 hours.)";
            print "\nRemove the 'maintain' file or wait.";
            print "\n</div>";
            print &GetFooterText();
            print "\n</div></div></div></div></body></html>";
            
            return;
        }
    }
    
    &RequestLock() or die( "Could not get maintain-lock" );
    print "\n<h2>Processed as follows:</h2>";

    foreach $name ( &AllPagesList() ) {
        &OpenPage($name);
        &OpenDefaultText();
        
        ( $status, $message ) = &ProcessVetos();
        &ExpireKeepFile() unless $status;
        
        print "\n.... " if ( $name =~ m|/| );
        print &GetPageLink($name);
        print "\n $message<br/>";
    }

    &WriteStringToFile( $fname, Ts( 'Maintenance done at %s', &TimeToText($Now) ) );
    &ReleaseLock();

    # Do any rename/deletion commands (Must be outside lock because it will grab its own lock)
    $fname = "$DataDir/editlinks";
    
    if ( -f $fname ) {
        $data = &ReadFileOrDie($fname);
        print "\n<h3>Processing rename/delete commands:</h3>";
        &UpdateLinksList( $data, 1, 1 );    # Always update RC and links
        unlink("$fname.old");
        rename( $fname, "$fname.old" );
    }
    
    if ($MaintTrimRc) {
        &RequestLock() or die( "Could not get lock for RC maintenance" );
        $status = &TrimRc();                # Consider error messages?
        &ReleaseLock();
    }
    
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

#------------------------------------------------------------------------------
# Must be called within a lock. Thanks to Alex Schroeder for original code
#------------------------------------------------------------------------------
sub TrimRc {
    my ( @rc, @temp, $starttime, $days, $status, $data, $i, $ts );

    # Determine the number of days to go back
    $days = 0;
    
    foreach (@RcDays) {
        $days = $_ if $_ > $days;
    }
    $starttime = $Now - $days * 24 * 60 * 60;
    return 1 if ( !-f $RcFile );    # No work if no file exists
    ( $status, $data ) = &ReadFile($RcFile);
    
    if ( !$status ) {
        print "\n<p><strong>Could not open $RCName log file</strong> $RcFile<p>Error was:<pre>$!</pre></p></p>";
        
        return 0;
    }

    # Move the old stuff from rc to temp
    @rc = split( /\n/, $data );
    
    for ( $i = 0 ; $i < @rc ; $i++ ) {
        ($ts) = split( /$FS3/, $rc[$i] );
        last if ( $ts >= $starttime );
    }
    
    return 1 if ( $i < 1 );    # No lines to move from new to old
    
    @temp = splice( @rc, 0, $i );

    # Write new files and backups
    if ( !open( OUT, ">>$RcOldFile" ) ) {
        print "\n<p><strong>Could not open $RCName log file:</strong> $RcOldFile<p>Error was:<pre>$!</pre></p></p>";
        
        return 0;
    }
    print OUT join( "\n", @temp ) . "\n";
    close(OUT);
    
    &WriteStringToFile( $RcFile . '.old', $data );
    $data = join( "\n", @rc );
    $data .= "\n" if ( $data ne "" );    # If no entries, don't add blank line
    &WriteStringToFile( $RcFile, $data );
    
    return 1;
}

sub DoMaintainRc {    
    return if ( !&UserIsAdminOrError('Maintain Recent Changes') );

    print &GetHeader( "", "Maintaining RC log", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    
    &RequestLock() or die( "Could not get lock for RC maintenance" );            
    if ( &TrimRc() ) { print "\n<h2>RC maintenance done.</h2>"; }
    else { print "\n<h2>RC maintenance not done.</h2>"; }
    &ReleaseLock();
    
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub UserIsEditorOrError {
    my ($operation) = @_;
    
    if ( !&UserIsEditor() ) {
        print &GetHeader( "", "Authorization Error - Editor", "" );
        print &GetLeftNav();
        print "\n<div class='wikiadmin'>";
        print "\n<h2>This operation is restricted to Editors and Adminstrators.</h2>";
        print "\nYou must be an editor or an administrator to process the task '$operation'.";
        print " Please either login or change your " . &GetPrefsLink() . " before trying this task again.";
        print "\n</div>";
        print &GetFooterText();
        print "\n</div></div></div></body></html>";
            
        return 0;
    }
    
    return 1;
}

sub UserIsAdminOrError {
    my ($operation) = @_;
    
    if ( !&UserIsAdmin() ) {
        print &GetHeader( "", "Authorization Error - Administrator", "" );
        print &GetLeftNav();
        print "\n<div class='wikiadmin'>";
        print "\n<h2>This operation is restricted to Administrators.</h2>";
        print "\nYou must be an administrator to process the task '$operation'.";
        print " Please either login or change your " . &GetPrefsLink() . " before trying this task again.";
        print "\n</div>";
        print &GetFooterText();
        print "\n</div></div></div></body></html>";    
        
        return 0;
    }
    
    return 1;
}

sub CheckTokenList {
    my ($tokenDir) = @_;
    my ($tokenId, $staleness, $timeDiff, $targetFile, $text, $entry);
    
    $tokenId = $q->param('tokenId');
    $staleness = 60 * 60; #Seconds; thus 1 hour
    
    unless ($tokenId){ return 0; }
    unless ($tokenId =~ /\d*/){ return 0; }
    
    $timeDiff = $Now - $tokenId;
    unless ($timeDiff <= $staleness){ return 0; }        
    
    $targetFile = "$tokenDir/tokens";
    
    local $/ = undef;      # Read complete files
    if (-f $targetFile){
        open( INFILE, "<$targetFile" ) or die( "Can't read file [ $targetFile ] $!" );
        $text = <INFILE>;
        close(INFILE);
    }
    
    if ($text =~ $tokenId){ return 0; }
    
    open ( OUT, ">$targetFile") or die ( "Can't write to file [ $targetFile ] $!" );
    foreach ( split( /$FS3/, $text ) ) {
        $timeDiff = $Now - $_;
        if ($timeDiff <= $staleness){ print OUT $_ . $FS3; }
    }
    print OUT $tokenId;
    close (OUT);
            
    return 1;
}    

#------------------------------------------------------------------------------
# PrivateUserGroups are managed here
#------------------------------------------------------------------------------
sub CheckIsAuthUser {
    my ($id) = @_;
    my $auth = ""; 
    my $found = 0;
    my $authtype;
    my $authname; 
    my $aname;
    my $afname;
    my $linecount = 0;

    if (!(&UserIsAdmin())) {
        $aname = $id;
        $aname =~ s/(^[^\/]+)\/*[^\/]*$/$1/;
        $afname = $PageDir . "/" . &GetPageDirectory($aname) . "/" . $aname . "/" . "AuthUsers.db";
        
        if (-r $afname) {            
            if ($id =~ /^(.*)\/.*/) { $aname = $1; }
            
            open (AFN,"<$afname");
            while (<AFN>) {
                if (/$FS1/) { next; }           # skip header and footer
                if (/^>\s[^\w]/) { next; }      # skip comments    
                if (/diff-/){ next; }        
                if (/>{([\w]+):([\w]+)}</) {    # pattern is {e:UserName} allow read and edit, or {r:UserName} for allow read
                    $authtype = $1;
                    $authname = $2; 
                    
                    if ($authtype eq "e"){ $authtype = "2"; $linecount++; }
                    elsif ($authtype eq "r"){ $authtype = "1"; }
                    else { $authtype = "1"; }
                    
                    if ($UserData{'username'} eq $authname) { $found = 1; $auth = $authtype; }
                }
            }
            close AFN;
            if ($linecount == 0){ $auth = "3"; }
            elsif ($found == 0) { $auth = ""; }
        }
        else {
            $auth = "3";
        }
    }
    else {
        $auth = "3";
    }
    return $auth;
}

sub DoEditLock {
    my ($fname);

    return if ( !&UserIsAdminOrError('Set Site Lock') );

    print &GetHeader( "", "Set or Remove global edit lock", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
    
    $fname = "$DataDir/noedit";
        
    if ( &GetParam( "set", 1 ) ) { &WriteStringToFile( $fname, "editing locked." ); }
    else { unlink($fname); }
    
    if ( -f $fname ) { print "\n<h2>Edit lock created.</h2>"; }
    else { print "\n<h2>Edit lock removed.</h2>"; }
    
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub DoPageLock {
    my ( $fname, $id );
    
    # Consider allowing page lock/unlock at editor level?
    return if ( !&UserIsAdminOrError('Set Page Lock') );
    
    print &GetHeader( "", "Set or Remove page edit lock", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
            
    $id = &GetParam( "id", "" );
    if ( $id eq "" ) {
        print "\n<p>Missing page id to lock/unlock...</p>";
        
        return;
    }
    
    return if ( !&ValidIdOrDie($id) );    # Consider nicer error?
    $fname = &GetLockedPageFile($id);
    
    if ( &GetParam( "set", 1 ) ) {
        &WriteStringToFile( $fname, "editing locked." );
    }
    else {
        unlink($fname);
    }

    if ( -f $fname ) {
        print "\n<h2>Lock for '$id' created.</h2>";
    }
    else {
        print "\n<h2>Lock for '$id' removed.</h2>";
    }
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub DoEditBanned {
    my ( $banList, $status );

    return if ( !&UserIsAdminOrError('Edit Banned List') );
    
    print &GetHeader( "", "Editing Banned list", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
        
    ( $status, $banList ) = &ReadFile("$DataDir/banlist");
    $banList = "" if ( !$status );
    
    print "\n<form id='wikiform' action='$ScriptName' enctype='application/x-www-form-urlencoded' method='POST'>";
    print GetHiddenValue( "edit_ban", 1 );
    print "\n<h2> Banned IP/network/host list:</h2>";
    print "\nEach entry is either a commented line (starting with #), ";
    print "\nor a Perl regular expression (matching either an IP address or ";
    print "\na hostname).  <br/><br/><b>Note:</b> To test the ban on yourself, you must ";
    print "\ngive up your admin access (remove password in Preferences).";
    print "\n<p><br/><b>Example:</b><br/><br/>";
    print "\n# blocks hosts ending with .foocorp.com<br/>";
    print "\n<tt> \\.foocorp\\.com\$</tt><br/><br/>";
    print "\n# blocks exact IP address<br/>";
    print "\n<tt> ^123\\.21\\.3\\.9\$</tt><br/><br/>";
    print "\n# blocks whole 123.21.3.* IP network<br/>";
    print "\n<tt> ^123\\.21\\.3\\.\\d+\$</tt><br/><br/></p>";
    print &GetTextArea( 'banlist', $banList, 12, 0 );
    print "\n<br/><br/>";
    print $q->submit( -name => 'Save' );
    print "\n</form>";
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    ;
}

sub DoUpdateBanned {
    my ( $newList, $fname );

    return if ( !&UserIsAdminOrError('Update Banned List') );
    
    print &GetHeader( "", "Updating Banned list", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
        
    $fname = "$DataDir/banlist";
    $newList = &GetParam( "banlist", "#Empty file" );
    
    if ( $newList eq "" ) {
        print "\n<p>Empty banned list or error.</p>";
        print "\n<p>Resubmit with at least one space character to remove.</p>";
    }
    elsif ( $newList =~ /^\s*$/s ) {
        unlink($fname);
        print "\n<p>Removed banned list</p>";
    }
    else {
        &WriteStringToFile( $fname, $newList );
        print "\n<h2>Updated banned list</h2>";
    }
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

#------------------------------------------------------------------------------
# Editing/Deleting pages and links
#------------------------------------------------------------------------------
sub DoEditLinks {
    if ($AdminDelete) { return if ( !&UserIsAdminOrError('Edit Links') ); }
    else { return if ( !&UserIsEditorOrError('Edit Links') ); }
    
    print &GetHeader( "", "Editing Links", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
        
    print "\n<form id='wikiform' action='$ScriptName' enctype='application/x-www-form-urlencoded' method='POST'>";
    print GetHiddenValue( "edit_links", 1 );
    print "\n<h2>Editing/Deleting page titles:</h2>";
    print "\nEnter one command on each line.  Page names are case-sensitive!<br/><br/><b>Commands are:</b><br/>";
	
	if ($UseSubpage){ print "\n<tt>?PageName</tt> -- lists all sub-pages of PageName<br/>"; }
	
    print "\n<tt>!PageName</tt> -- deletes the page called PageName<br/>";
    print "\n<tt>=OldPageName=NewPageName</tt> -- Renames OldPageName to NewPageName and updates links to OldPageName.<br/>";
    print "\n<tt>=OldPageName/*=NewPageName</tt> -- Renames OldPageName, its sub-pages, to NewPageName and updates links to OldPageName.<br/>";
    print "\n<tt>|OldPageName|NewPageName</tt> -- Changes links from OldPageName to NewPageName. (Used to rename links to non-existing pages.)<br/><br/>";
    print &GetTextArea( 'commandlist', "", 12, 0 );
    print "\n<br/><br/>";
    print $q->checkbox(
        -name     => "p_changerc",
        -override => 1,
        -checked  => 1,
        -label    => "Edit $RCName"
    );
    print "\n<br/>";
    print $q->checkbox(
        -name     => "p_changetext",
        -override => 1,
        -checked  => 1,
        -label    => "Substitute text for rename"
    );
    print "\n<br/><br/>";
    print $q->submit( -name => 'Process Command' );
    print "\n</form>";
    print "\n</div>";
    
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub UpdateLinksList {
    my ( $commandList, $doRC, $doText ) = @_;
    
    if ($doText) { &BuildLinkIndex(); }
    
    &RequestLock() or die "UpdateLinksList could not get main lock";
    unlink($IndexFile) if ($UseIndex);
    
    foreach ( split( /\n/, $commandList ) ) {
        s/\s+$//g;
        
        next if ( !(/^[=!|?]/) );    # Only valid commands.
        print "\n<h3>Processing $_</h3>\n";
        
        if (/^\!(.+)/) {
            &DeletePage( $1, $doRC, $doText );
        }
        elsif (/^\?(.+)/){
            print "\nSub-pages of " . &GetPageLink($1) . ":\n<br/><br/>";
            print join ("\n<br/>", map { &GetPageLink($_) }&AllSubPagesList($1));
            print "\n<br/><br/>";
        }
        elsif (/^\=(?:\[\[)?([^]=]+)(?:\]\])?\=(?:\[\[)?([^]=]+)(?:\]\])?/) {
              my $GivenPage = $1;
              my $GivenNewName = $2;
      
              if ($GivenPage =~ s[\/\*][]) {
                   print "\nRenaming subpages of $GivenPage too...<br/>";
        
                foreach (&AllSubPagesList($GivenPage)) {
                    my $NewSubName = $_;
                    
                    $NewSubName =~ s[$GivenPage][$GivenNewName]i;
                    print "\nrenaming $_ to $NewSubName<br/>";
                    &RenamePage($_, $NewSubName, $doRC, $doText);
                }
              }
			  
              # rename the page itself
              print "\nrenaming $GivenPage to $GivenNewName<br/>";
              &RenamePage($GivenPage, $GivenNewName, $doRC, $doText);
        }
        elsif (/^\|(?:\[\[)?([^]|]+)(?:\]\])?\|(?:\[\[)?([^]|]+)(?:\]\])?/) {
            &RenameTextLinks( $1, $2 );
        }
    }
    
    &NewPageCacheClear(".");        # Clear cache (needs testing?)
    unlink($IndexFile) if ($UseIndex);
    &ReleaseLock();
}

sub BuildLinkIndex {
    my ( @pglist, $page, @links, $link, %seen );
    
    @pglist    = &AllPagesList();
    %LinkIndex = ();
    
    foreach $page (@pglist) {
        &BuildLinkIndexPage($page);
    }
}

sub BuildLinkIndexPage {
    my ($page) = @_;
    my ( @links, $link, %seen );
    
    @links = &GetPageLinks( $page, 1, 0, 0 );
    %seen = ();
    
    foreach $link (@links) {
        if ( defined( $LinkIndex{$link} ) ) {
            if ( !$seen{$link} ) {
                $LinkIndex{$link} .= " " . $page;
            }
        }
        else {
            $LinkIndex{$link} .= " " . $page;
        }
        $seen{$link} = 1;
    }
}

sub DoUpdateLinks {
    my ( $commandList, $doRC, $doText );

    if ($AdminDelete) { return if ( !&UserIsAdminOrError('Update Links') ); }
    else { return if ( !&UserIsEditorOrError('Update Links') ); }
    
    print &GetHeader( "", "Updating Links", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
        
    $commandList = &GetParam( "commandlist", "" );
    $doRC        = &GetParam( "p_changerc",  "0" );
    $doRC = 1 if ( $doRC eq "on" );
    $doText = &GetParam( "p_changetext", "0" );
    $doText = 1 if ( $doText eq "on" );
    
    if ( $commandList eq "" ) {
        print "\n<h2>Empty command list or error.</h2>";
    }
    else {
        &UpdateLinksList( $commandList, $doRC, $doText );
		
		$commandList =~ s/\=/ \&rarr; /g;
        print "\n<h2>Finished command list.</h2>";
		print "\n<tt>" . join("<br/>", split(/\n/, $commandList)) .  "</tt>";
    }
    
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub EditRecentChanges {
    my ( $action, $old, $new ) = @_;
    
    &EditRecentChangesFile( $RcFile,    $action, $old, $new, 1 );
    &EditRecentChangesFile( $RcOldFile, $action, $old, $new, 0 );
}

sub EditRecentChangesFile {
    my ( $fname, $action, $old, $new, $printError ) = @_;
    my ( $status, $fileData, $errorText, $rcline, @rclist );
    my ( $outrc, $ts, $page, $junk );
    
    ( $status, $fileData ) = &ReadFile($fname);
    
    if ( !$status ) {

        # Save error text if needed.
        $errorText = "\n<p><strong>Could not open $RCName log file:</strong> $fname<p>Error was:<pre>$!</pre></p></p>";
        print $errorText if ($printError);
        
        return;
    }
    
    $outrc = "";
    @rclist = split( /\n/, $fileData );
    
    foreach $rcline (@rclist) {
        ( $ts, $page, $junk ) = split( /$FS3/, $rcline );
        if ( $page eq $old ) {
            if ( $action == 1 ) {    # Delete
                ;                    # Do nothing (don't add line to new RC)
            }
            elsif ( $action == 2 ) {
                $junk = $rcline;
                $junk =~ s/^(\d+$FS3)$old($FS3)/"$1$new$2"/ge;
                $outrc .= $junk . "\n";
            }
        }
        else {
            $outrc .= $rcline . "\n";
        }
    }
    
    &WriteStringToFile( $fname . ".old", $fileData );    # Backup copy
    &WriteStringToFile( $fname, $outrc );
}

#------------------------------------------------------------------------------
# Delete and rename must be done inside locks.
#------------------------------------------------------------------------------
sub DeletePage {
    my ( $page, $doRC, $doText ) = @_;
    my ( $fname, $status );
    
    $page =~ s/ /_/g;
    $page =~ s/\[+//;
    $page =~ s/\]+//;
    $status = &ValidId($page);
    
    if ( $status ne "" ) {
        print "\nDelete-Page: page $page is invalid, error is: $status<br/>";
        return;
    }
    
    #DELETE page file
    $fname = &GetPageFile($page);
    unlink($fname) if ( -f $fname );
    $fname = $KeepDir . "/" . &GetPageDirectory($page) . "/$page.kp";
    unlink($fname)     if ( -f $fname );
    unlink($IndexFile) if ($UseIndex);
    
    #UPDATE recent changes log
    &EditRecentChanges( 1, $page, "" ) if ($doRC);    # Delete page; currently don't do anything with page text

    #DELETE discussion file
    $fname = $DiscussDir . "/" . &GetPageDirectory($page) . "/$page.df";
    unlink($fname)     if ( -f $fname );
}

#------------------------------------------------------------------------------
# Given text, returns substituted text
#------------------------------------------------------------------------------
sub SubstituteTextLinks {
    my ( $old, $new, $text ) = @_;

    # Much of this is taken from the common markup
    %SaveUrl      = ();
    $SaveUrlIndex = 0;
    $text =~ s/$FS(\d)/$1/g;    # Remove separators (paranoia)
    
    if ($RawHtml) {
        $text =~ s/(<html>((.|\n)*?)<\/html>)/&StoreRaw($1)/ige;
    }
    
    $text =~ s/(<pre>((.|\n)*?)<\/pre>)/&StoreRaw($1)/ige;
    $text =~ s/(<tt>((.|\n)*?)<\/tt>)/&StoreRaw($1)/ige;
    $text =~ s/(<nowiki>((.|\n)*?)<\/nowiki>)/&StoreRaw($1)/ige;
    
    if ($FreeLinks) {
        $text =~ s/\[\[$FreeLinkPattern\|([^\]]+)\]\]/&SubFreeLink($1,$2,$old,$new)/geo;
        $text =~ s/\[\[$FreeLinkPattern\]\]/&SubFreeLink($1,"",$old,$new)/geo;
    }
    
    if ($BracketText) {         # Links like [URL text of link]
        $text =~ s/(\[$UrlPattern\s+([^\]]+?)\])/&StoreRaw($1)/geo;
        $text =~ s/(\[$InterLinkPattern\s+([^\]]+?)\])/&StoreRaw($1)/geo;
    }
    
    $text =~ s/(\[?$UrlPattern\]?)/&StoreRaw($1)/geo;
    $text =~ s/(\[?$InterLinkPattern\]?)/&StoreRaw($1)/geo;
    
    if ($WikiLinks) {
        $text =~ s/$LinkPattern/&SubWikiLink($1, $old, $new)/geo;
    }

    # Thanks to David Claughton for the following fix
    1 while $text =~ s/$FS(\d+)$FS/$SaveUrl{$1}/ge;    # Restore saved text
    
    return $text;
}

sub SubFreeLink {
    my ( $link, $name, $old, $new ) = @_;
    my ($oldlink);
    
    $oldlink = $link;
    $link =~ s/^\s+//;
    $link =~ s/\s+$//;
    
    if ( ( $link eq $old ) || ( &FreeToNormal($old) eq &FreeToNormal($link) ) ) { $link = $new; }    
    else { $link = $oldlink; }     # Preserve spaces if no match
    
    $link = "[[$link";
    
    if ( $name ne "" ) { $link .= "|$name"; }
    
    $link .= "]]";
    
    return &StoreRaw($link);
}

sub SubWikiLink {
    my ( $link, $old, $new ) = @_;
    my ($newBracket);
    
    $newBracket = 0;
    
    if ( $link eq $old ) {
        $link = $new;
        
        if ( !( $new =~ /^$LinkPattern$/ ) ) {
            $link = "[[$link]]";
        }
    }
    
    return &StoreRaw($link);
}

sub RenameDiscussionText {
    my ( $page, $old, $new ) = @_;
    my ( $fname, $status, $data, $changed );
    
    $fname = $DiscussDir . "/" . &GetPageDirectory($page) . "/$page.df";
    return if ( !( -f $fname ) );
    
    ( $status, $data ) = &ReadFile($fname);
    return if ( !$status );
    return unless ($data);    
    
    ($changed) = $data =~ s/$old/$new/mg;
    
    return if ( $changed eq $data );    # No translations made
    open( OUT, ">$fname" ) or return;
    
    print OUT $changed;
    close(OUT);
}

#------------------------------------------------------------------------------
# Rename is mostly copied from expire
#------------------------------------------------------------------------------
sub RenameKeepText {
    my ( $page, $old, $new ) = @_;
    my ( $fname, $status, $data, @kplist, %tempSection, $changed );
    my ( $sectName, $newText );
    
    $fname = $KeepDir . "/" . &GetPageDirectory($page) . "/$page.kp";
    return if ( !( -f $fname ) );
    
    ( $status, $data ) = &ReadFile($fname);
    return if ( !$status );
    
    @kplist = split( /$FS1/, $data, -1 );    # -1 keeps trailing null fields
    return if ( length(@kplist) < 1 );       # Also empty
    
    shift(@kplist) if ( $kplist[0] eq "" );  # First can be empty
    return if ( length(@kplist) < 1 );       # Also empty
    
    %tempSection = split( /$FS2/, $kplist[0], -1 );

    if ( !defined( $tempSection{'keepts'} ) ) { return; }

    # First pass: optimize for nothing changed
    $changed = 0;
    
    foreach (@kplist) {
        %tempSection = split( /$FS2/, $_, -1 );
        $sectName = $tempSection{'name'};
        
        if ( $sectName =~ /^(text_)/ ) {
            %Text = split( /$FS3/, $tempSection{'data'}, -1 );
            $newText = &SubstituteTextLinks( $old, $new, $Text{'text'} );
            $changed = 1 if ( $Text{'text'} ne $newText );
        }
    }
    
    return if ( !$changed );    # No sections changed
    open( OUT, ">$fname" ) or return;
    
    foreach (@kplist) {
        %tempSection = split( /$FS2/, $_, -1 );
        $sectName = $tempSection{'name'};
        
        if ( $sectName =~ /^(text_)/ ) {
            %Text = split( /$FS3/, $tempSection{'data'}, -1 );
            $newText = &SubstituteTextLinks( $old, $new, $Text{'text'} );
            $Text{'text'} = $newText;
            $tempSection{'data'} = join( $FS3, %Text );
            
            print OUT $FS1, join( $FS2, %tempSection );
        }
        else {
            print OUT $FS1, $_;
        }
    }
    
    close(OUT);
}

sub RenameTextLinks {
    my ( $old, $new ) = @_;
    my ( $changed, $file, $page, $section, $oldText, $newText, $status );
    my ( $oldCanonical, @pageList );
    
    $old =~ s/ /_/g;
    $oldCanonical = &FreeToNormal($old);
    $new =~ s/ /_/g;
    $status = &ValidId($old);
    
    if ( $status ne "" ) {
        print "\nRename-Text: old page $old is invalid, error is: $status<br/>";
        return;
    }
    
    $status = &ValidId($new);
    
    if ( $status ne "" ) {
        print "\nRename-Text: new page $new is invalid, error is: $status<br/>";
        return;
    }
    
    $old =~ s/_/ /g;
    $new =~ s/_/ /g;

    # Note: the LinkIndex must be built prior to this routine
    return if ( !defined( $LinkIndex{$oldCanonical} ) );
    
    @pageList = split( ' ', $LinkIndex{$oldCanonical} );
    foreach $page (@pageList) {
        $changed = 0;
        &OpenPage($page);

        foreach $section ( keys %Page ) {
            if ( $section =~ /^text_/ ) {
                &OpenSection($section);
                %Text    = split( /$FS3/, $Section{'data'}, -1 );
                $oldText = $Text{'text'};
                $newText = &SubstituteTextLinks( $old, $new, $oldText );
                
                if ( $oldText ne $newText ) {
                    $Text{'text'} = $newText;
                    $Section{'data'} = join( $FS3, %Text );
                    $Page{$section} = join( $FS2, %Section );
                    $changed = 1;
                }
            }
            elsif ( $section =~ /^cache_diff/ ) {
                $oldText = $Page{$section};
                $newText = &SubstituteTextLinks( $old, $new, $oldText );
                
                if ( $oldText ne $newText ) {
                    $Page{$section} = $newText;
                    $changed = 1;
                }
            }

            # Add other text-sections (categories) here
        }
        
        if ($changed) {
            $file = &GetPageFile($page);
            &WriteStringToFile( $file, join( $FS1, %Page ) );
        }
        
        &RenameKeepText( $page, $old, $new );
        &RenameDiscussionText ( $page, $old, $new );
    }
}

sub RenamePage {
    my ( $old, $new, $doRC, $doText ) = @_;
    my ( $oldfname, $newfname, $oldkeep, $newkeep, $status );
    my ( $oldDiscuss, $newDiscuss );
    
    $old =~ s/ /_/g;
    $new    = &FreeToNormal($new);
    $status = &ValidId($old);
    
    if ( $status ne "" ) {
        print "\nRename: old page $old is invalid, error is: $status<br/>";
        return;
    }
    
    $status = &ValidId($new);
    if ( $status ne "" ) {
        print "\nRename: new page $new is invalid, error is: $status<br/>";
        return;
    }
    
    $newfname = &GetPageFile($new);
    if ( -f $newfname ) {
        print "\nRename: new page $new already exists--not renamed.<br/>";
        return;
    }
    
    $oldfname = &GetPageFile($old);
    if ( !( -f $oldfname ) ) {
        print "\nRename: old page $old does not exist--nothing done.<br/>";
        return;
    }
    
    #RENAME page file
    &CreatePageDir( $PageDir, $new );    # It might not exist yet
    rename( $oldfname, $newfname );
    
    &CreatePageDir( $KeepDir, $new );
    $oldkeep = $KeepDir . "/" . &GetPageDirectory($old) . "/$old.kp";
    $newkeep = $KeepDir . "/" . &GetPageDirectory($new) . "/$new.kp";
    
    unlink($newkeep) if ( -f $newkeep );    # Clean up if needed.
    rename( $oldkeep, $newkeep );
    unlink($IndexFile) if ($UseIndex);
    
    #RENAME discussion file
    &CreatePageDir( $DiscussDir, $new );    # It might not exist yet
    
    $oldDiscuss = $DiscussDir . "/" . &GetPageDirectory($old) . "/$old.df";
    $newDiscuss = $DiscussDir . "/" . &GetPageDirectory($new) . "/$new.df";
    
    unlink($newDiscuss) if ( -f $newDiscuss );    # Clean up if needed.
    rename( $oldDiscuss, $newDiscuss );
    
    
    #UPDATE recent changes log
    &EditRecentChanges( 2, $old, $new ) if ($doRC);

    if ($doText) {
        &BuildLinkIndexPage($new);          # Keep index up-to-date
        &RenameTextLinks( $old, $new );
    }
}

sub DoShowVersion {
	my $html;
	
    $html .= &GetHeader( "", "$SiteName Version ", "" );
    $html .= &GetLeftNav();
    $html .= "\n<div class='wikiadmin'>";
    $html .= "\n<h2>License Information</h2>";
	$html .= "\nNobleWiki is licensed as <a href='http://www.gnu.org/licenses/gpl.html' class='external' target='_blank'>GPL</a> [ GNU General Public License ]";
    $html .= "\nThis is NobleWiki 1.0.0; it's engine is derived from UseModWiki version 1.04. See " . &GetPageLink("TourBusStop") . " for list of changes and features.<br/>";
	$html .= "\n";
	$html .= "\n<h3>System Requirements</h3>";
	$html .= "\nNobleWiki utilizes the following server and libraries:";
	$html .= "\n<pre>";
	$html .= "\n<dl><dt>Apache HTTPd Server 2.2</dt><dd>&copy; 2002 <a href='http://httpd.apache.org/' class='external'>Apache Software Foundation</a></dd><dd>Recommended for installation</dd></dl>";
	$html .= "\n<dl><dt>perl v.5.8</dt><dd>ActiveState Perl 5.8.8.0.280 for Windows XP, or Windows Vista</dd><dd>Recommended for installation</dd></dl>";
	$html .= "\n<dl><dt>Diff.pm 1.10</dt><dd>&copy; 2002 <a href='mailto:michael.buschbeck\@bitshapers.com' class='external'>Michael Buschbeck </a></dd><dd>Used in place of \*NIX diff</dl>";
	$html .= "\n</pre>";
	$html .= "\n<h3>History</h3>";
	$html .= "\n<p>The NobleWiki pedigree is as follows:";
	$html .= "\n<pre>";
	$html .= "\n NobleWiki version 1.0.0 (November 11, 2008)";
	$html .= "\n   &copy; 2006-2008 <a href='mailto:kitrok\@yahoo.com' class='external'>Robert Kurcina</a>\n";
	$html .= "\n Based on the UseModWiki version 1.0.4 (December 1, 2007)";
	$html .= "\n   &copy; 2000-2003 <a href='mailto:caadams\@usemod.com' class='external'>Clifford A. Adams</a>";
	$html .= "\n   &copy; 2002-2003 <a href='mailto:sunir\@sunir.org' class='external'>Sunir Shah</a>\n";
	$html .= "\n...which was based on";
	$html .= "\n   the GPLed AtisWiki 0.3 &copy; 1998 <a href='mailto:marcus\@ira.uka.de' class='external'>Markus Denker</a>\n";
	$html .= "\n...which was based on the LGPLed CVWiki CVS-patches &copy; 1997 Peter Merel";
	$html .= "\n   and The Original WikiWikiWeb &copy; <a href='mailto:ward\@c2.com' class='external'>Ward Cunningham</a> (code reused with permission)";
	$html .= "\n</pre>";
	$html .= "\n<h3>JavaScript Libraries</h3>";
	$html .= "\nNobleWiki utilizes the following third-party JavaScript libraries:";
	$html .= "\n<pre>";
	$html .= "\n<dl><dt>jQuery 1.2.6</dt><dd>&copy; 2008 John Resig via <a href='http://jquery.com/' class='external' target='_blank'>http://jquery.com/</a></dd><dd>Dual licensed under the MIT and <a href='http://www.gnu.org/licenses/gpl.html' class='external' target='_blank'>GPL</a> licenses.</dd></dl>";
	$html .= "\n<dl><dt>jQuery LightBox 0.5</dt><dd>&copy; 2008 Leandro Vieira Pinho via <a href='http://leandrovieira.com' class='external' target='_blank'>http://leandrovieira.com</a></dd><dd><a href='http://creativecommons.org/licenses/by-nd/2.5/br/deed.en_US' class='external' target='_blank'>CC Attribution-No Derivative Works 2.5 Brazil</a></dd></dl>";
	$html .= "\n<dl><dt>jQuery TableSorter 2.0.1</dt><dd>&copy; 2007 Christian Bach via <a href='http://tablesorter.com' class='external' target='_blank'>http://tablesorter.com</a></dd><dd>Dual licensed under the MIT and <a href='http://www.gnu.org/licenses/gpl.html' class='external' target='_blank'>GPL</a> licenses.</dd></dl>";
	$html .= "\n<dl><dt>Unobtrusive Flash Objects (UFO) v3.22</dt><dd>&copy; 2005-2007 Bobby van der Sluis via <a href='http://www.bobbyvandersluis.com/ufo/' class='external' target='_blank'>http://www.bobbyvandersluis.com/ufo/</a></dd><dd><a href='http://creativecommons.org/licenses/LGPL/2.1/' class='external' target='_blank'>Licensed under the CC-GNU LGPL</a></dd></dl>";
	$html .= "\n<dl><dt>Code Press</dt><dd>&copy; 2006 <a href='mailto:fermads\@gmail.com' class='external'>Fernando M.A.d.S.</a> via <a href='http://codepress.org/' class='external' target='_blank'>http://codepress.org/</a></dd><dd><a href='http://www.opensource.org/licenses/lgpl-license.php' class='external' target='_blank'>GNU Lesser General Public License as published by the Free Software Foundation.</a></dd></dl>";
	$html .= "\n</pre>";
    $html .= "\n</div>";
    $html .= &GetFooterText();
    $html .= "\n</div></div></div></div></body></html>";
	
	print $html;
}

sub GetCssChoices {
    my $choices = "";
    my $result = "";
    my $current = &GetParam('stylesheet', "");
    my $selected = "";
    
    opendir( TEMP, "$CssDir/wiki" );
    my @files = readdir(TEMP);
    closedir(TEMP);        

    foreach my $file(@files){
        next unless ($file =~ /\.css$/);    # allow wiki.something.css and wiki.css
        
        if ($current eq "/css/wiki/$file"){ $choices .= "\n<option value='/css/wiki/$file' selected='selected'>$file</option>"; }
        else {     $choices .= "\n<option value='/css/wiki/$file'>$file</option>"; }
    }
    
    $result .= "\n<select id='stylesheet' class='wikiselectbox' name='p_stylesheet'>";
    $result .= $choices;
    $result .= "\n</select>";
    
    return $result;
}

#------------------------------------------------------------------------------
# Admin bar contributed by ElMoro (with some changes)
#------------------------------------------------------------------------------
sub GetPageLockLink {
    my ( $id, $status, $name ) = @_;
    
    if ($FreeLinks) { $id = &FreeToNormal($id); }
    
    return &ScriptLink( "action=pagelock&set=$status&id=$id", $name );
}

sub GetGallery {
    my ($params) = @_;
    my @lines = split(/\r?\n/, $params);
    my $lineNum = 0;
    my $imageNum = 0;
    my %options;
    my $images = "";
    my $text = "";
    my $targetUrl = &NoDirSlash($UploadUrl);
    my $targetDir = &NoDirSlash($UploadDir);
    
    my $defaultImage = "image1.jpg";
    my $defaultThumb = "thumb_image1.jpg";
    my $image;
    my $thumb;
    my $title;
    my $header;
    my $caption;
    my $description;
    my $thumbWidth = 100;
    
    $GLOBAL_galleryCount++;
        
    foreach my $line (@lines){
        %options = &GetOptions($line);
        
        if ($lineNum == 0){
            $lineNum++;
            
            if ($options{'thumbWidth'}){ $thumbWidth = $options{'thumbWidth'}; } else { $thumbWidth = 100; }
            if ($options{'description'}){ $description = $options{'description'}; }
            if ($options{'header'}){ $header = $options{'header'}; }
            if ($options{'caption'}){ $caption = $options{'caption'}; }        
            
            next;    
        }
        else {        
            if ($options{'image'}){ $image = $options{'image'}; }
            if ($options{'thumb'}){ $thumb = $options{'thumb'}; }
            if ($options{'title'}){ $title = $options{'title'}; } else { $title = "IMAGE: $GLOBAL_galleryCount:$imageNum"; $imageNum++; }
            
            unless (-e "$targetDir/$image"){ $image = $defaultImage; }
            unless (-e "$targetDir/$thumb"){ $thumb = $defaultThumb; }
            
            my ($imageWidth, $imageHeight) = &ComputeImageRatio($thumb, $thumbWidth, "", 1);
                
            $images .= "\n            <li><a href='$targetUrl/$image' title='$title'><img width='$imageWidth' height='$imageHeight' src='$targetUrl/$thumb'/></a></li>";
        }
    }
    
    $text .= "\n<div id='gallery-$GLOBAL_galleryCount' class='gallery'>";
    $text .= "\n        <script type='text/javascript'>\$(function() { \$('#gallery-$GLOBAL_galleryCount a').lightBox(); });</script>";
    
    if ($header){ $text .= "\n        <div class='gallery header'>$header</div>"; }
    
    $text .= "\n        <ul>";    
    $text .= $images;
    $text .= "\n        </ul>";
    
    if ($caption){ $text .= "\n        <div class='gallery caption'>$caption</div>"; }
    if ($description){ $text .= "\n        <div class='gallery description'>$description</div>"; }
    
    $text .= "\n    </div>";        
    
    return $text;
}

sub GetJSON {
    my ($data) = @_;
    my ($dataId, $object);
        
    $data =~ s/^\s*(\S+)\s*/$dataId=$1,''/e;
    return &StoreRaw(T('No data namespace provided')) unless $dataId;    
    
    return &StoreRaw(T('No function definitions allowed within data object.')) if ($data =~ /function.*\}/);
    $data = "<script>var $dataId = {$data\}<\/script>";
    
    return $data;    
}

sub GetCodeBox {
    my ($language, $options, $syntax) = @_;
    my ($text, $idBox, %options, $fwidth, $fheight, $ftitle, $maxWidth, $maxHeight, $minHeight, $style);
    
    $maxHeight = 400;
    $minHeight = 100;
    
    %options = &GetOptions($options);    
    $GLOBAL_codeboxCount++;    
    $idBox = "codepress$GLOBAL_codeboxCount";
    
    unless($language){ $language = 'generic'; }
    if ($options{'height'}){ $fheight = $options{'height'}; } else { $fheight = $minHeight; }    
    if ($fheight < $minHeight){ $fheight = $minHeight; }
    elsif ($fheight > $maxHeight){ $fheight = $maxHeight; }
    
    $style = "style='width:100%;height:$fheight;";
    $text .= "\n<label for='$idBox'>$language code:</label><br/>";
    $text .= "\n<textarea id='$idBox' class='codepress $language linenumbers-on readonly-on autocomplete-off' $style wrap='off'>";
    $text .= $syntax;
    $text .= "\n</textarea>";
    
    return $text;
}

sub GetBox {
	my ($class, $options) = @_;
	my ($boxClass, $title, $message , %options);
	
	unless (
		$class eq "error" or 
		$class eq "alert" or 
		$class eq "info" or 
		$class eq "warn" or
		$class eq "update" or
		$class eq "yes" or
		$class eq "no" or
		$class eq "todo" or
		$class eq "delete" or
		$class eq "lock"
	){ $class = "info"; }
	
	$boxClass = $class . "Box";
	
	%options = &GetOptions($options);
	if ($options{'title'}){ $title = $options{'title'}; } else { $title = ''; }
	if ($options{'message'}){ $message  = $options{'message'}; } else { $message  = ''; }
		
	if ($message eq ''){ $message = $title; $title = ''; }
	if ($title eq ''){		
		if ($class eq "error"){ $title = T('Error!'); }
		if ($class eq "alert"){ $title = T('Alert!'); }
		if ($class eq "warn"){ $title = T('Warning!'); }
		if ($class eq "info"){ $title = T('Information!'); }
		if ($class eq "update"){ $title = T('Update!'); }
		if ($class eq "yes"){ $title = T('Approved!'); }
		if ($class eq "no"){ $title = T('Rejected!'); }
		if ($class eq "todo"){ $title = T('Needs Work!'); }
		if ($class eq "delete"){ $title = T('Deleted!'); }
		if ($class eq "lock"){ $title = T('Locked!'); }		
	}
	
	return "<div class='$boxClass'><div class='icon'></div><div class='notice'><div class='title'>$title</div><div class='message'>$message</div></div></div>";
}

sub GetColor {
	my ($options) = @_;
	my ($background, $color, $text, $padding, %options);
	
	%options = &GetOptions($options);
	if ($options{'padding'}){ $padding = $options{'padding'}; $padding = "padding:$padding;"; } else { $padding = ''; }
	if ($options{'color'}){ $color = $options{'color'}; $color = "color:$color;"; } else { $color = ''; }
	if ($options{'bgcolor'}){ $background = $options{'bgcolor'}; $background = "background-color:$background;"; } else { $background = ''; }
	if ($options{'text'}){ $text = $options{'text'}; } else { $text = ''; }
	
	return "<div style='$padding $color $background-color'>$text</div>";
}

sub GetFlash {
    my ($options) = @_;
    my ($defaultSWF, $maxWidth, $maxHeight, $ratio, $targetDir, $text, $idDiv, $idFO, %options);
    my ($fname, $fwidth, $fheight, $fpath);
    
    %options = &GetOptions($options);    
    $fpath = &NoDirSlash($UploadUrl);
    $defaultSWF = 'ufo.swf';
    $maxWidth = 400;
    $maxHeight = 300;
    $ratio = 1;
    $targetDir = &NoDirSlash($UploadDir);
    
    $GLOBAL_flashCount++;
        
    $idDiv = "ufoDiv$GLOBAL_flashCount";
    $idFO = "FO_$GLOBAL_flashCount";

    if ($options{'name'}){ $fname = $options{'name'}; } else { $fname = $defaultSWF; }
    if ($options{'width'}){ $fwidth = $options{'width'}; } else { $fwidth = $maxWidth; }
    if ($options{'height'}){ $fheight = $options{'height'}; } else { $fheight = $maxHeight; }
    
    if ($fwidth > $maxWidth){
        $ratio = $maxWidth / $fwidth;
        $fwidth = $maxWidth;
        $fheight = int ($ratio * $fheight);
    }
    elsif ($fheight > $maxHeight){
        $ratio = $maxHeight / $fheight;
        $fheight = $maxHeight;
        $fwidth = int ($ratio * $fwidth);
    }
            
    unless (-e "$targetDir/$fname"){ $fname = $defaultSWF; }
    
    $text .= "\n<div id='$idDiv' class='ufoFlash'>";
    $text .= "\n<script type='text/javascript'>";
    $text .= "\n            var fpath = '$fpath/';";
    $text .= "\n            var fname = '$fname';";
    $text .= "\n            var fwidth = $fwidth;";
    $text .= "\n            var fheight = $fheight;";
    $text .= "\n            var $idFO = { 'movie': fpath + fname, 'width':fwidth, 'height':fheight, 'majorversion':'8', 'build':'0', 'xi':'true' };";
    $text .= "\n            \$(window).load(function () {";
    $text .= "\n                UFO.create($idFO, '$idDiv');";                    
    $text .= "\n                document.getElementById('$idDiv').style.width = fwidth;";
    $text .= "\n                document.getElementById('$idDiv').style.height= fheight;";
    $text .= "\n            });";
    $text .= "\n        </script>";        
    $text .= "\n        <p style='margin-top: 0px;'>[ <i><b>$fname</b></i> ]<br/> is unavailable for viewing.    Please enable JavaScript and/or download the latest <a href='http://www.macromedia.com/go/getflashplayer'>Flash Player</a>.</p>";
    $text .= "\n        <p><a href='http://www.macromedia.com/go/getflashplayer'><img src='$SiteUrl/plugins/ufo/img/get_flash_player.gif' alt='Get macromedia Flash Player' style='border: none; float: right; margin-right:10px;' /></a></p>";
    $text .= "\n        <p style='clear: both;'></p>";
    $text .= "\n    </div>";

    return $text;        
}

#------------------------------------------------------------------------------
# Thanks to Phillip Riley for original code
#------------------------------------------------------------------------------
sub DoDeletePage {
    my ($id) = @_;
    
    return if ( !&ValidIdOrDie($id) );
    return if ( !&UserIsAdminOrError('Delete Page') );
    
    if ( $ConfirmDel && !&GetParam( 'confirm', 0 )) {
        print &GetHeader( "", Ts( 'Confirm Delete %s', $id ), "" );
        print &GetLeftNav();
        print "\n<div class='wikiadmin'>";
        print "\n<h2>Delete Page?</h2>";
        print "\nConfirm deletion of '<b>$id</b>' by following this link: ";
        print &GetDeleteLink( $id, "Confirm Delete", 1 );
        print "\n</div>";
        print &GetFooterText();
        print "\n</div></div></div></div></body></html>";    
        
        return;
    }
    
    print &GetHeader( "", Ts( 'Delete %s', $id ), "" );
    print &GetLeftNav();    
    print "\n<div class='wikiadmin'>";
    
    if ( $id eq $HomePage ) {
        print Ts( '%s can not be deleted.', $HomePage );
    }
    else {
        if ( -f &GetLockedPageFile($id) ) {
            print Ts( '%s can not be deleted because it is locked.', $id );
        }
        else {

            # Must lock because of RC-editing
            &RequestLock() or die( "Could not get editing lock" );
            DeletePage( $id, 1, 1 );
            &ReleaseLock();
            print Ts( '%s has been deleted.', $id );
        }
    }
    
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

#------------------------------------------------------------------------------
# Thanks to Ross Kowalski and Iliyan Jeliazkov for original uploading code
#------------------------------------------------------------------------------
sub DoUpload {
    my ($message) = @_;
    my (@list, @folders);
    my $targetDir = &NoDirSlash($UploadDir);
    
    print &GetHeader( "", "File Upload Page", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
        
    if ( !$AllUpload ) { return if ( !&UserIsEditorOrError('Upload Files') ); }
    
    print $message;
    print "\n<h2>Select File</h2>";
    print "\nThe current upload size limit is $MaxPostSizeKB.<br/>";
    print "\nThe Wiki Owner must change the <tt>\$MaxPostSizeKB</tt> variable to increase this limit.<br/>";
    print "\n<form id='wikiform' method='post' action='$ScriptName' enctype='multipart/form-data'>";
    print "\n<table><tr>";
    print "\n<td><input type='hidden' name='upload' value='1' />";
    print "\nFile to Upload:</td>";
    print "\n<td><input class='wikibutton' id='wikifile' type='file' name='file'></td><br/>";
    print "\n<tr><td colspan='2'>";
    
    @list = &GetAssetsList($targetDir);
    (@folders) = &GetAssetFolders($UploadDir, @list);
    &ShowUploadChoices("0", "0", @folders);

    print "\n<tr><td colspan='2' align='right'>";
    print "\n<input class='wikibutton' id='wikisubmit' type='submit' name='Submit' value='Upload'><br/>";    
    print "\n</td></tr></table>";
    print "\n</form>";
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub NoDirSlash {
    my ($dirname) = @_;
    
    if ( substr( $dirname, -1, 1 ) eq "/" ){ $dirname = substr( $dirname, 0, length($dirname) - 1); }
    
    return $dirname;
}

sub GetDestinationFolder {
    my ($manageDisabled) = @_;
    my ($moveto, $newfolder, $finalFolder, $targetDir, $targetUrl, $DISABLED, $NOFOLDER);
    
    $moveto = $q->param('moveto');
    $newfolder = $q->param('newfolder');
    
    unless ($moveto or $newfolder){ $NOFOLDER = 1; }
        
    $finalFolder = $moveto;    
    if ($newfolder ne ""){ $finalFolder = $newfolder; }
    $finalFolder = &ExtractName($finalFolder);
    $finalFolder =~ s/[^\w\-\.]//g;                # Remove characters not A-Za-z0-9, hyphen, underscore, or period.

    $targetDir = $UploadDir;
    $targetUrl = $UploadUrl;
    
    if ($finalFolder eq "MAIN"){ 
        if ($manageDisabled){
            $targetDir = $DisabledDir; 
            $DISABLED = "1"; 
            $finalFolder = "";
        }
        else {
            $finalFolder = "";
        }
    }
    elsif ($finalFolder eq "DISABLED"){ 
        $targetDir = $DisabledDir; 
        $DISABLED = "1"; 
        $finalFolder = ""; 
    }
    elsif ($finalFolder eq "ACTIVE"){
        $targetDir = $UploadDir; 
        $DISABLED = "";
    }
    elsif ($finalFolder eq "DELETE"){
        $targetDir = $DeletedDir; 
        $DISABLED = ""; 
    }

    $targetDir = &NoDirSlash($targetDir);
    $targetUrl = &NoDirSlash($targetUrl);
    
    return ($targetDir, $targetUrl, $finalFolder, $DISABLED, $NOFOLDER);
}

sub ExtractFolder {    
    my ($given) = @_;
    
    $given =~ s/(.*)[\/\\](.*)/$1/;    # Only name before last \ or /    
    
    return $given;    
}

sub ExtractName {
    my ($given) = @_;
    
    $given =~ s/.*[\/\\](.*)/$1/;    # Only name after last \ or /    
    
    return $given;    
}

sub RemoveCGITemp {
    # DELETE CGItemp files for Windows
    opendir (HANDLE,$CGIBIN);
    my @CGITempFiles = map("$CGIBIN/$_", grep(/^CGItemp/i, readdir HANDLE));
    unlink @CGITempFiles;
}

sub GetExtension {
    my ($filename) = @_;    
    my ($extension) = $filename =~ /.*\.(\w*)$/;
    
    return $extension;        
}

sub GetDownloadText {
    my ($filename) = @_;
    my $extension = &GetExtension($filename);
    
    if ($extension eq "pdf"){ return "an Adobe Acrobat Reader"; }
    if ($extension eq "psd"){ return "an Adobe Photoshop"; }
    if ($extension eq "ai"){ return "an Adobe Illustrator"; }
    if ($extension eq "xls"){ return "a Microsoft Excel"; }
    if ($extension eq "xml"){ return "an XML"; }
    if ($extension eq "ppt"){ return "a Microsoft Powerpoint"; }
    if ($extension eq "js"){ return "a JavaScript"; }
    if ($extension eq "css"){ return "a Cascading Style Sheet [CSS]"; }
    if ($extension eq "doc"){ return "a Microsoft Word"; }
    if ($extension eq "txt"){ return "a plain text"; }
    if ($extension eq "swf"){ return "an Adobe Flash Player"; }
    if ($extension eq "fla"){ return "an Adobe Flash Source"; }
    if ($extension eq "fh9"){ return "an Adobe Freehand 9.x"; }
    if ($extension eq "fh11"){ return "an Adobe Freehand MXa"; }
    if ($extension eq "blend"){ return "an Blender"; }
    if ($extension eq "java"){ return "a Java"; }
    if ($extension eq "zip"){ return "a zip archive"; }
    
    return "a missing or unknown"; 
}

sub GetAttachmentIconUrl {
    my ($filename) = @_;
    my ($iconpath, $iconfile, $icon, $extension);
    
    $extension = &GetExtension($filename);
    $icon = "icons/icons\.$extension\.50px\.jpg";
    $iconfile = &NoDirSlash($SiteUrl) . "/img/$icon";
    $iconpath = &NoDirSlash($ImageDir) . "/$icon";

    if (-e $iconpath){ return $iconfile; }
    else { return &NoDirSlash($SiteUrl) . "/img/icons/icons.UNKNOWN.50px.jpg"; }
}

sub GetDownloadsBox {
    my ($filename, $fileUrl) = @_;
    my ($result);

    $result .= "\n<div style='padding: 5px; border: 1px solid #cccccc; overflow: auto; width: 350px; background-color: #f5f5f5; margin-bottom: 5px; margin-right: 5px;'>";
    $result .= "<a class='floatleft' style='border: 1px solid #eeeeee;' href='$fileUrl' target='_blank' title='click to view in new window'>";
    $result .= "\n<img src='" . &GetAttachmentIconUrl($filename) . "' title='$fileUrl'></a>";
    $result .= "\n<b>$filename</b>";
    $result .= "\n<div style='font-size: 80%; font-style: italic;'>This is " . &GetDownloadText($filename) . " file.  Right-click the icon to download and save to your desktop.</div>";
    $result .= "<div class='clearboth'></div></div>"; 
    
    return $result;
}

sub SaveUpload {
    my ( $filename, $printFilename, $uploadFilehandle, $fileUrl, $finalFolder, $targetDir, $targetUrl, $DISABLED, $NOFOLDER );

    # DETERMINE TARGET FILE and FOLDER        
    $filename = $q->param('file');
    $filename = &ExtractName($filename); 
    unless ($filename) { return &DoUpload("<h2><small>Please select a file.</small></h2>"); }
    
    ($targetDir, $targetUrl, $finalFolder, $DISABLED, $NOFOLDER) = &GetDestinationFolder();    
    if ($NOFOLDER){ return &DoUpload("<h2><small>Please select a destination directory.</small></h2>"); }
    
    print &GetHeader( "", "Upload Finished", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
        
    if ( !$AllUpload ) { return if ( !&UserIsEditorOrError('Save Upload') ); }
        
    # CREATE FOLDER IF DOESN'T EXIST
    &CreateDir("$targetDir/$finalFolder");
    if ($finalFolder ne ""){ $finalFolder = "$finalFolder/"; }    
    
    # UPLOAD FILE INTO THE TARGET FOLDER
    $uploadFilehandle = $filename;
    open UPLOADFILE, ">$targetDir/$finalFolder$filename";
    binmode(UPLOADFILE);
    while (<$uploadFilehandle>) { print UPLOADFILE; }
    close UPLOADFILE;
    
    if ($Windows){ &RemoveCGITemp(); }

    print "\n<h2>Upload Completed</h2>";
    
    if ($DISABLED){
        print "\nYour file <tt>'$filename'</tt> has been uploaded into the <tt>'Disabled Assets'</tt> directory in the folder <tt>'$finalFolder'</tt>";
    }
    else {
        print "\nThe wiki link to your file is:<br/><br/>";
        
        $printFilename = "$finalFolder$filename";
        $printFilename =~ s/ /\%20/g;       # Replace spaces with escaped spaces
        $fileUrl = "$targetUrl/$printFilename";
        
        print "\n<code>upload:$printFilename</code><br/>[ <a href='$fileUrl' target='_blank' title='click to view in new window'><tt>$fileUrl</tt></a> ]<br/><br/>";
    
        if ( $filename =~ /${ImageExtensions}$/ ) { print "\n<div class='wikiuploadbar'><img src='$fileUrl' title='$fileUrl'></div>"; }
        elsif ( $filename =~ /${DownloadExtensions}$/ ) { print &GetDownloadsBox($filename, $fileUrl); }
        else { print "\n<h2>ERROR!</h2><div>Unknown extension encountered for [$filename].</div>"; }
    }
    
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub ConvertFsFile {
    my ( $oldFS, $newFS, $fname ) = @_;
    my ( $oldData, $newData, $status );
    
    return if ( !-f $fname );           # Convert only existing regular files
    ( $status, $oldData ) = &ReadFile($fname);
    
    if ( !$status ) {
        print "\n<br/><strong>Could not open file $fname:</strong>Error was:<pre>$!</pre><br/>";
        
        return;
    }
    
    $newData = $oldData;
    $newData =~ s/$oldFS(\d)/$newFS . $1/ge;
    
    return if ( $oldData eq $newData );    # Do not write if the same
    &WriteStringToFile( $fname, $newData );

    # print $fname . '<br/>';    # progress report
}

#------------------------------------------------------------------------------
# Converts up to 3 dirs deep  (like page/A/Apple/subpage.db)
# Note that top level directory (page/keep/user) contains only dirs
#------------------------------------------------------------------------------
sub ConvertFsDir {
    my ( $oldFS, $newFS, $topDir ) = @_;
    my ( @dirs, @files, @subFiles, $dir, $file, $subFile, $fname, $subFname );
    
    opendir( DIRLIST, $topDir );
    @dirs = readdir(DIRLIST);
    closedir(DIRLIST);
    @dirs = sort(@dirs);
    
    foreach $dir (@dirs) {
        next if ( substr( $dir, 0, 1 ) eq '.' );    # No ., .., or .dirs
        next if ( !-d "$topDir/$dir" );             # Top level directories only
        next if ( -f "$topDir/$dir.cvt" );          # Skip if already converted
        
        opendir( DIRLIST, "$topDir/$dir" );
        @files = readdir(DIRLIST);
        closedir(DIRLIST);
        
        foreach $file (@files) {
            next if ( ( $file eq '.' ) || ( $file eq '..' ) );
            $fname = "$topDir/$dir/$file";
            if ( -f $fname ) {
                # print $fname . '<br/>';   # progress
                &ConvertFsFile( $oldFS, $newFS, $fname );
            }
            elsif ( -d $fname ) {
                opendir( DIRLIST, $fname );
                @subFiles = readdir(DIRLIST);
                closedir(DIRLIST);
                
                foreach $subFile (@subFiles) {
                    next if ( ( $subFile eq '.' ) || ( $subFile eq '..' ) );
                    $subFname = "$fname/$subFile";
                    if ( -f $subFname ) {
                        # print $subFname . '<br/>';   # progress
                        &ConvertFsFile( $oldFS, $newFS, $subFname );
                    }
                }
            }
        }
        &WriteStringToFile( "$topDir/$dir.cvt", 'converted' );
    }
}

sub ConvertFsCleanup {
    my ($topDir) = @_;
    my ( @dirs, $dir );
    
    opendir( DIRLIST, $topDir );
    @dirs = readdir(DIRLIST);
    closedir(DIRLIST);
    
    foreach $dir (@dirs) {
        next if ( substr( $dir, 0, 1 ) eq '.' );    # No ., .., or .dirs
        next if ( !-f "$topDir/$dir" );             # Remove only files...
        next unless ( $dir =~ m/\.cvt$/ );          # ...that end with .cvt
        unlink "$topDir/$dir";
    }
}

sub DoConvert {
    my $oldFS = "\xb3";
    my $newFS = "\x1e\xff\xfe\x1e";
        
    return if ( !&UserIsAdminOrError('Convert Wiki Database') );
    
    print &GetHeader( "", "Convert wiki DB", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
        
    if ( $FS ne $newFS ) {
        print "\nYou must change the $NewFS option before converting the wiki DB.<br/>";
        return;
    }
    
    &WriteStringToFile( "$DataDir/noedit", 'editing locked.' );
    print "\nWiki DB locked for conversion.<br/>";
    print "\nConverting Wiki DB...<br/>";
    
    &ConvertFsFile( $oldFS, $newFS, "$DataDir/rclog" );
    &ConvertFsFile( $oldFS, $newFS, "$DataDir/rclog.old" );
    &ConvertFsFile( $oldFS, $newFS, "$DataDir/oldrclog" );
    &ConvertFsFile( $oldFS, $newFS, "$DataDir/oldrclog.old" );
    &ConvertFsDir( $oldFS, $newFS, $PageDir );
    &ConvertFsDir( $oldFS, $newFS, $KeepDir );
    &ConvertFsDir( $oldFS, $newFS, $UserDir );
    &ConvertFsCleanup($PageDir);
    &ConvertFsCleanup($KeepDir);
    &ConvertFsCleanup($UserDir);
    
    print "\nFinished converting wiki DB.<br/>";
    print "\nRemove file $DataDir/noedit to unlock wiki for editing.<br/>";
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

#------------------------------------------------------------------------------
# Remove user-id files if no useful preferences set
#------------------------------------------------------------------------------
sub DoTrimUsers {
    my ( %Data, $status, $data, $maxID, $id, $removed, $keep );
    my ( @dirs, @files, $dir, $file, $item );
        
    return if ( !&UserIsAdminOrError('Trim Wiki Users') );
    
    print &GetHeader( "", "Trim wiki users", "" );
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
        
    $removed = 0;
    $maxID   = 1001;
    
    opendir( DIRLIST, $UserDir );
    @dirs = readdir(DIRLIST);
    closedir(DIRLIST);

    foreach $dir (@dirs) {
        next if ( substr( $dir, 0, 1 ) eq '.' );    # No ., .., or .dirs
        next if ( !-d "$UserDir/$dir" );            # Top level directories only
        
        opendir( DIRLIST, "$UserDir/$dir" );
        @files = readdir(DIRLIST);
        closedir(DIRLIST);
        
        foreach $file (@files) {
            if ( $file =~ m/(\d+).db/ ) {           # Only numeric ID files
                $id    = $1;
                $maxID = $id if ( $id > $maxID );
                %Data  = ();
                
                ( $status, $data ) = &ReadFile("$UserDir/$dir/$file");
                
                if ($status) {
                    %Data = split( /$FS1/, $data, -1 );    # -1 keeps trailing null fields
                    $keep = 0;
                    
                    foreach $item (qw(username password adminpw stylesheet)) {
                        $keep = 1 if ( defined( $Data{$item} ) && ( $Data{$item} ne "" ) );
                    }
                    
                    if ( !$keep ) {
                        unlink "$UserDir/$dir/$file";
                        
                        # print "\n$UserDir/$dir/$file" . '<br/>';  # progress
                        $removed += 1;
                    }
                }
            }
        }
    }
    
    print Ts( 'Removed %s files.', $removed ) . '<br/>';
    print Ts( 'Recommended $StartUID setting is %s.', $maxID + 100 ) . '<br/>';
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";    
}

sub DoManageLocks {


}

sub GetAssetsList {
    my ($dir) = @_;
    my ($file, $entry, @dirs, @list);

    opendir( DIRLIST, $dir );
    @dirs = readdir(DIRLIST);
    closedir(DIRLIST);
    
    foreach $entry (@dirs){
        next if ( substr( $entry, 0, 1 ) eq '.' );    # No ., .., or .dirs
        if (-d "$dir/$entry"){
            opendir( DIRLIST, "$dir/$entry" );
            while (defined($file = readdir(DIRLIST))){ push @list, "$entry/$file"; }    
            closedir(DIRLIST);
        }
        else {
            push @list, "$entry";
        }
    }
    
    return @list;    
}
sub ShowUploadChoices {
    my ($manageDisabled, $showUpdate, @folders) = @_;
    my ($file, $action);
    
    if ($manageDisabled){ $action = "disabled"; }
    else { $action = "active"; }
    
    if ( &UserIsAdmin() || $showUpdate eq "0" ){
        print "\n<table>";
        print "\n<tr><td>Move to:</td><td><select id='wikifileselect' name='moveto' style='width: 200px;' title='Select the name of the folder to move all checked files.'>";
        print "\n<option value=''>---- select one ----</option>";
        print "\n<option value='MAIN' title='Move selection into main folder' style='font-weight: bold;'>MAIN</option>";
        
        if ($manageDisabled){ 
            print "\n<option value='ACTIVE' title='Re-enable the selection' style='font-weight: bold;'>ACTIVE</option>";
            
            if (&UserIsAdmin()){ print "\n<option value='DELETE' title='Remove selection from filesystem' style='color: #ff0000;font-weight: bold;'>DELETE</option>"; }
        }
        else { print "\n<option value='DISABLED' title='Disable the current selection' style='font-weight: bold;'>DISABLED</option>"; }
        
        print "\n<option value=''>------------------------</option>";
        foreach $file (@folders){ print "\n<option value='$file'>$file</option>"; }
                
        print "</select></td>";        
        print "</tr>";
        print "\n<tr><td>Create Folder: </td><td><input id='wikinewfolder' type='text' size='15' maxlength='25' style='width: 200px;' name='newfolder' title='Enter name of folder to create.'></td>";
        print "</tr><br/>";
        print "\n</table>";
    }
}

sub GetAssetFolders {
    my ($targetDir, @list) = @_;
    my (@folders, $file, $entry, $targetDir);
        
    $targetDir = &NoDirSlash($targetDir);
    my %TEMP;
    
    foreach $file (@list){
        if (-d "$targetDir/$file"){
            ($entry) = $file =~ m/(.*)\//;
            unless ($TEMP{$entry}){
                $TEMP{$entry} = 1;
                push @folders, $entry;
            }
        }    
    }    
    
    return (@folders);
}

sub ShowAssetTable {
    my ( $manageDisabled, @files ) = @_;
    my ( $html, $file, $isAdmin, $isPriviledged, $numlinks, $title, $action, $imagePath, $size, $filecount, $linkname, @links );
    my ( $id, $folder, $type );
    
    $isPriviledged = &UserIsEditorOrAdmin();
    $isAdmin = &UserIsAdmin();
        
    print "\n<table id='tablesorter-999' class='wikilargelist tablesorter'>";
    print "\n<thead><tr>";
    print "\n<th>Folder Name</th>";
    print "\n<th>File Name</th>";
    
    unless ($manageDisabled){ print "\n<th>WikiLink</th>"; }
    
    print "\n<th>Type</th>";    
    
    if ( $isPriviledged ){ 
        print "\n<th>Size</th>";
        unless ($manageDisabled){ print "<th>Links</th>"; }
    }
    
    if ( $isAdmin ){ print "\n<th>Move?</th>"; }
    
    print "</tr><\/thead><tbody>";
    
    # LIST files found
    foreach $file (@files) {
        $filecount++;
        $linkname = "upload:$file";
        $title = "";
        $action = "";

        if ($manageDisabled){
            $imagePath = &NoDirSlash($DisabledDir) . "/$file";
        }
        else {            
            $imagePath = &NoDirSlash($UploadDir) . "/$file";
        
            if ($isPriviledged){
                @links = SearchTitleAndBody($file, "", 0);
                $numlinks = scalar(@links);
            }
                    
            if ($numlinks > 0){
                $title = "click to see what pages link to this file.";
                $action = "href='$ScriptName?back=$file'";
            }
            else{
                $numlinks = 0;
            }
        }
        
        print "\n<tr>";
        $id = $file;
        
        ($folder) = $id =~ /(.*?)\/.*/;
        $id =~ s/.*[\/\\](.*)/$1/;
                
        if ($folder eq ""){ $folder = "MAIN"; }
        
        print "\n<td>$folder</td>";
        print "\n<td>$id</td>";
        
        unless ($manageDisabled){ print "\n<td><a href='" . &NoDirSlash($UploadUrl) . "/$file' target='_blank' title='click to view in a new window'>$linkname</a></td>"; }
        
        
        ($type) = uc($linkname) =~ /.*\.(.*)?$/;
        print "\n<td>$type</td>";
        
        if ($isPriviledged){
            $size = sprintf("%.3f&nbsp;KB", (-s $imagePath)/1000);
                
            print "\n<td align='right'>$size</td>";            
            unless ($manageDisabled){ 
                if ($numlinks){ print "\n<td><a class='wikilink' title='$title' $action>$numlinks</a></td>"; }
                else { print "\n<td>-</td>"; }
            }
        }
        
        if ( $isAdmin ){
            if ($manageDisabled){
                print "\n<td><input type='checkbox' id='move-$filecount' name='moveme' title='click to select this asset to move' value='$file'/></td>";
            }
            else {
                if ($numlinks == 0){ print "\n<td><input type='checkbox' id='move-$filecount' name='moveme' title='click to select this asset to move' value='$file'/></td>"; }
                else { print "\n<td><input type='checkbox' id='move-$filecount' name='' value='' disabled/></td>"; }
            }
        }
        
        print "\n</tr>";
    }
    
    if (scalar(@files) == 0){ print "\n<td colspan='6'>No files available</td></tr>"; }
    
    print "\n<\/tbody></table>";
    print "\n<script>\$(document).ready(function(){ \$('\#tablesorter\-999').tablesorter({widgets: ['zebra']}); });<\/script>";
}

sub ProcessAssets {
    my ($manageDisabled, $filter) = @_;
    my ($file, $asset, $action, $assetCount, $found, $prefix, $result, @moveList);
    my ($taskName, $targetDir, $targetUrl, $finalFolder, $DISABLED, $NOFOLDER, $oldname, $newname, $folder, $item);

    # GET assets            
    $found = 1;
    $assetCount = 0;    
    $prefix = "moveme";
    push (@moveList, $q->param('moveme'));    
    
    #MOVE assets
    unless ($NOFOLDER){ 
        unless (scalar(@moveList)) {
            print "<h2><small>No files selected for processing.</small></h2>"; 
            return;
        }
    }    

    # DETERMINE TARGET FOLDER    
    ($targetDir, $targetUrl, $finalFolder, $DISABLED, $NOFOLDER) = &GetDestinationFolder($manageDisabled);
    if (scalar(@moveList)){ if ($NOFOLDER){ print "<h2><small>Please select a destination folder</small></h2>"; return; }}
    if ($finalFolder ne ""){ $finalFolder = "$finalFolder/"; }

    # MOVE PROVIDED FILE INTO APPROPRIATE DIRECTORY if id has legitimate filename extension        
    foreach $item (@moveList){        
        $file = &ExtractName($item);
        
        if (&ExtensionAllowed($file)){            
            if ($manageDisabled){ 
                $oldname = "$DisabledDir/$item"; 
                $newname = "$DisabledDir/$finalFolder$file";
                $taskName = "MOVE"; 
                
                if ($finalFolder eq "DELETE/"){ $newname = "$DeletedDir/$file"; $taskName = "DELETE"; }
                if ($finalFolder eq "ACTIVE/"){ $newname = "$UploadDir/$item"; $taskName = "ACTIVATE"; }    
            }
            else {                
                $oldname = "$UploadDir/$item";
                $taskName = "MOVE";
                
                if ($DISABLED){ $newname = "$DisabledDir/$item"; $taskName = "DISABLE"; }
                else { $newname = "$UploadDir/$finalFolder$file"; $taskName = "MOVE"; }
            }

            # CREATE FOLDER IF DOESN'T EXIST
            unless ($folder){
                ($folder) = &ExtractFolder($newname);
                &CreateDir($folder);
            }
            
            if ($oldname eq $newname){
                $result .= "\nWARNING: The file <tt>$item</tt> was not touched because its origin is the same as the destination<br/>";
            }
            else {
                $result .= "\n$taskName File <tt>$item</tt> ... ";
                
                if (-e $oldname){
                    if (rename($oldname, $newname)){ $result .= "done<br/>"; }
                    else { $result .= "\n<h2><small>ERROR! Rename failed.</small></h2><br/>"; }
                }
                else {
                    $result .= "\n<h2><small>ERROR! File doesn't exist.</small></h2><br/>";
                }
            }
        }
    }

    # DELETE REMAINING EMPTY DIRECTORIES
    
    print $result;
}

sub SwitchAssetFolder {
    my ($file, $manageDisabled) = @_;
    my ($oldname, $newname, $folder, $result);
    my ($moveto, $newfolder, @marked);
    
    my $targetDir = &NoDirSlash($UploadDir);
    
    # MOVE PROVIDED FILE INTO APPROPRIATE DIRECTORY if id has legitimate filename extension
    if (&ExtensionAllowed($file)){
        ($folder) = $file =~ /(.*?)\/.*/;
        $file =~ s/.*[\/\\](.*)/$1/;
    
        if ($folder ne ""){ &CreateDir( &NoDirSlash($DisabledDir) . "/$folder");  $folder .= '/'; }
        
        $oldname = "$targetDir/$folder$file";
        $newname = &NoDirSlash($DisabledDir) . "/$folder$file";
        
        if ($manageDisabled){
            if (-e $oldname){
                if (rename($oldname, $newname)){ $result .= "\nSuccessfuly disabled <tt>$file</tt><br/><br/>"; }
                else { $result .= "\nEncountered error when attempting to disable <tt>$file</tt><br/><br/>"; }
            }
        }
        else {
            if (-e $newname){
                if (rename($newname, $oldname)){ $result .= "\nSuccessfuly re-enabled <tt>$file</tt><br/><br/>"; }
                else { $result .= "\nEncountered error when attempting to re-enabled <tt>$file</tt><br/><br/>"; }
            }
        }
    }
    
    return $result;
}

sub ProcessFilters {
    my ($filter, @list) = @_;    
    my ($file, @files, $item, $qualifies, $include, @includes, @filters);
    
    # CREATE array of filters
    $filter = lc($filter);
    $filter =~ s/\s//go;
    
    if ($filter ne ""){ 
        if ($filter =~ m/,/){ @filters = split(',', $filter); }
        else { push (@filters, $filter); }
    }
    
    # RUN INCLUSIVE FILTERS
    foreach $file (@list){        
        next unless &ExtensionAllowed($file);        # Only files with valid extensions may be shown
        
        if ($filter eq ""){  push @includes, $file; next; }
        
        $qualifies = 0;                        
        foreach $item (@filters){
            $item =~ s/\s//go;
            $include = $item;

            if ($item =~ m/^\!/){ next; }
            elsif ($include) { if (lc($file) =~ m/$include/){ $qualifies = 1;}}        
        }
        
        if ($qualifies){ push @includes, $file; }
    }
    
    if (scalar(@includes) == 0){ @includes = @list; }
    
    # RUN EXCLUSIVE FILTERS    
    foreach $file (@includes){
        next unless &ExtensionAllowed($file);        # Only files with valid extensions may be shown
        
        if ($filter eq ""){  push @files, $file; next; }
                
        $qualifies = 1;                        
        foreach $item (@filters){
            $item =~ s/\s//go;                    
            unless ($item =~ m/^\!/){ next; }
            $include = substr($item, 1);

            if ($include) { if (lc($file) =~ m/$include/){ $qualifies = 0; }}        
        }
        
        if ($qualifies){ push @files, $file; }
    }
    
    return @files;    
}

sub DoListFiles {
    my ( $id, $filter, $manageDisabled ) = @_;    
    my ( $result, $file, $size, $numlinks, $linkname, $title, $action, $isPriviledged );
    my ( $term, $targetDir, @files, @list, @folders );
    my ( $moveto, $newfolder, $targetDir, @marked);
    
    if ($manageDisabled){ print &GetHeader( "", "Manage Disabled Assets", "" ); }
    else { 
        if (&UserIsEditorOrAdmin()){ print &GetHeader( "", "Manage Active Assets", "" ); }
        else { print &GetHeader( "", "List Assets", "" ); }
    }
    
    print &GetLeftNav();
    print "\n<div class='wikiadmin'>";
        
    # DETERMINE FOLDERS and ASSETS
    if ($manageDisabled){ $targetDir = &NoDirSlash($DisabledDir); }
    else { $targetDir = &NoDirSlash($UploadDir); }

    &ProcessAssets($manageDisabled, $filter);
    $result = &SwitchAssetFolder($id, $manageDisabled);    
    @list = &GetAssetsList($targetDir);
    @folders = &GetAssetFolders($targetDir, @list);
    @files = &ProcessFilters($filter, @list);
    
    if ($filter ne ""){ $term = " using '<em>$filter</em>'"; }
    
    # CREATE OUTPUT HTML
    if ($manageDisabled){ print "\n<h2>", scalar(@files), " disabled assets found: $term</h2>"; }
    else { print "\n<h2>", scalar(@files), " assets found: $term</h2>"; }
        
    print "\n<form id='wikiform' action='$ScriptName' method='POST'>";
    &ShowAssetTable($manageDisabled, @files);    
    &ShowUploadChoices($manageDisabled, "1", @folders);
    
    print "\n<br/>Naming filter: &nbsp;<input type='text' id='filter' name='filter' value='$filter' style='width: 200px;' >";    
    print "\n<br/>Use <code>!</code> to exclude a term, separate terms with a comma.  Use <code>!/</code> to indicate <tt>'MAIN'</tt> folder.<br/>";
    
    if ($manageDisabled){
        print "\n<input type='hidden' name='action' value='listdisabled'>";        
        print "\n<br/><a onclick='listFiles();'><input type='button' value='View Active Files'/></a>";
    }
    else {
        print "\n<input type='hidden' name='action' value='listfiles'>";
        print "\n<br/><a onclick='listDisabled();'><input type='button' value='View Disabled Files'/></a>";
    }
    
    print "\n<input type='submit' value='Continue'>";
    print "\n</form>";
    print "<script>function listDisabled(){ var filter = document.getElementById('filter').value; window.location.href='$ScriptName?action=listdisabled&filter=' + filter; }</script>";
    print "<script>function listFiles(){ var filter = document.getElementById('filter').value; window.location.href='$ScriptName?action=listfiles&filter=' + filter; }</script>";
    print "\n</div>";
    print &GetFooterText();
    print "\n</div></div></div></div></body></html>";                
}

#------------------------------------------------------------------------------
# END_OF_OTHER_CODE
#------------------------------------------------------------------------------
&DoWikiRequest() if ( $RunCGI && ( $_ ne 'nocgi' ) );    # Do everything.
1;    # In case we are loaded from elsewhere

#------------------------------------------------------------------------------
# End of UseModWiki script.
#==============================================================================
