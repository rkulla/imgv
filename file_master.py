# list selection dialog code by Ryan Kulla, rkulla@gmail.com
import gl
import os
from input_box import ask
from img_screen import junk_rect, paint_screen
from cursor import hover_cursor
from show_message import show_message
from buttons import imgv_button, hover_button, close_button
from usr_event import left_click, right_click, middle_click, check_quit, hit_key
from pygame.display import update, set_caption, get_caption
import pygame.event, pygame.mouse, pygame.key, pygame.font
from pygame.locals import MOUSEMOTION, K_ESCAPE, K_SPACE, K_BACKSPACE, K_LCTRL, K_RCTRL


def command_file_master(screen, file_names, msg, down, button_op, disable_right_click, again):
    set_caption("Image Browser - imgv")
    screen_pause = place = marker = 0
    menu_items = []
    edit_rect = back_rect = forward_rect = sort_rect = junk_rect()
    (esc_rect, font) = close_button(screen)
    create_rect = imgv_button(screen, " Create New List ", 0, 18, "midtop")
    if len(file_names) < 1:
        my_string = ask(screen, "Create playlist first (Enter a name)")
        if my_string == None or my_string == []:
            return ([], [], [], []) # don't create a list
        if my_string != []: # create list
            if (len(my_string) > 0) and my_string != "\n":
                return (file_names, None, None, my_string)
    pygame.event.set_blocked(MOUSEMOTION)
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1)
        if screen_pause == 1:
            while 1:
                event = pygame.event.poll()
                pygame.time.wait(1)
                cursor = pygame.mouse.get_pos()
                hover_fx(screen, menu_items, cursor)
                hover_cursor(cursor, [esc_rect, edit_rect, sort_rect, back_rect, forward_rect, create_rect] + [x[0] for x in menu_items])
                if button_op:
                    hover_button(create_rect, cursor, screen, " Create New List ", 0, 18, "midtop")
                if (place + 1) < len(file_names):
                    hover_button(forward_rect, cursor, screen, " Next ", 10, 18, "topright")
                if (((place + 1) - gl.MAX_SCREEN_FILES) > 1):
                    hover_button(back_rect, cursor, screen, " Previous ", 10, 18, "topleft")
                if not gl.SORT_HIT:
                    hover_button(sort_rect, cursor, screen, " Sort ", 13, 42, "midtop")
                check_quit(event)
                if hit_key(event, K_ESCAPE):
                    return (None, None, None, None)
                if left_click(event):
                    if esc_rect.collidepoint(cursor):
                        return (None, None, None, None)
                if left_click(event):
                    for item in menu_items:
                        if item[0].collidepoint(cursor):
                            if pygame.mouse.get_pressed()[0] and (pygame.key.get_pressed()[K_LCTRL] or\
                               pygame.key.get_pressed()[K_RCTRL]):
                                return (file_names, item[1], "deleteit", None)
                            if again == "do again":
                                return (file_names, item[1], "do again", None)
                            return (file_names, item[1], menu_items, None)
                if right_click(event):
                    if not disable_right_click:
                        for item in menu_items:
                            if item[0].collidepoint(cursor):
                                if not os.path.isfile(gl.DATA_DIR + item[1]):
                                    if edit_rect != junk_rect():
                                        paint_screen(screen, gl.BLACK)
                                    edit_rect = show_message(
                                    "%s doesn't exist in %s" % (item[1], gl.DATA_DIR), "top", 9, ("bold", "transparent"))
                                else:
                                    return (None, item[1], "rclicked", None)
                if hit_key(event, K_SPACE) or right_click(event):
                    if not place >= len(file_names):
                        screen_pause = 0
                        marker = 0
                        menu_items = []
                        break
                if left_click(event):
                    if forward_rect.collidepoint(cursor):
                        if not place >= len(file_names):
                            screen_pause = 0
                            marker = 0
                            menu_items = []
                            break
                if hit_key(event, K_BACKSPACE) or middle_click(event):
                    if ((place - marker) > 0):
                        paint_screen(screen, gl.BLACK)
                        screen_pause = 0
                        place = place - (gl.MAX_SCREEN_FILES + marker)
                        marker = 0
                        menu_items = []
                        break
                if left_click(event):
                    if back_rect.collidepoint(cursor):
                        if ((place - marker) > 0):
                            paint_screen(screen, gl.BLACK)
                            screen_pause = 0
                            place = place - (gl.MAX_SCREEN_FILES + marker)
                            marker = 0
                            menu_items = []
                            break
                if left_click(event):
                    if sort_rect.collidepoint(cursor):
                        gl.SORT_HIT = 1
                        file_names = basename_sort(file_names)
                        (file_names, menu_items, screen_pause, place, marker, forward_rect, back_rect, sort_rect) = file_master(screen, file_names, place, marker, menu_items, msg, down, button_op)
                        screen_pause = place = marker = 0
                        menu_items = []
                        break
                if left_click(event):
                    if create_rect.collidepoint(cursor):
                        my_string = ask(screen, "Enter name of list")
                        if my_string != None:
                            if (len(my_string) > 0) and my_string != "\n":
                                return (file_names, None, menu_items, my_string)
        (file_names, menu_items, screen_pause, place, marker, forward_rect, back_rect, sort_rect) =\
            file_master(screen, file_names, place, marker, menu_items, msg, down, button_op)
        pygame.time.delay(5)


def file_master(screen, file_names, place, marker, menu_items, msg, down, button_op):
    paint_screen(screen, gl.BLACK)
    show_message(msg, down, 10, ("bold", "transparent"))
    font = pygame.font.Font(gl.FONT_NAME, 9)
    font.set_bold(1)
    (esc_rect, esc_font) = close_button(screen)
    font_height = font.size(file_names[0])[1]
    screen_height = screen.get_height()
    name_max = 16
    max_file_width = 116
    line = 65 # leave room at top of screen for other stuff
    col = 5
    count = 0
    back_rect = forward_rect = sort_rect = junk_rect()
    for name in file_names[place:]:
        count = count + 1
        place = place + 1
        marker = marker + 1
        if count >= gl.MAX_SCREEN_FILES or place >= len(file_names):
            ren_name = os.path.basename(name)
            if len(ren_name) > name_max:
                ren_name = ren_name[:name_max] + '...' # truncate
                if ren_name[-4:] == '....':
                    ren_name = ren_name[:-1] # 3 .'s are enough
            ren = font.render(ren_name, 1, gl.MSG_COLOR, gl.BLACK)
            if (place + 1) < len(file_names):
                forward_rect = imgv_button(screen, " Next ", 10, 18, "topright")
            if (((place + 1) - gl.MAX_SCREEN_FILES) > 1):
                back_rect = imgv_button(screen, " Previous ", 10, 18, "topleft")
            if not gl.SORT_HIT:
                sort_rect = imgv_button(screen, " Sort ", 13, 42, "midtop")
            ren_rect = ren.get_rect()
            ren_rect[0] = col
            ren_rect[1] = line
            menu_items.append((ren_rect, name))
            screen.blit(ren, ren_rect)
            update(ren_rect)
            return (file_names, menu_items, 1, place, marker, forward_rect, back_rect, sort_rect)
        ren_name = os.path.basename(name)
        if len(ren_name) > name_max:
            ren_name = ren_name[:name_max] + '...'
            if ren_name[-4:] == '....':
                ren_name = ren_name[:-1]
        ren = font.render(ren_name, 1, gl.MSG_COLOR, gl.BLACK)
        ren_rect = ren.get_rect()
        ren_rect[0] = col
        ren_rect[1] = line
        menu_items.append((ren_rect, name))
        screen.blit(ren, ren_rect)
        line = line + 12
        if (line + font_height) >= (screen_height - 15):
            line = 65
            col = col + max_file_width
        update(ren_rect)
    return (file_names, menu_items, 0, place, marker, forward_rect, back_rect, sort_rect)


def basename_sort(x):
    "sort a list of paths by their basename keeping their dirnames in tact"
    l = map(list, map(os.path.split, x))
    map(list.reverse, l)
    l = [os.path.join(path, fn) for fn, path in l]
    l.sort(lambda a, b: cmp(a.lower(), b.lower()))
    return l


def hover_fx(screen, x, cursor):
    flag = 0
    for it in x:
        if it[0].collidepoint(cursor):
            flag = 1
            gl.OLD_CAP = it[1] + " - imgv"
            if gl.OLD_CAP != get_caption()[0]:
                set_caption(gl.OLD_CAP)
            break
    if not flag:
        gl.OLD_CAP = "Image Browser - imgv"
        if gl.OLD_CAP != get_caption()[0]:
            set_caption(gl.OLD_CAP)

