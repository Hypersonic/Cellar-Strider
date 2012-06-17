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
        spawner = self.data["actor"].upper()
        if spawner.startswith("GROUP(") and spawner.endswith(")"):
            group = spawner[6:-1]
            spawners = self.game.level.object_groups[group]
            while spawners:  # Individual spawners will be popped when they die
                self._spawn(spawners[0])
        else:
            self._spawn(self.game.level.objects[spawner])
