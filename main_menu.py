# imgv menu code by Ryan Kulla, rkulla@gmail.com
import gl
from os import getcwd, chdir
from cursor import wait_cursor, normal_cursor, hover_cursor, drag_hand_cursor
from list_images import command_img_names
from thumb import command_thumbs
from verbose import command_verbose_info
from refresh import command_refresh
from help import command_help
from playlist import command_play_list_options, command_add_to_play_list
from slideshow import my_slideshow
from open_url import open_url
from hide import command_hide
from rm_img import command_remove_img
from rotate import command_horiz, command_vert, command_rotate_left, command_rotate_right
from randomizer import command_shuffle, command_unshuffle
from res import adjust_screen, restore_screen
from edit import command_edit_menu
from zoom import command_zoom_in, command_zoom_out
from img_screen import my_update_screen, get_center, clean_screen
from four import command_four
from img_surf import command_next_img, command_prev_img, command_first_img, command_last_img
import pygame.event
import pygame.mouse
from pygame.display import update
from pygame.locals import Rect, KEYDOWN, K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB, K_c, K_h, K_DOWN, K_UP, K_RIGHT, K_LEFT, VIDEORESIZE, RESIZABLE, MOUSEMOTION, MOUSEBUTTONDOWN
from usr_event import check_quit, left_click, middle_click, right_click
from dir_nav import command_show_dirs
from handle_keyboard import handle_keyboard
from buttons import imgv_button, hover_button
from downloader import save_remote_img
from load_img import load_img
from load_timers import start_timer, check_timer


def command_main_menu(gfx, ns):
    menu_items = []
    i = 23
    cursor = pygame.mouse.get_pos()
    if gfx['screen'].get_height() < 600:
        font_size = 10
        gl.MENU_DIVIDER_AMOUNT = 12
    else:
        gl.MENU_DIVIDER_AMOUNT = 15
        font_size = 12
    font = pygame.font.Font(gl.FONT_NAME, font_size)
    font.set_bold(1)
    if gl.MENU_POS == -1:
        gl.MENU_POS = cursor[0]
    main_menu_fg(gfx['screen'], font, i, menu_items)
    normal_cursor()
    last_rect = Rect(gfx['rect'])
    new_img_width = gfx['new_img'].get_width()
    new_img_height = gfx['new_img'].get_height()
    if gl.REMOTE and not gl.ALREADY_DOWNLOADED:
        download_rect = imgv_button(
            gfx['screen'], " Downlo(a)d Image ", None, None, "topright")
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1)
        check_quit(event)
        cursor2 = pygame.mouse.get_pos()

        if event.type == VIDEORESIZE:
            gl.JUST_RESIZED = 1
            gfx['screen'] = pygame.display.set_mode(
                event.dict['size'], RESIZABLE)
            rect = get_center(gfx['screen'], gfx['new_img'])
            my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
            return gfx
        if gl.REMOTE and not gl.ALREADY_DOWNLOADED:
            hover_button(download_rect, cursor2, gfx['screen'],
                         " Downlo(a)d Image ", None, None, "topright")

        if event.type == KEYDOWN:
            if event.key in (K_c, K_h, K_UP, K_DOWN, K_RIGHT, K_LEFT):
                if event.key != K_c:
                    pygame.event.set_allowed(MOUSEMOTION)
                    gl.HAND_TOOL = 1
                    drag_hand_cursor()
                # close the menu
                gl.MENU_POS = -1
                my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                if event.key == K_c:
                    normal_cursor()
                return gfx

            (gfx['screen'], gfx['rect'], gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['last_rect']) =\
                handle_keyboard(event, gfx, last_rect, ns)
            break
        hover_cursor(cursor2, [x[0] for x in menu_items])
        if left_click(event):
            if gl.REMOTE and not gl.ALREADY_DOWNLOADED:
                if download_rect.collidepoint(cursor2):
                    wait_cursor()
                    save_remote_img(gfx['screen'], gfx['file'])
                    break
            for it in menu_items:
                if it[0].collidepoint(cursor2):
                    if it[1] == " Next Image ":
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = command_next_img(gfx['new_img'], gfx['screen'], gfx['file'], gfx['rect'])
                    elif it[1] == " Previous Image ":
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = command_prev_img(gfx['new_img'], gfx['screen'], file, rect)
                    elif it[1] == " Directory Browser ":
                        gl.USING_SCROLL_MENU = 1
                        # save current things in case the user ESCAPES out of show_dirs()
                        gl.LAST_DIR = getcwd()
                        last_files = gl.files
                        (last_new_img, last_img, last_refresh_img, last_file, last_rect) =\
                        (gfx['new_img'], gfx[
                         'img'], gfx['refresh_img'], gfx['file'], gfx['rect'])
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = command_show_dirs(gfx['new_img'], gfx['img'], gfx['screen'], gfx['rect'], gfx['file'])
                        # user ESCAPED from show_dirs, reset last values
                        if gl.ESCAPED:
                            (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) =\
                            (last_new_img,
                             last_img, last_refresh_img, last_file, last_rect)
                            chdir(gl.LAST_DIR)
                            gl.files = last_files
                            gl.USING_SCROLL_MENU = 0
                            my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                        else:
                            gl.REFRESH_IMG_COUNT = 0
                        gl.ESCAPED = 0
                        gl.USING_SCROLL_MENU = 0
                    elif it[1] == " Image Browser ":
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = command_img_names(gfx['screen'], gfx['new_img'], gfx['img'], gfx['file'], gfx['rect'])
                    elif it[1] == " Thumbnails ":
                        gl.THUMBING = 1
                        gl.CALC_ZOOM = 0
                        zoom_percent = gl.CURRENT_ZOOM_PERCENT
                        real_width = gl.REAL_WIDTH
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = command_thumbs(gfx['screen'], gfx['new_img'], gfx['file'], ns)
                        if gl.ESCAPED:
                            gl.CURRENT_ZOOM_PERCENT = zoom_percent
                            gl.REAL_WIDTH = real_width
                        gl.ESCAPED = 0
                        gl.THUMBING = 0
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                    elif it[1] == " Image Properties ":
                        transparency = 0
                        if not gl.TOGGLE_TRANSPARENT:
                            gl.TOGGLE_TRANSPARENT = 1
                            transparency = 1
                        command_verbose_info(gfx['screen'], gfx['new_img'],
                                             gfx['rect'], gfx['file'])
                        if transparency:
                            gl.TOGGLE_TRANSPARENT = 0
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                    elif it[1] == " Zoom Out ":
                        if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                            try:
                                (
                                    gfx['new_img'], gfx['img'], gfx['rect']) = command_zoom_out(gfx['new_img'], new_img_width,
                                                                                                new_img_height, gfx['img'], gfx['screen'], gfx['file'], gfx['rect'], "normal")
                            except:
                                print 'Out of memory.'
                        else:
                            print "Can't zoom out. Out of memory. Resetting the image."
                            gl.SKIP_FIT = 1
                            gl.ZOOM_EXP = 0
                            start = start_timer()
                            wait_cursor()
                            gfx['new_img'] = load_img(gl.files[gfx['file']], gfx['screen'])
                            gfx['img'] = gfx['refresh_img'] = gfx['new_img']
                            gfx['rect'] = get_center(
                                gfx['screen'], gfx['new_img'])
                            ns = check_timer(start)
                            my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'], ns)
                            normal_cursor()
                            gl.N_MILLISECONDS = "0"
                    elif it[1] == " Zoom In ":
                        if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                            try:  # triple zoom crash protection
                                (
                                    gfx['new_img'], gfx['img'], gfx['rect']) = command_zoom_in(gfx['new_img'], new_img_width, new_img_height, gfx['img'], gfx['screen'], gl.files,
                                                                                               file, rect, "normal")
                            except:
                                print 'Zoom max reached.'
                        else:
                            print 'Zoom max reached.'
                    elif it[1] == " Fit to Window ":
                        gl.RESET_FIT = 0
                        gl.SCALE_UP = 1
                        if gl.FIT_IMAGE_VAL:
                            gl.RESET_FIT = 0
                        else:
                            gl.RESET_FIT = 1
                            gl.FIT_IMAGE_VAL = 1
                        start = start_timer()
                        wait_cursor()
                        gfx['new_img'] = load_img(gl.files[gfx['file']], gfx['screen'])
                        gfx['img'] = gfx['refresh_img'] = gfx['new_img']
                        gfx['rect'] = get_center(gfx['screen'], gfx['new_img'])
                        ns = check_timer(start)
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'], ns)
                        if gl.RESET_FIT == 1:
                            gl.FIT_IMAGE_VAL = 0
                        normal_cursor()
                    elif it[1] == " Lock Zoom ":
                        gl.PERSISTENT_ZOOM_VAL ^= 1
                        if not gl.PERSISTENT_ZOOM_VAL:
                            gl.ZOOM_EXP = 0
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'], ns)
                    elif it[1] == " Actual Size ":
                        gl.SKIP_FIT = 1
                        gl.ZOOM_EXP = 0
                        start = start_timer()
                        wait_cursor()
                        gfx['new_img'] = load_img(
                            gl.files[gfx['file']], gfx['screen'])
                        gfx['img'] = gfx['refresh_img'] = gfx['new_img']
                        gfx['rect'] = get_center(gfx['screen'], gfx['new_img'])
                        ns = check_timer(start)
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'], ns)
                        normal_cursor()
                    elif it[1] == " Close Image ":
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = command_remove_img(gfx['new_img'], gfx['screen'], gfx['file'], gfx['rect'])
                    elif it[1] == " Rotate Right ":
                        if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                            gl.CALC_ZOOM = 0
                            (gfx['new_img'], gfx['img'], gfx['rect']) = command_rotate_right(gfx['new_img'], gfx['screen'], gfx['file'], gfx['rect'])
                        else:
                            print "Can't rotate. Out of memory."
                    elif it[1] == " Rotate Left ":
                        if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                            gl.CALC_ZOOM = 0
                            (gfx['new_img'], gfx['img'], gfx['rect']) = command_rotate_left(gfx['new_img'], gfx['screen'], gfx['file'], gfx['rect'])
                        else:
                            print "Can't rotate. Out of memory."
                    elif it[1] == " Four at a Time ":
                        gl.CALC_ZOOM = 0
                        zoom_percent = gl.CURRENT_ZOOM_PERCENT
                        real_width = gl.REAL_WIDTH
                        (gfx['file'], gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['rect']) = command_four(gfx['screen'], gfx['file'], gfx['new_img'], ns)
                        if gl.ESCAPED:
                            gl.CURRENT_ZOOM_PERCENT = zoom_percent
                            gl.REAL_WIDTH = real_width
                        gl.ESCAPED = 0
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                        normal_cursor()
                    elif it[1] == " Refresh ":
                        (gfx['new_img'], gfx['img'], gfx['rect'], gfx['file']) = command_refresh(gfx['refresh_img'], gfx['screen'], gl.files, gfx['file'])
                    elif it[1] == " First Image ":
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = command_first_img(gfx['new_img'], gfx['screen'], gfx['file'], gfx['rect'])
                    elif it[1] == " Last Image ":
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = command_last_img(gfx['new_img'], gfx['screen'], gfx['file'], gfx['rect'])
                    elif it[1] == " Shuffle ":
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['rect']) = command_shuffle(gfx['new_img'], gfx['img'], gfx['screen'], gfx['rect'], gfx['file'])
                    elif it[1] == " Unshuffle ":
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['rect'], gfx['file']) = command_unshuffle(gfx['new_img'], gfx['img'], gfx['screen'], gfx['rect'], gfx['file'])
                    elif it[1] == " Flip Horizontal ":
                        (gfx['new_img'], gfx['img'], gfx['rect']) = command_horiz(gfx['new_img'], gfx['screen'], gfx['file'], gfx['rect'])
                    elif it[1] == " Flip Vertical ":
                        (gfx['new_img'], gfx['img'], gfx['rect']) = command_vert(gfx['new_img'], gfx['screen'], gfx['file'], gfx['rect'])
                    elif it[1] == " Slideshow ":
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = my_slideshow(gfx['new_img'], gfx['img'], gfx['screen'], gfx['file'], gfx['rect'])
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                    elif it[1] == " Playlists ":
                        (gfx['new_img'], gfx['new_img'], gfx['new_img'], gfx['file'], gfx['rect']) = command_play_list_options(gfx['screen'], gfx['file'])
                        gl.SORT_HIT = 0
                    elif it[1] == " Add to Playlist ":
                        command_add_to_play_list(gfx['screen'], gl.files[gfx['file']])
                        gl.SORT_HIT = 0
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                    elif it[1] == " Edit ":
                        (gfx['screen'], before_winsize,
                         not_accepted) = adjust_screen(gfx['screen'])
                        gl.USING_SCROLL_MENU = 1
                        (gfx['new_img'], gfx['img'], gfx['refresh_img'], gfx['file'], gfx['rect']) = command_edit_menu(gfx['screen'], gfx['file'], gfx['new_img'], gfx['rect'])
                        gfx['screen'] = restore_screen(gfx['screen'], before_winsize, not_accepted, gfx['new_img'], gfx['file'], gfx['rect'])
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                        gl.USING_SCROLL_MENU = 0
                    elif it[1] == " Hide Image ":
                        command_hide(gfx['screen'],
                                     gfx['new_img'], gfx['rect'], gfx['file'])
                    elif it[1] == " Extract from Web ":
                        (gfx['screen'], before_winsize,
                         not_accepted) = adjust_screen(gfx['screen'])
                        gfx['new_img'] = open_url(gfx['screen'], gfx['img'])
                        gl.URL_ERROR = False
                        gfx['file'] = 0
                        gfx['img'] = gfx['refresh_img'] = gfx['new_img']
                        gfx['screen'] = restore_screen(gfx['screen'], before_winsize, not_accepted, gfx['new_img'], gfx['file'], gfx['rect'])
                        gfx['rect'] = get_center(gfx['screen'], gfx['new_img'])
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                        normal_cursor()
                    elif it[1] == " Help ":
                        gl.CALC_ZOOM = 0
                        zoom_percent = gl.CURRENT_ZOOM_PERCENT
                        real_width = gl.REAL_WIDTH
                        command_help(gfx['screen'],
                                     gfx['new_img'], gfx['file'], gfx['rect'])
                        if gl.ESCAPED:
                            gl.CURRENT_ZOOM_PERCENT = zoom_percent
                            gl.REAL_WIDTH = real_width
                        gl.ESCAPED = 0
                    elif it[1] == " Close Menu " or it[1] == " Hand Tool ":
                        if it[1] == " Hand Tool ":
                            pygame.event.set_allowed(MOUSEMOTION)
                            gl.HAND_TOOL = 1
                            drag_hand_cursor()
                        gl.MENU_POS = -1
                        my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                        normal_cursor()
                        return gfx
                    elif it[1] == " Exit ":
                        clean_screen()
                        raise SystemExit
            break
        if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB):
            return gfx
        if middle_click(event):
            "close the menu upon middle click"
            gl.MENU_POS = -1
            my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
            normal_cursor()
            return gfx
        if right_click(event):
            wait_cursor()
            gl.MENU_POS = -1
            my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
            gfx = command_main_menu(gfx, ns)
            return gfx

        if event.type == MOUSEBUTTONDOWN:  # this needs to be down here to work
            if event.dict['button'] in (4, 5):  # scroll wheel activated
                # allow for mouse dragging:
                pygame.event.set_allowed(MOUSEMOTION)
                gl.HAND_TOOL = 1
                drag_hand_cursor()
                # close menu:
                gl.MENU_POS = -1
                my_update_screen(gfx['new_img'], gfx['rect'], gfx['file'])
                return gfx
    if gl.KEEP_MENU_OPEN == "1":
        # this code purposely closes the main menu by breaking the recursion to free up RAM memory
        gl.COUNT_CLICKS += 1
        if gl.COUNT_CLICKS == 1:  # free up ram every click
            return gfx
        gfx = command_main_menu(gfx, ns)
    normal_cursor()
    return gfx


def main_menu_fg(screen, font, i, menu_items):
    if gl.files == [gl.IMGV_LOGO]:
        gl.MENU_ITEMS = gl.MENU_ITEMS_SHORT
    else:
        gl.MENU_ITEMS = gl.MENU_ITEMS_LONG

    for item in gl.MENU_ITEMS:
        if screen.get_height() < 530 and item == "":  # don't show divider on small screens
            continue
        if gl.TOGGLE_TRANSPARENT and item != "":  # item != "" allows there to be a space-divider in the menu
            ren = font.render(item, 1, gl.MENU_COLOR, gl.FONT_BG)
        else:
            ren = font.render(item, 1, gl.MENU_COLOR)  # transparent
        ren_rect = ren.get_rect()
        ren_rect[0] = gl.MENU_POS
        ren_rect[1] = i
        if len(menu_items) <= gl.MENU_ITEMS:  # so it doesn't keep appending
            menu_items.append((ren_rect, item))
        screen.blit(ren, (gl.MENU_POS, i))
        i = i + gl.MENU_DIVIDER_AMOUNT  # space between each menu item in menu
        update(ren_rect)
