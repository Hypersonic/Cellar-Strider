# -*- coding: utf-8  -*-

__all__ = ["Action"]

class Action(object):
    def __init__(self, game, data):
        self.game = game
        self.data = data

    def get_duration(self):
        return 0

    def execute(self):
        pass
