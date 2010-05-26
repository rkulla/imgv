# imgv input box code by Ryan Kulla, rkulla@gmail.com
import gl
from show_message import show_message
from img_screen import paint_screen
from buttons import close_button
from cursor import hover_cursor
import types
import pygame.event, pygame.font, pygame.draw
from pygame.display import flip
from pygame.locals import KEYDOWN, K_BACKSPACE, K_RETURN, K_ESCAPE, K_UP, K_DOWN, Rect, MOUSEBUTTONDOWN
from encodings import * # needed for py2exe


def get_key(esc_rect):
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1)
        cursor = pygame.mouse.get_pos()
        if event.type == KEYDOWN:
            ev_unicode = event.unicode
            if type(ev_unicode) == types.UnicodeType:
                if ev_unicode == '':
                    ev_unicode = 0
                else:
                    ev_unicode = ord(ev_unicode)
            value = unichr(ev_unicode).encode('latin1')
            return (event.key, value)
        hover_cursor(cursor, (esc_rect,))
        if event.type == MOUSEBUTTONDOWN:
            if esc_rect.collidepoint(cursor):
                return (K_ESCAPE, None)


def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    box_len = 600
    fontobject = pygame.font.Font(gl.FONT_NAME, 12)
    mid_height = (screen.get_height() / 2) - 10
    pygame.draw.rect(screen, (0, 0, 0), (10, mid_height - 3, 600, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255), (10, mid_height - 3, box_len, 24), 1)
    if fontobject.size(message[gl.SKIP:])[0] >= (box_len - 1):
        # lets the line continue on when it reaches the end of the box
        gl.SKIP += 90
    else:
        if len(message[gl.SKIP:]) != 0:
            screen.blit(fontobject.render(message[gl.SKIP:], 1, (255, 255, 255)), (14, mid_height))
        else:
            screen.blit(fontobject.render(message, 1, (255, 255, 255)), (14, mid_height))
    flip()


def ask(screen, question, hist_list=[''], count=0):
    current_string = []
    (esc_rect, font) = close_button(screen)
    if question in ("Password", "New password"):
        paint_screen(screen, gl.BLACK, esc_rect) # Erase the close button, no need for it 
    if gl.ISURL:
        display_box(screen, "%s%s_" % (question, "".join(current_string)))
    else:
        display_box(screen, "%s: %s_" % (question, "".join(current_string)))
    while 1:
        (inkey, value) = get_key(esc_rect)
        if inkey == K_BACKSPACE:
            if len(current_string) == 1:
                # allows backspacing to work on the "readline" strings
                current_string = list(current_string[0])
            current_string = current_string[0:-1]
        elif inkey == K_RETURN:
            gl.SKIP = 0 # reset to render message properly
            show_message(screen, ' ' * 40, "bottom", 12) # erase message
            break
        elif inkey == K_ESCAPE:
            gl.ISURL = 0
            if gl.WAS_IN_CHANGE_DRIVES:
                gl.ADDED_DIR_NUMS = 0
            paint_screen(screen, gl.BLACK, Rect(0, 255, screen.get_width(), 100)) # erase box from screen
            show_message(screen, ' ' * 40, "bottom", 12) # erase message
            return None
        elif inkey == K_UP:
            if count < len(hist_list):
                current_string = current_string[1:]
                current_string.insert(0, hist_list[-count - 1])
                count = count + 1
        elif inkey == K_DOWN:
            if count > 0:
                count = count - 1
                current_string = current_string[1:]
                current_string.insert(0, hist_list[-count])
        elif inkey <= 127:
            current_string.append(value)
        if gl.ISURL:
            display_box(screen, "%s%s_" % (question, "".join(current_string)))
        else:
            display_box(screen, "%s: %s_" % (question, "".join(current_string)))

    current_string = "".join(current_string)
    hist_list.append(current_string)
    if gl.ISURL:
        gl.ISURL = 0
        return "%s%s" % ("http://", current_string)
    else:
        return current_string
