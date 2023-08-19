from .game_engine import GameEngine
from .ui import UI

class AsciiUI(UI):


    def get_board_objects(self) -> dict[int, str]:
        game_state = self.game_engine.get_game_state()
        return {
            game_state.get_active_fighter_state().get_position(): game_state.get_active_fighter().get_nickname()[0],
            game_state.get_reactive_fighter_state().get_position(): game_state.get_reactive_fighter().get_nickname()[0],
        }
    

    def display_game_state(self):
        pos = self.get_board_objects()
        pos.setdefault("-")
        for i in range(7):
            print(pos.get(i, "-"), end=" ")
        print()
        print()