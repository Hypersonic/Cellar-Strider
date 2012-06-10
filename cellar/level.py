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

    def _parse_object(self, char):
        if char == "@":
            return self.game.player
        elif char in ["+", "-", "|"]:
            return Wall(self.game, char)

    def _parse_map(self, mapstr):
        mapdata = []
        rows = mapstr.splitlines()
        for row in rows:
            rowdata = []
            for cell in row:
                rowdata.append(self._parse_object(cell))
            mapdata.append(rowdata)
        return mapdata

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

    def remove(self, target):
        for row in self.map:
            for i, obj in enumerate(row):
                if obj is target:
                    row[i] = None
                    return

    def step(self, events):
        for row in self.map:
            for obj in row:
                if obj:
                    obj.step(events)
