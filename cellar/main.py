# -*- coding: utf-8  -*-

from os import listdir, path

from cellar.display import Display
from cellar.game import Game

__all__ = ["MainMenu"]

class MainMenu(object):
    def __init__(self, gamesdir):
        self._gamesdir = gamesdir
        self._games = []
        self._display = Display()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._display.shutdown()

    def __repr__(self):
        return "MainMenu({0!r})".format(self._gamesdir)

    def _load_games(self):
        for item in listdir(self._gamesdir):
            full = path.join(self._gamesdir, item)
            if path.isdir(full) and path.exists(path.join(full, "game.yaml")):
                self._games.append(Game(self._display, full))

    def run(self):
        self._load_games()
        print self._games
        index = int(raw_input("Select a level: "))
        self._display.setup()
        self._games[index].play()
