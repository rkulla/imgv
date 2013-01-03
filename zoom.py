# image zooming code by Ryan Kulla, rkulla@gmail.com
import gl
from cursor import wait_cursor, normal_cursor
from img_screen import get_center, my_update_screen
from load_timers import start_timer, check_timer
from pygame.transform import scale, scale2x


def command_zoom_out(new_img, new_img_width, new_img_height, img, screen, file, rect, zoom_type):
    wait_cursor()
    start = start_timer()
    if new_img.get_width() >= gl.MIN_WIDTH and new_img.get_height() >= gl.MIN_HEIGHT:
        gl.ZOOM_EXP -= 1
        if zoom_type == "normal":
            gl.ZOOM_DOUBLE = 0
            new_img = scale(img, (new_img.get_width() / 1.1, new_img.get_height() / 1.1))
        else:
            gl.ZOOM_DOUBLE = 1
            new_img = scale(img, (new_img.get_width() / 2, new_img.get_height() / 2))
        rect = get_center(screen, new_img)
        my_update_screen(new_img, screen, rect, file, check_timer(start))
    normal_cursor()
    return (new_img, img, rect)


def command_zoom_in(new_img, new_img_width, new_img_height, img, screen, files, file, rect, zoom_type):
    wait_cursor()
    start = start_timer()
    gl.ZOOM_EXP += 1
    if zoom_type == "normal":
        gl.ZOOM_DOULBE = 0
        new_img = scale(img, (new_img.get_width() * 1.1, new_img.get_height() * 1.1))
    if zoom_type == "double":
        gl.ZOOM_DOUBLE = 1
        new_img = scale(img, (new_img.get_width() * 2, new_img.get_height() * 2))
    if zoom_type == "scale2x":
        gl.ZOOM_DOUBLE = 1
        new_img = scale2x(img) # don't alias simple solid color images (ie., black & white GIFs)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, screen, rect, file, check_timer(start))
    normal_cursor()
    return (new_img, img, rect)
