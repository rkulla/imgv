# image randomizer code by Ryan Kulla, rkulla@gmail.com
import gl
from cursor import wait_cursor, normal_cursor
from img_screen import get_center, my_update_screen
from load_img import load_img
from random import shuffle


def command_shuffle(new_img, img, screen, rect, file):
    "randomize the images"
    wait_cursor()
    shuffle(gl.files)
    new_img = load_img(gl.files[file])
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    normal_cursor()
    return (new_img, new_img, new_img, rect)


def command_unshuffle(new_img, img, screen, rect, file):
    "un-randomize the images"
    was_on = gl.files[file]
    wait_cursor()
    gl.files.sort(lambda x, y: cmp(x.lower(), y.lower()))
    file = gl.files.index(was_on)
    new_img = load_img(gl.files[file])
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    normal_cursor()
    return (new_img, new_img, new_img, rect, file)
