'''A roulette action selector'''
import math
import random
import copy as cp
import numpy
from config import *

class Roulette:
    ''' input: a weight vector, not necessarily normalized'''
    def __init__(self, weight):
        self.weight = cp.deepcopy(weight)
        self.num_actions = len(self.weight)
        # softmax version
#        total_weight = 0
#        for i,q in enumerate(self.weight):
#            temp = math.exp(q / float(TAU))
#            self.weight[i] = temp
#            total_weight += temp
        # proportional version        
        #normalize, get probability for each action
        total_weight = 0
        for i in range(self.num_actions):
            total_weight += self.weight[i]

        for i in range(self.num_actions):
            self.weight[i] = 1.0 * self.weight[i] / total_weight

    def select(self):
        '''return an index that proportional to its probability'''
        #calc cumulative probability
        cum_prob = numpy.zeros(self.num_actions + 1)
        cum_prob[0] = 0
        for i in range(self.num_actions):
            cum_prob[i+1] = cum_prob[i] + self.weight[i]
        
        #random seed
        seed = random.random()
        for i in range(self.num_actions):
            if (seed >= cum_prob[i] and seed < cum_prob[i+1]):
                action = i

        return action

if __name__ == '__main__':
    roul = Roulette([1,2,3,4,5,6])
    print(roul.weight)
    count = numpy.zeros(roul.num_actions)
    for i in range(1000000):
        count[roul.select()] += 1
    print(count)
