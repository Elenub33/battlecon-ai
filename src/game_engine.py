from .agent import Agent
from .game_state import GameState
from .game_phases import PhaseStateMachine


"""
GameEngine tracks a GameStatem, a phase state machine, and two agents.
It progresses the game engine and requests actions from the agents when appropriate.
"""
class GameEngine:


    def __init__(self, agent0, agent1):
        assert isinstance(agent0, Agent)
        assert isinstance(agent1, Agent)
        self.agents = [agent0, agent1]
        self._set_game_state(None)
    
    
    def initialize_from_start(self):
        self._set_game_state(GameState.from_start(self.agents[0].get_fighter(), self.agents[1].get_fighter()))
    
    # TODO: save/load
    def initialize_from_file(self):
        raise NotImplementedError()
    

    def run(self):
        game_state = self._get_game_state()
        if game_state == None:
            return ValueError("GameEngine not initialized before call to run().")
        psm = PhaseStateMachine()
        while not game_state.is_over():
            psm.do_next(self._get_game_state())

    
    def get_active_agent(self) -> Agent:
        active_fighter = self._get_game_state().get_active_fighter()
        for agent in self.agents:
            if agent.get_fighter() == active_fighter:
                return agent
        raise Exception("Unable to find active agent.")
    
    
    def get_reactive_agent(self) -> Agent:
        active_fighter = self._get_game_state().get_reactive_fighter()
        for agent in self.agents:
            if agent.get_fighter() == active_fighter:
                return agent
        raise Exception("Unable to find reactive agent.")


    def _set_game_state(self, game_state: GameState):
        self._game_state = game_state
        
        
    def _get_game_state(self) -> GameState:
        return self._game_state
        