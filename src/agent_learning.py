import random, json
import agent

"""
A learning AI.
"""

# TODO: This approach won't work well against a human opponent since it picks the optimal strategy every time. Would need some additional randomness or a fast learning rate to adjust to unpredictable enemies.

class LearningAgent(agent.Agent):
        
        
    def __init__(self, fighter_name, bases="alpha"):
        super().__init__(fighter_name, bases)
        self.epsilon = 0.04 # percent chance to take random action instead of strategic one (for learning purposes)
        self.discount = 0.97 # preference to take action now over later. 0.0 = 100% urgency, 1.0 = 0% urgency.
        self.alpha = 0.1 # amount to adjust weights when learning new information. 0.0 = no learning, 1.0 = discard all previous knowledge.
        self.clear_weights()
        

    def choose_strategy(self, limit_antes=False):
    
        # learn from everything that's happened since previous choice
        self.update()
        
        # choose what to do next
        if random.random() > self.epsilon:
            strategy, q_val = self.get_best_strategy()
        else:
            print("vvvv ACTING RANDOMLY vvvv")
            strategy = self.get_random_strategy()
        
        # record and commit to our choice
        self.record_chosen_strategy(strategy)
        return strategy
        
        
    def conclude_game(self, winner):
        self.update()
        
        
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
            return random.choice(best_s), best_q
        else:
            return None, best_q
        
        
    def record_chosen_strategy(self, strategy):
        self.log_strategy(strategy)
        self.save_strategy(strategy)
        self.get_fighter().chosen_ante = strategy[2]


    def get_weights(self):
        return self.weights


    def set_weights(self, weights):
        self.weights = weights
        
    
    def clear_weights(self):
        self.weights = dict()
    
        
    def set_weight(self, feature, weight):
        self.weights[feature] = weight
        
        
    def get_weight(self, feature):
        w = self.get_weights()
        if feature in w.keys():
            return w[feature]
        else:
            return 0.0


    def save_weights(self, filename):
        w = self.get_weights()
        f = open(filename, "w")
        f.write(json.dumps(w))
        f.close()


    def load_weights(self, filename):
        f = open(filename, "r")
        w = json.loads(f.read())
        f.close()
        self.set_weights(w)

            
    def get_health_diff(self):
        f = self.get_fighter()
        opp = f.opponent
        return f.effective_life() - opp.effective_life()
        
        
    """
    Remember details about the chosen strategy for learning later.
    """
    def save_strategy(self, strategy):
        self.last_strat_results = {
            'strategy': strategy,
            'features': self.get_features(strategy),
            'q_val': self.get_q_value(strategy),
            'health_diff': self.get_health_diff()
        }
        
       
    """
    Recall details about most recently chosen strategy.
    """
    def recall_strategy(self):
        if hasattr(self, 'last_strat_results'):
            return self.last_strat_results
        else:
            return None
        

    """
    Learn from the transition that was taken.
    Changes from original algorithm:
    state and nextState cannot be passed in, so they have been bookmarked and calculated as needed.
    reward is calculated based on the HP difference from last beat instead of being passed in.
    """
    def update(self):
        
        last_strat = self.recall_strategy()
        
        if last_strat == None:
            return
            
        reward = self.get_health_diff() - last_strat['health_diff']
        
        print("REWARD:", reward, "({} to {})\n".format(self.get_fighter().opponent.effective_life(), self.get_fighter().effective_life()))
        
        this_q = self.get_current_state_value()
        diff = self.alpha * ((reward + self.discount * this_q) - last_strat['q_val'])
        
        w = self.get_weights()
        f = last_strat['features']
        
        for i in f.keys():
            self.set_weight(i, self.get_weight(i) + diff * f[i])
        
        
    """
    Determine the value of a particular strategy according to current weights.
    """
    def get_q_value(self, strategy):
        f = self.get_features(strategy)
        val = 0.0
        for i in f.keys():
            val += self.get_weight(i) * f[i]
        return val
        
        
    """
    Determine the value of the current state given current weights.
    """
    def get_current_state_value(self):
        strategy, q_val = self.get_best_strategy()
        if strategy == None:
            return 0.0
        return q_val
        
    
    """
    Get features based on strategy and current state.
    Start with simple features and expand them as needed.
    """
    def get_features(self, strategy):
    
        features = dict()
        
        self.add_range_features(features)
        self.add_strategy_features(features, strategy)
        self.add_counterplay_features(features, strategy)
        self.add_my_option_features(features, strategy)
        self.add_opp_option_features(features)
        
        return features
        
        
    def get_range_from_edge(self, fighter):
        return round(min(fighter.position, 6 - fighter.position))
        
        
    def get_range_between_fighters(self):
        f = self.get_fighter()
        return round(abs(f.position - f.opponent.position))
        
    
    def get_minrange(self, *cards):
        return round(sum([(card.minrange if card.minrange != None else 0.0) + card.get_minrange_bonus() for card in cards]))
        
        
    def get_maxrange(self, *cards):
        return round(sum([(card.maxrange if card.maxrange != None else 0.0) + card.get_maxrange_bonus() for card in cards]))
        
        
    def get_power(self, *cards):
        return round(sum([(card.power if card.power != None else 0.0) + card.get_power_bonus() for card in cards]))
        
        
    def get_priority(self, *cards):
        return round(sum([(card.priority if card.priority != None else 0.0) + card.get_priority_bonus() for card in cards]))
        
        
    def get_stunguard(self, *cards):
        return round(sum([card.get_stunguard() for card in cards]))
        
        
    def get_soak(self, *cards):
        return round(sum([card.get_soak() for card in cards]))
        
        
    def add_range_features(self, features):
    
        # give bools and ranges as possible features
        fighter_range = self.get_range_between_fighters()
        my_edge_range = self.get_range_from_edge(self.get_fighter())
        opp_edge_range = self.get_range_from_edge(self.get_fighter().opponent)
        
        features["range"] = fighter_range
        features["range_equals_" + str(fighter_range)] = 1.0
        
        features["my_edge_range"] = my_edge_range
        features["my_edge_range_equals_" + str(my_edge_range)] = 1.0
        
        features["opp_edge_range"] = opp_edge_range
        features["opp_edge_range_equals_" + str(opp_edge_range)] = 1.0
        
        
    def add_strategy_features(self, features, strategy):
        
        style = strategy[0]
        base = strategy[1]
        ante = strategy[2][0]
        
        pair_name = style.name + base.name
        
        range = self.get_range_between_fighters()
        
        # booleans for individual elements of strategy and for combination
        features["Strategy " + self.get_strategy_name(strategy)] = 1.0
        features["play_" + pair_name + "_at_range_" + str(range)] = 1.0
        features["play_" + pair_name] = 1.0
        features["play_" + style.name] = 1.0
        features["play_" + base.name] = 1.0
        features["ante_" + str(ante)] = 1.0
        
        # number of tokens anted
        features["ante_count"] = ante
        
        min_range = self.get_minrange(style, base)
        max_range = self.get_maxrange(style, base)
        
        features["strat_minrange"] = min_range
        features["strat_maxrange"] = max_range
        features["strat_range_band"] = max_range - min_range
        features["strat_power"] = self.get_power(style, base)
        features["strat_priority"] = self.get_priority(style, base)
        features["strat_stun_guard"] = self.get_stunguard(style, base) + ante * 2
        features["strat_soak"] = self.get_soak(style, base)
        
        opp_range = self.get_range_between_fighters()
        features["opponent_too_close"] = min(0, min_range - opp_range)
        features["opponent_too_far"] = min(0, opp_range - max_range)
        
        
    def add_counterplay_features(self, features, my_strategy):
        
        my_style = my_strategy[0]
        my_base = my_strategy[1]
        my_ante = my_strategy[2][0]
        
        my_priority = self.get_priority(my_style, my_base)
        my_stun_resist = self.get_stunguard(my_style, my_base) + self.get_soak(my_style, my_base)
        distance = self.get_range_between_fighters()
        
        opp_pairs = self.get_fighter().opponent.get_pairs()
        for opp_style, opp_base in opp_pairs:
            features[my_style.name + my_base.name + "_when_" + opp_style.name + opp_base.name + "_available"] = 1.0
        
        opp_strategies = self.get_fighter().opponent.get_strategies()
        
        faster_opp_strats = 0
        clashing_opp_strats = 0
        stunning_opp_strats = 0
        in_range_opp_strats = 0
        total_opp_strats = len(opp_strategies)
        
        for opp_strategy in opp_strategies:
        
            opp_style = opp_strategy[0]
            opp_base = opp_strategy[1]
            opp_ante = opp_strategy[2][0]
            
            opp_priority = self.get_priority(opp_style, opp_base) + opp_ante
            opp_power = self.get_power(opp_style, opp_base)
            opp_minrange = self.get_minrange(opp_style, opp_base)
            opp_maxrange = self.get_maxrange(opp_style, opp_base)
            
            if opp_priority == my_priority:
                clashing_opp_strats += 1
            elif opp_priority > my_priority:
                faster_opp_strats += 1
            
            if opp_power > my_stun_resist and opp_priority >= my_priority:
                stunning_opp_strats += 1
                
            if opp_minrange <= distance and opp_maxrange >= distance:
                in_range_opp_strats += 1
            
        features["opponent_likely_to_act_faster"] = faster_opp_strats / total_opp_strats
        features["opponent_likely_to_stun_before_my_attack"] = faster_opp_strats / total_opp_strats
        features["opponent_likely_to_be_in_range"] = faster_opp_strats / total_opp_strats
        
        
    def add_my_option_features(self, features, strategy):
        
        f = self.get_fighter()
        
        style = strategy[0]
        base = strategy[1]
        
        next_hand = f.styles_and_bases_set - (f.discard[1] | set([style, base]))
        
        for card in next_hand:
            features[card.name + "_in_my_next_hand"] = 1.0
            
        features["my_tokens"] = len(f.pool)
        features["i_have_special"] = f.special_action_available
        
        
    def add_opp_option_features(self, features):
    
        f = self.get_fighter().opponent
        
        hand = f.styles_and_bases_set - (f.discard[1] | f.discard[2])
        
        for card in hand:
            features[card.name + "_in_opp_hand"] = 1.0
        for card in f.discard[1]:
            features[card.name + "_in_opp_disc_1"] = 1.0
        for card in f.discard[2]:
            features[card.name + "_in_opp_disc_2"] = 1.0
            
        
        features["opp_tokens"] = len(f.pool)
        features["opp_has_special"] = f.special_action_available