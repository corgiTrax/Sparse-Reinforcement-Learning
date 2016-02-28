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
CELL = int(SIZE * 0.6) # state granularity
PATH_SIZE = 0 * SIZE # for IRL landing distance, if gets into this range, the distance is 0.
VIS_CONE = 58 # degrees; visual cone range on one side
VIS_DIST = 10 * SIZE # visual cone radius
#0.5, 0.1, 55, 4

VIS = False; MOUSE = VIS # visualize or not
# actions
LEFT = 0; UPLEFT = 1; UP = 2; UPRIGHT = 3
RIGHT = 4; DOWNRIGHT = 5; DOWN = 6; DOWNLEFT = 7
ACTIONS = [LEFT, UPLEFT, UP, UPRIGHT, RIGHT, DOWNRIGHT, DOWN, DOWNLEFT]
ACT_NAMES = ["LEFT", "UPLEFT", "UP", "UPRIGHT", "RIGHT", "DOWNRIGHT", "DOWN", "DOWNLEFT"]
NUM_ACT = len(ACTIONS)
NUM_MODULE = 3
ELEVATOR = False
