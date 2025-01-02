from .game_state import GameState
from .ui import UI


class AsciiUI(UI):


    def get_board_objects(self, game_state: GameState) -> dict[int, str]:
        return {
            game_state.get_active_fighter_state().get_position(): game_state.get_active_fighter().get_nickname()[0],
            game_state.get_reactive_fighter_state().get_position(): game_state.get_reactive_fighter().get_nickname()[0],
        }
    

    def display_game_state(self, game_state: GameState):
        pos = self.get_board_objects(game_state)
        pos.setdefault("-")
        for i in range(7):
            print(pos.get(i, "-"), end=" ")
        print()
        print()
        