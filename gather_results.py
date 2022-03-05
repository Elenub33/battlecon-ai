import sys, os, time, pathlib, argparse
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/src")

from src.agent_yaron import YaronAgent
from src.battlecon import Game


"""
Outer class for CSE 573: run Eligor v. Shekhtur and output the win/loss ratio.
"""
class GatherResults:

    
    outdir = "results"
    outfile = outdir + "/cse_573_results.txt"
    loops = 1
    
    
    def __init__(self, iterations):
        self.iterations = iterations
    
    
    def go(self):
        for i in range(self.iterations):
        
            start_time = time.time()
            print(GatherResults.format_time(start_time) + ": starting duel " + str(i + 1))
            
            p1 = YaronAgent("eligor")
            p2 = YaronAgent("shekhtur")
            game = Game.from_start(p1, p2, default_discards=True)
            game_log, winner = game.play_game()
            
            end_time = time.time()
            
            print(GatherResults.format_time(end_time) + ": " + str(winner) + " won.")
            
            GatherResults.log_results(game, winner, end_time - start_time)


    @staticmethod
    def format_time(t):
        return time.asctime(time.localtime(t))
        
            
    @staticmethod
    def log_results(game, winner, duration):
        
        pathlib.Path(GatherResults.outdir).mkdir(parents=True, exist_ok=True)
        
        write_header = not os.path.exists(GatherResults.outfile)
            
        f = open(GatherResults.outfile, "a")
        if write_header:
            f.write(GatherResults.get_log_header())
        f.write("\"{}\",\"{}\",\"{}\"\n".format(str(winner), duration, game.current_beat))
        f.close()
        
    
    @staticmethod
    def get_log_header():
        return "\"winner\",\"duration\",\"beats\"\n"
        
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Collect results for CSE753.")
    
    parser.add_argument("iterations", type=int, help="The number of duels to simulate.")
    args = parser.parse_args()
    
    GatherResults(args.iterations).go()