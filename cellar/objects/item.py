# -*- coding: utf-8  -*-

from random import choice

from cellar.objects import Object

__all__ = ["Item"]

class Item(Object):
    def __init__(self, game, name, itemtype, attributes):
        super(Item, self).__init__(game, 0, 0, visible=False)
        self._name = name
        self._type = itemtype
        self._attributes = attributes

    def _get_point_carefully(self, x, y):
        try:
            cell = self.game.level.map[y][x]
        except IndexError:
            return None
        return [obj for obj in cell if hasattr(obj, "_is_actor")]

    def _get_distance(self, a, b):
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

    def _use_weapon(self):
        x, y = self.game.player.x, self.game.player.y
        neighbors = [
            self._get_point_carefully(x + 1, y),
            self._get_point_carefully(x - 1, y),
            self._get_point_carefully(x, y + 1),
            self._get_point_carefully(x, y - 1)
        ]
        targets = [neighbor for neighbor in neighbors if neighbor]
        if targets:
            target = choice(targets)
            for obj in target:
                obj.hit(self.attributes["damage"])

    def _use_key(self):
        player = self.game.player
        targets = self.game.level.get_actors(self.attributes["unlock"])
        dists = [self._get_distance(player, target) for target in targets]
        if min(dists) <= 2:
            while targets:
                targets[0].die()
            self.game.player.inventory.remove(self)
            self.game.player.current_item = None

    def _use_potion(self):
        self.game.player.health += self.attributes["health"]
        self.game.player.inventory.remove(self)
        self.game.player.current_item = None

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def attributes(self):
        return self._attributes

    def use(self):
        if self.type == "weapon":
            self._use_weapon()
        elif self.type == "key":
            self._use_key()
        elif self.type == "potion":
            self._use_potion()
