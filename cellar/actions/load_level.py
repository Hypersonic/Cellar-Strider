# -*- coding: utf-8  -*-

from cellar.actions import Action

__all__ = ["LoadLevelAction"]

class LoadLevelAction(Action):
    def _load(self):
        self.game.clear_schedule()
        name = self.data["level"]
        self.game.level = name

    def execute(self):
        self.game.schedule(0, self._load)
