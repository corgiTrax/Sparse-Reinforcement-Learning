import math
import copy as cp
from config import *

def calc_dist(posA, posB):
    '''euclidean distance'''
    return math.sqrt((posA[0] - posB[0]) ** 2 + (posA[1] - posB[1]) ** 2)

def calc_angle(posA, posB):
    '''find angle of an action'''
    x_diff = posB[0] - posA[0]; z_diff = posB[1] - posA[1]
    return math.degrees(math.atan2(z_diff, x_diff))

def calc_bin(angle):
    '''find the action according to the bin'''
    '''RIGHT: 0; UPRIGHT: -45; UP: -90; UPLEFT: -135; LEFT: 180; DOWNLEFT: 135; DOWN: 90; DOWNRIGHT: 45;'''
    halfbin = float(360) / (len(ACTIONS) - 1) / 2# do not count stay action, for 8 actions this should be 22.5 degrees
    if 0 - halfbin <= angle < 0 + halfbin: return RIGHT
    elif 45 - halfbin <= angle < 45 + halfbin: return DOWNRIGHT
    elif 90 - halfbin <= angle < 90 + halfbin: return DOWN
    elif 135 - halfbin <= angle < 135 + halfbin: return DOWNLEFT
    elif (180 - halfbin <= angle <= 180) or (-180 <= angle <= -180 + halfbin) : return LEFT
    elif -135 - halfbin <= angle < -135 + halfbin: return UPLEFT
    elif -90 - halfbin <= angle < -90 + halfbin: return UP
    elif -45 - halfbin <= angle < -45 + halfbin: return UPRIGHT

def tile(pos):
    '''given the float coordinates, calculate the discrete coordinate'''
    xd = int(pos[0] / CELL)
    zd = int(pos[1] / CELL)
    return xd, zd

def move(agentPos, action):
    '''given action, calculate where agent lands'''
    CELL2 = CELL / math.sqrt(2)
    if action == STAY: newPos = cp.deepcopy(agentPos)
    elif action == RIGHT: newPos = [agentPos[0] + CELL , agentPos[1]]
    elif action == UPRIGHT: newPos = [agentPos[0] + CELL2 , agentPos[1] - CELL2]
    elif action == UP: newPos = [agentPos[0], agentPos[1] - CELL]
    elif action == UPLEFT: newPos = [agentPos[0] - CELL2 , agentPos[1] - CELL2]
    elif action == LEFT: newPos = [agentPos[0] - CELL , agentPos[1]]
    elif action == DOWNLEFT: newPos = [agentPos[0] - CELL2, agentPos[1] + CELL2]
    elif action == DOWN: newPos = [agentPos[0], agentPos[1] + CELL]
    elif action == DOWNRIGHT: newPos = [agentPos[0] + CELL2 , agentPos[1] + CELL2]
    return newPos

def conseq(agentPos, objPos, action):
    '''given action, calculate the distance to the object after taken the action'''
    return int(round(calc_dist(move(agentPos, action), objPos) / CELL))

if __name__ == '__main__':
    print(calc_bin(calc_angle([0,0], [1,1])))


