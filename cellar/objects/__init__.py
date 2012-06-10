# -*- coding: utf-8  -*-

__all__ = ["Object"]

class Object(object):
    def __init__(self, game):
        self._game = game
        self._visible = True

    @property
    def game(self):
        return self._game

    @property
    def is_visible(self):
        return self._visible

    def die(self):
        self.game.level.remove(self)

    def render(self):
        pass

    def step(self, events):
        pass
