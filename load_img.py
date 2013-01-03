# imgv image/movie loading code by Ryan Kulla, rkulla@gmail.com
import gl
from os import getcwd, sep
from urllib import urlopen
from StringIO import StringIO
try:
    from movie_player import load_movie
except:
    print "imgv running in python2.4 doesn't support MPEG MOVIES on your platform currently"
from screensaver import disable_screensaver, enable_screensaver
from pygame.display import set_mode, get_surface
from pygame.locals import RESIZABLE
from pygame.image import load
from pygame.transform import scale
from pygame import error


def insensitive_find(haystack, needle):
    return haystack.lower().find(needle.lower())


def load_img(img_file, screen, allow_zoom=True):
    "load images and movies"
    if not gl.PERSISTENT_ZOOM_VAL:
        gl.ZOOM_EXP = 0
    if gl.PLAY_LIST_NAME != " ":
        gl.CUR_PATH = img_file
    else:
        gl.CUR_PATH = getcwd() + sep + img_file
    try:
        gl.CUR_PATH = gl.CUR_PATH[gl.CUR_PATH.rindex(getcwd()):]  # only show path once
    except:
        print "Couldn't load image"
    try:
        if img_file[:5] == "http:":  # load url
            try:
                gl.REMOTE = 1
                pic = urlopen(img_file).read()
                img = load(StringIO(pic))
                gl.REAL_WIDTH, gl.REAL_HEIGHT = img.get_width(), img.get_height()
                if gl.PERSISTENT_ZOOM_VAL and allow_zoom is True:
                    img = zoom_adjust(img)
                gl.REMOTE_FILE_SIZE = len(pic)
                gl.REMOTE_IMG_DATA = StringIO(pic)
                gl.REMOTE_IMG = img_file
                gl.ALREADY_DOWNLOADED = 0
            except:
                img = load(gl.ERROR_IMG).convert()
                gl.REAL_WIDTH, gl.REAL_HEIGHT = img.get_width(), img.get_height()
        elif insensitive_find(img_file, ".mpg") != -1 or insensitive_find(img_file, ".mpeg") != -1:
            disable_screensaver()
            if gl.THUMBING or gl.MULTI_VIEWING:
                img = load(gl.MOVIE_FILE).convert()
                gl.REAL_WIDTH, gl.REAL_HEIGHT = img.get_width(), img.get_height()
                if gl.PERSISTENT_ZOOM_VAL and allow_zoom is True:
                    img = zoom_adjust(img)
            else:
                img = load_movie(screen, img_file)
                gl.REAL_WIDTH, gl.REAL_HEIGHT = img.get_width(), img.get_height()
            if not gl.SLIDE_SHOW_RUNNING:
                enable_screensaver()
            return img
        else:
            # load normal image
            gl.REMOTE = 0
            img = load(img_file).convert()
            gl.REAL_WIDTH, gl.REAL_HEIGHT = img.get_width(), img.get_height()
            if (gl.FIT_IMAGE_VAL == 3 or (gl.SLIDE_SHOW_RUNNING and gl.FIT_IMAGE_SLIDESHOW_VAL == 3)) and allow_zoom is True:
                screen = fit_window(img)
            if gl.PERSISTENT_ZOOM_VAL and allow_zoom is True:
                img = zoom_adjust(img)
    except error:
        img = load(gl.ERROR_IMG).convert()
        gl.REAL_WIDTH, gl.REAL_HEIGHT = img.get_width(), img.get_height()
    if gl.SLIDE_SHOW_RUNNING and gl.FIT_IMAGE_SLIDESHOW_VAL and not gl.SKIP_FIT:
        if gl.FIT_IMAGE_SLIDESHOW_VAL == 1:
            if (gl.REAL_WIDTH > screen.get_rect().right or gl.REAL_HEIGHT > screen.get_rect().bottom) or gl.SCALE_UP:
                img = fit_image(img)
        if gl.FIT_IMAGE_SLIDESHOW_VAL == 2:
            img = fit_image(img)
    if gl.FIT_IMAGE_VAL and not gl.SKIP_FIT and not gl.SLIDE_SHOW_RUNNING:
        if gl.FIT_IMAGE_VAL == 1:
            if (gl.REAL_WIDTH > screen.get_rect().right or gl.REAL_HEIGHT > screen.get_rect().bottom) or gl.SCALE_UP:
                img = fit_image(img)
        if gl.FIT_IMAGE_VAL == 2 and allow_zoom is True:
            img = fit_image(img)
    gl.SKIP_FIT = 0
    return img


def zoom_adjust(img):
    "resize the image with the current zoom factor."
    img_width = img.get_width()
    img_height = img.get_height()
    if gl.ZOOM_EXP < 0:
        for i in range(gl.ZOOM_EXP, 0):
            if gl.ZOOM_DOUBLE:
                img_width /= 2
                img_height /= 2
            else:
                img_width /= 1.1
                img_height /= 1.1
    elif gl.ZOOM_EXP > 0:
        for i in range(gl.ZOOM_EXP):
            if gl.ZOOM_DOUBLE:
                img_width *= 2
                img_height *= 2
            else:
                img_width *= 1.1
                img_height *= 1.1
    img = scale(img, (img_width, img_height))
    return img


def fit_window(img):
    "resize window to fit the image"
    gl.IMGV_RESOLUTION = img.get_size()
    return set_mode(gl.IMGV_RESOLUTION, RESIZABLE)


def fit_image(img):
    "resize the image to fit the imgv window"
    screen = get_surface()
    gl.SCALE_UP = 0
    if gl.REAL_WIDTH > gl.REAL_HEIGHT:
        r = float(gl.REAL_WIDTH) / float(gl.REAL_HEIGHT)
        new_width = screen.get_width()
        new_height = int(new_width / r)
        scale_val = new_width, new_height
        img = scale(img, scale_val)
        gl.SHRUNK = 1
    elif gl.REAL_WIDTH < gl.REAL_HEIGHT:
        r = float(gl.REAL_HEIGHT) / float(gl.REAL_WIDTH)
        new_height = screen.get_height()
        new_width = int(new_height / r)
        scale_val = new_width, new_height
        img = scale(img, scale_val)
        gl.SHRUNK = 1
    elif gl.REAL_WIDTH == gl.REAL_HEIGHT:
        r = float(gl.REAL_WIDTH) / float(gl.REAL_HEIGHT)
        new_height = screen.get_height()
        new_width = screen.get_width()
        if new_height > new_width:
            scale_val = int(new_width / r), int(new_width / r)
        elif new_width > new_height:
            scale_val = int(new_height / r), int(new_height / r)
        else:
            scale_val = new_width, new_height
        img = scale(img, scale_val)
    else:
        new_height = new_width = screen.get_width()
        scale_val = new_width, new_height
        img = scale(img, scale_val)
    return img
