# image zooming code by Ryan Kulla, rkulla@gmail.com
import gl
from cursor import wait_cursor, normal_cursor
from img_screen import get_center, my_update_screen
from load_timers import start_timer, check_timer
from pygame.transform import scale, scale2x
from pygame.display import get_surface


def command_zoom_out(new_img, img, file, rect, zoom_type):
    wait_cursor()
    start = start_timer()
    screen = get_surface()
    new_img_width = new_img.get_width()
    new_img_height = new_img.get_height()
    if new_img_width >= gl.MIN_WIDTH and new_img_height >= gl.MIN_HEIGHT:
        gl.ZOOM_EXP -= 1
        if zoom_type == "normal":
            gl.ZOOM_DOUBLE = 0
            new_img = scale(img, (int(new_img_width / 1.1), int(new_img_height / 1.1)))
        else:
            gl.ZOOM_DOUBLE = 1
            new_img = scale(img, (new_img_width / 2, new_img_height / 2))
        rect = get_center(screen, new_img)
        my_update_screen(new_img, rect, file, check_timer(start))
    normal_cursor()
    return (new_img, img, rect)


def command_zoom_in(new_img, img, file, rect, zoom_type):
    wait_cursor()
    start = start_timer()
    screen = get_surface()
    new_img_width = new_img.get_width()
    new_img_height = new_img.get_height()
    gl.ZOOM_EXP += 1
    if zoom_type == "normal":
        gl.ZOOM_DOULBE = 0
        new_img = scale(img, (int(new_img_width * 1.1), int(new_img_height * 1.1)))
    if zoom_type == "double":
        gl.ZOOM_DOUBLE = 1
        new_img = scale(img, (new_img_width * 2, new_img_height * 2))
    if zoom_type == "scale2x":
        gl.ZOOM_DOUBLE = 1
        new_img = scale2x(img)  # don't alias simple solid color images (ie., black & white GIFs)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file, check_timer(start))
    normal_cursor()
    return (new_img, img, rect)
