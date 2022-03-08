import random, time
import agent, solve

"""
Yaron's original AI.
"""
class YaronAgent(agent.Agent):
    

    # choose a random strategy according to mix
    def choose_strategy(self, limit_antes=False):
    
        f = self.get_fighter()
        
        print("{} is thinking ({} options)... ".format(self.get_name(), len(f.mix)), end="")
        start_time = time.time()
    
        # If there's only one option, return it.
        if len(f.mix) == 1:
            print("chose {} ({}s).".format(self.get_strategy_name(f.mix[0][0]), time.time() - start_time))
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
        
        print("chose {} ({}s).".format(self.get_strategy_name(strategy), time.time() - start_time))
        self.log_strategy(strategy)
        return strategy
        
        
    def calculate_strategy_mix(self, strats, array_results):
        mix, value = solve.solve_game_matrix(array_results)
        return list(zip(strats, list(mix))), value