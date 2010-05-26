IMGV Instructions (by Ryan Kulla -- rkulla@gmail.com)
=====================================================

Note that the online documentation for imgv is MUCH better than this readme file. http://imgv.sf.net/


DO THIS FIRST
=============
Set the Environment
--------------------
If you're using MS-Windows and you unpacked imgv in C:\Program Files\imgv then put the following line in your autoexec.bat file:

	set IMGV_HOME=C:\Program Files\imgv

(Depending on your version of Windows you may need to reboot for changes to take affect)


If YOU INSTALLED IMGV FROM THE SELF-INSTALLER EXECUTABLE, READ HERE
===================================================================
Running imgv
------------
Click on imgv from the start menu or it's icon on the desktop.
You can also run it from the command line by clicking the Windows "Start" menu and then click "Run" and type in
"cmd.exe" for command line window. Then change directories to where imgv was installed (ie: cd C:\Program Files\imgv\") and type type:

    C:\"Program Files"\imgv> imgv.exe
Or:
    C:\"Program Files"\imgv> imgv.exe <directory|image|remote image|movie>
____________________________________________________________________________________________________


SOURCE CODE USERS ONLY
======================
Running imgv
------------
If you have the source file "imgv.py" type:

        python imgv.py
              or
        python imgv.py <directory|image|remote image>

____________________________________________________________________________________________________

Imgv allows the loading of remote images by forming a name like:

	imgv http://www.site.com/bla.jpg

When imgv is running you can click the 'Open URL' menu option and enter a valid URL for
imgv to extract images from such as:

	http://www.site.com/  (note: you usually need that appended / for this to work)
	http://www.site.com/foo.html
	http://www.site.com/bla.jpg


------------------------------------------------

-To load just a single image file type:

	imgv bla.jpg 

------------------------------------------------

Using the image viewer
======================
-When you right click in imgv a menu pops up. Simply click on what you want to do. (Clicking your middle-mouse button will close the menu)
-Or you can use the keyboard to operate imgv. Click 'help' or press 'h' to get a list of keyboard shortcuts. 


Configuration File For IMGV
===========================
In the data/ directory there is a file called "imgv.conf". This is a configuration file for imgv that allows you to customize imgv to your needs.

IMGV will first look in your home directory for a file named .imgv.conf (which you should create by copying the one from the data/ directory to your home directory). If IMGV could not find .imgv.conf in your home directory it will then look for imgv.conf in your data/ directory.  If you have both .imgv.conf in your home directory and imgv.conf in the data directory IMGV will use the one in your home directory.


Notes
=====
In order for the playlist feature to work you always must have a file named "playlists" in the data/ directory (the default). 

_________________________________________________________
If you have questions email me at: rkulla@gmail.com
IMGV's homepage is: http://imgv.sourceforge.net/
If you use IRC, I'm "gt3" on freenode (#python, #pygame).
