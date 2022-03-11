import sys, os, pathlib, argparse, json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/src")


"""
This class takes in a json learning list and writes it in csv format.
"""
class LearningParser:

    
    def __init__(self):
        self.data = None
	
	
    def read_training_file(self, filename):
        file = open(filename, "r")
        j = file.read()
        file.close()
        self.data = json.loads('[' + j[:-2] + ']')
    
    def write_as_csv(self, filename):
    
        if self.data == None:
            raise Exception("Call to write_as_csv was placed without first calling read_training_file.")
        
        all_features = set()
        
        # find all features
        for w in self.data:
            for f in w.keys():
                all_features.add(f)

        file = open(filename, 'w')
        
        # write column headers
        file.write(','.join(['"' + f + '"' for f in sorted(all_features)]) + '\n')
        
        for d in self.data:
            w = []
            for f in all_features:
                d_keys = set(d.keys())
                if f in d_keys:
                    w.append(d[f])
                else:
                    w.append(0.0)
            file.write(','.join(['"' + str(i) + '"' for i in w]) + '\n')
        
        file.close()
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Turn training record file into a CSV file for processing.")
    
    parser.add_argument("input", type=str, help="The input path.")
    parser.add_argument("output", type=str, help="The output path.")
    args = parser.parse_args()
    
    lp = LearningParser()
    lp.read_training_file(args.input)
    lp.write_as_csv(args.output)