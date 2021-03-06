# image resetting code by Ryan Kulla, rkulla@gmail.com
import gl
from cursor import wait_cursor, normal_cursor
from img_screen import my_update_screen, get_center
from load_img import load_img
from dir_nav import adjust_files


def command_refresh(refresh_img, screen, files, file):
    "reset image to its original state"
    wait_cursor()
    new_img = refresh_img
    rect = get_center(screen, new_img)
    cur_filename = ""
    if len(gl.files) > 1:
        cur_filename = gl.files[file]
    else:
        normal_cursor()
        return (new_img, new_img, get_center(screen, new_img), file)
    if gl.SHRUNK and len(gl.files) > 1:
        # reload shrunk images to their true size
        gl.SKIP_FIT = 1
        refresh_img = load_img(gl.files[file])
        rect = get_center(screen, refresh_img)
        adjust_files(gl.SUBDIRS)
        if cur_filename in gl.files:
            file = gl.files.index(cur_filename)  # go back if new images were loaded
        my_update_screen(refresh_img, rect, file)
        normal_cursor()
        return (refresh_img, new_img, rect, file)
    adjust_files(gl.SUBDIRS)
    if cur_filename in gl.files and len(gl.files) > 1:
        file = gl.files.index(cur_filename)  # go back if new images were loaded
    my_update_screen(refresh_img, rect, file)
    normal_cursor()
    return (new_img, new_img, get_center(screen, new_img), file)
