#!/usr/bin/env python


"""
    imgv.py
    Description: Image viewing application
    Version: 3.1.7
    Author: Ryan Kulla
    Email: rkulla@gmail.com
"""


from sys import platform
from os import environ
if platform == 'win32':
    # use the windib driver when the default is DirectX:
    environ['SDL_VIDEODRIVER'] = 'windib'
import pygame.event
import pygame.time
from pygame.display import set_caption, update
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, Rect, KEYDOWN, KEYUP, RESIZABLE, VIDEORESIZE, MOUSEBUTTONUP, K_UP, K_DOWN, K_RIGHT, K_LEFT
import gl
from load_timers import start_timer, check_timer
from img_screen import init_screen, get_center, my_update_screen, img_border, paint_screen
from show_message import show_message
from cursor import wait_cursor, normal_cursor, drag_hand_cursor, grab_hand_cursor
from usr_event import check_quit, right_click, left_click
from load_img import load_img
from handle_keyboard import handle_keyboard
from main_menu import command_main_menu
from pan import command_down, command_up, command_right, command_left
from res import command_fullscreen


class Imgv(object):
    def __init__(self):
        pygame.time.delay(5)  # to make start_timer() work initially
        start = start_timer()
        pygame.init()  # needed for Mac OSX?
        init_screen()
        wait_cursor()
        self.gfx = {}
        self.gfx['screen'] = pygame.display.set_mode(gl.DEFAULT_RES, RESIZABLE)
        set_caption(gl.TITLE)
        if gl.REMOTE == 1:
            show_message("Loading image. Please wait..", 34, 42)
        self.gfx['file'] = 0
        if len(gl.files) < 1:
            gl.files = [gl.IMGV_LOGO]
        self.gfx['img'] = load_img(gl.files[self.gfx['file']])
        wait_cursor()
        self.gfx['refresh_img'] = self.gfx['img']
        self.gfx['new_img'] = self.gfx['img']
        self.gfx['rect'] = get_center(self.gfx['screen'], self.gfx['new_img'])
        self.ns = check_timer(start)
        my_update_screen(self.gfx['new_img'], self.gfx['rect'], self.gfx['file'], self.ns)
        normal_cursor()
        if gl.START_FULLSCREEN:
            command_fullscreen()
            my_update_screen(self.gfx['new_img'], self.gfx['rect'], self.gfx['file'], self.ns)
        self.minus1 = 0
        self.minus2 = 0
        self.last_rect = Rect(self.gfx['rect'])

    def main(self):
        # start with menu open
        self.gfx = command_main_menu(self.gfx, self.ns)

        # main loop
        while 1:
            self.event = pygame.event.poll()
            pygame.time.wait(1)  # so pygame doesn't use 100% CPU
            cursor = pygame.mouse.get_pos()
            self.last_rect = Rect(self.gfx['rect'])

            # drag image code:
            if gl.HAND_TOOL:
                if left_click(self.event):  # calculate drag coordinates:
                    if gl.IMG_BORDER:
                        self.border_fix()  # erase the current border
                    grab_hand_cursor()
                    self.minus1 = cursor[0] - self.gfx['rect'][0]
                    self.minus2 = cursor[1] - self.gfx['rect'][1]
                    gl.DO_DRAG = 1
                if self.event.type == MOUSEMOTION and gl.DO_DRAG:  # move the image when dragged:
                    grab_hand_cursor()
                    self.gfx['rect'][0] = cursor[0] - self.minus1
                    self.gfx['rect'][1] = cursor[1] - self.minus2
                    self.gfx['screen'].fill(gl.IMGV_COLOR, self.last_rect)
                    self.gfx['screen'].blit(self.gfx['new_img'], self.gfx['rect'])
                    update(self.gfx['rect'].union(self.last_rect))
                if self.event.type == MOUSEBUTTONUP:  # released mouse button, redisplay status bars:
                    drag_hand_cursor()
                    my_update_screen(self.gfx['new_img'], self.gfx['rect'], self.gfx['file'], self.ns)
                    gl.DO_DRAG = 0

            if self.event.type == VIDEORESIZE:
                self.gfx['screen'] = pygame.display.set_mode(self.event.dict['size'], RESIZABLE)
                self.gfx['rect'] = get_center(self.gfx['screen'], self.gfx['new_img'])
                my_update_screen(self.gfx['new_img'], self.gfx['rect'], self.gfx['file'], self.ns)
            if self.event.type == KEYDOWN:
                gl.HAND_TOOL = 0
                if self.event.key not in (K_DOWN, K_UP, K_RIGHT, K_LEFT):
                    normal_cursor()  # stop displaying hand tool
                (self.gfx['screen'], self.gfx['rect'], self.gfx['new_img'], self.gfx['img'],
                 self.gfx['refresh_img'], self.gfx['file'], self.last_rect) =\
                handle_keyboard(self.event, self.gfx, self.last_rect, self.ns)
            if self.event.type == KEYUP:
                self.stop_auto_repeat()
            check_quit(self.event)

            if self.event.type == MOUSEBUTTONDOWN and right_click(self.event):
                self.open_main_menu()

            # Re-open the purposely closed window that frees up RAM
            if (gl.KEEP_MENU_OPEN == "1" and gl.COUNT_CLICKS == 1) or gl.JUST_RESIZED:
                gl.COUNT_CLICKS = 0
                gl.JUST_RESIZED = 0
                self.gfx = command_main_menu(self.gfx, self.ns)

            self.start_auto_repeat()

    def open_main_menu(self):
        gl.HAND_TOOL = 0
        self.gfx = command_main_menu(self.gfx, self.ns)

    def start_auto_repeat(self):
        screen = self.gfx['screen']
        rect = self.gfx['rect']
        new_img = self.gfx['new_img']
        file = self.gfx['file']
        if gl.MY_KEYDOWN:
            if rect.bottom > screen.get_height():
                command_up(rect, self.last_rect, new_img, file)
                if gl.IMG_BORDER:
                    self.border_fix()
                    img_border(new_img, rect)
        if gl.MY_KEYUP:
            if rect.top < 0:
                command_down(rect, self.last_rect, new_img, file)
                if gl.IMG_BORDER:
                    self.border_fix()
                    img_border(new_img, rect)
        if gl.MY_KEYRIGHT:
            if rect.right > screen.get_width():
                command_left(rect, self.last_rect, new_img, file)
                if gl.IMG_BORDER:
                    self.border_fix()
                    img_border(new_img, rect)
        if gl.MY_KEYLEFT:
            if rect.left < 0:
                command_right(rect, self.last_rect, new_img, file)
                if gl.IMG_BORDER:
                    self.border_fix()
                    img_border(new_img, rect)
        if self.event.type == MOUSEBUTTONDOWN:
            if self.event.dict['button'] == 4:  # mouse wheel up
                if rect.top < 0:
                    command_down(rect, self.last_rect, new_img, file)
                    if gl.IMG_BORDER:
                        self.border_fix()
                        img_border(new_img, rect)
            if self.event.dict['button'] == 5:  # mouse wheel down
                if rect.bottom > screen.get_height():
                    command_up(rect, self.last_rect, new_img, file)
                    if gl.IMG_BORDER:
                        self.border_fix()
                        img_border(new_img, rect)

    def border_fix(self):
        "draw over the last placed border with the background color to make it disappear"
        if gl.LRECT or gl.RRECT or gl.TRECT or gl.BRECT:
            paint_screen(gl.IMGV_COLOR, gl.LRECT)
            paint_screen(gl.IMGV_COLOR, gl.RRECT)
            paint_screen(gl.IMGV_COLOR, gl.TRECT)
            paint_screen(gl.IMGV_COLOR, gl.BRECT)

    def stop_auto_repeat(self):
        gl.MY_KEYDOWN = gl.MY_KEYUP = gl.MY_KEYRIGHT = gl.MY_KEYLEFT = 0


if __name__ == '__main__':
    imgv = Imgv()
    imgv.main()
