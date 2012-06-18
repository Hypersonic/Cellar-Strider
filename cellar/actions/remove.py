# -*- coding: utf-8  -*-

from cellar.actions import Action

__all__ = ["RemoveAction"]

class RemoveAction(Action):
    def execute(self):
        targets = self.game.level.get_actors(self.data["target"])
        for target in targets:
            target.die()
