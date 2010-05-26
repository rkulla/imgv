# verbose image details code by Ryan Kulla, rkulla@gmail.com
import gl
import os
from sys import platform
import imghdr
from img_screen import get_center, my_update_screen, junk_rect, img_border, paint_screen
from res import adjust_screen, restore_screen
from show_message import show_message, truncate_name
from buttons import imgv_button, hover_button, close_button
from cursor import wait_cursor, normal_cursor, hover_cursor
from load_img import load_img
from usr_event import check_quit, hit_key
if platform == 'win32':
    import BmpImagePlugin, JpegImagePlugin, PngImagePlugin, SgiImagePlugin, SunImagePlugin, TgaImagePlugin, TiffImagePlugin, PcxImagePlugin, PpmImagePlugin, XpmImagePlugin # for py2exe to work with PIL
import Image # PIL
import pygame.font, pygame.event
from pygame.transform import scale
from pygame.display import update, flip, set_caption
from pygame.locals import KEYDOWN, K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB, MOUSEBUTTONDOWN, MOUSEMOTION
from types import StringType, NoneType
import exif
from time import ctime, time, strptime, strftime
from stat import S_IMODE, ST_MODE, ST_MTIME, ST_ATIME, ST_CTIME, ST_UID, ST_GID


class verbose:
    # generate image information 
    def __init__(self, screen, file):
        if screen.get_width() == 640:
            self.font_size = 10
        else:
            self.font_size = 12
        self.font = pygame.font.Font(gl.FONT_NAME, self.font_size)
        gl.ROW_SEP = self.font.get_linesize() # recommended line separation size
        self.start_width = 230
        self.show_exif = 1
        self.row = 11
        show_message(screen, "Image Properties", self.row, self.font_size, ("bold", "underline", "transparent"))
        self.row += gl.ROW_SEP
        self.prev_pic_row = self.row + gl.ROW_SEP + 5
        self.screen = screen
        self.pil_info = 1
        self.bitsperpixel = None
        try:
            self.im = Image.open(gl.files[file])
        except:
            self.pil_info = 0
            self.show_exif = 0
    def file_and_dir_name(self, file, num_imgs):
        sw = self.screen.get_width()
        file_msg = "File name: "
        file_msg = check_truncate(sw, file_msg + os.path.basename(gl.files[file]))
        self.print_info(file_msg, 10)

        dir_msg = "Directory: "
        dir_msg = check_truncate(sw, dir_msg + os.path.dirname(gl.files[file]))
        self.print_info(dir_msg, 10)

        fpmsg = "Full path: "
        fpmsg = check_truncate(sw, fpmsg + gl.files[file])
        self.print_info(fpmsg, 10)

        self.print_info("Current index: %s / %s" % (comma_it(str(file + 1)), comma_it(str(num_imgs))), 14)
    def bits_per_pixel(self):
        if self.bitsperpixel:
            self.print_info("BPP (Bits Per Pixel): %s" % self.bitsperpixel, 21)
    def filesize(self, file, new_img):
        fsize = os.path.getsize(gl.files[file])
        if fsize <= 1024:
            filesize_details = "Size on disk: %s Bytes" % comma_it(fsize)
        elif fsize >= 1024 and fsize <= (1024 * 1024):
            filesize_details = "Size on disk: %s Kilobytes (%s Bytes)" % (comma_it((fsize / 1024.0)), comma_it(fsize))
        elif fsize >= 1024 and fsize <= (1024 * 1024 * 1024):
            filesize_details = "Size on disk: %.2f Megabytes (%s Kilobytes) (%s Bytes)" % ((fsize / (1024.0 * 1024.0), comma_it((fsize / 1024.0)), comma_it(fsize)))
        else:
            filesize_details = "0 Bytes"
        self.print_info(filesize_details, 13)

        if gl.CURRENT_ZOOM_PERCENT != 100:
            origmsg_start = "Original memory size:"
        else:
            origmsg_start = "Memory size:"
        try:
            # display current memory size of image
            origmembytesize = ((gl.REAL_WIDTH * gl.REAL_HEIGHT) * self.bitsperpixel) / 8
            if origmembytesize <= 1024:
                memsizemsg = "%s %s Bytes" % (origmsg_start, comma_it(origmembytesize))
            elif origmembytesize >= 1024 and origmembytesize <= (1024 * 1024):
                memsizemsg = "%s %s Kilobytes (%s Bytes)" % (origmsg_start, comma_it(origmembytesize / 1024.0), comma_it(origmembytesize))
            elif origmembytesize >= 1024 and origmembytesize <= (1024 * 1024 * 1024):
                memsizemsg = "%s %.2f Megabytes (%s Kilobytes) (%s Bytes)" % (origmsg_start, origmembytesize / (1024.0 * 1024.0), comma_it(origmembytesize / 1024.0), comma_it(origmembytesize))
            self.print_info(memsizemsg, len(origmsg_start))
        except:
            pass
        if gl.CURRENT_ZOOM_PERCENT != 100:
            try:
                # display current memory size of image
                curmembytesize = ((new_img.get_width() * new_img.get_height()) * self.bitsperpixel) / 8
                if curmembytesize <= 1024:
                    memsizemsg = "Current memory size: %s Bytes" % comma_it(curmembytesize)
                elif curmembytesize >= 1024 and curmembytesize <= (1024 * 1024):
                    memsizemsg = "Current memory size: %s Kilobytes (%s Bytes)" % (comma_it(curmembytesize / 1024.0), comma_it(curmembytesize))
                elif curmembytesize >= 1024 and curmembytesize <= (1024 * 1024 * 1024):
                    memsizemsg = "Current memory size: %.2f Megabytes (%s Kilobytes) (%s Bytes)" % (curmembytesize / (1024.0 * 1024.0), comma_it(curmembytesize / 1024.0), comma_it(curmembytesize))
                self.print_info(memsizemsg, 20)
            except:
                pass
    def img_type(self, file):
        self.img_type = imghdr.what(gl.files[file])
        if self.img_type != None:
            self.img_type = self.img_type.upper()
        if self.pil_info:
            if self.im.info.has_key("progression"):
                if type(self.img_type) != NoneType:
                    self.img_type += " (Progressive)"
        if self.img_type != None:
            self.print_info("File type: %s" % self.img_type, 10)
    def compression(self):
        img_format = " "
        if self.pil_info:
            if self.im.info.has_key('compression'):
                if self.img_type == "TIF" or self.img_type == "TIFF":
                    self.show_exif = 0 # compressed tiff's seem to break exif code
                compression = "Compression:  %s" % self.im.info['compression']
            else:
                compression = " "
            if self.im.info.has_key('version'): # gif
                if self.im.info['version'] in ('GIF87a', 'GIF89a'):
                    img_format = "Format: %s. Compression: LZW " % self.im.info['version']
                else:
                    img_format = "Format: %s.  " % self.im.info['version']
            if self.im.info.has_key('jfif'):
                compression = "Compression: JPEG"
                img_format = "Format: JFIF.  "
            if self.img_type == "PNG":
                compression = "Compression: PNG - ZIP"
            if img_format != " ":
                self.print_info(img_format + compression, 7)
    def aspect_ratio(self):
        if self.pil_info and self.im.info.has_key('jfif_unit'):
            if self.im.info.has_key('jfif_density'):
                aspect_ratio = str(self.im.info['jfif_density'][0]) + ' x ' + str(self.im.info['jfif_density'][1])
            if self.im.info['jfif_unit'] == 0:
                self.print_info("Aspect Ratio: %s" % aspect_ratio, 13)
            if self.im.info['jfif_unit'] == 2:
                self.print_info("Aspect Ratio: %s (Dots Per Centimeter)" % aspect_ratio, 13)
    def bit_depth(self):
        if self.pil_info:
            if self.im.mode == "RGB" or self.im.mode == "YCbCr":
                self.bitsperpixel = 24
            elif self.im.mode == "P" or self.im.mode == "L":
                self.bitsperpixel = 8
            elif self.im.mode == "1":
                self.bitsperpixel = 1
            elif self.im.mode == "RGBA" or self.im.mode == "CMYK" or self.im.mode == "I" or self.im.mode == "F":
                self.bitsperpixel = 32
    def get_pixel_format(self):
        if self.pil_info:
            if self.bitsperpixel == 1:
                self.pixel_format = "Bilevel (Black and White)"
            elif self.bitsperpixel == 8 and self.im.mode != "P":
                self.pixel_format = "Grayscale"
            elif self.im.mode == "P":
                self.pixel_format = "Color Palette"
            else:
                self.pixel_format = self.im.mode
            self.print_info("Pixel format: %s" % self.pixel_format, 13)
    def colors(self):
        uniquecolors_rect = junk_rect()
        total_colors = ""
        imret = None
        if self.pil_info and self.bitsperpixel not in (None, 32):
            imret = self.im
            if self.bitsperpixel == 24:
                total_colors = "Total colors: 16.7 Million."
            else:
                total_colors = "Total colors: %s." % (2 ** self.bitsperpixel)
            self.print_info(total_colors, 13)
            if gl.UNIQUE_COLORS == None and gl.SHOW_EXIFBUTTON and total_colors != "":
                uniquecolors_rect = imgv_button(self.screen, " Unique colors ", (self.font.size(total_colors)[0] + 230), self.row, None)
        return (uniquecolors_rect, total_colors, self.row, self.font, imret)
    def resolution(self):
        if self.pil_info:
            if self.im.info.has_key('dpi'):
                x, y = self.im.info['dpi']
                dpi = "Resolution: %d x %d PPI (Pixels Per Inch)" % (x, y)
                emph_len = 11
            else:
                dpi = " "
                emph_len = 0
            self.print_info(dpi, emph_len)
            try:
                self.print_info("Print size (from PPI): %s x %s inches" % (round(float(gl.REAL_WIDTH) / float(x), 1), round(float(gl.REAL_HEIGHT) / float(y), 1)), 22)
            except:
                pass
    def gamma(self):
        if self.pil_info:
            if self.im.info.has_key('gamma'):
                self.print_info("Gamma:  %s" % self.im.info['gamma'], 6)
    def transparency(self):
        if self.pil_info:
            if self.im.info.has_key('transparency'):
                self.print_info("Transparency:  %s" % self.im.info['transparency'], 13)
    def software(self):
        if self.pil_info:
            if self.im.info.has_key('Software'):
                self.print_info("Software: %s" % self.im.info['Software'], 9)
    def original_size(self):
        if gl.CURRENT_ZOOM_PERCENT != 100:
            origsizemsg_start = "Original size:"
        else:
            origsizemsg_start = "Size:"
        self.print_info("%s Width: %s Pixels. Height: %s Pixels" % (origsizemsg_start, comma_it(gl.REAL_WIDTH), comma_it(gl.REAL_HEIGHT)), len(origsizemsg_start))
    def current_size(self, new_img):
        dimensions = "Width: %s Pixels. Height: %s Pixels" % (comma_it(new_img.get_width()), comma_it(new_img.get_height()))
        self.print_info("Current size: %s %s" % (dimensions, ('', '(Zoomed to: ' + comma_it(gl.CURRENT_ZOOM_PERCENT) + '%)')[gl.CURRENT_ZOOM_PERCENT != 100]), 13)
    def picture_taken(self, filen):
        filename = gl.files[filen]
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
                    date_str = strftime('%a %b %d %H:%M:%S %Y', strptime(data[i].printable, '%Y:%m:%d %H:%M:%S'))
                    self.print_info("Created with digital camera: %s" % convert_times(date_str, 1), 28)
            except:
                self.print_info("Created with digital camera: %s" % data[i].printable, 28)
    def file_times(self, file):
        fname = gl.files[file]
        # created time:
        created_msg = convert_times(str(ctime(os.stat(fname)[ST_CTIME])), 1)
        self.print_info("Created on disk: %s" % created_msg, 16)
        # modified time:
        modified_msg = convert_times(str(ctime(os.stat(fname)[ST_MTIME])), 1)
        self.print_info("Last Modified: %s" % modified_msg, 14)
        # accessed time:
        accessed_msg = convert_times(str(ctime(os.stat(fname)[ST_ATIME])), 1)
        self.print_info("Last Accessed: %s" % accessed_msg, 14)
    def show_current_image(self, file):
        self.current = load_img(gl.files[file], self.screen, False)
        (self.current, img_width, img_height) = preview_img(self.screen, self.current)
        current_rect = self.current.get_rect()
        current_rect[0] = 15
        current_rect[1] = self.prev_pic_row
        self.screen.blit(self.current, current_rect)
        update(current_rect)
        img_border(self.screen, img_width, img_height, 15, self.prev_pic_row - 2)
    def loaded_time(self):
        self.print_info("Loaded in: %s milliseconds %s" % (comma_it(gl.N_MILLISECONDS), ('', '(From Zoom)')[gl.CURRENT_ZOOM_PERCENT != 100]), 10)
    def exif_data(self, filen):
        paint_screen(self.screen, gl.BLACK)
        close_button(self.screen)
        if not self.show_exif: 
            gl.SHOW_EXIFBUTTON = 0
            return 
        exif_info = []
        filename = gl.files[filen]
        try:
            file = open(filename, 'rb')
        except:
            exif_info.append("%s unreadable" % filename)
            gl.SHOW_EXIFBUTTON = 0
            return
        data = exif.process_file(file)
        if not data:
            font_size = 13
            font = pygame.font.Font(gl.FONT_NAME, font_size)
            no_exif_msg = "No Exif information found"
            show_message(self.screen, no_exif_msg, ((self.screen.get_width() / 2) - (font.size(no_exif_msg)[0] / 2), self.screen.get_height() / 2), font_size, ("bold", "transparent"))
            gl.SHOW_EXIFBUTTON = 0
            return
        x = data.keys()
        x.sort()
        for i in x:
            if i in ('JPEGThumbnail', 'TIFFThumbnail'):
                continue
            try:
                exif_info.append('%s:  %s' % (i, data[i].printable))
            except:
                exif_info.append('error', i, '"', data[i], '"')
        gl.SHOW_EXIFBUTTON = 0
        pos = 25
        show_message(self.screen, "Exif Information", "top", 13, ("underline", "bold", "transparent"))
        try:
            for line in exif_info:
                if type(line) is StringType and len(line) <= 250: # parachutes on long lines without this
                    exif_font = pygame.font.Font(gl.FONT_NAME, 9)
                    ren = exif_font.render(line, 1, gl.MENU_COLOR)
                    ren_rect = ren.get_rect()
                    ren_rect[0] = 14
                    ren_rect[1] = pos
                    self.screen.blit(ren, ren_rect)
                    pos = pos + 9
        except:
            pass 
        flip()
    def histogram(self):
        if not self.pil_info:
            return
        w = self.screen.get_width()
        h = gl.ROW_SEP + 415
        hist = self.im.histogram()
        redlist = hist[0:255]
        greenlist = hist[256:(256 + 255)]
        bluelist = hist[(256 + 255 + 1):]
        wdiv = 1.3 # shorten the width of the histogram
        vdiv = max(hist) / 130 # shorten the height of the histogram
        wpos = 16
        vlen = 175
        if self.pixel_format == "Grayscale":
            for i, v in enumerate(hist):
                if v > vlen: v -= vlen # don't go outside of border on long histograms
                pygame.draw.line(self.screen, gl.SILVER, ((i / wdiv) + wpos, h), ((i / wdiv) + wpos, (h - (v / vdiv))), 1)
        else:
            for i, v in enumerate(redlist):
                if v > vlen: v -= vlen
                pygame.draw.line(self.screen, gl.RED, ((i / wdiv) + wpos, h), ((i / wdiv) + wpos, (h - (v / vdiv))), 1)
            for i, v in enumerate(greenlist):
                if v > vlen: v -= vlen
                pygame.draw.line(self.screen, gl.GREEN, ((i / wdiv) + wpos, h), ((i / wdiv) + wpos, (h - (v / vdiv))), 1)
            for i, v in enumerate(bluelist):
                if v > vlen: v -= vlen
                pygame.draw.line(self.screen, gl.BLUE, ((i / wdiv) + wpos, h), ((i / wdiv) + wpos, (h - (v / vdiv))), 1)
        show_message(self.screen, "Histogram", (wpos + 1, h - 174), 11, ("transparent"))
        pygame.draw.line(self.screen, gl.MSG_COLOR, (wpos - 2, h + 2), (wpos - 2, h - vlen)) # left side of border
        pygame.draw.line(self.screen, gl.MSG_COLOR, ((i / wdiv) + wpos, h - vlen), ((i / wdiv) + wpos, h + 2)) # right side
        pygame.draw.line(self.screen, gl.MSG_COLOR, (wpos - 2, h - vlen), ((i / wdiv) + wpos, h - vlen)) # top 
        pygame.draw.line(self.screen, gl.MSG_COLOR, (wpos - 2, h + 2), ((i / wdiv) + wpos, h + 2)) # bottom 
    def system_info(self):
        info = pygame.display.Info()
        self.row += gl.ROW_SEP * 2
        show_message(self.screen, "Display Properties", self.row, self.font_size, ("bold", "underline", "transparent"))
        self.row += gl.ROW_SEP
        self.print_info('Using video driver: %s' % pygame.display.get_driver(), 20)
        self.print_info('Video mode is accelerated: %s' % ('No', 'Yes')[info.hw], 27)
        self.print_info('Display depth (Bits Per Pixel): %d' % info.bitsize, 31)
        self.print_info('Screen size of imgv: %s' % gl.ORIG_WINSIZE, 21)
    def print_info(self, msg, emphasize_length):
        if msg == " ":
            return
        self.row += gl.ROW_SEP
        before_color = gl.MSG_COLOR
        if gl.MSG_COLOR == gl.SILVER:
            gl.MSG_COLOR = (142, 142, 142)
        else:
            gl.MSG_COLOR = gl.SILVER
        show_message(self.screen, msg, (self.start_width, self.row), self.font_size, (""), (emphasize_length, before_color))
        gl.MSG_COLOR = before_color


def command_verbose_info(screen, new_img, rect, file, num_imgs):
    gl.ORIG_WINSIZE = "%sx%s" % (screen.get_width(), screen.get_height())
    (screen, before_winsize, not_accepted) = adjust_screen(screen)
    paint_screen(screen, gl.BLACK)
    if gl.REMOTE:
        remote_img_details(screen, new_img, rect, file, num_imgs)
    else:
        verbose_info(screen, new_img, file, num_imgs)
    screen = restore_screen(screen, before_winsize, not_accepted, new_img, file, num_imgs, rect)
    rect = get_center(screen, new_img)
    my_update_screen(new_img, screen, rect, file, num_imgs)


def verbose_info(screen, new_img, file, num_imgs):
    # main engine
    wait_cursor()
    paint_screen(screen, gl.BLACK)
    try:
        (uniquecolors_rect, total_colors, row, font, im, verb) = print_verbose_info(screen, new_img, file, num_imgs)
    except:
        return
    if gl.SHOW_EXIFBUTTON:
        exif_rect = imgv_button(screen, " Exif Data ", 5, gl.ROW_SEP + 435, None)
    (esc_rect, close_font) = close_button(screen)
    normal_cursor()
    transparency = 0
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(35)
        check_quit(event)
        cursor = pygame.mouse.get_pos()
        hover_cursor(cursor, (esc_rect, exif_rect, uniquecolors_rect))
        if gl.SHOW_EXIFBUTTON:
            hover_button(exif_rect, cursor, screen, " Exif Data ", 5, gl.ROW_SEP + 435, None)
        if gl.UNIQUE_COLORS == None and gl.SHOW_EXIFBUTTON and total_colors != "":
            hover_button(uniquecolors_rect, cursor, screen, " Unique colors ", (font.size(total_colors)[0] + 230), row, None)

        show_message(screen, convert_times(ctime(), 0), "bottom", 15, ("transparent"))

        if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if uniquecolors_rect != junk_rect():
                if uniquecolors_rect.collidepoint(cursor):
                    wait_cursor()
                    gl.UNIQUE_COLORS = comma_it(len(dict.fromkeys(im.getdata()))) # determine unique colors
                    before_color = gl.MSG_COLOR
                    if gl.MSG_COLOR == gl.SILVER:
                        gl.MSG_COLOR = (142, 142, 142)
                    else:
                        gl.MSG_COLOR = gl.SILVER
                    show_message(screen,  "Unique colors: %s%s" % (gl.UNIQUE_COLORS, ' ' * 12), ((font.size(total_colors)[0] + 235), row), 12, (""), (14, before_color))
                    gl.MSG_COLOR = before_color
                    normal_cursor()
            if exif_rect.collidepoint(cursor):
                wait_cursor()
                try:
                    verb.exif_data(file)
                except:
                    break
                normal_cursor()
            if esc_rect.collidepoint(cursor):
                before_exit()
                break
        if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB):
            before_exit()
            break


def print_verbose_info(screen, new_img, file, num_imgs):
    verb = verbose(screen, file)
    verb.bit_depth()
    verb.show_current_image(file)
    verb.file_and_dir_name(file, num_imgs)
    verb.original_size()
    if gl.CURRENT_ZOOM_PERCENT != 100:
        verb.current_size(new_img)
    verb.resolution()
    verb.img_type(file)
    verb.compression()
    verb.aspect_ratio()
    verb.get_pixel_format()
    (uniquecolors_rect, total_colors, row, font, im) = verb.colors()
    verb.bits_per_pixel()
    verb.gamma()
    verb.transparency()
    verb.software()
    verb.filesize(file, new_img)
    try:
        verb.picture_taken(file)
    except:
        pass
    verb.file_times(file)
    try: 
        verb.histogram()
    except: # a few rare images cause a ZeroDivisionError from histogram()
        print "Couldn't display histogram"
    verb.loaded_time()
    try:
        verb.system_info()
    except:
        pass
    flip()
    return (uniquecolors_rect, total_colors, row, font, im, verb)


def remote_img_details(screen, new_img, rect, file, num_imgs):
    # show no details if image is on a web server
    paint_screen(screen, gl.BLACK)
    while 1:
        event = pygame.event.wait()
        show_message(screen, gl.REMOTE_IMG, (0, 30, 0, 0), 12)
        check_quit(event)
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            return


def preview_img(screen, img):
    # generate an image preview
    square_width = 200
    square_height = 175
    (img_width, img_height) = img.get_size()
    small_img = img
    # display a preview image in dimensions that won't distort it:
    if img_width > img_height:
        if (not img_width < square_width and not img_height < square_height) or (img_width > square_width) or (img_height > square_height) or (img_width > square_width and img_height > square_height):
            r = float(img_width) / float(img_height)
            new_width = square_width
            new_height = int(new_width / r)
            scale_val = new_width, new_height
            small_img = scale(img, scale_val)
    if img_width < img_height:
        if (not img_width < square_width and not img_height < square_height) or (img_width > square_width) or (img_height > square_height) or (img_width > square_width and img_height > square_height):
            r = float(img_height) / float(img_width)
            new_height = square_height
            new_width = int(new_height / r)
            scale_val = new_width, new_height
            small_img = scale(img, scale_val)
    if img_width == img_height: 
        if (not img_width < square_width and not img_height < square_height) or (img_width > square_width) or (img_height > square_height) or (img_width > square_width and img_height > square_height):
            r = float(img_width) / float(img_height)
            new_height = square_height
            new_width = square_width
            scale_val = new_width, new_height
            small_img = scale(img, scale_val)
    (img_width, img_height) = small_img.get_size()
    return (small_img, img_width, img_height)


def before_exit():
    # clean up
    gl.UNIQUE_COLORS = None
    gl.SHOW_EXIFBUTTON = 1
    set_caption(gl.TITLE)


def check_truncate(screen_width, name):
    if screen_width >= 640 and screen_width < 800:
        name = truncate_name(name, 50)
    if screen_width >= 800 and screen_width < 1024:
        name = truncate_name(name, 81)
    if screen_width >= 1024 and screen_width < 1280:
        name = truncate_name(name, 115)
    if screen_width >= 1280:
        name = truncate_name(name, 140)
    return name


def convert_times(time_msg, show_today):
    "convert dates/times into a more human format"
    csplit = ctime().split()
    time_split = time_msg.split()
    timesplit = time_msg.split()
    # if time is today then say "Today" instead of today's name:
    if show_today and (' '.join(timesplit[:3] + [timesplit[4]]) == ' '.join(csplit[:3] + [csplit[4]])):
        time_msg = "Today, "
    # Format the time nicely:
    hour, minutes, seconds = timesplit[3].split(':')
    if int(hour) > 12:
        ampm = ' PM'
    else:
        ampm = ' AM'
    if time_msg.startswith("Today, "):
        time_msg += gl.EXPAND_MONTH_MAP[timesplit[1]] + ' ' + gl.DAY_SUFFIX_MAP[timesplit[2]] + ', ' + timesplit[4] + ', ' + gl.HOUR_MAP[hour] + ':' + minutes + ':' + seconds + ampm
    else:
        time_msg = gl.EXPAND_DAY_MAP[timesplit[0]] + ', ' + gl.EXPAND_MONTH_MAP[timesplit[1]] + ' ' + gl.DAY_SUFFIX_MAP[timesplit[2]] + ', ' + timesplit[4] + ', ' + gl.HOUR_MAP[hour] + ':' + minutes + ':' + seconds + ampm
    return time_msg


def comma_it(n):
    "Comma separate numbers"
    comma = ','
    isfloat = 0
    nstr = str(n)
    if nstr.count('.') > 0:
        isfloat = 1
        nstr, remainder = nstr.split('.')
    nstr = ' '.join(nstr).split()
    nstr_len = len(nstr)
    if nstr_len == 4: # thousands
        nstr.insert(1, comma)
    if nstr_len == 5: # 10 thousands
        nstr.insert(2, comma)
    if nstr_len == 6: # hundred thousands
        nstr.insert(3, comma)
    if nstr_len == 7: # millions
        nstr.insert(1, comma), nstr.insert(5, comma)
    if nstr_len == 8: # 10 millions
        nstr.insert(2, comma), nstr.insert(6, comma)
    if nstr_len == 9: # 100 millions
        nstr.insert(3, comma), nstr.insert(7, comma)
    if nstr_len == 10: # billions
        nstr.insert(1, comma), nstr.insert(5, comma)
        nstr.insert(9, comma),
    if nstr_len == 11: # 10 billions
        nstr.insert(2, comma), nstr.insert(6, comma), nstr.insert(10, comma)
    if nstr_len == 12: # 100 billions
        nstr.insert(3, comma), nstr.insert(7, comma), nstr.insert(11, comma)
    if nstr_len == 13: # 1 trillions
        nstr.insert(1, comma), nstr.insert(5, comma), nstr.insert(9, comma), nstr.insert(13, comma)
    nstr = ''.join(nstr)
    if isfloat:
        nstr += '.' + remainder[:2]
    return nstr

