# -*- coding: utf-8  -*-

from random import random
from sys import maxint

from cellar.actions import Action

__all__ = ["WalkAction"]

class WalkAction(Action):
    def _get_neighbor_nodes(self, map, point):
        """Return the neighboring nodes of the input node (point)."""
        tests = [
            (point[0] + 1, point[1]),
            (point[0] - 1, point[1]),
            (point[0], point[1] + 1),
            (point[0], point[1] - 1)
        ]
        nodes = []
        for node in tests:
            if node[0] < 0 or node[1] < 0:  # Cannot be negative!
                continue
            try:
                point = map[node[1]][node[0]]
            except IndexError:
                continue
            if not point:  # Must not be a wall:
                nodes.append(node)
        return nodes

    def _calculate_fitness(self, fitness, map, start, goal):
        jobs = [start]
        while jobs:
            for job in jobs:
                neighbors = self._get_neighbor_nodes(map, job)
                for neighbor in neighbors:
                    if fitness[neighbor] == maxint:
                        # Increment their fitness from the current tile's:
                        fitness[neighbor] = fitness[job] + 1
                        jobs.append(neighbor)
                    if neighbor == goal:
                        return fitness

    def _calculate_path_by_fitness(self, fitness, map, start, goal):
        # At this point all the fitnesses are set, or at least they should be,
        # so it's time to make the path:
        path = [goal]
        this = goal
        while 1:
            neighbors = self._get_neighbor_nodes(map, this)
            for neighbor in neighbors:
                if fitness[neighbor] == fitness[this]:
                    # To vary the route a bit, randomly pick another path if it
                    # has the same fitness as the current one
                    if round(random()):
                        this = neighbor
                elif fitness[neighbor] < fitness[this]:
                    this = neighbor
            if this == start:
                return path
            path.append(this)

    def _get_path(self, map, start, goal):
        fitness = {}  # (x, y) -> fitness
        # Set all the fitnesses to a stupidly high value:
        for y, row in enumerate(map):
            for x in range(len(row)):
                fitness[(x, y)] = maxint

        fitness[start] = 0
        self._calculate_fitness(fitness, map, start, goal)
        path = self._calculate_path_by_fitness(fitness, map, start, goal)

        # Since we went from end to start, the path is backwards, so we have to
        # reverse it:
        path.reverse()
        return path

    def _convert_map(self, map, actors, dest):
        """Convert a level map to 1s and 0s for the pathfinding code.

        1 represents a square that you cannot go on, whereas 0 is a square that
        you can.
        """
        newmap = [[1 if any([obj.is_visible for obj in cell]) else 0 \
                  for cell in row] for row in map]

        for actor in actors:
            newmap[actor.y][actor.x] = 0
        newmap[dest.y][dest.x] = 0
        return newmap

    def execute(self):
        actors = self.game.level.get_actors(self.data["actor"])
        destination = self.game.level.get_actors(self.data["target"])[0]
        speed = self.data.get("speed", 1)

        map = self._convert_map(self.game.level.map, actors, destination)
        end = (destination.x, destination.y)
        keep_going = False

        for actor in actors:
            start = actor.x, actor.y
            path = self._get_path(map, start, end)
            if path:
                actor.move(path[0][0] - actor.x, path[0][1] - actor.y)
            if len(path) > 1:
                keep_going = True

        if keep_going:
            wait = float(speed) / self.game.display.max_fps
            self.game.schedule(wait, self.execute)
