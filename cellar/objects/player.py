# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Player"]

class Player(Object):
    def __init__(self, game, health):
        super(Player, self).__init__(game, 0, 0)
        self._health = health

        self._inventory = []
        self._current_item = None
        self._invincible = False

    def _reset_invincibility(self):
        self.invincible = False

    @property
    def health(self):
        return self._health

    @property
    def inventory(self):
        return self._inventory

    @property
    def current_item(self):
        return self._current_item

    @property
    def invincible(self):
        return self._invincible

    @health.setter
    def health(self, value):
        self._health = value

    @current_item.setter
    def current_item(self, value):
        self._current_item = value

    @invincible.setter
    def invincible(self, value):
        self._invincible = value

    def die(self):
        if self._alive:
            self._alive = False
            self.game.level.map[self.y][self.x].remove(self)
            self.game.level.objects["PLAYER"].remove(self)
            self.game.level.object_groups["PLAYER"].remove(self)
            self.game.schedule(2, self.game.end)
            self.game.display.flash()

    def render(self):
        if self.invincible:
            return "@", (self.game.display.CYAN | self.game.display.BOLD |
                         self.game.display.REVERSE)
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

        if self.health == -1:
            self.health = 0  # Don't trigger this again
            self.invincible = True
            next = 2.0 / self.game.display.max_fps
            self.game.schedule(next, self.die)

    def hit(self, damage):
        if self.invincible:
            return

        self.health -= damage
        if self.health <= 0:
            self.health = -1

        self.game.display.beep()
        self.invincible = True
        next = 1.0 / self.game.display.max_fps
        self.game.schedule(next, self._reset_invincibility)
