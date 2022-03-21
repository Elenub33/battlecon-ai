import random
import agent

"""
A player that makes every choice randomly.
"""
class RandomAgent(agent.Agent):
        

    # choose randomly
    def choose_strategy(self, limit_antes=False):
        return random.choice(self.get_available_strategies(self.get_fighter()))