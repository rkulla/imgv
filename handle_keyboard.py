# keyboard event code by Ryan Kulla, rkulla@gmail.com
import gl
from cfg import get_config_val
from os import getcwd, chdir
from os.path import basename
from img_screen import get_center, my_update_screen, img_border
from dir_nav import command_show_dirs
from usr_event import hit_key
from list_images import command_img_names
#from res import resize_it
from edit import command_edit_menu
from img_surf import command_next_img, command_prev_img, command_last_img, command_first_img
from refresh import command_refresh
from res import command_640x480, command_800x600, command_1024x768, command_1280x1024, command_fullscreen, command_show_res_modes, adjust_screen, restore_screen
from open_url import open_url
from help import command_help
from verbose import command_verbose_info
from zoom import command_zoom_in, command_zoom_out
from cursor import normal_cursor, wait_cursor, drag_hand_cursor
from slideshow import my_slideshow
from four import command_four
from thumb import command_thumbs
from pan import command_full_right, command_full_left, command_full_up, command_full_down
from randomizer import command_shuffle, command_unshuffle
from playlist import command_add_to_play_list, command_play_list_options
from hide import command_hide
from rm_img import command_remove_img, command_delete_img
from confirm import get_confirmation
from rotate import command_rotate_left, command_rotate_right, command_horiz, command_vert
from downloader import save_remote_img
from load_img import load_img
from load_timers import start_timer, check_timer
import pygame.key
from pygame.locals import *


def handle_keyboard(event, gfx, last_rect, ns):
    screen = gfx['screen']
    rect = gfx['rect']
    new_img = gfx['new_img']
    img = gfx['img']
    refresh_img = gfx['refresh_img']
    file = gfx['file']

    new_img_width = new_img.get_width()
    new_img_height = new_img.get_height()
    if hit_key(event, K_d):
        gl.USING_SCROLL_MENU = 1
        # save current things in case the user ESCAPES out of show_dirs()
        gl.LAST_DIR = getcwd()
        last_files = gl.files
        (last_new_img, last_img, last_refresh_img, last_file,
         last_rect) = (new_img, img, refresh_img, file, rect)
        (new_img, img, refresh_img, file,
         rect) = command_show_dirs(new_img, img, screen, rect, file)
        # user ESCAPED from show_dirs, reset last values
        if gl.ESCAPED:
            gl.ADDED_DIR_NUMS = 0
            (new_img, img, refresh_img, file, rect) = (last_new_img,
                                                       last_img, last_refresh_img, last_file, last_rect)
            chdir(gl.LAST_DIR)
            gl.files = last_files
            gl.USING_SCROLL_MENU = 0
            my_update_screen(new_img, rect, file)
        else:
            gl.REFRESH_IMG_COUNT = 0
        gl.ESCAPED = 0
        gl.USING_SCROLL_MENU = 0
    if hit_key(event, K_i):
        (new_img, img, refresh_img, file,
         rect) = command_img_names(screen, new_img, img, file, rect)
    if hit_key(event, K_F1):
        gl.CALC_ZOOM = 0
        zoom_percent = gl.CURRENT_ZOOM_PERCENT
        real_width = gl.REAL_WIDTH
        command_help(screen, new_img, file, rect)
        if gl.ESCAPED:
            gl.CURRENT_ZOOM_PERCENT = zoom_percent
            gl.REAL_WIDTH = real_width
        gl.ESCAPED = 0
    if hit_key(event, K_F2):
        rect = command_640x480(new_img, file, rect)
        normal_cursor()
    if hit_key(event, K_F3):
        rect = command_800x600(new_img, file, rect)
        normal_cursor()
    if hit_key(event, K_F4):
        rect = command_1024x768(new_img, file, rect)
        normal_cursor()
    if hit_key(event, K_F5):
        rect = command_1280x1024(new_img, file, rect)
        normal_cursor()
    if hit_key(event, K_F6):
        screen = command_fullscreen()
        rect = get_center(screen, new_img)
        my_update_screen(new_img, rect, file)
        normal_cursor()
    if event.type == KEYDOWN:  # alt+enter code
        mods = pygame.key.get_mods()
        if ((event.key == K_RETURN and mods & KMOD_ALT)):
            screen = command_fullscreen()
            rect = get_center(screen, new_img)
            my_update_screen(new_img, rect, file)
    if hit_key(event, K_F7):
        gl.USING_SCROLL_MENU = 1
        gl.CALC_ZOOM = 0
        zoom_percent = gl.CURRENT_ZOOM_PERCENT
        real_width = gl.REAL_WIDTH
        rect = command_show_res_modes(screen, new_img, file, rect)
        gl.CURRENT_ZOOM_PERCENT = zoom_percent
        gl.REAL_WIDTH = real_width
        gl.USING_SCROLL_MENU = 0
        my_update_screen(new_img, rect, file)
        normal_cursor()
    if hit_key(event, K_s):
        (new_img, img, refresh_img, rect) = command_shuffle(
            new_img, img, screen, rect, file)
    if hit_key(event, K_u):
        (new_img, img, refresh_img, rect,
         file) = command_unshuffle(new_img, img, screen, rect, file)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if event.key == K_r and mods & KMOD_CTRL == 0:
            if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                gl.CALC_ZOOM = 0
                (new_img, img,
                 rect) = command_rotate_right(new_img, screen, file, rect)
            else:
                print "Can't rotate. Out of memory."
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if event.key == K_r and mods & KMOD_CTRL:
            if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                gl.CALC_ZOOM = 0
                (new_img, img, rect) = command_rotate_left(
                    new_img, screen, file, rect)
            else:
                print "Can't rotate. Out of memory."
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if event.key == K_p and mods & KMOD_CTRL == 0:
            command_add_to_play_list(screen, gl.files[file])
            gl.SORT_HIT = 0
            my_update_screen(new_img, rect, file)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if event.key == K_p and mods & KMOD_CTRL:
            (new_img, new_img, new_img, file,
             rect) = command_play_list_options(screen, file)
            gl.SORT_HIT = 0
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if event.key == K_x and mods & KMOD_CTRL == 0:
            command_hide(screen, new_img, rect, file)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if event.key == K_x and mods & KMOD_CTRL:
            if get_config_val("ON_THE_FLY_EXIF_STATUS_BAR") == 1:
                gl.ON_FLY_EXIF_STATUS_BAR ^= 1
            gl.TOGGLE_STATUS_BAR ^= 1
            my_update_screen(new_img, rect, file)
            normal_cursor()
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_MINUS or event.key == K_KP_MINUS) and mods & KMOD_CTRL == 0:
            if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                try:
                    (
                        new_img, img, rect) = command_zoom_out(new_img, new_img_width, new_img_height,
                                                               img, screen, file, rect, "normal")
                except:
                    print 'Out of memory.'
            else:
                print "Can't zoom out. Out of memory. Resetting the image."
                gl.SKIP_FIT = 1
                gl.ZOOM_EXP = 0
                start = start_timer()
                wait_cursor()
                new_img = load_img(gl.files[file])
                img = refresh_img = new_img
                rect = get_center(screen, new_img)
                ns = check_timer(start)
                my_update_screen(new_img, rect, file, ns)
                normal_cursor()
                gl.N_MILLISECONDS = "0"
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_MINUS or event.key == K_KP_MINUS) and mods & KMOD_CTRL:
            try:
                (
                    new_img, img, rect) = command_zoom_out(new_img, new_img_width, new_img_height,
                                                           img, screen, file, rect, "double")
            except:
                print 'Out of memory.'
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_EQUALS or event.key == K_KP_PLUS) and mods & KMOD_CTRL == 0:
            # Zoom in only if there seems to be enough memory
            if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                try:  # triple zoom crash protection
                    (
                        new_img, img, rect) = command_zoom_in(new_img, new_img_width, new_img_height, img,
                                                              screen, gl.files, file, rect, "normal")
                except:
                    print 'Zoom max reached.'
            else:
                print 'Zoom max reached.'
    if event.type == KEYDOWN:  # ctrl+'+' code
        mods = pygame.key.get_mods()
        if (event.key == K_EQUALS or event.key == K_KP_PLUS) and (mods & KMOD_CTRL and mods & KMOD_ALT == 0):
            if int(gl.N_MILLISECONDS) < gl.DBL_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                try:
                    (
                        new_img, img, rect) = command_zoom_in(new_img, new_img_width, new_img_height, img,
                                                              screen, gl.files, file, rect, "double")
                except:
                    print 'Zoom max reached.'
            else:
                print 'Zoom max reached.'
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_EQUALS or event.key == K_KP_PLUS) and (mods & KMOD_CTRL and mods & KMOD_ALT):
            try:
                (
                    new_img, img, rect) = command_zoom_in(new_img, new_img_width, new_img_height, new_img,
                                                          screen, gl.files, file, rect, "scale2x")
            except:
                print 'Zoom max. Out of memory.'
    if hit_key(event, K_DOWN):
        pygame.event.set_allowed(MOUSEMOTION)
        gl.MY_KEYDOWN = 1
        gl.HAND_TOOL = 1
    if hit_key(event, K_UP):
        pygame.event.set_allowed(MOUSEMOTION)
        gl.MY_KEYUP = 1
        gl.HAND_TOOL = 1
    if hit_key(event, K_RIGHT):
        pygame.event.set_allowed(MOUSEMOTION)
        gl.MY_KEYRIGHT = 1
        gl.HAND_TOOL = 1
    if hit_key(event, K_LEFT):
        pygame.event.set_allowed(MOUSEMOTION)
        gl.MY_KEYLEFT = 1
        gl.HAND_TOOL = 1
    if hit_key(event, K_HOME):
        pygame.event.set_allowed(MOUSEMOTION)
        command_full_right(rect, last_rect, new_img, file)
        if gl.IMG_BORDER:
            img_border(screen, new_img.get_width(
            ), new_img.get_height(), rect[0], rect[1])
    if hit_key(event, K_END):
        pygame.event.set_allowed(MOUSEMOTION)
        command_full_left(rect, last_rect, new_img, file)
        if gl.IMG_BORDER:
            img_border(screen, new_img.get_width(
            ), new_img.get_height(), rect[0], rect[1])
    if hit_key(event, K_PAGEDOWN):
        pygame.event.set_allowed(MOUSEMOTION)
        command_full_up(rect, last_rect, new_img, file)
        if gl.IMG_BORDER:
            img_border(screen, new_img.get_width(
            ), new_img.get_height(), rect[0], rect[1])
    if hit_key(event, K_PAGEUP):
        pygame.event.set_allowed(MOUSEMOTION)
        command_full_down(rect, last_rect, new_img, file)
        if gl.IMG_BORDER:
            img_border(screen, new_img.get_width(), new_img.get_height(), rect[0], rect[1])
    if hit_key(event, K_m):
        (new_img, img, rect) = command_horiz(new_img, screen, file, rect)
    if hit_key(event, K_v):
        (new_img, img, rect) = command_vert(new_img, screen, file, rect)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_TAB and mods & KMOD_CTRL) or hit_key(event, K_SPACE) or\
                hit_key(event, K_n):
            (new_img, img, refresh_img, file,
             rect) = command_next_img(new_img, screen, file, rect)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (hit_key(event, K_BACKSPACE) or hit_key(event, K_b)) and mods & KMOD_CTRL == 0:
            (new_img, img, refresh_img, file,
             rect) = command_prev_img(new_img, screen, file, rect)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if event.key == K_b and mods & KMOD_CTRL:
            gl.IMG_BORDER ^= 1
            my_update_screen(new_img, rect, file)
            normal_cursor()
    if hit_key(event, K_o):
        (screen, before_winsize, not_accepted) = adjust_screen(screen)
        new_img = open_url(screen, img)
        gl.URL_ERROR = False
        file = 0
        img = refresh_img = new_img
        screen = restore_screen(
            screen, before_winsize, not_accepted, new_img, file, rect)
        rect = get_center(screen, new_img)
        my_update_screen(new_img, rect, file)
        normal_cursor()
    if hit_key(event, K_ESCAPE):
        (new_img, img, rect, file) = command_refresh(refresh_img,
                                                     screen, gl.files, file)
        my_update_screen(new_img, rect, file)
    if event.type == KEYDOWN:  # Ctrl+0 (Fit to Window) code
        mods = pygame.key.get_mods()
        if event.key == K_0 and mods & KMOD_CTRL:
            gl.RESET_FIT = 0
            gl.SCALE_UP = 1
            if gl.FIT_IMAGE_VAL:
                gl.RESET_FIT = 0
            else:
                gl.RESET_FIT = 1
                gl.FIT_IMAGE_VAL = 1
            start = start_timer()
            wait_cursor()
            new_img = load_img(gl.files[file])
            img = refresh_img = new_img
            rect = get_center(screen, new_img)
            ns = check_timer(start)
            my_update_screen(new_img, rect, file, ns)
            if gl.RESET_FIT == 1:
                gl.FIT_IMAGE_VAL = 0
            normal_cursor()
    if event.type == KEYDOWN:  # Alt+0 (Actual Size) code
        mods = pygame.key.get_mods()
        if ((event.key == K_0 and mods & KMOD_ALT)):
            gl.SKIP_FIT = 1
            gl.ZOOM_EXP = 0
            start = start_timer()
            wait_cursor()
            new_img = load_img(gl.files[file])
            img = refresh_img = new_img
            rect = get_center(screen, new_img)
            ns = check_timer(start)
            my_update_screen(new_img, rect, file, ns)
            normal_cursor()
    if hit_key(event, K_1) or hit_key(event, K_KP1):
        #gl.SCALE_UP = 1
        if gl.FIT_IMAGE_VAL:
            gl.FIT_IMAGE_VAL = 0
            gl.RESET_FIT = 1
        else:
            gl.SKIP_FIT = 0
            gl.FIT_IMAGE_VAL = 1
            gl.RESET_FIT = 0
        start = start_timer()
        wait_cursor()
        if new_img.get_width() > screen.get_width() or new_img.get_height() > screen.get_height() or gl.RESET_FIT:
            new_img = load_img(gl.files[file])
            img = refresh_img = new_img
            rect = get_center(screen, new_img)
        if gl.RESET_FIT:
            gl.FIT_IMAGE_VAL = 0
        my_update_screen(new_img, rect, file, check_timer(start))
        normal_cursor()
    if hit_key(event, K_f):
        (new_img, img, refresh_img, file,
         rect) = command_first_img(new_img, screen, file, rect)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_l and mods & KMOD_CTRL == 0):
            (new_img, img, refresh_img, file,
             rect) = command_last_img(new_img, screen, file, rect)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_l and mods & KMOD_CTRL):
            gl.PERSISTENT_ZOOM_VAL ^= 1
            if not gl.PERSISTENT_ZOOM_VAL:
                gl.ZOOM_EXP = 0
            my_update_screen(new_img, rect, file, ns)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_DELETE and mods & KMOD_CTRL == 0) or\
                (event.key == K_KP_PERIOD and mods & KMOD_CTRL == 0) or\
                (event.key == K_w and mods & KMOD_CTRL):
            (new_img, img, refresh_img, file,
             rect) = command_remove_img(new_img, screen, file, rect)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_DELETE and mods & KMOD_CTRL) or\
           (event.key == K_KP_PERIOD and mods & KMOD_CTRL):
            fn = gl.files[file]
            answer = get_confirmation(
                screen, "Delete %s? [y/n]" % basename(fn))
            if answer == "yes":
                (new_img, img, refresh_img, file, rect) = command_delete_img(
                    fn, new_img, screen, file, rect)
            my_update_screen(new_img, rect, file)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_w and mods & KMOD_CTRL == 0) and hit_key(event, K_w):
            (new_img, img, refresh_img, file,
             rect) = my_slideshow(new_img, img, screen, file, rect)
            my_update_screen(new_img, rect, file)
    if hit_key(event, K_e):
        (screen, before_winsize, not_accepted) = adjust_screen(screen)
        gl.USING_SCROLL_MENU = 1
        zoom_percent = gl.CURRENT_ZOOM_PERCENT
        real_width = gl.REAL_WIDTH
        (new_img, img, refresh_img, file,
         rect) = command_edit_menu(screen, file, new_img, rect)
        if gl.ESCAPED:
            gl.CURRENT_ZOOM_PERCENT = zoom_percent
            gl.REAL_WIDTH = real_width
        screen = restore_screen(
            screen, before_winsize, not_accepted, new_img, file, rect)
        my_update_screen(new_img, rect, file)
        gl.ESCAPED = 0
        gl.USING_SCROLL_MENU = 0
    if hit_key(event, K_z):
        transparency = 0
        if not gl.TOGGLE_TRANSPARENT:
            gl.TOGGLE_TRANSPARENT = 1
            transparency = 1
        command_verbose_info(screen, new_img, rect, file)
        if transparency:
            gl.TOGGLE_TRANSPARENT = 0
        my_update_screen(new_img, rect, file)
    if hit_key(event, K_4):
        gl.CALC_ZOOM = 0
        zoom_percent = gl.CURRENT_ZOOM_PERCENT
        real_width = gl.REAL_WIDTH
        (file, new_img, img, refresh_img, rect) = command_four(
            screen, file, new_img, ns)
        if gl.ESCAPED:
            gl.CURRENT_ZOOM_PERCENT = zoom_percent
            gl.REAL_WIDTH = real_width
        gl.ESCAPED = 0
        my_update_screen(new_img, rect, file)
        normal_cursor()
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_t and mods & KMOD_CTRL):
            gl.TOGGLE_TRANSPARENT ^= 1
            my_update_screen(new_img, rect, file)
    if event.type == KEYDOWN:
        mods = pygame.key.get_mods()
        if (event.key == K_t and mods & KMOD_CTRL == 0) and hit_key(event, K_t):
            gl.THUMBING = 1
            gl.CALC_ZOOM = 0
            zoom_percent = gl.CURRENT_ZOOM_PERCENT
            real_width = gl.REAL_WIDTH
            (new_img, img, refresh_img, file,
             rect) = command_thumbs(screen, new_img, file, ns)
            if gl.ESCAPED:
                gl.CURRENT_ZOOM_PERCENT = zoom_percent
                gl.REAL_WIDTH = real_width
            gl.ESCAPED = 0
            gl.THUMBING = 0
            my_update_screen(new_img, rect, file)
    if hit_key(event, K_h):
        pygame.event.set_allowed(MOUSEMOTION)
        gl.HAND_TOOL = 1
        drag_hand_cursor()
    if gl.REMOTE and not gl.ALREADY_DOWNLOADED:
        if hit_key(event, K_a):
            save_remote_img(screen, file)

    return (screen, rect, new_img, img, refresh_img, file, last_rect)
