# -*- coding: utf-8  -*-

__all__ = ["Object"]

class Object(object):
    def __init__(self):
        self._visible = True

    @property
    def is_visible(self):
        return self._visible

    def render(self):
        raise NotImplementedError()

    def step(self):
        raise NotImplementedError()
