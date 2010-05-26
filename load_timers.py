# timer code by Ryan Kulla, rkulla@gmail.com
import gl
from pygame.time import get_ticks


def start_timer():
    return get_ticks()


def check_timer(start):
    return (get_ticks() - start) / 1000.0
