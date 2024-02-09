#!/usr/bin/env python3
from .agent import Agent
from .fighters.fighter_loader import FighterLoader
from .game_engine import GameEngine
from .ui import UI


class Game:


    def __init__(self, ui: UI):
        self.ui = ui


    # TODO: inject f1, f2, a1, a2 as dependencies
    def run(self):
        f1 = FighterLoader.load_fighter_from_module("eligor")
        f2 = FighterLoader.load_fighter_from_module("shekhtur")
        a1 = Agent(f1)
        a2 = Agent(f2)
        ge = GameEngine(a1, a2)
        ge.initialize_from_start()

        self.ui.display_game_state(ge.get_game_state())

        # TODO: finish main loop
        while not ge.get_game_state().is_over():
            ge.resolve_phase()
            self.ui.display_game_state(ge.get_game_state())
