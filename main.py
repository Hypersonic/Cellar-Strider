#! /usr/bin/env python
# -*- coding: utf-8  -*-

from os import path
from sys import argv

from cellar.main import MainMenu

if len(argv) > 1 and (argv[1].startswith("-d") or argv[1].startswith("--d")):
    debug = True
else:
    debug = False

gamesdir = path.join(path.abspath(path.dirname(__file__)), "games")
with MainMenu(gamesdir, debug) as menu:
    menu.run()
