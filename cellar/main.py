# -*- coding: utf-8  -*-

from os import listdir, path

from cellar.display import Display
from cellar.game import Game

__all__ = ["MainMenu"]

class MainMenu(object):
    def __init__(self, gamesdir, debug):
        self._gamesdir = gamesdir
        self._debug = debug

        self._games = []
        self._display = Display(debug)

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
                self._games.append(Game(self._display, self._debug, full))

    def run(self):
        self._load_games()
        print "Loaded games:"
        for i, game in enumerate(self._games):
            print "\t{0}: {1}".format(i, game.name)
        index = int(raw_input("Select a game ID: "))
        self._display.setup()
        self._games[index].play()
