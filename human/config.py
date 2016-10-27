# actions
L = 0; LLU = 1; LU = 2; LUU = 3; U = 4; UUR = 5; UR = 6; URR = 7; R = 8;
RRD = 9; RD = 10; RDD = 11; D = 12; DDL = 13; DL = 14; DLL = 15
ACTIONS = [L, LLU, LU, LUU, U, UUR, UR, URR, R, RRD, RD, RDD, D, DDL, DL, DLL]
ACT_NAMES = ["LEFT", "LEFT LEFT UP", "LEFT UP", "LEFT UP UP", "UP", "UP UP RIGHT", "UP RIGHT", "UP RIGHT RIGHT", "RIGHT",\
"RIGHT RIGHT DOWN", "RIGHT DOWN", "RIGHT DOWN DOWN", "DOWN", "DONW DOWN LEFT", "DONW LEFT", "DOWN LEFT LEFT"]
NUM_ACT = len(ACTIONS)
MIRL, RANDOM, REFLEX = 0,1,2
AGENT = MIRL

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
PATH_SIZE = 0 * SIZE # for IRL landing distance, if gets into this range, the distance is 0.
# VIS_CONE = 58 # 58 degrees; visual cone range on one side

# visualization parameters
VIS = False; MOUSE = VIS # visualize or not
SHOW_GRID = False
PILG = True # use PIL or graphics.py for visualization
ALPHA = 40 # range 0~255, controls opacity of the trajectory
TRAJ_WID = 3 # width of fitted trajectories

# adjustable parameters
NUM_MODULE = 3
ELEVATOR = False
VISCONE = True # using distance now only
# PATH_LOOKAHEAD = False

DISCRETE = False

SOFTMAX_ACT = True # for free run only
TAU = 1.5 # temperature parameter for softmax selection
NUM_TRAJ = 0
MAX_STEP = 1000 # do not exceed this, ow abandon current trial

# tuning
VEC = [0.5, 6, 5, 5, 0.6]
CELL = int(SIZE * VEC[0]) # state granularity
VIS_DIST = VEC[1] * SIZE # visual cone radius
NUM_PATH_LOOKAHEAD = VEC[2]
SKIP_THRESH = VEC[3]
EXCLUDE = SIZE * VEC[4] # exclude data that are too close to start/elevator 
