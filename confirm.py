# imgv confirmation screen code by Ryan Kulla, rkulla@gmail.com
import gl
from img_screen import paint_screen
from show_message import show_message
from usr_event import check_quit, hit_key
from buttons import imgv_button, hover_button
from cursor import normal_cursor, hover_cursor
import pygame.event, pygame.display
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION, K_ESCAPE, K_y, K_n


def get_confirmation(screen, confirm_msg):
    paint_screen(screen, gl.IMGV_COLOR)
    pygame.display.update()
    normal_cursor()
    show_message(screen, confirm_msg, "top", 12, ("bold"))
    yes_rect = imgv_button(screen, " YES ", 0, 30, "midtop")
    no_rect = imgv_button(screen, " NO ", 0, 60, "midtop")
    pygame.event.set_blocked(MOUSEMOTION)
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(35)
        cursor = pygame.mouse.get_pos()
        hover_button(yes_rect, cursor, screen, " YES ", 0, 30, "midtop")
        hover_button(no_rect, cursor, screen, " NO ", 0, 60, "midtop")
        hover_cursor(cursor, (yes_rect, no_rect))
        check_quit(event)
        if hit_key(event, K_ESCAPE):
            return 
        if hit_key(event, K_y):
            return "yes"
        if hit_key(event, K_n):
            return "no"
        if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if yes_rect.collidepoint(cursor):
                return "yes"
            if no_rect.collidepoint(cursor):
                return "no"
