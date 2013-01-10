# imgv.conf configuration code by Ryan Kulla, rkulla@gmail.com
import gl
from os import chdir
from error_box import errorbox


def get_config_val(val):
    "return the value of a configuration option"
    f = open(gl.CONF_FILE)
    for line in f.readlines():
        if cfg_match(line, val):
            return int(chopnl(line))
    f.close()


def set_configuration():
    "set global configuration variables from imgv.conf"
    f = open(gl.CONF_FILE)
    for line in f.readlines():
        if cfg_match(line, "WRAP"):
            gl.WRAP = int(chopnl(line))
        if cfg_match(line, "WRAP_SLIDESHOW"):
            gl.WRAP_SLIDESHOW = int(chopnl(line))
        if cfg_match(line, "PASSWORD"):
            gl.CORRECT_PASSWORD = chopnl(line)
        if cfg_match(line, "KEEP_MENU_OPEN"):
            gl.KEEP_MENU_OPEN = chopnl(line)
        if cfg_match(line, "IMAGE_BORDER"):
            gl.IMG_BORDER = int(chopnl(line))
        if cfg_match(line, "THUMB_SIZE"):
            gl.THUMB_VAL = chopnl(line)
        if cfg_match(line, "THUMB_BORDER"):
            gl.THUMB_BORDER_VAL = int(chopnl(line))
        if cfg_match(line, "TRANSPARENT_TEXT"):
            gl.TOGGLE_TRANSPARENT = int(chopnl(line))
        if cfg_match(line, "MAIN_STATUS_BAR"):
            gl.TOGGLE_STATUS_BAR = int(chopnl(line))
        if cfg_match(line, "FOUR_AT_A_TIME_STATUS_BARS"):
            gl.FOUR_STATUS_BARS = int(chopnl(line))
        if cfg_match(line, "THUMBNAIL_STATUS_BARS"):
            gl.THUMB_STATUS_BARS = int(chopnl(line))
        if cfg_match(line, "ON_THE_FLY_EXIF_STATUS_BAR"):
            gl.ON_FLY_EXIF_STATUS_BAR = int(chopnl(line))
        if cfg_match(line, "FIT_IMAGE"):
            gl.FIT_IMAGE_VAL = int(chopnl(line))
        if cfg_match(line, "PERSISTENT_ZOOM"):
            gl.PERSISTENT_ZOOM_VAL = int(chopnl(line))
        if cfg_match(line, "FIT_IMAGE_SLIDESHOW"):
            gl.FIT_IMAGE_SLIDESHOW_VAL = int(chopnl(line))
        if cfg_match(line, "START_DIRECTORY"):
            gl.START_DIRECTORY_VAL = chopnl(line)
            try:
                chdir(gl.START_DIRECTORY_VAL)
            except:
                print 'invalid start directory'
        if cfg_match(line, "FONT_COLOR"):
            color = get_color(line)
            gl.MENU_COLOR = gl.MSG_COLOR = color
        if cfg_match(line, "IMGV_COLOR"):
            gl.IMGV_COLOR = get_color(line)
        if cfg_match(line, "IMAGE_BORDER_COLOR"):
            gl.IMG_BORDER_COLOR = get_color(line)
        if cfg_match(line, "FOUR_AT_A_TIME_DIVIDER_COLOR"):
            gl.FOUR_DIV_COLOR = get_color(line)
        if cfg_match(line, "THUMB_BORDER_COLOR"):
            gl.THUMB_BORDER_COLOR = get_color(line)
        if cfg_match(line, "FONT_BGCOLOR"):
            gl.FONT_BG = get_color(line)
        if cfg_match(line, "BUTTON_BGCOLOR"):
            gl.BUTTON_BGCOLOR = get_color(line)
        if cfg_match(line, "BUTTON_HOVERCOLOR"):
            gl.BUTTON_HOVERCOLOR = get_color(line)
        if cfg_match(line, "BUTTON_TEXTCOLOR"):
            gl.BUTTON_TEXTCOLOR = get_color(line)
        if cfg_match(line, "BUTTON_TEXTHOVERCOLOR"):
            gl.BUTTON_TEXTHOVERCOLOR = get_color(line)
        if cfg_match(line, "CLOSE_BUTTONCOLOR"):
            gl.CLOSE_BUTTONCOLOR = get_color(line)
        if cfg_match(line, "THUMB_BG_COLOR"):
            gl.THUMB_BG_COLOR_VAL = get_color(line)
        if cfg_match(line, "MOVIES"):
            gl.MOVIES_VAL = int(chopnl(line))
        if cfg_match(line, "EXTERNAL_EDITOR"):
            gl.EXTERNAL_EDITOR = chopnl(line)
        if cfg_match(line, "COLOR_DIRECTORY_NUMBERS"):
            gl.DIRNUM_COLORS = int(chopnl(line))
        if cfg_match(line, "WALLPAPER_PROGRAM"):
            gl.WALLPAPER_PROGRAM = chopnl(line)
        if cfg_match(line, "IMGV_WINDOW_SIZE"):
            gl.IMGV_RESOLUTION = chopnl(line)
            try:
                gl.MAX_SCREEN_FILES = gl.MAX_SF[gl.IMGV_RESOLUTION]
            except:
                gl.MAX_SCREEN_FILES = gl.MAX_SF["640x480"]
            x = None
            if gl.IMGV_RESOLUTION.find('x') != -1:
                x = 'x'
            elif gl.IMGV_RESOLUTION.find('X') != -1:
                x = 'X'
            if x is not None:
                gl.IMGV_RESOLUTION = int(gl.IMGV_RESOLUTION.split(x)[0]), int(gl.IMGV_RESOLUTION.split(x)[1])
        if cfg_match(line, "FULLSCREEN"):
            gl.START_FULLSCREEN = int(chopnl(line))
        if cfg_match(line, "TRANSITIONAL_EFFECT"):
            line = chopnl(line)
            if line == "MELT":
                gl.TRANS_FX = "MELT"
            elif line == "FADE_IN":
                gl.TRANS_FX = "FADE_IN"
            elif line == "NONE":
                gl.TRANS_FX = "NONE"
            else:
                gl.TRANS_FX = line
    f.close()


def cfg_match(line, val):
    if line.find(val + "=") != -1 and line.find("#") == -1:
        return 1
    return 0


def chopnl(line):
    "return the value with no newline for parsing"
    return line.split('=')[1].replace('\n', '')


def get_color(line):
    color = chopnl(line).upper()  # strip newline and make case insensitive
    if color.find(',') != -1:
        color = color.split(',')
        if len(color) >= 3:
            try:
                color = (int(color[0]), int(color[1]), int(color[2]))
                return color
            except:
                errorbox("Error in imgv.conf", "'%s' is an invalid color" % (line[:-1]))
    elif color not in gl.COLORS.keys():
        errorbox("Error in imgv.conf", "'%s' is an invalid color" % (line[:-1]))
    return gl.COLORS[color]
