# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Wall"]

class Wall(Object):
    def __init__(self, game, x, y, char):
        super(Wall, self).__init__(game, x, y)
        self._char = char

    def render(self):
        return self._char
