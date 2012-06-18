# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Player"]

class Player(Object):
    def __init__(self, game, health):
        super(Player, self).__init__(game, 0, 0)
        self._health = health

        self._inventory = []
        self._current_item = None

    @property
    def health(self):
        return self._health

    @property
    def inventory(self):
        return self._inventory

    @property
    def current_item(self):
        return self._current_item

    @health.setter
    def health(self, value):
        self._health = value

    @current_item.setter
    def current_item(self, value):
        self._current_item = value

    def render(self):
        return "@", self.game.display.CYAN | self.game.display.BOLD

    def step(self, events):
        for key in events:
            if key == ord("w"):
                self.move(0, -1)
            elif key == ord("a"):
                self.move(-1, 0)
            elif key == ord("s"):
                self.move(0, 1)
            elif key == ord("d"):
                self.move(1, 0)
            elif key == ord("i"):
                self.game.show_inventory()
            elif key == ord(" "):
                if self._current_item:
                    self._current_item.use()
        if self.health <= 0:
            self.game.schedule(2, self.game.end)
            self.die()

    def hit(self, damage):
        self.health -= damage
