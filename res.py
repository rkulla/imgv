# imgv window resolution/resizing code by Ryan Kulla, rkulla@gmail.com
import gl
from sys import platform
from cursor import wait_cursor, hover_cursor
from show_message import show_message
from buttons import close_button
from img_screen import my_update_screen, get_center, paint_screen
from input_box import ask
from usr_event import check_quit, hit_key, left_click
from load_img import load_img
import pygame.mouse
import pygame.event
import pygame.font
from pygame.display import set_mode, toggle_fullscreen, list_modes, update, set_caption, get_surface
from pygame.locals import FULLSCREEN, MOUSEMOTION, K_ESCAPE, KEYDOWN, K_F2, K_F3, K_F4, K_F5, K_F6, K_c, RESIZABLE, VIDEORESIZE


def adjust_screen(screen, *flags):
    before_winsize = screen.get_size()
    not_accepted = 0
    if not flags:
        flags = 0
    else:
        flags = flags[0]
    if ("%sx%s" % before_winsize) not in gl.ACCEPTED_WINSIZES:
        not_accepted = 1
        if gl.DEFAULT_RES[0] <= 640:
            gl.MAX_SCREEN_FILES = gl.MAX_SF["640x480"]
            screen = set_mode((640, 480), flags)
        elif gl.DEFAULT_RES[0] <= 800:
            gl.MAX_SCREEN_FILES = gl.MAX_SF["800x600"]
            screen = set_mode((800, 600), flags)
        elif gl.DEFAULT_RES[0] <= 1024:
            gl.MAX_SCREEN_FILES = gl.MAX_SF["1024x768"]
            screen = set_mode((1024, 768), flags)
        elif gl.DEFAULT_RES[0] <= 1280:
            gl.MAX_SCREEN_FILES = gl.MAX_SF["1280x1024"]
            screen = set_mode((1280, 1024), flags)
        else:
            # default to 800x600 if the screen size isn't an imgv preset size:
            gl.MAX_SCREEN_FILES = gl.MAX_SF["800x600"]
            screen = set_mode((800, 600), flags)
    else:
        if flags and not gl.TOGGLE_FULLSCREEN_SET:
            screen = set_mode(before_winsize, flags)
        else:
            if not gl.TOGGLE_FULLSCREEN_SET:
                screen = set_mode(
                    before_winsize)  # take away resize priviledges
    return (screen, before_winsize, not_accepted)


def restore_screen(screen, before_winsize, not_accepted, new_img, file, rect):
    if gl.TOGGLE_FULLSCREEN_SET and not_accepted:
        # we were fullscreen with gl.FULLSCREEN_SPECIAL on a non-accepted window size
        screen = command_fullscreen(new_img, file, rect)
    else:
        if not gl.TOGGLE_FULLSCREEN_SET:
            screen = set_mode(before_winsize, RESIZABLE)
    return screen


def command_640x480(new_img, file, rect):
    "switch to 640x480"
    gl.MAX_SCREEN_FILES = gl.MAX_SF["640x480"]
    wait_cursor()
    resolution = 640, 480
    screen = set_mode(resolution, RESIZABLE)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    if gl.TOGGLE_FULLSCREEN_SET:
        my_toggle_fullscreen()
    return rect


def command_800x600(new_img, file, rect):
    "switch to 800x600"
    gl.MAX_SCREEN_FILES = gl.MAX_SF["800x600"]
    wait_cursor()
    resolution = 800, 600
    screen = set_mode(resolution, RESIZABLE)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    if gl.TOGGLE_FULLSCREEN_SET:
        my_toggle_fullscreen()
    return rect


def command_1024x768(new_img, file, rect):
    "switch to 1024x768"
    gl.MAX_SCREEN_FILES = gl.MAX_SF["1024x768"]
    wait_cursor()
    resolution = 1024, 768
    screen = set_mode(resolution, RESIZABLE)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    if gl.TOGGLE_FULLSCREEN_SET:
        my_toggle_fullscreen()
    return rect


def command_1280x1024(new_img, file, rect):
    "switch to 1280x1024"
    gl.MAX_SCREEN_FILES = gl.MAX_SF["1280x1024"]
    wait_cursor()
    resolution = 1280, 1024
    screen = set_mode(resolution, RESIZABLE)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    if gl.TOGGLE_FULLSCREEN_SET:
        my_toggle_fullscreen()
    return rect


def command_custom_res(screen, new_img, file, rect, resolution):
    "switch to customxcustom"
    wait_cursor()
    screen = set_mode(resolution, RESIZABLE)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)
    if gl.TOGGLE_FULLSCREEN_SET:
        my_toggle_fullscreen()
    return rect


def command_fullscreen(new_img, file, rect):
    "Toggle between full screen and last screen resolution"
    screen = get_surface
    wait_cursor()
    if not toggle_fullscreen():
        try:
            if gl.FULLSCREEN_SPECIAL:
                screen_res = screen.get_size()
            else:
                screen_res = screen.get_size()
                gl.MAX_SCREEN_FILES = gl.MAX_SF["%sx%s" % (
                    screen_res[0], screen_res[1])]

            if not gl.TOGGLE_FULLSCREEN_SET:  # go into fullscreen mode
                gl.BEFORE_WINSIZE = screen.get_size()
                screen = set_mode(screen_res, screen.get_flags(
                ) ^ FULLSCREEN, screen.get_bitsize())
            else:  # returning from fullscreen. Go back to last screen size:
                set_mode(gl.BEFORE_WINSIZE, screen.get_flags(
                ) ^ FULLSCREEN, screen.get_bitsize())
                screen = set_mode(
                    gl.BEFORE_WINSIZE, RESIZABLE)  # make resizeable
            my_toggle_fullscreen()
        except:
            print "Couldn't toggle fullscreen. Resolution probably not supported by your video card."
    return screen


def get_resolution():
    default_res = (800, 600)
    if platform == 'win32':
        from win32api import GetSystemMetrics
        screen_res = (
            GetSystemMetrics(0), GetSystemMetrics(1))  # user's screen res
        if screen_res not in list_modes():
            screen_res = default_res
    else:
        screen_res = default_res
    return screen_res


def command_show_res_modes(screen, new_img, file, rect):
    paint_screen(gl.BLACK)
    set_caption("Resize Options - imgv")
    menu_items = []
    (esc_rect, font) = close_button(screen)
    res_font = pygame.font.Font(gl.FONT_NAME, 18)
    res_font.set_bold(1)
    show_message("Choose a preset or custom window size for imgv",
                 "top", 12, ("underline", "bold"))
    show_message(
        "Use current window size as fullscreen resolution?", (170, 192), 10)
    show_message("No  Yes", (430, 182), 10)
    show_message("Option: _", "bottom", 12)
    (menu_items, men_ops) = show_res_modes(screen, menu_items, res_font)
    pygame.event.set_blocked(MOUSEMOTION)
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(35)  # don't use 100% CPU
        cursor = pygame.mouse.get_pos()
        hover_fx(screen, menu_items, cursor, res_font)
        if gl.NOT_HOVERED:
            show_message(
                "%sOption: _%s" % (" " * 100, " " * 100), "bottom", 12)
            blank_fx(screen, 0)
        check_quit(event)

        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            rect = get_center(screen, new_img)
            command_show_res_modes(screen, new_img, file, rect)
            break

        # draw checked box:
        checked_img = load_img(gl.CHECKED_BOX, screen, False)
        checked_img_rect = checked_img.get_rect()
        if gl.FULLSCREEN_SPECIAL == 0:
            checked_img_rect[0] = 432
        else:
            checked_img_rect[0] = 455
        checked_img_rect[1] = 195
        screen.blit(checked_img, checked_img_rect)
        update(checked_img_rect)

        # draw unchecked box:
        unchecked_img = load_img(gl.UNCHECKED_BOX, screen, False)
        unchecked_img_rect = unchecked_img.get_rect()
        if gl.FULLSCREEN_SPECIAL == 0:
            unchecked_img_rect[0] = 455
        else:
            unchecked_img_rect[0] = 432
        unchecked_img_rect[1] = 195
        screen.blit(unchecked_img, unchecked_img_rect)
        update(unchecked_img_rect)

        hover_cursor(cursor, [esc_rect, checked_img_rect,
                     unchecked_img_rect] + [x[0] for x in menu_items])

        if hit_key(event, K_ESCAPE):
            update_res_screen(screen, file, new_img)
            return rect
        if event.type == KEYDOWN and event.key in (K_F2, K_F3, K_F4, K_F5, K_F6, K_c):
            if hit_key(event, K_F2):
                rect = command_640x480(new_img, file, rect)
            if hit_key(event, K_F3):
                rect = command_800x600(new_img, file, rect)
            if hit_key(event, K_F4):
                rect = command_1024x768(new_img, file, rect)
            if hit_key(event, K_F5):
                rect = command_1280x1024(new_img, file, rect)
            if hit_key(event, K_F6):
                screen = command_fullscreen(new_img, file, rect)
                rect = get_center(screen, new_img)
                my_update_screen(new_img, rect, file)
            if hit_key(event, K_c):
                rect = do_custom(screen, new_img, file, rect)
            return rect
        if left_click(event):
            if esc_rect.collidepoint(cursor):
                gl.ESCAPED = 1
                update_res_screen(screen, file, new_img)
                return rect
            if unchecked_img_rect.collidepoint(cursor):
                gl.FULLSCREEN_SPECIAL ^= 1  # toggle
            for it in menu_items:
                if it[0].collidepoint(cursor) and it[1] in men_ops:
                    if it[1] == "F2) 640x480":
                        rect = command_640x480(new_img, file, rect)
                    elif it[1] == "F3) 800x600":
                        rect = command_800x600(new_img, file, rect)
                    elif it[1] == "F4) 1024x768":
                        rect = command_1024x768(new_img, file, rect)
                    elif it[1] == "F5) 1280x1024":
                        rect = command_1280x1024(new_img, file, rect)
                    elif it[1] == "F6) Fullscreen":
                        screen = command_fullscreen(new_img, file, rect)
                        rect = get_center(screen, new_img)
                        my_update_screen(new_img, rect, file)
                    elif it[1] == "C) Custom":
                        rect = do_custom(screen, new_img, file, rect)
                    return rect
        gl.NOT_HOVERED = 1
    return rect


def show_res_modes(screen, menu_items, font):
    men_ops = ["F2) 640x480", "F3) 800x600", "F4) 1024x768",
               "F5) 1280x1024", "F6) Fullscreen", "C) Custom"]
    line = 65
    col = 20
    for m in men_ops:
        ren_name = m
        ren = font.render(ren_name, 1, gl.BLUE)
        ren_rect = ren.get_rect()
        ren_rect[0] = col
        ren_rect[1] = line
        menu_items.append((ren_rect, m))
        screen.blit(ren, ren_rect)
        line = line + 30
        update(ren_rect)
    return (menu_items, men_ops)


def hover_fx(screen, menu_items, cursor, font):
    for it in menu_items:
        if it[0].collidepoint(cursor):
            if it[1] == "F2) 640x480":
                blank_fx(screen, 1)
                gl.FIRST_RECT = index_fx(screen, it, font, "Resize to 640x480")
                break
            elif it[1] == "F3) 800x600":
                blank_fx(screen, 2)
                gl.SECOND_RECT = index_fx(
                    screen, it, font, "Resize to 800x600")
                break
            elif it[1] == "F4) 1024x768":
                blank_fx(screen, 3)
                gl.THIRD_RECT = index_fx(
                    screen, it, font, "Resize to 1024x768")
                break
            elif it[1] == "F5) 1280x1024":
                blank_fx(screen, 4)
                gl.FOURTH_RECT = index_fx(
                    screen, it, font, "Resize to 1280x1024")
                break
            elif it[1] == "F6) Fullscreen":
                if gl.FULLSCREEN_SPECIAL:
                    sw, sh = screen.get_size()
                    fsmsg = "Toggle Fullscreen @ %sx%s" % (sw, sh)
                else:
                    screen_res = get_resolution()
                    fsmsg = "Toggle Fullscreen @ %sx%s" % (
                        screen_res[0], screen_res[1])
                blank_fx(screen, 5)
                gl.FIFTH_RECT = index_fx(screen, it, font, fsmsg)
                break
            elif it[1] == "C) Custom":
                blank_fx(screen, 6)
                gl.SIXTH_RECT = index_fx(screen, it, font, "Custom Size")
                break


def blank_fx(screen, row):
    l = [gl.FIRST_RECT, gl.SECOND_RECT, gl.THIRD_RECT, gl.FOURTH_RECT,
         gl.FIFTH_RECT, gl.SIXTH_RECT]
    for i in range(len(l)):
        if i != row - 1:
            show_message("  ", l[i], 12, ("bold"))
                         # erase effect from non-hovered items


def index_fx(screen, it, font, msg):
    gl.NOT_HOVERED = 0
    fxpos = (it[0][0] - 10, it[0][1] + (font.size(it[1])[1] / 2) - 13,
             it[0][2], it[0][3])
    show_message(".", fxpos, 16, ("bold"))
    show_message("%s%s%s" % (" " * 20, msg, " " * 20), "bottom", 12)
    return fxpos


def update_res_screen(screen, file, new_img):
    rect = get_center(screen, new_img)
    my_update_screen(new_img, rect, file)


def do_custom(screen, new_img, file, rect):
    paint_screen(gl.BLACK)
    show_message("Enter a custom window size/resolution. (Example:  455x500)",
                 "top", 12, ("bold"))
    res = ask(screen, "New size")
    if res is None:
        return rect
    try:
        res = res.lower().split('x')
        res = int(res[0]), int(res[1])
        rect = command_custom_res(screen, new_img, file, rect, res)
    except:
        return rect
    return rect


def my_toggle_fullscreen():
    # global sentinel objects (not to be confused with Pygame's toggle_fullscreen() function)
    if gl.TOGGLE_FULLSCREEN:
        gl.TOGGLE_FULLSCREEN = 0
    else:
        gl.TOGGLE_FULLSCREEN = 1
    if gl.TOGGLE_FULLSCREEN:
        gl.TOGGLE_FULLSCREEN_SET = 1
    else:
        gl.TOGGLE_FULLSCREEN_SET = 0
