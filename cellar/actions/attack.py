# -*- coding: utf-8  -*-

from cellar.actions.walk import WalkAction

__all__ = ["AttackAction"]

class AttackAction(WalkAction):
    def execute(self):
        actors = self.game.level.get_actors(self.data["actor"])
        target = self.game.level.get_actors(self.data["target"])[0]
        speed = self.data.get("speed", 1)
        damage = self.data.get("damage", 1)

        map = self._convert_map(self.game.level.map, actors, target)
        end = (target.x, target.y)
        keep_going = False

        for actor in actors:
            start = actor.x, actor.y
            path = self._get_path(map, start, end)
            if len(path) > 1:
                actor.move(path[0][0] - actor.x, path[0][1] - actor.y)
                actor._char = "O"
                actor._color = self.game.display.YELLOW
            else:
                actor._char = "X"
                actor._color = self.game.display.RED

        wait = float(speed) / self.game.display.max_fps
        self.game.schedule(wait, self.execute)
