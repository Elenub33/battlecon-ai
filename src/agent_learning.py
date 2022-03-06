import random
import agent

"""
A learning AI.
"""


# TODO: unit test and add the ability to write weights to and save them from file
# watch out for using instances as keys

# TODO: Against the Yaron AI, I don't think we actually need to be unpredictable (though remember to include epsilon for random learning chance?)
# consider eliminating randomness (outside of epsilon) and simply choosing the best strategy

class LearningAgent(agent.Agent):
        

    # decide randomly for now
    def choose_strategy(self, limit_antes=False):
        f = self.get_fighter()
        strategy = random.choice(f.get_strategies())
        f.chosen_ante = strategy[2]
        print("{} chose {}.".format(self.get_name(), strategy))
        return strategy