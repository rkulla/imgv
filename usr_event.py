# imgv user event code by Ryan Kulla, rkulla@gmail.com
from cursor import wait_cursor
from img_screen import clean_screen
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_q
import pygame.mouse


def check_quit(event):
    "quit the program if the close window icon or the 'q' key is hit"
    if event.type == KEYDOWN and event.key == K_q or event.type == QUIT:
        wait_cursor()
        clean_screen()
        raise SystemExit


def hit_key(event, key):
    if event.type == KEYDOWN and event.key == key:
        return 1
    return 0


def left_click(event):
    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
        return 1
    return 0


def middle_click(event):
    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1]:
        return 1
    return 0 


def right_click(event):
    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
        return 1
    return 0
