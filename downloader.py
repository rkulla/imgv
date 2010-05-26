# remote image downloading code by Ryan Kulla, rkulla@gmail.com
import gl
from os import sep
from os.path import basename
from img_screen import paint_screen
from sys import platform
if platform == 'win32':
    import BmpImagePlugin, JpegImagePlugin, PngImagePlugin, SgiImagePlugin, SunImagePlugin, TgaImagePlugin, TiffImagePlugin, PcxImagePlugin, PpmImagePlugin, XpmImagePlugin # for py2exe to work with PIL
try:
    import Image # PIL
except:
    print "You are missing the python-imaging package (PIL). Please install it"
from usr_event import check_quit
from cursor import normal_cursor
from show_message import show_message
import pygame.event
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, K_LALT, K_RALT


def save_remote_img(screen, file):
    save_path = gl.DATA_DIR + "downloads" + sep
    filename = gl.files[file]
    paint_screen(screen, gl.BLACK)
    try:
        im = Image.open(gl.REMOTE_IMG_DATA)

        show_message(screen, "Saving: %s" % basename(gl.files[file]), (20, 50), 12, ("bold"))
        show_message(screen, "From: %s" % filename[:filename.rindex('/')] + '/', (20, 70), 12, ("bold"))
        show_message(screen, "To: %s" % save_path, (20, 90), 12, ("bold"))

        im.save(save_path + basename(filename))

        show_message(screen, "Done", (20, 120), 12, ("bold", "underline"))
        show_message(screen, "[Press any key]", "bottom", 15)
        gl.ALREADY_DOWNLOADED = 1
        normal_cursor()
    except:
        return
    
    while 1:
        event = pygame.event.wait()
        check_quit(event)
        #if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
        if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT):
            return
        
