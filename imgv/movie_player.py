# imgv movie playing code by Ryan Kulla, rkulla@gmail.com
import gl
import os.path
from cursor import normal_cursor, wait_cursor
from img_screen import clean_screen, paint_screen
from usr_event import left_click
from show_message import show_message
import pygame.image, pygame.mixer, pygame.movie, pygame.event, pygame.mouse
from pygame.display import flip, set_caption
from pygame.locals import *


def load_movie(screen, movie_file, *options):
    vol = 0.5  # volume starting half way. min is 0.0 max is 1.0
    paused = 0
    skipped = 0
    image = pygame.image.load(gl.MOVIE_FILE).convert()
    paint_screen(gl.BLACK)

    pygame.mixer.quit()  # so sound in the movie works
    set_caption("imgv - %s" % movie_file)
    movie = pygame.movie.Movie(movie_file)
    screen_center = ((screen.get_width() / 2) - (movie.get_size()[0] / 2), ((screen.get_height() / 2)) -\
                     (movie.get_size()[1] / 2))  # where to center the movie
    if len(options) > 0:
        if options[0] == "fitwindow":
            movie.set_display(screen, (0, 0, screen.get_width(), screen.get_height()))
    else:
        movie.set_display(screen, screen_center)

    if len(movie_file) > 70:
        movie_name = movie_file[:70] + '...'
    else:
        movie_name = movie_file
    movie.play()
    movie.set_volume(vol)
    normal_cursor()
    mute_rect = show_message("Mute", (20, 0), 12)
    lower_rect = show_message("Lower", (80, 0), 12)
    louder_rect = show_message("Louder", (140, 0), 12)
    pause_rect = show_message("Pause", (200, 0), 12)
    stop_rect = show_message("Stop", (260, 0), 12)
    skip_rect = show_message("Skip-Half", (320, 0), 12)
    fw_rect = show_message("Fit-Window", (400, 0), 12)
    show_message("(%d:%02.f)" % (movie.get_length() / 60, movie.get_length() % 60), (480, 0), 12)
    if gl.TOGGLE_STATUS_BAR:
        show_message("%s/%s, %s" % (gl.files.index(movie_file) + 1, len(gl.files),\
        os.path.basename(movie_name)), "bottom", 12)
    flip()#
    while movie:
        if not movie.get_busy() and not paused and gl.SLIDE_SHOW_RUNNING:
            break
        for event in pygame.event.get():
            cursor = pygame.mouse.get_pos()
            if event.type == KEYDOWN and event.key == K_q or event.type == QUIT:
                wait_cursor()
                movie.stop()
                movie = None
                clean_screen()
                raise SystemExit
            if event.type == KEYDOWN and event.key not in (K_LALT, K_RALT, K_LCTRL, K_RCTRL, K_p, K_TAB):
                movie.stop()
                movie = None
                return image
            if left_click(event):
                if mute_rect.collidepoint(cursor):
                    movie.set_volume(0)
                    break
                if lower_rect.collidepoint(cursor):
                    if vol >= 0.0:
                        vol = vol - 0.2
                        movie.set_volume(vol)
                        break
                if louder_rect.collidepoint(cursor):
                    if vol <= 1.0:
                        vol = vol + 0.2
                        movie.set_volume(vol)
                        break
                if pause_rect.collidepoint(cursor):
                    if paused:
                        paused = 0
                    else:
                        paused = 1
                    movie.pause()
                    break
                if stop_rect.collidepoint(cursor):
                    movie.stop()
                    movie = None
                    return image
                if skip_rect.collidepoint(cursor):
                    if not skipped:
                        movie.skip(movie.get_length() / 2)
                    break
                if fw_rect.collidepoint(cursor):
                    movie.stop()
                    movie = None
                    image = load_movie(screen, movie_file, "fitwindow")
                    break
    movie = None
    return image
