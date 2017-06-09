'''sparse inverse reinforcement learning algorithm for human data fitting'''
from scipy.optimize import minimize,fmin,brute
import random
import numpy
import copy as cp
import math
import sys
import time
import numpy as np
from config import *
np.set_printoptions(precision = 3, suppress = True, linewidth = 1000, threshold = 'nan')

class inverse_rl:
    def __init__(self, data_file, sparse):
        '''data format per time step, per module instance, separated by space
        module class number, unit reward(-1 or 1), action chosen, distance to this instance after taken an action'''
        self.data_file = data_file
        if int(sparse) == 0: self.sparse = False
        else: self.sparse = True
        if self.sparse == True:
            print("sparse version")
        else:
            print("non sparse version")
        # output file is in result/subj#/, the file name without ".fit"
        self.out_filename = "../result/" + data_file.split('/')[-2] + '/' + ((data_file.split('/')[-1]).split('.')[0])
        self.task = int(((data_file.split('/')[-1]).split('.')[0])[-1])
        print("Current Task: ",self.task)

    def construct_obj(self, x):
        # construct objective function
        data_file = open(self.data_file,'r')
        logl = 0
        
        # each line is a single time step
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
                    ds.append(float(inst_data[i + 3]))        
                
                # the w*r*(gamma**d) term 
                terms = []
                # for each action:
                for d in ds:
                    term = x[mc_id * 2] * unit_r * ((x[mc_id * 2 + 1])**d)
                    terms.append(cp.deepcopy(term))
                insts.append(cp.deepcopy(terms))
            
            # first term in loglikelihood function
            first_term = 0 
            for inst in insts:
                first_term += inst[act]
            
            # second term
            second_term = 0
            for a in range(NUM_ACT):
                temp = 1
                for inst in insts:
                    if inst[a] > 709: inst[a] = 709 # prevent overflow
                    temp = temp * math.exp(inst[a])
                second_term += cp.deepcopy(temp)
            if second_term != 0:
                second_term = math.log(second_term) 
            
            logl = logl + cp.deepcopy(first_term) - cp.deepcopy(second_term)
        
        # l1 norm on w
        if self.sparse:
            delta = 0.25 # sparsity bias, requires tuning
            for i in range(NUM_MODULE): 
                logl = logl - delta * x[i * 2]

        data_file.close()
        obj = -logl
        # print("objective function constructed, one optimization iter completed >>>")
        return obj

    def optimize(self):
        # differential evolution
        # two modules the variables are x[0] = w0, x[1] = gamma0, x[2] = w1, x[3] = gamma1...
        x0 = []
        bound = []
        # initialization
        EST_REWARD = True
        if EST_REWARD:
            for i in range(NUM_MODULE):
                x0.append(0)
                x0.append(0.99)
                bound.append((0, None))
                bound.append((0.99,0.99)) #TODO can fix discount factor here, ow be (0.0, 0.99)
        else: # fix reward weights to be binary and estimate discount factors
            for i in range(NUM_MODULE):
                if self.task == 1:
                    if i == 0: x0.append(0)
                    elif i == 1: x0.append(0)
                    elif i == 2: x0.append(1)
                elif self.task == 2:
                    if i == 0: x0.append(0)
                    elif i == 1: x0.append(1)
                    elif i == 2: x0.append(1)
                elif self.task == 3:
                    if i == 0: x0.append(1)
                    elif i == 1: x0.append(0)
                    elif i == 2: x0.append(1)
                elif self.task == 4:
                    if i == 0: x0.append(1)
                    elif i == 1: x0.append(1)
                    elif i == 2: x0.append(1)
                x0.append(0.5)
                if self.task == 1:
                    if i == 0: bound.append((0, 0))
                    elif i == 1: bound.append((0, 0))
                    elif i == 2: bound.append((1, 1))
                elif self.task == 2:
                    if i == 0: bound.append((0, 0))
                    elif i == 1: bound.append((1, 1))
                    elif i == 2: bound.append((1, 1))
                elif self.task == 3:
                    if i == 0: bound.append((1, 1))
                    elif i == 1: bound.append((0, 0))
                    elif i == 2: bound.append((1, 1))
                elif self.task == 4:
                    if i == 0: bound.append((1, 1))
                    elif i == 1: bound.append((1, 1))
                    elif i == 2: bound.append((1, 1))
                bound.append((0.0,0.99))
        #print(x0)
        #print(bound)
        #print("begin minimization algorithm >>>")
        #return differential_evolution(self.construct_obj, bounds)
        #cons = [{'type':'ineq', 'fun': lambda x: x[4] - x[0]}, 
        #{'type':'ineq', 'fun': lambda x: x[4] - x[2]}, 
        #{'type':'ineq', 'fun': lambda x: x[6] - x[0]},          
        #{'type':'ineq', 'fun': lambda x: x[6] - x[2]}]
        #cons = [{'type':'eq', 'fun': lambda x: x[0] + x[2] + x[4] - 1}]
        #self.result = minimize(self.construct_obj, x0, method = 'SLSQP', bounds = bound, constraints = cons)['x']
        self.result = minimize(self.construct_obj, x0, method = 'SLSQP', bounds = bound).x # note: in python2, this should be ['x'] since it was dictionary, now it's a class
        self.result = self.result.tolist()
        print(self.result) 
        #print(self.result)
#        rranges = (slice(0,1,0.1), slice(0,0.99,0.1),slice(0,1,0.1), slice(0,0.99,0.1),slice(0,1,0.1), slice(0,0.99,0.1),slice(0,1,0.1), slice(0,0.99,0.1))
#        resbrute =  brute(self.construct_obj, rranges, full_output = True, finish = fmin)
#        return resbrute
    
    def write_result(self):
        out_file = open(self.out_filename, 'w')
        for result in self.result:
            out_file.write(str(result))
            out_file.write('\n')
        out_file.close()
        print("Results write to " + self.out_filename)

if __name__ == '__main__':
    test = inverse_rl(sys.argv[1], sys.argv[2]) # filename; sparse or not
    test.optimize()
    test.write_result()
 
