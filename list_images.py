# image name list dialog code by Ryan Kulla, rkulla@gmail.com
import gl
from file_master import command_file_master
from img_screen import my_update_screen, get_center, paint_screen
from load_timers import start_timer, check_timer
from load_img import load_img
from cursor import normal_cursor, wait_cursor
from res import  adjust_screen, restore_screen


def command_img_names(screen, new_img, img, file, rect):
    num_imgs = len(gl.files)
    (screen, before_winsize, not_accepted) = adjust_screen(screen)
    paint_screen(screen, gl.BLACK)
    normal_cursor()
    gl.SORT_HIT = 0
    (list_names, filename, x, my_string) = command_file_master(screen, gl.files,\
    "(%d Images)" % len(gl.files), 15, 0, 1, 0)
    wait_cursor()
    start = start_timer()
    screen = restore_screen(screen, before_winsize, not_accepted, new_img, file, rect)
    if not filename == None:
        if num_imgs > 1:
            file = gl.files.index(filename)
        new_img = load_img(gl.files[file], screen)
        rect = get_center(screen, new_img)
        ns = check_timer(start)
        my_update_screen(new_img, rect, file, ns)
    normal_cursor()
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    return (new_img, new_img, new_img, file, rect)

