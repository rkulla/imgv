# screensaver disabling code by Ryan Kulla, rkulla@gmail.com
from sys import platform
if platform == 'win32':
    import ctypes
    from win32con import SPI_SETSCREENSAVEACTIVE


def disable_screensaver():
    if platform == 'win32':
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETSCREENSAVEACTIVE, 0, 0, 0)
    else:
        try:
            system("killall xscreensaver")
        except:
            print "Couldn't kill xscreensaver"


def enable_screensaver():
    if platform == 'win32':
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETSCREENSAVEACTIVE, 1, 0, 0)
    else:
        try:
            system("xscreensaver -no-splash&")
        except:
            print "Couldn't enable xscreensaver"
