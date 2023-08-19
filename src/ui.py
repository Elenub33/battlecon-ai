from .game_engine import GameEngine


class UI:


    def __init__(self, game_engine: GameEngine):
        print("Assigning Game Engine", game_engine)
        self.game_engine = game_engine


    def display_game_state(self):
        return