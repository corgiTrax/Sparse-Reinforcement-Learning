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
SHOW_GRID = False
DISCRETE = False
EXCLUDE = SIZE * 1 # exclude data that are too close to start/elevator 
#WAY_POINT_PASS_THRESHOLD = 0.3 * SIZE
CELL = int(SIZE * 0.7) # state granularity
PATH_SIZE = 0 * SIZE # for IRL landing distance, if gets into this range, the distance is 0.
VIS_CONE = 58 # degrees; visual cone range on one side
VIS_DIST = 10 * SIZE # visual cone radius
#0.7, 0, 58, 10

VIS = False; MOUSE = VIS # visualize or not
# actions
EIGHT_ACTIONS = False
if EIGHT_ACTIONS:
    LEFT = 0; UPLEFT = 1; UP = 2; UPRIGHT = 3
    RIGHT = 4; DOWNRIGHT = 5; DOWN = 6; DOWNLEFT = 7
    ACTIONS = [LEFT, UPLEFT, UP, UPRIGHT, RIGHT, DOWNRIGHT, DOWN, DOWNLEFT]
    ACT_NAMES = ["LEFT", "UPLEFT", "UP", "UPRIGHT", "RIGHT", "DOWNRIGHT", "DOWN", "DOWNLEFT"]
else:
    L = 0; LLU = 1; LU = 2; LUU = 3; U = 4; UUR = 5; UR = 6; URR = 7; R = 8;
    RRD = 9; RD = 10; RDD = 11; D = 12; DDL = 13; DL = 14; DLL = 15
    ACTIONS = [L, LLU, LU, LUU, U, UUR, UR, URR, R, RRD, RD, RDD, D, DDL, DL, DLL]
    ACT_NAMES = ["LEFT", "LEFT LEFT UP", "LEFT UP", "LEFT UP UP", "UP", "UP UP RIGHT", "UP RIGHT", "UP RIGHT RIGHT", "RIGHT",\
"RIGHT RIGHT DOWN", "RIGHT DOWN", "RIGHT DOWN DOWN", "DOWN", "DONW DOWN LEFT", "DONW LEFT", "DOWN LEFT LEFT"]

NUM_ACT = len(ACTIONS)
NUM_MODULE = 3
ELEVATOR = False
VISCONE = True
PATH_LOOKAHEAD = False
NUM_PATH_LOOKAHEAD = 3
THROW_OUT = 2 # throw out bad ones
