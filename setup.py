#! /usr/bin/env python
# -*- coding: utf-8  -*-

from setuptools import setup, find_packages

from cellar import __version__

with open("README.md") as fp:
    long_docs = fp.read()

setup(
    name = "cellar-strider",
    packages = find_packages(),
    install_requires = [
                        "PyYAML >= 3.10",  # Map file parsing
                        ],
    version = __version__,
    author = "Ben Kurtovic and Josh Hofing",
    author_email = "ben.kurtovic@verizon.net and joshhofing@gmail.com",
    url = "https://github.com/Hypersonic/Cellar-Strider",
    description = "Cellar Strider is a game where you stride around a cellar!",
    long_description = long_docs,
    download_url = "https://github.com/Hypersonic/Cellar-Strider/tarball/v{0}".format(__version__),
    keywords = "cellar strider roguelike text-based game hypersonic earwig",
    license = "MIT License",
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console :: Curses",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Games/Entertainment :: Role-Playing",
    ],
)
