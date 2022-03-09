import sys, os, time, pathlib, argparse, json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/src")

from src.agent_yaron import YaronAgent
from src.agent_learning import LearningAgent
from src.battlecon import Game


"""
Outer class for CSE 573 data gathering: run Eligor v. Shekhtur and output the win/loss ratio.
"""
class GatherResults:

    
    outdir = "results"
    match_results_file = outdir + "/cse_573_match_results.csv"
    training_file = outdir + "/cse_573_training.txt"
    log_file_base = outdir + "/game_log_"
    eligor_strat_file = outdir + "/eligor_strategies.csv"
    shekhtur_strat_file = outdir + "/shekhtur_strategies.csv"
    weights_file = outdir + "/eligor_bot_weights.json"
    
    
    def __init__(self, iterations):
        self.iterations = iterations
    
    
    def go(self):
    
        i = 0
        iterations = self.iterations
    
        while iterations > 0:
            
            i += 1
            if GatherResults.log_exists_for_game(i):
                continue
            
            start_time = time.time()
            print(GatherResults.format_time(start_time) + ": starting duel " + str(i))
            
            p1 = YaronAgent("shekhtur")
            p2 = LearningAgent("eligor")
            
            if os.path.exists(GatherResults.weights_file):
                print("Using weights from " + GatherResults.weights_file)
                p2.load_weights(GatherResults.weights_file)
            
            game = Game.from_start(p1, p2, default_discards=True)
            game_log, winner = game.play_game()
            
            end_time = time.time()
            
            print(GatherResults.format_time(end_time) + ": " + str(winner) + " won.")
            
            GatherResults.make_output_dir()
            p2.save_weights(GatherResults.weights_file)
            GatherResults.log_match_results(game, i, winner, end_time - start_time)
            GatherResults.log_learning(p2)
            GatherResults.log_strategies(p1, i, GatherResults.shekhtur_strat_file)
            GatherResults.log_strategies(p2, i, GatherResults.eligor_strat_file)
            GatherResults.log_game_log(game_log, i)
            
            iterations -= 1


    @staticmethod
    def format_time(t):
        return time.asctime(time.localtime(t))
        
        
    @staticmethod
    def make_output_dir():
        pathlib.Path(GatherResults.outdir).mkdir(parents=True, exist_ok=True)
        
        
    def game_log_file_name(game_num):
        return GatherResults.log_file_base + str(game_num) + ".log"
        
        
    @staticmethod
    def log_exists_for_game(game_num):
        return os.path.exists(GatherResults.game_log_file_name(game_num))
        
        
    @staticmethod
    def log_game_log(game_log, game_num):
        GatherResults.log_content(
            GatherResults.game_log_file_name(game_num),
            "",
            "\n".join(game_log)
        )
    
        
    @staticmethod
    def log_match_results(game, round_number, winner, duration):
    
        p0 = game.player[0]
        p1 = game.player[1]
    
        GatherResults.log_content(
            GatherResults.match_results_file,
            '"game","winner","duration","beats","{} HP","{} HP"\n'.format(p0.get_name(), p1.get_name()),
            '"{}","{}","{}","{}","{}","{}"\n'.format(
                round_number,
                str(winner),
                duration,
                game.current_beat,
                p0.get_fighter().life,
                p1.get_fighter().life
            )
        )
        
        
    @staticmethod
    def log_learning(agent):
        # TODO: write a script to turn this into a list by adding brackets and parse into csv for processing
        GatherResults.log_content(
            GatherResults.training_file,
            "",
            str(json.dumps(agent.get_weights())) + ",\n"
        )
        
        
    @staticmethod
    def log_strategies(agent, game_id, filepath):
        GatherResults.log_content(
            filepath,
            '"game","style","base","ante"\n',
            GatherResults.get_agent_strategies_as_csv(agent, game_id)
        )
        
        
    """
    If necessary, create a new file and write a header. Then write the body content.
    """
    @staticmethod
    def log_content(filepath, header_content, body_content):
        write_header = not os.path.exists(filepath)
        f = open(filepath, "a")
        if write_header:
            f.write(header_content)
        f.write(body_content)
        f.close()
        
        
    @staticmethod
    def get_agent_strategies_as_csv(agent, game_id):
        result = []
        strats = agent.get_logged_strategies()
        for strat in strats:
            result.append('"{}","{}","{}","{}"\n'.format(
                game_id,
                strat[0].name,
                strat[1].name,
                strat[2][0])
            )
        return "".join(result)
        
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Collect results for CSE753.")
    
    parser.add_argument("iterations", type=int, help="The number of duels to simulate.")
    args = parser.parse_args()
    
    GatherResults(args.iterations).go()