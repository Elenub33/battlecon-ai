#!/usr/bin/env python3

# TO DO

# Pulse: when no character has board markers, can use board symmetry
# to trim fork size.  This means every character should have a function
# that says if board is currently empty (or at least symmetrical).

# KNOWN BUGS/PROBLEMS

# Cancel currently ignored by AI (not played or played around).
# Option 1: For each cancel vs. pair, solve 15x8 matrix.
#     Problems:
#         1. Takes a long time.
#         2. Imprecise, because original sims didn't take into account
#            the extra missing pair at end of beat.
#                (can simulate gain, but that's even longer.)
# Option 2: Evaluate in simulation the loss of a pair for 3 beats
#     Problems:
#         1. Always the same evaluation of lost pair.  There's also
#            preferred_range of lost/remaining card, but that's
#            very rough.
#         2. Not clear how to evaluate spent ante, which might be
#            a complete loss, or still useful this beat.

# Cancel vs. Finisher doesn't discard real base played to invoke the
# Finisher.  Can be tricky to fix, since real base played isn't
# determined.

# when a Cancel ends up killing the opponent, points are still deducted
# for spending the special action

# When a clash empties hands, the result is 0.  Actually, cycling should happen.

# Active ante triggers (Heketch's move) are reported twice when
# there's a Cancel

# Discard piles should be ordered.  For example, Kehrolyn's current form
# is the top (=latest) style that isn't a special action.

# Reveal effects happen only once, so they shouldn't change after a
# clash.  Examples: Eligor's Aegis, Aria's Ionic.  This can't be helped
# without a major refactoring.

# "Deal damage" effects are considered attacks, so dodge effects can
# cause them to miss.

# TO CHECK OPENING DISCARDS
# free_for_all (1, <name>, skip=['kehrolyn'], first_beats=True)

from operator import attrgetter
import itertools
import logging
import math
import numpy
import os.path
import pstats
import random
import sys
import time

import fighters
import solve
import utils

from agent_yaron import YaronAgent
from agent_human import HumanAgent

log = logging.getLogger(__name__)


debug_log = []

# MAIN FUNCTIONS


playable = [
  #             'abarene', not a final version
  "adjenna",
  "alexian",
  "alumis",
  "arec",
  "aria",
  #             'borneo', weak promo
  "baenvier",
  "byron",
  "cadenza",
  "cesar",
  "claus",
  "clinhyde",
  "danny",
  "demitras",
  "eligor",
  "eustace",
  #             'gerard',  too long
  "heketch",
  "hikaru",
  "iri",
  "jager",
  #             'juto', weak promo
  "kajia",
  "kallistar",
  "karin",
  "kehrolyn",
  "khadath",
  "larimore",
  "lesandra",
  "lixis",
  "luc",
  "lymn",
  "magdelina",
  "marmelee",
  "mikhail",
  #             'oriana', too long
  "ottavia",
  "rexan",
  "rukyuk",
  "runika",
  "sarafina",
  "seth",
  "shekhtur",
  "tanis",
  "tatsumi",
  "vanaah",
  "voco",
  "xenitia",
  "zaamassal",
]


def test(first=None, bases="alpha"):
    log_content = []
    random.seed(0)
    found_first = not first
    for p1_name, p2_name in utils.IterChunks(playable, 2, fill=playable[0]):
        if not found_first:
            if p1_name == first:
                found_first = True
            else:
                continue
        log.info("%s vs %s", p1_name, p2_name)
        start_time = time.time()
        p1 = YaronAgent(p1_name, bases)
        p2 = YaronAgent(p2_name, bases)
        game = Game.from_start(p1, p2, default_discards=True)
        game_log, unused_winner = game.play_game()
        end_time = time.time()
        log.info("total time: %d s", end_time - start_time)
        log_content.extend(game_log)
    logfilename = "logs/v1.1_test"
    with open(logfilename, "w") as f:
        for g in log_content:
            f.write(g + "\n")


def play():
    names = sorted([k.capitalize() for k in fighters.character_dict])
    while True:
        print("Select your character:")
        idx = utils.MenuPrompt(names + ["Random"], num_columns=3)
        human_name = names.pop(idx if idx < len(names) else random.randint(0, len(names) - 1))
        print(f"You will be playing {human_name}\n")

        print("Select AI character:")
        idx = utils.MenuPrompt(names + ["Random"], num_columns=3)
        ai_name = names.pop(idx if idx < len(names) else random.randint(0, len(names) - 1))
        print(f"AI will be playing {ai_name}\n")

        print("Which set of bases should be used?")
        idx = utils.MenuPrompt(
            [
                "Standard bases",
                "Beta bases",
                "I use standard, AI uses beta",
                "I use beta, AI uses standard",
            ]
        )
        ai_bases = "beta" if idx in (1, 2) else "alpha"
        human_bases = "beta" if idx in (1, 3) else "alpha"
        
        human = HumanAgent(human_name, human_bases)
        ai = YaronAgent(ai_name, ai_bases)
        
        print("Default Discards?")
        default_discards = utils.MenuPrompt(["No", "Yes"])
        game = Game.from_start(
            ai,
            human,
            default_discards=default_discards
        )
        game.select_finishers()
        game_log, unused_winner = game.play_game()
        if not os.path.exists("logs"):
            os.mkdir("logs")
        if ai_bases == "beta":
            ai_name = ai_name + "_beta"
        if human_bases == "beta":
            human_name = human_name + "_beta"
        basename = "logs/" + ai_name + "(AI)_vs_" + human_name
        name = save_log(basename, game_log)
        print("Log saved at: ", name)
        print()
        print("\nAnother game?")
        if not utils.MenuPrompt(["No", "Yes"]):
            break


def save_log(basename, log):
    for i in range(1, 10000):
        name = basename + "[" + str(i) + "].txt"
        if not os.path.isfile(name):
            with open(name, "w") as f:
                for g in log:
                    f.write(g + "\n")
            break
    return name


# Play everyone against everyone
def beta_challenge(next_pair=None, last_pair=None, beta0=False, beta1=False):
    if next_pair is None:
        next_pair = (playable[0], playable[0])
    if last_pair is None:
        last_pair = (playable[-1], playable[-1])
    firsts = [name for name in playable if name >= next_pair[0] and name <= last_pair[0]]
    for first in firsts:
        seconds = playable
        if first == next_pair[0]:
            seconds = [name for name in seconds if name >= next_pair[1]]
        if first == last_pair[0]:
            seconds = [name for name in seconds if name <= last_pair[1]]
        for second in seconds:
            if (beta0 == beta1 and first < second) or (beta0 != beta1 and first != second):
                duel(first, second, 1, beta0, beta1)


# Play consecutive pairs, so that each character plays one as alpha
# and one as delta.
def alpha_vs_delta_challenge(first=None):
    n = len(playable)
    for i in range(n):
        if playable[i] >= first:
            duel(playable[i], playable[(i + 1) % n], 1, "alpha", "delta")


# play everyone in names against everyone from start onwards, unless in skip
def free_for_all(
  repeat, names=None, start=None, skip=[], raise_exceptions=True, first_beats=False
):
    if isinstance(names, str):
        names = [names]
    if names is None:
        names = playable
    for i in range(len(playable)):
        for j in range(i + 1, len(playable)):
            if (
              playable[i] in names and playable[j] >= start and playable[j] not in skip
            ) or (
              playable[j] in names and playable[i] >= start and playable[i] not in skip
            ):
                if raise_exceptions:
                    duel(playable[i], playable[j], repeat, first_beats=first_beats)
                else:
                    try:
                        duel(playable[i], playable[j], repeat, first_beats=first_beats)
                    except Exception as e:
                        print("duel: %s vs. %s" % (playable[i], playable[j]))
                        print("exception", e)


def duel(name0, name1, repeat, bases0="alpha", bases1="alpha", first_beats=False):
    victories = [0, 0]
    print(name0, "vs.", name1)
    log = []
    start = time.time()
    for i in range(repeat):
        game = Game.from_start(
            YaronAgent(name0, bases0), YaronAgent(name0, bases1), default_discards=False, first_beats=first_beats
        )
        game_log, winner = game.play_game()
        log.append("GAME %d\n-------\n" % i)
        log.extend(game_log)
        if winner == None:
            victories[0] += 0.5
            victories[1] += 0.5
        else:
            winner = winner.lower()
        if winner == name0:
            victories[0] += 1
        elif winner == name1:
            victories[1] += 1
        print(winner, end=" ")
        sys.stdout.flush()
    print()
    print(victories[0], ":", victories[1])
    end = time.time()
    logfilename = "logs/" + name0 + "_" + name1 + "_log.txt"
    time_string = "total_time: %d" % (end - start)
    log.append(time_string)
    print(time_string)
    with open(logfilename, "w") as f:
        for g in log:
            f.write(g + "\n")


# runs one beat from file data
def play_beat(filename="starting states/start.txt"):
    game = Game.from_file(filename)
    print("Simulating...")
    game.simulate_beat()
    print("Solving...")
    game.solve()
    game.print_solution()
    return game


def play_start_beat(agent0, agent1):
    game = Game.from_start(agent0, agent1, default_discards=True, first_beats=True)
    game.play_game()
    return game


# Profiling

# copy this:
# cProfile.run ("play_beat ('vanaah', 'demitras')", 'profstat')
# profile ('profstat')
def profile(pfile, n=30):
    p = pstats.Stats(pfile)
    p.strip_dirs().sort_stats("cumulative").print_stats(n)


# input functions


def string_is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# check if some line in lines starts with start, and return it.
def find_start_line(lines, start):
    for line in lines:
        if line.startswith(start):
            return line
    return None


# check if some line in lines starts with start, and return its index
def find_start_index(lines, start):
    for i, line in enumerate(lines):
        if line.startswith(start):
            return i
    return None


def find_start(lines, start):
    return bool(find_start_line(lines, start))


# check if some line in lines ends with end, and return it.
def find_end_line(lines, end):
    for line in lines:
        if line.endswith(end):
            return line
    return None


def find_end(lines, end):
    return bool(find_end_line(lines, end))


def all_mean_priorities():
    chars = [
      character(the_game=None, n=0) for character in fighters.character_dict.values()
    ]
    chars = sorted(chars, key=attrgetter("mean_priority"), reverse=True)
    for c in chars:
        print("%.1f  %s" % (c.mean_priority, c.name))
    print()
    print("Mean: %.1f" % (sum(c.mean_priority for c in chars) / len(chars)))
    print("Median: %.1f" % chars[len(chars) / 2].mean_priority)


# GENERAL CLASSES


# main game class, holds all information and methods
class Game:

    # Constants for indicating special events in result matrix.
    # These will never actually given to the solver - they need to
    # be dealt with in pre-processing.
    # (all constants are floats, so that the numpy array stays a float array)
    CLASH_INDICATOR = -1000.0
    CANCEL_0_INDICATOR = -2000.0
    CANCEL_1_INDICATOR = -2001.0
    CANCEL_BOTH_INDICATOR = -2002.0
    CANCEL_INDICATORS = set(
        [CANCEL_0_INDICATOR, CANCEL_1_INDICATOR, CANCEL_BOTH_INDICATOR]
    )
    # Very good/bad result constant (used to prevent certain strats
    # from being chosen by AI:
    EXTREME_RESULT = 20.0

    # Constants for priorities of deciding where you are next beat.
    CHOOSE_POSITION_NOW = 2
    CHOOSE_POSITION_BEFORE_ATTACK_PAIRS = 1
    CHOOSE_POSITION_IN_ANTE = 0

    @staticmethod
    def from_file(file_name):
        """Create non-interactive game from text file.
            Text file is beat situation report as written to log by a previous game.
            """
        with open(file_name) as f:
            lines = [line for line in f]
        char1_start = 0
        while lines[char1_start] != "\n":
            char1_start += 1
        char1_start += 1
        char1_end = char1_start
        while lines[char1_end] != "\n":
            char1_end += 1
        board_start = char1_end
        while lines[board_start] == "\n":
            board_start += 1

        name0 = lines[0][:-1].lower()
        name1 = lines[char1_start][:-1].lower()
        bases0, bases1 = ("alpha", "alpha")
        if name0.endswith(" bases)"):
            bases0 = name0.split()[-2]
            name0 = name0[: -(len(bases0) + 9)]
        if name1.endswith(" bases)"):
            bases1 = name1.split()[-2]
            name1 = name1[: -(len(bases1) + 9)]

        game = Game(YaronAgent(name0, bases0), YaronAgent(name1, bases))
        lines0 = lines[2 : char1_start - 1]
        lines1 = lines[char1_start + 2 : char1_end]
        board = lines[board_start]
        a0 = game.player[0].board_addendum_lines
        a1 = game.player[1].board_addendum_lines
        addendum0 = lines[board_start + 1 : board_start + 1 + a0]
        addendum1 = lines[board_start + 1 + a0 : board_start + 1 + a0 + a1]
        game.player[0].read_my_state(lines0, board, addendum0)
        game.player[1].read_my_state(lines1, board, addendum1)
        game.debugging = True
        game.interactive_mode = True
        game.initialize_simulations()
        game.interactive_mode = False
        game.debugging = False
        return game

    @staticmethod
    def from_start(
        agent0,
        agent1,
        default_discards=True,
        cheating=0,
        first_beats=False,
    ):
        """Create a game in starting position."""
        game = Game(agent0, agent1, cheating, first_beats=first_beats)
        game.set_starting_setup(default_discards, use_special_actions=not first_beats)
        game.initialize_simulations()
        return game

    def __init__(
        self, agent0, agent1, cheating=0, first_beats=False
    ):

        agent0.initialize_game(self, 0)
        agent1.initialize_game(self, 1)
        
        self.range_weight = 0.3
        # fast clash evaluation - can only be used for one beat checks
        self.clash0 = False
        self.interactive = agent1.is_human()
        self.cheating = cheating
        # If first_beats==True, we're checking initial discards,
        # so we only play two beats, and start the game with all cards
        # in hand.
        self.first_beats = first_beats
        # Initial beat is 1, even if starting from file.  Might need changing.
        self.current_beat = 1

        self.interactive_mode = False
        self.replay_mode = False
        self.interactive_counter = None
        self.log = []
        
        self.player = [
            agent0,
            agent1
        ]
        self.fighter = [
            agent0.get_fighter(),
            agent1.get_fighter()
        ]
        for i in range(2):
            self.player[i].set_opponent(self.player[1 - i])
            self.fighter[i].set_mean_priority_effects()
        self.debugging = False
        self.reporting = False

    # sets default state for current characters
    def set_starting_setup(self, default_discards, use_special_actions):
        for f in self.fighter:
            f.set_starting_setup(default_discards, use_special_actions)

    def select_finishers(self):
        for p in self.player:
            p.select_finisher()

    def initialize_simulations(self):
        # save initial game state
        self.initial_state = self.initial_save()
        # evaluate game situation, as reference point for further evaluation
        self.reset()
        self.initial_evaluation = self.evaluate()

    # Play a game from current situation to conclusion
    def play_game(self):
        full_names = [f.name_with_base_set() for f in self.fighter]
        log = ["\n" + " vs. ".join(full_names)]
        for f in self.fighter:
            log.append(
              "Chosen finisher for %s: " % f.name + ", ".join(o.name for o in f.finishers)
            )
        # Loop over beats:
        while True:
            log.append("\nBeat %d" % self.current_beat)
            log.append("-------\n")
            log.extend(self.situation_report())
            self.initialize_simulations()
            if self.interactive:
                self.dump(log)
            self.reporting = False
            self.simulate_beat()
            self.log_unbeatable_strategies(log)
            self.solve()
            self.reporting = True
            log.extend(self.make_pre_attack_decision() + [""])
            if self.interactive:
                self.dump(log)
                if self.cheating > 0:
                    self.dump(self.report_solution())
            else:
                log.extend(self.report_solution())
            final_state, report = self.execute_beat()
            log.extend(report)
            if final_state.winner != None:
                break
            if self.first_beats and self.current_beat == 2:
                break
            self.full_restore(final_state)
            self.prepare_next_beat()
        winner = final_state.winner
        if winner == 0.5 or winner is None:
            winner = None
        else:
            winner = self.player[winner].get_name()
        self.dump(log)
        return self.log, winner

    def situation_report(self):
        report = []
        for f in self.fighter:
            report.extend(f.situation_report())
            report.append("")
        report.extend(self.get_board())
        return report

    def log_unbeatable_strategies(self, log):
        # check if there's a 100% positive strategy, and note it in log:
        # disregard special actions
        if self.interactive:
            return
        n = len(self.pads[0])
        m = len(self.pads[1])
        for i in range(n):
            for j in range(m):
                results = numpy.array(self.results[i][j])
                s0 = self.strats[0][i]
                s1 = self.strats[1][j]
                regular_0 = [
                  k for k in range(len(s0)) if not isinstance(s0[k][0], fighters.SpecialAction)
                ]
                regular_1 = [
                  k for k in range(len(s1)) if not isinstance(s1[k][0], fighters.SpecialAction)
                ]
                results = results[regular_0, :][:, regular_1]
                row_values = results.min(1)
                if row_values.max() > 0:
                    for k in range(len(row_values)):
                        if row_values[k] > 0:
                            if n > 1:
                                log.append("Given %s by %s" % (self.pads[0][i], self.player[0].get_fighter()))
                            if m > 1:
                                log.append("Given %s by %s" % (self.pads[1][j], self.player[1].get_fighter()))
                            log.append(
                              "Unbeatable strategy for %s: %s: %.2f"
                              % (
                                self.player[0].get_name(),
                                self.player[0].get_strategy_name(s0[regular_0[k]]),
                                row_values[k],
                              )
                            )
                    log.append("")
                col_values = results.max(0)
                if col_values.min() < 0:
                    for k in range(len(col_values)):
                        if col_values[k] < 0:
                            if n > 1:
                                log.append("Given %s by %s" % (self.pads[0][i], self.player[0]))
                            if m > 1:
                                log.append("Given %s by %s" % (self.pads[1][j], self.player[1]))
                            log.append(
                              "Unbeatable strategy for %s: %s: %.2f"
                              % (
                                self.player[1].get_name(),
                                self.player[1].get_strategy_name(s1[regular_1[k]]),
                                col_values[k],
                              )
                            )
                    log.append("")

    # empty given log into Game.log; print it if game is interactive
    def dump(self, log):
        for line in log:
            self.log.append(line)
            if self.interactive:
                print(line)
        log[:] = []

    def logfile_name(self):
        return "%s_%s" % (self.fighter[0].logfile_name(), self.fighter[1].logfile_name())

    # makes snapshot of game state (pre strategy selection)
    def initial_save(self):
        state = GameState()
        state.player_states = [p.initial_save() for p in self.player]
        state.current_beat = self.current_beat
        return state

    def initial_restore(self, state):
        for i in range(2):
            self.player[i].initial_restore(state.player_states[i])
        self.current_beat = state.current_beat

    # makes full snapshot, mid beat
    def full_save(self, stage):
        state = GameState()
        state.player_states = [p.full_save() for p in self.player]
        state.reports = [s for s in self.reports]
        state.decision_counter = self.decision_counter
        state.winner = self.winner
        state.active = self.active
        state.stop_the_clock = self.stop_the_clock
        state.current_beat = self.current_beat
        state.stage = stage
        return state

    def full_restore(self, state):
        for i in range(2):
            self.player[i].full_restore(state.player_states[i])
        self.reports = [s for s in state.reports]
        self.decision_counter = state.decision_counter
        self.winner = state.winner
        self.active = state.active
        self.stop_the_clock = state.stop_the_clock
        self.current_beat = state.current_beat

    # resets game state to start of beat position (post strategy selection)
    def reset(self):
        for p in self.player:
            p.reset()
        self.reports = []
        self.fork_decisions = []
        self.decision_counter = 0
        self.winner = None
        self.active = None
        self.stop_the_clock = False

    # run simulation for all strategies, creating result table
    def simulate_beat(self):
        # get lists of strategies from both players
        for p in self.player:
            p.get_fighter().strats = p.get_all_possible_strategies()
        # run simulations, create result table
        self.results = [
            [self.simulate(s0, s1) for s1 in self.player[1].get_fighter().strats]
            for s0 in self.player[0].get_fighter().strats
        ]

        self.initial_restore(self.initial_state)

        # remove redundant finisher strategies
        # (that devolve into identical cancels)
        self.remove_redundant_finishers()

        # Usually this does nothing, but some characters might need to
        # fix the result tables and strategies (e.g. Seth, Ottavia).
        for f in self.fighter:
            f.post_simulation_processing()

        # Once we're done with special processing, we can discard
        # the full final state of each simulation, and keep just
        # the evaluation.
        self.results = [[float(result[0]) for result in row] for row in self.results]

        # For each player, make list of strategies, separated into
        # sub lists by pre-attack decision (pad).
        self.pads = [[], []]
        self.strats = [[], []]
        for i, p in enumerate(self.player):
            # group player strategies by pre attack decision.
            for pad, pad_strats in itertools.groupby(p.get_fighter().strats, lambda s: s[2][2]):
                self.pads[i].append(pad)
                self.strats[i].append(list(pad_strats))
        # split results into subtables according to pads:
        self.results = [
            [
                self.get_pad_subresults(
                    self.results, [p.get_fighter().strats for p in self.player], pad0, pad1
                )
                for pad1 in self.pads[1]
            ]
            for pad0 in self.pads[0]
        ]

    def remove_redundant_finishers(self):
        redundant_finishers = []
        s0 = self.player[0].get_fighter().strats
        for i in range(len(self.results)):
            if isinstance(s0[i][1], fighters.Finisher):
                for ii in range(len(self.results)):
                    if isinstance(s0[ii][1], fighters.Cancel) and s0[ii][2] == s0[i][2]:
                        if [res[0] for res in self.results[i]] == [
                          res[0] for res in self.results[ii]
                        ]:
                            redundant_finishers.append(i)
                            break
        self.results = [
            self.results[i] for i in range(len(self.results)) if i not in redundant_finishers
        ]
        self.player[0].get_fighter().strats = [
            s0[i] for i in range(len(s0)) if i not in redundant_finishers
        ]

        redundant_finishers = []
        s1 = self.player[1].get_fighter().strats
        for j in range(len(self.results[0])):
            if isinstance(s1[j][1], fighters.Finisher):
                for jj in range(len(self.results[0])):
                    if isinstance(s1[jj][1], fighters.Cancel) and s1[jj][2] == s1[j][2]:
                        if [row[j][0] for row in self.results] == [
                          row[jj][0] for row in self.results
                        ]:
                            redundant_finishers.append(j)
                            break
        self.results = [
            [r[j] for j in range(len(r)) if j not in redundant_finishers]
            for r in self.results
        ]
        self.player[1].get_fighter().strats = [
            s1[j] for j in range(len(s1)) if j not in redundant_finishers
        ]

    def get_pad_subresults(self, results, strats, pad0, pad1):
        ii = [i for i, s in enumerate(strats[0]) if s[2][2] == pad0]
        jj = [i for i, s in enumerate(strats[1]) if s[2][2] == pad1]
        return [[results[i][j] for j in jj] for i in ii]

    # if state != None, this is a forked simulation
    def simulate(self, s0, s1, state=None):
        # in a forked simulation, restore the given state
        if state != None:
            self.full_restore(state)

        # if this isn't a forked simulation, execute initial setup
        # (up to pulse check)
        else:
            # restore situation to initial pre-strategy state
            self.initial_restore(self.initial_state)

            self.player[0].set_chosen_strategy(s0)
            self.player[1].set_chosen_strategy(s1)

            # resets basic beat information to start of beat state
            self.reset()

            if self.reporting:
                self.report("")
                for p in self.player:
                    self.report(p.get_name() + ": " + p.get_chosen_strategy_name())
                self.report("")

            for f in self.fighter:
                f.pre_attack_decision_effects()

            # Put attack pairs in discard.
            for p in self.player:
                strat = p.get_chosen_strategy()
                f = p.get_fighter()
                f.style = strat[0]
                f.base = strat[1]
                if not isinstance(f.style, fighters.SpecialAction):
                    # Adding to existing set,
                    # because Vanaah's token might already be there.
                    f.discard[0] |= set([f.style, f.base])

            for f in self.fighter:
                f.ante_trigger()

            # Attack pairs are now active.
            for f in self.fighter:
                f.set_active_cards()

            # Special Actions

            # fighters.Finishers devolve into fighters.Cancels above 7 life
            # or if failing to meet their specific conditions
            for f in self.fighter:
                if isinstance(f.base, fighters.Finisher) and f.base.devolves_into_cancel():
                    f.base = f.cancel

            # fighters.Cancel - return an appropriate cancel indicator
            # (depending on who cancelled).
            # This will be solved retroactively.
            # Check that there's no Pulse that trumps the fighters.Cancel.
            cancel = [f.base is f.cancel for f in self.fighter]
            pulse = [f.base is f.pulse for f in self.fighter]
            # A double Pulse devolves to a double fighters.Cancel.
            if all(pulse):
                final_state = self.full_save(None)
                return self.CANCEL_BOTH_INDICATOR, final_state, self.fork_decisions[:]
            if any(cancel) and not any(pulse):
                final_state = self.full_save(None)
                if all(cancel):
                    return self.CANCEL_BOTH_INDICATOR, final_state, self.fork_decisions[:]
                if cancel[0]:
                    return self.CANCEL_0_INDICATOR, final_state, self.fork_decisions[:]
                if cancel[1]:
                    return self.CANCEL_1_INDICATOR, final_state, self.fork_decisions[:]

            # save state before pulse phase (stage 0)
            state = self.full_save(0)

        # catch ForkExceptions and WinExceptions
        try:

            # Stage 0 includes: pulse check, reveal trigger, clash check.
            if state.stage <= 0:
                pulsing_fighters = [f for f in self.fighter if f.base is f.pulse]
                # With one pulse - fork to decide new player positions.
                # Not using execute_move, because Pulse negates any blocking
                # or reaction effects (including status effects from last beat).
                if len(pulsing_fighters) == 1:
                    pulser = pulsing_fighters[0]
                    opp = pulser.opponent
                    # If opponent used fighters.Cancel/fighters.Finisher, we have them
                    # retroactively choose which base activated it.
                    # and put the base and the special action in
                    # discard 0, so that they'll cycle.
                    if opp.style is opp.special_action:
                        if opp.base is opp.cancel:
                            options = opp.cancel_generators.copy()
                            if any(finisher.devolves_into_cancel() for finisher in opp.finishers):
                                options |= opp.finisher_generators
                        else:
                            options = opp.finisher_generators.copy()
                        options &= set(opp.bases)
                        options -= opp.discard[1] | opp.discard[2]
                        options = list(options)
                        prompt = "Which base did you use to play your special action?"
                        ans = self.make_fork(len(options), opp, prompt, [o.name for o in options])
                        opp.discard[0].add(options[ans])
                        opp.discard[0].add(opp.special_action)

                    # Perform the Pulse.
                    pairs = list(itertools.permutations(range(7), 2))
                    prompt = "Choose positions after Pulse:"
                    options = []
                    if pulser.agent.is_human() and self.interactive_mode:
                        current_pair = (self.player[0].position, self.player[1].position)
                        for pair in pairs:
                            (self.player[0].position, self.player[1].position) = pair
                            options.append(self.get_basic_board())
                        (self.player[0].position, self.player[1].position) = current_pair
                    (self.player[0].position, self.player[1].position) = pairs[
                      self.make_fork(len(pairs), pulser, prompt, options)
                    ]
                    if self.reporting:
                        self.report("%s Pulses:" % pulser)
                        for s in self.get_board():
                            self.report(s)
                    # Skip directly to cycle and evaluation phase.
                    if pulsing_fighters:
                        self.stop_the_clock = True
                        return self.cycle_and_evaluate()

                for f in self.fighter:
                    f.reveal_trigger()

                # clash_priority is fraction
                # that represents autowinning/losing clashes
                priority = [f.get_priority() for f in self.fighter]
                clash_priority = [
                    priority[i] + f.clash_priority() for i, f in enumerate(self.fighter)
                ]

                if self.reporting:
                    self.report("Priorities:  %d | %d" % (priority[0], priority[1]))

                if clash_priority[0] > clash_priority[1]:
                    self.active = self.player[0]
                    if self.reporting:
                        self.report(self.active.get_name() + " is active")
                elif clash_priority[1] > clash_priority[0]:
                    self.active = self.player[1]
                    if self.reporting:
                        self.report(self.active.get_name() + " is active")
                # priority tie
                else:
                    # Two clashing finishers turn into cancels.
                    if isinstance(self.fighter[0].base, fighters.Finisher) and isinstance(
                      self.fighter[1].base, fighters.Finisher
                    ):
                        final_state = self.full_save(None)
                        return self.CANCEL_BOTH_INDICATOR, final_state, self.fork_decisions[:]
                    else:
                        if self.reporting:
                            self.report("Clash!\n")
                        final_state = self.full_save(None)
                        if self.clash0:
                            return 0, final_state, self.fork_decisions[:]
                        else:
                            return self.CLASH_INDICATOR, final_state, self.fork_decisions[:]
                state = self.full_save(1)

            # start triggers
            if state.stage <= 1:
                for f in self.fighters_in_order():
                    f.start_trigger()
                state = self.full_save(2)

            # player activations
            if state.stage <= 2:
                active = self.active.get_fighter()
                # check if attack needs to be re-executed
                while active.attacks_executed < active.max_attacks:
                    if active.is_stunned():
                        break
                    self.activate(active)
                    active.attacks_executed += 1
                state = self.full_save(3)
            if state.stage <= 3:
                reactive = self.active.opponent.get_fighter()
                # check if attack needs to be re-executed
                while reactive.attacks_executed < reactive.max_attacks:
                    if reactive.is_stunned():
                        break
                    self.activate(reactive)
                    reactive.attacks_executed += 1
                state = self.full_save(4)

            # end triggers and evaluation
            for f in self.fighters_in_order():
                f.end_trigger()

            for f in self.fighter:
                f.unique_ability_end_trigger()

            return self.cycle_and_evaluate()

        # when a fork is raised, rerun the simulation with n_options values
        # appended to self.fork_decisions
        except utils.ForkException as fork:
            # if a fork is created in interactive mode
            if self.interactive_mode:
                # save current state, so that we come back here in next sim
                self.interactive_state = state
                # save the decision counter
                # this is where the replay will go interactive again
                self.interactive_counter = self.decision_counter
                # switch to thinking mode
                self.interactive_mode = False
            # make list of results for all fork options
            results = []
            # locally remember the decision list, and reset it before each branch
            fork_decisions = self.fork_decisions[:]
            ##            print fork.forking_player, "-", fork.n_options
            ##            print "fork decisions:", fork_decisions
            for option in range(fork.n_options):
                self.fork_decisions = fork_decisions + [option]
                results.append(self.simulate(self.player[0].get_chosen_strategy(), self.player[1].get_chosen_strategy(), state))
            values = [r[0] for r in results]
            val = max(values) if fork.forking_player.get_player_number() == 0 else min(values)
            i = values.index(val)
            return results[i]

        # when a player wins, give them points
        except utils.WinException as win:
            w = win.winner
            self.winner = w
            if self.reporting:
                if w == 0.5:
                    self.report("THE GAME IS TIED!")
                else:
                    self.report(self.player[w].get_name().upper() + " WINS!")
            if w == 0.5:
                value = 0
            else:
                value = ((-1) ** w) * (5 + self.initial_state.player_states[1 - w].life)
            final_state = self.full_save(None)
            return value, final_state, self.fork_decisions[:]

    def players_in_order(self):
        if self.active == self.player[0]:
            return [self.player[0], self.player[1]]
        else:
            return [self.player[1], self.player[0]]
            
    def fighters_in_order(self):
        return [p.get_fighter() for p in self.players_in_order()]

    # activation for one player
    def activate(self, f):
        f.before_trigger()
        if f.is_attacking():
            if f.can_hit() and f.opponent.can_be_hit() and not f.opponent.replace_hit():
                if self.reporting:
                    self.report(f.agent.get_name() + " hits")
                f.hit_trigger()
                f.opponent.take_a_hit_trigger()
                # hits_scored is set after triggers, so that triggers can check
                # if this is first hit this beat
                f.hits_scored += 1
                if f.base.deals_damage:
                    f.deal_damage(f.get_power())
            else:
                if self.reporting:
                    self.report(f.agent.get_name() + " misses")
        f.opponent.after_trigger_for_opponent()
        f.after_trigger()

    def cycle_and_evaluate(self):
        for f in self.fighter:
            f.cycle()

        # If 15 beats have been played, raise WinException
        if self.current_beat == 15 and not self.stop_the_clock:
            if self.reporting:
                self.report("Game goes to time")
            for f in self.fighter:
                if f.wins_on_timeout():
                    raise utils.WinException(f.my_number)
            diff = self.fighter[0].life - self.fighter[1].life
            if diff > 0:
                raise utils.WinException(0)
            elif diff < 0:
                raise utils.WinException(1)
            else:
                # A tie.
                raise utils.WinException(0.5)

        evaluation = self.evaluate()
        if self.debugging:
            for p in self.player:
                self.report(
                  p.get_name()
                  + "'s life: "
                  + str(self.initial_state.player_states[p.get_player_number()].life)
                  + " -> "
                  + str(p.get_fighter().life)
                )
            self.report(
                "preferred ranges: %.2f - %.2f    [%d]"
                % (
                    self.player[0].get_preferred_range(),
                    self.player[1].get_preferred_range(),
                    self.distance(),
                )
            )
            self.report(
              "range_evaluation: %.2f - %.2f = %.2f"
              % (
                self.fighter[0].evaluate_range(),
                self.fighter[1].evaluate_range(),
                self.fighter[0].evaluate_range() - self.fighter[1].evaluate_range(),
              )
            )
            self.report(
              "eval: %.2f vs %.2f gives %.2f"
              % (evaluation, self.initial_evaluation, evaluation - self.initial_evaluation)
            )
        final_state = self.full_save(None)
        ##        if self.reporting:
        ##            print "decisions returned: ", self.fork_decisions
        return evaluation - self.initial_evaluation, final_state, self.fork_decisions[:]

    def evaluate(self):
        # Some characters (Tanis, Sarafina, Arec with clone)
        # can end the beat in a "superposition" of different positions.
        # We need to evaluate every possibility.
        real_positions = [f.position for f in self.fighter]
        positions = [f.get_superposed_positions() for f in self.fighter]
        # This is the order in which they'll collapse the superposition.
        priorities = [f.get_superposition_priority() for f in self.fighter]
        evaluations = []
        for p0 in positions[0]:
            row = []
            for p1 in positions[1]:
                if p0 != p1:
                    self.fighter[0].position = p0
                    self.fighter[1].position = p1
                    row.append(self.player[0].evaluate() - self.player[1].evaluate())
            if row:
                evaluations.append(row)
        for i in range(2):
            self.player[i].position = real_positions[i]
        # Higher priority chooses first, so evaluated last.
        # In case of tie, player 0 chooses before player 1
        # (it's arbitrary, but that's how it will happen during the ante phase)
        if priorities[0] >= priorities[1]:
            minima = [min(row) for row in evaluations]
            value = max(minima)
        else:
            evaluations = list(zip(*evaluations))
            maxima = [max(row) for row in evaluations]
            value = min(maxima)

        return value + (
            self.player[0].evaluate_superposition() - self.player[1].evaluate_superposition()
        )

    def distance(self):
        return int(abs(self.fighter[0].position - self.fighter[1].position))  # int cast

    # Number of beats expected until end of game.
    def expected_beats(self):
        # TODO: This takes into account alternate counting of own life
        # (like Byron's), but not alternate counting of opponent's life
        # (like Adjenna's).
        return min(
          0.5 * min([f.effective_life() for f in self.fighter]), 15 - self.current_beat
        )

    # check for a fork
    # n_options = number of branches in fork
    # player = who makes the decision?
    # prompt = string prompting a human player for this decision
    # options = strings enumerating the options for the player
    #   (if options = None, the question is numerical, no enumerated options)
    # choice = when this is not None, this is a "fake" fork, in which
    #       the AI will always pick the given choice.
    #       human player will be prompted normally
    def make_fork(self, n_options, fighter, prompt, options=None, choice=None):
        # if no options, it's a bug.
        assert n_options > 0, "Fork with 0 options"
        # if just 1 option, no fork needed
        if n_options == 1:
            return 0

        # If the character who makes the decision is controlled by the opponent,
        # let the opponent make the decision
        controlled = fighter.opponent.controls_opponent()
        if controlled:
            fighter = fighter.opponent
            prompt = "Make this decision for opponent:\n" + prompt

        # when a game against a human player is in active progress
        # the player is prompted to make a decision,
        # which is added to the list
        # any further decisions (from a replay) are deleted
        if self.interactive_mode and not self.replay_mode and fighter.agent.is_human():
            # prompt for decision, and delete any postulated decisions
            print(prompt)
            if options is None:
                print("[0-%d]" % (n_options - 1))
                decision = utils.ReadNumber(0, n_options)
            else:
                decision = utils.MenuPrompt(options)
            self.fork_decisions = self.fork_decisions[: self.decision_counter]
            self.fork_decisions.append(decision)
            self.decision_counter += 1
            return decision
        # in all other situations, check whether the decision was
        # made

        # decision is in list:
        if self.decision_counter < len(self.fork_decisions):
            # in replay mode, switch back to interactive at correct spot
            if self.replay_mode and self.decision_counter == self.interactive_counter:
                self.replay_mode = False
            # return decision from list, increment decision counter
            decision = self.fork_decisions[self.decision_counter]
            ##            if self.debugging:
            ##                print "returning fork"
            ##                print "fd:", self.fork_decisions
            ##                print "counter:", self.decision_counter
            ##                print "decision:", decision
            self.decision_counter += 1
            return decision
        # new decision:
        else:
            # If it's a fake fork, return the given choice
            # and add it to fork_decisions.
            # (unless the decision is controlled by opponent - in which
            # case ignore the given a choice and make it normally.)
            if choice != None and not controlled:
                self.fork_decisions.append(choice)
                self.decision_counter += 1
                return choice
            # in a real fork, raise the Exception
            # in interactive mode, saving the current state for next sim
            # and switching to thinking mode are handled by the except block
            else:
                raise utils.ForkException(n_options, fighter.agent)

    def get_board(self):
        addenda = []
        for f in self.fighter:
            a = f.get_board_addendum()
            if a:
                if isinstance(a, str):
                    a = [a]
                addenda += a
        return [""] + [self.get_basic_board()] + addenda + [""]

    def get_basic_board(self):
        board = ["."] * 7
        for f in self.fighter:
            if f.position is not None:
                # TODO :: Figure out why f.position is sometimes a float
                board[int(f.position)] = f.get_board_symbol()
        return "".join(board)

    # find minmax for results table
    def solve(self):
        self.value = [[None] * len(self.strats[1]) for s in self.strats[0]]
        for f in self.fighter:
            f.mix = [[None] * len(self.strats[1]) for s in self.strats[0]]
        self.pre_clash_results = [
          [[row[:] for row in pad_col] for pad_col in pad_row] for pad_row in self.results
        ]
        for pad0 in range(len(self.strats[0])):
            for pad1 in range(len(self.strats[1])):
                value, mix0, mix1 = self.solve_per_pad(
                  self.results[pad0][pad1],
                  self.pre_clash_results[pad0][pad1],
                  self.strats[0][pad0],
                  self.strats[1][pad1],
                )
                self.value[pad0][pad1] = value
                self.fighter[0].mix[pad0][pad1] = mix0
                self.fighter[1].mix[pad0][pad1] = mix1

    # Find minmax for one results table (for given set of pads).
    def solve_per_pad(self, results, pre_clash_results, strats0, strats1):
        self.fix_clashes(results, pre_clash_results, strats0, strats1)
        self.fix_cancels(results)
        array_results = numpy.array(results)
        
        stratmix0, value0 = self.player[0].calculate_strategy_mix(strats0, array_results)
        stratmix1, value1 = self.player[1].calculate_strategy_mix(strats1, -array_results.transpose())
        
        # if p0 does not estimate a state value, flip p1's and use that
        if value0 == 0:
            value = - value1
        else:
            value = value0
        
        return value, stratmix0, stratmix1

    def make_pre_attack_decision(self):
        # Player 0 makes a decision.
        values = [row[0] for row in self.value]
        d0 = max([(val, i) for i, val in enumerate(values)])[1]
        # Player 1 makes a decision.
        if self.interactive:
            d1 = self.player[1].input_pre_attack_decision_index()
        else:
            values = self.value[0]
            d1 = min([(val, i) for i, val in enumerate(values)])[1]
        self.value = self.value[d0][d1]
        self.results = self.results[d0][d1]
        self.pre_clash_results = self.pre_clash_results[d0][d1]
        for f in self.fighter:
            f.mix = f.mix[d0][d1]
        self.fighter[0].final_pad = self.pads[0][d0]
        self.fighter[1].final_pad = self.pads[1][d1]
        return self.fighter[0].pre_attack_decision_report(self.pads[0][d0]) + self.fighter[
          1
        ].pre_attack_decision_report(self.pads[1][d1])

    def execute_beat(self, post_clash=False):
        self.initial_restore(self.initial_state)
        s0 = self.player[0].choose_strategy(post_clash)
        if self.interactive and self.cheating == 2:
            print(self.player[0], "plays", self.player[0].get_strategy_name(s0))
        s1 = self.player[1].choose_strategy(post_clash)
        if self.interactive:
            self.interactive_state = None
            self.replay_mode = False
            while not self.interactive_mode:
                self.interactive_mode = True
                value, final_state, self.fork_decisions = self.simulate(
                  s0, s1, self.interactive_state
                )
                self.replay_mode = True
            self.interactive_mode = False
        else:
            value, final_state, unused_forks = self.simulate(s0, s1)
        report = final_state.reports

        ss0 = [m[0] for m in self.fighter[0].mix]
        ss1 = [m[0] for m in self.fighter[1].mix]

        # Solve cancels
        if value in self.CANCEL_INDICATORS:
            # Both players can only cancel into (non special action)
            # strategies with the same ante and no components of original
            # strategy (this last restriction will only affect
            # any player who didn't cancel).
            post_cancel_strats0 = [
              s
              for s in ss0
              if s[2] == s0[2]
              and s[0] != s0[0]
              and s[1] != s0[1]
              and not isinstance(s[0], fighters.SpecialAction)
            ]
            post_cancel_strats1 = [
              s
              for s in ss1
              if s[2] == s1[2]
              and s[0] != s1[0]
              and s[1] != s1[1]
              and not isinstance(s[0], fighters.SpecialAction)
            ]
            # Before re-simulating, we need to update the game state
            # (record the lost special action/s and any discarded
            # attack pairs).
            self.initial_restore(self.initial_state)
            # Anyone who used a special action (for cancel or finisher)
            # loses the action:
            if isinstance(s0[0], fighters.SpecialAction):
                self.fighter[0].special_action_available = False
            if isinstance(s1[0], fighters.SpecialAction):
                self.fighter[1].special_action_available = False
            # In a double cancel, both players put special action
            # in discard.
            if value == self.CANCEL_BOTH_INDICATOR:
                for f in self.fighter:
                    f.discard[1].add(f.special_action)
            # In a single cancel, opponent puts pair in discard.
            else:
                s01 = (s0, s1)
                opponent = self.player[0] if self.CANCEL_1_INDICATOR else self.player[1]
                opp_strat = s01[opponent.get_player_number()]
                # Discard style, which may be special action.
                opponent.get_fighter().discard[1].add(opp_strat[0])
                # Discard base.  If using a finisher, decide which
                # base it was.
                if isinstance(opp_strat[0], fighters.SpecialAction):
                    self.dump(report)
                    base = opponent.choose_finisher_base_retroactively()
                else:
                    base = opp_strat[1]
                opponent.get_fighter().discard[1].add(base)

            self.initial_state = self.initial_save()
            # Re-simulate available strategies with updated situation.
            post_cancel_results = [
              [float(self.simulate(t0, t1)[0]) for t1 in post_cancel_strats1]
              for t0 in post_cancel_strats0
            ]
            # solve new table
            array_results = numpy.array(post_cancel_results)
            (mix0, value0) = solve.solve_game_matrix(array_results)
            (mix1, value1) = solve.solve_game_matrix(-array_results.transpose())
            stratmix0 = list(zip(post_cancel_strats0, list(mix0)))
            stratmix1 = list(zip(post_cancel_strats1, list(mix1)))
            assert abs(value0 + value1) < 0.01, "Error: value0=%f, value1=%f" % (
              value0,
              value1,
            )
            value = value0
            self.fighter[0].mix = stratmix0
            self.fighter[1].mix = stratmix1
            # Both players choose new strategies
            if self.interactive:
                self.dump(report)
                if self.cheating > 0:
                    self.dump(self.report_solution())
            else:
                report.extend(self.report_solution())
            s0 = self.player[0].choose_strategy(limit_antes=True)
            if self.interactive and self.cheating == 2:
                print(self.player[0], "plays", self.player[0].get_strategy_name(s0))
            s1 = self.player[1].choose_strategy(limit_antes=True)

            # Simulate beat based on new solutions
            if self.interactive:
                self.interactive_state = None
                self.replay_mode = False
                while not self.interactive_mode:
                    self.interactive_mode = True
                    value, final_state, self.fork_decisions = self.simulate(
                      s0, s1, self.interactive_state
                    )
                    self.replay_mode = True
                self.interactive_mode = False
            else:
                value, final_state, unused_forks = self.simulate(s0, s1)
            report.extend(final_state.reports)

        # if we have a real result (possibly after the cancel/s)
        # return it
        if value != self.CLASH_INDICATOR:
            return final_state, report

        # clash - find strategies that can be switched into
        # (same style and ante, different base)
        g0 = [
          ii
          for ii in range(len(ss0))
          if ss0[ii][0] == s0[0] and ss0[ii][2] == s0[2] and ss0[ii][1] != s0[1]
        ]
        g1 = [
          jj
          for jj in range(len(ss1))
          if ss1[jj][0] == s1[0] and ss1[jj][2] == s1[2] and ss1[jj][1] != s1[1]
        ]
        # if one player ran out of bases in clash, just cycle
        # (not sure if end-of-beat UAs should happen,
        # but some of them (Voco) require Forks, so I can't
        # have them outside of simulate(), anyway)
        if min(len(g0), len(g1)) == 0:
            for f in self.fighter:
                f.cycle()
            state = self.full_save(None)
            report.append("\nout of bases - cycling")
            return state, report
        # make sub matrix of remaining results
        i = ss0.index(s0)
        j = ss1.index(s1)
        f0 = self.fighter[0]
        f1 = self.fighter[1]
        self.results = [
          [
            self.pre_clash_results[f0.clash_strat_index(ii, jj, i, j)][
                f1.clash_strat_index(jj, ii, j, i)
            ]
            for jj in g1
          ]
          for ii in g0
        ]
        self.pre_clash_results = [row[:] for row in self.results]
        # make vectors of remaining strategies
        self.strats[0] = self.fighter[0].fix_strategies_post_clash([ss0[i] for i in g0], s1)
        self.strats[1] = self.fighter[1].fix_strategies_post_clash([ss1[j] for j in g1], s0)
        # solve clash
        value, self.fighter[0].mix, self.fighter[1].mix = self.solve_per_pad(
            self.results, self.pre_clash_results, self.strats[0], self.strats[1]
        )
        # Run this function recursively with post-clash strategies only.
        if self.interactive:
            self.dump(report)
        recursive_state, recursive_report = self.execute_beat(post_clash=True)
        report.extend(recursive_report)
        return recursive_state, report

    # fix clash results
    def fix_clashes(self, results, pre_clash_results, ss0, ss1):
        if self.clash0:
            return
        n = len(results)
        m = len(results[0])
        # if at least one matrix dimension is 1, clashes are final,
        # and approximated with 0
        final_clashes = min(n, m) == 1
        # when each clash is resolved, other clashes should still be unresolved
        for i in range(n):
            for j in range(m):
                if pre_clash_results[i][j] == self.CLASH_INDICATOR:
                    if final_clashes:
                        # Cutting a corner here:
                        # In fact, when someone runs out of bases, cycling
                        # happens, which might be better for one player.
                        results[i][j] = 0
                    else:
                        # find indices of strategies that share
                        # style and ante decisions with clash
                        # (but not base, i.e, not exact same strategy)
                        g0 = [
                          ii
                          for ii in range(n)
                          if ss0[ii][0] == ss0[i][0]
                          and ss0[ii][2] == ss0[i][2]
                          and ss0[ii][1] != ss0[i][1]
                        ]
                        g1 = [
                          jj
                          for jj in range(m)
                          if ss1[jj][0] == ss1[j][0]
                          and ss1[jj][2] == ss1[j][2]
                          and ss1[jj][1] != ss1[j][1]
                        ]
                        # make sub matrix of those results
                        p0 = self.fighter[0]
                        p1 = self.fighter[1]
                        try:
                            subresults = [
                              [
                                pre_clash_results[p0.clash_strat_index(ii, jj, i, j)][
                                  p1.clash_strat_index(jj, ii, j, i)
                                ]
                                for jj in g1
                              ]
                              for ii in g0
                            ]
                        except Exception as e:
                            print("Failure")
                            print("n m i j")
                            print(n, m, i, j)
                            print(ss0[i])
                            print(ss1[j])
                            print(g0)
                            print(g1)
                            print("p0 clash indices")
                            for ii in g0:
                                for jj in g1:
                                    print(p0.clash_strat_index(ii, jj, i, j), end=" ")
                                print()
                            print("p1 clash indices")
                            for ii in g0:
                                for jj in g1:
                                    print(p1.clash_strat_index(jj, ii, j, i), end=" ")
                                print()
                            raise e
                        # and solve it
                        results[i][j] = self.sub_solve(subresults)

    # Fix cancel results in matrix.
    # Until a better solution is found, just cause AI to ignore the
    # possibility: it doesn't play cancel, or play around cancel.
    def fix_cancels(self, results):
        n = len(results)
        m = len(results[0])
        for i in range(n):
            for j in range(m):
                if results[i][j] in self.CANCEL_INDICATORS:
                    if results[i][j] == self.CANCEL_0_INDICATOR:
                        results[i][j] = -self.EXTREME_RESULT
                    elif results[i][j] == self.CANCEL_1_INDICATOR:
                        results[i][j] = self.EXTREME_RESULT
                    else:
                        results[i][j] = 0

    # solves 4x4 (or smaller) matrix created by clash
    def sub_solve(self, matrix):
        n = len(matrix)
        m = len(matrix[0])
        # trivial matrix: one dimensional
        if min(n, m) == 1:
            # a final clash ends the beat, approximate as 0:
            for i in range(n):
                for j in range(m):
                    if matrix[i][j] == self.CLASH_INDICATOR:
                        matrix[i][j] = 0
            # solve matrix trivially
            if n == 1:
                return min(matrix[0])
            else:  # m=1
                return max([row[0] for row in matrix])
        # non-trivial matrix
        # fix clashes
        for i in range(n):
            for j in range(m):
                if matrix[i][j] == self.CLASH_INDICATOR:
                    sub_matrix = [
                      [matrix[ii][jj] for jj in range(m) if jj != j] for ii in range(n) if ii != i
                    ]
                    matrix[i][j] = self.sub_solve(sub_matrix)
        (unused_sol, val) = solve.solve_game_matrix(numpy.array(matrix))
        return val

    # return report of positive strategies
    def report_solution(self):
        report = []
        for p in self.player:
            report.append(p.get_name() + ":")
            for m in p.get_fighter().mix:
                if m[1] > 0.0001:
                    report.append(str(int(100 * m[1] + 0.5)) + "% " + p.get_strategy_name(m[0]))
            report.append("")
        return report

    # print solution with positive strategies,
    # plus any strategies called by name in extra
    # if extra contains a character name, show all for that character
    # transpose if it's p1
    def print_solution(self, extra=[]):
        if isinstance(extra, str):
            extra = [extra]
        extra = [e.lower() for e in extra]
        for i, pad0 in enumerate(self.pads[0]):
            for j, pad1 in enumerate(self.pads[1]):
                if len(self.pads[0]) > 1:
                    print("Pre attack decision: %s" % pad0)
                if len(self.pads[1]) > 1:
                    print("Pre attack decision: %s" % pad1)
                # for each player
                for p in self.player:
                    f = p.get_fighter()
                    # keep only positive probs
                    if p.get_name().lower() in extra:
                        f.filtered_indices = list(range(len(f.mix[i][j])))
                    else:
                        f.filtered_indices = [
                          k
                          for k in range(len(f.mix[i][j]))
                          if f.mix[i][j][k][1] > 0.0001
                          or f.get_strategy_name(f.mix[i][j][k][0]).lower() in extra
                        ]
                    f.filtered_mix = [f.mix[i][j][k] for k in f.filtered_indices]
                    r = random.random()
                    total = 0
                    print("\n", p)
                    for m in f.filtered_mix:
                        print(str(int(100 * m[1] + 0.5)) + "%", f.get_strategy_name(m[0]), end=" ")
                        if total + m[1] >= r and total < r:
                            print(" ***", end=" ")
                        print(" ")
                        total = total + m[1]
                print("\n" + self.player[0].get_name() + "'s Value:", self.value[i][j], "\n")
                small_mat = numpy.array(
                  [
                    [self.results[i][j][k][m] for m in self.player[1].get_fighter().filtered_indices]
                    for k in self.player[0].get_fighter().filtered_indices
                  ]
                )
                # if all player 1 strategies displayed, transpose for ease of reading
                if (
                  self.player[1].get_name().lower() in extra
                  and self.player[0].get_name().lower() not in extra
                ):
                    small_mat = small_mat.transpose()
                    print("(transposing matrix)")
                print(small_mat.round(2))

    # game value if one player uses given strategy, and other player uses
    # calculated mix
    # Assumes no pre-attack decisions (so no Tanis)
    def vs_mix(self, name):
        name = name.lower()
        mix0 = self.fighter[0].mix[0][0]
        mix1 = self.fighter[1].mix[0][0]
        ii = [
          i
          for i in range(len(mix0))
          if self.fighter[0].get_strategy_name(mix0[i][0]).lower() == name
        ]
        jj = [
          j
          for j in range(len(mix1))
          if self.fighter[1].get_strategy_name(mix1[j][0]).lower() == name
        ]
        for i in ii:
            value = 0
            for j in range(len(mix1)):
                value += self.results[0][0][i][j] * mix1[j][1]
            print(value)
        for j in jj:
            value = 0
            for i in range(len(mix0)):
                value += self.results[0][0][i][j] * mix0[i][1]
            print(value)

    # for each strategy (of each player), print worst possible case
    def worst_case(self):
        array_results = numpy.array(self.results)
        n, m = array_results.shape
        worst = array_results.argmin(1)
        for i in range(n):
            print(array_results[i, worst[i]], ":", end=" ")
            print(self.fighter[0].get_strategy_name(self.fighter[0].strats[i]), "--->", end=" ")
            print(self.fighter[1].get_strategy_name(self.fighter[1].strats[worst[i]]))
        print("##################################################")
        worst = array_results.argmax(0)
        for j in range(m):
            print(array_results[worst[j], j], ":", end=" ")
            print(self.fighter[1].get_strategy_name(self.fighter[1].strats[j]), "--->", end=" ")
            print(self.fighter[0].get_strategy_name(self.fighter[0].strats[worst[j]]))

    # run one simulation by strategy names
    # and print reports
    def debug(self, name0, name1, full_debug=True):
        name0 = name0.lower()
        name1 = name1.lower()
        self.debugging = full_debug
        self.reporting = True
        self.initial_restore(self.initial_state)
        for p in self.player:
            p.set_preferred_range()
        print(
          (
            "preferred ranges: %.2f - %.2f    [%d]"
            % (
              self.fighter[0].preferred_range,
              self.fighter[1].preferred_range,
              self.distance(),
            )
          )
        )
        print(
          (
            "range_evaluation: %.2f - %.2f = %.2f"
            % (
              self.player[0].evaluate_range(),
              self.player[1].evaluate_range(),
              self.player[0].evaluate_range() - self.player[1].evaluate_range(),
            )
          )
        )
        s0 = [
          s
          for s in self.fighter[0].strats
          if self.fighter[0].get_strategy_name(s).lower() == name0
        ]
        s1 = [
          s
          for s in self.fighter[1].strats
          if self.fighter[1].get_strategy_name(s).lower() == name1
        ]
        unused_value, state, forks = self.simulate(s0[0], s1[0])
        self.debugging = False
        self.reporting = False
        for s in state.reports:
            print(s)
        return state, forks

    # add a string to reports
    def report(self, s):
        if self.interactive_mode:
            if not self.replay_mode:
                print(s)
                self.log.append(s)
        else:
            self.reports.append(s)

    # re-solve matrix assuming that one player antes first
    def first_ante(self, first):
        ss0 = self.fighter[0].strats
        ss1 = self.fighter[1].strats
        array_results = numpy.array(self.results)
        # assumes first anteer is player 0
        # if not, reverse everything now, then put it back at the end
        if first == 1:
            array_results = -array_results.transpose()
            ss0, ss1 = ss1, ss0

        ab0, ab1 = array_results.shape
        b0 = len(set(s[2] for s in ss0))
        b1 = len(set(s[2] for s in ss1))
        if ab0 % b0 != 0 or ab1 % b1 != 0:
            print("Total strategies not divisible by antes")
            return
        a0 = ab0 / b0
        a1 = ab1 / b1
        (mix0, value0) = solve.solve_for_player0_with_b0_known(
          array_results, a0, b0, a1, b1
        )
        (mix1, value1) = solve.solve_for_player0_with_b1_known(
          -array_results.transpose(), a1, b1, a0, b0
        )
        # mix1 (2nd ante) has full pair/ante mix for each ante of player 0
        # followed by pre-ante pair mix
        # for each pair 1 x ante 0: print ante 1 mix
        for a1i in range(a1):
            pair_prob = mix1[b0 * a1 * b1 + a1i]
            if pair_prob > 0.0001:
                for b0i in range(b0):
                    print(self.fighter[1 - first].get_strategy_name(ss1[a1i * b1]), end=" ")
                    print("vs.", end=" ")
                    opposing_ante = self.fighter[first].get_ante_name(ss0[b0i][2])
                    print(("No Ante" if opposing_ante == "" else opposing_ante))
                    for b1i in range(b1):
                        prob = mix1[b0i * a1 * b1 + a1i * b1 + b1i]
                        if prob > 0.0001:
                            print("   ", str(int(100 * prob / pair_prob + 0.5)) + "%", end=" ")
                            my_ante = self.fighter[1 - first].get_ante_name(ss1[b1i][2])
                            print(("No Ante" if my_ante == "" else my_ante))
        print()

        spread = [0.0 for i in range(ab1)]
        for i in range(a1):
            spread[i * b1] = mix1[b0 * a1 * b1 + i]
        mix1 = spread

        # if results were transposed, put them back,
        if first == 1:
            array_results = -array_results.transpose()
            ss0, ss1 = ss1, ss0
            mix0, mix1 = mix1, mix0
            value0, value1 = value1, value0

        stratmix0 = list(zip(ss0, mix0))
        stratmix1 = list(zip(ss1, mix1))
        if abs(value0 + value1) > 0.01:
            print("ERROR:")
            print("  value0:", value0)
            print("  value1:", value1)
            raise Exception()
        self.value = value0
        self.fighter[0].mix = stratmix0
        self.fighter[1].mix = stratmix1

        self.print_solution()

    def prepare_next_beat(self):
        if not self.stop_the_clock:
            self.current_beat += 1
        for f in self.fighter:
            f.prepare_next_beat()


class GameState(object):
    pass


# raised on bugs to return game object
class DebugException(Exception):
    def __init__(self, game):
        self.game = game
