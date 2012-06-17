# -*- coding: utf-8  -*-

import curses
import time

from cellar import __author__, __version__

__all__ = ["Display"]

class Display(object):
    BOLD = curses.A_BOLD
    REVERSE = curses.A_REVERSE

    def __init__(self, debug):
        self._debug = debug
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

    def _block_until_char_with_time_limit(self, char, limit):
        until = time.time() + limit
        while time.time() < until:
            if self.window.getch() == ord(char):
                return True
            time.sleep(0.01)
        return False

    def _crop_map(self, map, center, rows, cols):
        center_row, center_col = center
        total_rows = len(map)
        total_cols = max([len(row) for row in map])

        if total_rows > rows:
            if center_row < rows / 2:  # Top
                map = map[:rows]
            elif center_row > total_rows - rows / 2:  # Bottom
                map = map[total_rows - rows:]
            else:  # Middle, where scrolling magic happens
                top = center_row - rows / 2
                bottom = center_row + rows / 2
                map = map[top:bottom]

        if total_cols > cols:
            if center_col < cols / 2:  # Left
                map = [row[0:cols] for row in map]
            elif center_col > total_cols - cols / 2:  # Right
                map = [row[total_cols - cols:total_cols] for row in map]
            else:  # Middle, where scrolling magic happens
                left = center_col - cols / 2
                right = center_col + cols / 2
                map = [row[left:right] for row in map]
        return map

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

        successful = self._block_until_char_with_time_limit(" ", limit=3)
        if not successful:
            self.window.addstr(row, col + 2, "<space>...", self.BOLD)
            self._block_until_char(" ")
        self.window.deleteln()

    def _render_header(self):
        template = "    Cellar Strider v{0} by {1}    "
        header = template.format(__version__, __author__)
        self.window.addstr(0, 0, header, self.REVERSE)
        if self._debug:
            self.window.addstr(0, len(header) + 1, "DEBUG MODE!", self.BOLD)

    def _render_map(self, map, center):
        rows, cols = self.window.getmaxyx()
        rows -= 4  # Subtract for header and messages
        map = self._crop_map(map, center, rows, cols)
        for row, cells in enumerate(map):
            for col, cell in enumerate(cells):
                for obj in cell:
                    self._render_object(obj, row + 2, col)
        return len(map) + 3

    def _render_messages(self, offset):
        if not self._message_buffer:
            return offset
        for message in self._message_buffer:
            self._render_blocking_message(message, offset)
        self._message_buffer = []

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

    def debug(self, message):
        if self._debug:
            if isinstance(message, list):
                message = [str(msg) for msg in message]
            else:
                message = str(message).splitlines()
            self.window.erase()
            self._render_header()
            self.window.addstr(2, 0, "Debug information:", self.BOLD)
            row = 4
            for msg in message:
                self.window.addstr(row, 0, msg)
                row += 1
            self.window.addstr(row + 1, 0, "Press <space> to resume...")
            self.window.refresh()
            self._block_until_char(" ")

    def message(self, messages):
        self._message_buffer += messages

    def show_menu(self, builder):
        while 1:
            lines = builder()
            if not lines:
                return
            self.window.erase()
            self._render_header()
            for row, col, line, flags in lines:
                if flags:
                    self.window.addstr(row + 2, col, line, flags)
                else:
                    self.window.addstr(row + 2, col, line)
            self.tick()

    def render(self, map, center):
        self.window.erase()
        self._render_header()
        offset = self._render_map(map, center)
        self._render_messages(offset)
        self.window.refresh()

    def tick(self):
        wait = (1.0 / self._max_fps) - (time.time() - self._last_update_time)
        if wait > 0:
            time.sleep(wait)
        self._last_update_time = time.time()
