# -*- coding: utf-8  -*-

from cellar.actions import Action
import math

__all__ = ["WalkAction"]

class WalkAction(Action):
    def _neighbor_nodes(self, current):
        """ Returns the neighboring coordinates to the input coordinate,
        as a list of tuples """
        nodes = []
        nodes.append((current[0] + 1, current[1]))
        nodes.append((current[0] - 1, current[1]))
        nodes.append((current[0], current[1] + 1))
        nodes.append((current[0], current[1] - 1))
        return nodes
    
    def _depth_first_search(self, map, start, goal):
        # so the map is 0's representing navigable space, and 1's
        # representing walls
        start = (start[0], start[1]) # make sure that start is a tuple for easier use later
        goal = (goal[0], goal[1]) # do the same for goal
        fitness = {} # (x, y) -> fitness
        for x in range(map):
            for y in range(x):
                fitness[(x, y)] = 2 ** 32 # Set all the fitnesses to a stupidly high value
        fitness[start] = 0
        current = start
        while current != goal:
            neighbors = _neighbor_nodes(current) # find the neighbors of this tile
            for neighbor in neighbors:
                if fitness[neighbor] > fitness[current] and map[neighbor[0], neighbor[1]] == 0: # it's closer to this that previously thought, and it's not a wall
                        fitness[neighbor] = fitness[current] + 1 #increment their fitness from the current tile's
            current = neighbor[0] # switch up the current tile
        # at this point all the fitnesses are set, or at least they should be, so it's time to make the path
        path = [] # empty path, will eventually be (x,y)s from the start to the goal
        current = goal
        while current != start:
            path.append[current]
            neighbors = _neighbor_nodes(current)
            # find the neighbor with the lowest fitness value
            next = neighbors[0]
            for neighbor in neighbors:
                if fitness[next] > fitness[neighbor]:
                    next = neighbor
            current = next
        path.reverse() # since we went from end to start, the path is obviously backwards. So we have to reverse it
        return path
    def execute(self):
        pass
