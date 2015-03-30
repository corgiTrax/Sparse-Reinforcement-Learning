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
R_PRIZE = 0
GAMMA_PRIZE = 0

R_OBS = -10
GAMMA_OBS = 0.3

R_PRED = -100 
GAMMA_PRED = 0.1


'''ModuleClass.py, flag for decideAct function'''
SOFTMAX_ACTION = True
'''ModuleClass.py, flags for vote function'''
SUMQ = True
VOTE = False
SELECT = False

'''Test world'''
#Index
PRIZE = 0
OBS = 1
PRED = 2

#Obstacle and price probabilities
P_OBS = 0.1
P_PRIZE = 0.2

NUM_PREDATOR = 0
P_CHASE = P_OBS #actually, see implementation
P_PRED_RAND = 1 - P_CHASE

#Test Maze size
TESTR = 5
TESTC = 5
MAX_STEP = 100

#test trial numbers
MAX_TRIAL = 200
DRAW = False
MOUSE = False

#Graphic visualization
#Maze cell size in pixel, everything else depends on this
CELL_SIZE = 30

'''IRL stuff'''
RECORDING = True
RECORD_FILENAME = "sparseTest3"

ETA = 1
