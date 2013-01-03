Imgv - cross-platform image viewer.

Latest Version: 3.1.7

About
=====
Imgv is a image viewer with an opinionated interface - meaning that certain
features were add or missing intentionally. It's main opinion is that screen
real-estate is very important and so the interface tries to stay out of your
way. It also has very flexible viewing options, such as the ability to view 4
images at a time, and view/download from URLs.

The viewer also cares about privacy and so it doesn't cache your images and it
even has the ability to temporarily 'hide' what you're viewing.


Requirements
============
- python 2.2 or higher
- pygame
- python-imaging (PIL)

The operating system doesn't matter as long as you have the above requirements.
Thus it should work on Linux, Mac OS X, Windows, etc.

Environment
-----------
The very first thing you should do is create a new environment variable called
*IMGV_HOME* with the value of the directory you installed imgv in. For example,
if you unpacked the imgv source into /usr/home/foo/imgv then put the following line in
your bash_profile (or the equivalent depending on your shell):
    
    export IMGV_HOME="/usr/home/foo/imgv"

If you're using MS-Windows and you unpacked imgv in C:\Program Files\imgv then 
put the following line in your autoexec.bat file:

    set IMGV_HOME=C:\Program Files\imgv

On Windows you may need to reboot for changes to take affect


Starting the image viewer
-------------------------
If you have the source file "imgv.py" type:

    python imgv.py

or:

    python imgv.py <directory|image|remote image>

If you're in Windows and have the executable binary version "imgv.exe" Click on imgv
from the start menu if it was installed there or in a DOS window type:

    C:\"Program Files"\imgv> imgv.exe

or (assuming imgv is installed in C:\Program Files\imgv\):

    C:\"Program Files"\imgv> imgv.exe <directory|image|remote image|movie>



Using the image viewer
----------------------
- When you right click in imgv a menu pops up. Simply click on what you
  want to do. (Clicking your middle mouse button will close the menu)

- Or you can use the keyboard to operate imgv press 'h' from inside imgv
  to get a list of keys supported and their functions. 


Loading images from web sites
-----------------------------
Imgv allows the loading of remote images by forming a name like:

    imgv http://www.site.com/bla.jpg

When imgv is running you can click the 'Open URL' menu option and enter a valid URL for
imgv to extract images from such as:

    http://www.site.com/  (note: you usually need that appended / for this to work)
    http://www.site.com/foo.html
    http://www.site.com/bla.jpg


Configuration File For IMGV
---------------------------
In the data/ directory there is a file called 'imgv.conf'.  This is a 
configuration file for imgv that allows you to customize imgv to your needs.

IMGV will first look in your home directory for a file named .imgv.conf (which
you should create by copying the one from the data/ directory to your home
directory). If IMGV could not find .imgv.conf in your home directory it will 
then look for imgv.conf in your data/ directory.  If you have both .imgv.conf
in your home directory and imgv.conf in the data directory IMGV will use the
one in your home directory.


Playlists
---------
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


Contact
-------
If you have questions email me at: rkulla@gmail.com

IMGV's homepage is: http://imgv.sf.net/
