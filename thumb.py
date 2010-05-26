# image thumbnail code by Ryan Kulla, rkulla@gmail.com
import gl
from img_screen import paint_screen, get_center, my_update_screen
from buttons import close_button
from usr_event import check_quit, hit_key, left_click, right_click, middle_click
from cursor import normal_cursor, wait_cursor, hover_cursor
from load_timers import start_timer, check_timer
from load_img import load_img
from show_message import show_message, truncate_name
from pygame.draw import line
import pygame.event, pygame.mouse, pygame.transform, pygame.time, pygame.font
from pygame.display import update, set_caption, get_caption, set_mode
from pygame.locals import K_ESCAPE, K_SPACE, K_BACKSPACE, MOUSEMOTION, K_t, K_b, K_n, K_p, K_PAUSE, RESIZABLE
from os.path import basename


def command_thumbs(screen, new_img, file, ns):
    normal_cursor()
    gl.THUMBING = 1

    screen_width = screen.get_width()
    if gl.THUMB_VAL.upper() == "AUTO" or gl.USING_THUMB_DEFAULT:
        gl.USING_THUMB_DEFAULT = 1
        if screen_width == 640:
            gl.THUMB_VAL = "85x90"
        elif screen_width == 800:
            gl.THUMB_VAL = "108x114"
        elif screen_width == 1024:
            gl.THUMB_VAL = "108x104"
        else:
            gl.THUMB_VAL = "100x100"

    if not gl.TOGGLE_FULLSCREEN_SET:
        screen = set_mode(screen.get_size()) # take away resize priviledges
    paint_screen(screen, gl.IMGV_COLOR)
    set_caption("imgv")
    orig_ns = ns
    (new_img, new_img, new_img, file, start) = thumbs_engine(screen, new_img, file, ns)
    if not gl.TOGGLE_FULLSCREEN_SET:
        screen = set_mode(screen.get_size(), RESIZABLE) # restore resize priviledges
    rect = get_center(screen, new_img)
    if start != orig_ns:
        ns = check_timer(start)
        my_update_screen(new_img, screen, rect, file, len(gl.files), ns)
    else:
        my_update_screen(new_img, screen, rect, file, len(gl.files))
    normal_cursor()
    gl.THUMBING = 0
    return (new_img, new_img, new_img, file, rect)


def thumbs_engine(screen, new_img, file, ns):
    screen_pause = 0
    SPACER = 5
    x = []
    place = file # start thumbing from current image position
    marker = 0
    (i, j) = (SPACER, SPACER)
    (esc_rect, close_font) = close_button(screen)
    font_size = 9
    font = pygame.font.Font(gl.FONT_NAME, font_size)
    pygame.event.set_blocked(MOUSEMOTION)
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1)
        check_quit(event)
        cursor = pygame.mouse.get_pos()
        hover_cursor(cursor, (esc_rect,))
        gl.PAUSED = 0 # critical
        if hit_key(event, K_ESCAPE):
            gl.ESCAPED = 1
            return (new_img, new_img, new_img, file, ns)
        if left_click(event):
            if esc_rect.collidepoint(cursor):
                gl.ESCAPED = 1
                break
        if hit_key(event, K_t) or hit_key(event, K_p) or hit_key(event, K_PAUSE):
            # pause
            set_caption("Thumbnails [Paused]")
            try:
                if place % gl.MAX_THUMBS_SET != 0:
                    # only pause if it's not the last thumbnail on the page
                    gl.PAUSED = 1
                    screen_pause = 1
            except:
                gl.PAUSED = 1
                screen_pause = 1
        if screen_pause == 1:
            normal_cursor()
            while 1:
                event = pygame.event.poll()
                pygame.time.wait(1)
                cursor = pygame.mouse.get_pos()
                (esc_rect, close_font) = close_button(screen)
                hover_fx(screen, x, cursor, marker)
                hover_cursor(cursor, [esc_rect] + [y[0] for y in x])
                if left_click(event):
                    if esc_rect.collidepoint(cursor):
                        gl.ESCAPED = 1
                        return (new_img, new_img, new_img, file, ns)
                    start = start_timer()
                    for item in x: # load clicked image:
                        if item[0].collidepoint(cursor):
                            wait_cursor()
                            new_img = load_img(item[1], screen)
                            file = gl.files.index(item[1])
                            return (new_img, new_img, new_img, file, start)
                check_quit(event)
                if hit_key(event, K_SPACE) or hit_key(event, K_t) or hit_key(event, K_n) or hit_key(event, K_p) or hit_key(event, K_PAUSE) or right_click(event):
                    if not place >= len(gl.files):
                        if not gl.PAUSED: # go to next thumb page:
                            paint_screen(screen, gl.IMGV_COLOR)
                            close_button(screen)
                            set_caption("Thumbnails [Paused]")
                            x = []
                            screen_pause = 0
                            marker = 0
                            break
                        # unpause:
                        gl.PAUSED = 0
                        screen_pause = 0
                        break
                if hit_key(event, K_BACKSPACE) or hit_key(event, K_b) or middle_click(event): 
                    # go back to previous thumb page, even if paused:
                    if ((place - marker) > 0):
                        i = j = SPACER
                        if gl.PAUSED:
                            gl.PAUSED = 0
                        paint_screen(screen, gl.IMGV_COLOR)
                        close_button(screen)
                        screen_pause = 0
                        place = place - (marker + gl.MAX_THUMBS)
                        marker = 0
                        x = []
                        break
                if hit_key(event, K_ESCAPE):
                    gl.ESCAPED = 1
                    return (new_img, new_img, new_img, file, ns)
        else:
            set_caption("Loading Thumbnails [%d] - imgv" % marker)
            (x, i, j, place, screen_pause, marker) = show_thumbs(screen, SPACER, x, i, j, place, marker, font, font_size)
        pygame.time.delay(5)
    return (new_img, new_img, new_img, file, ns)


def show_thumbs(screen, SPACER, x, i, j, place, marker, font, font_size):
    # show thumbnails with correct aspect ratio
    if place < len(gl.files):
        img_name = gl.files[place]
        img = load_img(img_name, screen, 0)
        (img_width, img_height) = img.get_size()

        splitval = None
        if gl.THUMB_VAL.find('x') != -1:
            splitval = 'x'
        elif gl.THUMB_VAL.find('X') != -1:
            splitval = 'X'
        if splitval != None:
            (square_width, square_height) = int(gl.THUMB_VAL.split(splitval)[0]), int(gl.THUMB_VAL.split(splitval)[1])

        small_img = img
        if img_width > img_height:
            if (not img_width < square_width and not img_height < square_height) or (img_width > square_width) or (img_height > square_height) or (img_width > square_width and img_height > square_height):
                r = float(img_width) / float(img_height)
                new_width = square_width
                new_height = int(new_width / r)
                scale_val = new_width, new_height
                if scale_val[0] > square_width or scale_val[1] > square_height:
                    scale_val = int(new_width / 1.32), int(new_height / 1.32) 
                if scale_val[0] > square_width or scale_val[1] > square_height:
                    if square_width >= 200 or square_height >= 200:
                        scale_val = int(scale_val[0] / 2), int(scale_val[1] / 2)
                small_img = pygame.transform.scale(img, scale_val)
        if img_width < img_height:
            if (not img_width < square_width and not img_height < square_height) or (img_width > square_width) or (img_height > square_height) or (img_width > square_width and img_height > square_height):
                r = float(img_height) / float(img_width)
                new_height = square_height
                new_width = int(new_height / r)
                scale_val = new_width, new_height
                if scale_val[0] > square_width or scale_val[1] > square_height:
                    scale_val = int(new_width / 2), int(new_height / 2) 
                else:
                    scale_val = new_width, new_height
                small_img = pygame.transform.scale(img, scale_val)
        if img_width == img_height: 
            if (not img_width < square_width and not img_height < square_height) or (img_width > square_width) or (img_height > square_height) or (img_width > square_width and img_height > square_height):
                r = float(img_width) / float(img_height)
                new_height = square_height
                new_width = square_width
                scale_val = new_width, new_height
                small_img = pygame.transform.scale(img, scale_val)
        (img_width, img_height) = small_img.get_size()

        if (i + square_width) >= screen.get_width():
            i = SPACER
            j = j + (square_height + SPACER)
        if (j + square_height) >= screen.get_height():
            i, j = SPACER, SPACER
            gl.MAX_THUMBS = marker # figure out how many thumbs fit on a page
            set_caption("imgv")
            if not gl.MAX_THUMBS_SET:
                gl.MAX_THUMBS_SET = gl.MAX_THUMBS
            return (x, i, j, place, 1, marker)

        # draw individual thumbnail backgrounds:
        paint_screen(screen, gl.THUMB_BG_COLOR_VAL, (i, j, square_width, square_height))

        if gl.THUMB_BORDER_VAL:
            # draw borders:
            left_line = line(screen, gl.THUMB_BORDER_COLOR, (i - 1, j - 1), (i - 1, square_height + j)) 
            right_line = line(screen, gl.THUMB_BORDER_COLOR, (i + square_width, j), (i + square_width, square_height + j))
            top_line = line(screen, gl.THUMB_BORDER_COLOR, (i, j - 1), ((i + square_width), j - 1)) 
            bottom_line = line(screen, gl.THUMB_BORDER_COLOR, (i, square_height + j), ((i + square_width), square_height + j)) 
            update(left_line), update(top_line), update(right_line), update(bottom_line)

        thumb_name = check_truncate(square_width, basename(img_name))
        wpos = i + ((square_width / 2) - (font.size(thumb_name)[0] / 2))

        small_img_rect = small_img.get_rect()
        small_img_rect[0] = i
        small_img_rect[1] = j
        x.append((small_img_rect, img_name))
        screen.blit(small_img, (i, j))
        update(small_img_rect)
        i = i + (square_width + SPACER)
        place = place + 1
        marker = marker + 1

        if gl.THUMB_STATUS_BARS:
            # display thumbnail's filename:
            show_message(screen, thumb_name, (wpos, j + square_height - 12), font_size, ("bold"))

    if place >= len(gl.files):
        return (x, 0, 0, place, 1, marker)
    return (x, i, j, place, 0, marker)


def check_truncate(width, name):
    if width <= 20:
        name = truncate_name(name, 1)
    if width <= 50 and width > 20:
        name = truncate_name(name, 5)
    elif width <= 100 and width > 50:
        name = truncate_name(name, 10)
    elif width <= 200 and width > 100:
        name = truncate_name(name, 15)
    else:
        name = truncate_name(name, 5)
    return name


def hover_fx(screen, x, cursor, marker):
    flag = 0
    for it in x:
        if it[0].collidepoint(cursor):
            flag = 1
            gl.OLD_CAP = it[1] + " [%d/%d] - imgv" % (gl.files.index(it[1]) + 1, len(gl.files))
            if gl.OLD_CAP != get_caption()[0]:
                set_caption(gl.OLD_CAP)
            break
    if not flag:
        if gl.PAUSED:
            gl.OLD_CAP = "%d Thumbnails [Paused] - imgv" % marker
        else:
            gl.OLD_CAP = "%d Thumbnails - imgv" % marker
        if gl.OLD_CAP != get_caption()[0]:
            set_caption(gl.OLD_CAP)

