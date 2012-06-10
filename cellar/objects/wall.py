# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Wall"]

class Wall(Object):
    def __init__(self, char):
        super(Wall, self).__init__()
        self._char = char

    def render(self):
        return self._char

    def step(self):
        pass
