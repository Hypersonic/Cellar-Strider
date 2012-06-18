# -*- coding: utf-8  -*-

from cellar.actions.walk import WalkAction

__all__ = ["AttackAction"]

class AttackAction(WalkAction):
    def execute(self):
        actors = self.game.level.get_actors(self.data["actor"])
        targets = self.game.level.get_actors(self.data["target"])
        speed = self.data.get("speed", 1)
        damage = self.data.get("damage", 1)

        if not targets:
            # No target; try again next step:
            self.game.schedule(1.0 / self.game.display.max_fps, self.execute)
            return
        target = targets[0]

        map = self._convert_map(self.game.level.map, actors, target)
        end = (target.x, target.y)
        keep_going = False

        for actor in actors:
            if not actor.attributes.get("health", True):
                # Dead things can't do stuff:
                continue
            start = actor.x, actor.y
            path = self._get_path(map, start, end)
            if len(path) > 1:
                actor.move(path[0][0] - actor.x, path[0][1] - actor.y)
            else:
                target.hit(damage)
            keep_going = True

        if keep_going:
            wait = speed / 15.0
            self.game.schedule(wait, self.execute)
