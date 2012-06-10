# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Player"]

class Player(Object):
    def __init__(self, game, health):
        super(Player, self).__init__()
        self._game = game
        self._health = health

    @property
    def game(self):
        return self._game

    @property
    def health(self):
        return self._health

    @property
    def alive(self):
        return self.health > 0

    def render(self):
        return "@", self.game.display.CYAN | self.game.display.BOLD

    def step(self):
        # Do some user input stuff LOL
        pass
