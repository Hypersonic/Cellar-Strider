# -*- coding: utf-8  -*-

from cellar.actions import get_action
from cellar.objects import Object

__all__ = ["Actor"]

class Actor(Object):
    def __init__(self, game, x, y, char, name, group, visible, color,
                 start, attributes):
        super(Actor, self).__init__(game, x, y, visible)
        self._char = char
        self._name = name
        self._group = group
        self._color = color
        self._attributes = attributes
        
        for action in start:
            action["actor"] = self
        self.game.do_actions(start)

    def die(self):
        self.game.level.map[self.y][self.x].remove(self)
        self.game.level.objects[self._name].remove(self)
        self.game.level.object_groups[self._group].remove(self)

    def render(self):
        return self._char, self._color
