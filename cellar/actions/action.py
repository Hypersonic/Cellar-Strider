# -*- coding: utf-8  -*-

__all__ = ["Action"]

class Action(object):
    def __init__(self, game, data):
        self.game = game
        self.data = data

    def get_duration(self):
        return 1.0 / self.game.display.max_fps

    def execute(self):
        pass
