# -*- coding: utf-8  -*-

from cellar.actions.action import Action

from cellar.actions.end_game import EndGameAction
from cellar.actions.give import GiveAction
from cellar.actions.remove import RemoveAction
from cellar.actions.script import ScriptAction
from cellar.actions.spawn import SpawnAction
from cellar.actions.walk import WalkAction

__all__ = ["Action", "get_action"]

_actions = {
    "end game": EndGameAction,
    "give": GiveAction,
    "remove": RemoveAction,
    "script": ScriptAction,
    "spawn": SpawnAction,
    "walk": WalkAction,
}

def get_action(game, data):
    name = data["action"]
    action = _actions[name](game, data)
    return action.execute, action.get_duration()
