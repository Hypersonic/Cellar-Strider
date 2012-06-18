# -*- coding: utf-8  -*-

from collections import defaultdict

try:
    import yaml
except ImportError:
    yaml = None

from cellar.objects.actor import Actor
from cellar.objects.trigger import Trigger
from cellar.objects.wall import Wall

__all__ = ["Level"]

class Level(object):
    def __init__(self, game, levelfile):
        self._game = game
        self._levelfile = levelfile

        self._map = []
        self._rooms = {}
        self._object_data = {}
        self._trigger_data = {}
        self._objects = defaultdict(list)
        self._object_groups = defaultdict(list)
        self._triggers = defaultdict(list)

        self._load()

    def __repr__(self):
        return "Level({0!r})".format(self.levelfile)

    def _insert_object(self, obj, name, group):
        self._objects[name].append(obj)
        self._object_groups[group].append(obj)

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
            self._insert_object(player, "PLAYER", "PLAYER")
            return player
        elif char in ["+", "-", "|", "\\", "/"]:
            return Wall(self.game, col, row, char)
        elif char in self._object_data:
            return self.create_actor(char, row, col)
        elif char in self._trigger_data:
            actions = self._trigger_data[char]
            trigger = Trigger(self.game, col, row, char, actions)
            self._triggers[char].append(trigger)
            return trigger

    def _load(self):
        with open(self.levelfile) as fp:
            raw = yaml.load(fp)

        self._rooms = raw.get("rooms", {})
        self._object_data = raw.get("objects", {})
        self._trigger_data = raw.get("triggers", {})
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
    def objects(self):
        return self._objects

    @property
    def object_groups(self):
        return self._object_groups

    @property
    def triggers(self):
        return self._triggers

    def get_actors(self, ident):
        if isinstance(ident, Actor):
            if not ident.is_alive:
                return []
            return [ident]
        actor = ident.upper()
        if actor.startswith("GROUP(") and actor.endswith(")"):
            group = actor[6:-1]
            return self.game.level.object_groups[group]
        else:
            return self.game.level.objects[actor]

    def create_actor(self, char, row, col):
        info = self._object_data[char]
        name = info["name"].upper()
        group = info["group"].upper()
        visible = info.get("visible", True)
        color = self.game.display.convert_color(info.get("color", "white"))
        start = info.get("start", [])
        die = info.get("die", [])
        attributes = info.get("attributes", {})

        obj = Actor(self.game, col, row, char, name, group, visible, color,
                    start, die, attributes)
        self._insert_object(obj, name, group)
        return obj

    def step(self, events):
        stepped = []
        for row in self.map:
            for cell in row:
                for obj in cell:
                    if obj not in stepped:
                        obj.step(events)
                        stepped.append(obj)
