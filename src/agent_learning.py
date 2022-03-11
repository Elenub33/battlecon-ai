import random, json, time
import agent, fighters

"""
A learning AI.
"""

# TODO: This approach won't work well against a human opponent since it picks the optimal strategy every time. Would need some additional randomness or a fast learning rate to adjust to unpredictable enemies.

class LearningAgent(agent.Agent):
        
        
    def __init__(self, fighter_name, bases="alpha"):
        super().__init__(fighter_name, bases)
        self.epsilon = 0.04 # percent chance to take random action instead of strategic one (for learning purposes)
        self.discount = 1.0 # preference to take action now over later. 0.0 = 100% urgency, 1.0 = 0% urgency.
        self.alpha = 0.01 # amount to adjust weights when learning new information.
        self.last_learned_beat = 0
        self.clear_weights()
        

    def choose_strategy(self, limit_antes=False):
    
        # learn from everything that's happened since previous beat
        # (sometimes due to clashes, we have to pick multiple strategies in the same beat)
        if self.last_learned_beat < self.game.current_beat:
            self.update()
            self.last_learned_beat = self.game.current_beat
        
        print("{} is thinking ({} options)... ".format(self.get_name(), len(self.get_fighter().mix)), end="")
        start_time = time.time()
        
        # choose what to do next
        if random.random() > self.epsilon:
            strategy, q_val = self.get_best_strategy()
        else:
            print("vvvv ACTING RANDOMLY vvvv")
            strategy = self.get_random_strategy()
        
        # record and commit to our choice
        print("chose {} ({}s).".format(self.get_strategy_name(strategy), time.time() - start_time))
        self.record_chosen_strategy(strategy)
        return strategy
        
        
    def conclude_game(self, winner):
        self.update()
        
        
    def get_random_strategy(self):
        return random.choice(self.get_available_strategies(self.get_fighter()))
        
        
    def get_best_strategy(self):
        best_s, best_q = [], float('-inf')
        for s in self.get_available_strategies(self.get_fighter()):
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
        
        
    def get_available_strategies(self, fighter):
        return [m[0] for m in fighter.mix]
        
        
    def record_chosen_strategy(self, strategy):
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
    
        features, features_for_enemy_strat = self.get_features(strategy)
    
        self.last_strat_results = {
            'strategy': strategy,
            'features': features,
            'features_for_enemy_strat': features_for_enemy_strat,
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
        
        
    def get_last_enemy_pair_name(self):
    
        enemy_strat = self.opponent.get_logged_strategies()[-1]
        
        enemy_style = enemy_strat[0]
        enemy_base = enemy_strat[1]
        
        return enemy_style.name + enemy_base.name
        

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
        
        this_q = self.get_current_state_value()
        diff = self.alpha * ((reward + self.discount * this_q) - last_strat['q_val'])
        
        w = self.get_weights()
        
        my_last_pair_name = last_strat['strategy'][0].name + last_strat['strategy'][1].name
        last_enemy_pair_name = self.get_last_enemy_pair_name()
        
        print("REWARD: {} ({} to {}). Learning from {} vs. {}, Q VALUE {} -> {} (diff {})".format(reward, self.get_fighter().opponent.effective_life(), self.get_fighter().effective_life(), my_last_pair_name, last_enemy_pair_name, last_strat['q_val'], this_q, diff))
        
        f = last_strat['features_for_enemy_strat'][last_enemy_pair_name]
        
        for i in f.keys():
            self.set_weight(i, self.get_weight(i) + diff * f[i])
        
        
    """
    Determine the value of a particular strategy according to current weights.
    """
    def get_q_value(self, strategy):
        f, features_for_enemy_strat = self.get_features(strategy)
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
    Warning: to avoid accidentally dominating other features, each feature should be scaled from 0.0 to 1.0.
    """
    def get_features(self, strategy):
    
        features = dict()
        
        self.add_strategy_features(features, strategy)
        features_for_enemy_strat = self.add_counterplay_features(features, strategy)
        
        return features, features_for_enemy_strat
        
        
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
        
        
    def add_strategy_features(self, features, strategy):
        
        style = strategy[0]
        base = strategy[1]
        ante = strategy[2][0]
        
        pair_name = style.name + base.name
        
        range = self.get_range_between_fighters()
        
        # booleans for individual elements of strategy and for combination
        features[self.get_strategy_name(strategy)] = 1.0
        features[pair_name + " at Range " + str(range)] = 1.0
        features[pair_name + " at Distance " + str(self.get_range_from_edge(self.get_fighter())) + " from edge"] = 1.0
        features[pair_name] = 1.0
        features[style.name] = 1.0
        features[base.name] = 1.0
        features["Ante " + str(ante)] = 1.0
        
        features[pair_name + " when Opponent Close"] = (6.0 - range) / 5.0
        features[pair_name + " when Opponent Far"] = (range - 1.0) / 5.0
        
        
    """
    Adds all possible strats to all_features and returns a dictionary containing all generic features plus all features for a specific enemy option.
    """
    def add_counterplay_features(self, all_features, my_strategy):
        
        my_style = my_strategy[0]
        my_base = my_strategy[1]
        my_ante = my_strategy[2][0]
        
        range = self.get_range_between_fighters()
        
        my_pair_name = my_style.name + my_base.name
        
        my_priority = self.get_priority(my_style, my_base)
        my_stun_resist = self.get_stunguard(my_style, my_base) + self.get_soak(my_style, my_base)
        distance = self.get_range_between_fighters()
        
        opp_strats = self.get_available_strategies(self.get_fighter().opponent)
        
        faster_opp_strats = 0
        clashing_opp_strats = 0
        stunning_opp_strats = 0
        killing_opp_strats_exist = False
        total_opp_strats = len(opp_strats)
        
        for opp_style, opp_base, opp_ante in opp_strats:
        
            opp_ante = opp_ante[0]
            
            opp_priority = self.get_priority(opp_style, opp_base) + opp_ante
            opp_power = self.get_power(opp_style, opp_base)
            
            if opp_priority == my_priority:
                clashing_opp_strats += 1
            elif opp_priority > my_priority:
                faster_opp_strats += 1
            
            if (opp_power > my_stun_resist and opp_priority >= my_priority):
                stunning_opp_strats += 1
            
            if (opp_power >= self.get_fighter().life):
                killing_opp_strats_exist = True
                
        all_features[my_pair_name + " When Opponent Likely to Go Faster"] = faster_opp_strats / total_opp_strats
        all_features[my_pair_name + " When Opponent Likely to Stun Me"] = stunning_opp_strats / total_opp_strats
        
        if killing_opp_strats_exist:
            all_features[my_pair_name + " When Opponent Can Kill Me"] = 1.0
        
        features_for_enemy_strat = dict()
        non_strat_specific_features = all_features.copy()
            
        for opp_style, opp_base, opp_ante in opp_strats:
            opp_pair_name = opp_style.name + opp_base.name
            if not opp_pair_name in features_for_enemy_strat.keys():
                features_for_enemy_strat[opp_pair_name] = non_strat_specific_features.copy()
                features_for_enemy_strat[opp_pair_name][my_pair_name + " when " + opp_pair_name + " Available"] = 1.0
                features_for_enemy_strat[opp_pair_name][my_pair_name + " vs " + opp_pair_name + " at Range " + str(range)] = 1.0
                all_features[my_pair_name + " when " + opp_pair_name + " Available"] = 1.0
                all_features[my_pair_name + " vs " + opp_pair_name + " at Range " + str(range)] = 1.0
                
        return features_for_enemy_strat