imgv readme by Ryan Kulla 
=========================

Imgv Requirements
-----------------
python2.2 or higher
pygame
python-imaging (PIL)


Environment
===========
The very first thing you should do is create a new environment variable called
"IMGV_HOME" with the value of the directory you installed imgv in. For example,
if you unpacked the imgv source into /usr/home/foo/imgv then put the following line in
your bash_profile (or the equivalent depending on your shell):
	
	export IMGV_HOME="/usr/home/foo/imgv"

If you're using MS-Windows and you unpacked imgv in C:\Program Files\imgv then 
put the following line in your autoexec.bat file:

	set IMGV_HOME=C:\Program Files\imgv

(In Windows you may need to reboot for changes to take affect)


Starting the image viewer
=========================
If you have the source file "imgv.py" type:

        python imgv.py
              or
        python imgv.py <directory|image|remote image>

or if you're in Windows and have the executable binary version "imgv.exe" Click on imgv
from the start menu if it was installed there or in a DOS window type:

        C:\"Program Files"\imgv> imgv.exe
         or
        C:\"Program Files"\imgv> imgv.exe <directory|image|remote image|movie>

(assuming imgv is installed in C:\Program Files\imgv\)
---------------------------------------------------------

Imgv allows the loading of remote images by forming a name like:

	imgv http://www.site.com/bla.jpg

When imgv is running you can click the 'Open URL' menu option and enter a valid URL for
imgv to extract images from such as:

	http://www.site.com/  (note: you usually need that appended / for this to work)
	http://www.site.com/foo.html
	http://www.site.com/bla.jpg


------------------------------------------------

- To load just a single image file type:

	imgv bla.jpg 

------------------------------------------------

Using the image viewer
======================
- When you right click in imgv a menu pops up. Simply click on what you
  want to do. (Clicking your middle mouse button will close the menu)

- Or you can use the keyboard to operate imgv press 'h' from inside imgv
  to get a list of keys supported and their functions. 


Configuration File For IMGV
===========================
In the data/ directory there is a file called 'imgv.conf'.  This is a 
configuration file for imgv that allows you to customize imgv to your needs.

IMGV will first look in your home directory for a file named .imgv.conf (which
you should create by copying the one from the data/ directory to your home
directory). If IMGV could not find .imgv.conf in your home directory it will 
then look for imgv.conf in your data/ directory.  If you have both .imgv.conf
in your home directory and imgv.conf in the data directory IMGV will use the
one in your home directory.


Notes
=====
In order for the play list feature to work you always must have a file named 
'playlists' in the data/ directory (the default).  If you want to create new playlists 
and/or edit them manually using your text editor you need to put the name of the play
list on its own line in the 'playlists' file and also create a file with the
name of the playlist. Make sure there are NO blank lines in either file. I 
recommend only using imgv to handle all the playlist stuff but this way can
be faster.

	To create a new playlist manually:
	cd data/
	echo "new playlist name" >> playlists
	touch "new playlist name"
	
	To add new images to a play list manually:
	cd data/	
	echo "/home/user/pics/bla.jpg" >> "play list name"


If you have questions email me at: rkulla@gmail.com
IMGV's homepage is: http://imgv.sf.net/
If you use IRC, I'm "gt3" on freenode (#python, #pygame).
