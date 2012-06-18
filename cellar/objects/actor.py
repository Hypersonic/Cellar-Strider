# -*- coding: utf-8  -*-

from copy import deepcopy

from cellar.actions import get_action
from cellar.objects import Object

__all__ = ["Actor"]

class Actor(Object):
    _is_actor = True  # LOL, what is duck typing? - Ben

    def __init__(self, game, x, y, char, name, group, visible, color,
                 start, die, attributes):
        super(Actor, self).__init__(game, x, y, visible)
        self._char = char
        self._name = name
        self._group = group
        self._color = color
        self._action_queue = deepcopy(start)
        self._on_die = deepcopy(die)
        self._attributes = deepcopy(attributes)

    def _highlight(self):
        self._old_color = self._color
        self._color = (self.game.display.WHITE | self.game.display.REVERSE |
                       self.game.display.BOLD)

    def _unhighlight(self):
        self._color = self._old_color

    def _is_invincible(self):
        return self._color == (self.game.display.WHITE |
                               self.game.display.REVERSE |
                               self.game.display.BOLD)

    @property
    def attributes(self):
        return self._attributes

    def die(self):
        if self._alive:
            self._alive = False
            self.game.do_actions(self._on_die)
            self.game.level.map[self.y][self.x].remove(self)
            self.game.level.objects[self._name].remove(self)
            self.game.level.object_groups[self._group].remove(self)

    def render(self):
        return self._char, self._color

    def hit(self, damage):
        if "health" in self.attributes:
            if self._is_invincible():
                return
            self.attributes["health"] -= damage
            self._highlight()
            if self.attributes["health"] <= 0:
                self.attributes["health"] = 0
                oper = self.die
            else:
                oper = self._unhighlight
            self.game.schedule(0.2, oper)

    def step(self, events):
        if self._action_queue:
            for action in self._action_queue:
                action["actor"] = self
            self.game.do_actions(self._action_queue)
            self._action_queue = []
