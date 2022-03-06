import random
import agent
import solve

"""
Yaron's original AI.
"""
class YaronAgent(agent.Agent):
    

    # choose a random strategy according to mix
    def choose_strategy(self, limit_antes=False):
        # If there's only one option, return it.
        f = self.get_fighter()
        if len(f.mix) == 1:
            return f.mix[0][0]
        r = random.random()
        total = 0
        for m in f.mix:
            total = total + m[1]
            if total >= r:
                strategy = m[0]
                break
        # in case I need to report my ante choice to opponent's input_strategy
        f.chosen_ante = strategy[2]
        
        print("{} chose {}.".format(self.get_name(), strategy))
        
        return strategy
        
        
    def calculate_strategy_mix(self, strats, array_results):
        mix, value = solve.solve_game_matrix(array_results)
        return list(zip(strats, list(mix))), value