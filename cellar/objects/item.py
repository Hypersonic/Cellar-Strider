# -*- coding: utf-8  -*-

from cellar.objects import Object

__all__ = ["Item"]

class Item(Object):
    def __init__(self, game, name, itemtype, attributes):
        super(Item, self).__init__(game, 0, 0, visible=False)
        self._name = name
        self._type = itemtype
        self._attributes = attributes

    def _use_weapon(self):
        pass

    def _use_key(self):
        pass

    def _use_potion(self):
        pass

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
        else:
            raise NotImplementedError(self.type)
