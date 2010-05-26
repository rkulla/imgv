#! /usr/bin/env python


""" imgv.py 
    Description: Image viewing application
    Version: 3.1.5
    Author: Ryan Kulla 
    Site: http://imgv.sourceforge.net/
    Email: rkulla@gmail.com
    IRC: gt3 (freenode) """


from sys import platform
from os import environ
if platform == 'win32': 
    # use the windib driver when the default is DirectX:
    environ['SDL_VIDEODRIVER'] = 'windib'
import pygame.event, pygame.time
from pygame.display import set_caption, set_mode, update
from pygame.locals import  MOUSEMOTION, MOUSEBUTTONDOWN, Rect, KEYDOWN, KEYUP, RESIZABLE, VIDEORESIZE, MOUSEBUTTONUP, K_UP, K_DOWN, K_RIGHT, K_LEFT
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

def main():
    pygame.time.delay(5) # to make start_timer() work initially
    start = start_timer()
    num_imgs = len(gl.files) 
    pygame.init() # needed for Mac OSX?
    init_screen()
    wait_cursor()
    screen = pygame.display.set_mode(gl.DEFAULT_RES, RESIZABLE)
    set_caption(gl.TITLE)
    if gl.REMOTE == 1:
        show_message(screen, "Loading image. Please wait..", 34, 42)
    file = 0
    if num_imgs < 1:
        gl.files = [gl.IMGV_LOGO]
        num_imgs = 1 
        img = load_img(gl.files[file], screen)
    else:
        img = load_img(gl.files[file], screen)
    wait_cursor()
    img_width = img.get_width()
    img_height = img.get_height()
    refresh_img = img
    new_img = img
    rect = get_center(screen, new_img)
    ns = check_timer(start)
    my_update_screen(new_img, screen, rect, file, num_imgs, ns)
    normal_cursor()
    if gl.START_FULLSCREEN:
        command_fullscreen(screen, new_img, file, num_imgs, rect)
        my_update_screen(new_img, screen, rect, file, num_imgs, ns)
    # start with menu open
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    new_img_width = new_img.get_width()
    new_img_height = new_img.get_height()
    (refresh_img, screen, file, num_imgs, new_img, img,\
    new_img_width, new_img_height, rect) = command_main_menu(refresh_img, screen,\
    file, len(gl.files), rect, new_img, img, new_img_width, new_img_height, ns)
    minus1 = minus2 = 0

    # main loop
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1) # so pygame doesn't use 100% CPU
        cursor = pygame.mouse.get_pos()
        last_rect = Rect(rect)
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        new_img_width = new_img.get_width()
        new_img_height = new_img.get_height()

        # drag image code:
        if gl.HAND_TOOL:
            if left_click(event): # calculate drag coordinates:
                if gl.IMG_BORDER:
                    border_fix(screen) # erase the current border
                grab_hand_cursor()
                minus1 = cursor[0] - rect[0]
                minus2 = cursor[1] - rect[1]
                gl.DO_DRAG = 1
            if event.type == MOUSEMOTION and gl.DO_DRAG: # move the image when dragged:
                grab_hand_cursor()
                rect[0] = cursor[0] - minus1 
                rect[1] = cursor[1] - minus2
                screen.fill(gl.IMGV_COLOR, last_rect)
                screen.blit(new_img, rect)
                update(rect.union(last_rect))
            if event.type == MOUSEBUTTONUP: # released mouse button, redisplay status bars:
                drag_hand_cursor()
                my_update_screen(new_img, screen, rect, file, num_imgs, ns)
                gl.DO_DRAG = 0

        if event.type == VIDEORESIZE:#
             print 'resize imgv.py'#
             screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)
             rect = get_center(screen, new_img)
             my_update_screen(new_img, screen, rect, file, num_imgs, ns)
        if event.type == KEYDOWN:
            gl.HAND_TOOL = 0
            if event.key not in (K_DOWN, K_UP, K_RIGHT, K_LEFT):
                normal_cursor() # stop displaying hand tool
            (screen, rect, new_img, img, refresh_img, file, num_imgs,\
            screen_width, screen_height, new_img_width, new_img_height, last_rect) =\
            handle_keyboard(event, screen, rect, new_img, img, refresh_img, file, len(gl.files),\
            screen_width, screen_height, new_img_width, new_img_height, last_rect, ns)
        if event.type == KEYUP:
             stop_auto_repeat()
        check_quit(event)

        if event.type == MOUSEBUTTONDOWN: # open main menu:
            if right_click(event):
                gl.HAND_TOOL = 0
                (refresh_img, screen, file, num_imgs, new_img, img,\
                new_img_width, new_img_height, rect) = command_main_menu(refresh_img, screen,\
                file, num_imgs, rect, new_img, img, new_img_width, new_img_height, ns)
        if (gl.KEEP_MENU_OPEN == "1" and gl.COUNT_CLICKS == 1) or gl.JUST_RESIZED: # Re-open the purposely closed window that frees up RAM
            gl.COUNT_CLICKS = 0
            gl.JUST_RESIZED = 0
            (refresh_img, screen, file, num_imgs, new_img, img,\
            new_img_width, new_img_height, rect) = command_main_menu(refresh_img, screen,\
            file, num_imgs, rect, new_img, img, new_img_width, new_img_height, ns)
        start_auto_repeat(rect, last_rect, new_img, screen, file, len(gl.files), screen_width, screen_height, event)
    clean_screen()


def start_auto_repeat(rect, last_rect, new_img, screen, file, num_imgs, screen_width, screen_height, event):
    if gl.MY_KEYDOWN:
        if rect.bottom > screen_height:
            command_up(rect, last_rect, new_img, screen, file, num_imgs, screen_height)
            if gl.IMG_BORDER:
                border_fix(screen)
                img_border(screen, new_img.get_width(), new_img.get_height(), rect[0], rect[1])
    if gl.MY_KEYUP:
        if rect.top < 0:
            command_down(rect, last_rect, new_img, screen, file, num_imgs)
            if gl.IMG_BORDER:
                border_fix(screen)
                img_border(screen, new_img.get_width(), new_img.get_height(), rect[0], rect[1])
    if gl.MY_KEYRIGHT:
        if rect.right > screen_width:
            command_left(rect, last_rect, new_img, screen, file, num_imgs, screen_width)   
            if gl.IMG_BORDER:
                border_fix(screen)
                img_border(screen, new_img.get_width(), new_img.get_height(), rect[0], rect[1])
    if gl.MY_KEYLEFT:
        if rect.left < 0:
            command_right(rect, last_rect, new_img, screen, file, num_imgs)
            if gl.IMG_BORDER:
                border_fix(screen)
                img_border(screen, new_img.get_width(), new_img.get_height(), rect[0], rect[1])
    if event.type == MOUSEBUTTONDOWN:
        if event.dict['button'] == 4: # mouse wheel up
            if rect.top < 0:
                command_down(rect, last_rect, new_img, screen, file, num_imgs)
                if gl.IMG_BORDER:
                    border_fix(screen)
                    img_border(screen, new_img.get_width(), new_img.get_height(), rect[0], rect[1])
        if event.dict['button'] == 5: # mouse wheel down
            if rect.bottom > screen_height:
                command_up(rect, last_rect, new_img, screen, file, num_imgs, screen_height)
                if gl.IMG_BORDER:
                    border_fix(screen)
                    img_border(screen, new_img.get_width(), new_img.get_height(), rect[0], rect[1])


def border_fix(screen):
    "draw over the last placed border with the background color to make it disappear"
    if gl.LRECT or gl.RRECT or gl.TRECT or gl.BRECT:
        paint_screen(screen, gl.IMGV_COLOR, gl.LRECT)
        paint_screen(screen, gl.IMGV_COLOR, gl.RRECT)
        paint_screen(screen, gl.IMGV_COLOR, gl.TRECT)
        paint_screen(screen, gl.IMGV_COLOR, gl.BRECT)


def stop_auto_repeat():
    gl.MY_KEYDOWN = gl.MY_KEYUP = gl.MY_KEYRIGHT = gl.MY_KEYLEFT = 0


if __name__ == '__main__': 
    main()
