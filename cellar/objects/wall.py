# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Wall"]

class Wall(Object):
    def __init__(self, game, char):
        super(Wall, self).__init__(game)
        self._char = char

    def render(self):
        return self._char
