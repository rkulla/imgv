# imgv editing options code by Ryan Kulla, rkulla@gmail.com
import gl
from wallpaper import windows_wallpaper, unix_wallpaper
from buttons import close_button
from input_box import ask
from rm_img import command_delete_img
from cfg import get_config_val
from load_img import load_img
from show_message import show_message
from confirm import get_confirmation
from img_screen import get_center, my_update_screen, paint_screen
from usr_event import check_quit, hit_key, left_click
from cursor import wait_cursor, hover_cursor
from sys import platform
import os
from pygame.display import update, set_caption, iconify, set_gamma#, set_mode#
import pygame.font, pygame.event, pygame.mouse
from pygame.locals import K_ESCAPE, MOUSEBUTTONDOWN, MOUSEMOTION, KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_RETURN, K_SPACE, K_1, K_2, K_3, K_4, K_KP1, K_KP2, K_KP3, K_KP4, RESIZABLE, VIDEORESIZE


def command_edit_menu(screen, file, new_img, rect):
    menu_items = []
    paint_screen(screen, gl.BLACK)
    (esc_rect, font) = close_button(screen)
    show_message(screen, "%s" % os.path.basename(gl.files[file]), "top", 12, "bold")
    show_message(screen, "Option number: _", "bottom", 12)
    pygame.event.set_blocked(MOUSEMOTION)
    (menu_items, men_ops) = edit_menu(screen, file, menu_items)
    while 1:
       event = pygame.event.poll()
       pygame.time.wait(1)
       check_quit(event)
       cursor = pygame.mouse.get_pos()
       hover_fx(screen, menu_items, men_ops, cursor, font)
       hover_cursor(cursor, [esc_rect] + [x[0] for x in menu_items])
       if gl.NOT_HOVERED:
           show_message(screen, "%sOption number: _%s" % (" " * 100, " " * 100), "bottom", 12)
           blank_fx(screen, -1)

       if hit_key(event, K_ESCAPE):
           gl.USING_SCROLL_MENU = 0
           update_edit_screen(screen, file, new_img)
           return (new_img, new_img, new_img, file, rect)
       if left_click(event):
           if esc_rect.collidepoint(cursor):
               gl.USING_SCROLL_MENU = 0
               update_edit_screen(screen, file, new_img)
               return (new_img, new_img, new_img, file, rect)

       if event.type == KEYDOWN and event.key in (K_1, K_2, K_3, K_4, K_KP1, K_KP2, K_KP3, K_KP4):
           if hit_key(event, K_1) or hit_key(event, K_KP1):
               (new_img, img, refresh_img, file, rect) = do_delete_image(screen, new_img, file, rect)
               paint_screen(screen, gl.BLACK)
               (menu_items, men_ops) = edit_menu(screen, file, menu_items)
           if hit_key(event, K_2) or hit_key(event, K_KP2):
               do_set_wallpaper(screen, file, new_img, rect)
               paint_screen(screen, gl.BLACK)
               (menu_items, men_ops) = edit_menu(screen, file, menu_items)
           if hit_key(event, K_3) or hit_key(event, K_KP3):
                if gl.EXTERNAL_EDITOR not in ('"None"', '"none"', '"NONE"', ''):
                    do_external_viewer(screen, file, new_img)
                paint_screen(screen, gl.BLACK)
                (menu_items, men_ops) = edit_menu(screen, file, menu_items)
           if hit_key(event, K_4) or hit_key(event, K_KP4):
               preferences(screen)
               (menu_items, men_ops) = edit_menu(screen, file, menu_items)

       if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
           for it in menu_items:
               if it[0].collidepoint(cursor) and it[1] in men_ops:
                   if it[1] == "1) Delete image":
                       (new_img, new_img, new_img, file, rect) = do_delete_image(screen, new_img, file, rect)
                       paint_screen(screen, gl.BLACK)
                       (menu_items, men_ops) = edit_menu(screen, file, menu_items)
                       break
                   if it[1] == "2) Set as wallpaper":
                       do_set_wallpaper(screen, file, new_img, rect)
                       paint_screen(screen, gl.BLACK)
                       (menu_items, men_ops) = edit_menu(screen, file, menu_items)
                       break
                   if it[1] == "3) Open in external viewer":
                        do_external_viewer(screen, file, new_img)
                        paint_screen(screen, gl.BLACK)
                        (menu_items, men_ops) = edit_menu(screen, file, menu_items)
                        break
                   if it[1] == "4) Preferences":
                       preferences(screen)
                       (menu_items, men_ops) = edit_menu(screen, file, menu_items)
                       break
                   return (new_img, new_img, new_img, file, rect)
       gl.NOT_HOVERED = 1
    return (new_img, new_img, new_img, file, rect)


def do_delete_image(screen, new_img, file, rect):
    fn = gl.files[file]
    answer = get_confirmation(screen, "Delete %s? [y/n]" % os.path.basename(fn))
    if answer == "yes":
        (new_img, img, refresh_img, file, rect) = command_delete_img(fn, new_img, screen, file, rect)
    return (new_img, new_img, new_img, file, rect)


def do_set_wallpaper(screen, file, new_img, rect):
    wait_cursor()
    if platform == 'win32':
        windows_wallpaper(file)
    else:
        unix_wallpaper(file)
    update_edit_screen(screen, file, new_img)


def do_external_viewer(screen, file, new_img):
    wait_cursor()
    iconify() # minimize imgv to avoid ugliness
    cmd = "%s %s" % (gl.EXTERNAL_EDITOR, gl.files[file])
    try:
        os.system(cmd)
    except:
        pass
    update_edit_screen(screen, file, new_img)


def do_gamma(screen):
    paint_screen(screen, gl.BLACK)
    show_message(screen, "Set the RGB gamma values on the display hardware while imgv is running.", 20, 13, ("bold"))
    show_message(screen, "Valid values are 0.3 to 4.4.  1.0 is the default. Higher than 1.0 = brighter. Lower than 1.0 = darker.", 40, 12)
    gl.CURRENT_GAMMA = new_gamma = ask(screen, "New gamma value")
    return new_gamma


def edit_menu(screen, file, menu_items):
    font = pygame.font.Font(gl.FONT_NAME, 18)
    font.set_bold(1)
    men_ops = ["1) Delete image", "2) Set as wallpaper", "3) Open in external viewer", "4) Preferences"]
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
    close_button(screen)
    return (menu_items, men_ops)


def update_edit_screen(screen, file, new_img):
    rect = get_center(screen, new_img)
    my_update_screen(new_img, screen, rect, file)


def hover_fx(screen, menu_items, men_ops, cursor, font):
    for it in menu_items:
        if it[0].collidepoint(cursor):
            if it[1] == men_ops[0]:
                blank_fx(screen, 0)
                gl.FIRST_RECT = index_fx(screen, it, font, "Delete image off disk")
                break
            elif it[1] == men_ops[1]:
                blank_fx(screen, 1)
                gl.SECOND_RECT = index_fx(screen, it, font, "Set image as desktop wallpaper")
                break
            elif it[1] == men_ops[2]:
                if gl.EXTERNAL_EDITOR in ('"None"', '"none"', '"NONE"', ''):
                    viewer = "No viewer specified"
                else:
                    viewer = os.path.basename(gl.EXTERNAL_EDITOR) # extract program name from path:
                    viewer = viewer[:viewer.rfind('.')] # take out file extention
                blank_fx(screen, 2)
                gl.THIRD_RECT = index_fx(screen, it, font, viewer)
                break
            elif it[1] == men_ops[3]:
                blank_fx(screen, 3)
                gl.FOURTH_RECT = index_fx(screen, it, font, "imgv options")
                break


def blank_fx(screen, row):
    l = [gl.FIRST_RECT, gl.SECOND_RECT, gl.THIRD_RECT, gl.FOURTH_RECT]
    for i in range(len(l)):
        if i != row:
            show_message(screen, "  ", l[i], 12, ("bold")) # erase effect from non-hovered items


def index_fx(screen, it, font, msg):
    gl.NOT_HOVERED = 0
    fxpos = (it[0][0] - 10, it[0][1] + (font.size(it[1])[1] / 2) - 10, it[0][2], it[0][3])
    show_message(screen, ".", fxpos, 16, ("bold"))
    show_message(screen, "%s%s%s" % (" " * 100, msg, " " * 100), "bottom", 12)
    return fxpos


def preferences(screen):
    paint_screen(screen, gl.BLACK)
    set_caption("imgv preferences")
    font_size = 12
    font = pygame.font.Font(gl.FONT_NAME, font_size)
    (esc_rect, font) = close_button(screen)
    pref_items = print_preferences(screen)

    (transparent_text_crect, transparent_text_ucrect, main_statusbar_crect, main_statusbar_ucrect, four_statusbars_crect, four_statusbars_ucrect, exif_statusbar_crect, exif_statusbar_ucrect, thumb_statusbars_crect, thumb_statusbars_ucrect, image_border_crect, image_border_ucrect, fit_image_rect, dirnum_colors_crect, dirnum_colors_ucrect, screen_bgcolor_rect, lock_zoom_crect, lock_zoom_ucrect, wrap_crect, wrap_ucrect, wrap_slideshow_crect, wrap_slideshow_ucrect, start_fullscreen_crect, start_fullscreen_ucrect, thumb_border_crect, thumb_border_ucrect, show_movies_crect, show_movies_ucrect, font_color_rect, font_bgcolor_rect, img_border_color_rect, thumb_border_color_rect, thumb_bgcolor_rect, four_divcolor_rect, button_bgcolor_rect, button_hover_color_rect, button_textcolor_rect, button_texthovercolor_rect, close_button_color_rect, gamma_rect, winsize_rect, thumbsize_rect, transeffect_rect, startdir_rect, external_editor_rect, fit_slideshow_rect, passwd_rect) = pref_options(screen)

    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1)
        check_quit(event)
        cursor = pygame.mouse.get_pos()
        prefs_hover_fx(screen, pref_items, cursor, font)

        hover_cursor(cursor, [esc_rect, transparent_text_crect, transparent_text_ucrect, main_statusbar_crect, main_statusbar_ucrect, four_statusbars_crect, four_statusbars_ucrect, exif_statusbar_crect, exif_statusbar_ucrect, thumb_statusbars_crect, thumb_statusbars_ucrect, image_border_crect, image_border_ucrect, fit_image_rect, dirnum_colors_crect, dirnum_colors_ucrect, screen_bgcolor_rect, lock_zoom_crect, lock_zoom_ucrect, wrap_crect, wrap_ucrect, wrap_slideshow_crect, wrap_slideshow_ucrect, start_fullscreen_crect, start_fullscreen_ucrect, thumb_border_crect, thumb_border_ucrect, show_movies_crect, show_movies_ucrect, font_color_rect, font_bgcolor_rect, img_border_color_rect, thumb_border_color_rect, thumb_bgcolor_rect, four_divcolor_rect, button_bgcolor_rect, button_hover_color_rect, button_textcolor_rect, button_texthovercolor_rect, close_button_color_rect, gamma_rect, winsize_rect, thumbsize_rect, transeffect_rect, startdir_rect, external_editor_rect, fit_slideshow_rect, passwd_rect])

        if gl.NOT_HOVERED:
            show_message(screen, "%s%s" % (" " * 100, " " * 100), "bottom", 12, ("transparent"))
            prefs_blank_fx(screen, -1)
        if hit_key(event, K_ESCAPE):
            gl.ESCAPED = 1
            paint_screen(screen, gl.BLACK)
            return
        if left_click(event):
            if esc_rect.collidepoint(cursor):
                gl.ESCAPED = 1
                paint_screen(screen, gl.BLACK)
                return
            if transparent_text_ucrect.collidepoint(cursor):
                gl.TOGGLE_TRANSPARENT ^= 1
                write_cfg("TRANSPARENT_TEXT")
            if main_statusbar_ucrect.collidepoint(cursor):
                gl.TOGGLE_STATUS_BAR ^= 1
                write_cfg("MAIN_STATUS_BAR")
            if four_statusbars_ucrect.collidepoint(cursor):
                gl.FOUR_STATUS_BARS ^= 1
                write_cfg("FOUR_AT_A_TIME_STATUS_BARS")
            if exif_statusbar_ucrect.collidepoint(cursor):
                gl.ON_FLY_EXIF_STATUS_BAR ^= 1
                write_cfg("ON_THE_FLY_EXIF_STATUS_BAR")
            if thumb_statusbars_ucrect.collidepoint(cursor):
                gl.THUMB_STATUS_BARS ^= 1
                write_cfg("THUMBNAIL_STATUS_BARS")
            if image_border_ucrect.collidepoint(cursor):
                gl.IMG_BORDER ^= 1
                write_cfg("IMAGE_BORDER")
            if lock_zoom_ucrect.collidepoint(cursor):
                gl.PERSISTENT_ZOOM_VAL ^= 1
                write_cfg("PERSISTENT_ZOOM")
            if wrap_ucrect.collidepoint(cursor):
                gl.WRAP ^= 1
                write_cfg("WRAP")
            if wrap_slideshow_ucrect.collidepoint(cursor):
                gl.WRAP_SLIDESHOW ^= 1
                write_cfg("WRAP_SLIDESHOW")
            if start_fullscreen_ucrect.collidepoint(cursor):
                gl.START_FULLSCREEN ^= 1
                write_cfg("FULLSCREEN")
            if thumb_border_ucrect.collidepoint(cursor):
                gl.THUMB_BORDER_VAL ^= 1
                write_cfg("THUMB_BORDER")
            if show_movies_ucrect.collidepoint(cursor):
                gl.MOVIES_VAL ^= 1
                show_message(screen, "(You must restart imgv for this change to take effect)", (375, 204), 10, ("bold", "transparent"))
                write_cfg("MOVIES")
            if fit_image_rect.collidepoint(cursor):
                paint_screen(screen, gl.BLACK)
                show_message(screen, "Enter an option letter and press enter", (15, 20), 13, ("bold", "transparent"))
                show_message(screen, "A = Fit nothing.", (15, 60), 13, ("bold", "transparent"))
                show_message(screen, "B = Fit only large images to the window.", (15, 80), 13, ("bold", "transparent"))
                show_message(screen, "C = Fit all images to the window. (both in normal mode and Four-at-a-Time mode)", (15, 100), 13, ("bold", "transparent"))
                show_message(screen, "D = Fit the window to images.", (15, 120), 13, ("bold", "transparent"))
                answer = ask(screen, "Option")
                if answer != None and answer in ('a','A', 'b','B', 'c','C', 'd','D'):
                    dmap = {'a':0, 'b':1, 'c':2, 'd':3}
                    gl.FIT_IMAGE_VAL = dmap[answer.lower()]
                    write_cfg("FIT_IMAGE", str(gl.FIT_IMAGE_VAL))
                clean_prefs(screen)
            if fit_slideshow_rect.collidepoint(cursor):
                paint_screen(screen, gl.BLACK)
                show_message(screen, "Enter an option letter and press enter", (15, 20), 13, ("bold", "transparent"))
                show_message(screen, "A = Fit nothing.", (15, 60), 13, ("bold", "transparent"))
                show_message(screen, "B = Fit only large images to the window.", (15, 80), 13, ("bold", "transparent"))
                show_message(screen, "C = Fit all images to the window. (both in normal mode and Four-at-a-Time mode)", (15, 100), 13, ("bold", "transparent"))
                show_message(screen, "D = Fit the window to images.", (15, 120), 13, ("bold", "transparent"))
                answer = ask(screen, "Option")
                if answer != None and answer in ('a','A', 'b','B', 'c','C', 'd','D'):
                    dmap = {'a':0, 'b':1, 'c':2, 'd':3}
                    gl.FIT_IMAGE_SLIDESHOW_VAL = dmap[answer.lower()]
                    write_cfg("FIT_IMAGE_SLIDESHOW", str(gl.FIT_IMAGE_SLIDESHOW_VAL))
                clean_prefs(screen)
            if gamma_rect.collidepoint(cursor):
                new_gamma = do_gamma(screen)
                if new_gamma != None:
                    try:
                        set_gamma(float(new_gamma))
                    except:
                        print 'invalid gamma value: %s' % new_gamma
                clean_prefs(screen)
            if dirnum_colors_ucrect.collidepoint(cursor):
                gl.DIRNUM_COLORS ^= 1
                write_cfg("COLOR_DIRECTORY_NUMBERS")
            if screen_bgcolor_rect.collidepoint(cursor):
                answer = color_msg(screen, "Set this to the color you want the background in imgv to be. (Default is BLACK)")
                (gl.IMGV_COLOR, cfg_str) = color_change(answer, gl.IMGV_COLOR)
                color_clean(screen, "IMGV_COLOR", cfg_str)
            if font_color_rect.collidepoint(cursor):
                answer = color_msg(screen, "Set this to the font color you want. (Default is WHITE)")
                (gl.MSG_COLOR, cfg_str) = color_change(answer, gl.MSG_COLOR)
                gl.MENU_COLOR = gl.MSG_COLOR
                color_clean(screen, "FONT_COLOR", cfg_str)
            if font_bgcolor_rect.collidepoint(cursor):
                answer = color_msg(screen, "Font background color you want. (Default is BLACK)")
                (gl.FONT_BG, cfg_str) = color_change(answer, gl.FONT_BG)
                gl.MENU_COLOR = gl.MSG_COLOR
                color_clean(screen, "FONT_BGCOLOR", cfg_str)
            if img_border_color_rect.collidepoint(cursor):
                answer = color_msg(screen, "Set this to the color you want the image border to be when it's activated. (Default is LIGHT_GREEN)")
                (gl.IMG_BORDER_COLOR, cfg_str) = color_change(answer, gl.IMG_BORDER_COLOR)
                color_clean(screen, "IMAGE_BORDER_COLOR", cfg_str)
            if thumb_border_color_rect.collidepoint(cursor):
                answer = color_msg(screen, "Set this to the color you want the image divider to be in Four-at-a-Time mode. (Default is WHITE)")
                (gl.THUMB_BORDER_COLOR, cfg_str) = color_change(answer, gl.THUMB_BORDER_COLOR)
                color_clean(screen, "THUMB_BORDER_COLOR", cfg_str)
            if thumb_bgcolor_rect.collidepoint(cursor):
                answer = color_msg(screen, "Set this to the color you want the background of individual thumbnails to be. (Default is BLACK)")
                (gl.THUMB_BG_COLOR_VAL, cfg_str) = color_change(answer, gl.THUMB_BG_COLOR_VAL)
                color_clean(screen, "THUMB_BG_COLOR", cfg_str)
            if four_divcolor_rect.collidepoint(cursor):
                answer = color_msg(screen, "Set this to the color you want the image divider to be in Four-at-a-Time mode. (Default is WHITE)")
                (gl.FOUR_DIV_COLOR, cfg_str) = color_change(answer, gl.FOUR_DIV_COLOR)
                color_clean(screen, "FOUR_AT_A_TIME_DIVIDER_COLOR", cfg_str)
            if button_bgcolor_rect.collidepoint(cursor):
                answer = color_msg(screen, "Background color of buttons. (Default is IMGV_LOGO_BLUE)")
                (gl.BUTTON_BGCOLOR, cfg_str) = color_change(answer, gl.BUTTON_BGCOLOR)
                color_clean(screen, "BUTTON_BGCOLOR", cfg_str)
            if button_hover_color_rect.collidepoint(cursor):
                answer = color_msg(screen, "Color of buttons when your mouse cursor hovers over them. (Default is SKY_BLUE)")
                (gl.BUTTON_HOVERCOLOR, cfg_str) = color_change(answer, gl.BUTTON_HOVERCOLOR)
                color_clean(screen, "BUTTON_HOVERCOLOR", cfg_str)
            if button_textcolor_rect.collidepoint(cursor):
                answer = color_msg(screen, "Color of text on buttons. (Default is BLACK)")
                (gl.BUTTON_TEXTCOLOR, cfg_str) = color_change(answer, gl.BUTTON_TEXTCOLOR)
                color_clean(screen, "BUTTON_TEXTCOLOR", cfg_str)
            if button_texthovercolor_rect.collidepoint(cursor):
                answer = color_msg(screen, "Color of text on buttons when mouse cursor hovers over them. (Default is BLACK)")
                (gl.BUTTON_TEXTHOVERCOLOR, cfg_str) = color_change(answer, gl.BUTTON_TEXTHOVERCOLOR)
                color_clean(screen, "BUTTON_TEXTHOVERCOLOR", cfg_str)
            if close_button_color_rect.collidepoint(cursor):
                answer = color_msg(screen, "Color of the close/cancel buttons, the 'X' in the top/right corner of the screen. (Default is SADDLE_BROWN)")
                (gl.CLOSE_BUTTONCOLOR, cfg_str) = color_change(answer, gl.CLOSE_BUTTONCOLOR)
                color_clean(screen, "CLOSE_BUTTONCOLOR", cfg_str)
            if winsize_rect.collidepoint(cursor):
                paint_screen(screen, gl.BLACK)
                show_message(screen, "Default Window Size or resolution of imgv (in the format: width x height. Default is: 800x600)", (15, 80), 13, ("bold", "transparent"))
                answer = ask(screen, "New window size")
                if answer != None:
                    x = None
                    if answer.find('x') != -1:
                        x = 'x'
                    elif answer.find('X') != -1:
                        x = 'X'
                    if x != None:
                        gl.IMGV_RESOLUTION = int(answer.split(x)[0]), int(answer.split(x)[1])
                    write_cfg("IMGV_WINDOW_SIZE", answer)
                clean_prefs(screen)
            if thumbsize_rect.collidepoint(cursor):
                paint_screen(screen, gl.BLACK)
                show_message(screen, "The size you set will be used as the size of the thumbnail border/box, not the images themselves.", (15, 60), 13, ("bold", "transparent"))
                show_message(screen, "Values are in the format: width x height. Example: 100x100", (15, 100), 13, ("transparent"))
                show_message(screen, "To have imgv choose the best thumb size for a given default screen size use the default value of: AUTO", (15, 120), 13, ("transparent"))
                answer = ask(screen, "New thumbnail size")
                if answer != None:
                    gl.THUMB_VAL = answer
                    write_cfg("THUMB_SIZE", answer)
                clean_prefs(screen)
            if transeffect_rect.collidepoint(cursor):
                paint_screen(screen, gl.BLACK)
                show_message(screen, "Valid values: NONE (default), MELT, FADE_IN", (15, 60), 13, ("bold", "transparent"))
                show_message(screen, "You can also apply multiple effects by separating them with |'s such as: MELT|FADE_IN", (15, 90), 13, ("transparent"))
                answer = ask(screen, "Transitional effect")
                if answer != None:
                    gl.TRANS_FX = answer
                    write_cfg("TRANSITIONAL_EFFECT", answer)
                clean_prefs(screen)
            if startdir_rect.collidepoint(cursor):
                paint_screen(screen, gl.BLACK)
                show_message(screen, "Set this to an already existing directory that you want imgv to initially load images from.", (15, 60), 13, ("bold", "transparent"))
                if platform == 'win32':
                    show_message(screen, "For example: C:\photos\\", (15, 80), 13, ("transparent"))
                else:
                     show_message(screen, "For example: /home/photos/", (15, 80), 13, ("transparent"))
                show_message(screen, "Set to / (default) to have imgv load images from the root directory.", (15, 110), 13, ("transparent"))
                show_message(screen, "You an also specify a single image name.", (15, 150), 13, ("transparent"))
                show_message(screen, "For example: C:\pics\dog.jpg", (15, 170), 13, ("transparent"))
                answer = ask(screen, "Start directory")
                if answer != None:
                    gl.START_DIRECTORY_VAL = answer
                    write_cfg("START_DIRECTORY", answer)
                clean_prefs(screen)
            if external_editor_rect.collidepoint(cursor):
                paint_screen(screen, gl.BLACK)
                show_message(screen, "Path to an external image editing application (You must put quotes around the value)", (15, 60), 13, ("bold", "transparent"))
                show_message(screen, "For example, if you want to use Adobe Photoshop with imgv you might put:", (15, 80), 13, ("transparent"))
                show_message(screen, "\"C:\\Program Files\\Adobe\\Photoshop CS2\\Photoshop.exe\"", (15, 100), 13, ("transparent"))
                show_message(screen, "Set to \"None\" (default) if you don't need this feature.", (15, 130), 13, ("transparent"))
                answer = ask(screen, "External editor")
                if answer != None:
                    gl.EXTERNAL_EDITOR = answer
                    write_cfg("EXTERNAL_EDITOR", answer)
                clean_prefs(screen)
            if passwd_rect.collidepoint(cursor):
                paint_screen(screen, gl.BLACK)
                show_message(screen, "Set this to the password you want to be used in the 'Hide Image' feature.", (15, 60), 13, ("bold", "transparent"))
                show_message(screen, "It's case sensitive and don't use quotes.", (15, 90), 13, ("transparent"))
                show_message(screen, "Set to None (default) if you don't want to be prompted for a password.", (15, 110), 13, ("transparent"))
                answer = ask(screen, "New password")
                if answer != None:
                    gl.CORRECT_PASSWORD = answer
                    write_cfg("PASSWORD", answer)
                clean_prefs(screen)
            (transparent_text_crect, transparent_text_ucrect, main_statusbar_crect, main_statusbar_ucrect, four_statusbars_crect, four_statusbars_ucrect, exif_statusbar_crect, exif_statusbar_ucrect, thumb_statusbars_crect, thumb_statusbars_ucrect, image_border_crect, image_border_ucrect, fit_image_rect, dirnum_colors_crect, dirnum_colors_ucrect, screen_bgcolor_rect, lock_zoom_crect, lock_zoom_ucrect, wrap_crect, wrap_ucrect, wrap_slideshow_crect, wrap_slideshow_ucrect, start_fullscreen_crect, start_fullscreen_ucrect, thumb_border_crect, thumb_border_ucrect, show_movies_crect, show_movies_ucrect, font_color_rect, font_bgcolor_rect, img_border_color_rect, thumb_border_color_rect, thumb_bgcolor_rect, four_divcolor_rect, button_bgcolor_rect, button_hover_color_rect, button_textcolor_rect, button_texthovercolor_rect, close_button_color_rect, gamma_rect, winsize_rect, thumbsize_rect, transeffect_rect, startdir_rect, external_editor_rect, fit_slideshow_rect, passwd_rect) = pref_options(screen)
        gl.NOT_HOVERED = 1



def color_msg(screen, msg):
    paint_screen(screen, gl.BLACK)
    show_message(screen, msg, (15, 20), 13, ("bold", "transparent"))
    show_message(screen, "Valid colors: BLACK, WHITE, PURPLE, BLUE, IMGV_LOGO_BLUE, SKY_BLUE, SILVER, GREEN, LIGHT_GREEN,", (15, 50), 13, ("transparent"))
    show_message(screen, "SADDLE_BROWN, RED, ORANGE, YELLOW, DARK_SLATE_BLUE, DARK_SLATE_GRAY, MID_GRAY.", (15, 70), 13, ("transparent"))
    show_message(screen, "You can also specify coma separated RGB color values in the format: n,n,n (where n is a number from 0 to 255)", (15, 100), 13, ("transparent"))
    return ask(screen, "Color")


def color_clean(screen, what, cfg_str):
    write_cfg(what, cfg_str)
    clean_prefs(screen)


def clean_prefs(screen):
    paint_screen(screen, gl.BLACK)
    print_preferences(screen)


def color_change(answer, tochange):
    ret_color = tochange
    if answer != None and answer.find(',') != -1:
        answer = answer.split(',')
        if len(answer) >= 3:
            ret_color = (int(answer[0]), int(answer[1]), int(answer[2]))
            cfg_str = "%s,%s,%s" % (answer[0], answer[1], answer[2])
    elif answer != None and answer.upper() in gl.COLORS.keys():
        ret_color = gl.COLORS[answer.upper()]
        cfg_str = "%s,%s,%s" % (ret_color[0], ret_color[1], ret_color[2])
    else:
        cfg_str = "%s,%s,%s" % (tochange[0], tochange[1], tochange[2])
    return (ret_color, cfg_str)


def print_preferences(screen):
    font_size = 12
    font = pygame.font.Font(gl.FONT_NAME, font_size)
    row_sep = 16
    row = 11
    col = 20
    pref_items = []
    for op_msg in gl.PREF_LIST:
        ren_name = op_msg[0]
        ren = font.render(ren_name, 1, gl.WHITE)
        ren_rect = ren.get_rect()
        ren_rect[0] = col
        ren_rect[1] = row
        pref_items.append((ren_rect, op_msg[0]))
        screen.blit(ren, ren_rect)
        row += row_sep
        update(ren_rect)
    return pref_items


def prefs_hover_fx(screen, pref_items, cursor, font):
    for it in pref_items:
        if it[0].collidepoint(cursor):
            if it[1] == gl.PREF_LIST[0][0]:
                prefs_blank_fx(screen, 0)
                gl.FIRST_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[0][1])
                break
            elif it[1] == gl.PREF_LIST[1][0]:
                prefs_blank_fx(screen, 1)
                gl.SECOND_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[1][1])
                break
            elif it[1] == gl.PREF_LIST[2][0]:
                prefs_blank_fx(screen, 2)
                gl.THIRD_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[2][1])
                break
            elif it[1] == gl.PREF_LIST[3][0]:
                prefs_blank_fx(screen, 3)
                gl.FOURTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[3][1])
                break
            elif it[1] == gl.PREF_LIST[4][0]:
                prefs_blank_fx(screen, 4)
                gl.FIFTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[4][1])
                break
            elif it[1] == gl.PREF_LIST[5][0]:
                prefs_blank_fx(screen, 5)
                gl.SIXTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[5][1])
            elif it[1] == gl.PREF_LIST[6][0]:
                prefs_blank_fx(screen, 6)
                gl.SEVENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[6][1])
            elif it[1] == gl.PREF_LIST[7][0]:
                prefs_blank_fx(screen, 7)
                gl.EIGHTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[7][1])
            elif it[1] == gl.PREF_LIST[8][0]:
                prefs_blank_fx(screen, 8)
                gl.NINTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[8][1])
            elif it[1] == gl.PREF_LIST[9][0]:
                prefs_blank_fx(screen, 9)
                gl.TENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[9][1])
            elif it[1] == gl.PREF_LIST[10][0]:
                prefs_blank_fx(screen, 10)
                gl.ELEVENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[10][1])
            elif it[1] == gl.PREF_LIST[11][0]:
                prefs_blank_fx(screen, 11)
                gl.TWELFTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[11][1])
            elif it[1] == gl.PREF_LIST[12][0]:
                prefs_blank_fx(screen, 12)
                gl.THIRTEENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[12][1])
            elif it[1] == gl.PREF_LIST[13][0]:
                prefs_blank_fx(screen, 13)
                gl.FOURTEENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[13][1])
            elif it[1] == gl.PREF_LIST[14][0]:
                prefs_blank_fx(screen, 14)
                gl.FIFTEENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[14][1])
            elif it[1] == gl.PREF_LIST[15][0]:
                prefs_blank_fx(screen, 15)
                gl.SIXTEENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[15][1])
            elif it[1] == gl.PREF_LIST[16][0]:
                prefs_blank_fx(screen, 16)
                gl.SEVENTEENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[16][1])
            elif it[1] == gl.PREF_LIST[17][0]:
                prefs_blank_fx(screen, 17)
                gl.EIGHTEENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[17][1])
            elif it[1] == gl.PREF_LIST[18][0]:
                prefs_blank_fx(screen, 18)
                gl.NINETEENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[18][1])
            elif it[1] == gl.PREF_LIST[19][0]:
                prefs_blank_fx(screen, 19)
                gl.TWENTIETH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[19][1])
            elif it[1] == gl.PREF_LIST[20][0]:
                prefs_blank_fx(screen, 20)
                gl.TWENTYFIRST_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[20][1])
            elif it[1] == gl.PREF_LIST[21][0]:
                prefs_blank_fx(screen, 21)
                gl.TWENTYSECOND_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[21][1])
            elif it[1] == gl.PREF_LIST[22][0]:
                prefs_blank_fx(screen, 22)
                gl.TWENTYTHIRD_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[22][1])
            elif it[1] == gl.PREF_LIST[23][0]:
                prefs_blank_fx(screen, 23)
                gl.TWENTYFOURTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[23][1])
            elif it[1] == gl.PREF_LIST[24][0]:
                prefs_blank_fx(screen, 24)
                gl.TWENTYFIFTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[24][1])
            elif it[1] == gl.PREF_LIST[25][0]:
                prefs_blank_fx(screen, 25)
                gl.TWENTYSIXTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[25][1])
            elif it[1] == gl.PREF_LIST[26][0]:
                prefs_blank_fx(screen, 26)
                gl.TWENTYSEVENTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[26][1])
            elif it[1] == gl.PREF_LIST[27][0]:
                prefs_blank_fx(screen, 27)
                gl.TWENTYEIGTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[27][1])
            elif it[1] == gl.PREF_LIST[28][0]:
                prefs_blank_fx(screen, 28)
                gl.TWENTYNINTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[28][1])
            elif it[1] == gl.PREF_LIST[29][0]:
                prefs_blank_fx(screen, 29)
                gl.THIRTIETH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[29][1])
            elif it[1] == gl.PREF_LIST[30][0]:
                prefs_blank_fx(screen, 30)
                gl.THIRTYFIRST_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[30][1])
            elif it[1] == gl.PREF_LIST[31][0]:
                prefs_blank_fx(screen, 31)
                gl.THIRTYSECOND_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[31][1])
            elif it[1] == gl.PREF_LIST[32][0]:
                prefs_blank_fx(screen, 32)
                gl.THIRTYTHIRD_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[32][1])
            elif it[1] == gl.PREF_LIST[33][0]:
                prefs_blank_fx(screen, 33)
                gl.THIRTYFOURTH_RECT = prefs_index_fx(screen, it, font, gl.PREF_LIST[33][1])


def prefs_blank_fx(screen, row):
    l = [gl.FIRST_RECT, gl.SECOND_RECT, gl.THIRD_RECT, gl.FOURTH_RECT, gl.FIFTH_RECT, gl.SIXTH_RECT, gl.SEVENTH_RECT, gl.EIGHTH_RECT, gl.NINTH_RECT, gl.TENTH_RECT, gl.ELEVENTH_RECT, gl.TWELFTH_RECT, gl.THIRTEENTH_RECT, gl.FOURTEENTH_RECT, gl.FIFTEENTH_RECT, gl.SIXTEENTH_RECT, gl.SEVENTEENTH_RECT, gl.EIGHTEENTH_RECT, gl.NINETEENTH_RECT, gl.TWENTIETH_RECT, gl.TWENTYFIRST_RECT, gl.TWENTYSECOND_RECT, gl.TWENTYTHIRD_RECT, gl.TWENTYFOURTH_RECT, gl.TWENTYFIFTH_RECT, gl.TWENTYSIXTH_RECT, gl.TWENTYSEVENTH_RECT, gl.TWENTYEIGTH_RECT, gl.TWENTYNINTH_RECT, gl.THIRTIETH_RECT, gl.THIRTYFIRST_RECT, gl.THIRTYSECOND_RECT, gl.THIRTYTHIRD_RECT, gl.THIRTYFOURTH_RECT]
    for i in range(len(l)):
        if i != row:
            show_message(screen, "  ", l[i], 12, ("bold", "transparent")) # Erase effect from non-hovered items


def prefs_index_fx(screen, it, font, msg):
    gl.NOT_HOVERED = 0
    fxpos = (it[0][0] - 10, it[0][1] + (font.size(it[1])[1] / 2) - 13, it[0][2], it[0][3])
    show_message(screen, ".", fxpos, 16, ("bold", "transparent"))
    show_message(screen, "%s%s%s" % (" " * 100, msg, " " * 100), "bottom", 12, ("transparent"))
    return fxpos


def pref_options(screen):
    yes_wpos = 280
    no_wpos = yes_wpos + 50
    cbox_wpos1 = yes_wpos + 30
    cbox_wpos2 = cbox_wpos1 + 47
    change_wpos = yes_wpos
    change_msg_wpos = change_wpos + 60

    # travel down printing each message option 16 pixels as at time (same value as row_sep in print_preferences())
    show_message(screen, "Yes:", (yes_wpos, 13), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 13), 10, ("transparent"))
    main_statusbar_crect, main_statusbar_ucrect = check_boxes(screen, (15, cbox_wpos1, cbox_wpos2), "main_statusbar")

    show_message(screen, "Yes", (yes_wpos, 29), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 29), 10, ("transparent"))
    four_statusbars_crect, four_statusbars_ucrect = check_boxes(screen, (31, cbox_wpos1, cbox_wpos2), "four_statusbars")

    show_message(screen, "Yes:", (yes_wpos, 45), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 45), 10, ("transparent"))
    exif_statusbar_crect, exif_statusbar_ucrect = check_boxes(screen, (47, cbox_wpos1, cbox_wpos2), "exif_statusbar")

    show_message(screen, "Yes:", (yes_wpos, 61), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 61), 10, ("transparent"))
    thumb_statusbars_crect, thumb_statusbars_ucrect = check_boxes(screen, (63, cbox_wpos1, cbox_wpos2), "thumb_statusbars")

    show_message(screen, "Yes:", (yes_wpos, 77), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 77), 10, ("transparent"))
    transparent_text_crect, transparent_text_ucrect = check_boxes(screen, (79, cbox_wpos1, cbox_wpos2), "transparent_text")

    show_message(screen, "Yes:", (yes_wpos, 93), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 93), 10, ("transparent"))
    image_border_crect, image_border_ucrect = check_boxes(screen, (95, cbox_wpos1, cbox_wpos2), "image_border")

    show_message(screen, "Yes:", (yes_wpos, 109), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 109), 10, ("transparent"))
    lock_zoom_crect, lock_zoom_ucrect = check_boxes(screen, (110, cbox_wpos1, cbox_wpos2), "lock_zoom")

    show_message(screen, "Yes:", (yes_wpos, 125), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 125), 10, ("transparent"))
    wrap_crect, wrap_ucrect = check_boxes(screen, (126, cbox_wpos1, cbox_wpos2), "wrap")

    show_message(screen, "Yes:", (yes_wpos, 141), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 141), 10, ("transparent"))
    wrap_slideshow_crect, wrap_slideshow_ucrect = check_boxes(screen, (142, cbox_wpos1, cbox_wpos2), "wrap_slideshow")

    show_message(screen, "Yes:", (yes_wpos, 157), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 157), 10, ("transparent"))
    start_fullscreen_crect, start_fullscreen_ucrect = check_boxes(screen, (158, cbox_wpos1, cbox_wpos2), "start_fullscreen")

    show_message(screen, "Yes:", (yes_wpos, 173), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 173), 10, ("transparent"))
    thumb_border_crect, thumb_border_ucrect = check_boxes(screen, (174, cbox_wpos1, cbox_wpos2), "thumb_border")

    show_message(screen, "Yes:", (yes_wpos, 189), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 189), 10, ("transparent"))
    dirnum_colors_crect, dirnum_colors_ucrect = check_boxes(screen, (190, cbox_wpos1, cbox_wpos2), "dirnum_colors")

    show_message(screen, "Yes:", (yes_wpos, 205), 10, ("transparent"))
    show_message(screen, "No:", (no_wpos, 205), 10, ("transparent"))
    show_movies_crect, show_movies_ucrect = check_boxes(screen, (206, cbox_wpos1, cbox_wpos2), "show_movies")

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 223, 12, 10))
    paint_screen(screen, gl.IMGV_COLOR, (change_msg_wpos+1, 224, 10, 8))
    screen_bgcolor_rect = change_box(screen, (224, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 239, 12, 10))
    paint_screen(screen, gl.MSG_COLOR, (change_msg_wpos+1, 240, 10, 8))
    font_color_rect = change_box(screen, (240, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 255, 12, 10))
    paint_screen(screen, gl.FONT_BG, (change_msg_wpos+1, 256, 10, 8))
    font_bgcolor_rect = change_box(screen, (256, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 271, 12, 10))
    paint_screen(screen, gl.IMG_BORDER_COLOR, (change_msg_wpos+1, 272, 10, 8))
    img_border_color_rect = change_box(screen, (272, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 287, 12, 10))
    paint_screen(screen, gl.THUMB_BORDER_COLOR, (change_msg_wpos+1, 288, 10, 8))
    thumb_border_color_rect = change_box(screen, (288, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 303, 12, 10))
    paint_screen(screen, gl.THUMB_BG_COLOR_VAL, (change_msg_wpos+1, 304, 10, 8))
    thumb_bgcolor_rect = change_box(screen, (304, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 320, 12, 10))
    paint_screen(screen, gl.FOUR_DIV_COLOR, (change_msg_wpos+1, 321, 10, 8))
    four_divcolor_rect = change_box(screen, (321, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 336, 12, 10))
    paint_screen(screen, gl.BUTTON_BGCOLOR, (change_msg_wpos+1, 337, 10, 8))
    button_bgcolor_rect = change_box(screen, (337, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 352, 12, 10))
    paint_screen(screen, gl.BUTTON_HOVERCOLOR, (change_msg_wpos+1, 353, 10, 8))
    button_hover_color_rect = change_box(screen, (353, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 368, 12, 10))
    paint_screen(screen, gl.BUTTON_TEXTCOLOR, (change_msg_wpos+1, 369, 10, 8))
    button_textcolor_rect = change_box(screen, (369, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 384, 12, 10))
    paint_screen(screen, gl.BUTTON_TEXTHOVERCOLOR, (change_msg_wpos+1, 385, 10, 8))
    button_texthovercolor_rect = change_box(screen, (385, change_wpos))

    paint_screen(screen, gl.WHITE, (change_msg_wpos, 400, 12, 10))
    paint_screen(screen, gl.CLOSE_BUTTONCOLOR, (change_msg_wpos+1, 401, 10, 8))
    close_button_color_rect = change_box(screen, (401, change_wpos))

    show_message(screen, "%s" % ('Fit nothing', 'Fit large images', 'Fit all images', 'Fit window to image')[gl.FIT_IMAGE_VAL], (change_msg_wpos, 416), 10, ("transparent"))
    fit_image_rect = change_box(screen, (417, change_wpos))

    show_message(screen, gl.CURRENT_GAMMA, (change_msg_wpos, 432), 10, ("transparent"))
    gamma_rect = change_box(screen, (433, change_wpos))

    show_message(screen, "%sx%s" % (gl.IMGV_RESOLUTION[0], gl.IMGV_RESOLUTION[1]), (change_wpos+60, 448), 10, ("transparent"))
    winsize_rect = change_box(screen, (449, change_wpos))

    show_message(screen, gl.THUMB_VAL, (change_wpos+60, 464), 10, ("transparent"))
    thumbsize_rect = change_box(screen, (465, change_wpos))

    show_message(screen, gl.TRANS_FX, (change_wpos+60, 480), 10, ("transparent"))
    transeffect_rect = change_box(screen, (481, change_wpos))

    show_message(screen, gl.START_DIRECTORY_VAL, (change_wpos+60, 496), 10, ("transparent"))
    startdir_rect = change_box(screen, (497, change_wpos))

    show_message(screen, gl.EXTERNAL_EDITOR, (change_wpos+60, 512), 10, ("transparent"))
    external_editor_rect = change_box(screen, (513, change_wpos))

    show_message(screen, "%s" % ('Fit nothing', 'Fit large images', 'Fit all images', 'Fit window to image')[gl.FIT_IMAGE_SLIDESHOW_VAL], (change_msg_wpos, 528), 10, ("transparent"))
    fit_slideshow_rect = change_box(screen, (529, change_wpos))

    if gl.CORRECT_PASSWORD.lower() == "none":
        show_message(screen, gl.CORRECT_PASSWORD , (change_msg_wpos, 544), 10, ("transparent"))
    else:
        show_message(screen, '*' * len(gl.CORRECT_PASSWORD), (change_msg_wpos, 544), 10, ("transparent"))
    passwd_rect = change_box(screen, (545, change_wpos))

    close_button(screen)

    return (transparent_text_crect, transparent_text_ucrect, main_statusbar_crect, main_statusbar_ucrect, four_statusbars_crect, four_statusbars_ucrect, exif_statusbar_crect, exif_statusbar_ucrect, thumb_statusbars_crect, thumb_statusbars_ucrect, image_border_crect, image_border_ucrect, fit_image_rect, dirnum_colors_crect, dirnum_colors_ucrect, screen_bgcolor_rect, lock_zoom_crect, lock_zoom_ucrect, wrap_crect, wrap_ucrect, wrap_slideshow_crect, wrap_slideshow_ucrect, start_fullscreen_crect, start_fullscreen_ucrect, thumb_border_crect, thumb_border_ucrect, show_movies_crect, show_movies_ucrect, font_color_rect, font_bgcolor_rect, img_border_color_rect, thumb_border_color_rect, thumb_bgcolor_rect, four_divcolor_rect, button_bgcolor_rect, button_hover_color_rect, button_textcolor_rect, button_texthovercolor_rect, close_button_color_rect, gamma_rect, winsize_rect, thumbsize_rect, transeffect_rect, startdir_rect, external_editor_rect, fit_slideshow_rect, passwd_rect)


def change_box(screen, positions):
    change_img = load_img(gl.CHANGE_BOX, screen, False)
    change_rect = change_img.get_rect()
    change_rect[0] = positions[1]
    change_rect[1] = positions[0]
    screen.blit(change_img, change_rect)
    update(change_rect)
    return change_rect


def check_boxes(screen, positions, opt):
    # positions[0]=hpos, positions[1]=checked_wpos, positions[2]=unchecked_wpos
    # draw checked box:
    checked_img = load_img(gl.CHECKED_BOX, screen, False)
    checked_rect = checked_img.get_rect()
    if opt == "transparent_text":
        checked_rect[0] = (positions[1], positions[2])[get_config_val("TRANSPARENT_TEXT")]
    elif opt == "main_statusbar":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("MAIN_STATUS_BAR")]
    elif opt == "four_statusbars":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("FOUR_AT_A_TIME_STATUS_BARS")]
    elif opt == "exif_statusbar":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("ON_THE_FLY_EXIF_STATUS_BAR")]
    elif opt == "thumb_statusbars":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("THUMBNAIL_STATUS_BARS")]
    elif opt == "image_border":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("IMAGE_BORDER")]
    elif opt == "dirnum_colors":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("COLOR_DIRECTORY_NUMBERS")]
    elif opt == "lock_zoom":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("PERSISTENT_ZOOM")]
    elif opt == "wrap":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("WRAP")]
    elif opt == "wrap_slideshow":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("WRAP_SLIDESHOW")]
    elif opt == "start_fullscreen":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("FULLSCREEN")]
    elif opt == "thumb_border":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("THUMB_BORDER")]
    elif opt == "show_movies":
        checked_rect[0] = (positions[2], positions[1])[get_config_val("MOVIES")]
    checked_rect[1] = positions[0]
    screen.blit(checked_img, checked_rect)
    update(checked_rect)
    # draw unchecked box:
    unchecked_img = load_img(gl.UNCHECKED_BOX, screen, False)
    unchecked_rect = unchecked_img.get_rect()
    if opt == "transparent_text":
        unchecked_rect[0] = (positions[2], positions[1])[get_config_val("TRANSPARENT_TEXT")]
    elif opt == "main_statusbar":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("MAIN_STATUS_BAR")]
    elif opt == "four_statusbars":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("FOUR_AT_A_TIME_STATUS_BARS")]
    elif opt == "exif_statusbar":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("ON_THE_FLY_EXIF_STATUS_BAR")]
    elif opt == "thumb_statusbars":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("THUMBNAIL_STATUS_BARS")]
    elif opt == "image_border":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("IMAGE_BORDER")]
    elif opt == "dirnum_colors":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("COLOR_DIRECTORY_NUMBERS")]
    elif opt == "lock_zoom":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("PERSISTENT_ZOOM")]
    elif opt == "wrap":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("WRAP")]
    elif opt == "wrap_slideshow":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("WRAP_SLIDESHOW")]
    elif opt == "start_fullscreen":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("FULLSCREEN")]
    elif opt == "thumb_border":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("THUMB_BORDER")]
    elif opt == "show_movies":
        unchecked_rect[0] = (positions[1], positions[2])[get_config_val("MOVIES")]
    unchecked_rect[1] = positions[0]
    screen.blit(unchecked_img, unchecked_rect)
    update(unchecked_rect)
    return (checked_rect, unchecked_rect)


def write_cfg(what, a_string=False):
    " save changes to imgv.conf "
    f = open(gl.CONF_FILE, 'rw')
    lines = f.readlines()
    for i, item in enumerate(lines): # get the index of searched item:
        if item.startswith(what):
            break
    was = lines.pop(i)
    right, left = split_var(was)
    if a_string is False:
        # it's an int so let's toggle it:
        isnow = right + '=' + str(int(left) ^ 1) + '\n'
    else:
        isnow = right + '=' + a_string + '\n'
    lines.insert(i, isnow)
    f.close()
    f = open(gl.CONF_FILE, 'wa') # erase the file
    for line in lines: # rewrite the file with new changes:
        f.write(line)


def split_var(line):
    right, left = line.split('=')
    return (right, left.replace('\n', ''))

