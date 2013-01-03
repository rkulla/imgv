# image slideshow code by Ryan Kulla, rkulla@gmail.com
import gl
from string import digits
from show_message import show_message
from buttons import close_button
from cursor import normal_cursor, wait_cursor, hover_cursor
from load_timers import check_timer, start_timer
from img_screen import paint_screen, get_center, my_update_screen
from img_surf import next_img
from usr_event import check_quit, hit_key, left_click
from screensaver import disable_screensaver, enable_screensaver
import pygame.event
import pygame.mouse
import pygame.time
import pygame.font
import pygame.key
from pygame.display import update, set_caption, set_mode
from pygame.locals import K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_p, K_TAB, K_SPACE, K_BACKSPACE, K_RETURN, K_KP_ENTER, KEYDOWN, MOUSEMOTION, K_ESCAPE, K_PAUSE, K_DELETE, K_KP_PERIOD, RESIZABLE


def stopped_msg(screen):
    gl.SLIDE_SHOW_RUNNING = 0
    set_caption("[Slideshow Stopped] - imgv")
    enable_screensaver()
    show_message("Stopped", 30, 23, ("bold"))
    pygame.time.wait(1000) # display the stopped message for 1 second


def pause(screen):
    while 1:
        set_caption("[Slideshow Paused] - imgv")
        ren_rect = show_message("Paused", 30, 23, ("bold"))
        event = pygame.event.wait()
        check_quit(event)
        if event.type == KEYDOWN and event.key not in(K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_TAB):
            set_caption("Slideshow = imgv")
            paint_screen(screen, gl.BLACK, ren_rect)
            break


def my_slideshow(new_img, img, screen, file, rect):
    num_imgs = len(gl.files)
    if not gl.TOGGLE_FULLSCREEN_SET:
        screen = set_mode(screen.get_size())
    set_caption("Slideshow Options - imgv")
    speed = get_speed(screen, new_img, rect, gl.files[file], file)
    if not speed == -1: # didn't hit Esc from get_speed:
        gl.SLIDE_SHOW_RUNNING = 1
        disable_screensaver()
        dont_call = 0
        pygame.event.set_blocked(MOUSEMOTION)
        while 1:
            event = pygame.event.poll()
            pygame.time.wait(1)
            check_quit(event)
            if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_p, K_PAUSE, K_TAB, K_SPACE, K_BACKSPACE):
                stopped_msg(screen)
                my_update_screen(new_img, rect, file)
                file = file - 1
                break
            if hit_key(event, K_p) or hit_key(event, K_PAUSE):
                pause(screen)
                my_update_screen(new_img, rect, file)
            if dont_call == 1:
                break
            if not gl.WRAP_SLIDESHOW:
                if file < num_imgs:
                    (new_img, file, rect, dont_call) = show_slideshow_img(screen, new_img, file, speed)
            if gl.WRAP_SLIDESHOW:
                if file >= num_imgs:
                    file = 0
                (new_img, file, rect, dont_call) = show_slideshow_img(screen, new_img, file, speed)
            pygame.time.delay(5) # don't hog CPU
    if not gl.TOGGLE_FULLSCREEN_SET:
        screen = set_mode(screen.get_size(), RESIZABLE)
    return (new_img, new_img, new_img, file, rect)


def show_slideshow_img(screen, new_img, file, speed):
    start = start_timer()
    wait_cursor()
    new_img = next_img(file, new_img, screen)
    rect = get_center(screen, new_img)
    ns = check_timer(start)
    my_update_screen(new_img, rect, file, ns)
    normal_cursor()
    if speed > 0:
        for i in range(speed):
            # trick delay into letting you escape anytime
            event = pygame.event.poll()
            pygame.time.wait(1)
            if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL,\
                K_p, K_PAUSE, K_TAB, K_SPACE, K_BACKSPACE):
                stopped_msg(screen)
                my_update_screen(new_img, rect, file)
                return (new_img, file, rect, 1)
            if hit_key(event, K_p) or hit_key(event, K_PAUSE):
                pause(screen)
                my_update_screen(new_img, rect, file)
            if hit_key(event, K_SPACE):
                # skip forward an image immediately
                file = file + 1
                return (new_img, file, rect, 0)
            if hit_key(event, K_BACKSPACE):
                # skip backward an image immediately
                file = file - 1
                return (new_img, file, rect, 0)
            pygame.time.delay(1000) # check every second
    file = file + 1
    return (new_img, file, rect, 0)


def get_speed(screen, new_img, rect, filename, file):
    "get input from keyboard (including number pad) and only accept/display digits"
    paint_screen(screen, gl.BLACK)
    normal_cursor()
    DEFAULT_SPEED = 5
    MAX_SPEED = 100000
    speed_msg = " Enter number of seconds to delay between images (Default=5): _ "
    speed = ['0']
    char_space = 0
    screen_midtop = (screen.get_rect().midtop[0], screen.get_rect().midtop[1] + 20)
    font = pygame.font.Font(gl.FONT_NAME, 13)
    ren_speed_msg = font.render(speed_msg, 1, gl.MSG_COLOR)
    ren_speed_msg_rect = ren_speed_msg.get_rect()
    ren_speed_msg_width = ren_speed_msg.get_width()
    ren_speed_msg_rect.midtop = screen_midtop
    screen.blit(ren_speed_msg, ren_speed_msg_rect)
    update(ren_speed_msg_rect)
    (esc_rect, close_font) = close_button(screen)
    my_digits = [] # keypad number list.
    dirty_rects = []
    for num in range(10):
        my_digits.append('[%d]' % num) # [0],[1]...[9]
    pygame.event.set_allowed(MOUSEMOTION)
    while 1:
        event = pygame.event.wait()
        cursor = pygame.mouse.get_pos()
        hover_cursor(cursor, (esc_rect,))
        if event.type == KEYDOWN and not event.key == K_RETURN:
            speed_input = pygame.key.name(event.key)
            try:
                check_quit(event)
                if speed_input in my_digits or speed_input in digits:
                    # only echo digits (0-9)
                    for i in speed_input:
                        # extract n from brackets, [n]
                        if i in digits:
                            speed_input = i
                    speed.append(speed_input)
                    ren_speed = font.render(speed_input, 1, gl.MSG_COLOR, gl.BLACK)
                    ren_speed_rect = ren_speed.get_rect()
                    ren_speed_rect.midtop = screen_midtop
                    # dividing by 2.12 allows to overwrite the "_" fake cursor marker:
                    ren_speed_rect[0] = ren_speed_rect[0] + (char_space + (ren_speed_msg_width / 2.12) + 5)
                    dirty_rects.append(ren_speed_rect)
                    screen.blit(ren_speed, ren_speed_rect)
                    update(ren_speed_rect)
                    char_space = char_space + ren_speed.get_width()
            except TypeError:
                # don't crash if user hits Backspace, Esc, etc.
                pass
        if hit_key(event, K_RETURN) or hit_key(event, K_KP_ENTER):
            break
        if left_click(event):
            if esc_rect.collidepoint(cursor):
                wait_cursor()
                my_update_screen(new_img, rect, file)
                normal_cursor()
                return -1
        if hit_key(event, K_ESCAPE):
            wait_cursor()
            my_update_screen(new_img, rect, file)
            normal_cursor()
            return -1
        if hit_key(event, K_BACKSPACE) or hit_key(event, K_DELETE) or hit_key(event, K_KP_PERIOD):
            # erase whatever text was inputed
            speed = ['0']
            try:
                for rect in dirty_rects:
                    paint_screen(screen, gl.BLACK, rect)
                char_space = ren_speed.get_width()
            except:
                pass
    # convert to a valid speed
    if not len(speed) > 1:
        speed.append(str(DEFAULT_SPEED))
    speed = int(''.join(speed))
    if speed > MAX_SPEED:
        speed = DEFAULT_SPEED
    return speed

