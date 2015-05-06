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

'''ModuleClass.py, flag for decideAct function'''
SOFTMAX_ACTION = True
ETA = 1
'''ModuleClass.py, flags for vote function'''
SUMQ = True
VOTE = False
SELECT = False

'''Test world'''
#Test Maze size
MAZE_ROW = 100
MAZE_COL = 100

#test trial numbers
MAX_STEP = 10000
MAX_TRIAL = 200
DRAW = False
MOUSE = False

'''Module Classes and Instances'''
NUM_MODULE_CLASS = 5
RAND_MODULE = True


'''Graphic visualization'''
#Maze cell size in pixel, everything else depends on this
CELL_SIZE = 30

'''IRL stuff'''
RECORDING = True
RECORD_FILENAME = "sparseTest3"


