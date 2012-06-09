# -*- coding: utf-8  -*-

import curses
import time

__all__ = ["Display"]

class Display(object):
    def __init__(self):
        self._max_fps = 10
        self._window = None

        self._last_update_time = time.time()


    @property
    def max_fps(self):
        return self._max_fps

    @property
    def window(self):
        return self._window

    @max_fps.setter
    def max_fps(self, value):
        self._max_fps = value

    def setup(self):
        self._window = curses.initscr()  # Initialize curses
        curses.start_color()  # Allow color manipulation
        curses.noecho()  # Don't echo stdin
        curses.cbreak()  # Disable stdin line buffering
        self.window.keypad(1)  # Interpret escape sequences correctly
        self.window.nodelay(1)  # Do not block getting characters from stdin

        # Set up colors:
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_RED)

    def shutdown(self):
        if not self.window:
            return

        self.window.keypad(0)  # Don't break escape sequences
        curses.nocbreak()  # Restore stdin line buffering
        curses.echo()  # Restore echoing stdin
        curses.endwin()  # Shut down curses

    def render(self, map):
        self.window.erase()
        for row, chars in enumerate(map):
            for col, char in enumerate(chars):
                self.window.addch(row, col, char)
        self.window.refresh()

    def tick(self):
        wait = (1.0 / self._max_fps) - (time.time() - self._last_update_time)
        if wait > 0:
            time.sleep(wait)
        self._last_update_time = time.time()
