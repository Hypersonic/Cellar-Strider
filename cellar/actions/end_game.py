# -*- coding: utf-8  -*-

from cellar.actions import Action

__all__ = ["EndGameAction"]

class EndGameAction(Action):
    def execute(self):
        self.game.end()
