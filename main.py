#!/usr/bin/env python3

# main.py is the main command line interface. It controls game options 

from src.game import Game
from src.ascii_ui import AsciiUI


if __name__ == "__main__":
    Game(AsciiUI()).run()
