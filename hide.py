# image hiding code by Ryan Kulla, rkulla@gmail.com
import gl
from img_screen import my_update_screen, get_center, paint_screen
from cursor import normal_cursor
from usr_event import check_quit
import pygame.event
from pygame.display import set_caption, set_icon
from res import  adjust_screen, restore_screen
from input_box import ask
from show_message import show_message
from pygame.locals import K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB, MOUSEBUTTONDOWN, KEYDOWN, NOFRAME
from time import ctime
from random import shuffle


def command_hide(screen, new_img, rect, file):
    "hide the image by making the screen blank"
    (screen, before_winsize, not_accepted) = adjust_screen(screen, NOFRAME)
    set_caption("")
    hide(screen)
    screen = restore_screen(screen, before_winsize, not_accepted, new_img, file, rect)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, screen, rect, file)


def hide(screen):
    paint_screen(screen, gl.BLACK)
    set_icon(pygame.image.load(gl.DATA_DIR + "imgv-icon-blank.png"))
    normal_cursor()
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(150)
        check_quit(event)
        if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB):
            if gl.CORRECT_PASSWORD.lower() not in ("none", None):
                pw = ask(screen, "Password")
                if pw == gl.CORRECT_PASSWORD:
                    break
                else:
                    show_message(screen, "Incorrect Password", (150), 24, ("bold", "transparent"))
                    show_message(screen, "Press any key to try again", (175), 12, ("bold", "transparent"))
                    f = open(gl.DATA_DIR + "security.log", "a")
                    f.write("Password failure: %s\n" % ctime())
                    f.close()
                    continue
            else:
                break
    set_icon(pygame.image.load(gl.DATA_DIR + "imgv-icon.png"))
