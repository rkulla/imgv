# buttons code by Ryan Kulla, rkulla@gmail.com
import gl
import pygame.font
from pygame.display import update


def imgv_button(screen, msg, x, y, where):
    font = pygame.font.Font(gl.FONT_NAME, 10)
    if gl.BEING_HOVERED:
        ren = font.render(msg, 1, gl.BUTTON_TEXTHOVERCOLOR, gl.BUTTON_HOVERCOLOR)
        ren_rect = do_button(screen, ren, where, x, y)
    else:
        ren = font.render(msg, 1, gl.BUTTON_TEXTCOLOR, gl.BUTTON_BGCOLOR)
        ren_rect = do_button(screen, ren, where, x, y)
    return ren_rect


def do_button(screen, ren, where, x, y):
    ren_rect = ren.get_rect().inflate(20, 10)
    if where == "topleft":
        ren_rect.topleft = screen.get_rect().topleft
        if x != None:
            ren_rect[0] = x
        if y != None:
            ren_rect[1] = y
    if where == "midtop":
        ren_rect.midtop = screen.get_rect().midtop
        if y != None:
            ren_rect[1] = y
    if where == "topright":
        ren_rect.topright = screen.get_rect().topright
        if x != None: 
            ren_rect[0] = ren_rect[0] - x
        if y != None:
            ren_rect[1] = y
    if where == None:
        if x != None:
            ren_rect[0] = x
        if y != None:
            ren_rect[1] = ren_rect[1] + y
    screen.blit(ren, ren_rect.inflate(-20, -10))
    update(ren_rect)
    return ren_rect


def hover_button(rect, cursor, screen, msg, x, y, where):
    if rect.collidepoint(cursor):
        gl.BEING_HOVERED = 1
        imgv_button(screen, msg, x, y, where)
    else:
        gl.BEING_HOVERED = 0
        imgv_button(screen, msg, x, y, where)


def close_button(screen):
    close_font = pygame.font.Font(gl.FONT_NAME, 15)
    close_font.set_bold(1)
    close = close_font.render("X", 1, gl.CLOSE_BUTTONCOLOR)
    close_rect = close.get_rect()
    close_rect[0] = screen.get_width() - 20
    screen.blit(close, close_rect)
    pygame.display.update(close_rect)
    return (close_rect, close_font)
