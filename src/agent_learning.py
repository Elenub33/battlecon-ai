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
        

    """
    Learn from the transition that was taken.
    Changes from original algorithm:
    state and nextState cannot be passed in, so they have been bookmarked and calculated as needed.
    reward is calculated based on the HP difference from last beat instead of being passed in.
    """
    def update(self):
    
        last_beat = self.recall_beat()
        last_state = last_beat['state']
        last_strat = last_beat['strategy']
        
        if last_beat == None:
            return
        
        this_state = self.current_state()
        
        reward = self.get_health_diff(this_state) - self.get_health_diff(last_state)
        
        last_q = self.get_q_value(last_state, last_strat)
        this_q = self.get_best_q_value(this_state)
        diff = self.alpha * ((reward + self.discount * this_q) - last_q)
        
        print("REWARD: {} ({} to {}). Learning from {} vs. {}, Q VALUE {} -> {} (diff {})".format(
            reward,
            self.get_fighter().opponent.effective_life(),
            self.get_fighter().effective_life(),
            last_beat['strategy'][0].name + last_beat['strategy'][1].name,
            self.get_last_enemy_pair_name(),
            last_q,
            this_q,
            diff
        ))
        
        # TODO: UPDATE ENEMY STRATEGY DISTRIBUTION IN LAST_STATE BEFORE THIS CALL
        f = self.get_features(last_state, last_strat)
        for i in f.keys():
            self.set_weight(i, self.get_weight(i) + diff * f[i])
        
        
    def conclude_game(self, winner):
        self.update()
        
        
    def get_random_strategy(self):
        return random.choice(self.get_available_strategies(self.get_fighter()))
        
        
    def get_best_strategy(self):
        best_strats, best_q = [], float('-inf')
        for strat in self.get_available_strategies(self.get_fighter()):
            q = self.get_q_value(strat)
            if q == best_q:
                best_strats.append(strat)
            elif q > best_q:
                best_strats = [strat]
                best_q = q
        if len(best_strats) > 0:
            return random.choice(best_strats), best_q
        else:
            return None, best_q
        
        
    def get_available_strategies(self, fighter):
        return [m[0] for m in fighter.mix]
        
        
    def record_chosen_strategy(self, strategy):
        self.save_beat(strategy)
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


    def save(self, filename):
        w = self.get_weights()
        f = open(filename, "w")
        f.write(json.dumps(w))
        f.close()


    def load(self, filename):
        f = open(filename, "r")
        w = json.loads(f.read())
        f.close()
        self.set_weights(w)

            
    def get_health_diff(self, state):
        return state['my_effective_life'] - state['opp_effective_life']
        
        
    """
    Remember details about the chosen strategy for learning later.
    """
    def save_beat(self, strategy):
        self.saved_beat = {'strategy': strategy, 'state': self.current_state()}
        
       
    """
    Recall details about most recently chosen strategy.
    """
    def recall_beat(self):
        if hasattr(self, 'saved_beat'):
            return self.saved_beat
        else:
            return None
        
        
    def get_last_enemy_strategy(self):
        return self.opponent.get_logged_strategies()[-1]
        
        
    def get_last_enemy_pair_name(self):
        enemy_strat = self.get_last_enemy_strategy()
        return enemy_strat[0].name + enemy_strat[1].name
        
        
    """
    Determine the value of a particular strategy according to current weights.
    """
    def get_q_value(self, state, strategy):
        f = self.get_features(state, strategy)
        val = 0.0
        for i in f.keys():
            val += self.get_weight(i) * f[i]
        return val
        
        
    """
    Determine the value of the current state given current weights.
    """
    def get_best_q_value(self, state): # TODO: not using state yet
        strategy, q_val = self.get_best_strategy()
        if strategy == None:
            return 0.0
        return q_val
        
    
    """
    Get features based on strategy and current state.
    Start with simple features and expand them as needed.
    Warning: to avoid accidentally dominating other features, each feature should be scaled from 0.0 to 1.0.
    """
    def get_features(self, state, strategy):
        features = dict()
        self.add_strategy_features(features, state, strategy)
        self.add_counterplay_features(features, state, strategy)
        return features
        
        
    def get_my_range_from_edge(self, state):
        return self._get_range_from_edge(state['my_position'])
        
        
    def get_opp_range_from_edge(self, state):
        return self._get_range_from_edge(state['opp_position'])
    
    
    def _get_range_from_edge(self, position):
        pos = state['opp_position']
        return round(min(pos, 6 - pos))
        
        
    def get_range_between_fighters(self, state):
        return round(abs(state['my_position'] - state['opp_position']))
        
    
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
        
        
    def add_strategy_features(self, features, state, strategy):
    
        # TODO: feature scales will need to be adjusted; see notes in S Note
        
        style = strategy[0]
        base = strategy[1]
        ante = strategy[2][0]
        
        pair_name = style.name + base.name
        
        range = self.get_range_between_fighters(state)
        
        # booleans for individual elements of strategy and for combination
        features[self.get_strategy_name(strategy)] = 1.0
        features[pair_name + " at Range " + str(range)] = 1.0
        features[pair_name + " at Distance " + str(self.get_my_range_from_edge(state) + " from edge"] = 1.0
        features[pair_name] = 1.0
        features[style.name] = 1.0
        features[base.name] = 1.0
        features["Ante " + str(ante)] = 1.0
        
        features[pair_name + " when Opponent Close"] = (6.0 - range) / 5.0
        features[pair_name + " when Opponent Far"] = (range - 1.0) / 5.0
        
        
    """
    Adds all possible strats to all_features and returns a dictionary containing all generic features plus all features for a specific enemy option.
    """
    def add_counterplay_features(self, features, state, my_strategy):
    
        # TODO: feature scales will need to be adjusted; see notes in S Note
        
        my_style = my_strategy[0]
        my_base = my_strategy[1]
        my_ante = my_strategy[2][0]
        
        range = self.get_range_between_fighters(state)
        
        my_pair_name = my_style.name + my_base.name
        
        my_priority = self.get_priority(my_style, my_base)
        my_stun_resist = self.get_stunguard(my_style, my_base) + self.get_soak(my_style, my_base)
        
        opp_strats = state['opp_strat_distribution'] # TODO: will need light rework once this becomes an actual distribution
        
        faster_opp_strats = 0
        clashing_opp_strats = 0
        stunning_opp_strats = 0
        killing_opp_strats_exist = False
        total_opp_strats = len(opp_strats)
        
        # TODO: Instead of simply using mean to determine likelihood here, use the distribution percentages in opp_strats
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
                
        features[my_pair_name + " When Opponent Likely to Go First"] = faster_opp_strats / total_opp_strats
        features[my_pair_name + " When Opponent Likely to Stun"] = stunning_opp_strats / total_opp_strats
        
        if killing_opp_strats_exist:
            features[my_pair_name + " When Opponent Trying to Kill Me This Beat"] = 1.0 # TODO: change this to use likelihood of a killing blow based on distribution
            
        for opp_style, opp_base, opp_ante in opp_strats:
            opp_pair_name = opp_style.name + opp_base.name
            features[my_pair_name + " when " + opp_pair_name + " Available"] = 1.0
            features[my_pair_name + " vs " + opp_pair_name + " at Range " + str(range)] = 1.0
            features[my_pair_name + " when " + opp_pair_name + " Available"] = 1.0
            features[my_pair_name + " vs " + opp_pair_name + " at Range " + str(range)] = 1.0
        
    
    def current_state(self):
        
        me = self.get_fighter()
        opp = me.opponent
    
        state = dict()
        
        # state['my_strats'] = self.get_available_strategies(me) # TODO: remove this if not needed
        state['opp_strat_distribution'] = self.get_available_strategies(opp) # TODO: this should actually be supplemented w/ percentages based on previous observations
        state['my_position'] = me.position
        state['opp_position'] = opp.position
        state['my_effective_life'] = me.effective_life()
        state['opp_effective_life'] = opp.effective_life()
        
        return state