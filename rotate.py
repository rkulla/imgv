# image rotate/flip code by Ryan Kulla, rkulla@gmail.com
from load_timers import start_timer, check_timer
from cursor import wait_cursor, normal_cursor
from img_screen import get_center, my_update_screen
from pygame.transform import rotate, flip


def command_rotate_left(new_img, screen, file, rect):
    "rotate counter clockwise"
    wait_cursor()
    start = start_timer()
    new_img = rotate(new_img, 90)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, screen, rect, file, check_timer(start))
    normal_cursor()
    return (new_img, new_img, rect)


def command_rotate_right(new_img, screen, file, rect):
    "rotate clockwise"
    wait_cursor()
    start = start_timer()
    new_img = rotate(new_img, -90)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, screen, rect, file, check_timer(start))
    normal_cursor()
    return (new_img, new_img, rect)


def command_horiz(new_img, screen, file, rect):
    "flip horizontally (mirror)"
    wait_cursor()
    start = start_timer()
    new_img = flip(new_img, 90, 0)
    my_update_screen(new_img, screen, rect, file, check_timer(start))
    normal_cursor()
    return (new_img, new_img, rect)


def command_vert(new_img, screen, file, rect):
    "flip vertically"
    wait_cursor()
    start = start_timer()
    new_img = flip(new_img, 90, 90)
    my_update_screen(new_img, screen, rect, file, check_timer(start))
    normal_cursor()
    return (new_img, new_img, rect)
