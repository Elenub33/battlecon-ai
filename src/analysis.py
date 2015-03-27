#!/usr/bin/python

from collections import Counter, defaultdict
from numpy import array
from operator import itemgetter
import csv
import math
import os
import pylab
import re

phrases = {  #'abarene' : ['Hallicris Snare'],
             'adjenna' : ['Basilisk Gaze'],
             'alexian' : ['Empire Divider', 'Hail the King'],
             'alumis' : ['Aphotic Terror', 'Umbral Vice'],
             'arec': ['Uncanny Oblivion'],
             'aria' : ['Laser Lattice'],
             'baenvier' : [],
             #'borneo': ['Master Plan', 'Scene Shift', 'Mama Mazzaroth'],
             'byron' : ['Soul Trap', 'Soul Gate'],
             'cadenza' : ['Rocket Press', 'Feedback Field'],
             'cesar' : ['Level 4 Protocol'],
             'claus' : ["Autumn's Advance"],
             'clinhyde' : ['Vital Silver Infusion', 'Ritherwhyte Infusion'],
             'danny': ['The Dark Ride'],
             'demitras' : ['Symphony of Demise'],
             'eligor' : ['Sweet Revenge', 'Sheet Lightning'],
             'eustace' : ['Bone Breaker', 'Rime Blitzer'],
             #'gerard' : ['Ultra Beatdown'],
             'heketch' : ['Million Knives', 'Living Nightmare'],
             'hikaru' : ['Wrath of Elements', 'Four Winds', 'Palm Strike'],
             'jager' : ['Blood Moon', 'Blood Hunt', 'Sign of the Wolf'],
             'iri' : ['Limit Exceed', 'Final Galaxy Sword Atamos'],
             #'juto' : ['Ban Hammer'],
             'kajia' : ['Imago Emergence'],
             'kallistar' : ['Chain of Destruction'],
             'karin' : ['Red Moon Rage', 'Lunar Cross', 'Full Moon'],
             'kehrolyn' : ['Hydra Fork'],
             'khadath' : ['Dimensional Exile'],
             'larimore' : ['The Jump'],
             'lesandra' : ['Invoke Duststalker'],
             'lixis' : ['Virulent Miasma'],
             'luc' : ['Temporal Recursion'],
             'lymn' : [],
             'magdelina' : ['Solar Soul'],
             'marmelee' : ['Astral Cannon', 'Astral Trance'],
             'mikhail' : ['Magnus Malleus', 'The Fourth Seal'],
             #'oriana' : ['Nihil Eraser', 'Galaxy Conduit'],
             'ottavia' : ['Extreme Prejudice'],
             'rexan' : ['Zero Hour'],
             'rukyuk' : ['Point Blank', 'Fully Automatic', 'Force Grenade'],
             'runika' : ['Artifice Avarice', 'Udstad Beam'],
             'sarafina' : ['Ritherwhyte Infusion', 'Fulminating Vortex'],
             'seth' : ['Fortune Buster'],
             'shekhtur' : ['Coffin Nails'],
             'tanis' : ['Scene Shift', 'Curtain Call'],
             'tatsumi' : ['Tsunamis Collide', 'Bear Arms', 'Guardian Xandjinn'],
             'vanaah' : ['Death Walks', 'Hand of Divinity'],
             'voco' : ['The Wave'],
             'xenitia' : ['Awakening Blood'],
             'zaamassal' : ['Paradigm Shift', 'Open the Gate', 'Plane Divider']}

devastation_flights = [['alexian', 'eligor', 'karin', 'marmelee', 'shekhtur'],
                       ['cesar', 'kajia', 'mikhail', 'ottavia', 'rexan', 'runika'],
                       ['aria', 'byron', 'clinhyde', 'lesandra', 'lymn', 'oriana'],
                       ['adjenna', 'arec', 'gerard', 'voco'],
                       ['tanis']]
devastation = sum(devastation_flights, [])
war_flights = [['cadenza', 'hikaru', 'kallistar', 'luc', 'magdelina', 'vanaah'],
               ['demitras', 'heketch', 'kehrolhyn', 'rukyuk', 'zaamassal'],
               ['khadath', 'lixis', 'seth', 'tatsumi']]
war = sum(war_flights, [])
all_names = sorted(phrases.keys())

def list_files (logdir, name=None, player_num=None):
    fulldir = 'logs/' + logdir + '/'
    filenames = [fn for fn in os.listdir(fulldir) 
                 if os.path.isfile(fulldir+fn)]
    if name is None:
        return [fulldir+fn for fn in filenames]
    if player_num is None:
        return [fulldir+fn for fn in filenames if name in fn]
    return [fulldir+fn for fn in filenames 
            if name == fn.split('_')[player_num]]
    
def all_victories(logdir='core_tests', devastation_only=False):
    names = devastation if devastation_only else all_names
    name_power = []
    for name in names:
        vics = victories(name, logdir, silent=True)
        if vics is not None:
            name_power.append((name, vics))
    name_power = sorted(name_power, key=itemgetter(1))
    for np in name_power:
        print "%s: %s" %(np[0], percentify(np[1]))

def victories (name, logdir="core_tests", return_timeouts=False, silent=False,
               per_name=False):
    (win,lose,draw,time_win,time_lose) = (0,0,0,0,0)
    next_result_is_timeout = False
    for filename in list_files(logdir, name):
        (_win,_lose,_draw) = (0,0,0)
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if line.endswith ('WINS!\n'):
                if line.find(name.upper()) > -1:
                    _win += 1
                    if next_result_is_timeout:
                        time_win += 1
                else:
                    _lose += 1
                    if next_result_is_timeout:
                        time_lose += 1
                next_result_is_timeout = False
            if line.endswith ('TIED!\n'):
                _draw += 1
                next_result_is_timeout = False
            if line.endswith ('Game goes to time\n'):
                next_result_is_timeout = True
        if per_name:
            names = filename.split('/')[-1].split('_')
            other_name = names[0] if names[0] != name else names[1]
            print other_name, _win + _draw/2.0
        win += _win
        lose += _lose
        draw += _draw

    games = float(win+lose+draw)
    if games == 0:
        return None
    if not silent:
        print "power:", percentify ((win+draw/2.0)/games)
        print "win: %d (%s) - %s by time out" %(win, percentify(win/games),
                                                percentify(time_win/float(win)))
        print "lose: %d (%s) - %s by time out" %(lose, percentify(lose/games),
                                                 percentify(time_lose/float(lose)))
        print "draw: %d (%s)" %(draw, percentify(draw/games))
        print "total: %s by timeout" %percentify((time_win+time_lose+draw)/games)

    if return_timeouts:
        return (time_win+time_lose+draw)/games
    else:
        return (win+draw/2.0)/games

def side_victories (logdir="core_tests"):
    (win,lose,draw,time_win,time_lose) = (0,0,0,0,0)
    next_result_is_timeout = False
    for filename in list_files(logdir, None):
        names = filename.split('/')[-1].split('_')
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if line.endswith ('WINS!\n'):
                if line.find(names[0].upper()) > -1:
                    win += 1
                    if next_result_is_timeout:
                        time_win += 1
                else:
                    lose += 1
                    if next_result_is_timeout:
                        time_lose += 1
                next_result_is_timeout = False
            if line.endswith ('TIED!\n'):
                draw += 1
                next_result_is_timeout = False
            if line.endswith ('Game goes to time\n'):
                next_result_is_timeout = True

    games = float(win+lose+draw)
    print "alpha power:", percentify ((win+draw/2.0)/games)
    print "alpha wins: %d (%s) - %s by time out" %(win, percentify(win/games),
                                            percentify(time_win/float(win)))
    print "beta wins: %d (%s) - %s by time out" %(lose, percentify(lose/games),
                                             percentify(time_lose/float(lose)))
    print "draw: %d (%s)" %(draw, percentify(draw/games))
    print "total: %s by timeout" %percentify((time_win+time_lose)/games)

def victory_csv (logdir="core_tests"):
    index = {name:i for (i,name) in enumerate(all_names)}
    wins = [[0 for i in all_names] for j in all_names]
    logdir = "logs/" + logdir + "/"
    filenames = os.listdir (logdir)
    for filename in filenames:
        split = filename.split('_')
        i = index [split[0]]
        j = index [split[1]]
        with open (logdir+filename) as f:
            log = [line for line in f]
        for line in log:
            if line.endswith ('WINS\n'):
                if line.find(split[0].upper()) > -1:
                    wins[i][j] += 1
                else:
                    wins[j][i] += 1
            if line.endswith ('TIED!\n'):
                wins[i][j] += 0.5
                wins[j][i] += 0.5
    for i in xrange(len(wins)):
        for j in xrange(i):
            if wins[i][j]+wins[j][i] != 10:
                print all_names[i], all_names[j], wins[i][j], wins[j][i]
    # sort names by total wins
    sums = [sum(row) for row in wins]
    names_sums = sorted (zip (all_names, sums), key=itemgetter(1),
                         reverse=True)
    names = [ns[0].capitalize() for ns in names_sums]
    # sort rows by total wins
    wins = sorted(wins, key=lambda x: sum(x), reverse=True)
    # sort columns by total wins
    wins = zip(*wins)
    wins = sorted(wins, key=lambda x: sum(x))
    wins = zip(*wins)
    for i in xrange(len(wins)):
        wins[i] = list(wins[i])
        wins[i][i]=''
    csv.register_dialect('my_excel', delimiter=',', lineterminator='\n')
    with open ('victories.csv','w') as csvfile:
        writer = csv.writer (csvfile,dialect='my_excel')
        writer.writerow(['']+names)
        for (i,name) in enumerate(names):
            writer.writerow([name]+wins[i])

def check_redundancies():
    for name0 in all_names:
        for name1 in all_names:
            if name0 < name1:
                file01 = 'logs/main/'+name0+'_'+name1+'_log.txt'
                file10 = 'logs/main/'+name1+'_'+name0+'_log.txt'
                exist01 = os.path.isfile (file01)
                exist10 = os.path.isfile (file10)
                if exist01 and exist10:
                    print name0, name1
                if not exist01 and not exist10:
                    print "missing:", name0, name1

def analyze (name, logdir="core_tests"):
    victories (name,logdir)
    print "Average game length: %.1f"% game_length(name, logdir)
    strategies(name, logdir)
    hitting (name, logdir)

class BeatData(object):
    """ Holds the following data:
    player: name of analyzed player
    opponent: name of opponent
    player_num: number of analyzed player (0 or 1)
    number: beat number
    style: the style chosen by analyzed player
    base: the base chosen by analyzed player
    final_base: the final base played (after clashes)
    ante: the ante chosen by analyzed player (without induced ante)
    induced_ante: the induced ante chosen by analyzed player
    opp_style: the style chosen by opponent
    opp_base: the base chosen by opponent
    opp_induced_ante: the induced ante chosen by opponent
    text: list of text lines for the beat.
    """
    def __init__(self, name, opp_name, player_num, lines, replacement):
        self.player = name
        self.opponent = opp_name
        self.player_num = player_num
        self.number = int(lines[0].split(' ')[1])
        self.lines = lines
        styles = [None, None]
        bases = [None, None]
        final_bases = [None, None]
        antes = [None, None]
        induced_antes = [None, None]
        line_starts = ["%s: " % n.capitalize()
                       for n in (name, opp_name)]
        for i in (0,1):
            my_lines = [line for line in lines
                        if line.startswith(line_starts[i])]
            styles[i], bases[i], antes[i], induced_antes[i] = \
                self.parse_line(my_lines[0], replacement)
            if len(my_lines) == 1:
                final_bases[i] = bases[i]
            else:
                final_bases[i] = self.parse_line(my_lines[-1], 
                                                 replacement) [1]

        self.style, self.opp_style = tuple(styles)
        self.base, self.opp_base = tuple(bases)
        self.final_base, self.opp_final_base = tuple(final_bases)
        self.ante, self.opp_ante = tuple(antes)
        self.induced_ante, self.opp_induced_ante = tuple(induced_antes)
            
    def parse_line(self, line, replacement):
        line = line[:-1] # snip new line
        induced_split = line.split(' | ')
        if len(induced_split) > 1:
            induced_ante = induced_split[1]
        else:
            induced_ante = None
        line = induced_split[0]
        for p in replacement:
            line = line.replace(p, replacement[p])
        split = line.split(' ')
        style = split[1]
        base = split[2]
        ante = ' '.join(split[3:])
        return style, base, ante, induced_ante
    
    def lines_starting_with(self, start):
        return [line for line in self.lines
                if line.startswith(start)]

    def lines_ending_with(self, end):
        end += '\n'
        return [line for line in self.lines
                if line.endswith(end)]

    def lines_containing(self, text):
        return [line for line in self.lines
                if text in line]
                     
def entropy(logdir='core_tests'):
    my_entropy = defaultdict(list)
    opp_entropy = defaultdict(list)
    min_entropy = defaultdict(list)
    dicts = {"SELF ENTROPIES": my_entropy, 
             "OPPONENT ENTROPIES": opp_entropy, 
             "MINIMUM ENTROPIES": min_entropy}
    for filename in list_files(logdir):
        names = filename.split('/')[-1].split('_')[:2]
        with open (filename) as f:
            log = [line for line in f]
        starts = [i for i, line in enumerate(log)
                  if line.startswith("Beat")]
        for start in starts:
            es = [calc_entropy(log, start, name) for name in names]
            my_entropy[names[0]].append(es[0])
            my_entropy[names[1]].append(es[1])
            opp_entropy[names[0]].append(es[1])
            opp_entropy[names[1]].append(es[0])
            min_entropy[names[0]].append(min(es))
            min_entropy[names[1]].append(min(es))
    for title, d in dicts.items():
        print title
        for name in d:
            d[name] = 2 ** sorted(d[name])[len(d[name])/2]
        items = sorted(d.items(), key=itemgetter(1))
        for i in items:
            print "%.1f %s" % (i[1], i[0])
    my_names = [m[0] for m in sorted(my_entropy.items(), key=itemgetter(1))]
    opp_names = [m[0] for m in sorted(opp_entropy.items(), key=itemgetter(1))]
    diffs = []
    for i, m in enumerate(my_names):
        j = opp_names.index(m)
        diffs.append((i-j, m))
    diffs = sorted(diffs)
    print "DIFFS:"
    for d in diffs:
        print d[0], d[1]
    
    mys = sorted(my_entropy.items())
    opps = sorted(opp_entropy.items())
    antes = ['abarene',
             'alexian',
             'arec',
             'cadenza',
             'clinhyde',
             'demitras',
             'eligor',
             'gerard',
             'heketch',
             'hikaru',
             'jager',
             'larimore',
             'lesandra',
             'luc',
             'mikhail',
             'oriana',
             'ottavia',
             'rexan',
             'rukyuk',
             'sarafina',
             'seth',
             'shekhtur',
             'vanaah']
    
    pylab.scatter([x[1] for x in mys if x[0] in antes], 
                  [x[1] for x in opps if x[0] in antes],
                  c='r')
    pylab.scatter([x[1] for x in mys if x[0] not in antes], 
                  [x[1] for x in opps if x[0] not in antes],
                  c='b')
    pylab.grid()
    pylab.show()
       
def calc_entropy(log, start, name):
    i = start
    line = "%s:\n" % name.capitalize()
    while log[i] != line:
        i += 1
    i += 1
    probs = []
    while log[i] != '\n':
        probs.append(float(log[i].split()[0][:-1])/100)
        i += 1
    s = sum(probs)
    probs = [p/s for p in probs if p > 0]
    return -sum(p * math.log(p, 2) for p in probs)
        
                     
def parse_beats(name, logdir='core_tests'):
    replacement = {phrase : phrase.replace(' ','') 
                   for char_name in phrases
                   for phrase in phrases[char_name]}
    beats = [] 
    for filename in list_files(logdir, name):
        names = filename.split('/')[-1].split('_')
        number = 0 if names[0] == name else 1
        opp_name = names[1-number]
        with open (filename) as f:
            log = [line for line in f]
        starts = [i for i, line in enumerate(log)
                  if line.startswith("Beat")]
        starts.append(len(log))
        file_beats = [BeatData(name, opp_name, number, 
                               log[starts[i]:starts[i+1]], replacement)
                               for i in xrange(len(starts) - 1)]
        beats += file_beats
    return beats

def check_victories(beats):
    # For each beat, indicate who won the game.
    # Only works if list includes all beats of each game, in order.
    # Also assumes all beats are of same player.
    upper = beats[0].name.upper()
    for i in xrange(len(beats) - 1, -1 ,-1):
        beat = beats[i]
        if i == len(beats) - 1 or beat.number > beats[i+1].number:
            beat.final = True
            # last beat of game
            lines = beat.lines_ending_with('WINS!')
            if lines:
                if lines[0].startswith(upper):
                    beat.game_points = 1
                else:
                    beat.game_points = 0
            else:
                beat.game_points = 0.5
        else:
            beat.final = False
            beat.game_points = beats[i+1].game_points

def strategies (name, logdir="core_tests", beat=None,
                condition='',reverse_condition=False):
    beats = parse_beats(name, logdir)
    if beat is not None:
        beats = [b for b in beats if b.number == beat]
    if condition:
        beats = [b for b in beats 
                 if bool(b.lines_starting_with(condition)) != reverse_condition]
    if name == 'adjenna':
        post_processing_adjenna(beats)
    if name == 'arec':
        post_processing_arec(beats)
    if name == 'byron':
        post_processing_byron(beats)
    if name == 'cesar':
        post_processing_cesar(beats)
    if name == 'jager':
        post_processing_jager(beats)
    if name == 'kallistar':
        post_processing_kallistar(beats)
    if name == 'lymn':
        post_processing_lymn(beats)
    if name == 'magdelina':
        post_processing_magdelina(beats)
    if name == 'seth':
        post_processing_seth(beats)
    if name == 'tanis':
        post_processing_tanis(beats)
    strategy_dict = Counter([(b.style, b.base, b.ante) for b in beats])
    count, styles, bases = pair_count (strategy_dict, True) 
    total = count.sum()
    print "total beats:", total
    print '--------------'
    style_count = count.sum(axis=1)
    dash_index = bases.index('Dash')
    no_dash_style_count = style_count - count[:,dash_index]
    no_dash_total = float(no_dash_style_count.sum())
    sc = [(styles[i],style_count[i], no_dash_style_count[i]) for i in range(len(styles))]
    sc = sorted (sc, key=itemgetter(1), reverse=True)
    for s in sc:
        print "%s %s (%s)" % (percentify(s[2]/no_dash_total), s[0],
                              percentify(s[1]/float(total)))
    print '--------------'
    base_count = count.sum(axis=0)
    bc = [(bases[i],base_count[i]) for i in range(len(bases))]
    bc = sorted (bc, key=itemgetter(1), reverse=True)
    for b in bc:
        print percentify(b[1]/float(total)), b[0]
    print '--------------'
    count, styles, antes = style_ante_count (strategy_dict, True)
    if len (antes) > 1:
        ante_count = count.sum(axis=0)
        ac = [(antes[i],ante_count[i]) for i in range(len(antes))]
        ac = sorted (ac, key=itemgetter(1), reverse=True)
        for a in ac:
            print percentify(a[1]/float(total)), a[0]
        print '--------------'
    for func in [pair_count, base_ante_count, style_ante_count]:
        count, first, second = func (strategy_dict, False)
        if len (second) > 1:
            first_count = count.sum(axis=1)
            second_count = count.sum(axis=0)
            total = count.sum()
            for x in range(len(first)):
                for y in range(len(second)):
                    cxy = count[x][y]
                    print first[x], second[y], \
                          percentify(cxy/float(first_count[x])), \
                          percentify(cxy/float(second_count[y])),
                    ratio = float(cxy * total) / (first_count[x]*second_count[y])
                    if ratio > 1.5:
                        print "STRONG - %.2f" %ratio
                    elif ratio < 0.5:
                        print "WEAK - %.2f" %ratio
                    else:
                        print                                     
            print '-----------'

class HitRecord (object):
    def __init__(self, name):
        self.name = name
        self.beats = 0
        self.hits = 0
        self.misses = 0
        self.stunned = 0
        self.damage = 0
        self.opp_hits = 0
        self.opp_misses = 0
        self.opp_stunned = 0
        self.opp_damage = 0
    def __str__(self):
        return "%s b%d h%d m%d s%d d%d oh%d om%d os%d od%d" %(
            self.name, self.beats, self.hits, self.misses, self.stunned, self.damage, 
            self.opp_hits, self.opp_misses, self.opp_stunned, self.opp_damage)

def hitting (name, logdir="core_tests", printing=True):
    style_record = {}
    base_record = {}
    cap_name = name.capitalize()
    beats = parse_beats(name, logdir)
    for beat in beats:
        style = beat.style
        base = beat.final_base
        if style == 'Special' or beat.opp_base == 'Pulse':
            continue
        active_lines = beat.lines_ending_with(" is active")
        if not active_lines:
            continue
        me_active = active_lines[0].startswith(cap_name)
        stun_lines = beat.lines_ending_with(" is stunned")
        my_stuns = [line.startswith(cap_name) for line in stun_lines]
        me_stunned = any(my_stuns)
        opp_stunned = not all(my_stuns)
        miss_lines = beat.lines_ending_with(" misses")
        my_misses = [line.startswith(cap_name) for line in miss_lines]
        me_missed = any(my_misses)
        opp_missed = not all(my_misses)
        hit_lines = beat.lines_ending_with(" hits")
        my_hits = [line.startswith(cap_name) for line in hit_lines]
        me_hit = any(my_hits)
        opp_hit = not all(my_hits)
        damage_lines = beat.lines_containing(" damage (now at ")
        my_damage = 0
        opp_damage = 0
        for line in damage_lines:
            if line.startswith(cap_name):
                opp_damage += int(line.split(' ')[2])
            else:
                my_damage += int(line.split(' ')[2])
        for key, record in ((style, style_record),
                            (base, base_record)):
            if key not in record.keys():
                record[key] = HitRecord(key)
            record[key].beats += 1
            if me_active and opp_stunned:
                record[key].opp_stunned += 1
            if not me_active and me_stunned:
                record[key].stunned += 1
            record[key].misses += me_missed
            record[key].opp_misses += opp_missed
            record[key].hits += me_hit
            record[key].opp_hits += opp_hit
            record[key].damage += my_damage
            record[key].opp_damage += opp_damage
    for record in style_record, base_record:
        total = HitRecord("All")
        for key in total.__dict__.keys():
            if key != 'name':
                total.__dict__[key] = sum([rec.__dict__[key] 
                                           for rec in record.itervalues()])
        all_recs = record.values() + [total]
        print "stunned/missed/hit/dam per hit/dam per beat"
        for rec in all_recs:
            if rec.name != 'Special' and rec.hits > 0:
                beats = float(rec.beats)
                print "%.2f %s %s %s %s %.1f %.1f | %s %s %s %.1f %.1f" % \
                      (rec.damage/beats/((rec.opp_damage+0.00001)/beats),
                       rec.name + (' ' * (12-len(rec.name))),
                       percentify(rec.stunned/beats),
                       percentify(rec.misses/beats),
                       percentify(rec.hits/beats),
                       rec.damage/float(rec.hits),
                       rec.damage/beats,
                       percentify(rec.opp_stunned/beats),
                       percentify(rec.opp_misses/beats),
                       percentify(rec.opp_hits/beats),
                       rec.opp_damage/float(rec.opp_hits),
                       rec.opp_damage/beats)

class HitWinCorrelationRecord (object):
    def __init__ (self):
        self.win_hits = [0] * 6
        self.tie_hits = [0] * 6
        self.lose_hits = [0] * 6
        
def style_win_correlation (name, logdir="core_tests"):
    replacement = {p : p.replace(' ','') for p in phrases[name]} 
    record = {}
    cap_name = name.capitalize()
    upper_name = name.upper()
    style = None
    style_hits = {}
    for filename in list_files(logdir, name):
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if line.startswith('GAME '):
                style_hits = {}
            if line.startswith('Beat '):
                style = None
            if style is None and line.startswith (name.capitalize()+": "):
                for p in replacement:
                    line = line.replace(p,replacement[p])
                style = line.split(' ')[1]
                if style not in style_hits.iterkeys():
                    style_hits[style] = 0
            if line.endswith(" hits\n") and line.startswith(cap_name):
                style_hits[style] += 1
            win = line.endswith ('WINS\n')
            tie = line.endswith ('TIED!\n')
            if  win or tie:
                styles = style_hits.keys()
                for style in styles:
                    if style not in record.iterkeys():
                        record[style] = HitWinCorrelationRecord()
                if win:
                    if upper_name in line:
                        for style in styles:
                            record[style].win_hits[style_hits[style]] += 1
                    else:
                        for style in styles:
                            record[style].lose_hits[style_hits[style]] += 1
                else:
                    for style in styles:
                        record[style].tie_hits[style_hits[style]] += 1
    for style in record.iterkeys():
        print style
        rec = record[style]
        for hits in range(6):
            win = rec.win_hits[hits]
            lose = rec.lose_hits[hits]
            tie = rec.tie_hits[hits]
            total = float (win+lose+tie)
            if total > 20:
                print "%d: %s / %s (%d)" % (hits,
                                            percentify (win/total),
                                            percentify (lose/total),
                                            total)
##                print "%d: %d / %d (%d)" % (hits,
##                                            win,
##                                            lose,
##                                            tie)

def specials (name=None, logdir="core_tests"):
    names = [name] if name else phrases.keys()
    stats = {'all': [0]*16,
             'pulse': [0]*16,
             'cancel': [0]*16,
             'finisher': [0]*16}
    games=0
    for name in names:
        beats = parse_beats(name, logdir)
        for i, beat in enumerate(beats):
            if beat.number == 1 and beats[i+1].number != 1:
                games += 1
            if beat.style == 'Special':
                stats['all'][beat.number] += 1
                if beat.base == 'Pulse':
                    stats['pulse'][beat.number] += 1
                elif beat.base == 'Cancel':
                    stats['cancel'][beat.number] += 1
                else:
                    stats['finisher'][beat.number] += 1
    for stat in sorted(stats.keys()):
        s = stats[stat]
        total = 0
        print stat.upper(), percentify(sum(s)/float(games)) 
        for beat in range(1,16):
            total += s[beat]
            print "%d: %s - %s" %(beat, percentify(s[beat]/float(games)),
                                  percentify(total/float(games)))
        
def anomalies(logdir='core_tests'):
    for name in all_names:
        strategy_dict = Counter([(b.style, b.base, b.ante) 
                                 for b in parse_beats(name, logdir)])
        count, styles, bases = pair_count (strategy_dict, False) 
        style_count = count.sum(axis=1)
        base_count = count.sum(axis=0)
        total = float(count.sum())
        print '----------'
        print name.capitalize()
        print '----------'
        for s in range(len(style_count)):
            fraction = style_count[s] / total
            if fraction >= .25 or fraction <= .12:
                print percentify(fraction), styles[s]
        for b in range(len(base_count)):
            fraction = base_count[b] / total
            if fraction >= .25 or fraction <= .08:
                print percentify(fraction), bases[b]
        for s in range(len(style_count)):
            for b in range(len(base_count)):
                sb = count[s][b]
                fraction = sb / float(style_count[s])
                if fraction >= 0.35 or fraction <= 0.035:
                    print "%s attached to %s %d of %d times (%s)" \
                          %(bases[b], styles[s], sb, style_count[s],
                            percentify (sb/float(style_count[s])))
                fraction = sb / float(base_count[b])
                if fraction >= 0.5 or fraction <= 0.05:
                    print "%s attached to %s %d of %d times (%s)" \
                          %(styles[s], bases[b], sb, base_count[b],
                            percentify (sb/float(base_count[b])))
        
def total_bases(specials=True, player_num=None, base_set='alpha', 
                logdir="core_tests"):
    if base_set == 'alpha':
        base_dict = {"Strike" : 0,
                     "Shot" : 0,
                     "Drive" : 0,
                     "Burst" : 0,
                     "Grasp" : 0,
                     "Dash" : 0,
                     "Pulse" : 0,
                     "Cancel" : 0}
    elif base_set == 'beta':
        base_dict = {"Counter" : 0,
                     "Wave" : 0,
                     "Force" : 0,
                     "Spike" : 0,
                     "Throw" : 0,
                     "Parry" : 0,
                     "Pulse" : 0,
                     "Cancel" : 0}
    else:
        base_dict = {"Stagger" : 0,
                     "Leap" : 0,
                     "Lunge" : 0,
                     "Sweep" : 0,
                     "Catch" : 0,
                     "Block" : 0,
                     "Pulse" : 0,
                     "Cancel" : 0}
        
    total_total = 0
    for name in all_names:
        beats = parse_beats(name, logdir)
        if player_num is not None:
            beats = [b for b in beats if b.player_num==player_num]
        strategy_dict = Counter([(b.style, b.base, b.ante) 
                                 for b in beats])
        count, unused_styles, bases = pair_count (strategy_dict, specials)
        base_count = count.sum(axis=0)
        total = (count.sum())
        for b in range(len(bases)):
            if bases[b] in base_dict.keys():
                base_dict[bases[b]] += base_count[b]
        total_total += total
    sub_total = sum ([base_dict[k] for k in base_dict])
    base_dict['Unique'] = total_total - sub_total
    bases_counts = sorted(base_dict.items(), key=itemgetter(1),
                          reverse=True)
    for b in bases_counts:
        print percentify(b[1]/float(total_total)), b[0]

def game_length (name, logdir="core_tests"):
    beats = parse_beats(name, logdir)
    beats = [beats[i] for i in xrange(len(beats))
             if i==0 or beats[i-1].number != beats[i].number]
    games = len([i for i in xrange(len(beats))
                 if beats[i].number == 1])
    return len(beats) / float(games)
    
def all_game_lengths(logdir="core_tests"):
    res = []
    filenames_string = ''.join(list_files(logdir))
    for name in all_names:
        if name in filenames_string:
            res.append ((name, game_length(name, logdir),
                         victories(name,logdir,return_timeouts=True,silent=True)))
    res = sorted(res,key=itemgetter(2))
    print "mean game length: %.1f" %(sum([r[1] for r in res])/len(res))
    print "mean timeout percent: %s" %percentify((sum([r[2] for r in res])/len(res))) 
    for r in res:
        print "%s   %.1f   %s" %(r[0], r[1], percentify(r[2]))

def pair_count (strat_dict, specials):
    styles = sorted(list(set([p[0] for p in strat_dict.keys()
                       if p[0]!= 'Special' or specials])))
    bases = sorted(list(set([p[1] for p in strat_dict.keys()
                      if p[0]!= 'Special' or specials])))
    antes = sorted(list(set([p[2] for p in strat_dict.keys()
                      if p[0]!= 'Special' or specials])))
    count = array([[sum([strat_dict[(s,b,a)] if (s,b,a) in strat_dict.keys()
                                             else 0
                         for a in antes])
                    for b in bases]
                   for s in styles])
    return count, styles, bases

def style_ante_count (strat_dict, specials=False):
    styles = sorted(list(set([p[0] for p in strat_dict.keys()
                       if p[0]!= 'Special' or specials])))
    bases = sorted(list(set([p[1] for p in strat_dict.keys()
                      if p[0]!= 'Special' or specials])))
    antes = sorted(list(set([p[2] for p in strat_dict.keys()
                      if p[0]!= 'Special' or specials])))
    count = array([[sum([strat_dict[(s,b,a)] if (s,b,a) in strat_dict.keys()
                                             else 0
                         for b in bases])
                    for a in antes]
                   for s in styles])
    return count, styles, antes

def base_ante_count (strat_dict, specials=False):
    styles = sorted(list(set([p[0] for p in strat_dict.keys()
                       if p[0]!= 'Special' or specials])))
    bases = sorted(list(set([p[1] for p in strat_dict.keys()
                      if p[0]!= 'Special' or specials])))
    antes = sorted(list(set([p[2] for p in strat_dict.keys()
                      if p[0]!= 'Special' or specials])))
    count = array([[sum([strat_dict[(s,b,a)] if (s,b,a) in strat_dict.keys()
                                             else 0
                         for s in styles])
                    for a in antes]
                   for b in bases])
    return count, bases, antes

def first_beats_percents (name, logdir="first_beats"):
    solution_percents (name, logdir, 1)
    print '----------'
    solution_percents (name, logdir, [1,2])

def solution_percents (name, logdir="first_beats", beat=None):
    if isinstance (beat, int):
        beat = [beat]
    style_dict = {}
    base_dict = {}
    n_beats = 0
    replacement = {p : p.replace(' ','') for p in phrases[name]}
    for filename in list_files(logdir, name):
        with open (filename) as f:
            log = [line for line in f]
        i=0
        while True:
            # forward to start of beat
            while i < len (log) and not log[i].startswith("Beat"):
                i += 1
            if i == len (log):
                break
            current_beat = int(log[i].split(' ')[1])
            # look for first strategy percentage breakdown
            while not log[i] == name.capitalize() + ":\n":
                i += 1
            i += 1
            if beat==None or current_beat in beat:
                n_beats += 1
                while '%' in log[i]:
                    line = log[i][:-1] # snip newline
                    for p in replacement:
                        line = line.replace(p,replacement[p])
                    split = line.split(' ')
                    percent = int (split[0][:-1])
                    if split[1] in style_dict.keys():
                        style_dict[split[1]] += percent
                    else:
                        style_dict[split[1]] = percent
                    if split[2] in base_dict.keys():
                        base_dict[split[2]] += percent
                    else:
                        base_dict[split[2]] = percent
                    i += 1
    bases = sorted ([b for b in base_dict.items()
                     if b[0] not in ['Cancel','Pulse']],
                    key=itemgetter(1), reverse=True)
    for b in bases:
        print b[0], percentify(b[1]/100.0/n_beats)
    if len(bases) < 7:
        print 7-len(bases), "MISSING"
    print '----------------'
    styles = sorted ([s for s in style_dict.items()if s[0] != 'Special'],
                     key=itemgetter(1), reverse=True)
    for s in styles:
        print s[0], percentify(s[1]/100.0/n_beats)
    if len(styles) < 5:
        print 5-len(styles), "MISSING"

def string_is_float (s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def unbeatable_strategies (name, thresh=5, life_thresh=8,
                           logdir="core_tests", outdir="logs/unbeatables/"):
    winfile = open (outdir+'/'+name+'_win_by_%d.txt'%thresh,'w')
    total = 0
    for filename in list_files(logdir, name):
        names = filename.split('/')[-1].split('_')
        count = 0
        with open (filename) as f:
            log = [line for line in f]
        i=0
        while True:
            # search for unbeatable strategy reports
            while i < len (log) and \
                  not log[i].startswith("Unbeatable strategy for %s"
                                        % name.capitalize()):
                i += 1
            if i == len (log):
                break
            if len(log[i].split(' ')) < 6:
                    i += 1
            diffs = []
            first_unbeatable_line = i
            while string_is_float(log[i][:-1].split(' ')[-1]):
                    diffs.append (abs(float(log[i][:-1].split(' ')[-1])))
                    i+=1
            if max(diffs) >= thresh:
                # go back to start of beat
                start = i
                while not log[start].startswith('Beat '):
                    start -= 1
                # find opponent's life total
                j = start
                while True:
                    j += 1
                    if log[j].startswith('life: ') and \
                       not log[j-2].startswith(name.capitalize()):
                        life = int(log[j].split()[-1])
                        break
                if life >= life_thresh:
                    for j in range(start, first_unbeatable_line):
                        winfile.write (log[j])
                    for j in range(len (diffs)):
                        if diffs[j] >= thresh:
                            winfile.write (log[first_unbeatable_line+j])
                    winfile.write("###############################\n")
                    count += 1
        print count, "vs.", \
              (names[0] if names[0].lower()!=name else names[1])
        total += count
    winfile.close()
    print "total:", total

def text (text, name=None, logdir="core_tests", show=False):
    total = 0
    for filename in list_files(logdir, name):
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if line.find(text) != -1:
                total += 1
                if show:
                    print filename, line
    return total
  
def percentify (fraction):
    if fraction >= 0.1:
        return str (int (fraction*100+.5)) + '%'
    else:
        return str(int(fraction*1000+.5)/10.0) + '%'

def abarene_tokens (logdir="core_tests"):
    token_dict = {'Dizziness':0,
                  'Fatigue':0,
                  'Nausea':0,
                  'Lethargy':0}
    beats = 0
    for filename in list_files(logdir, 'abarene'):
        with open (filename) as f:
            log = [line for line in f]
        abarene_reporting = False
        previous_line = ''
        for line in log:
            if line.startswith('---'):
                abarene_reporting = (previous_line == 'Abarene\n')
            elif abarene_reporting and line.startswith ('pool:'):
                tokens = line[6:-1].split(', ')
                for t in tokens:
                    if t!='':
                        token_dict[t] += 1
                beats += 1
            previous_line = line
    for token, count in token_dict.items():
        print token, percentify(count/float(beats))
    print "total:", sum([token_dict[t] for t in token_dict])/float(beats)

def adjenna_marker_beat (target=1, logdir="core_tests"):
    beats = parse_beats('adjenna', logdir)
    check_victories(beats)
    final_beats = [b for b in beats if b.final]
    victories = sum([beat.points for beat in final_beats])
    petrifications = len([beat for beat in final_beats 
                          if beat.lines_ending_with(
                                    'has 6 Petrificatoin Markers')])
    for beat in beats:
        lines = beat.lines_containing('Petrification markers on')
        beat.markers = int(lines[0][0])
    victories_with_target = sum([beat.points for beat in final_beats
                                 if beat.markers >= target])
    # 1-15 is beat in which opponent got to target number of markers
    # 0 means never
    gain_beat = [0] * 16
    for i in xrange(1, len(beats)):
        if beats[i].markers >= target and beats[i-1].markers < target:
            gain_beat[beats[i].number] += 1
        if beats[i].final and beats[i].maker < target:
            gain_beat[0] += 1 
    print "total games:", sum(gain_beat)
    print "victories:", victories
    print "petrifications:", petrifications
    games_with_target = sum(gain_beat) - gain_beat[0]
    print "victories with at least %d markers: %d/%d (%s)"\
          %(target, victories_with_target, games_with_target,
            percentify (victories_with_target/float(games_with_target)))
    for beat,count in enumerate(gain_beat):
        print beat,count
                        
def adjenna_marker_and_wins (target_beat, logdir="core_tests"):
    games_with_x_markers = [0,0,0,0,0,0,0]
    victories_with_x_markers = [0,0,0,0,0,0,0]
    beats = parse_beats['adjenna', logdir]
    for i in xrange(len(beats)):
        if (beats[i].beat_number == target_beat and
            beats[i-1].beat_number < target_beat): 
            lines = beats[i].lines_containing('Petrification markers on')
            markers = int(lines[0][0])
            games_with_x_markers[markers] += 1
            victories_with_x_markers[markers] += beats[i].points
    total = sum (games_with_x_markers)
    print "total games:", total
    print "or more:"
    for i in range(7):
        print i, percentify (sum(games_with_x_markers[i:])/float(total)), \
              percentify (float(sum(victories_with_x_markers[i:])) /\
                          (0.000001+sum(games_with_x_markers[i:])))
    print "or less:"
    for i in range(7):
        print i, percentify (sum(games_with_x_markers[:i+1])/float(total)), \
              percentify (float(sum(victories_with_x_markers[:i+1])) /\
                          (0.000001+sum(games_with_x_markers[:i+1])))

def alexian_tokens (logdir="core_tests"):
    beats = parse_beats('alexian', logdir)
    for beat in beats:
        if beat.opp_induced_ante:
            beat.opp_induced_ante = int(beat.opp_induced_ante[1])
        else:
            beat.opp_induced_ante = 0
        for line in beat.lines:
            if " has " in line and " Chivalry token" in line:
                beat.tokens = int(line.split()[2])
                break
    tokens = Counter([beat.tokens for beat in beats])
    antes = Counter([beat.opp_induced_ante for beat in beats])
    post_ante = Counter([beat.tokens - beat.opp_induced_ante for beat in beats])
    beat_sums = Counter([beat.number for beat in beats])
    beat_counts = [sum([beat.tokens for beat in beats
                        if beats.number == i])
                   for i in xrange(16)]
    print "Chivalry tokens at start of beat:"
    for i, count in enumerate(tokens):
        print i, percentify(count/float(sum(tokens)))
    print "total:", sum(tokens)

    print "Anted chivalry tokens"
    for i, count in enumerate(antes):
        print i, percentify(count/float(sum(antes)))
    print "total:", sum(antes)

    print "Un-anted chivalry tokens"
    for i, count in enumerate(post_ante):
        print i, percentify(count/float(sum(antes)))
    print "total:", sum(post_ante)

    print "Chivalry token accumulation by beat"
    for i in range(1,16):
        print "%d: %.1f" %(i, beat_counts[i]/float(beat_sums[i]))
    print

    parse_base_vs_induced_ante('alexian', logdir)

def alumis_styles(logdir='core_tests'):
    beats = parse_beats('alumis', logdir)
    arcane = [b for b in beats if b.style == 'Arcane']
    arcane_hits = [b for b in arcane 
                   if any(line != 'Alumis hits\n' 
                          for line in b.lines_containing(' hits\n'))]
    arcane_soak = [b for b in arcane_hits
                   if b.lines_containing('Alumis has 2 soak')]
    print "Arcane beats:", len(arcane)
    print "Arcane hits taken:", len(arcane_hits)
    print "Arcane soaks: %d (%s)" % (len(arcane_soak),
                                     percentify(len(arcane_soak) / 
                                                float(len(arcane_hits))))
    for b in arcane_soak:
        if b not in arcane_hits:
            for line in b.lines:
                print line
    ghastly = [b for b in beats if b.style == 'Ghastly']
    ghastly_power = [b for b in ghastly
                     if b.lines_containing('Alumis gets +2 power')]
    ghastly_life = [b for b in ghastly
                      if not all(line.startswith('Alumis loses 2 life') 
                                 for line in b.lines_containing(' loses 2 life'))]
    print "Ghastly beats:", len(ghastly)
    print "Ghastly power: %d (%s)" % (len(ghastly_power),
                                      percentify(len(ghastly_power) /
                                                 float(len(ghastly))))
    print "Ghastly life loss: %d (%s)" % (len(ghastly_life),
                                         percentify(len(ghastly_life) /
                                                    float(len(ghastly))))
    tenebrous = [b for b in beats if b.style == 'Tenebrous']
    tenebrous_life = [b for b in tenebrous
                      if not all(line.startswith('Alumis loses 2 life') 
                                 for line in b.lines_containing(' loses 2 life'))]
    print "Tenebrous beats:", len(tenebrous)
    print "Tenebrous life loss: %d (%s)" % (len(tenebrous_life),
                                            percentify(len(tenebrous_life) /
                                                       float(len(tenebrous))))
    sinister = [b for b in beats if b.style == 'Sinister']
    sinister_hits = 0
    sinister_moves = 0
    for b in sinister:
        hit = False
        for line in b.lines:
            if line == "Alumis hits\n":
                hit = True
                sinister_hits += 1
            # Any move after the hit is from Sinister.
            if hit:
                if line == 'Alumis moves:\n':
                    sinister_moves += 1
                    break
    print "Sinister beats:", len(sinister)
    print "Sinister hits:", sinister_hits
    print "Sinister moves: %d (%s)" % (sinister_moves,
                                       percentify(sinister_moves / 
                                                  float(sinister_hits)))

def arec_tokens (logdir="core_tests"):
    token_dict = {'Fear':0,
                  'Hesitation':0,
                  'Mercy':0,
                  'Recklessness':0}
    beats = 0
    for filename in list_files(logdir, 'arec'):
        with open (filename) as f:
            log = [line for line in f]
        arec_reporting = False
        previous_line = ''
        for line in log:
            if line.startswith('---'):
                arec_reporting = (previous_line == 'Arec\n')
            elif arec_reporting and line.startswith ('pool:'):
                tokens = line[6:-1].split(', ')
                for t in tokens:
                    if t!='':
                        token_dict[t] += 1
                beats += 1
            previous_line = line
    for token, count in token_dict.items():
        print token, percentify(count/float(beats))
    print "total:", sum([token_dict[t] for t in token_dict])/float(beats)

def aria_droids (logdir="core_tests"):
    n_beats = 0.0
    # last slot is for 'None'
    dampening = [0] * 8
    magnetron = [0] * 8
    turret = [0] * 8
    beat = None
    for filename in list_files(logdir, 'aria'):
        with open (filename) as f:
            log = [line for line in f]
        # figure out what side aria starts on in this matchup
        left = 'aria' in filename.split('_')[0]
        for i, line in enumerate(log):
            if line.startswith ("Beat "):
                beat = int(line.split()[-1])
                n_beats += 1
            # board will alway have '..' in it
            elif beat is not None and '..' in line:
                beat = None # stop looking for droids this beat
                d = log[i+1].find('d')
                if d == -1:
                    d = 7
                else:
                    d = d if left else 6-d
                dampening[d] += 1 
                m = log[i+2].find('m')
                if m == -1:
                    m = 7
                else:
                    m = m if left else 6-m
                magnetron[m] += 1 
                t = log[i+3].find('t')
                if t == -1:
                    t = 7
                else:
                    t = t if left else 6-t
                turret[t] += 1 
    print "dampening: %s" % percentify(sum(dampening[:-1])/n_beats)
    for i in range(7):
        print percentify(dampening[i]/n_beats),
    print
    print "magnetron: %s" % percentify(sum(magnetron[:-1])/n_beats)
    for i in range(7):
        print percentify(magnetron[i]/n_beats),
    print
    print "turret: %s" % percentify(sum(turret[:-1])/n_beats)
    for i in range(7):
        print percentify(turret[i]/n_beats),
    print

def baenvier_tokens (logdir="core_tests"):
    beat_counts = [0] * 16
    beat_tokens = [0] * 16
    beats = parse_beats('baenvier', logdir)
    for beat in beats:
        beat_counts[beat.number] += 1
        for line in beat.lines:
            if (line[1:] == " Spell Eater token\n" or 
                line[1:] == " Spell Eater tokens\n"):
                beat.tokens = int(line[0])
                beat_tokens[beat.number] += beat.tokens
                break
    tokens = Counter([beat.tokens for beat in beats])
    total = len(beats)
    for t in sorted(tokens.keys()):
        print t, percentify(tokens[t]/float(total))
    print "total:", total
    print
    for b in xrange(1,16):
        print "%d: %.1f" % (b, beat_tokens[b]/float(beat_counts[b]))

def clinhyde_stims (logdir="core_tests"):
    stims = {}
    n_stims = [0,0,0,0]
    for filename in list_files(logdir, 'clinhyde'):
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if line.startswith('Active Stim Packs:'):
                s = line.strip().split(' ')
                n_stims[len(s)-3] += 1
                for p in s[3:]:
                    p = p.strip(',\n')
                    if p in stims.keys():
                        stims[p] += 1
                    else:
                        stims[p] = 1
    total = float(sum(n_stims))
    print "Number of Stims:"
    for i,n in enumerate (n_stims):
        print i, percentify(n/total)
    for p in stims.keys():
        print p, percentify (stims[p]/total)
     
def eligor_tokens (logdir="core_tests"):
    tokens = [0,0,0,0,0,0]
    for filename in list_files(logdir, 'eligor'):
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if line[2:] == "Vengeance tokens\n":
                tokens[int(line[0])] += 1
    for i, count in enumerate(tokens):
        print i, percentify(count/float(sum(tokens)))
    print "total:", sum(tokens)

def eustace_counters (logdir="core_tests"):
    beat_counts = [0] * 16
    beat_tokens = [0] * 16
    beats = parse_beats('eustace', logdir)
    for beat in beats:
        beat_counts[beat.number] += 1
        for line in beat.lines:
            if (line.startswith("Frost: ")):
                beat.tokens = int(line[-2])
                beat_tokens[beat.number] += beat.tokens
                break
    tokens = Counter([beat.tokens for beat in beats])
    total = len(beats)
    for t in sorted(tokens.keys()):
        print t, percentify(tokens[t]/float(total))
    print "total:", total
    print
    for b in xrange(1,16):
        print "%d: %.1f" % (b, beat_tokens[b]/float(beat_counts[b]))
    print "Defrosting losses:", text("Eustace runs out of Frost",
                                     'eustace', logdir)

def gerard_gold(logdir='core_tests'):
    beat_counts = [0] * 16
    beat_gold = [0] * 16
    for filename in list_files(logdir, 'gerard'):
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if line.startswith("Beat "):
                current_beat = int(line[5:-1])
                beat_counts[current_beat] += 1
            if line.startswith("Gold: "):
                gold = int(line[6:-1])
                beat_gold[current_beat] += gold
    for beat in xrange(1,16):
        print "%d: %f" % (beat, beat_gold[beat] / float(beat_counts[beat]))

def hikaru_tokens (logdir="core_tests"):
    token_dict = {'Earth':0,
                  'Fire':0,
                  'Water':0,
                  'Wind':0}
    beats = 0
    for filename in list_files(logdir, 'hikaru'):
        with open (filename) as f:
            log = [line for line in f]
        hikaru_reporting = False
        previous_line = ''
        for line in log:
            if line.startswith('---'):
                hikaru_reporting = (previous_line == 'Hikaru\n')
            elif hikaru_reporting and line.startswith ('Pool:'):
                tokens = line[6:-1].split(', ')
                for t in tokens:
                    if t!='':
                        token_dict[t] += 1
                beats += 1
            previous_line = line
    for token, count in token_dict.items():
        print token, percentify(count/float(beats))
    print "total:", sum([token_dict[t] for t in token_dict])/float(beats)

def jager_signatures(logdir='core_tests'):
    beats = parse_beats('jager', logdir)
    full_count = Counter(beat.ante for beat in beats)
    refined_count = Counter(beat.ante for beat in beats
                            if beat.lines_starting_with('+1 power & priority to signature moves'))
    del full_count['']
    del refined_count['']
    for ante in full_count:
        if ante:
            print "%s: %d (%d)" % (ante, full_count[ante], 
                                         refined_count[ante]) 
    print "Total: %d (%d)" % (sum(full_count.values()), 
                              sum(refined_count.values()))
    
def iri_forms(logdir="core_tests"):
    beats = parse_beats('iri', logdir)
    beats = [b for b in beats 
             if b.ante and b.base not in ('Pulse', 'Dash')]
    forms = Counter(beat.ante for beat in beats)
    total = float(sum(forms.values()))
    print "Forms:"
    for form, count in forms.items():
        print form, count, percentify(count / total)
    for beat in beats:
        beat.current_form = beat.lines_ending_with(' Form')[0][:-1]
    transforms = Counter(beat.ante for beat in beats
                         if beat.ante[1:-1] != beat.current_form)
    total = float(sum(transforms.values()))
    print "\nTransforms:"
    for form, count in transforms.items():
        print form, count, percentify(count / total), percentify(count/float(forms[form]))
        
def kajia_insects(logdir='core_tests'):
    insect_count = [[0]*10 for unused in (0,1,2)]
    totals_count = [0] * 10
    piles_count = [0] * 3
    for filename in list_files(logdir, 'kajia'):
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if " insects on opponent's discard " in line:
                discard = int(line[-2])
                insects = int(line[0])
                insect_count[discard][insects] += 1
                if discard == 1:
                    discard1 = insects
                else:
                    total = discard1 + insects
                    n_piles = (discard1 > 0) + (insects > 0)
                    totals_count[total] += 1
                    piles_count[n_piles] += 1
    print "Total insects:"
    beats = float(sum(totals_count))
    for i in xrange(10):
        if totals_count[i]:
            print "%d: %s" % (i, percentify(totals_count[i]/beats))
    print "Discard piles with insects:"
    assert beats == float(sum(piles_count))
    for i in xrange(3):
        print "%d: %s" % (i, percentify(piles_count[i]/beats))
    print "Discard 1 insects:"
    assert beats == float(sum(insect_count[1]))
    for i in xrange(10):
        if insect_count[1][i]:
            print "%d: %s" % (i, percentify(insect_count[1][i]/beats))
    print "Discard 2 insects:"
    assert beats == float(sum(insect_count[2]))
    for i in xrange(10):
        if insect_count[2][i]:
            print "%d: %s" % (i, percentify(insect_count[2][i]/beats))

def karin_jager (logdir="core_tests"):
    karin_dists = [0,0,0,0,0,0,0]
    opp_dists = [0,0,0,0,0,0,0]
    for filename in list_files(logdir, 'karin'):
        names = filename.split('/')[-1].split('_')
        initial0 = names[0][0].upper()
        initial1 = names[1][0].upper()
        if initial0 == initial1:
            initial1 = initial1.lower()
        if names[0] == 'karin':
            karin_init, opp_init = initial0, initial1
        else:
            karin_init, opp_init = initial1, initial0
        with open (filename) as f:
            log = [line for line in f]
        i=0
        while True:
            # forward to start of beat
            while i < len (log) and not log[i].startswith("Beat"):
                i += 1
            if i == len (log):
                break
            # look for board
            while sum([c=='.' for c in log[i]]) != 5:
                i += 1
            karin_pos = log[i].find(karin_init)
            opp_pos = log[i].find(opp_init)
            j = i + 1
            while True:
                jager_pos = log[j].find('j')
                if jager_pos > -1:
                    break
                j += 1
            karin_dists [abs(karin_pos-jager_pos)] += 1
            opp_dists [abs(opp_pos-jager_pos)] += 1
    total = float(sum(karin_dists))
    print "Karin-Jager distances:"
    for i,d in enumerate(karin_dists):
        print "%d: %s" %(i, percentify(d/total))
    print "Opponent-Jager distances:"
    for i,d in enumerate(opp_dists):
        print "%d: %s" %(i, percentify(d/total))

def larimore_counters (logdir="core_tests"):
    beat_counts = [0] * 16
    beat_tokens = [0] * 16
    beats = parse_beats('larimore', logdir)
    for beat in beats:
        beat_counts[beat.number] += 1
        for line in beat.lines:
            if (line.startswith("Firepower: ")):
                beat.tokens = int(line[-2])
                beat_tokens[beat.number] += beat.tokens
                break
    tokens = Counter([beat.tokens for beat in beats])
    total = len(beats)
    for t in sorted(tokens.keys()):
        print t, percentify(tokens[t]/float(total))
    print "total:", total
    print
    for b in xrange(1,16):
        print "%d: %.1f" % (b, beat_tokens[b]/float(beat_counts[b]))

def larimore_spending(logdir='core_tests'):
    beats = parse_beats('larimore', logdir)
    for beat in beats:
        beat.style_spend = 0
        beat.might_spend = 0
        for i, line in enumerate(beat.lines):
            if line.startswith('Larimore spends '):
                spend = int(line.split()[2])
                if (beat.final_base == 'Might' and 
                    beat.lines[i+1] == "Larimore gets +%d power\n" % spend):
                    beat.might_spend += spend
                else:
                    beat.style_spend += spend
    styles = set(beat.style for beat in beats)
    total_spend = 0
    for style in styles:
        style_spend = 0
        print style
        for spend in range(6):
            n = len([b for b in beats if b.style == style and 
                     b.style_spend == spend])
            print spend, n 
            style_spend += spend * n
        print "total:", style_spend 
        total_spend += style_spend
    print 'Might'
    might_spend = 0
    for spend in range(6):
        n = len([b for b in beats if b.final_base == 'Might' and 
                 b.might_spend == spend])
        print spend, n
        might_spend += spend *n
    print "total:", might_spend
    total_spend += might_spend
    print "grand total:", total_spend

def luc_tokens (logdir="core_tests"):
    beat_counts = [0] * 16
    beat_tokens = [0] * 16
    beats = parse_beats('luc', logdir)
    for beat in beats:
        beat_counts[beat.number] += 1
        for line in beat.lines:
            if (line[1:] == " Time token\n" or 
                line[1:] == " Time tokens\n"):
                beat.tokens = int(line[0])
                beat_tokens[beat.number] += beat.tokens
                break
    tokens = Counter([beat.tokens for beat in beats])
    total = len(beats)
    for t in sorted(tokens.keys()):
        print t, percentify(tokens[t]/float(total))
    print "total:", total
    print
    for b in xrange(1,16):
        print "%d: %.1f" % (b, beat_tokens[b]/float(beat_counts[b]))

def magdelina_spiritual(logdir="core_tests"):
    beats = parse_beats('magdelina', logdir)
    for beat in beats:
        if (beat.style == 'Spiritual' and
            "Level: 0\n" in beat.lines):
            for line in beat.lines:
                print line 

def marmelee_counters (logdir="core_tests"):
    beat_counts = [0] * 16
    beat_tokens = [0] * 16
    beats = parse_beats('marmelee', logdir)
    for beat in beats:
        beat_counts[beat.number] += 1
        for line in beat.lines:
            if (line[1:] == " Concentration counter\n" or 
                line[1:] == " Concentration counters\n"):
                beat.tokens = int(line[0])
                beat_tokens[beat.number] += beat.tokens
                break
    tokens = Counter([beat.tokens for beat in beats])
    total = len(beats)
    for t in sorted(tokens.keys()):
        print t, percentify(tokens[t]/float(total))
    print "total:", total
    print
    for b in xrange(1,16):
        print "%d: %.1f" % (b, beat_tokens[b]/float(beat_counts[b]))

def marmelee_spending (logdir="core_tests"):
    style_spend_dict = {}
    for filename in list_files(logdir, 'marmelee'):
        names = filename.split('/')[-1].split('_')
        with open (filename) as f:
            log = [line for line in f]
        style = None
        spend = 0
        for i in range(len(log)):
            line = log[i][:-1]
            if line.startswith("Marmelee: "):
                split = line.split(' ')
                style = split[1]
                if split[2]=='Meditation':
                    style += ' Meditation'
                if split[2]=='Dash':
                    style += ' Dash'
            if style is not None and line.startswith('Beat '):
                key = (style, spend)
                if spend >=6:
                    name = [n for n in names if n!='Marmelee'][0]
                    print "spent 6 tokens against %s: line %d" %(name, i)
                if key in style_spend_dict.keys():
                    style_spend_dict[key] += 1
                else:
                    style_spend_dict[key] = 1
                spend = 0
            if re.search(r'Marmelee discards . Concentration Counters$',
                         line):
                spend += int(line.split(' ')[2])
                if log[i+1].startswith ('Marmelee moves:'):
                    spend += .1 # additional +.1 marks spending for move
            if line.startswith('Marmelee gains Soak'):
                spend += .01 * int (line[-1])
            if line.startswith('Marmelee becomes the active player'):
                spend += .001
        key = (style, spend)
        if key in style_spend_dict.keys():
            style_spend_dict[key] += 1
        else:
            style_spend_dict[key] = 1
    for key in sorted (style_spend_dict.keys()):
        total = 0
        for otherkey in style_spend_dict.keys():
            if otherkey[0]==key[0]:
                total += style_spend_dict[otherkey]
        print key, style_spend_dict[key], \
              percentify(style_spend_dict[key]/float(total))

def mikhail_pairs_with_tokens (logdir="core_tests"):
    beats = parse_beats('mikhail', logdir)
    beats = [b for b in beats if b.ante]
    d = Counter([(b.style, b.base, b.ante) for b in beats])
    count, first, second = pair_count (d, False)
    if len (second) > 1:
        first_count = count.sum(axis=1)
        second_count = count.sum(axis=0)
        total = count.sum()
        for x in range(len(first)):
            for y in range(len(second)):
                cxy = count[x][y]
                print first[x], second[y], \
                      percentify(cxy/float(first_count[x])), \
                      percentify(cxy/float(second_count[y])),
                ratio = float(cxy * total) / (first_count[x]*second_count[y])
                if ratio > 1.5:
                    print "STRONG - %.2f" %ratio
                elif ratio < 0.5:
                    print "WEAK - %.2f" %ratio
                else:
                    print                                     
          
def mikhail_tokens (logdir="core_tests"):
    beat_tokens = [[0] * 4 for unused in range(16)]
    antes = [[0] * 2 for unused in range(16)]
    ante_this_beat = None
    for filename in list_files(logdir, 'mikhail'):
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if line.startswith('Beat '):
                beat = int(line.split(' ')[1])
                if ante_this_beat is not None:
                    antes[beat][int(ante_this_beat)] += 1
                ante_this_beat = False
            elif len(line) == 14 and line.endswith (' Seal tokens\n'):
                beat_tokens[beat][int(line[0])] += 1
            elif line.startswith('Mikhail: ') and ' (Seal)' in line:
                ante_this_beat = True
    tokens = [sum([beat_tokens[b][t] for b in range(16)]) for t in range(4)]
    total = sum(tokens)
    for t in range(4):
        print t, "tokens:", percentify(tokens[t]/float(total))
    for b in range(1,16):  
        print "beat %d: %.1f tokens;  %s ante" \
              %(b,
                sum([beat_tokens[b][t]*t for t in range(4)]) /
                   float(sum(beat_tokens[b])),
                percentify(antes[b][1]/float(sum(antes[b]))))

def oriana_meteor (logdir="core_tests"):
    beats = parse_beats('oriana', logdir)
    d = Counter([(b.style, b.base, b.ante) for b in beats])
    styles = sorted(list(set([k[0] for k in d])))
    bases = sorted(list(set([k[1] for k in d])))
    tokens = sorted(list(set([k[2] for k in d])))
    for s in styles:
        if s != "Special":
            print s, "Meteor"
            total = float(sum([d.get((s,"Meteor",t),0) for t in tokens]))
            for t in tokens:
                print t, percentify(d.get((s,"Meteor",t),0)/total)
            print s, "(no Meteor)"
            total = float(sum([d[k] for k in d if k[0]==s and k[1]!="Meteor"]))
            for t in tokens:
                tmp = 0
                for b in bases:
                    if b != "Meteor":
                        tmp += d.get((s,b,t),0)
                print t, percentify(tmp/total)
        
def oriana_tokens (logdir="core_tests"):
    beat_counts = [0] * 16
    beat_tokens = [0] * 16
    beats = parse_beats('oriana', logdir)
    for beat in beats:
        beat_counts[beat.number] += 1
        for line in beat.lines:
            if (line[1:] == " Magic Point token\n" or 
                line[1:] == " Magic Point tokens\n" or
                line[2:] == " Magic Point token\n" or
                line[2:] == " Magic Point tokens\n"):
                beat.tokens = int(line[0])
                beat_tokens[beat.number] += beat.tokens
                break
    tokens = Counter([beat.tokens for beat in beats])
    total = len(beats)
    for t in sorted(tokens.keys()):
        print t, percentify(tokens[t]/float(total))
    print "total:", total
    print
    for b in xrange(1,16):
        print "%d: %.1f" % (b, beat_tokens[b]/float(beat_counts[b]))


def rexan_tokens (logdir="core_tests"):
    beats = parse_beats('alexian', logdir)
    for beat in beats:
        if beat.opp_induced_ante:
            beat.opp_induced_ante = int(beat.opp_induced_ante[1])
        else:
            beat.opp_induced_ante = 0
        for line in beat.lines:
            if " has " in line and " Curse token" in line:
                beat.tokens = int(line.split()[2])
                break
    tokens = Counter([beat.tokens for beat in beats])
    antes = Counter([beat.opp_induced_ante for beat in beats])
    post_ante = Counter([beat.tokens - beat.opp_induced_ante for beat in beats])
    beat_sums = Counter([beat.number for beat in beats])
    beat_counts = [sum([beat.tokens for beat in beats
                        if beats.number == i])
                   for i in xrange(16)]
    print "Curse tokens at start of beat:"
    for i, count in enumerate(tokens):
        print i, percentify(count/float(sum(tokens)))
    print "total:", sum(tokens)

    print "Anted curse tokens"
    for i, count in enumerate(antes):
        print i, percentify(count/float(sum(antes)))
    print "total:", sum(antes)

    print "Un-anted curse tokens"
    for i, count in enumerate(post_ante):
        print i, percentify(count/float(sum(antes)))
    print "total:", sum(post_ante)

    print "Curse token accumulation by beat"
    for i in range(1,16):
        print "%d: %.1f" %(i, beat_counts[i]/float(beat_sums[i]))

    print
    parse_base_vs_induced_ante('rexan', logdir)
    
def runika_artifacts (logdir="core_tests"):
    artifacts = ['Hover Boots',
                 'Battlefist',
                 'Autodeflector',
                 'Shield Amulet',
                 'Phase Goggles']
    active = {a:0 for a in artifacts}
    removed = {a:0 for a in artifacts}
    beats = 0
    for filename in list_files(logdir, 'runika'):
        with open (filename) as f:
            log = [line for line in f]
        for i in range(len(log)):
            if log[i].startswith('Active artifacts:'):
                beats += 1
                k = i + 1
                while log[k].startswith('  '):
                    active[log[k][2:-1]] += 1
                    k += 1
            if log[i].startswith('Removed artifacts:'):
                k = i + 1
                while log[k].startswith('  '):
                    removed[log[k][2:-1]] += 1
                    k += 1
    print "Active:"
    for artifact in active:
        print "%s: %s" % (artifact, percentify(active[artifact]/float(beats)))
    print
    print "Removed:"
    for artifact in removed:
        print "%s: %s" % (artifact, percentify(removed[artifact]/float(beats)))
    print
    games = float(10 * (len(phrases)-1))
    activations = {a : text("%s is activated"%a, 'runika', logdir) / games
                   for a in artifacts}
    deactivations = {a : text("%s is de-activated"%a, 'runika', logdir) / games
                     for a in artifacts}
    removals = {a : text("%s is removed"%a, 'runika', logdir) / games
                for a in artifacts}
    overcharges = {a : text("Runika overcharges her %s"%a, 'runika', logdir) / games
                   for a in artifacts}
    print "Activations:"
    for a in artifacts:
        print "%s: %.2f" %(a, activations[a])
    print
    print "Deactivations (without overcharged):"
    for a in artifacts:
        print "%s: %.2f" %(a, deactivations[a])
    print
    print "Overcharges (including Artifice Avarice):"
    for a in artifacts:
        print "%s: %.2f" %(a, overcharges[a])
    print
    print "removals:"
    for a in artifacts:
        print "%s: %.2f" %(a, removals[a])
    print
    print "Net Loss:"
    for a in artifacts:
        print "%s: %.2f" %(a, deactivations[a]+removals[a]-activations[a])
    print
    print "Total:"
    print "activations: %.2f"% sum(activations.itervalues())
    print "deactivations (no overcharge): %.2f"% (sum(deactivations.itervalues()))
    print "removals: %.2f"% sum(removals.itervalues())
    print "net loss: %.2f"% (sum(deactivations.itervalues())
                           + sum(removals.itervalues())
                           - sum(activations.itervalues()))
    

def shekhtur_tokens (logdir="core_tests"):
    tokens = [0,0,0,0,0,0]
    for filename in list_files(logdir, 'shekhtur'):
        with open (filename) as f:
            log = [line for line in f]
        for line in log:
            if line[2:] == "Malice tokens\n":
                tokens[int(line[0])] += 1
    for i, count in enumerate(tokens):
        print i, percentify(count/float(sum(tokens)))
    print "total:", sum(tokens)

def voco_zombies (logdir="core_tests"):
    zombies = [0,0,0,0,0,0,0,0]
    zom_pos = [0,0,0,0,0,0,0]
    zom_opp = 0
    for filename in list_files(logdir, 'voco'):
        names = filename.split('/')[-1].split('_')
        voco_on_right = (names[1] == 'voco')
        voco_initial = 'v' if voco_on_right and names[0][0]=='v' else 'V'
        with open (filename) as f:
            log = [line for line in f]
        i=0
        while True:
            # forward to start of beat
            while i < len (log) and not log[i].startswith("Beat"):
                i += 1
            if i == len (log):
                break
            # look for board
            while sum([c=='.' for c in log[i]]) != 5:
                i += 1
            for p in range(7):
                if log[i][p] not in ['.',voco_initial]:
                    opponent = p
                    break
            zombies[sum([c=='z' for c in log[i+1]])] += 1
            if len (log[i+1]) == 8:
                for pos in range(7):
                    if log[i+1][pos] == 'z':
                        if voco_on_right:
                            pos = 6-pos
                        zom_pos[pos] += 1
                if log[i+1][opponent] == 'z':
                    zom_opp += 1
    total = float(sum(zombies))
    for i,z in enumerate(zombies):
        print "%d: %s" %(i, percentify(z/total))
    print "average: %.2f" %sum([i*z/total for i,z in enumerate(zombies)])
    print "positions:"
    for p,z in enumerate(zom_pos):
        print "%d: %s" %(p, percentify(z/total))
    print "on opponent:", percentify(zom_opp/total)

def xenitia_draw(logdir="core_tests"):
    beats = parse_beats('xenitia', logdir)
    style_dict = {}
    for beat in beats:
        if beat.style == 'Special' or beat.base in ('Dash', 'Bloodweapon'):
            continue
        if beat.style not in style_dict:
            style_dict[beat.style] = [0] * 6
        style_dict[beat.style][int(beat.ante[1])] += 1
    for style, draws in style_dict.items():
        print style
        total = float(sum(draws))
        for i, d in enumerate(draws):
            print i, percentify(d / total)

def zaamassal_paradigms (logdir="core_tests"):
    for paradigm in ['Pain','Fluidity','Haste','Resilience','Distortion']:
        print paradigm, 
        print text("Zaamassal assumes the Paradigm of %s"%paradigm, 'zaamassal',
             logdir)

def parse_base_vs_induced_ante (name, logdir="core_tests"):
    beats = parse_beats(name, logdir)
    bases = ['Burst','Dash','Drive','Grasp','Shot','Strike','Cancel','Pulse']
    all_bases = bases + ['Finisher','Unique']
    for beat in beats:
        if beat.opp_base not in bases:
            if beat.opp_style == 'Special':
                beat.opp_base = 'Finisher'
            else:
                beat.opp_base = 'Unique'
    strategy_dict = Counter([(beat.opp_base, beat.opp_induced_ante)
                             for beat in beats])
    antes = sorted(list(set([s[1] for s in strategy_dict])))
    count = array([[strategy_dict.get((b,a), 0)
                    for a in antes]
                   for b in all_bases])

    base_count = count.sum(axis=1)
    ante_count = count.sum(axis=0)
    total = count.sum()

    bc = [(all_bases[i],base_count[i]) for i in range(len(all_bases))]
    bc = sorted (bc, key=itemgetter(1), reverse=True)
    for b in bc:
        print percentify(b[1]/float(total)), b[0]
    print '--------------'
    ac = [(antes[i],ante_count[i]) for i in range(len(antes))]
    ac = sorted (ac, key=itemgetter(1), reverse=True)
    for a in ac:
        print percentify(a[1]/float(total)), a[0]
    print '--------------'
    for x in range(len(all_bases)):
        if base_count[x]:
            for y in range(len(antes)):
                if ante_count[y]:
                    cxy = count[x][y]
                    print all_bases[x], antes[y], \
                          percentify(cxy/float(base_count[x])), \
                          percentify(cxy/float(ante_count[y])),
                    ratio = float(cxy * total) / (base_count[x]*ante_count[y])
                    if ratio > 1.5:
                        print "STRONG - %.2f" %ratio
                    elif ratio < 0.5:
                        print "WEAK - %.2f" %ratio
                    else:
                        print                                     

def post_processing_adjenna(beats):
    for beat in beats:
        lines = beat.lines_containing(' Petrification markers on ')
        beat.ante = "(Petrification %d)" % int(lines[0][0])
        
def post_processing_arec(beats):
    for beat in beats:
        if beat.ante == '(move to clone)':
            beat.ante = ''
        elif 'move to clone' in beat.ante:
            beat.ante = beat.ante.split(';')[0] + ')'
        
def post_processing_byron(beats):
    for beat in beats:
        lines = beat.lines.ending_with(' Mask emblems')
        beat.ante = '(%d masks)' % lines[0][0]

def post_processing_cesar(beats):
    print "Threat level is expected level after ante.\n"
    for beat in beats:
        lines = beat.lines_starting_with('Threat level: ')
        beat.ante = int(lines[0].split(' ')[2])
    
def post_processing_kallistar(beats):
    for beat in beats:
        if beat.lines_containing('Elemental Form'):
            beat.ante = 'Elemental'
        else:
            beat.ante = 'Human'

def post_processing_jager(beats):
    for beat in beats:
        if beat.ante != '':
            beat.style = 'Special'
            beat.base = beat.ante
            beat.ante = ''

def post_processing_lymn(beats):
    for beat in beats:
        lines = beat.lines_starting_with('Disparity is ')
        beat.ante = '(disparity: %s)' % lines[0][13]

def post_processing_magdelina(beats):
    for beat in beats:
        lines = beat.lines_starting_with('Level: ')
        beat.ante = '(level %s)' % lines[0][7]

def post_processing_seth(beats):
    standard_antes = ['(Strike)','(Shot)','(Dash)',
                      '(Burst)','(Drive)','(Grasp)','']
    for beat in beats:
        if beat.ante not in standard_antes:
            beat.ante = '(Unique)'
    
def post_processing_tanis(beats):
    # Set beat antes to the puppet possessed.
    for beat in beats:
        line = beat.lines_starting_with("Tanis possesses ")[0]
        beat.ante = line.split(' ')[2]

