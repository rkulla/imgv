# help screen code by Ryan Kulla, rkulla@gmail.com
import gl
from usr_event import check_quit
from cursor import normal_cursor, wait_cursor, hover_cursor
from buttons import close_button
from img_screen import get_center, my_update_screen, paint_screen
from load_img import load_img
from show_message import show_message
from res import  adjust_screen, restore_screen
import pygame.font, pygame.event
from pygame.display import update, set_caption
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEMOTION, K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB, K_ESCAPE, K_SPACE
from usr_event import left_click, hit_key
import webbrowser


def command_help(screen, new_img, file, rect):
    (screen, before_winsize, not_accepted) = adjust_screen(screen)

    set_caption("Help [imgv v3.1.6]")
    help(screen)

    screen = restore_screen(screen, before_winsize, not_accepted, new_img, file, rect)

    rect = get_center(screen, new_img)
    my_update_screen(new_img, screen, rect, file)


def help(screen):
    paint_screen(screen, gl.BLACK)
    (screen_width, screen_height) = (screen.get_width(), screen.get_height())
    (esc_rect, font) = close_button(screen)
    show_message(screen, "Main Keyboard Commands", "top", 11, ("bold", "underline", "transparent"))
    key_list = [" Space/N/Ctrl+Tab=Next image, Backspace/B=Previous Image. Ctrl+B=Toggle Image Border ",
                " D=Change Directory ",
                " I=Image Browser ",
                " T=Thumbnails (Space/N/Right-Click=Next. Backspace/B/Middle-Click=Prev. P/Pause=Pause), Ctrl+T=Transparent font ",
                " 4=View four images at a time (Space/N/Right-Click=Next. Backspace/B/Middle-Click=Previous. W=Slideshow) ",
                " W=Slideshow (Space=Skip forward. Backspace=Skip backward. P/Pause=Pause) ",
                " P=Add to Playlist, Ctrl+P=Playlist Options ",
                " C=Close Menu ",
                " F=First Image (Jump to the first image), L=Last Image (Jump to the last image), Ctrl+L=Lock Zoom ",
                " '+'=Zoom In. '-'=Zoom Out. Ctrl+'+'=Zoom In (Double). Ctrl+'-'=Zoom Out (Double). Ctrl+Alt+'+'=Zoom In (Scale2X) ",
                " R=Rotate Right. Ctrl+R=Rotate Left ",
                " Escape=Refresh (Reverts images to original state or reloads after directory changes) ",
                " M=Flip Horizontal (Mirror), V=Flip Vertical ",
                " S=Shuffle, U=Unshuffle ",
                " A=Download Image (Saves remote images to your imgv download directory) ",
                " Delete/Ctrl+W=Close Image, Ctrl+Delete=Permanently delete image from harddisk",
                " X=Hide Image, Ctrl+X=Toggle displaying the main and on-the-fly-Exif status bars ",
                " O=Open URL to extract images from a Website ",
                " F1=Help, F2=640x480, F3=800x600, F4=1024x768, F5=1280x1024, F6/Alt+Enter=Fullscreen, F7=Resize Options ",
                " H=Hand Tool (Allows you to pan/move images on the screen) ",
                " Q=Exit imgv at any time (except when prompted for input) ",
                " Arrow keys=Scroll the image left/right/up/down. PgUp/PgDown/Home/End=full up/full down/full left/full right, (Mouse Wheel=up/down) ",
                " E=Edit ",
                " Z=Image Properties ",
                " 1=Toggle scaling large images to fit the window ",
                " Ctrl+Zero=Fit image to the window, Alt+Zero=Actual Size (Show image at its real size) "]
    key_list.sort()
    if screen_width == 640:
        linesep = 13
        font_size = 9
    else:
        linesep =15
        font_size = 11
    pos = linesep
    for line in key_list:
        show_message(screen, line, (2, pos), font_size, ("transparent"))
        pos += linesep

    mouse_msg = "Main Mouse Commands"
    show_message(screen, mouse_msg, ((screen_width / 2) - (font.size(mouse_msg)[0] / 2), pos, 0, 0), 11, ("bold", "underline", "transparent"))
    mouse_list = [" Left-Click=Select menu options/Load images in Four at a Time, Thumbnail and Image browser/Click buttons and links/Change directories ", " Right-Click=Open or move the main menu/Go forward a page in Four at a Time, Thumbnail and Image Browser/Tag directories ", " Middle-Click=Close the main menu/Go back a page in Four at a Time, Thumbnail and Image Browser ", " Mouse Scroll Wheel=Scroll images that are larger than the screen up or down/Activate the Hand Tool "]
    pos += linesep
    for line in mouse_list:
        show_message(screen, line, (2, pos), font_size, ("transparent"))
        pos += linesep

    gl.MSG_COLOR = gl.BLUE
    doc_msg = "View imgv's online documentation"
    doc_rect = show_message(screen, doc_msg, ((screen_width / 2) - (font.size(doc_msg)[0] / 2), screen_height - 20, 0, 0), 12, ("underline", "bold"))

    donate_msg = "Donate!"
    donate_rect = show_message(screen, donate_msg, ((screen_width) - (font.size(donate_msg)[0] + 70), screen_height - 35, 0, 0), 12, ("bold", "underline"))

    gl.MSG_COLOR = gl.SILVER
    author_msg = "Author: Ryan Kulla"
    show_message(screen, author_msg, ((screen_width) - (font.size(author_msg)[0] - 10), screen_height - 15, 0, 0), 9, ("bold", "transparent"), (7, gl.WHITE))

    normal_cursor()
    print_version(screen, screen_height)
    pygame.event.set_blocked(MOUSEMOTION)
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1)
        cursor = pygame.mouse.get_pos()
        check_quit(event)
        hover_cursor(cursor, (doc_rect, esc_rect, donate_rect))
        if hit_key(event, K_ESCAPE) or hit_key(event, K_SPACE):
           gl.ESCAPED = 1
           gl.MSG_COLOR = gl.MENU_COLOR
           break
        if left_click(event):
            wait_cursor()
            if doc_rect.collidepoint(cursor):
                webbrowser.open("http://imgv.sourceforge.net/doc/", 1, 1)
            if donate_rect.collidepoint(cursor):
                webbrowser.open("http://imgv.sourceforge.net/donate.html", 1, 1)
            elif esc_rect.collidepoint(cursor):
                gl.ESCAPED = 1
                gl.MSG_COLOR = gl.MENU_COLOR
                break


def print_version(screen, screen_height):
    imgvlogo = load_img(gl.IMGV_LOGO_SMALL, screen, False)
    imgvlogo_rect = imgvlogo.get_rect()
    imgvlogo_rect[0] = 5
    imgvlogo_rect[1] = screen_height - 50
    screen.blit(imgvlogo, imgvlogo_rect)
    update(imgvlogo_rect)

    msg = "Version      %s" % gl.IMGV_VERSION
    msg_font = pygame.font.Font(gl.FONT_NAME, 11)
    msg_font.set_bold(1)
    char = 0
    i = 0
    pygame.event.set_blocked(MOUSEMOTION)
    while 1:
        event = pygame.event.poll()
        pygame.time.wait(1)
        check_quit(event)
        if char < len(msg):
            if msg[char] != ' ': # don't delay on spaces
                pygame.time.delay(75)
            ren = msg_font.render(msg[char], 1, gl.RED) # one char at a time
            ren_rect = ren.get_rect()
            # center it
            ren_rect[0] += (i + 7)
            ren_rect[1] = screen_height - 15
            screen.blit(ren, ren_rect)
            i += ren.get_width() # make letters space evenly
            char += 1
            update(ren_rect)
        else:
            break

