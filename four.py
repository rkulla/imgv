# View four images on the screen at a time code by Ryan Kulla, rkulla@gmail.com
import gl
import os
from sys import platform
from img_screen import get_center, my_update_screen, paint_screen, junk_rect
from load_timers import start_timer, check_timer
from screensaver import disable_screensaver
from slideshow import get_speed, stopped_msg, pause
from show_message import show_message, truncate_name
from buttons import close_button
from load_img import load_img
from usr_event import hit_key, left_click, right_click, middle_click, check_quit
from cursor import wait_cursor, normal_cursor, hover_cursor
import pygame.event, pygame.mouse, pygame.draw, pygame.transform, pygame.time
from pygame.display import update, set_caption, set_mode, get_caption
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, K_SPACE, K_BACKSPACE, K_4,\
K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_p, K_PAUSE, K_w, K_TAB, K_n, K_b, VIDEOEXPOSE, VIDEORESIZE, RESIZABLE


def command_four(screen, file, new_img, ns):
    gl.MULTI_VIEWING = 1
    orig_ns = ns
    paint_screen(gl.IMGV_COLOR)
    set_caption("Four at a time - imgv")
    (file, new_img, start) = four(screen, file, new_img, ns)
    rect = get_center(screen, new_img)
    if start != orig_ns:
        ns = check_timer(start)
        my_update_screen(new_img, rect, file, ns)
    else:
        my_update_screen(new_img, rect, file)
    pygame.event.set_blocked(MOUSEMOTION) # without this the hovers don't work right
    gl.MULTI_VIEWING = 0
    return (file, new_img, new_img, new_img, rect)


def four(screen, file, new_img, ns):
    paint_screen(gl.IMGV_COLOR) # so transparent status bars don't mess up on VIDEOEXPOSE repaints
    old_file = file
    (img_one_rect, img_two_rect, img_three_rect, img_four_rect) = (0, 0, 0, 0)
    (img_one_name, img_two_name, img_three_name, img_four_name) = (0, 0, 0, 0)
    (show_img_one, show_img_two, show_img_three, show_img_four) = (0, 0, 0, 0)

    rect = show_message("", "bottom", 9, ("bold")) # needed to not paint on esc_rect first time
    (file, img_one_rect, img_one_name, img_one_file) = square_one(screen, file)
    (file, img_two_rect, img_two_name, img_two_file) = square_two(screen, file)
    (file, img_three_rect, img_three_name, img_three_file) = square_three(screen, file)
    (file, img_four_rect, img_four_name, img_four_file) = square_four(screen, file)

    (esc_rect, close_font) = close_button(screen)
    start = ns
    while 1:
        flag = 0
        event = pygame.event.poll()
        pygame.time.wait(1)
        cursor = pygame.mouse.get_pos()

        if event.type == VIDEORESIZE:
            pygame.event.set_blocked(VIDEOEXPOSE)
            screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            file = file - 4
            pygame.event.set_allowed(VIDEOEXPOSE)
            (file, new_img, start) = four(screen, file, new_img, ns)
            flag = 1
            break

        if hit_key(event, K_ESCAPE):
            gl.ESCAPED = 1
            file = old_file
            break
        check_quit(event)
        if hit_key(event, K_SPACE) or hit_key(event, K_n) or hit_key(event, K_4) or right_click(event): # show next 4 images
            paint_screen(gl.IMGV_COLOR)
            flag = 1
        if hit_key(event, K_BACKSPACE) or hit_key(event, K_b) or middle_click(event): # show previous 4 images
            paint_screen(gl.IMGV_COLOR)
            file = file - 8
            flag = 1

        if flag == 1:
            (file, img_one_rect, img_one_name, img_one_file) = square_one(screen, file)
        if flag == 1:
            (file, img_two_rect, img_two_name, img_two_file) = square_two(screen, file)
        if flag == 1:
            (file, img_three_rect, img_three_name, img_three_file) = square_three(screen,\
            file)
        if flag == 1:
            (file, img_four_rect, img_four_name, img_four_file) = square_four(screen, file)
        (show_img_one, show_img_two, show_img_three, show_img_four, rect) = hover_square(\
         screen, show_img_one, show_img_two, show_img_three, show_img_four, img_one_rect,\
        img_two_rect, img_three_rect, img_four_rect, img_one_name, img_two_name, img_three_name,\
        img_four_name, img_one_file, img_two_file, img_three_file, img_four_file, rect, event)

        hover_fx(screen, img_one_name, img_two_name, img_three_name, img_four_name, img_one_rect, img_two_rect, img_three_rect, img_four_rect, cursor)

        if show_img_one == None:
            file = old_file
            break
        if hit_key(event, K_w):
            if len(gl.files) <= 1: # nothin to slideshow
                file = old_file
                break # kick 'em out
            (file, img_one_file, img_two_file, img_three_file, img_four_file) =\
            my_fourslideshow(screen, new_img, rect, gl.files[file], file - 4,\
            len(gl.files), img_one_file, img_two_file, img_three_file, img_four_file, ns)
            paint_screen(gl.IMGV_COLOR)
            (file, new_img, start) = four(screen, file - 4, new_img, ns)
            flag = 1
            break
        if left_click(event):
            start = start_timer()
            if img_one_rect.collidepoint(cursor):
                wait_cursor()
                new_img = load_img(gl.files[img_one_file])
                return (img_one_file, new_img, start)
            if img_two_rect.collidepoint(cursor):
                wait_cursor()
                new_img = load_img(gl.files[img_two_file])
                return (img_two_file, new_img, start)
            if img_three_rect.collidepoint(cursor):
                wait_cursor()
                new_img = load_img(gl.files[img_three_file])
                return (img_three_file, new_img, start)
            if img_four_rect.collidepoint(cursor):
                wait_cursor()
                new_img = load_img(gl.files[img_four_file])
                return (img_four_file, new_img, start)
            if esc_rect.collidepoint(cursor):
                file = old_file
                gl.ESCAPED = 1
                break
        if event.type == VIDEOEXPOSE:
       # if event.type == VIDEOEXPOSE and not pygame.mouse.get_focused():#
            # repaint the screen in case other windows painted over it:
            file = file - 4
            (file, new_img, start) = four(screen, file, new_img, ns)
            flag = 1
            break
    return (file, new_img, start)


def square_one(screen, file):
    wait_cursor()
    draw_lines(screen)
    num_imgs = len(gl.files)
    if file >= num_imgs or file <= 0:
        file = 0
    img_one_name = gl.files[file]
    img_one_file = file
    img_one = load_img(img_one_name, 0)
    file = file + 1
    img_one = adjust_img_size(img_one, screen.get_width(), screen.get_height())
    img_one_rect = img_one.get_rect()
    screen.blit(img_one, img_one_rect)
    update(img_one_rect)
    draw_lines(screen)
    if gl.FOUR_STATUS_BARS:
        font_size = 9
        font = pygame.font.Font(gl.FONT_NAME, font_size)
        name = os.path.basename(img_one_name)
        name = check_truncate(screen.get_width(), name)
        img_status = "%s [%d/%d]" % (name, img_one_file + 1, num_imgs)
        raise_up = 12
        show_message(img_status, ((screen.get_width() / 4) - (font.size(img_status)[0] / 2), screen.get_height() / 2 - raise_up), font_size, ("bold"))
    normal_cursor()
    return (file, img_one_rect, img_one_name, img_one_file)


def square_two(screen, file):
    wait_cursor()
    draw_lines(screen)
    num_imgs = len(gl.files)
    if file >= num_imgs or file <= 0:
        file = 0
    img_two_name = gl.files[file]
    img_two_file = file
    img_two = load_img(img_two_name, 0)
    file = file + 1
    img_two = adjust_img_size(img_two, screen.get_width(), screen.get_height())
    img_two_rect = img_two.get_rect()
    img_two_rect[0] = (screen.get_width() / 2)
    screen.blit(img_two, img_two_rect)
    update(img_two_rect)
    draw_lines(screen)
    if gl.FOUR_STATUS_BARS:
        font_size = 9
        font = pygame.font.Font(gl.FONT_NAME, font_size)
        name = os.path.basename(img_two_name)
        name = check_truncate(screen.get_width(), name)
        img_status = "%s [%d/%d]" % (name, img_two_file + 1, num_imgs)
        raise_up = 12
        show_message(img_status, ((screen.get_width() / 2) + (screen.get_width() / 4 - font.size(img_status)[0]/2), screen.get_height() / 2 - raise_up), font_size, ("bold"))
    normal_cursor()
    return (file, img_two_rect, img_two_name, img_two_file)


def square_three(screen, file):
    wait_cursor()
    draw_lines(screen)
    num_imgs = len(gl.files)
    if file >= num_imgs or file <= 0:
        file = 0
    img_three_name = gl.files[file]
    img_three_file = file
    img_three = load_img(img_three_name, 0)
    file = file + 1
    img_three = adjust_img_size(img_three, screen.get_width(), screen.get_height())
    img_three_rect = img_three.get_rect()
    img_three_rect[1] = (screen.get_height() / 2)
    screen.blit(img_three, img_three_rect)
    update(img_three_rect)
    draw_lines(screen)
    if gl.FOUR_STATUS_BARS:
        font_size = 9
        font = pygame.font.Font(gl.FONT_NAME, font_size)
        name = os.path.basename(img_three_name)
        name = check_truncate(screen.get_width(), name)
        img_status = "%s [%d/%d]" % (name, img_three_file + 1, num_imgs)
        raise_up = 12
        show_message(img_status, ((screen.get_width() / 4) - (font.size(img_status)[0] / 2), screen.get_height() - raise_up), font_size, ("bold"))
    normal_cursor()
    return (file, img_three_rect, img_three_name, img_three_file)


def square_four(screen, file):
    wait_cursor()
    draw_lines(screen)
    num_imgs = len(gl.files)
    if file >= num_imgs or file <= 0:
        file = 0
    img_four_name = gl.files[file]
    img_four_file = file
    img_four = load_img(img_four_name, 0)
    file = file + 1
    img_four = adjust_img_size(img_four, screen.get_width(), screen.get_height())
    img_four_rect = img_four.get_rect()
    img_four_rect[0] = (screen.get_width() / 2)
    img_four_rect[1] = (screen.get_height() / 2)
    screen.blit(img_four, img_four_rect)
    update(img_four_rect)
    draw_lines(screen)
    if gl.FOUR_STATUS_BARS:
        font_size = 9
        font = pygame.font.Font(gl.FONT_NAME, font_size)
        name = os.path.basename(img_four_name)
        name = check_truncate(screen.get_width(), name)
        img_status = "%s [%d/%d]" % (name, img_four_file + 1, num_imgs)
        raise_up = 12
        show_message(img_status, ((screen.get_width() / 2) + (screen.get_width() / 4 - font.size(img_status)[0]/2), screen.get_height() - raise_up), font_size, ("bold"))
    normal_cursor()
    return (file, img_four_rect, img_four_name, img_four_file)


def check_truncate(screen_width, name):
    if screen_width <= 300:
        name = truncate_name(name, 5)
    if screen_width < 640 and screen_width > 300:
        name = truncate_name(name, 10)
    if screen_width >= 640 and screen_width < 800:
        name = truncate_name(name, 30)
    if screen_width >= 800 and screen_width < 1024:
        name = truncate_name(name, 50)
    if screen_width >= 1024 and screen_width < 1280:
        name = truncate_name(name, 80)
    if screen_width >= 1280:
        name = truncate_name(name, 100)
    return name


def draw_lines(screen):
    "Draw the lines that split the screen into 4 squares"
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    line_color = gl.FOUR_DIV_COLOR
    vline = pygame.draw.line(screen, line_color, ((screen_width / 2), screen_height), ((screen_width / 2), 0), 1)
    hline = pygame.draw.line(screen, line_color, (0, (screen_height / 2)), (screen_width, (screen_height / 2)), 1)
    update(vline)
    update(hline)


def hover_square(screen, show_img_one, show_img_two, show_img_three, show_img_four,\
img_one_rect, img_two_rect, img_three_rect, img_four_rect, img_one_name, img_two_name,\
img_three_name, img_four_name, img_one_file, img_two_file, img_three_file, img_four_file, rect, event):
    "display image name in title bar or on the screen on a mouse over"
    num_imgs = len(gl.files)
    cursor = pygame.mouse.get_pos()
    (esc_rect, font) = close_button(screen)
    hover_cursor(cursor, (esc_rect, img_one_rect, img_two_rect, img_three_rect, img_four_rect))
    if left_click(event):
        if esc_rect.collidepoint(cursor):
            gl.ESCAPED = 1
            return (None, None, None, None, None)
    if show_img_one == 0:
        if img_one_rect:
            if img_one_rect.collidepoint(cursor):
                name = img_one_name
                set_caption("%s - imgv" % name)
                show_img_one = 1
                (show_img_two, show_img_three, show_img_four) = (0, 0, 0)
    if show_img_two == 0:
        if img_two_rect:
            if img_two_rect.collidepoint(cursor):
                name = img_two_name
                set_caption("%s - imgv" % name)
                show_img_two = 1
                (show_img_one, show_img_three, show_img_four) = (0, 0, 0)
    if show_img_three == 0:
        if img_three_rect:
            if img_three_rect.collidepoint(cursor):
                name = img_three_name
                set_caption("%s - imgv" % name)
                show_img_three = 1
                (show_img_one, show_img_two, show_img_four) = (0, 0, 0)
    if show_img_four == 0:
        if img_four_rect:
            if img_four_rect.collidepoint(cursor):
                name = img_four_name
                set_caption("%s - imgv" % name)
                show_img_four = 1
                (show_img_one, show_img_two, show_img_three) = (0, 0, 0)
    return (show_img_one, show_img_two, show_img_three, show_img_four, rect)


def adjust_img_size(the_img, screen_width, screen_height):
    "scale the image down if necessary to fit in its square and with proper aspect ratio"
    square_width = screen_width / 2
    square_height = screen_height / 2
    small_img = the_img
    (img_width, img_height) = the_img.get_size()
    if img_width > img_height:
        if (not img_width < square_width and not img_height < square_height) or (img_width > square_width) or (img_height > square_height) or (img_width > square_width and img_height > square_height) or gl.FIT_IMAGE_VAL == 2:
            r = float(img_width) / float(img_height)
            new_width = square_width
            new_height = int(new_width / r)
            if new_width > square_width or new_height > square_height: # make sure
                scale_val = int(new_width / r), int(new_height / r)
            else:
                scale_val = new_width, new_height
            # some images are still too large:
            if scale_val[0] > square_width or scale_val[1] > square_height:
                # 1.32 seems to be the perfect number:
                scale_val = int(scale_val[0] / 1.32), int(scale_val[1] / 1.32)
            # but sometime's it's not:
            if scale_val[0] > square_width or scale_val[1] > square_height + 1:
                if screen_width > 600 and screen_height < 300:
                    scale_val = int(scale_val[0] / 4), int(scale_val[1] / 4)
                else:
                    scale_val = int(scale_val[0] / 2), int(scale_val[1] / 2)
            small_img = pygame.transform.scale(the_img, scale_val)
    if img_width < img_height:
        if (not img_width < square_width and not img_height < square_height) or (img_width > square_width) or (img_height > square_height) or (img_width > square_width and img_height > square_height) or gl.FIT_IMAGE_VAL == 2:
            r = float(img_height) / float(img_width)
            new_height = square_height
            new_width = int(new_height / r)
            if new_width > square_width or new_height > square_height: # make sure
                scale_val = int(new_width / r), int(new_height / r)
            else:
                scale_val = new_width, new_height
            if scale_val[0] > square_width or scale_val[1] > square_height:
                if screen_width < 200 and screen_height > 300:
                    scale_val = int(scale_val[0] / 2), int(scale_val[1] / 2)
                else:
                    scale_val = int(scale_val[0] / 2), int(scale_val[1] / 2)
            small_img = pygame.transform.scale(the_img, scale_val)
    if img_width == img_height:
        if (not img_width < square_width and not img_height < square_height) or (img_width > square_width) or (img_height > square_height) or (img_width > square_width and img_height > square_height) or gl.FIT_IMAGE_VAL == 2:
            r = float(img_width) / float(img_height)
            new_height = square_height
            new_width = square_width
            if new_height > new_width:
                scale_val = int(new_width / r), int(new_width / r)
            elif new_width > new_height:
                scale_val = int(new_height / r), int(new_height / r)
            else:
                scale_val = new_width, new_height
            small_img = pygame.transform.scale(the_img, scale_val)
    return small_img


def my_fourslideshow(screen, new_img, rect, filename, file, num_imgs, img_one_file, img_two_file, img_three_file, img_four_file, ns):
    if not gl.TOGGLE_FULLSCREEN_SET:
        screen = set_mode(screen.get_size())
    set_caption("Slideshow Options - imgv")
    speed = get_speed(screen, new_img, rect, filename, file, num_imgs)
    if not speed == -1:  # didn't hit Esc from get_speed:
        gl.SLIDE_SHOW_RUNNING = 1
        disable_screensaver()
        dont_call = 0
        while 1:
            event = pygame.event.poll()
            pygame.time.wait(1)
            check_quit(event)
            if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL,\
                K_p, K_PAUSE, K_TAB, K_SPACE, K_BACKSPACE):
                stopped_msg(screen)
                file = file - 1
                (file, new_img, start) = four(screen, file, new_img, ns) # needed to repaint
                break
            if hit_key(event, K_p) or hit_key(event, K_PAUSE):
                pause(screen)
            if dont_call == 1:
                break
            if not gl.WRAP_SLIDESHOW:
                if file < num_imgs:
                    (file, dont_call, img_one_file, img_two_file, img_three_file, img_four_file) =\
                    show_fourslideshow_imgs(screen, file, speed)
            if gl.WRAP_SLIDESHOW:
                if file >= num_imgs:
                    file = 0
                (file, dont_call, img_one_file, img_two_file, img_three_file, img_four_file) =\
                show_fourslideshow_imgs(screen, file, speed)
            pygame.time.delay(5)
    else: # escaped
        file = file + 4
        return (file, img_one_file, img_two_file, img_three_file, img_four_file)
    if not gl.TOGGLE_FULLSCREEN_SET:
        screen = set_mode(screen.get_size(), RESIZABLE)
    return (file, img_one_file, img_two_file, img_three_file, img_four_file)


def show_fourslideshow_imgs(screen, file, speed):
    paint_screen(gl.IMGV_COLOR)
    set_caption("Slideshow - imgv")
    (file, img_one_rect, img_one_name, img_one_file) = square_one(screen, file)
    (file, img_two_rect, img_two_name, img_two_file) = square_two(screen, file)
    (file, img_three_rect, img_three_name, img_three_file) = square_three(screen, file)
    (file, img_four_rect, img_four_name, img_four_file) = square_four(screen, file)
    if speed > 0:
        for i in range(speed):
            event = pygame.event.poll()
            pygame.time.wait(1)
            if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL,\
            K_p, K_PAUSE, K_TAB, K_SPACE, K_BACKSPACE):
                stopped_msg(screen)
                return (file, 1, img_one_file, img_two_file, img_three_file, img_four_file)
            if hit_key(event, K_p) or hit_key(event, K_PAUSE):
                pause(screen)
            pygame.time.delay(1000)
    return (file, 0, img_one_file, img_two_file, img_three_file, img_four_file)


def hover_fx(screen, img_one_name, img_two_name, img_three_name, img_four_name, img_one_rect, img_two_rect, img_three_rect, img_four_rect, cursor):
    dash = ' - '
    if img_one_rect.collidepoint(cursor):
        gl.OLD_CAP = img_one_name + " - imgv"
        if gl.OLD_CAP != get_caption()[0]:
            set_caption(gl.OLD_CAP)
    elif img_two_rect.collidepoint(cursor):
        gl.OLD_CAP = img_two_name + " - imgv"
        if gl.OLD_CAP != get_caption()[0]:
            set_caption(gl.OLD_CAP)
    elif img_three_rect.collidepoint(cursor):
        gl.OLD_CAP = img_three_name + " - imgv"
        if gl.OLD_CAP != get_caption()[0]:
            set_caption(gl.OLD_CAP)
    elif img_four_rect.collidepoint(cursor):
        gl.OLD_CAP = img_four_name + " - imgv"
        if gl.OLD_CAP != get_caption()[0]:
            set_caption(gl.OLD_CAP)
    else:
        gl.OLD_CAP = "Four at a time - imgv"
        if gl.OLD_CAP != get_caption()[0]:
            set_caption(gl.OLD_CAP)

