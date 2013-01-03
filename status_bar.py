# image status bar code by Ryan Kulla, rkulla@gmail.com
import gl
from sys import platform
from time import ctime
from stat import ST_MTIME
from os import getcwd, stat
from os.path import basename, getsize
import pygame
from pygame.display import update, set_caption, get_caption
from show_message import show_message, truncate_name
from buttons import imgv_button
import exif
if platform == 'win32':
    import BmpImagePlugin, JpegImagePlugin, PngImagePlugin, SgiImagePlugin, SunImagePlugin, TgaImagePlugin, TiffImagePlugin, PcxImagePlugin, PpmImagePlugin, XpmImagePlugin # for py2exe to work with PIL
    import Image # PIL


def exif_data(screen, filename):
    exif_data1 = []
    exif_data2 = []
    font_size = 9
    font = pygame.font.Font(gl.FONT_NAME, font_size)
    try:
        file = open(filename, 'rb')
    except:
        return
    data = exif.process_file(file)
    if not data:
        return
    x = data.keys()
    x.sort()
    for i in x:
        if i in ('JPEGThumbnail', 'TIFFThumbnail'):
            continue
        try:
            if i == "EXIF DateTimeOriginal":
                # convert date/time to same format used on status bar
                splitdate, splittime = data[i].printable.split()
                spl = data[i].printable.split()[0].split(':')
                exif_data1.append('/'.join(spl[1:] + [spl[0]]) + " / " + splittime)
            if i == "EXIF FocalLength":
                mm = data[i].printable.split('/')
                mm = float(mm[0]) / float(mm[1])
                exif_data1.append("Focal Length: %smm" % mm)
            if i == "EXIF ExposureTime":  # shutter speed
                exif_data1.append("Shutter Speed: " + data[i].printable + "sec")
            if i == "EXIF FNumber":
                aperture = data[i].printable.split('/')
                aperture = float(aperture[0]) / float(aperture[1])
                exif_data1.append("Aperture: %s" % aperture)
            if i == "EXIF ExposureProgram":
                exif_data2.append("Exposure Mode: %s" % data[i].printable)
            if i == "EXIF ExposureBiasValue":
                exif_data2.append("Exposure Bias: %s" % data[i].printable)
            if i == "EXIF ISOSpeedRatings":
                exif_data1.append("ISO: %s" % data[i].printable)
            if i == "EXIF LightSource":
                exif_data1.append("White Balance: %s" % data[i].printable)
            if i == "EXIF Flash":
                exif_data1.append("Flash: %s" % data[i].printable)
            if i == "EXIF MeteringMode":
                if data[i].printable == "5":
                    exif_data2.append("Metering Mode: Multi-segment")
                else:
                    exif_data2.append("Metering Mode: %s" % data[i].printable)
            if i == "Image Make":
                exif_data2.append("Make: %s" % data[i].printable)
            if i == "Image Model":
                exif_data2.append("Model: %s" % data[i].printable)
        except:
            pass
    try:
        divider = ",  "
        exif_data1 = [x + divider for x in exif_data1[:-1]] + [exif_data1[-1]] # add a divider
        exif_data2 = [x + divider for x in exif_data2[:-1]] + [exif_data2[-1]]
        exif_data1_msg = " " + ' '.join(exif_data1) + " "
        exif_data2_msg = " " + ' '.join(exif_data2) + " "

        # round the shutter speed:
        if exif_data1_msg.find("Shutter") != -1:
            shutspd_text = exif_data1_msg.split(divider)[1].split()[-1]
            shutspd_vals = shutspd_text.split('/')
            shutspd_vals = shutspd_vals[0][0] + '/' + shutspd_vals[1][:2].replace('s', '').replace('sec', '')
            if shutspd_vals == "3/10": shutspd_vals = "1/3" # some kodak's
            exif_data1_msg = exif_data1_msg.replace(shutspd_text, shutspd_vals + " sec")

        # round the apeture value:
        if exif_data1_msg.find("Aperture") != -1:
             aperture_text = exif_data1_msg.split(divider)[2].split()[-1]
             exif_data1_msg = exif_data1_msg.replace(aperture_text, "f/" + str(round(float(aperture_text), 1)))

        # round the focal length:
        if exif_data1_msg.find("Focal") != -1:
            focal_text = exif_data1_msg.split(divider)[4].split()[-1]
            exif_data1_msg = exif_data1_msg.replace(focal_text, str(round(float(focal_text.replace('mm', '')), 1)))

        show_message(screen, exif_data1_msg, (1, 0), 9)
        if font.size(exif_data2_msg)[0] > screen.get_width():
            exif_data2_wrap = " " + exif_data2.pop()
            exif_data2_msg = " " + ' '.join(exif_data2)[:-3]
            show_message(screen, exif_data2_wrap, (1, 20), font_size)
        show_message(screen, exif_data2_msg, (1, 10), font_size)
    except:
        pass


def img_info(screen, filename, file, new_img, ns):
    num_imgs = len(gl.files)
    if screen.get_width() < 800:
        font_size = 9
    else:
        font_size = 10
    font = pygame.font.Font(gl.FONT_NAME, font_size)

    # set the main caption:
    if filename == gl.IMGV_LOGO:
        set_caption("[No images in %s] - %s" % (getcwd(), gl.TITLE))
    else:
        set_caption("%s%s %s%s- %s" % (('', '+')[new_img.get_width() > screen.get_width() or new_img.get_height() > screen.get_height()], filename.capitalize(), ('', '[Fit Image] ')[gl.FIT_IMAGE_VAL and not gl.RESET_FIT], ('', '[Lock Zoom] ')[gl.PERSISTENT_ZOOM_VAL], gl.TITLE))

    bitsperpixelmsg = ""
    try:
        im = Image.open(filename)
        if im.mode == "RGB" or im.mode == "YCbCr":
            bitsperpixel = 24
            bitsperpixelmsg = "x24 BPP"
        elif im.mode == "P" or im.mode == "L":
            bitsperpixel = 8
            bitsperpixelmsg = "x8 BPP"
        elif im.mode ==  1:
            bitsperpixel = 1
            bitsperpixelmsg = "x1 BPP"
        elif im.mode == "RGBA" or im.mode == "CMYK" or im.mode == "I" or im.mode == "F":
            bitsperpixel = 32
            bitsperpixelmsg = "x32 BPP"
    except:
        pass

    file_mtime = ctime(stat(filename)[ST_MTIME]).split()
    file_mtime = "%s/%s/%s / %s" % (gl.MONTH_MAP[file_mtime[1]], file_mtime[2], file_mtime[-1], file_mtime[3])

    full_filename = filename
    if gl.TOGGLE_STATUS_BAR and gl.files != [gl.IMGV_LOGO]:
        # display info about the current image
        current_img = str(file + 1)
        (img_width, img_height) = new_img.get_size()
        if gl.REMOTE:
            fsize = gl.REMOTE_FILE_SIZE
            filename = gl.REMOTE_IMG
            filename = basename(filename)
        else:
            fsize = getsize(filename)
            filename = basename(filename)

        if fsize <= 1024:
            file_size = "%d b" % fsize
        elif fsize >= 1024 and fsize <= (1024 * 1024):
            file_size = "%.2f KB" % (fsize / 1024.0)
        elif fsize >= 1024 and fsize <= (1024 * 1024 * 1024):
            file_size = "%.2f MB" % (fsize / (1024.0 * 1024.0))
        else:
            file_size = "0 bytes"

        memsizemsg = "?"
        try:
            # display memory size of image
            curmembytesize = ((img_width * img_height) * bitsperpixel) / 8
            if curmembytesize <= 1024:
                memsizemsg = "%d b" % curmembytesize
            elif curmembytesize >= 1024 and curmembytesize <= (1024 * 1024):
                memsizemsg = "%.2f KB" % (curmembytesize / 1024.0)
            elif curmembytesize >= 1024 and curmembytesize <= (1024 * 1024 * 1024):
                memsizemsg = "%.2f MB" % (curmembytesize / (1024.0 * 1024.0))
        except:
            pass

        if gl.PLAY_LIST_NAME != " ":
            set_caption("%s [%s] - imgv" % (get_caption()[0].replace(' - imgv', ''), gl.PLAY_LIST_NAME))
        if gl.SLIDE_SHOW_RUNNING == 1:
            set_caption("Slideshow - %s" % get_caption()[0])

        if gl.CALC_ZOOM:
            zoom_percent = (float(img_width) / float(gl.REAL_WIDTH)) * 100
            zoom_percent = int(round(zoom_percent, -1))
            gl.CURRENT_ZOOM_PERCENT = zoom_percent
        else:
            zoom_percent = gl.CURRENT_ZOOM_PERCENT
        gl.CALC_ZOOM = 1

        msmsg = calc_ms(str(ns))
        if msmsg == "":
            msmsg = "0"
        gl.N_MILLISECONDS = msmsg

        if zoom_percent == 100:
            img_status = " %s  [%s/%s]  %sx%s%s  %d%%  %.1fs  -  %s / %s, %s" % (filename, current_img, str(num_imgs), img_width, img_height, bitsperpixelmsg, zoom_percent, ns, str(file_size), memsizemsg, file_mtime)
        else:
            img_status = " %s  [%s/%s]  %sx%s%s  %d%%  [Zoom: %sx%s]  %.1fs  -  %s / %s, %s" % (filename, current_img, str(num_imgs), gl.REAL_WIDTH, gl.REAL_HEIGHT, bitsperpixelmsg, zoom_percent, img_width, img_height, ns, str(file_size), memsizemsg, file_mtime)

        filename = check_truncate(screen.get_width(), filename, font.size('  '.join(img_status.split()[1:]))[0])
        if zoom_percent == 100:
            img_status = " %s  [%s/%s]  %sx%s%s  %d%%  %.1fs  -  %s / %s, %s" % (filename, current_img, str(num_imgs), img_width, img_height, bitsperpixelmsg, zoom_percent, ns, str(file_size), memsizemsg, file_mtime)
        else:
            img_status = " %s  [%s/%s]  %sx%s%s  %d%%  [Zoom: %sx%s]  %.1fs  -  %s / %s, %s" % (filename, current_img, str(num_imgs), gl.REAL_WIDTH, gl.REAL_HEIGHT, bitsperpixelmsg, zoom_percent, img_width, img_height, ns, str(file_size), memsizemsg, file_mtime)

        if not gl.TOGGLE_TRANSPARENT:
            # draw transparent 'tinted' bar to be the background for the image status message to appear on
            transren = pygame.Surface((screen.get_width(), 13)).convert_alpha()
            transren.fill([gl.BLACK[0], gl.BLACK[1], gl.BLACK[2], 60]) # RGBA (A=Alpha)
            transrect = transren.get_rect()
            transrect.midbottom = screen.get_rect().midbottom
            screen.blit(transren, transrect)
            update(transrect)

        # write the image status message:
        show_message(screen, img_status, "bottom", font_size)

    try:
        if gl.ON_FLY_EXIF_STATUS_BAR:
            exif_data(screen, full_filename)
    except:
        print "Can't display exif"


def calc_ms(ms):
    # calculate milliseconds
    left, right = ms.split('.')
    l = len(right)
    if l == 2: # pad with a 0 when it only does 2 decimal places
        l = right[1:] + "0"
    else:
        l = right
    if ms[0] == "0":
        msmsg = l
    else:
        msmsg = left + right
        if len(right) == 2:
            msmsg = msmsg + "0"
    return msmsg.lstrip("0")


def check_truncate(screen_width, name, rest_size):
    allow = (screen_width - rest_size) / 6 - 15 # 6 = hardcoded value of how many pixels wide a char is font.size'd
    name = truncate_name(name, allow)
    return name

