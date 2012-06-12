# -*- coding: utf-8  -*-

from cellar.actions import Action

__all__ = ["ScriptAction"]

class ScriptAction(Action):
    def execute(self):
        messages = []
        script = self.data["script"]
        for line in script:
            actor, message = line.items()[0]
            messages.append((
                (actor, self.game.display.BOLD),
                (": {0}".format(message), 0),
                (" <space>", self.game.display.BOLD)
            ))
        self.game.display.message(messages)
