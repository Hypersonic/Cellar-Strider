# -*- coding: utf-8  -*-

import curses
import time

from cellar import __author__, __version__

__all__ = ["Display"]

class Display(object):
    BOLD = curses.A_BOLD

    def __init__(self):
        self._max_fps = 10
        self._window = None

        self._last_update_time = time.time()

    def _display_header(self):
        template = "    Cellar Strider v{0} by {1}    "
        header = template.format(__version__, __author__)
        self.window.addstr(header, curses.A_REVERSE)

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
        def def_color(num, color):
            name = "COLOR_" + color
            curses.init_pair(num, getattr(curses, name), curses.COLOR_BLACK)
            setattr(self, color, curses.color_pair(num))

        def_color(1, "BLACK")
        def_color(2, "BLUE")
        def_color(3, "CYAN")
        def_color(4, "GREEN")
        def_color(5, "MAGENTA")
        def_color(6, "RED")
        def_color(7, "YELLOW")

    def shutdown(self):
        if not self.window:
            return
        self.window.keypad(0)  # Don't break escape sequences
        curses.nocbreak()  # Restore stdin line buffering
        curses.echo()  # Restore echoing stdin
        curses.endwin()  # Shut down curses

    def render(self, map):
        self.window.erase()
        self._display_header()
        for row, objects in enumerate(map):
            for col, obj in enumerate(objects):
                if not obj:
                    continue
                if not obj.is_visible:
                    continue
                char = obj.render()
                if isinstance(char, tuple):
                    self.window.addch(row + 2, col, char[0], char[1])
                else:
                    self.window.addch(row + 2, col, char)
        self.window.refresh()

    def tick(self):
        wait = (1.0 / self._max_fps) - (time.time() - self._last_update_time)
        if wait > 0:
            time.sleep(wait)
        self._last_update_time = time.time()
