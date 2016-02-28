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
    if DISCRETE: return [int(pos[0] / CELL), int(pos[1] / CELL)]
    else: return pos

def move(agentPos, action):
    '''given action, calculate where agent lands'''
    if not(DISCRETE):
        CELL2 = float(CELL) / math.sqrt(2)
        if action == RIGHT: newPos = [agentPos[0] + CELL , agentPos[1]]
        elif action == UPRIGHT: newPos = [agentPos[0] + CELL2 , agentPos[1] - CELL2]
        elif action == UP: newPos = [agentPos[0], agentPos[1] - CELL]
        elif action == UPLEFT: newPos = [agentPos[0] - CELL2 , agentPos[1] - CELL2]
        elif action == LEFT: newPos = [agentPos[0] - CELL , agentPos[1]]
        elif action == DOWNLEFT: newPos = [agentPos[0] - CELL2, agentPos[1] + CELL2]
        elif action == DOWN: newPos = [agentPos[0], agentPos[1] + CELL]
        elif action == DOWNRIGHT: newPos = [agentPos[0] + CELL2, agentPos[1] + CELL2]
    else: # move into discrete positions
        UNIT = 1
        if action == RIGHT: newPos = [agentPos[0] + UNIT , agentPos[1]]
        elif action == UPRIGHT: newPos = [agentPos[0] + UNIT , agentPos[1] - UNIT]
        elif action == UP: newPos = [agentPos[0], agentPos[1] - UNIT]
        elif action == UPLEFT: newPos = [agentPos[0] - UNIT , agentPos[1] - UNIT]
        elif action == LEFT: newPos = [agentPos[0] - UNIT , agentPos[1]]
        elif action == DOWNLEFT: newPos = [agentPos[0] - UNIT, agentPos[1] + UNIT]
        elif action == DOWN: newPos = [agentPos[0], agentPos[1] + UNIT]
        elif action == DOWNRIGHT: newPos = [agentPos[0] + UNIT, agentPos[1] + UNIT]
    return newPos

def conseq(agentPos, objPos, action, threhold):
    '''given action, calculate the distance to the object after taken the action'''
    dist = calc_dist(move(agentPos, action), objPos)
    # if distance is within object threhold, treat this as 0
    if dist <= threhold: dist = 0
    return round(dist,ACC)

def calc_err(action1, action2):
    '''calculate the actions difference, in absolute value'''
    diff = abs(action1 - action2)
    if diff <= 4: return diff * 45 # degrees
    elif diff == 5: return 135
    elif diff == 6: return 90
    elif diff == 7: return 45
    else: print("angular diff calculation error") 

def facing(agentPos, angle, dist):
    '''return a vector that indicates agent's current facing angle'''
    newPos = [agentPos[0] + dist * math.sin(math.radians(angle)), agentPos[1] + dist * math.cos(math.radians(angle))]
    return newPos

def in_vcone(B, angle, A):
    '''give a obj's position (A) and agent's angle and pos (B), tell if obj is in visual cone or not'''
    if calc_dist(B,A) > VIS_DIST: return False
    C = facing(B, angle, 1)
    BA = [A[0] - B[0], A[1] - B[1]]
    BC = [C[0] - B[0], C[1] - B[1]]
    prod = BA[0] * BC[0] + BA[1] * BC[1]
    BA_norm = math.hypot(BA[0], BA[1])
    BC_norm = math.hypot(BC[0], BC[1])
    if BA_norm == 0: # object is really close to agent's position
        return True
    theta = math.copysign(1, BA[0]) * math.acos(prod / float(BA_norm * BC_norm)) # in radians
    theta = math.degrees(theta) # -180 ~ 180
    if -VIS_CONE <= theta <= VIS_CONE: return True
    else: return False

if __name__ == '__main__':
    #print(calc_bin(calc_angle([0,0], [1,1])))
    print(in_vcone([0,0], 182, [1,-1]))

