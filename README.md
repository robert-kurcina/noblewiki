# noblewiki
===============================================================================
 NobleWiki Installation Instructions
-------------------------------------------------------------------------------

	Welcome to NobleWiki.  This is a powerful but easy to use Wiki engine
	derived from the UseModWiki wiki engine available at http://www.usemode.com. 
	These instructions cover the installation of the perl programming language, 
	and the Apache HTTP [ Web ]	Server.  NobleWiki requires both in order to
	run.  Once	the installation steps are completed, you will be able to access
	NobleWiki via a browser. The installation steps are for local use only and
	nobody outside of your computer network will be able to see the contents of
	your Web site.

	
	
-------------------------------------------------------------------------------
OVERVIEW
-------------------------------------------------------------------------------

	TIME REQUIRED
		30 minutes


	MANIFEST
		NobleWiki.zip
		ActivePerl-5.10.0.1004-MSWin32-x86-287188.msi
		apache_2.2.9-win32-x86-openssl-0.9.8h-r2.msi
		httpd-vhosts.conf
		README.txt [ this file ]



-------------------------------------------------------------------------------
INSTALLATION
-------------------------------------------------------------------------------

	If you've already installed Apache or Perl, you'll need only to worry about
	the configuration steps for those two packages.

	INSTALL PERL
		1.  Run ActivePerl-5.10.0.1004-MSWin32-x86-287188.msi via double-click
		2.  Install into C:/Program Files/Perl
		
	INSTALL APACHE
		1.  Run apache_2.2.9-win32-x86-openssl-0.9.8h-r2.msi via double-click
		2.  Install into C:/Program Files/Apache Software Foundation [ the default ]
		2.  Start > Apache HTTP Server 2.2 > Control Apache Server > Restart

	TEST APACHE
		1.  Open a browser
		2.  Enter http://localhost/ into the address bar and press ENTER
		3.  You should see an Apache welcome screen
		
	CONFIGURE HOSTS FILE
		1.  Open Notepad application via Start > Programs > Accessories > Notepad
		2.  Edit C:\WINDOWS\System32\drivers\etc\hosts using NotePad
		3.  Add this line
		
		127.0.0.1	lipikas.org
		127.0.0.1	www.lipikas.org

	TEST HOSTS	
		1.  Start > Apache HTTP Server 2.2 > Control Apache Server > Restart
		2.  Open a browser
		3.  Enter http://wiki.lipikas.org/ into the address bar and press ENTER
		4.  You should see the same Apache welcome screen

	PREPARE WIKI
		1.  Unzip NobleWiki.zip
		2.  Copy NobleWiki into C:/Program Files
		
	CONFIGURE APACHE
		1.  Start > Apache HTTP Server 2.2 > Control Apache Server > Stop
		2.  Move httpd-vhosts.conf into 
			E:\Program Files\Apache Software Foundation\Apache2.2\conf\extra
		3.  Edith the file found at 
			C:\Program Files\Apache Software Foundation\Apache2.2\conf\httpd.conf 
			on lines 460-461 to look like this
		
			# Virtual hosts
			Include conf/extra/httpd-vhosts.conf
		
	TEST WIKI
		1.  Start > Apache HTTP Server 2.2 > Control Apache Server > Start
		2.  Enter http://wiki.lipikas.org/ into the address bar and press ENTER
		3.  You should now see the Home page for NobleWiki



-------------------------------------------------------------------------------
USE THE WIKI
-------------------------------------------------------------------------------

	THE SANDBOX
		1.  Click on the SandBox link at the left navigation.
		2.  The page for the SandBox will open up and provide a textarea for
			you to enter WikiMarkup code as you desire.
		3.  Above the textarea are links that you should open into new browser
			tabs that will provide helpful instructions on how to edit a page
			using proper markup code.
		4.  For the SandBox use the following markup by copying and pasting into
			the textarea:
			
			
== Greetings! =

This is my first page.
It links to [http://www.google.com/ an external] Web site.

It links to the WikiContacts page, which is not locked.

It also links to the HomePage, which is LOCKED.

And it links to a page NotYetCreated.


			
		5.  What you've just entered is known as Wiki Markup Language.  Press the 
		    Preview button at the bottom of the textarea to see how the page 
			might look when rendered.
		6.  Notice a few things about the text that you inserted
		
			-- Notice the syntax for creating a level two header is == Greetings! =
			   followed by a blank line. A level one header is = Greetings! = and a 
			   level three header is === Greetings! =
			   
			-- The external link is surrounded by brackets.  The syntax is 
			   [link term] where the link is a complete URL and the term can be any
			   number of words.
			   
			-- Internal links are identified by a WikiWord.  These are terms
			   comprised of words with TWO capitalized letters, the first of which
			   is at the start of the term.  Examples are SomeWord, CompoundTerms,
			   ReallyReallyLongWord.
			   
			-- All WikiWords that don't exist as of yet within the Wiki database
			   will render in RED with a small question mark symbol next to it.  
			   Clicking on that link will prompt the wiki engine to allow you to
			   create that page.
			   
			-- Pages are either LOCKED or un-locked.  Locked pages require at the
			   minimum that a user has clicked on the Preferences link at the bottom
			   of the page and has provided a username and a password.
			   
			   Editor password for you is:          lipikas
			   Administrator password for you is:   enkidu
			   
			   Administrators have enormous power; only one person should ever have
			   the administrator password and that person should endeavor to covet
			   it and learn how to properly manage the wiki.
			   
			-- In order to save the changes made to the SandBox, click on the Save
			   button.  Be sure to play around with the SandBox with the information
			   learned.
