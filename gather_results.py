import sys, os, time, pathlib, argparse
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/src")

from src.agent_yaron import YaronAgent
from src.agent_learning import LearningAgent
from src.battlecon import Game


"""
Outer class for CSE 573: run Eligor v. Shekhtur and output the win/loss ratio.
"""
class GatherResults:

    
    outdir = "results"
    match_results_file = outdir + "/cse_573_match_results.csv"
    training_file = outdir + "/cse_573_training.txt"
    eligor_strat_file = outdir + "/eligor_strategies.csv"
    shekhtur_strat_file = outdir + "/shekhtur_strategies.csv"
    
    
    def __init__(self, iterations):
        self.iterations = iterations
    
    
    def go(self):
        for i in range(self.iterations):
        
            start_time = time.time()
            print(GatherResults.format_time(start_time) + ": starting duel " + str(i + 1))
            
            p1 = YaronAgent("shekhtur")
            p2 = LearningAgent("eligor")
            
            game = Game.from_start(p1, p2, default_discards=True)
            game_log, winner = game.play_game()
            
            end_time = time.time()
            
            print(GatherResults.format_time(end_time) + ": " + str(winner) + " won.")
            
            GatherResults.make_output_dir()
            GatherResults.log_match_results(game, i, winner, end_time - start_time)
            GatherResults.log_learning(p2)
            GatherResults.log_strategies(p1, GatherResults.shekhtur_strat_file)
            GatherResults.log_strategies(p2, GatherResults.eligor_strat_file)


    @staticmethod
    def format_time(t):
        return time.asctime(time.localtime(t))
        
            
    @staticmethod
    def make_output_dir():
        pathlib.Path(GatherResults.outdir).mkdir(parents=True, exist_ok=True)
        
        
    @staticmethod
    def log_match_results(game, round_number, winner, duration):
        
        write_header = not os.path.exists(GatherResults.match_results_file)
            
        f = open(GatherResults.match_results_file, "a")
        if write_header:
            f.write(GatherResults.get_match_result_header())
        f.write("\"{}\",\"{}\",\"{}\",\"{}\"\n".format(round_number, str(winner), duration, game.current_beat))
        f.close()
        
    
    @staticmethod
    def get_match_result_header():
        return "\"game\",\"winner\",\"duration\",\"beats\"\n"
        
        
    @staticmethod
    def log_learning(agent):
        
        write_header = not os.path.exists(GatherResults.training_file)
            
        f = open(GatherResults.training_file, "a")
        if write_header:
            f.write(GatherResults.get_match_result_header())
        f.write("\"{}\",\"{}\",\"{}\",\"{}\"\n".format(round_number, str(winner), duration, game.current_beat))
        f.close()
        
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Collect results for CSE753.")
    
    parser.add_argument("iterations", type=int, help="The number of duels to simulate.")
    args = parser.parse_args()
    
    GatherResults(args.iterations).go()