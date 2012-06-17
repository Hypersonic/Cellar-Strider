# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Trigger"]

class Trigger(Object):
    def __init__(self, game, x, y, group, actions):
        super(Trigger, self).__init__(game, x, y, visible=False)
        self._group = group
        self._actions = actions

    def _kill_group(self):
        for member in self.game.level.triggers[self._group]:
            member.die()
        del self.game.level.triggers[self._group]

    def step(self, events):
        here = self.game.level.map[self.y][self.x]
        if self.game.player in here:
            self.game.do_actions(self._actions)
            self._kill_group()
