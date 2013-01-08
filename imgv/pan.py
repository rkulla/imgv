# image panning code by Ryan Kulla, rkulla@gmail.com
import gl
from status_bar import img_info
from cursor import drag_hand_cursor
from pygame.display import update, get_surface


def command_down(rect, last_rect, new_img, file):
    "scroll image to downward to see more of the top"
    screen = get_surface()
    gl.HAND_TOOL = 1
    if (0 - rect.top <= gl.MOVE):
        rect.top = 0
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    elif (rect.top + gl.MOVE) < 0:
        rect.top += gl.MOVE
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    drag_hand_cursor()
    return rect


def command_full_down(rect, last_rect, new_img, file):
    "scroll image to all the way downward to see the very top"
    screen = get_surface()
    gl.HAND_TOOL = 1
    if rect.top < 0:
        rect.top = 0
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    drag_hand_cursor()
    return rect


def command_up(rect, last_rect, new_img, file):
    "scroll image upward to see more of the bottom"
    screen = get_surface()
    screen_height = screen.get_height()
    gl.HAND_TOOL = 1
    if (rect.bottom - screen_height <= gl.MOVE) and rect.bottom > screen_height:
        rect.bottom = screen_height  # snap
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    elif (rect.bottom - gl.MOVE) > screen_height:
        rect.bottom -= gl.MOVE
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    drag_hand_cursor()
    return rect


def command_full_up(rect, last_rect, new_img, file):
    "scroll image all the way upward to see the very bottom"
    screen = get_surface()
    screen_height = screen.get_height()
    gl.HAND_TOOL = 1
    if rect.bottom > screen_height:
        rect.bottom = screen_height
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    drag_hand_cursor()
    return rect


def command_right(rect, last_rect, new_img, file):
    "scroll image to the right to see more of its left side"
    screen = get_surface()
    if 0 - rect.left <= gl.MOVE:
        rect.left = 0  # snap
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    elif (rect.left + gl.MOVE) < 0:
        rect.left += gl.MOVE
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    drag_hand_cursor()
    return rect


def command_full_right(rect, last_rect, new_img, file):
    "scroll image to all the way to the right to see the very left side"
    screen = get_surface()
    gl.HAND_TOOL = 1
    if rect.left < 0:
        rect.left = 0
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    drag_hand_cursor()
    return rect


def command_left(rect, last_rect, new_img, file):
    "scroll image to the left to see more of its right side"
    screen = get_surface()
    screen_width = screen.get_width()
    if (rect.right - screen_width <= gl.MOVE) and rect.right > screen_width:
        rect.right = screen_width  # snap
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    elif (rect.right - gl.MOVE) > screen_width:
        rect.right -= gl.MOVE
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    drag_hand_cursor()
    return rect


def command_full_left(rect, last_rect, new_img, file):
    "scroll image to all the way to the left to see the very right side"
    screen = get_surface()
    screen_width = screen.get_width()
    gl.HAND_TOOL = 1
    if rect.right > screen_width:
        rect.right = screen_width
        screen.blit(new_img, rect)
        update(rect.union(last_rect))
        img_info(gl.files[file], file, new_img, gl.NS_GLOBAL[0])
    drag_hand_cursor()
    return rect
