#! /usr/bin/env python
# -*- coding: utf-8  -*-

from os import path

from cellar.main import MainMenu

gamesdir = path.join(path.abspath(path.dirname(__file__)), "games")
with MainMenu(gamesdir) as menu:
    menu.run()
