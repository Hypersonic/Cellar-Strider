# -*- coding: utf-8  -*-

from os import path

try:
    import yaml
except ImportError:
    yaml = None

from cellar.actions import get_action
from cellar.level import Level
from cellar.objects.player import Player

__all__ = ["Game"]

class Game(object):
    def __init__(self, display, debug, gamedir):
        self._display = display
        self._debug = debug
        self._gamedir = gamedir

        self._playing = False
        self._clock = 0
        self._name = None
        self._entry_level = None
        self._level = None
        self._player = None
        self._schedule = []

        self._load()

    def __repr__(self):
        return "Game({0!r})".format(self.gamedir)

    def _load(self):
        gamefile = path.join(self.gamedir, "game.yaml")
        with open(gamefile) as fp:
            raw = yaml.load(fp)
        self._name = raw.get("name", path.split(self.gamedir)[1])
        self._entry_level = raw["entryLevel"]
        self._player = Player(self, raw.get("playerHealth", 100))

    def _get_events(self):
        events = []
        key = self.display.window.getch()
        while key > -1:
            if key not in events:
                events.append(key)
            key = self.display.window.getch()
        return events

    def _handle_global_events(self, events):
        if ord("q") in events:
            self.end()

    def _step_schedule(self):
        for i, (when, action, args, kwargs) in enumerate(self._schedule):
            if self._clock >= when:
                self._schedule.pop(i)
                action(*args, **kwargs)

    def _step(self):
        events = self._get_events()
        self._handle_global_events(events)
        self._step_schedule()
        self.level.step(events)
        self.display.render(self.level.map, (self.player.y, self.player.x))
        self.display.tick()
        self._clock += 1

    def _update_inventory(self, player, events):
        if ord("w") in events and player.inventory:
            if not player.current_item:
                player.current_item = player.inventory[-1]
            else:
                index = player.inventory.index(player.current_item)
                if index == 0:
                    player.current_item = None
                else:
                    player.current_item = player.inventory[index - 1]

        if ord("s") in events and player.inventory:
            if not player.current_item:
                player.current_item = player.inventory[0]
            else:
                index = player.inventory.index(player.current_item)
                try:
                    player.current_item = player.inventory[index + 1]
                except IndexError:
                    player.current_item = None

    def _build_inventory(self):
        events = self._get_events()
        if ord("q") in events:
            self.end()
            return None
        elif ord(" ") in events:
            return None
        self._update_inventory(self.player, events)

        lines = [
            (0, 0, "Your inventory:", self.display.BOLD),
            (2, 4, "-", None),
            (2, 6, "Nothing", self.display.REVERSE if not self.player.current_item else None)
        ]

        row = 3
        for item in self.player.inventory:
            lines.append((row, 4, "-", None))
            if item is self.player.current_item:
                lines.append((row, 6, item.name, self.display.REVERSE))
            else:
                lines.append((row, 6, item.name, None))
            row += 1
        return lines

    @property
    def display(self):
        return self._display

    @property
    def debug(self):
        return self._debug

    @property
    def gamedir(self):
        return self._gamedir

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def player(self):
        return self._player

    def end(self):
        self._playing = False

    def schedule(self, when, action, args=None, kwargs=None):
        if not args:
            args = ()
        if not kwargs:
            kwargs = {}
        end = self._clock + self.display.max_fps * when
        self._schedule.append((end, action, args, kwargs))

    def do_actions(self, actions):
        offset = 0
        for action in actions:
            runner, duration = get_action(self, action)
            if offset:
                self.schedule(offset, runner)
            else:
                runner()
            offset += duration

    def show_inventory(self):
        self.display.show_menu(self._build_inventory)        

    def play(self):
        levelfile = path.join(self.gamedir, self._entry_level + ".yaml")
        self._level = Level(self, levelfile)
        self._playing = True
        while self._playing:
            self._step()
