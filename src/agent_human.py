import agent

"""
A human player.
"""
class HumanAgent(agent.Agent):

    
    def is_human(self):
        return True
        
        
    def evaluate(self):
        self.set_preferred_range()
        res = self.get_fighter().evaluate()
        # print(self.get_name() + " (HUMAN) evaluating " + self.get_chosen_strategy_name() + ". Result: " + res)
        return res
        

    # prompt human player for a strategy
    def choose_strategy(self, limit_antes=False):
        f = self.get_fighter()
        strategy = f.input_strategy(limit_antes)
        # in case I need to report my ante choice to opponent's input_strategy
        f.chosen_ante = strategy[2]
        return strategy