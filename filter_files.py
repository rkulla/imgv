# image search/filter code by Ryan Kulla, rkulla@gmail.com
import gl
from os.path import basename
from show_message import show_message
from input_box import ask
from img_screen import paint_screen
from usr_event import check_quit, left_click, hit_key
from buttons import close_button
from cursor import hover_cursor
import pygame.event, pygame.font, pygame.mouse
from pygame.display import update, set_caption
from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION, KEYDOWN, K_ESCAPE, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9


def command_get_filter_info(screen):
    paint_screen(screen, gl.BLACK)
    set_caption("imgv")
    menu_items = []
    (esc_rect, font) = close_button(screen)
    
    show_message(screen, 'To build a search filter click as many options below as you need and then click "Done"', (21, 15), 12, ("bold"))
    show_message(screen, 'Example: If you don\'t want to view movies then just choose "Do not end with" and input:  .mpg, .mpeg', (21, 45), 12)
    show_message(screen, "Option number: _", "bottom", 12)
    (menu_items, filt_ops) = get_filter_info(screen, menu_items)
    pygame.event.set_blocked(MOUSEMOTION)
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(35)
        check_quit(event)
        if hit_key(event, K_ESCAPE):
            gl.ADDED_DIR_NUMS = 0
            return
        if event.type == KEYDOWN and event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9):
            if hit_key(event, K_1) or hit_key(event, K_KP1):
                do_startwith(screen)
            if hit_key(event, K_2) or hit_key(event, K_KP2):
                do_donot_startwith(screen)
            if hit_key(event, K_3) or hit_key(event, K_KP3):
                do_endwith(screen)
            if hit_key(event, K_4) or hit_key(event, K_KP4):
                do_donot_endwith(screen)
            if hit_key(event, K_5) or hit_key(event, K_KP5):
                do_contain(screen)
            if hit_key(event, K_6) or hit_key(event, K_KP6):
                do_donot_contain(screen)
            if hit_key(event, K_7) or hit_key(event, K_KP7):
                do_view_filter(screen)
            if hit_key(event, K_8) or hit_key(event, K_KP8):
                do_erase_filter(screen)
            if hit_key(event, K_9) or hit_key(event, K_KP9):
                gl.ADDED_DIR_NUMS = 0
                return
            break
        
        cursor = pygame.mouse.get_pos()

        if left_click(event):
            if esc_rect.collidepoint(cursor):
                gl.ADDED_DIR_NUMS = 0
                return 
        
        hover_fx(screen, menu_items, cursor, font)
        hover_cursor(cursor, [esc_rect] + [x[0] for x in menu_items])
        if gl.NOT_HOVERED:
            show_message(screen, "%sOption number: _%s" % (" " * 100, " " * 100), "bottom", 12)
            blank_fx(screen, 0)
        if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            for it in menu_items:
                if it[0].collidepoint(cursor) and it[1] in filt_ops:
                    if it[1] == "1) Start with":
                        do_startwith(screen)
                    if it[1] == "2) Do not start with":
                        do_donot_startwith(screen)
                    if it[1] == "3) End with":
                        do_endwith(screen)
                    if it[1] == "4) Do not end with":
                        do_donot_endwith(screen)
                    if it[1] == "5) Contain":
                        do_contain(screen)
                    if it[1] == "6) Do not contain":
                        do_donot_contain(screen)
                    if it[1] == "7) View filter":
                        do_view_filter(screen)
                    if it[1] == "8) Erase filter":
                        do_erase_filter(screen)
                    if it[1] == "9) Done":
                        gl.ADDED_DIR_NUMS = 0
                        return
                    break
            else:
                continue
            break
        gl.NOT_HOVERED = 1


def get_filter_info(screen, menu_items):
    filt_ops = ["1) Start with", "2) Do not start with", "3) End with", "4) Do not end with", "5) Contain", "6) Do not contain", "7) View filter", "8) Erase filter", "9) Done"]
    line = 95 # start position of menu from top of screen
    for op in filt_ops:
        font = pygame.font.Font(gl.FONT_NAME, 18)
        font.set_bold(1)
        ren = font.render(op, 1, gl.BLUE)
        ren_rect = ren.get_rect()
        ren_rect[0] = 20
        ren_rect[1] = line
        menu_items.append((ren_rect, op))
        screen.blit(ren, ren_rect)
        line = line + 30
        update(ren_rect)    
    return (menu_items, filt_ops)


def filter_files(file_list):
    # weee, no regex's. Gotta love Python
    new_list = []
    temp_list = []
    if "endwith" in gl.FILTER_COMMAND.keys():
        if new_list == []:
            new_list = file_list
        filt_split = convert_to_list("endwith")
        if len(filt_split) >= 1:
            for i in filt_split:
                temp_list = temp_list + [x for x in new_list if x.endswith(i)]
            new_list = temp_list
            temp_list = []
    if "notendwith" in gl.FILTER_COMMAND.keys():
        if new_list == []:
            new_list = file_list
        filt_split = convert_to_list("notendwith")
        if len(filt_split) >= 1:
            for i in filt_split:
                new_list = [x for x in new_list if not x.endswith(i)]
    if "startwith" in gl.FILTER_COMMAND.keys():
        if new_list == []: 
            new_list = file_list
        filt_split = convert_to_list("startwith")
        if len(filt_split) >= 1:
            for i in filt_split:
                temp_list = temp_list + [x for x in new_list if basename(x).startswith(i)]
            new_list = temp_list
            temp_list = []
    if "notstartwith" in gl.FILTER_COMMAND.keys():
        if new_list == []: 
            new_list = file_list
        filt_split = convert_to_list("notstartwith")
        if len(filt_split) >= 1:
            for i in filt_split:
                new_list = [x for x in new_list if not basename(x).startswith(i)]
    if "contain" in gl.FILTER_COMMAND.keys():
        if new_list == []:
            new_list = file_list
        filt_split = convert_to_list("contain")
        if len(filt_split) >= 1:
            for i in filt_split:
                temp_list = temp_list + [x for x in new_list if basename(x).find(i) != -1]
            new_list = temp_list
            temp_list = []
    if "notcontain" in gl.FILTER_COMMAND.keys():
        if new_list == []:
            new_list = file_list
        filt_split = convert_to_list("notcontain")
        if len(filt_split) >= 1:
            for i in filt_split:
                temp_list = temp_list + [x for x in new_list if basename(x).find(i) == -1]
            new_list = temp_list
            temp_list = []
    if new_list == []:
        new_list = [gl.NO_MATCHES_IMG]
    return new_list


def convert_to_list(name):
    # convert string to a split up list and allowing spaces between commas
    return [x.strip() for x in gl.FILTER_COMMAND[name].split(',')]


def view_filter(screen):
    paint_screen(screen, gl.BLACK)
    show_message(screen, "Current filter", "top", 20, ("underline", "bold"))
    show_message(screen, "Imgv will only display files whose filenames:", (5, 30), 15, ("bold"))
    line = 60
    for k in gl.FILTER_COMMAND.keys():
        font = pygame.font.Font(gl.FONT_NAME, 12)
        if k == "startwith":
            ren = font.render("Start with: %s" % gl.FILTER_COMMAND["startwith"], 1, (255, 255, 255), (0, 0, 0))
        if k == "notstartwith":
            ren = font.render("Do not start with:  %s" % gl.FILTER_COMMAND["notstartwith"], 1, (255, 255, 255), (0, 0, 0))
        if k == "endwith":
            ren = font.render("End with:  %s" % gl.FILTER_COMMAND["endwith"], 1, (255, 255, 255), (0, 0, 0))
        if k == "notendwith":
            ren = font.render("Do not end with:  %s" % gl.FILTER_COMMAND["notendwith"], 1, (255, 255, 255), (0, 0, 0))
        if k == "contain":
            ren = font.render("Contain:  %s" % gl.FILTER_COMMAND["contain"], 1, (255, 255, 255), (0, 0, 0))
        if k == "notcontain":
            ren = font.render("Do not contain:  %s" % gl.FILTER_COMMAND["notcontain"], 1, (255, 255, 255), (0, 0, 0))
        ren_rect = ren.get_rect()
        ren_rect[0] = 5
        ren_rect[1] = line
        screen.blit(ren, ren_rect)
        line = line + 30
        update(ren_rect)
    while 1:
        ev = pygame.event.wait()
        check_quit(ev)
        if ev.type == KEYDOWN or ev.type == MOUSEBUTTONDOWN:
            return


def do_startwith(screen):
    paint_screen(screen, gl.BLACK)
    show_message(screen, "Enter the string you want all image names to start with.", (10, 25), 12, ("bold"))
    show_message(screen, 'Example: Type red to view only images that start with the string'
                         ' "red" (i.e., red_car.jpg)', (10, 55), 12)
    show_message(screen, '(To input multiple strings separate them with commas)', (10, 75), 11)
    startwith_str = ask(screen, "Start with")
    if startwith_str != None:
        gl.FILTER_COMMAND["startwith"] = startwith_str
    command_get_filter_info(screen)


def do_donot_startwith(screen):
    paint_screen(screen, gl.BLACK)
    show_message(screen, "Enter the string that you do not want image names to start with.", (10, 25), 12, ("bold"))
    show_message(screen, 'Example: Type blue to view all images that do not start with the string'
                         ' "blue"', (10, 55), 12)
    show_message(screen, '(To input multiple strings separate them with commas)', (10, 75), 11)
    notstartwith_str = ask(screen, "Do not start with")
    if notstartwith_str != None:
        gl.FILTER_COMMAND["notstartwith"] = notstartwith_str
    command_get_filter_info(screen)


def do_endwith(screen):
    paint_screen(screen, gl.BLACK)
    show_message(screen, "Enter the string you want all image names to end with.", (10, 25), 12, ("bold"))
    show_message(screen, 'Example 1: Type .jpg to view all images that end with the string'
                         ' ".jpg" (i.e., dog.jpg)', (10, 55), 12)
    show_message(screen, 'Example 2: To load only jpegs and bitmaps, input:  .jpg, .jpeg, .bmp', (10, 75), 12)
    show_message(screen, '(To input multiple strings separate them with commas)', (10, 95), 11)
    endwith_str = ask(screen, "End with")
    if endwith_str != None:
        gl.FILTER_COMMAND["endwith"] = endwith_str
    command_get_filter_info(screen)


def do_donot_endwith(screen):
    paint_screen(screen, gl.BLACK)
    show_message(screen, "Enter the string that you do not want image names to end with.", (10, 25), 12, ("bold"))
    show_message(screen, 'Example 1: Type .jpg to view all images that do not end with the string'
                         ' ".jpg" (i.e., car.jpg)', (10, 55), 12)
    show_message(screen, 'Example 2: To only load images that are not GIFs, input:  .gif', (10, 75), 12)
    show_message(screen, '(To input multiple strings separate them with commas)', (10, 95), 11)
    notendwith_str = ask(screen, "Do not end with")
    if notendwith_str != None:
        gl.FILTER_COMMAND["notendwith"] = notendwith_str
    command_get_filter_info(screen)


def do_contain(screen):
    paint_screen(screen, gl.BLACK)
    show_message(screen, "Enter the string you want all image names to contain.", (10, 25), 12, ("bold"))
    show_message(screen, 'Example: Type red to view all images that contain the string'
                         ' "red" (i.e., my_red_car.jpg)', (10, 55), 12)
    show_message(screen, '(To input multiple strings separate them with commas)', (10, 75), 11)
    contain_str = ask(screen, "Contain")
    if contain_str != None:
        gl.FILTER_COMMAND["contain"] = contain_str
    command_get_filter_info(screen)


def do_donot_contain(screen):
    paint_screen(screen, gl.BLACK)
    show_message(screen, "Enter the string that you do not want image names to contain.", (10, 25), 12, ("bold"))
    show_message(screen, 'Example: Type blue to view only images that do not contain the string'
                         ' "blue" (i.e., my_blue_car.jpg)', (10, 55), 12)
    show_message(screen, '(To input multiple strings separate them with commas)', (10, 75), 11)
    notcontain_str = ask(screen, "Do not contain")
    if notcontain_str != None:
        gl.FILTER_COMMAND["notcontain"] = notcontain_str
    command_get_filter_info(screen)


def do_view_filter(screen):
    view_filter(screen)
    command_get_filter_info(screen)


def do_erase_filter(screen):
    gl.FILTER_COMMAND = {}
    command_get_filter_info(screen)


def hover_fx(screen, menu_items, cursor, font):
    for it in menu_items:
        if it[0].collidepoint(cursor):
            if it[1] == "1) Start with":
                blank_fx(screen, 1)
                gl.FIRST_RECT = index_fx(screen, it, font, "[What file names should start with]")
                break
            elif it[1] == "2) Do not start with":
                blank_fx(screen, 2)
                gl.SECOND_RECT = index_fx(screen, it, font, "[What file names should not start with]")
                break
            elif it[1] == "3) End with":
                blank_fx(screen, 3)
                gl.THIRD_RECT = index_fx(screen, it, font, "[What file names should end with]")
                break
            elif it[1] == "4) Do not end with":
                blank_fx(screen, 4)
                gl.FOURTH_RECT = index_fx(screen, it, font, "[What file names should not end with]")
                break
            elif it[1] == "5) Contain":
                blank_fx(screen, 5)
                gl.FIFTH_RECT = index_fx(screen, it, font, "[What file names should contain]")
                break
            elif it[1] == "6) Do not contain":
                blank_fx(screen, 6)
                gl.SIXTH_RECT = index_fx(screen, it, font, "[What file names should not contain]")
                break
            elif it[1] == "7) View filter":
                blank_fx(screen, 7)
                gl.SEVENTH_RECT = index_fx(screen, it, font, "[Your current filter]")
                break
            elif it[1] == "8) Erase filter":
                blank_fx(screen, 8)
                gl.EIGHTH_RECT = index_fx(screen, it, font, "[Erase your current filter]")
                break
            elif it[1] == "9) Done":
                blank_fx(screen, 9)
                gl.NINTH_RECT = index_fx(screen, it, font, "[Prepare to run filter]")
                break


def blank_fx(screen, row):
    l = [gl.FIRST_RECT, gl.SECOND_RECT, gl.THIRD_RECT, gl.FOURTH_RECT, gl.FIFTH_RECT, gl.SIXTH_RECT, gl.SEVENTH_RECT, gl.EIGHTH_RECT, gl.NINTH_RECT]
    for i in range(len(l)):
        if i != row - 1:
            show_message(screen, "  ", l[i], 12, ("bold")) # erase effect from non-hovered items
            

def index_fx(screen, it, font, msg):
    gl.NOT_HOVERED = 0
    fxpos = (it[0][0] - 10, it[0][1] + (font.size(it[1])[1] / 2) - 10, it[0][2], it[0][3])
    show_message(screen, ".", fxpos, 16, ("bold"))
    show_message(screen, "%s%s%s" % (" " * 100, msg, " " * 100), "bottom", 12)
    return fxpos

