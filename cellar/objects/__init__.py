# -*- coding: utf-8  -*-

__all__ = ["Object"]

class Object(object):
    def __init__(self, game, x, y, visible=True):
        self._game = game
        self._x = x
        self._y = y
        self._visible = visible
        self._alive = True

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

    @property
    def is_alive(self):
        return self._alive

    def move(self, dx, dy, noclip=False):
        if not self._alive:
            return

        destination = self.game.level.map[self.y + dy][self.x + dx]
        if not noclip:
            collisions = [obj.is_visible for obj in destination]
            if any(collisions):
                return

        current = self.game.level.map[self.y][self.x]
        current.remove(self)
        destination.append(self)
        self.x += dx
        self.y += dy

    def die(self):
        self.game.level.map[self.y][self.x].remove(self)
        self._alive = False

    def render(self):
        pass

    def step(self, events):
        pass
