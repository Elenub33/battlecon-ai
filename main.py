#!/usr/bin/env python3
from src.agent import Agent
from src.fighters.fighter_loader import FighterLoader
from src.game_engine import GameEngine
from src.ascii_ui import AsciiUI


if __name__ == "__main__":
    f1 = FighterLoader.load_fighter_from_module("eligor")
    f2 = FighterLoader.load_fighter_from_module("shekhtur")
    a1 = Agent(f1)
    a2 = Agent(f2)
    ge = GameEngine(a1, a2)
    ge.initialize_from_start()
    ui = AsciiUI(ge)
    ui.display_game_state()

    # TODO: main loop