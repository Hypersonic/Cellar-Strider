# -*- coding: utf-8  -*-

__all__ = ["Object"]

class Object(object):
    def __init__(self, game, x, y):
        self._game = game
        self._x = x
        self._y = y
        self._visible = True

    @property
    def game(self):
        return self._game

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def is_visible(self):
        return self._visible

    def move(self, dx, dy, noclip=False):
        self.game.level.map[self.y][self.x].remove(self)
        self.x += dx
        self.y += dy
        self.game.level.map[self.y][self.x].append(self)

    def die(self):
        self.game.level.map[self.y][self.x].remove(self)

    def render(self):
        pass

    def step(self, events):
        pass
