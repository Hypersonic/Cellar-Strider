# -*- coding: utf-8  -*-

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

    def _debug(self, fitness, job, neighbor):
        from collections import defaultdict
        map = defaultdict(lambda: defaultdict(list))
        for point in fitness:
            fit = [fitness[point], None]
            if fit[0] == maxint:
                fit = ["-1", self.game.display.YELLOW]
            if point == job:
                fit[1] = self.game.display.RED | self.game.display.BOLD
            if point == neighbor:
                fit[1] = self.game.display.GREEN | self.game.display.BOLD
            map[point[1]][point[0]] = fit

        self.game.display.window.erase()
        self.game.display._render_header()
        for row, cells in map.iteritems():
            for col, (char, flags) in cells.iteritems():
                if flags:
                    self.game.display.window.addstr(row + 2, col * 3, str(char).rjust(3), flags)
                else:
                    self.game.display.window.addstr(row + 2, col * 3, str(char).rjust(3))
        self.game.display.window.refresh()

    def _get_path(self, map, start, goal):
        fitness = {}  # (x, y) -> fitness

        # Set all the fitnesses to a stupidly high value:
        for y, row in enumerate(map):
            for x in range(len(row)):
                fitness[(x, y)] = maxint

        fitness[start] = 0
        jobs = [start]
        while jobs:
            for job in jobs:
                neighbors = self._get_neighbor_nodes(map, job)
                for neighbor in neighbors:
                    self._debug(fitness, job, neighbor)
                    if fitness[neighbor] == maxint:
                        # Increment their fitness from the current tile's:
                        fitness[neighbor] = fitness[job] + 1
                        jobs.append(neighbor)

        # At this point all the fitnesses are set, or at least they should be,
        # so it's time to make the path:
        path = []  # Empty path, will eventually be (x,y)s from the start to
                   # the goal

        current = goal
        while current != start:
            path.append(current)
            neighbors = self._get_neighbor_nodes(map, current)
            # Find the neighbor with the lowest fitness value:
            next = neighbors[0]
            for neighbor in neighbors:
                if fitness[next] > fitness[neighbor]:
                    next = neighbor
            current = next

        # Since we went from end to start, the path is obviously backwards. So
        # we have to reverse it:
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
            self.game.schedule(0, self.execute)
