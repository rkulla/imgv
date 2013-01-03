# transitional effects code by Ryan Kulla, rkulla@gmail.com
import gl
from img_screen import get_center, paint_screen
from effect_melt import Meltdown
import pygame.event
import pygame.display
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN


def transitional_fx(screen, img):
    if gl.TRANS_FX.find('|') != -1:
        multi = gl.TRANS_FX.split('|')
        for m in multi:
            if m in ("MELT", "melt"):
                melt_it(screen)
            if m in ("FADE_IN", "fade_in"):
                fade_in(screen, img)
    else:
        if gl.TRANS_FX in ("MELT", "melt"):
            melt_it(screen)
        if gl.TRANS_FX in ("FADE_IN", "fade_in"):
            fade_in(screen, img)


def melt_it(screen):
    meltdown = Meltdown(screen)
    surface, dirty = meltdown.step()
    while surface:
        for ev in pygame.event.get():
            if ev.type in (QUIT, KEYDOWN, MOUSEBUTTONDOWN):
                return
        surface.blit(screen, screen.get_size())
        pygame.display.update(dirty)
        surface, dirty = meltdown.step()


def fade_in(screen, image):
    paint_screen(gl.IMGV_COLOR)
    for darken in range(50):
        image.set_alpha(darken)
        r = screen.blit(image, get_center(screen, image))
        pygame.display.update(r)
    image.set_alpha(255)
