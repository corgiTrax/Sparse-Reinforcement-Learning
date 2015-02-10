'''config file'''

import random
import numpy
import copy as py_copy
import graphics as cg
import math

#State index
ROW = 0
COL = 1

#Actions for agent
NUM_ACT = 4
UP = 0; DOWN = 1; LEFT = 2; RIGHT = 3;
ACTIONS = [UP,DOWN,LEFT,RIGHT]

'''Reinforcement learning paramters'''
R_PRIZE = 10
GAMMA_PRIZE = 0.9

R_OBS = -10 
GAMMA_OBS = 0

R_PRED = -100 
GAMMA_PRED = 0.1


'''ModuleClass.py, flag for decideAct function'''
SOFTMAX_ACTION = True
'''ModuleClass.py, flags for vote function'''
SUMQ = True
VOTE = False
SELECT = False

'''Test world'''
#Obstacle and price probabilities
P_OBS = 0.0
P_PRIZE = 0.1

NUM_PREDATOR = 1
P_CHASE = P_OBS #actually, see implementation
P_PRED_RAND = 1 - P_CHASE

#Test Maze size
TESTR = 9
TESTC = 9
MAX_STEP = 500

#test trial numbers
MAX_TRIAL = 200
DRAW = True
MOUSE = False

#Graphic visualization
#Maze cell size in pixel, everything else depends on this
CELL_SIZE = 30



