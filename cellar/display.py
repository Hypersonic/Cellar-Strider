# -*- coding: utf-8  -*-

import curses
import time

from cellar import __author__, __version__

__all__ = ["Display"]

class Display(object):
    BOLD = curses.A_BOLD
    REVERSE = curses.A_REVERSE

    def __init__(self):
        self._window = None
        self._max_fps = 15
        self._message_scroll_fps = 50
        self._color_table = {}
        self._message_buffer = []
        self._last_update_time = time.time()

    def _block_until_char(self, char):
        self.window.nodelay(0)
        while self.window.getch() != ord(char):
            pass
        self.window.nodelay(1)

    def _render_object(self, obj, row, col):
        if not obj.is_visible:
            return
        char = obj.render()
        if isinstance(char, tuple):
            self.window.addch(row, col, char[0], char[1])
        else:
            self.window.addch(row, col, char)

    def _render_blocking_message(self, message, row):
        maxwidth = sum([len(msg) for msg, flags in message])
        i = 0
        while i < maxwidth:
            col = 0
            if self.window.getch() == ord(" "):
                i = maxwidth
            for msg, flags in message:
                for char in msg:
                    if col > i:
                        break
                    if flags:
                        self.window.addch(row, col, char, flags)
                    else:
                        self.window.addch(row, col, char)
                    col += 1
            self.window.refresh()
            time.sleep(1.0 / self._message_scroll_fps)
            i += 1

        self.window.refresh()
        self._block_until_char(" ")
        self.window.deleteln()

    def _render_header(self, offset=0):
        template = "    Cellar Strider v{0} by {1}    "
        header = template.format(__version__, __author__)
        self.window.addstr(header, self.REVERSE)
        return offset + 2

    def _render_map(self, map, offset=0):
        for row, cells in enumerate(map):
            for col, cell in enumerate(cells):
                for obj in cell:
                    self._render_object(obj, row + offset, col)
        return offset + len(map) + 1

    def _render_messages(self, offset=0):
        if not self._message_buffer:
            return offset
        for message in self._message_buffer:
            self._render_blocking_message(message, offset)
        self._message_buffer = []
        return offset + 2

    @property
    def window(self):
        return self._window

    @property
    def max_fps(self):
        return self._max_fps

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
        def def_color(num, color, no_init=False):
            name = "COLOR_" + color
            if not no_init:
                color_code = getattr(curses, name)
                curses.init_pair(num, color_code, curses.COLOR_BLACK)
            pair = curses.color_pair(num)
            setattr(self, color, pair)
            self._color_table[color.lower()] = pair

        def_color(0, "WHITE", no_init=True)
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

    def convert_color(self, name):
        return self._color_table[name]

    def message(self, messages):
        self._message_buffer += messages

    def render(self, map):
        self.window.erase()
        offset = self._render_header()
        offset = self._render_map(map, offset)
        self._render_messages(offset)
        self.window.refresh()

    def tick(self):
        wait = (1.0 / self._max_fps) - (time.time() - self._last_update_time)
        if wait > 0:
            time.sleep(wait)
        self._last_update_time = time.time()
