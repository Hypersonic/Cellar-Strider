# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Player"]

class Player(Object):
    def __init__(self, game, health):
        super(Player, self).__init__(game)
        self._health = health

    @property
    def health(self):
        return self._health

    def render(self):
        return "@", self.game.display.CYAN | self.game.display.BOLD

    def step(self, events):
        # Do some user input stuff LOL
        if self.health <= 0:
            self.game.schedule(2, self.game.end)
            self.die()
