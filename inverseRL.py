'''inverse reinforcement learning algorithm'''
from config import *

class observed_instance():
    '''observed data from agent
    look at log likelihood function, at time t, for module instance m of module class n
    we need to record time t, module class n (obstacle or prize), chosen action a, discount factor power x(a), and x(-a)
    a sample is of the form [trial, t, n(0-prize, 1-obstacle], a, [x(Up, Down, Left, Right)]]'''
    def __init__(self, exp_trial, stepCount, module_class, chosen_action, xs):
        self.exp_trial = exp_trial
        self.stepCount = stepCount
        self.module_class = module_class
        self.chosen_action = chosen_action
        self.xs = py_copy.deepcopy(xs) #array of length |ACTIONS|
    
    def record(self, data_file):
        '''write data to file'''
        data_file.write(str(self.module_class) + ',' \
                        + str(self.chosen_action) +',' \
                        + str(self.xs[0]) + ',' + str(self.xs[1]) + ',' 
                        + str(self.xs[2]) + ',' + str(self.xs[3]) )
   
    def __str__(self):
        return "[Trial:{}, Step:{}, ModuleClassi:{}, Action:{}, Dists: {}]".format \
                (self.exp_trial, self.stepCount, self.module_class, self.chosen_action, self.xs)        

class inverse_rl():
    def __init__(self, filename):
        pass

    def process_data(self):
        pass

    def inverse_rl(self):
        pass
