'''inverse reinforcement learning algorithm'''
from scipy.optimize import differential_evolution, minimize
import random
import numpy
import copy as py_copy
import math
import sys

NUM_ACT = 4

class observed_inst():
    '''observed data from agent
    look at log likelihood function, at time t, for module instance m of module class n
    we need to record time t, module class n (obstacle or prize), chosen action a, discount factor power d(a), and d(-a)
    a sample is of the form [trial, t, n(0-prize, 1-obstacle], a, [d(Up, Down, Left, Right)]]'''
    def __init__(self, stepCount, module_class, unit_r, chosen_action, ds):
        self.stepCount = stepCount
        self.module_class = module_class
        self.unit_r = unit_r
        self.chosen_action = chosen_action
        self.ds = py_copy.deepcopy(ds) #array of length |ACTIONS|
    
    def record(self, data_file):
        '''write data to file'''
        data_file.write(str(self.module_class) + ',' \
                        + str(self.unit_r) + ','\
                        + str(self.chosen_action) + ',' \
                        + str(self.ds[0]) + ',' + str(self.ds[1]) + ',' + str(self.ds[2]) + ',' + str(self.ds[3]) )
   
    def __str__(self):
        return "[Step:{}, ModuleClassID:{}, UnitReward:{}, Action:{}, Dists: {}]".format \
                (self.stepCount, self.module_class, self.unit_r, self.chosen_action, self.ds)        

class inverse_rl:
    def __init__(self, data_file):
        self.data_file = data_file

    def construct_obj(self, x):
        # construct objective function
        data_file = open(self.data_file,'r')
        logl = 0
        
        # each line is a step of execution
        for line in data_file:
            data = line.split()
            
            insts = []
            # each inst 
            for inst in data:
                inst_data = inst.split(',')
                mc_id = int(inst_data[0])
                unit_r = int(inst_data[1])
                act = int(inst_data[2])
                ds = []
                for i in range(NUM_ACT):
                    ds.append(int(inst_data[i + 3]))        
                
                # the w*r*(gamma**d) term 
                terms = []
                # for each action:
                for d in ds:
                    term = x[mc_id * 2] * unit_r * (x[mc_id * 2 + 1]**d)
                    terms.append(py_copy.deepcopy(term))
                insts.append(py_copy.deepcopy(terms))
            
            # first term in loglikelihood function
            first_term = 0 
            for inst in insts:
                first_term += inst[act]
            
            # second term
            second_term = 0
            for a in range(NUM_ACT):
                temp = 1
                for inst in insts:
                    temp = temp * math.exp(inst[a]) 
                second_term += temp
            second_term = math.log(second_term) 
            
            logl = logl + first_term - second_term

        data_file.close()
        obj = -logl
        print("objective function constructed >>>")
        return obj

    def diff_ev(self):
        # differential evolution
        # two modules the variables are x[0] = w0, x[1] = gamma0, x[2] = w1, x[3] = gamma1...
        bounds = [(0,20),(0.0, 0.99), (0,20),(0.0, 0.99), (0,20),(0.0, 0.99), (0,20),(0.0, 0.99), (0,20),(0.0, 0.99), (0,20),(0.0, 0.99)]
        print("begin differential evolution algorithmi >>>")
        return differential_evolution(self.construct_obj, bounds, tol = 0.05)

if __name__ == '__main__':
    test = inverse_rl(sys.argv[1])
    print(test.diff_ev())
 
