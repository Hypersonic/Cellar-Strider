# -*- coding: utf-8  -*-

from cellar.actions import Action

__all__ = ["SpawnAction"]

class SpawnAction(Action):
    def _spawn(self, spawner):
        row, col = spawner.y, spawner.x
        actor = self.game.level.create_actor(self.data["target"], row, col)
        self.game.level.map[row][col].append(actor)
        spawner.die()

    def execute(self):
        spawners = self.game.level.get_actors(self.data["actor"])
        while spawners:  # Individual spawners will be popped when they die
            self._spawn(spawners[0])
