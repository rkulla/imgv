# imgv directory navigation code by Ryan Kulla, rkulla@gmail.com
from __future__ import generators
import gl
import os
from string import digits
from sys import platform
from load_timers import start_timer, check_timer
from load_img import load_img
from show_message import show_message, truncate_name
from buttons import imgv_button, hover_button, close_button
from input_box import ask
from img_screen import get_center, my_update_screen, paint_screen
from playlist import command_add_to_play_list
from cursor import wait_cursor, normal_cursor, hover_cursor
from error_screen import error_screen
from usr_event import left_click, right_click, hit_key, check_quit
from filter_files import command_get_filter_info, filter_files
from res import  adjust_screen, restore_screen
import pygame.font, pygame.event, pygame.mouse
from pygame.display import update, set_caption, get_caption
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEMOTION, K_RETURN, K_SPACE, K_ESCAPE, K_RCTRL, K_LCTRL, K_LALT, K_RALT, K_TAB, K_s, K_a, K_d, K_c, K_v, K_l, K_h, K_t, K_SLASH, K_KP_ENTER, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP0, K_BACKSPACE, K_DELETE, K_KP_PERIOD


def dirwalk(dir, show_subdirs):
    "walk a directory tree, using a generator"
    try:
        for f in os.listdir(dir):
            fullpath = os.path.join(dir, f)
            if os.path.isdir(fullpath) and not os.path.islink(fullpath):
                if show_subdirs:
                    for x in dirwalk(fullpath, show_subdirs): # recurse into subdir
                        yield x
            else:
                yield fullpath
    except:
        print "Directory error1: [%s] Permission denied?" % dir


def get_imgs(start_dir, show_subdirs):
    "return a list of image files from a giving directory"
    gl.files = []
    for i in dirwalk(start_dir, show_subdirs):
        for ext in gl.IMG_TYPES:
            if i.endswith(ext):
                gl.files.append(i)
    return gl.files 


def command_show_dirs(new_img, img, screen, rect, file, num_imgs):
    (screen, before_winsize, not_accepted) = adjust_screen(screen)
    set_caption("Directory Browser - imgv")
    paint_screen(screen, gl.BLACK)
    (num_imgs, file) = show_dirs(screen, num_imgs, file)
    wait_cursor()
    if gl.ESCAPED != 1:
        start = start_timer()
        if num_imgs < 1 or len(gl.files) == 0:
            gl.files = [gl.IMGV_LOGO]
            num_imgs = 0
            new_img = img = load_img(gl.files[file], screen)
        else:
            new_img = load_img(gl.files[file], screen)
    screen = restore_screen(screen, before_winsize, not_accepted, new_img, file, num_imgs, rect)
    rect = get_center(screen, new_img)
    if gl.ESCAPED != 1:
        ns = check_timer(start)
        my_update_screen(new_img, screen, rect, file, num_imgs, ns)
    else:
        my_update_screen(new_img, screen, rect, file, num_imgs)
    normal_cursor()
    return (new_img, new_img, new_img, num_imgs, file, rect)


def show_dirs(screen, num_imgs, file):
    wait_cursor()
    if platform == 'win32':
        try:
            os.chdir(gl.DRIVE + ":")
        except:
            pass # Probably an OSError from not having a cd in the drive
    slash, get_curdir = os.sep, os.getcwd()
    fg_color = gl.SILVER
    font_size = 10
    font = pygame.font.Font(gl.FONT_NAME, font_size)
    font.set_bold(1) # very important
    line = 55
    name_max = 16 # dir name max
    menu_items = []
    if get_curdir[-1] == slash:
        curdir = get_curdir 
    else:
        curdir = get_curdir + slash
    paint_screen(screen, gl.BLACK)
    screen_height = screen.get_height()

    if not gl.BEEN_THERE_DONE_THAT:
        show_message(screen, "You can type in a directory number or shortcut (L/T/A/D/C/V/S/Q) instead of clicking: _", "bottom", 11)
    else:
        show_message(screen, "Directory number or shortcut: _", "bottom", 11)

    curdir_msg = check_truncate(screen.get_width(), curdir)
    all_files = os.listdir('.')
    all_files.sort(lambda a, b: cmp(a.lower(), b.lower())) # case-insensitive sorting
    n_dirs = len([d for d in all_files if os.path.isdir(d)])
    all_files = [f for f in all_files if not os.path.isdir(f)]
    n_files = len(all_files)
    all_images = get_imgs(os.getcwd(), 0)
    n_images = len(all_images)
    get_movies = lambda x, y: [i.upper().endswith(y) for i in all_images].count(True)
    n_movies = get_movies(all_images, ".MPG") + get_movies(all_images, ".MPEG")
    dirs_text = "Directories"
    files_text = "Files"
    images_text = "Images"
    movies_text = "MPEGs"
    if n_dirs == 1: dirs_text = "Directory" # unplural
    if n_files == 1: files_text = "File"
    if n_images == 1: images_text = "Image"
    if n_movies == 1: movies_text = "MPEG"
    files_msg = "[%d %s. %d %s. %d %s. %d %s]" % (n_dirs, dirs_text, n_files, files_text, n_images - n_movies, images_text, n_movies, movies_text)
    curdir_msg_wpos = (screen.get_width() / 2 - font.size(curdir_msg)[0] / 2) - font.size(files_msg)[0] / 2 + 10
    files_msg_wpos = screen.get_width() / 2 + font.size(curdir_msg)[0] / 2 - font.size(files_msg)[0] / 2 + 20

    if not gl.REFRESH_IMG_COUNT and gl.CACHE_DIR_OK:
        dirs = gl.CACHE_DIRS
        gl.REFRESH_IMG_COUNT = 1
        set_caption(curdir)
        show_message(screen, curdir_msg, (curdir_msg_wpos, 4), 10, ("bold"))
        show_message(screen, files_msg, (files_msg_wpos, 4), 10)
    else:
        show_message(screen, curdir_msg, (curdir_msg_wpos, 4), 10, ("bold"))
        show_message(screen, files_msg, (files_msg_wpos, 4), 10)
        set_caption(curdir)
        dirs = os.listdir(curdir)
        #dirs.sort()
        dirs.sort(lambda a, b: cmp(a.lower(), b.lower())) # case-insensitive sorting
        dirs = strip_dirs(dirs)
        # ensure the root dir and last dir items go at top
        dirs.insert(0, "..")
        dirs.insert(0, slash)
        gl.CACHE_DIRS = dirs
    ren_load_rect = imgv_button(screen, " (L)oad ", 0, 18, "topleft")
    ren_load_subdirs_rect = imgv_button(screen, " Subdirs (T)oo ", 62, 18, "topleft")
    if platform == 'win32':
        ren_drive_rect = imgv_button(screen, " Change (D)rive ", 271, 18, "topleft")
    dirpl_rect = imgv_button(screen, " (A)dd To Playlist ", 160, 18, "topleft")
    untag_all_rect = imgv_button(screen, " (C)lear Tags ", 380, 18, "topleft")
    view_tagged_rect = imgv_button(screen, " (V)iew Tags ", 472, 18, "topleft")
    filter_rect = imgv_button(screen, " (S)earch ", 559, 18, "topleft")
    col = 10
    show_message(screen, "Right-Click directories to tag multiple directories to load. Ctrl+Left-Click to untag.", (10, 40), 10)
    if gl.MULT_DIRS != []:
        show_message(screen, "[Dirs tagged: %s]" % len(gl.MULT_DIRS), (440, 40), 10, "bold")

    if gl.FILTER_COMMAND != {}:
        show_message(screen, "[Filter: on]", (560, 40), 10, "bold")

    # add numbers to directory names
    if gl.ADDED_DIR_NUMS == 0 and dirs[0] != '*':
        gl.ADDED_DIR_NUMS = 1
        for i, d in enumerate(dirs):
            dirs[i] = '*' + str(i) + gl.DIRNUMSEP + d
    for d in dirs:
        d = d[1:] # strip out the '*' marker
        if d[3:] == slash:
            if gl.DIRNUM_COLORS:
                dmsg = d
            else:
                ren = font.render(d, 1, gl.MSG_COLOR)
        else:
            if len(d) > name_max:
                if gl.DIRNUM_COLORS:
                    dmsg = truncate_name(d, name_max)
                else:
                    ren = font.render(truncate_name(d, name_max), 1, gl.MSG_COLOR)
            else:
                if gl.DIRNUM_COLORS:
                    dmsg = d + slash
                else:
                    ren = font.render(d + slash, 1, gl.MSG_COLOR)
            
        # print directory names on screen, wrapping if necessary
        font_height = font.size(' '.join(d.split(' ')[1:]))[1]
        if (line + font_height) >= (screen_height - 10):
            line = 55 # reset to beginning of screen
            col = col + (name_max + 130) # go to next column

        if gl.DIRNUM_COLORS:
            before_color = gl.MSG_COLOR
            if gl.MSG_COLOR == gl.SILVER:
                gl.MSG_COLOR = (142, 142, 142)
            else:
                gl.MSG_COLOR = gl.SILVER
            if before_color == gl.WHITE:
                ren_rect = show_message(screen, dmsg, (col, line), font_size, ("bold"), (len(dmsg[:dmsg.index(gl.DIRNUMSEP) + 1]), gl.SILVER))
            else:
                ren_rect = show_message(screen, dmsg, (col, line), font_size, ("bold"), (len(dmsg[:dmsg.index(gl.DIRNUMSEP) + 1]), before_color))
        else:
            ren_rect = ren.get_rect()
            ren_rect[0] = col
            ren_rect[1] = line
            screen.blit(ren, ren_rect)
            update(ren_rect)
        line = line + 12
        menu_items.append((ren_rect, d))
        if gl.DIRNUM_COLORS:
            gl.MSG_COLOR = before_color

    normal_cursor()
    pygame.event.set_blocked(MOUSEMOTION)
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1)
        cursor = pygame.mouse.get_pos()
        (esc_rect, close_font) = close_button(screen)
        hover_fx(screen, curdir, menu_items, cursor)
        if platform == 'win32':#
            hover_cursor(cursor, [ren_load_rect, ren_load_subdirs_rect, ren_drive_rect, dirpl_rect, untag_all_rect, view_tagged_rect, filter_rect, esc_rect] + [x[0] for x in menu_items])
        hover_button(ren_load_rect, cursor, screen, " (L)oad ", 0, 18, "topleft")
        hover_button(ren_load_subdirs_rect, cursor, screen, " Subdirs (T)oo ", 62, 18, "topleft")
        if platform == 'win32':
            hover_button(ren_drive_rect, cursor, screen, " Change (D)rive ", 271, 18, "topleft")
        hover_button(dirpl_rect, cursor, screen, " (A)dd To Playlist ", 160, 18, "topleft")
        hover_button(untag_all_rect, cursor, screen, " (C)lear Tags ", 380, 18, "topleft")
        hover_button(view_tagged_rect, cursor, screen, " (V)iew Tags ", 472, 18, "topleft")
        hover_button(filter_rect, cursor, screen, " (S)earch ", 559, 18, "topleft")
        if left_click(event):
            for item in menu_items:
                if item[0].collidepoint(cursor):
                    if pygame.mouse.get_pressed()[0] and (pygame.key.get_pressed()[K_LCTRL] or\
                       pygame.key.get_pressed()[K_RCTRL]): 
                        try: # untag directory
                            gl.MULT_DIRS.remove(os.getcwd() + slash + ' '.join(item[1].split(' ')[1:]))
                            show_message(screen, " " * 30, (440, 40), 10, ("bold"))
                            show_message(screen, "[Dirs tagged: %s]" % len(gl.MULT_DIRS), (440, 40), 10, "bold")
                        except:
                            pass
                    else: # (normal mode) change to a single directory and load its images
                        (num_imgs, file) = do_change_dir(screen, num_imgs, file, item[1])
                        return (num_imgs, file)
        if right_click(event):
            for item in menu_items:
                if item[0].collidepoint(cursor):
                    # tag directory
                    if os.getcwd()[-1] != slash:
                        gl.MULT_DIRS.append(os.getcwd() + slash + ' '.join(item[1].split(' ')[1:]))
                    else:
                        gl.MULT_DIRS.append(os.getcwd() + ' '.join(item[1].split(' ')[1:]))
                    show_message(screen, " " * 30, (440, 40), 10, ("bold"))
                    show_message(screen, "[Dirs tagged: %s]" % len(gl.MULT_DIRS), (440, 40), 10, "bold")
                    
        # allow number keys to be used to change directories
        dirnum = None
        if event.type == KEYDOWN and event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP0):
            dirnum = get_dirnum(screen, event.key)
            if dirnum != 'backspaced':
                for item in menu_items:
                    if item[1].startswith(str(dirnum)):
                        (num_imgs, file) = do_change_dir(screen, num_imgs, file, item[1])
                        return (num_imgs, file)
                break

        if hit_key(event, K_RETURN) or hit_key(event, K_SPACE) or hit_key(event, K_l):
            (num_imgs, file) = do_load_dir()
            break
        if hit_key(event, K_t): # load subdirs on keypress 't'
            (num_imgs, file) = do_subdirs_too()
            break
        if hit_key(event, K_s): # search
           command_get_filter_info(screen)
           (num_imgs, file) = show_dirs(screen, num_imgs, file)
           break
        if hit_key(event, K_d): # change drives
           if platform == 'win32':
               gl.WAS_IN_CHANGE_DRIVES = 1
               (num_imgs, file) = do_change_drive(screen, num_imgs, file)
               gl.WAS_IN_CHANGE_DRIVES = 0
               break
        if hit_key(event, K_c): # clear tag list
            do_untag(screen)
        if hit_key(event, K_v): # view tagged dirs
           do_view_tagged(screen, num_imgs, file)
           break # break main loop to display properly
        if hit_key(event, K_a): # add curdir to playlist
           command_add_to_play_list(screen, curdir)
           return (num_imgs, file) 
        if hit_key(event, K_ESCAPE):
            gl.ESCAPED = 1
            gl.ADDED_DIR_NUMS = 0
            break
        if left_click(event):
            if esc_rect.collidepoint(cursor):
                gl.ESCAPED = 1
                gl.ADDED_DIR_NUMS = 0
                break
            if ren_load_rect.collidepoint(cursor): # load current dir
                (num_imgs, file) = do_load_dir()
                break
            if ren_load_subdirs_rect.collidepoint(cursor): # load subdirs too
                (num_imgs, file) = do_subdirs_too()
                break
            if platform == 'win32':
                if ren_drive_rect.collidepoint(cursor):
                    gl.WAS_IN_CHANGE_DRIVES = 1
                    (num_imgs, file) = do_change_drive(screen, num_imgs, file)
                    gl.WAS_IN_CHANGE_DRIVES = 0
                    break
            if dirpl_rect.collidepoint(cursor):
                command_add_to_play_list(screen, curdir)
                return (num_imgs, file)
            if untag_all_rect.collidepoint(cursor):
                do_untag(screen)
            if view_tagged_rect.collidepoint(cursor): 
                do_view_tagged(screen, num_imgs, file)
                break # break main loop to display properly
            if filter_rect.collidepoint(cursor):
                command_get_filter_info(screen)
                (num_imgs, file) = show_dirs(screen, num_imgs, file)
                break
        check_quit(event)
    gl.CACHE_DIR_OK = 1 
    return (num_imgs, file)


def adjust_files(show_subdirs):
    if gl.MULT_DIRS != []: # load all tagged directories
        gl.files = []
        for d in gl.MULT_DIRS:
            gl.files = gl.files + get_imgs(d, show_subdirs)
    else: # load only a single directory
        gl.files = get_imgs(os.getcwd(), show_subdirs)
    if gl.FILTER_COMMAND != {}:
        gl.files = filter_files(gl.files)
    file = 0
    return file


def strip_dirs(dirs):
    l = []
    for dir in dirs:
        if os.path.isdir(dir):
            l.append(dir)
    return l


def get_dirnum(screen, key_type):
    BACKSPACED = 0
    keyz = {K_1:1, K_2:2, K_3:3, K_4:4, K_5:5, K_6:6, K_7:7, K_8:8, K_9:9, K_0:0, K_KP1:1, K_KP2:2, K_KP3:3, K_KP4:4,\
            K_KP5:5, K_KP6:6, K_KP7:7, K_KP8:8, K_KP9:9, K_KP0:0}
    dirnum = ['0']
    dirnum.append(str(keyz[key_type]))
    show_message(screen, " " * screen.get_width(), (0, screen.get_height() - 15), 11, ("bold"))
    if not gl.BEEN_THERE_DONE_THAT:
        msg1 = "You can type in a directory number or shortcut (L/T/A/D/C/V/S/Q) instead of clicking: _"
        msg2 = "You can type in a directory number or shortcut (L/T/A/D/C/V/S/Q) instead of clicking: %s" % dirnum[1]
    else:
        msg1 = "Directory number or shortcut: _"
        msg2 = "Directory number or shortcut: %s" % dirnum[1] # start with num showing
    show_message(screen, msg2, "bottom", 11)
    my_digits = [] # keypad number list.

    for num in range(10):
        my_digits.append('[%d]' % num) # [0],[1],..[9]
        
    # pass control to input gathering
    while 1:
        event = pygame.event.wait()
        check_quit(event)
        if event.type == KEYDOWN:
            dirnum_input = pygame.key.name(event.key)
            try:
                if dirnum_input in my_digits or dirnum_input in digits:
                    # only echo digits (0-9)
                    for i in dirnum_input:
                        # extract n from brackets, [n]
                        if i in digits:
                            dirnum_input = i
                    dirnum.append(dirnum_input)
                    if BACKSPACED:
                        show_message(screen, msg2 + ''.join(dirnum[1:]), "bottom", 11)
                    else:
                        show_message(screen, msg2 + ''.join(dirnum[2:]), "bottom", 11)
            except TypeError:
                pass
    
        if hit_key(event, K_RETURN) or hit_key(event, K_KP_ENTER) or hit_key(event, K_SPACE) or hit_key(event, K_l):
            break
        if hit_key(event, K_ESCAPE):
            return
        if hit_key(event, K_BACKSPACE) or hit_key(event, K_DELETE) or hit_key(event, K_KP_PERIOD):
            # erase whatever text was inputed"
            BACKSPACED = 1
            dirnum = ['0']
            msg2 = msg1
            show_message(screen, " " * screen.get_width(), (0, screen.get_height() - 15), 11)
            show_message(screen, msg1, "bottom", 11)
            return 'backspaced' # get control back so you can click directories

    dirnum = int(''.join(dirnum)) # convert to valid number
    return dirnum


def do_view_tagged(screen, num_imgs, file):
    "show all tagged dir names"
    paint_screen(screen, gl.BLACK)
    (esc_rect, close_font) = close_button(screen)
    line = 5
    if len(gl.MULT_DIRS) == 0:
        show_message(screen, "[No directories are currently tagged]", "bottom", 12)
    for d in gl.MULT_DIRS:
        font = pygame.font.Font(gl.FONT_NAME, 9)
        ren = font.render(d, 1, (255, 255, 255), (0, 0, 0))
        ren_rect = ren.get_rect()
        ren_rect[0] = 5
        ren_rect[1] = line
        screen.blit(ren, ren_rect)
        line = line + 12
        update(ren_rect)
    pygame.event.set_allowed(MOUSEMOTION)
    while 1:
        ev = pygame.event.wait()
        check_quit(ev)
        hover_cursor(pygame.mouse.get_pos(), (esc_rect,))
        if ev.type == KEYDOWN and ev.key not in (K_LALT, K_RALT, K_TAB, K_LCTRL, K_RCTRL) or ev.type == MOUSEBUTTONDOWN:
            gl.ADDED_DIR_NUMS = 0
            (num_imgs, file) = show_dirs(screen, num_imgs, file)
            break # break event loop


def do_load_dir():
    "load the current directory"
    gl.SUBDIRS = 0
    wait_cursor()
    file = adjust_files(0)
    num_imgs = len(gl.files)
    gl.PLAY_LIST_NAME = " "
    return (num_imgs, file)


def do_subdirs_too():
    gl.SUBDIRS = 1
    wait_cursor()
    file = adjust_files(1)
    num_imgs = len(gl.files)
    gl.PLAY_LIST_NAME = " "
    return (num_imgs, file)


def do_change_drive(screen, num_imgs, file):
    paint_screen(screen, gl.BLACK)
    my_string = ask(screen, "Enter a Drive Letter")
    if my_string != None:
        gl.ADDED_DIR_NUMS = 0
        gl.DRIVE = my_string[0]
    (num_imgs, file) = show_dirs(screen, num_imgs, file)
    return (num_imgs, file)


def do_untag(screen):
    gl.MULT_DIRS = []
    show_message(screen, " " * 30, (440, 40), 10, ("bold"))
    show_message(screen, "[Dirs tagged: %s]" % len(gl.MULT_DIRS), (440, 40), 10, "bold")


def do_change_dir(screen, num_imgs, file, dirname):
    wait_cursor()
    try:
        change_to = ' '.join(dirname.split(' ')[1:])
        if change_to != os.getcwd(): # don't add numbers more than once
            gl.ADDED_DIR_NUMS = 0
        os.chdir(change_to)
        gl.BEEN_THERE_DONE_THAT = 1
                            
        # adjust the variables for the new dir
        file = adjust_files(0)
        
        show_dirs(screen, num_imgs, file)
        
        # get new num_imgs value here for recursion reasons
        num_imgs = len(gl.files)
        
        normal_cursor()
        return (num_imgs, file)
    except:
        gl.ADDED_DIR_NUMS = 0
        normal_cursor()
        error_screen(screen, "Directory error2. [%s] Permission denied?" % change_to)
        return (num_imgs, file)


def check_truncate(screen_width, name):
    if screen_width >= 640 and screen_width < 800:
        name = truncate_name(name, 43)
    if screen_width >= 800 and screen_width < 1024:
        name = truncate_name(name, 68)
    if screen_width >= 1024 and screen_width < 1280:
        name = truncate_name(name, 103)
    if screen_width >= 1280:
        name = truncate_name(name, 133)
    return name


def hover_fx(screen, curdir, x, cursor):
    slash = os.sep
    dash = ' - '
    flag = 0
    for it in x:
        if it[0].collidepoint(cursor):
            flag = 1
            (shortcut, dirname) = it[1].split(gl.DIRNUMSEP)
            if dirname == slash:
                fullpath = curdir.split(slash)[0] + slash
            elif dirname == '..':
                fullpath = slash.join(curdir.rstrip(slash).split(slash)[:-1]) + slash
                if fullpath.split(dash)[0] == slash:
                    # make it so when in root dir of MS-Windows it prints drive letter
                    fullpath = curdir.split(slash)[0] + slash
            else:
                fullpath = curdir + dirname + slash
            gl.OLD_CAP = fullpath + ' [' + shortcut + '] - imgv'
            if gl.OLD_CAP != get_caption()[0]:
                # perform only once (otherwise it flashes in title bar)
                set_caption(gl.OLD_CAP)
            break
    if not flag:
        gl.OLD_CAP = curdir + " - imgv"
        # nothing was hovered on the last pass
        if gl.OLD_CAP != get_caption()[0]:
            set_caption(gl.OLD_CAP)

