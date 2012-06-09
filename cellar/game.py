# -*- coding: utf-8  -*-

from os import path

try:
    import yaml
except NameError:
    yaml = None

from cellar.level import Level
from cellar.player import Player

__all__ = ["Game"]

class Game(object):
    def __init__(self, display, gamedir):
        self._display = display
        self._gamedir = gamedir

        self._name = None
        self._entry_level = None
        self._level = None
        self._player = None

        self._load_gamefile()

    def __repr__(self):
        return "Game({0!r})".format(self.gamedir)

    def _load_gamefile(self):
        gamefile = path.join(self.gamedir, "game.yaml")
        with open(gamefile) as fp:
            raw = yaml.load(fp)
        self._name = raw.get("name", path.split(self.gamedir)[1])
        self._entry_level = raw["entryLevel"]

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

    def play(self):
        self._player = Player(100)
        levelfile = path.join(self.gamedir, self._entry_level + ".yaml")
        self._level = Level(levelfile)
        while self.player.alive:
            self.display.render(self.level.map)
            self.display.tick()
