# -*- coding: utf-8  -*-

try:
    import yaml
except NameError:
    yaml = None

from cellar.objects.wall import Wall

__all__ = ["Level"]

class Level(object):
    def __init__(self, game, levelfile):
        self._game = game
        self._levelfile = levelfile

        self._map = []
        self._rooms = {}
        self._associations = {}
        self._triggers = {}

        self._load()

    def __repr__(self):
        return "Level({0!r})".format(self.levelfile)

    def _parse_map(self, mapstr):
        mapdata = []
        rows = mapstr.splitlines()
        for row, cells in enumerate(rows):
            rowdata = []
            for col, cell in enumerate(cells):
                obj = self._parse_object(cell, row, col)
                if obj:
                    rowdata.append([obj])
                else:
                    rowdata.append([])
            mapdata.append(rowdata)
        return mapdata

    def _parse_object(self, char, row, col):
        if char == "@":
            player = self.game.player
            player.x, player.y = col, row
            return player
        elif char in ["+", "-", "|"]:
            return Wall(self.game, col, row, char)

    def _load(self):
        with open(self.levelfile) as fp:
            raw = yaml.load(fp)

        self._rooms = raw.get("rooms", {})
        self._associations = raw.get("associations", {})
        self._triggers = raw.get("triggers", {})
        self._map = self._parse_map(raw.get("map", ""))

    @property
    def game(self):
        return self._game

    @property
    def levelfile(self):
        return self._levelfile

    @property
    def map(self):
        return self._map

    @property
    def rooms(self):
        return self._rooms

    @property
    def associations(self):
        return self._associations

    @property
    def triggers(self):
        return self._triggers

    def step(self, events):
        stepped = []
        for row in self.map:
            for cell in row:
                for obj in cell:
                    if obj not in stepped:
                        obj.step(events)
                        stepped.append(obj)
