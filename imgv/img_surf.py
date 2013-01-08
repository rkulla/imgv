# image navigation code by Ryan Kulla, rkulla@gmail.com
import gl
from cursor import wait_cursor, normal_cursor
from load_img import load_img
from img_screen import my_update_screen, get_center
from transitional import transitional_fx


def command_first_img(new_img, screen, file, rect):
    "jump to the first image"
    wait_cursor()
    file = 0
    new_img = load_img(gl.files[file])
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    normal_cursor()
    return (new_img, new_img, new_img, file, rect)


def command_last_img(new_img, screen, file, rect):
    "jump to the last image"
    wait_cursor()
    num_imgs = len(gl.files)
    while file < (num_imgs - 1):
        file = file + 1
    new_img = load_img(gl.files[file])
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    normal_cursor()
    return (new_img, new_img, new_img, file, rect)


def command_next_img(new_img, screen, file, rect):
    "jump to next image"
    wait_cursor()
    num_imgs = len(gl.files)
    if not gl.WRAP:
        if file < (num_imgs - 1):
            file = file + 1
            new_img = next_img(file, new_img, screen)
            rect = get_center(screen, new_img)
            my_update_screen(new_img, rect, file)
    else:
        file = file + 1
        if file > (num_imgs - 1):
            file = 0
        if num_imgs > 1:
            new_img = next_img(file, new_img, screen)
            rect = get_center(screen, new_img)
            my_update_screen(new_img, rect, file)
    normal_cursor()
    return (new_img, new_img, new_img, file, rect)


def command_prev_img(new_img, screen, file, rect):
    "jump to previous image"
    wait_cursor()
    if file > 0:
        file = file - 1
        new_img = previous_img(file, new_img, screen)
        rect = get_center(screen, new_img)
        my_update_screen(new_img, rect, file)
    normal_cursor()
    return (new_img, new_img, new_img, file, rect)


def next_img(file, old_img, screen):
    img = old_img
    if file < len(gl.files):
        img = load_img(gl.files[file])
    transitional_fx(screen, img)
    return img


def previous_img(file, old_img, screen):
    img = old_img
    img = load_img(gl.files[file])
    return img
