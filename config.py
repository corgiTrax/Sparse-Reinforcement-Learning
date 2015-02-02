'''config file'''

import random
import numpy
import copy as py_copy
import graphics as cg
import math

######## Globals
#State index
ROW = 0
COL = 1

#Actions for agent
NUM_ACT = 4
Up = 0; Down = 1; Left = 2; Right = 3;
ACTIONS = [Up,Down,Left,Right]
#Special action for predator, since agent move first, if it moves into predator, predator should stay
Stay = 5

######## Reinforcement learning paramters
#!!!Notice VRANGE now has to be odd, see reinforcement.stateMapping()
#Vision range for prices(Module 1)
VRANGE_M1 = 9
#Size of M1 Q table
MAX_ROW_M1 = VRANGE_M1 * 2 + 1
MAX_COL_M1 = VRANGE_M1 * 2 + 1
#Training maze size (we partition state space into 4 parts to allow more efficient training)
TMAZE_SIZE_M1 = VRANGE_M1 + 1
#Reward
R_PRICE = 10
GAMMA_M1 = 0.7
#Training parameters
#ALPHA_M1 = 0.6
NUM_EPISODE_M1 = 100
MAX_STEP_EACH_EPISODE_M1 = 100
#EPSILON_M1 = 0.95
#Eligibility traces
LAMBDA_M1 = 0.8

#Vision range for obstacles(Module 2), 3 means (0,0) can see (3,3)
VRANGE_M2 = 9
#Size of M2 Q tables
MAX_ROW_M2 = VRANGE_M2 * 2 + 1
MAX_COL_M2 = VRANGE_M2 * 2 + 1
TMAZE_SIZE_M2 = VRANGE_M2 + 1
R_OBSTACLE = -10 
GAMMA_M2 = 0.0
#ALPHA_M2 = 0.6
NUM_EPISODE_M2 = 10
MAX_STEP_EACH_EPISODE_M2 = 100
#EPSILON_M2 = 0.5
LAMBDA_M2 = 0.8

#Vision range for predator(Module 3), 3 means (0,0) can see (3,3)
VRANGE_M3 = 3
#Size of M2 Q tables
MAX_ROW_M3 = VRANGE_M3 * 2 + 1
MAX_COL_M3 = VRANGE_M3 * 2 + 1
TMAZE_SIZE_M3 = VRANGE_M3 + 1
R_PREDATOR = -100 
GAMMA_M3 = 0.0
#ALPHA_M3 = 0.5
NUM_EPISODE_M3 = 20
MAX_STEP_EACH_EPISODE_M3 = 100
#EPSILON_M3 = 0.9
LAMBDA_M3 = 0.9

#Reward for empty slot
R_EMPTY = 0

#Training Method
SARSA_ET = True
Q_ET = False


########## Test parameters
#Action selection parameters
#Main.py, attention mechanism
NEAREST_PRICE_ONLY = False
#this VRANGE is for actual navigation, altough agent is trained to see VRANGE_M1, it does not need to see that far
TEST_VRANGE_M1 = 9
TEST_VRANGE_M2 = 9
TEST_VRANGE_M3 = 3
#ModuleClass.py, flag for decideAct function
SOFTMAX_ACTION = True
#ModuleClass.py, flags for vote function
SUMQ = True
VOTE = False
ONE_WINNER = False

#Test maze
#Obstacle and price probabilities
pObstacle = 0.2
pPrice = 0.3
#Probability of
NUM_PREDATOR = 3
P_PREDATOR_CHASE = 0.5 #actually, see implementation
P_PREDATOR_RANDOM_ACT = 1 - P_PREDATOR_CHASE

#Test Maze size
TESTR = 10
TESTC = 20
MAX_STEP = 1000

#test trial numbers
MAX_TRIAL = 1
DRAW = False
MOUSE = False
if (MAX_TRIAL == 1):
    DRAW = True
    MOUSE = False


#Graphic visualization
#Maze cell size in pixel, everything else depends on this
CELL_SIZE = 30



