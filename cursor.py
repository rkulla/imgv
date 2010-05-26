# imgv mouse cursor code by Ryan Kulla, rkulla@gmail.com
import gl
from pygame.mouse import set_cursor
import pygame.cursors


def wait_cursor():
    set_cursor(*pygame.cursors.diamond)


def normal_cursor():
    set_cursor(*pygame.cursors.tri_left)


def click_hand_cursor():
    clickhand = (          #24x24
      "       ..               ",
      "      .XX.              ",
      "      .XX.              ",
      "      .XX.              ",
      "      .XX.              ",
      "      .XX...            ",
      "      .XX.XX...         ",
      "      .XX.XX.XX..       ",
      "      .XX.XX.XX.X.      ",
      "  ... .XX.XX.XX.XX.     ",
      " .XXX..XXXXXXXX.XX.     ",
      "  .XXX.XXXXXXXXXXX.     ",
      "   .XX.XXXXXXXXXXX.     ",
      "    .XXXXXXXXXXXXX.     ",
      "     .XXXXXXXXXXXX.     ",
      "     .XXXXXXXXXXXX.     ",
      "      .XXXXXXXXXX.      ",
      "      .XXXXXXXXXX.      ",
      "       .XXXXXXXX.       ",
      "       .XXXXXXXX.       ",
      "        ........        ",
      "                        ", 
      "                        ",
      "                        ",
    )
    curs, mask = pygame.cursors.compile(clickhand, 'X', '.')
    set_cursor((24, 24), (7, 0), curs, mask)


def drag_hand_cursor():
    draghand = (           #24x24
      "                        ",
      "                        ",
      "         ..             ",
      "    ..  .XX...          ",
      "   .XX. .XX.XX.         ",
      "    .XX..XX.XX...       ",
      "    .XX..XX.XX..X.      ",
      "     .XX.XX.XX.XX.      ",
      " ... .XXXXXXXX.XX.      ",
      " .XX..XXXXXXXXXXX.      ",
      "  .XX.XXXXXXXXXX.       ",
      "  .XXXXXXXXXXXXX.       ",
      "   .XXXXXXXXXXXX.       ",
      "    .XXXXXXXXXX.        ",
      "    .XXXXXXXXXX.        ",
      "     .XXXXXXXX.         ",
      "      .XXXXXX.          ",
      "      .XXXXXX.          ",
      "      .      .          ", 
      "                        ", 
      "                        ",
      "                        ",
      "                        ",
      "                        ",
    )
    curs, mask = pygame.cursors.compile(draghand, 'X', '.')
    set_cursor((24, 24), (7, 0), curs, mask)


def grab_hand_cursor(): 
    grabhand = (           #24x24
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "                        ",
      "     .........          ",
      "    .XX..XX.XX...       ",
      "     .XX.XX.XX.XX.      ",
      "     .XXXXXXXX.XX.      ",
      "    ..XXXXXXXXXXX.      ",
      "   .X.XXXXXXXXXX.       ",
      "  .XXXXXXXXXXXXX.       ",
      "   .XXXXXXXXXXXX.       ",
      "    .XXXXXXXXXX.        ",
      "    .XXXXXXXXXX.        ",
      "     .XXXXXXXX.         ",
      "      .XXXXXX.          ",
      "      .XXXXXX.          ",
      "      .      .          ", 
      "                        ", 
      "                        ",
      "                        ",
      "                        ",
      "                        ",
    )
    curs, mask = pygame.cursors.compile(grabhand, 'X', '.')
    set_cursor((24, 24), (7, 0), curs, mask)


def hover_cursor(cursor, rects):
    " takes a tuple of rects and displays hand cursor when hovered over "
    for r in rects:
        if r.collidepoint(cursor):
            click_hand_cursor()
            break
    else: # for else :)
        normal_cursor()
