# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Actor"]

class Actor(Object):
    def __init__(self, game, x, y, char, name, group, visible, color,
                 attributes):
        super(Actor, self).__init__(game, x, y, visible)
        self._char = char
        self._name = name
        self._group = group
        self._color = color
        self._attributes = attributes

    def render(self):
        return self._char, self._color

    def step(self, events):
        pass
