# -*- coding: utf-8  -*-

from cellar.actions import Action

__all__ = ["LoadLevelAction"]

class LoadLevelAction(Action):
    def execute(self):
        name = self.data["level"]
        self.game.level = name
