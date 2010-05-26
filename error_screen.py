# error screen code by Ryan Kulla, rkulla@gmail.com
from usr_event import check_quit
from img_screen import paint_screen
from show_message import show_message
from usr_event import check_quit, hit_key
import pygame.event
from pygame.locals import KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, K_LALT, K_RALT, K_LCTRL, K_RCTRL


def error_screen(screen, msg):
   paint_screen(screen, gl.BLACK)
   while 1:
        event = pygame.event.wait()
        show_message(screen, msg, "top", 12)
        check_quit(event)
        if (event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL)) or event.type == MOUSEBUTTONDOWN:
            return
