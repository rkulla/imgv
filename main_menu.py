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
from res import command_640x480, command_800x600, command_1024x768, command_1280x1024, command_fullscreen, command_show_res_modes, adjust_screen, restore_screen
from edit import command_edit_menu
from zoom import command_zoom_in, command_zoom_out
from img_screen import my_update_screen, get_center, clean_screen
from four import command_four
from img_surf import command_next_img, command_prev_img, command_first_img, command_last_img
import pygame.event, pygame.mouse
from pygame.display import update
from pygame.locals import Rect, KEYDOWN, K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB, K_c, K_h, KEYUP, KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, VIDEORESIZE, RESIZABLE, MOUSEMOTION, MOUSEBUTTONDOWN
from usr_event import check_quit, left_click, middle_click, right_click
from dir_nav import command_show_dirs
from handle_keyboard import handle_keyboard
from buttons import imgv_button, hover_button
from downloader import save_remote_img
from load_img import load_img
from load_timers import start_timer, check_timer


def command_main_menu(refresh_img, screen, file, num_imgs, rect, new_img, img, new_img_width, new_img_height, ns):
    menu_items = []
    i = 23
    cursor = pygame.mouse.get_pos()
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    if screen_height < 600:
        font_size = 10
        gl.MENU_DIVIDER_AMOUNT = 12
    else:
        gl.MENU_DIVIDER_AMOUNT = 15
        font_size = 12
    font = pygame.font.Font(gl.FONT_NAME, font_size)
    font.set_bold(1)
    if gl.MENU_POS == -1:
        gl.MENU_POS = cursor[0]
    main_menu_fg(screen, font, i, menu_items)
    normal_cursor()
    last_rect = Rect(rect)
    new_img_width = new_img.get_width()
    new_img_height = new_img.get_height()
    if gl.REMOTE and not gl.ALREADY_DOWNLOADED:
        download_rect = imgv_button(screen, " Downlo(a)d Image ", None, None, "topright")
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1)
        check_quit(event)
        cursor2 = pygame.mouse.get_pos()

        if event.type == VIDEORESIZE:#
            gl.JUST_RESIZED = 1
            screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            rect = get_center(screen, new_img)
            my_update_screen(new_img, screen, rect, file, len(gl.files))
            return (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect)
        if gl.REMOTE and not gl.ALREADY_DOWNLOADED:
            hover_button(download_rect, cursor2, screen, " Downlo(a)d Image ", None, None, "topright")

        if event.type == KEYDOWN:
            if event.key in (K_c, K_h, K_UP, K_DOWN, K_RIGHT, K_LEFT):
                if event.key != K_c:
                    pygame.event.set_allowed(MOUSEMOTION)
                    gl.HAND_TOOL = 1
                    drag_hand_cursor()
                # close the menu
                gl.MENU_POS = -1
                my_update_screen(new_img, screen, rect, file, len(gl.files))
                if event.key == K_c:
                    normal_cursor()
                return (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect)
            
            (screen, rect, new_img, img, refresh_img, file, num_imgs,\
            screen_width, screen_height, new_img_width, new_img_height, last_rect) =\
            handle_keyboard(event, screen, rect, new_img, img, refresh_img, file, len(gl.files),\
            screen_width, screen_height, new_img_width, new_img_height, last_rect, ns)
            break
        hover_cursor(cursor2, [x[0] for x in menu_items])
        if left_click(event):
            if gl.REMOTE and not gl.ALREADY_DOWNLOADED:
                if download_rect.collidepoint(cursor2):
                    wait_cursor()
                    save_remote_img(screen, file)
                    break
            for it in menu_items:
                if it[0].collidepoint(cursor2):
                    if it[1] == " Next Image ": 
                        (new_img, img, refresh_img, file, rect) = command_next_img(new_img, screen, file, len(gl.files), rect)
                    elif it[1] == " Previous Image ":
                        (new_img, img, refresh_img, file, rect) = command_prev_img(new_img, screen, file, len(gl.files), rect)        
                    elif it[1] == " Directory Browser ":
                        gl.USING_SCROLL_MENU = 1
                        # save current things in case the user ESCAPES out of show_dirs()
                        gl.LAST_DIR = getcwd()
                        last_files = gl.files
                        (last_new_img, last_img, last_refresh_img, last_num_imgs, last_file, last_rect) =\
                        (new_img, img, refresh_img, num_imgs, file, rect)
                        (new_img, img, refresh_img, num_imgs, file, rect) = command_show_dirs(new_img, img, screen, rect,\
                        file, num_imgs)
                        # user ESCAPED from show_dirs, reset last values
                        if gl.ESCAPED:
                            (new_img, img, refresh_img, num_imgs, file, rect) =\
                            (last_new_img, last_img, last_refresh_img, last_num_imgs, last_file, last_rect)
                            chdir(gl.LAST_DIR)
                            gl.files = last_files
                            gl.USING_SCROLL_MENU = 0
                            my_update_screen(new_img, screen, rect, file, num_imgs)
                        else:
                            gl.REFRESH_IMG_COUNT = 0
                        gl.ESCAPED = 0
                        gl.USING_SCROLL_MENU = 0
                    elif it[1] == " Image Browser ":
                        (new_img, img, refresh_img, file, rect) = command_img_names(screen, new_img, img, file,\
                        num_imgs, rect)
                    elif it[1] == " Thumbnails ":
                        gl.THUMBING = 1
                        gl.CALC_ZOOM = 0
                        zoom_percent = gl.CURRENT_ZOOM_PERCENT
                        real_width = gl.REAL_WIDTH
                        (new_img, img, refresh_img, file, rect) = command_thumbs(screen, new_img, file, ns)
                        if gl.ESCAPED:
                            gl.CURRENT_ZOOM_PERCENT = zoom_percent
                            gl.REAL_WIDTH = real_width
                        gl.ESCAPED = 0
                        gl.THUMBING = 0
                        my_update_screen(new_img, screen, rect, file, num_imgs)
                    elif it[1] == " Image Properties ":
                        transparency = 0
                        if not gl.TOGGLE_TRANSPARENT:
                            gl.TOGGLE_TRANSPARENT = 1
                            transparency = 1
                        command_verbose_info(screen, new_img, rect, file, num_imgs)
                        if transparency:
                            gl.TOGGLE_TRANSPARENT = 0
                        my_update_screen(new_img, screen, rect, file, num_imgs)
                    elif it[1] == " Zoom Out ":
                        if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT< gl.ZOOM_PERCENT_MAX:
                            try:
                                (new_img, img, rect) = command_zoom_out(new_img, new_img_width, new_img_height, img, screen, file, num_imgs, rect, "normal")
                            except:
                                print 'Out of memory.'
                        else:
                            print "Can't zoom out. Out of memory. Resetting the image."
                            gl.SKIP_FIT = 1
                            gl.ZOOM_EXP = 0
                            start = start_timer()
                            wait_cursor()
                            new_img = load_img(gl.files[file], screen)
                            img = refresh_img = new_img
                            rect = get_center(screen, new_img)
                            ns = check_timer(start)
                            my_update_screen(new_img, screen, rect, file, num_imgs, ns)
                            normal_cursor()
                            gl.N_MILLISECONDS = "0" 
                    elif it[1] == " Zoom In ":
                        if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                            try: # triple zoom crash protection
                                (new_img, img, rect) = command_zoom_in(new_img, new_img_width, new_img_height, img, screen, gl.files, file, num_imgs, rect, "normal")
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
                        new_img = load_img(gl.files[file], screen)
                        img = refresh_img = new_img
                        rect = get_center(screen, new_img)
                        ns = check_timer(start)
                        my_update_screen(new_img, screen, rect, file, num_imgs, ns)
                        if gl.RESET_FIT == 1:
                            gl.FIT_IMAGE_VAL = 0
                        normal_cursor()
                    elif it[1] == " Lock Zoom ":
                        gl.PERSISTENT_ZOOM_VAL ^= 1
                        if not gl.PERSISTENT_ZOOM_VAL:
                            gl.ZOOM_EXP = 0
                        my_update_screen(new_img, screen, rect, file, num_imgs, ns)
                    elif it[1] == " Actual Size ":
                        gl.SKIP_FIT = 1
                        gl.ZOOM_EXP = 0
                        start = start_timer()
                        wait_cursor()
                        new_img = load_img(gl.files[file], screen)
                        img = refresh_img = new_img
                        rect = get_center(screen, new_img)
                        ns = check_timer(start)
                        my_update_screen(new_img, screen, rect, file, num_imgs, ns)
                        normal_cursor()
                    elif it[1] == " Close Image ":
                        (new_img, img, refresh_img, file, num_imgs, rect) = command_remove_img(new_img, screen, file, rect)
                    elif it[1] == " Rotate Right ":
                        if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                            gl.CALC_ZOOM = 0
                            (new_img, img, rect) = command_rotate_right(new_img, screen, file, num_imgs, rect)
                        else:
                            print "Can't rotate. Out of memory."
                    elif it[1] == " Rotate Left ":
                        if int(gl.N_MILLISECONDS) < gl.MAX_ZOOM_MAX_MS and gl.CURRENT_ZOOM_PERCENT < gl.ZOOM_PERCENT_MAX:
                            gl.CALC_ZOOM = 0
                            (new_img, img, rect) = command_rotate_left(new_img, screen, file, num_imgs, rect)
                        else:
                            print "Can't rotate. Out of memory."
                    elif it[1] == " Four at a Time ":
                        gl.CALC_ZOOM = 0
                        zoom_percent = gl.CURRENT_ZOOM_PERCENT
                        real_width = gl.REAL_WIDTH
                        (file, new_img, img, refresh_img, rect) = command_four(screen, file, new_img, ns)
                        if gl.ESCAPED:
                            gl.CURRENT_ZOOM_PERCENT = zoom_percent
                            gl.REAL_WIDTH = real_width
                        gl.ESCAPED = 0
                        my_update_screen(new_img, screen, rect, file, num_imgs)
                        normal_cursor()
 #                   elif it[1] == " Resize Options ":##
 #                       gl.USING_SCROLL_MENU = 1
 #                       gl.CALC_ZOOM = 0
 #                       zoom_percent = gl.CURRENT_ZOOM_PERCENT
 #                       real_width = gl.REAL_WIDTH
 #                       rect = command_show_res_modes(screen, new_img, file, num_imgs, rect)
 #                       gl.CURRENT_ZOOM_PERCENT = zoom_percent
 #                       gl.REAL_WIDTH = real_width
 #                       gl.USING_SCROLL_MENU = 0
                    elif it[1] == " Refresh ":
                        (new_img, img, rect, file) = command_refresh(refresh_img, screen, gl.files, file, num_imgs)
                    elif it[1] == " First Image ":
                        (new_img, img, refresh_img, file, rect) = command_first_img(new_img, screen, file, len(gl.files), rect)
                    elif it[1] == " Last Image ":
                        (new_img, img, refresh_img, file, rect) = command_last_img(new_img, screen, file, len(gl.files), rect)
                    elif it[1] == " Shuffle ":
                        (new_img, img, refresh_img, rect) = command_shuffle(new_img, img, screen, rect, file, num_imgs)
                    elif it[1] == " Unshuffle ":
                        (new_img, img, refresh_img, rect, file) = command_unshuffle(new_img, img, screen, rect, file, num_imgs)
                    elif it[1] == " Flip Horizontal ":
                        (new_img, img, rect) = command_horiz(new_img, screen, file, num_imgs, rect)
                    elif it[1] == " Flip Vertical ":
                        (new_img, img, rect) = command_vert(new_img, screen, file, num_imgs, rect)
                    elif it[1] == " Slideshow ":
                        (new_img, img, refresh_img, file, rect) = my_slideshow(new_img, img, screen, file, num_imgs, rect)
                        my_update_screen(new_img, screen, rect, file, len(gl.files))
                    elif it[1] == " Playlists ":
                        (new_img, new_img, new_img, file, rect, num_imgs) = command_play_list_options(screen, file)
                        gl.SORT_HIT = 0
                    elif it[1] == " Add to Playlist ":
                        command_add_to_play_list(screen, gl.files[file])
                        gl.SORT_HIT = 0
                        my_update_screen(new_img, screen, rect, file, len(gl.files))
                    elif it[1] == " Edit ":
                        (screen, before_winsize, not_accepted) = adjust_screen(screen)
                        gl.USING_SCROLL_MENU = 1
                        (new_img, img, refresh_img, file, num_imgs, rect) = command_edit_menu(screen, file, new_img, num_imgs, rect)
                        screen = restore_screen(screen, before_winsize, not_accepted, new_img, file, num_imgs, rect)
                        my_update_screen(new_img, screen, rect, file, num_imgs)
                        gl.USING_SCROLL_MENU = 0
                    elif it[1] == " Hide Image ":
                        command_hide(screen, new_img, rect, file, num_imgs)
                    elif it[1] == " Extract from Web ":
                        (screen, before_winsize, not_accepted) = adjust_screen(screen)
                        (new_img, num_imgs) = open_url(screen, img)
                        gl.URL_ERROR = False
                        file = 0
                        img = refresh_img = new_img
                        screen = restore_screen(screen, before_winsize, not_accepted, new_img, file, num_imgs, rect)
                        rect = get_center(screen, new_img)
                        my_update_screen(new_img, screen, rect, file, len(gl.files))
                        normal_cursor()
                    elif it[1] == " Help ":
                        gl.CALC_ZOOM = 0
                        zoom_percent = gl.CURRENT_ZOOM_PERCENT
                        real_width = gl.REAL_WIDTH
                        command_help(screen, new_img, file, rect, num_imgs)
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
                        my_update_screen(new_img, screen, rect, file, len(gl.files))
                        normal_cursor()
                        return (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect)
                    elif it[1] == " Exit ":
                        clean_screen()
                        raise SystemExit
            break
        if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB):
            return (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect)
        if middle_click(event):
            "close the menu upon middle click"
            gl.MENU_POS = -1
            my_update_screen(new_img, screen, rect, file, len(gl.files))
            normal_cursor()
            return (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect)
        if right_click(event):
            wait_cursor()
            gl.MENU_POS = -1
            my_update_screen(new_img, screen, rect, file, len(gl.files))
            (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect) =\
            command_main_menu(refresh_img, screen, file, num_imgs, rect, new_img, img, new_img_width, new_img_height, ns)
            return (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect)

        if event.type == MOUSEBUTTONDOWN: # this needs to be down here to work
            if event.dict['button'] in (4, 5): # scroll wheel activated
                # allow for mouse dragging:
                pygame.event.set_allowed(MOUSEMOTION) 
                gl.HAND_TOOL = 1
                drag_hand_cursor()
                # close menu:
                gl.MENU_POS = -1 
                my_update_screen(new_img, screen, rect, file, len(gl.files))
                return (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect)
 

    if gl.KEEP_MENU_OPEN == "1":
        # this code purposely closes the main menu by breaking the recursion to free up RAM memory
        gl.COUNT_CLICKS += 1
        if gl.COUNT_CLICKS == 1: # free up ram every click
            return (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect)
        (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect) =\
        command_main_menu(refresh_img, screen, file, num_imgs, rect, new_img, img, new_img_width, new_img_height, ns)
    normal_cursor()
    return (refresh_img, screen, file, num_imgs, new_img, img, new_img_width, new_img_height, rect)


def main_menu_fg(screen, font, i, menu_items):
    if gl.files == [gl.IMGV_LOGO]:
        gl.MENU_ITEMS = gl.MENU_ITEMS_SHORT
    else:
        gl.MENU_ITEMS = gl.MENU_ITEMS_LONG
    
    for item in gl.MENU_ITEMS:
        if screen.get_height() < 530 and item == "": # don't show divider on small screens
            continue
        if gl.TOGGLE_TRANSPARENT and item != "": # item != "" allows there to be a space-divider in the menu
            ren = font.render(item, 1, gl.MENU_COLOR, gl.FONT_BG)
        else:
            ren = font.render(item, 1, gl.MENU_COLOR) # transparent
        ren_rect = ren.get_rect()
        ren_rect[0] = gl.MENU_POS
        ren_rect[1] = i
        if len(menu_items) <= gl.MENU_ITEMS: # so it doesn't keep appending
            menu_items.append((ren_rect, item))
        screen.blit(ren, (gl.MENU_POS, i))
        i = i + gl.MENU_DIVIDER_AMOUNT # space between each menu item in menu
        update(ren_rect)
