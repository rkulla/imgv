# imgv message rendering code by Ryan Kulla, rkulla@gmail.com
import gl
import pygame.font
from pygame.display import update
from types import StringType


def show_message(screen, msg, down_value, font_size, *font_ops):
    "write a message centered anywhere on the screen"
    font = pygame.font.Font(gl.FONT_NAME, font_size)
    if font_ops:
        if font_ops[0] != "":
            font_options(font_ops, font)
    if not gl.TOGGLE_TRANSPARENT: # use transparent font background:
        ren = font.render(msg, 1, gl.MSG_COLOR)
    else: # use a font background color:
        if gl.TOGGLE_TRANSPARENT and not gl.TEXT_TRANSPARENT:
            ren = font.render(msg, 1, gl.MSG_COLOR, gl.FONT_BG)
        else:
            ren = font.render(msg, 1, gl.WHITE, gl.BLACK)
    if gl.USING_SCROLL_MENU: # to let the blank_fx() work right
        ren = font.render(msg, 1, gl.WHITE, gl.BLACK)
    ren_rect = ren.get_rect()
    if down_value == "bottom":
        ren_rect.midbottom = screen.get_rect().midbottom
    elif down_value == "top":
        ren_rect.midtop = screen.get_rect().midtop
    elif isinstance(down_value, tuple): # allow you to uncenter too:
        ren_rect = ren.get_rect()
        ren_rect[0] = down_value[0]
        ren_rect[1] = down_value[1]
    else:
        ren_rect.centerx = screen.get_rect().centerx
        ren_rect[1] = down_value
    screen.blit(ren, ren_rect)
    update(ren_rect)

    if len(font_ops) > 1:
        # make color emphasis over part of the msg start from beginning of string
        if not gl.TEXT_TRANSPARENT:
            ren = font.render(msg[:font_ops[1][0]], 1, font_ops[1][1], gl.FONT_BG)
        else:
            ren = font.render(msg[:font_ops[1][0]], 1, font_ops[1][1], gl.BLACK)
        screen.blit(ren, ren_rect)
        update(ren_rect)

    gl.TEXT_TRANSPARENT = 0

    return ren_rect


def font_options(font_ops, font):
    "lets you have bold and/or underline and/or italic fonts"
    if type(font_ops[0]) is StringType:
        if font_ops[0] == "bold":
            font.set_bold(1)
        if font_ops[0] == "underline":
            font.set_underline(1)
        if font_ops[0] == "italic":
            font.set_italic(1)
        if font_ops[0] == "transparent":
            gl.TEXT_TRANSPARENT = 1
    else:
        if font_ops[0][0] == "bold":
            font.set_bold(1)
        if font_ops[0][0] == "underline":
            font.set_underline(1)
        if font_ops[0][0] == "italic":
            font.set_italic(1)
        if font_ops[0][0] == "transparent":
            gl.TEXT_TRANSPARENT = 1

    if len(font_ops[0]) > 1:
        if font_ops[0][1] == "underline":
            font.set_underline(1)
        if font_ops[0][1] == "bold":
            font.set_bold(1)
        if font_ops[0][1] == "italic":
            font.set_italic(1)
        if font_ops[0][1] == "transparent":
            gl.TEXT_TRANSPARENT = 1
            
        if len(font_ops[0]) > 2:
            if font_ops[0][2] == "underline":
                font.set_underline(1)
            if font_ops[0][2] == "bold":
                font.set_bold(1)
            if font_ops[0][2] == "italic":
                font.set_italic(1)
            if font_ops[0][2] == "transparent":
                gl.TEXT_TRANSPARENT = 1


def truncate_name(name, allow):
    "Truncate long strings and append a '...'"
    if len(name) > allow:
        if name[:allow][-1] == ' ': 
            name = name[:allow - 1] # make 'foo ...' into 'foo...'
        name = name[:allow] + '...'
        if name[-4:] == '....': # make 'foo....' into 'foo...'
            name = name[:-1] 
    return name
