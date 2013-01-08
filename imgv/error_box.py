# imgv error box code by Ryan Kulla, rkulla@gmail.com
import gl
from buttons import imgv_button, hover_button
from img_screen import clean_screen, init_screen, paint_screen
from show_message import show_message
from usr_event import left_click, check_quit, hit_key
from cursor import normal_cursor, hover_cursor
from pygame.display import set_mode, set_caption
from pygame.event import wait
from pygame.mouse import get_pos
from pygame.locals import K_SPACE


def errorbox(title, msg):
    "display a pygame error box"
    clean_screen()
    init_screen()
    screen = set_mode((450, 150))
    normal_cursor()
    set_caption(title)
    show_message(msg, (10, 10), 12, ("bold"))
    ok_rect = imgv_button(screen, " OK ", 20, screen.get_height() - 40, "midtop")
    while 1:
        event = wait()
        cursor = get_pos()
        check_quit(event)
        hover_button(ok_rect, cursor, screen, " OK ", 20, screen.get_height() - 40, "midtop")
        hover_cursor(cursor, [ok_rect])
        if left_click(event):
            if ok_rect.collidepoint(cursor):
                clean_screen()
                raise SystemExit
        if hit_key(event, K_SPACE):
            clean_screen()
            raise SystemExit

