# image removal (closing, not deleting) code by Ryan Kulla, rkulla@gmail.com
import gl
from load_timers import check_timer, start_timer
from cursor import wait_cursor, normal_cursor
from img_surf import next_img, previous_img
from img_screen import get_center, my_update_screen
from error_screen import error_screen
from os import unlink


def command_remove_img(new_img, screen, file, rect):
    "Don't display the image anymore during the session"
    wait_cursor()
    start = start_timer()
    num_imgs = len(gl.files)
    # only remove file if its not the only one:
    if not num_imgs < 2:
        gl.files.remove(gl.files[file])
        # go to the next image if there is one
        if file < (num_imgs - 1):
            new_img = next_img(file, new_img, screen)
        # if not go to the previous image
        else:
            if file > 0:
                file = file - 1
                new_img = previous_img(file, new_img, screen)
        rect = get_center(screen, new_img)
        ns = check_timer(start)
        my_update_screen(new_img, screen, rect, file, ns)
    normal_cursor()
    return (new_img, new_img, new_img, file, rect)


def command_delete_img(fn, new_img, screen, file, rect):
    try:
        unlink(fn)
        (new_img, new_img, new_img, file, rect) = command_remove_img(new_img, screen, file, rect)
        return (new_img, new_img, new_img, file, rect)
    except OSError, err_msg:
        error_screen(screen, "Can't delete: %s" % err_msg)
        return (new_img, new_img, new_img, file, rect)
