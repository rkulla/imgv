# image playlist code by Ryan Kulla, rkulla@gmail.com
import gl
import os
import dir_nav
from load_img import load_img
from file_master import command_file_master
from show_message import show_message
from img_screen import my_update_screen, get_center, paint_screen
from usr_event import check_quit
from cursor import normal_cursor, wait_cursor
import pygame.font, pygame.event
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN


def command_add_to_play_list(screen, filename):
    paint_screen(gl.BLACK)
    normal_cursor()
    gl.SORT_HIT = 1
    small_font = pygame.font.Font(gl.FONT_NAME, 10)
    f = open(gl.IMGV_PLAYLISTS)
    file_names = f.readlines()
    if len(file_names) == 0:
        return (file_names, None, None, None, None)
    f.close()
    file_names.sort(lambda x, y: cmp(x.lower(), y.lower()))
    for count in range(len(file_names)):
        file_names[count] = file_names[count].replace('\n', '')
    (list_names, play_list_name, x, my_string) = command_file_master(screen,\
    file_names, "LEFT-CLICK list name to add to list", 25, 0, 1, 0)
    if (list_names == None):
        return
    play_list = gl.DATA_DIR + play_list_name
    f = open(play_list, 'a')
    if os.path.isdir(filename):
        filez = dir_nav.get_imgs(os.getcwd(), 0)
        filez.sort(lambda x, y: cmp(x.lower(), y.lower()))
        for file in filez:
            f.write(file + "\n")
    else:
        if os.sep not in filename and filename.startswith("http:") != 1:
            filename = os.getcwd() + os.sep + filename + "\n"
        f.write(filename + "\n")
    f.close()
    normal_cursor()


def command_play_list_options(screen, file):
    paint_screen(gl.BLACK)
    old_file = file
    (file, msg) = play_list_options(screen, file)
    if (msg != None and file != "rclicked" and file != "deleteit"):
        play_list_options_msg(screen, msg)
    if (file == "rclicked"):
        edit_play_list(screen, msg)
        file = old_file
    if (file == "deleteit"):
        delete_play_list(msg)
        file = old_file
    new_img = load_img(gl.files[file])
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    normal_cursor()
    return (new_img, new_img, new_img, file, rect)


def play_list_options(screen, file):
    normal_cursor()
    f = open(gl.IMGV_PLAYLISTS)
    file_names = f.readlines()
    f.close()
    file_names.sort(lambda x, y: cmp(x.lower(), y.lower()))
    gl.SORT_HIT = 1
    for count in range(len(file_names)):
        file_names[count] = file_names[count].replace('\n', '')
    (list_names, play_list_name, x, my_string) = command_file_master(screen, file_names, "There are %d Play Lists. (LEFT-CLICK list name to use. RIGHT-CLICK to edit. CTRL+LEFT-CLICK to delete)" % len(file_names), 5, 1, 0, 0)
    wait_cursor()
    if x == "deleteit":
        return ("deleteit", play_list_name)
    if x == "rclicked":
        return ("rclicked", play_list_name)
    if my_string != None and my_string != "\n":
        my_string = str(''.join(my_string))
        new_list = gl.DATA_DIR + my_string
        f = open(gl.IMGV_PLAYLISTS, 'a')
        new_list_name = os.path.basename(new_list + "\n")
        if new_list_name != "\n": # no blank lists (user just hit RETURN)
            f.write(new_list_name)
            f.close()
            open(new_list, 'w')
        return (file, None)
    if (play_list_name == None):
        return (file, None)
    play_list = gl.DATA_DIR + play_list_name
    try:
        f = open(play_list)
        tmp_files = f.readlines()
        if len(tmp_files) > 0:
            gl.files = tmp_files
            for count in range(len(gl.files)):
                gl.files[count] = gl.files[count].replace('\n', '')
            f.close()
            gl.PLAY_LIST_NAME = os.path.basename(play_list)
            return (0, None)
        return (file, "\"%s\" is empty or not in %s" % (os.path.basename(play_list), gl.DATA_DIR))
    except IOError:
        return (file, "\"%s\" is empty or not in %s" % (os.path.basename(play_list), gl.DATA_DIR))


def edit_play_list(screen, play_list_name):
    paint_screen(gl.BLACK)
    keep_going = 1
    play_list = gl.DATA_DIR + play_list_name
    f = open(play_list)
    file_names = f.readlines()
    f.close()
    if len(file_names) < 1:
        play_list_options_msg(screen, "Can't edit %s, it is empty" %\
        play_list)
        keep_going = 0
    for count in range(len(file_names)):
        file_names[count] = file_names[count].replace('\n', '')
    normal_cursor()
    if keep_going:
        (list_names, play_list_item, x, my_string) = command_file_master(screen,\
        file_names, "Click item to delete it from play list", 47, 0, 1, "do again")
        file_names = delete_item(screen, play_list_item, play_list)
        if x == "do again":
            while 1:
                if len(file_names) < 1:
                    break
                (list_names, play_list_item, x, my_string) = command_file_master(screen,\
                file_names,    "Click to delete another item from play list", 47, 0, 1,\
                "do again")
                file_names = delete_item(screen, play_list_item, play_list)
                if x != "do again":
                    break


def delete_item(screen, play_list_item, play_list):
    f = open(play_list)
    file_names = f.readlines()
    f.close()
    for count in range(len(file_names)):
        file_names[count] = file_names[count].replace('\n', '')
    # rewrite the list
    f = open(play_list, 'w+')
    for line in file_names:
        if line == play_list_item:
            continue # don't rewrite this item
        f.write(line + "\n")
    f.close()
    # get changed items
    f = open(play_list)
    file_names = f.readlines()
    f.close()
    for count in range(len(file_names)):
        file_names[count] = file_names[count].replace('\n', '')
    return file_names


def delete_play_list(play_list):
    if os.path.isfile(gl.DATA_DIR + play_list):
        del_file = gl.DATA_DIR + play_list
        os.remove(del_file)
    f = open(gl.IMGV_PLAYLISTS)
    file_names = f.readlines()
    f.close()
    for count in range(len(file_names)):
        file_names[count] = file_names[count].replace('\n', '')
    f = open(gl.IMGV_PLAYLISTS, 'w+')
    for line in file_names:
        if line == play_list:
            continue # don't rewrite this item
        f.write(line + "\n")
    f.close()


def play_list_options_msg(screen, msg):
    paint_screen(gl.BLACK)
    show_message(msg, 100, 10)
    normal_cursor()
    while 1:
        event = pygame.event.wait()
        check_quit(event)
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            wait_cursor()
            break
