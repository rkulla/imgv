# imgv data objects code by Ryan Kulla, rkulla@gmail.com
# Note: The order in which objects are declared in this file are very important and
# rearranging the order could cause certain code to break.
import os
from sys import argv
from cfg import get_conf_name, set_configuration
from dir_nav import strip_dirs, get_imgs
from error_box import errorbox
from res import my_toggle_fullscreen
from pygame import version


BASE_DIR = os.getcwd()
try:
    DATA_DIR = os.environ['IMGV_HOME'] + os.sep + 'data' + os.sep
except KeyError:
    DATA_DIR = os.path.join(BASE_DIR, 'data' + os.sep)


IMGV_VERSION = "3.1.5"
TOGGLE_TRANSPARENT = 0
TOGGLE_STATUS_BAR = 1
FOUR_STATUS_BARS = 1
THUMB_STATUS_BARS = 1
ON_FLY_EXIF_STATUS_BAR = 1
TRANS_FX = "NONE"
LAST_DIR = ""
ADDED_DIR_NUMS = 0
BEEN_THERE_DONE_THAT = 0
ALREADY_DOWNLOADED = 0
EXTERNAL_EDITOR = "None"
ESCAPED = 0
DIRNUM_COLORS = 1
HAND_TOOL = 0
DO_DRAG = 0
OLD_CAP = ""
PAUSED = 0
BEING_HOVERED = 0
ROW_SEP = 19
SHOW_EXIFBUTTON = 1
UNIQUE_COLORS = None
FIRST_RECT = SECOND_RECT = THIRD_RECT = FOURTH_RECT = FIFTH_RECT = SIXTH_RECT = SEVENTH_RECT = EIGHTH_RECT = NINTH_RECT = TENTH_RECT = ELEVENTH_RECT = TWELFTH_RECT = THIRTEENTH_RECT = FOURTEENTH_RECT = FIFTEENTH_RECT = SIXTEENTH_RECT = SEVENTEENTH_RECT = EIGHTEENTH_RECT = NINETEENTH_RECT = TWENTIETH_RECT = TWENTYFIRST_RECT = TWENTYSECOND_RECT = TWENTYTHIRD_RECT = TWENTYFOURTH_RECT = TWENTYFIFTH_RECT = TWENTYSIXTH_RECT = TWENTYSEVENTH_RECT = TWENTYEIGTH_RECT = TWENTYNINTH_RECT = THIRTIETH_RECT = THIRTYFIRST_RECT = THIRTYSECOND_RECT = THIRTYTHIRD_RECT = THIRTYFOURTH_RECT = (-1, -1, -1, -1)
NOT_HOVERED = 1
MAX_THUMBS = 0
MAX_THUMBS_SET = 0
USING_THUMB_DEFAULT = 0
MY_KEYDOWN = 0
MY_KEYUP = 0
MY_KEYRIGHT = 0
MY_KEYLEFT = 0
LRECT, RRECT, TRECT, BRECT = 0, 0, 0, 0
FONT_NAME = DATA_DIR + "Vera.ttf"
IMGV_COLOR = 0, 0, 0
WHITE = 255, 255, 255
MID_GRAY = 192, 192, 192
SILVER = 200, 200, 200
BLACK = 0, 0, 0
BLUE = 0, 0, 255
RED = 255, 000, 051
PURPLE = 102, 000, 255
SKY_BLUE = 000, 255, 255
IMGV_LOGO_BLUE = 000, 128, 234
LIGHT_GREEN = 0, 255, 102
YELLOW = 255, 255, 51
ORANGE = 255, 102, 051
GREEN = 0, 136, 0
DARK_SLATE_BLUE = 72, 41, 139
DARK_SLATE_GRAY = 49, 79, 79
SADDLE_BROWN = 139, 69, 19
COLORS = {"RED":RED, "BLUE":BLUE, "PURPLE":PURPLE, "SKY_BLUE":SKY_BLUE, "SILVER":SILVER,\
"GREEN":GREEN, "LIGHT_GREEN":LIGHT_GREEN, "ORANGE":ORANGE, "YELLOW":YELLOW, "BLACK":BLACK, "WHITE":WHITE,\
"DARK_SLATE_BLUE":DARK_SLATE_BLUE, "DARK_SLATE_GRAY":DARK_SLATE_GRAY, "SADDLE_BROWN":SADDLE_BROWN, "MID_GRAY":MID_GRAY, "IMGV_LOGO_BLUE":IMGV_LOGO_BLUE}
FONT_BG = BLACK
TEXT_TRANSPARENT = 0
BUTTON_BGCOLOR = IMGV_LOGO_BLUE
BUTTON_HOVERCOLOR = SKY_BLUE
BUTTON_TEXTCOLOR = BLACK
BUTTON_TEXTHOVERCOLOR = BLACK
CLOSE_BUTTONCOLOR = BLUE
MSG_COLOR = WHITE
IMG_BORDER_COLOR = WHITE
FOUR_DIV_COLOR = PURPLE
THUMB_BORDER_COLOR = WHITE
THUMB_BG_COLOR_VAL = BLACK
THUMB_BORDER_VAL=1
IMG_BORDER = 0
MAX_SCREEN_FILES = 0 # number of image names file_master can show on a given screen res 
MAX_SF = {"640x480":165, "800x600":301, "1024x768":513, "1280x1024":858}
ACCEPTED_WINSIZES = ["640x480", "800x600", "1024x768", "1280x1024"]
CONF_FILE = get_conf_name()
WRAP = "1"
WRAP_SLIDESHOW = "1"
THUMB_VAL = "100x100"
THUMBING = 0
USING_SCROLL_MENU = 0 # sentinel for TOGGLE_TRANSPARENT
MOVIES_VAL = 1
KEEP_MENU_OPEN = "1"
MENU_DIVIDER_AMOUNT = 14
COUNT_CLICKS = 0
JUST_RESIZED = 0
ORIG_WINSIZE = "800x600"
FIT_IMAGE_VAL = "1"
FIT_IMAGE_SLIDESHOW_VAL = 1
CURRENT_GAMMA = "1.0"
RESET_FIT = 0
SCALE_UP = 0
PERSISTENT_ZOOM_VAL = 0
ZOOM_EXP = 0 # Exp of the zoom factor
ZOOM_DOUBLE = 0
CURRENT_ZOOM_PERCENT = "100"
ZOOM_PERCENT_MAX = 1600 # 1600%
CALC_ZOOM = 1
N_MILLISECONDS = "0"
MAX_ZOOM_MAX_MS = 5000
DBL_ZOOM_MAX_MS = 2000
START_DIRECTORY_VAL = os.getcwd()
CORRECT_PASSWORD = None
START_FULLSCREEN = 0
TOGGLE_FULLSCREEN_SET = 0
IMGV_RESOLUTION = (800, 600)
set_configuration() # set up user defined default values
MOVIE_FILE = DATA_DIR + "movie-file.jpg"
SLIDE_SHOW_RUNNING = 0
TRANSPARENT = 1, 1, 1
if START_FULLSCREEN == 1:
    TOGGLE_FULLSCREEN = 1
    my_toggle_fullscreen()
else:
    TOGGLE_FULLSCREEN = 0
FULLSCREEN_SPECIAL = 0 # flag for launching fullscreen mode with or without current window resolution
MENU_COLOR = MSG_COLOR
MENU_COLOR_ITEM = 0
MENU_ADJUST = COLORS.values()
NS_GLOBAL = 0 # number of seconds it took to load. used with check_timer()
DEFAULT_RES = IMGV_RESOLUTION
MENU_POS = DEFAULT_RES[0] - 150
BEFORE_WINSIZE = DEFAULT_RES
IMGV_LOGO = DATA_DIR + "imgv-logo1.jpg"
IMGV_LOGO_SMALL = DATA_DIR + "imgv-logo1-small.jpg"
NO_MATCHES_IMG = DATA_DIR + "no-matches.jpg"
CHECKED_BOX = DATA_DIR + "checked-box.jpg"
UNCHECKED_BOX = DATA_DIR + "unchecked-box.jpg"
CHANGE_BOX = DATA_DIR + "change-box.jpg"
TITLE = "imgv"
WAS_IN_CHANGE_DRIVES = 0
MONTH_MAP = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
DAY_SUFFIX_MAP = {'01':'1st', '02':'2nd', '03':'3rd', '04':'4th', '05':'5th', '06':'6th', '07':'7th', '08':'8th', '09':'9th', '10':'10th', '11':'11th', '12':'12th', '13':'13th', '14':'14th', '15':'15th', '16':'16th', '17':'17th', '18':'18th', '19':'19th', '20':'20th', '21':'21st', '22':'22nd', '23':'23rd', '24':'24th', '25':'25th', '26':'26th', '27':'27th', '28':'28th', '29':'29th', '30':'30th', '31':'31st'}
EXPAND_DAY_MAP = {'Mon':'Monday', 'Tue':'Tuesday', 'Wed':'Wednesday', 'Thu':'Thursday', 'Fri':'Friday', 'Sat':'Saturday', 'Sun':'Sunday'}
EXPAND_MONTH_MAP = {'Jan':'January', 'Feb':'February', 'Mar':'March', 'Apr':'April', 'May':'May', 'Jun':'June', 'Jul':'July', 'Aug':'August', 'Sep':'September', 'Oct':'October', 'Nov':'November', 'Dec':'December'}
HOUR_MAP = {'00':'12', '01':'1', '02':'2', '03':'3', '04':'4', '05':'5', '06':'6', '07':'7', '08':'8', '09':'9', '10':'10', '11':'11', '12':'12', '13':'1', '14':'2', '15':'3', '16':'4', '17':'5', '18':'6', '19':'7', '20':'8', '21':'9', '22':'10', '23':'11', '24':'12'}
IMGV_PLAYLISTS = DATA_DIR + "playlists"
PLAY_LIST_NAME = " "
REMOTE = 0 # true if its a remote url to the image
REMOTE_IMG = "" # remote image name
REMOTE_IMG_DATA = "" # remote image data
REMOTE_FILE_SIZE = 0 # remote image byte size
MIN_WIDTH = 10
MIN_HEIGHT =10 
MOVE = 21 # how much to nudge larger-than-window images by
ERROR_IMG = DATA_DIR + "imgv-error.jpg" 
DRIVE = os.getcwd()[0] # used for multi-drive support
REAL_WIDTH = 0
REAL_HEIGHT = 0
CUR_PATH = ""
SHRUNK = 0
SKIP_FIT = 0
THUMBING = 0
MULTI_VIEWING = 0
SKIP = 0 # used for long strings in inputbox()
REFRESH_IMG_COUNT = 1
ISURL = 0
URL = ""
SHOW_DATA = False
INDEX_OF = False
JUST_SOURCE = 0 # for complete url image links
URL_ERROR = False
DIRNUMSEP = ') '
MULT_DIRS = [] # to store multiple tagged directories
FILTER_COMMAND = {}
SUBDIRS = 0
SORT_HIT = 0


IMG_TYPES = [".gif",".GIF", ".jpg",".JPG", ".jpeg",".JPEG", ".png",".PNG", ".bmp",".BMP", ".ppm",".PPM", ".pcx",".PCX", 
".tga",".TGA", ".tif",".TIF", ".tiff",".TIFF", ".pnm",".PNM", ".pbm",".PBM", ".pgm",".PGM", ".xpm",".XPM", ".xcf",".XCF",
".lbm",".LBM", ".iff",".IFF"]


if MOVIES_VAL:
    for t in (".mpg", ".MPG", ".mpeg", ".MPEG"):
        IMG_TYPES.append(t)


if not version.ver >= "1.1":
    errorbox("Version Error", "You need pygame 1.1 or greater to run imgv")


if len(argv) < 2:
    if START_DIRECTORY_VAL == "CURRENT":
        dir_or_file = '.'
    else:
        dir_or_file = START_DIRECTORY_VAL
else:
    dir_or_file = argv[1]
    if not os.path.exists(dir_or_file):
        # make a full path if user didn't (i.e., they typed "../foo/bar/bla.jpg")
        dir_or_file = BASE_DIR + os.sep + dir_or_file 


# set initial directory values
CACHE_DIRS = os.listdir(START_DIRECTORY_VAL)
CACHE_DIRS = strip_dirs(CACHE_DIRS)
CACHE_DIR_OK = 0


if os.path.isdir(dir_or_file) or os.path.isdir(dir_or_file + os.sep):
    os.chdir(dir_or_file)
    DRIVE = dir_or_file.split(":")[0]
    # store only image files in 'files'
    files = get_imgs(os.getcwd(), 0)
elif os.path.isfile(dir_or_file):
    if dir_or_file[1] == ":" and dir_or_file[2] == os.sep:
        os.chdir(os.path.dirname(dir_or_file))
    files = [dir_or_file]
elif dir_or_file[:5] == "http:":
    REMOTE = 1
    files = [dir_or_file]
else:
    errorbox("Invalid File or Directory", os.path.basename(dir_or_file))


MENU_ITEMS_SHORT = [
    " Directory Browser ",
    " Extract from Web ",
    " Playlists ",
    "",
    " Close Menu ",
    " Help ",
    " Exit "]


MENU_ITEMS_LONG = [
    " Image Properties ",
    "",
    " Next Image ",
    " Previous Image ",
    " First Image ",
    " Last Image ",
    " Shuffle ",
    " Unshuffle ",
    "",
    " Directory Browser ",
    " Image Browser ",
    " Extract from Web ",
    " Playlists ",
    " Add to Playlist ",
    "",
    " Thumbnails ",
    " Four at a Time ",
    " Slideshow ",
    "", 
    " Flip Horizontal ",
    " Flip Vertical ",
    " Rotate Right ",
    " Rotate Left ",
    " Zoom In ",
    " Zoom Out ",
    " Lock Zoom ",
    "",
    " Fit to Window ",
    " Actual Size ", 
    " Hand Tool ",
    " Close Image ",
    " Hide Image ",
    " Refresh ",
    "",
    " Close Menu ",
    " Edit ",
    " Help ",
    " Exit "]


PREF_LIST = [
        ("Main screen status bar:", "Show the main status bar. Default = Yes"),
        ("Four at a Time status bars:", "Show status bars in Four-at-a-Time mode. Default = Yes"), 
        ("On-the-fly Exif status bar:", "Show on-the-fly camera metadata in the main screen. Default = Yes"), 
        ("Thumbnail status bars:", "Show filenames in thumbnail mode. Default = Yes"),
        ("Transparent text:", "Show the font of the main menu and status bars as transparent (no background color.) Default = No"), 
        ("Image border:", "Show a border around images (helps to see their true pixels against the background.) Default = No"), 
        ("Persistent zoom:", "Always Lock Zoom. Default = No"), 
        ("Wrap images:", "Allow going to the first image after the last image. Default = Yes"), 
        ("Wrap slideshow images:", "Allow going to the first image after the last image in a slideshow. Default = Yes"), 
        ("Start in fullscreen mode:", "Start imgv in fullscreen mode. Default = No"), 
        ("Thumbnail border:", "Show borders around images in thumbnail mode. Default = Yes"), 
        ("Colored directory numbers:", "Show directory browser numbers in color (Note: This is slower.) Default = No"), 
        ("Show movies:", "Load MPEG movies along with images for viewing. Default = Yes"), 
        ("Screen background color:", "The color of the background to show images against. Default = BLACK"), 
        ("Font color:", "Color of the font for the main menu, status bars and empahsized text. Default = WHITE"), 
        ("Font background color:", "Background color of the main font. Default = BLACK"), 
        ("Image border color:", "Color of the image border when active. Default = LIGHT_GREEN"),
        ("Thumbnail border color:", "Color of the image border for thumbnails. Default = WHITE"),
        ("Thumbnail background box color:", "Color of the background the thumbnail images will show against. Default = BLACK"), 
        ("Four-at-a-Time divider color:", "Color of the image divider in Four-at-a-Time mode. Default = WHITE"),
        ("Button background color:", "Background color of buttons. Default = IMGV_LOGO_BLUE"), 
        ("Button hover color:", "Background color of buttons when your mouse hovers them. Default = SKY_BLUE"), 
        ("Button text color:", "Color of the text on buttons. Default = BLACK"), 
        ("Button text hover color:", "Color of the text on buttons when your mouse hovers them. Default = BLACK"), 
        ("Close button color:", "Color of the close/cancel buttons (The 'X' in the top/right of the screen. Default = SADDLE_BROWN"), 
        ("Fit images:", "How to scale the images or window to fit eachother. Default = Fit nothing"),
        ("Screen brightness:", "Temporarily change the gamma values on the display hardware. Default = 1.0"), 
        ("Default window size:", "Default window size of imgv. Default = 800x600"), 
        ("Thumbnail size:", "Size of the thumbnail border/box that each thumb will fit in. Default = AUTO"), 
        ("Transitional effects:", "Set this if you want a transitional effect when loading images. Default = NONE"), 
        ("Start directory:", "Directory to load images from when imgv first starts. Default = /"), 
        ("External editor:", "Path to external image editing software. Default = \"None\""),
        ("Fit slideshow images:", "How to scale the images or window to fit eachother while in a slideshow. Default = Fit large images"),
        ("Password", "Password to use in when hiding images. Default = None"),
        ]
