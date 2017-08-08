# actions
L = 0; LLU = 1; LU = 2; LUU = 3; U = 4; UUR = 5; UR = 6; URR = 7; R = 8;
RRD = 9; RD = 10; RDD = 11; D = 12; DDL = 13; DL = 14; DLL = 15
ACTIONS = [L, LLU, LU, LUU, U, UUR, UR, URR, R, RRD, RD, RDD, D, DDL, DL, DLL]
ACT_NAMES = ["LEFT", "LEFT LEFT UP", "LEFT UP", "LEFT UP UP", "UP", "UP UP RIGHT", "UP RIGHT", "UP RIGHT RIGHT", "RIGHT",\
"RIGHT RIGHT DOWN", "RIGHT DOWN", "RIGHT DOWN DOWN", "DOWN", "DONW DOWN LEFT", "DONW LEFT", "DOWN LEFT LEFT"]
NUM_ACT = len(ACTIONS)
MIRL, RANDOM, BINARY_R, GAMMA05, GAMMA099, GAMMA01 = 0,1,2,3,4,5
AGENT = GAMMA01 #TODO

# environment parameters
SIZE = 10
ACC = 0 # rounding accuracy
FACTOR = 10 # when visualize need to enlarge
ROOM_X = 8.534 * SIZE
ROOM_Z = 7.315 * SIZE
OFF_X = ROOM_X/2
OFF_Z = ROOM_Z/2
TAR_SIZE = 0.2134 * SIZE #0.1524 * SIZE # radius
OBS_SIZE = 0.1753 * SIZE
AGENT_SIZE = 0.05 * SIZE
FONT_SIZE = SIZE / 10 
#WAY_POINT_PASS_THRESHOLD = 0.3 * SIZE
# VIS_CONE = 58 # 58 degrees; visual cone range on one side
#ARR_DIST = 0.2 * SIZE

# visualization parameters
VIS = False; MOUSE = VIS # visualize or not
SHOW_GRID = False
PILG = True # use PIL or graphics.py for visualization
ALPHA = 8 # range 0~255, controls opacity of the trajectory
TRAJ_WID = 3 # width of fitted trajectories

# adjustable parameters
NUM_MODULE = 3
ELEVATOR = False
VISCONE = True # using distance now only
# PATH_LOOKAHEAD = False

DISCRETE = False

SOFTMAX_ACT = True # for free run only
TAU = 1 # temperature parameter for softmax selection
NUM_TRAJ = 200
MAX_STEP = 80 # do not exceed this, ow abandon current trial

# tuning
SUBJ_DIC = [26,27,28,31,32,33,34,35,36,37,38,39,42,43,44,45,46,47,48,54,56,59,61,63,64]
SUBJ = 27
VECS = [
[0.4,	5,	4,	5,	0.5],
[0.5,	5,	5,	3,	0.6,    0.0],
[0.4,	1.5,	8,	4,	0.6],
[0.6,	1.5,	4,	5,	0.9],
[0.5,	2,	4,	4,	0.5],
[0.8,	2.5,	8,	6,	0.8],
[0.6,	1,	6,	2,	0.6],
[0.5,	0.5,	6,	7,	0.6,    0.6],
[0.7,	5,	6,	5,	0.6],
[0.8,	4,	6,	7,	0.7],
[0.5,	5,	5,	6,	0.5],
[0.5,	6,	5,	5,	0.6],
[0.5,	1.5,	4,	3,	0.4],
[0.6,	3,	9,	5,	0.5,    0.1],
[0.6,	3,	6,	5,	0.5],
[0.6,	4,	5,	5,	0.5],
[0.5,	1,	5,	2,	0.6,    0.0],
[0.7,	4,	4,	3,	0.6],
[0.4,	2.5,	6,	7,	0.6],
[0.6,	3,	4,	5,	0.6],
[0.6,	4,	7,	8,	0.7],
[0.6,	5,	5,	3,	0.7],
[0.6,	5,	5,	8,	0.7],
[0.5,	4,	4,	3,	0.5],
[0.7,	4,	4,	5,	0.6]]
#VEC = VECS[SUBJ_DIC.index(SUBJ)]
# 0.572, 50, 5, 5, 0.6, 0
VEC = [0.572, 50, 5, 5, 0.6, 0.0] # 3.32 for the second one, on average, put 50 for infinite distance
CELL = int(SIZE * VEC[0]) # state granularity
VIS_DIST = VEC[1] * SIZE # visual cone radius
NUM_PATH_LOOKAHEAD = VEC[2]
SKIP_THRESH = VEC[3]
EXCLUDE = VEC[4] * SIZE #0.5 * SIZE for plotting  # exclude data that are too close to start/elevator, only for fitting, when generating traj should be 0 
PATH_SIZE = VEC[5] * SIZE # for IRL landing distance, if gets into this range, the distance is 0.

