# website image extraction code by Ryan Kulla, rkulla@gmail.com
import gl
from cursor import wait_cursor, normal_cursor
from show_message import show_message
from img_screen import get_center, paint_screen
from load_img import load_img
from input_box import ask
from HTMLParser import HTMLParser
import htmllib
import urllib2
import formatter
from pygame.display import set_caption


class CheckIndexHTML(HTMLParser):
    def handle_data(self, data):
        if data == "404 Not Found" or data == "404 Error":
            gl.INDEX_OF = True


def check_indexhtml():
    gl.INDEX_OF = False
    parser = CheckIndexHTML()
    try:
        # check if URL is using an index.html or "Index Of Files"
        if not gl.URL.count('/') <= 3 and not gl.URL.endswith("index.html") and not\
        gl.URL[gl.URL.rfind('/'):].count('.'):
            gl.URL = gl.URL + '/'
            html = urllib2.urlopen(gl.URL + "index.html").read()
        else:
            html = urllib2.urlopen(gl.URL).read()
        parser.feed(html)
        parser.close()
    except:
        gl.URL_ERROR = True
        return
    if gl.INDEX_OF == True:
        index_of_files()
    else:
        html_file()


class IndexOfParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for i in attrs:
            try:
                for ext in gl.IMG_TYPES:
                    if i[1].find(ext) != -1 and i[1].find("/icons") == -1:
                        gl.SHOW_DATA = True
            except:
                pass
    def handle_data(self, data):
        if gl.SHOW_DATA == True:
            gl.files.append(gl.URL + data)
            gl.SHOW_DATA = False


def index_of_files():
    parser = IndexOfParser()
    try:
        html = urllib2.urlopen(gl.URL).read()
        parser.feed(html)
        parser.close()
    except:
        gl.URL_ERROR = True
        return


class TagParse(htmllib.HTMLParser):
    def handle_image(self, source, alt, ismap, align, width, height):
        for i in gl.IMG_TYPES:
            if source.find(i) != -1 and source.split('.')[-1] == i[1:] and\
                source[:4] != "http" and source[:4] != "www.":
                if source[0] == '/':
                    source = source[1:]
                if gl.URL.count('/') >= 3:
                    if gl.URL.split('/')[-1].find('.') != -1:
                        # get rid of any bla.html type endings
                        gl.URL = gl.URL[:gl.URL.index(gl.URL.split('/')[gl.URL.count('/')])]
                if gl.URL[-1] == '/':
                    gl.URL = gl.URL[:-1]
                print_links(source, alt)
            if source.find("http") != -1:
                gl.JUST_SOURCE = 1
                if gl.URL[-1] == '/':
                    gl.URL = gl.URL[:-1]
                print_links(source, alt)


def print_links(source, alt):
    text_list = []
    if gl.JUST_SOURCE:
        link_name = source
        text_list.append(link_name)
        if text_list.count(link_name) == 1:
            if not link_name.startswith("http://"):
                link_name = "%s/%s" % (gl.URL, link_name)
            if not link_name in gl.files:
                gl.files.append(link_name)
    else:
        link_name = gl.URL + '/' + source
        text_list.append(link_name)
        if text_list.count(link_name) == 1:
            if not link_name.startswith("http://"):
                link_name = "%s/%s" % (gl.URL, link_name)
            if not link_name in gl.files:
                gl.files.append(link_name)


def html_file():
    parser = TagParse(formatter.NullFormatter())
    try:
        html = urllib2.urlopen(gl.URL).read()
        parser.feed(html)
        parser.close()
    except:
        gl.URL_ERROR = True
        return


def open_url(screen, img):
    gl.ISURL = 1
    paint_screen(gl.BLACK)
    set_caption("Extract from Web - imgv")
    normal_cursor()
    show_message("Enter a Web URL to extract images from", 20, 15, ("transparent"))
    gl.URL = ask(screen, "http://")
    if gl.URL != None:
        gl.files = []
        wait_cursor()
        show_message("Loading. Please wait..", 39, 42, ("transparent"))
        for ext in gl.IMG_TYPES:
            if gl.URL.endswith(ext):
                gl.files.append(str(''.join(gl.URL)))
                return (load_img(gl.files[0]), 1)
    else:
        return img
    gl.files = []
    check_indexhtml()
    if gl.URL_ERROR:
        gl.files.append(gl.ERROR_IMG)
        return (load_img(gl.ERROR_IMG), len(gl.files))
    if len(gl.files) < 1:
        gl.files.append(gl.ERROR_IMG)
    gl.files = [x.replace(' ', '%20') for x in gl.files] # urls need %20 for spaces
    return load_img(gl.files[0])
