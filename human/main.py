import world


class Experiment:
    def __init__(self, data_file):
        # read in a data file (a single trial) and build data structure
        pass

    def visualize(self):
        # visualize the environment
        pass

    def discretize(self, gridsize):
        # discretize the state space and convert positions into states
        pass

    def irl(self):
        # call IRL
        pass

    def agent_walk(self):
        # rl agent walk the enviornment and get the path
        pass

    def calc_diff(self):
        # calculate the difference btw agent path and model path
        pass

main()
