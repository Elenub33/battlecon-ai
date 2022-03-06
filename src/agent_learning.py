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
        
        
    def __init__(self, fighter_name, bases="alpha"):
        super().__init__(fighter_name, bases)
        self.epsilon = 0.03 # percent chance to take random action instead of strategic one (for learning purposes)
        self.discount = 0.97 # preference to take action now over later. 0.0 = 100% urgency, 1.0 = 0% urgency.
        self.alpha = 0.1 # amount to adjust weights when learning new information. 0.0 = no learning, 1.0 = discard all previous knowledge.
        self.weights = dict()
        

    def choose_strategy(self, limit_antes=False):
        self.update(self.calculate_reward())
        if random.random() > self.epsilon:
            strategy = self.get_best_strategy()
        else:
            strategy = self.get_random_strategy()
        self.record_chosen_strategy(strategy)
        return strategy
        
        
    def get_random_strategy(self):
        return random.choice(self.get_fighter().get_strategies())
        
        
    def get_best_strategy(self):
        best_s, best_q = [], float('-inf')
        for s in self.get_fighter().get_strategies():
            q = self.get_q_value(s)
            if q == best_q:
                best_s.append(s)
            else if q > best_q:
                best_s = [s]
                best_q = q
        if len(best_s) > 0:
            return random.choice(best_s)
        else:
            return None
        
        
    def record_chosen_strategy(self, strategy):
        self.save_strategy(strategy)
        self.get_fighter().chosen_ante = strategy[2]
        print("{} chose {}.".format(self.get_name(), strategy))

0
    def get_weights(self):
        return self.weights
        
        
    def get_weight(self, feature):
        w = self.get_weights()
        if feature in w.keys:
            return w[feature]
        else
            return 0.0
        
        
    """
    Remember details about the chosen strategy for learning later.
    """
    def save_strategy(self, strategy):
        self.last_strategy_features = self.get_features(strategy)
        self.last_strategy = strategy
        self.last_strategy_q_value = self.get_q_value(strategy)
        
       
    """
    Recall details about most recently chosen strategy.
    """
    def recall_strategy(self):
        if hasattr(self, 'last_strategy'):
            return self.last_strategy, self.last_strategy_q_value, self.last_strategy_features
        else:
            return None, None, None
        

    """
    Learn from the transition that was taken.
    Changes from original algorithm:
    state and nextState cannot be passed in, so they have been bookmarked and calculated as needed.
    """
    def update(self, reward):
        
        strategy, prev_q, prev_features = self.recall_strategy()
        
        if strategy == None:
            return
        
        this_q = self.get_current_state_value()
        diff = self.alpha * ((reward + self.discount * this_q) - prev_q)
        
        w = self.get_weights()
        for i in prev_features.keys():
            w[i] = w.get_weight(i) + diff * prev_features[i]

    """
    Determine the value of a particular strategy according to current weights.
    """
    def get_q_value(self, strategy):
        f = self.get_features(strategy)
        val = 0.0
        for i in f.keys:
            val += self.get_weight(i) * f[i]
        return val
        
        
    """
    Determine the value of the current state given current weights.
    """
    def get_current_state_value(self):
        strategies = self.get_fighter().get_strategies()
        if len(strategies) == 0:
            return 0.0
        value = float('-inf')
        for strategy in strategies:
            value = max(value, self.get_q_value(strategy))
        return value
        
        
    """
    Determine the reward earned since the last update.
    """
    def calculate_reward()
        # TODO: update this w/ health changes since last state
        return 0.0
    
    """
    Get features based on strategy and current state.
    Start with simple features and expand them as needed.
    """
    def get_features(self, strategy):
        f = dict()
        # TODO: add features
        return f