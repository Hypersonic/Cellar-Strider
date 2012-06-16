# -*- coding: utf-8  -*-

from cellar.actions import Action
from cellar.objects.item import Item

__all__ = ["EndGameAction"]

class GiveAction(Action):
    def execute(self):
        name = self.data["item"]
        itemtype = self.data["type"]
        actor = self.data.get("actor")
        attributes = self.data.get("attributes", {})
        if actor:
            message = (
                (actor, self.game.display.BOLD),
                (" gave you a ", None),
                (name.upper(), self.game.display.BOLD),
                ("!", None)
            )
        else:
            message = (
                ("You got a ", None),
                (name.upper(), self.game.display.BOLD),
                ("!", None)
            )

        self.game.display.message([message])
        item = Item(self.game, name, itemtype, attributes)
        self.game.player.inventory.append(item)
