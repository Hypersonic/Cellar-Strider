Cellar Strider
==============

A game where you stride around a cellar!

Dependencies
============

Cellar Strider runs on pure Python, using the `curses` module for drawing,
which is a wrapper for `ncurses`. This should come with Python. The sole
external dependency is `PyYAML`, used for loading map files. You can
install it automatically by running:

> pip install PyYAML

or

> easy_install PyYAML

...which may require `sudo`.

Running
=======

To play, simply run `main.py`. It will ask you to select a game, or "map pack".
Choose the tutorial to start with, so you can get a feeling for the controls,
but definitely check out the main game once you've finished it -- that's where
the action's at!

Controls
========

The game is completely keyboard-based. Use `WASD` to navigate the player.
`Enter` (or `Return`) is used to progress through most dialogs and messages.

Press `i` to open your inventory, select an item with `W` and `S`, then close
the inventory with `Enter`. To use the item, press `Space` while in the game.
For swords and keys, remember to be right next to the object when using it. For
swords, a good technique is to move towards the enemy, press `Space`, and then
immediate move away so they cannot retaliate.

Maps
====

A sample of the map format can be viewed in `games/tutorial/tutorial.yaml`. A
(much) more complex example is `games/main-game/level02.yaml`.
