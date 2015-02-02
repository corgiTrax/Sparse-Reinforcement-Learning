#Module class
#Modular RL Project
#Ruohan Zhang
#Module classes

import random
import mathtool
import numpy
import copy as py_copy
import config

ROW = config.ROW
COL = config.COL

#Key function here: measure the consensus of actions
#This function should capture two things
#1. How much is the expected reward (signaled by learned value, related to reward when training)
#2. at this state, indifference level on actions?
def calc_weight(Qvalues):
    #standard deviation, for discrete actions
    return mathtool.calc_sd(Qvalues)

#Another key function here: voting
#Input are all modules (regardless of types)
def vote(modules):
    #Count the total weight of all actions
    scoreCount = numpy.zeros(config.NUM_ACT)   

    #Method 1: Russell and Zimdars: Q-decomposition: sum Q values of all modules
    if (config.SUMQ == True):
        for i in range(len(modules)):
            for act in range(config.NUM_ACT):
                scoreCount[act] += modules[i].Qvalues[act]

    #Method 2: each module votes standard deviation (weight) of Q values over actions
    if (config.VOTE == True):
        for i in range(len(modules)):
            scoreCount[modules[i].optimalAct] += modules[i].weight

    #Method 3: choose the module with highest weight (standard deviation), and choose its optimal action
    if (config.ONE_WINNER == True):
        maxWeight = 0
        chosenModule = 0
        for i in range(len(modules)):
            if (modules[i].weight >= maxWeight):
                maxWeight = modules[i].weight
                chosenModule = i
        scoreCount[modules[chosenModule].optimalAct] = 10

    return scoreCount

#Find action with highest accumulated weight
def decideAct(scoreCount):
    softmaxFlag = config.SOFTMAX_ACTION
    #Method 1: Choosing the action with highest score Count
    if (softmaxFlag == False):
        act = 0
        score = scoreCount[0]
        for i in range(len(scoreCount)):
            if (scoreCount[i] == score):
                if (random.random() >= 0.5):
                    act = i
                    score = scoreCount[i]
            if (scoreCount[i] > score):
    	        act = i
    	        score = scoreCount[i]
      
    #Method 2: Choosing actions with softmax probability(roulette, but this is questionable, since it is a randomized algorithm)
    if (softmaxFlag == True):
        act = mathtool.roulette(scoreCount)

    return act   


#Class module
class Module:
    def __init__(self,Qtable,state):
        self.state = py_copy.deepcopy(state)
        self.Qtable = py_copy.deepcopy(Qtable)
        #Q values for actions under current state
        self.Qvalues = py_copy.deepcopy(Qtable[state[0]][state[1]])
        self.weight = calc_weight(self.Qvalues)
        self.optimalAct = mathtool.optimalActionSelect(Qtable,state,config.NUM_ACT)
