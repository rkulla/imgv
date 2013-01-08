# multiplatform wallpaper setting code by Ryan Kulla, rkulla@gmail.com
import gl
from sys import platform
from os import system
from os.path import basename
from error_box import errorbox
if platform == 'win32':
    import BmpImagePlugin, JpegImagePlugin, PngImagePlugin, SgiImagePlugin, SunImagePlugin, TgaImagePlugin, TiffImagePlugin, PcxImagePlugin, PpmImagePlugin, XpmImagePlugin # for py2exe to work with PIL
    import Image # PIL
    import ctypes
    from win32con import SPI_SETDESKWALLPAPER, WM_SETTINGCHANGE, SPIF_UPDATEINIFILE


def windows_wallpaper(file):
    picname = gl.files[file]
    if picname.split('.')[-1] == "bmp": # if not a bitmap we convert it to one for windows
        picconvert = picname
    else:
        picconvert = ' '.join(basename(gl.files[file]).split('.')[:-1]) + '.bmp'
    try:
        im = Image.open(picname)
        picconvert = gl.DATA_DIR + "wallpaper\\" + picconvert
        im.save(picconvert)
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, WM_SETTINGCHANGE, picconvert, SPIF_UPDATEINIFILE)
    except:
        return


def unix_wallpaper(file):
    cmd = "%s %s" % (gl.WALLPAPER_PROGRAM, gl.files[file])
    try:
        system(cmd)
    except:
        print "Couldn't set wallpaper"
