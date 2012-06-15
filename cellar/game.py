# -*- coding: utf-8  -*-

from os import path
from time import time

try:
    import yaml
except ImportError:
    yaml = None

from cellar.level import Level
from cellar.objects.player import Player

__all__ = ["Game"]

class Game(object):
    def __init__(self, display, gamedir):
        self._display = display
        self._gamedir = gamedir

        self._playing = False
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
        now = time()
        for i, (when, action, args, kwargs) in enumerate(self._schedule):
            if now >= when:
                self._schedule.pop(i)
                action(*args, **kwargs)

    def _step(self):
        events = self._get_events()
        self._handle_global_events(events)
        self._step_schedule()
        self.level.step(events)
        self.display.render(self.level.map, (self.player.y, self.player.x))
        self.display.tick()

    @property
    def display(self):
        return self._display

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
        self._schedule.append((time() + when, action, args, kwargs))

    def play(self):
        levelfile = path.join(self.gamedir, self._entry_level + ".yaml")
        self._level = Level(self, levelfile)
        self._playing = True
        while self._playing:
            self._step()
