import random
import agent

"""
A learning AI.
"""

# TODO: This approach won't work well against a human opponent since it picks the optimal strategy every time. Would need some additional randomness or a fast learning rate to adjust to unpredictable enemies.

class LearningAgent(agent.Agent):
        
        
    def __init__(self, fighter_name, bases="alpha"):
        super().__init__(fighter_name, bases)
        self.epsilon = 0.03 # percent chance to take random action instead of strategic one (for learning purposes)
        self.discount = 0.97 # preference to take action now over later. 0.0 = 100% urgency, 1.0 = 0% urgency.
        self.alpha = 0.1 # amount to adjust weights when learning new information. 0.0 = no learning, 1.0 = discard all previous knowledge.
        self.weights = dict()
        

    def choose_strategy(self, limit_antes=False):
    
        # learn from everything that's happened since previous choice
        self.update()
        
        # choose what to do next
        if random.random() > self.epsilon:
            strategy = self.get_best_strategy()
        else:
            strategy = self.get_random_strategy()
        
        # record and commit to our choice
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
            elif q > best_q:
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


    def get_weights(self):
        return self.weights
        
        
    def get_weight(self, feature):
        w = self.get_weights()
        if feature in w.keys:
            return w[feature]
        else:
            return 0.0
            
    def get_health_diff(self):
        f = self.get_fighter()
        opp = f.opponent
        return f.effective_life() - opp.effective_life()
        
        
    """
    Remember details about the chosen strategy for learning later.
    """
    def save_strategy(self, strategy):
        self.last_strategy_features = self.get_features(strategy)
        self.last_strategy = strategy
        self.last_strategy_q_value = self.get_q_value(strategy)
        self.last_strategy_health_diff = self.get_health_diff()
        
       
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
        
        strategy, prev_q, prev_features, last_health_diff = self.recall_strategy()
        
        if strategy == None:
            return
            
        reward = self.get_health_diff() - last_health_diff
        
        this_q = self.get_current_state_value()
        diff = self.alpha * ((reward + self.discount * this_q) - prev_q)
        
        w = self.get_weights()
        for i in prev_features.keys():
            w[i] = w.get_weight(i) + diff * prev_features[i]


    """
    Determine the value of a particular strategy according to current weights.
    """
    def get_q_value(self, strategy):
        f = self.get_features(strategy) # TODO: remove this comment. This is where the magic happens; features that make a difference based on strategy are critical. all others are likely the same across all decisions.
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
    Get features based on strategy and current state.
    Start with simple features and expand them as needed.
    """
    def get_features(self, strategy):
    
        features = dict()
        
        self.add_strategy_features(features, strategy) # stun guard, damage, hit confirm etc.
        self.add_range_features(features, strategy) # player distance, my edge distance, opp edge distance
        self.add_my_option_features(features, strategy)
        self.add_opp_option_features(features, strategy)
        self.add_my_state_option_combo_features(features, strategy)
        self.add_opp_state_option_combo_features(features, strategy)
        self.add_strategy_range_combo_features(features, strategy) # strategy combined w/ range features; hitting ranges that are near opponent, etc.
        
        # how can we add more features that estimate what the next beat will be like?
        
        return features
        
        
    def get_range_from_edge(self, fighter):
        return min(fighter.position, 6 - fighter.position)
        
        
    def get_range_between_fighters(self):
        f = self.get_fighter()
        return abs(f.position - f.opponent.position)
        
        
    def add_strategy_features(self, features, strategy):
        
        # booleans for individual elements of strategy and for combination
        features[self.get_strategy_name(strategy)] = 1.0
        features["strat_style_" + strategy[0].name] = 1.0
        features["strat_base_" + strategy[1].name] = 1.0
        features["strat_ante_" + str(strategy[0][0])] = 1.0
        
        # number of tokens anted
        features["strat_ante"] = strategy[0][0]
        
        
    def add_range_features(self, features, strategy):
        pass
        
        
    def add_my_option_features(self, features, strategy):
        pass
        
        
    def add_opp_option_features(self, features, strategy):
        pass
        
        
    def add_my_state_option_combo_features(self, features, strategy):
        pass
        
        
    def add_opp_state_option_combo_features(self, features, strategy):
        pass
        
        
    def add_strategy_range_combo_features(self, features, strategy):
        pass