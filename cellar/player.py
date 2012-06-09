# -*- coding: utf-8  -*-

__all__ = ["Player"]

class Player(object):
    def __init__(self, health):
        self._health = health

    @property
    def health(self):
        return self._health

    @property
    def alive(self):
        return self.health > 0
