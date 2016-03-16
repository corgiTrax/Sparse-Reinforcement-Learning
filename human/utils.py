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
    halfbin = float(360) / (len(ACTIONS)) / 2
    if EIGHT_ACTIONS: # bin size is 45
        if 0 - halfbin <= angle < 0 + halfbin: return RIGHT
        elif 45 - halfbin <= angle < 45 + halfbin: return DOWNRIGHT
        elif 90 - halfbin <= angle < 90 + halfbin: return DOWN
        elif 135 - halfbin <= angle < 135 + halfbin: return DOWNLEFT
        elif (180 - halfbin <= angle <= 180) or (-180 <= angle <= -180 + halfbin) : return LEFT
        elif -135 - halfbin <= angle < -135 + halfbin: return UPLEFT
        elif -90 - halfbin <= angle < -90 + halfbin: return UP
        elif -45 - halfbin <= angle < -45 + halfbin: return UPRIGHT
    else: # 16 actions, bin size is 22.5
        if 0 - halfbin <= angle < 0 + halfbin: return R
        elif 22.5 - halfbin <= angle < 22.5 + halfbin: return RRD 
        elif 45 - halfbin <= angle < 45 + halfbin: return RD
        elif 67.5 - halfbin <= angle < 67.5 + halfbin: return RDD
        elif 90 - halfbin <= angle < 90 + halfbin: return D
        elif 112.5 - halfbin <= angle < 112.5 + halfbin: return DDL
        elif 135 - halfbin <= angle < 135 + halfbin: return DL
        elif 157.5 - halfbin <= angle < 157.5 + halfbin: return DLL
        elif (180 - halfbin <= angle <= 180) or (-180 <= angle <= -180 + halfbin) : return L
        elif -157.5 - halfbin <= angle < -157.5 + halfbin: return LLU
        elif -135 - halfbin <= angle < -135 + halfbin: return LU
        elif -112.5 - halfbin <= angle < -112.5 + halfbin: return LUU
        elif -90 - halfbin <= angle < -90 + halfbin: return U
        elif -67.5 - halfbin <= angle < -67.5 + halfbin: return UUR
        elif -45 - halfbin <= angle < -45 + halfbin: return UR
        elif -22.5 - halfbin <= angle < -22.5 + halfbin: return URR

def tile(pos):
    '''given the float coordinates, calculate the discrete coordinate'''
    if DISCRETE: return [int(pos[0] / CELL), int(pos[1] / CELL)]
    else: return pos

def move(agentPos, action):
    '''given action, calculate where agent lands'''
    if not(DISCRETE):
        if EIGHT_ACTIONS:
            MED = CELL * 0.70711
            if action == RIGHT: newPos = [agentPos[0] + CELL , agentPos[1]]
            elif action == UPRIGHT: newPos = [agentPos[0] + MED , agentPos[1] - MED]
            elif action == UP: newPos = [agentPos[0], agentPos[1] - CELL]
            elif action == UPLEFT: newPos = [agentPos[0] - MED , agentPos[1] - MED]
            elif action == LEFT: newPos = [agentPos[0] - CELL , agentPos[1]]
            elif action == DOWNLEFT: newPos = [agentPos[0] - MED, agentPos[1] + MED]
            elif action == DOWN: newPos = [agentPos[0], agentPos[1] + CELL]
            elif action == DOWNRIGHT: newPos = [agentPos[0] + MED, agentPos[1] + MED]
        else:
            SHORT = CELL * 0.38268; LONG = CELL * 0.92388 # sin and cos values for 22.5 degrees
            MED = CELL * 0.70711 # sin and cos of 45 degrees
            if action == R: newPos = [agentPos[0] + CELL , agentPos[1]]
            elif action == URR: newPos = [agentPos[0] + LONG, agentPos[1] - SHORT]
            elif action == UR: newPos = [agentPos[0] + MED , agentPos[1] - MED]
            elif action == UUR: newPos = [agentPos[0] + SHORT, agentPos[1] - LONG]
            elif action == U: newPos = [agentPos[0], agentPos[1] - CELL]
            elif action == LUU: newPos = [agentPos[0] - SHORT, agentPos[1] - LONG]
            elif action == LU: newPos = [agentPos[0] - MED , agentPos[1] - MED]
            elif action == LLU: newPos = [agentPos[0] - LONG, agentPos[1] - SHORT]
            elif action == L: newPos = [agentPos[0] - CELL , agentPos[1]]
            elif action == DLL: newPos = [agentPos[0] - LONG, agentPos[1] + SHORT] 
            elif action == DL: newPos = [agentPos[0] - MED, agentPos[1] + MED]
            elif action == DDL: newPos = [agentPos[0] - SHORT, agentPos[1] + LONG] 
            elif action == D: newPos = [agentPos[0], agentPos[1] + CELL]
            elif action == RDD: newPos = [agentPos[0] + SHORT, agentPos[1] + LONG]
            elif action == RD: newPos = [agentPos[0] + MED, agentPos[1] + MED]
            elif action == RRD: newPos = [agentPos[0] + LONG, agentPos[1] + SHORT]

    else: # move into discrete positions
        if EIGHT_ACTIONS:
            UNIT = 1
            if action == RIGHT: newPos = [agentPos[0] + UNIT , agentPos[1]]
            elif action == UPRIGHT: newPos = [agentPos[0] + UNIT , agentPos[1] - UNIT]
            elif action == UP: newPos = [agentPos[0], agentPos[1] - UNIT]
            elif action == UPLEFT: newPos = [agentPos[0] - UNIT , agentPos[1] - UNIT]
            elif action == LEFT: newPos = [agentPos[0] - UNIT , agentPos[1]]
            elif action == DOWNLEFT: newPos = [agentPos[0] - UNIT, agentPos[1] + UNIT]
            elif action == DOWN: newPos = [agentPos[0], agentPos[1] + UNIT]
            elif action == DOWNRIGHT: newPos = [agentPos[0] + UNIT, agentPos[1] + UNIT]
        else: print("16 actions version not supported.")
    return newPos

def conseq(agentPos, objPos, action, threhold):
    '''given action, calculate the distance to the object after taken the action'''
    dist = calc_dist(move(agentPos, action), objPos)
    # if distance is within object threhold, treat this as 0
    if dist <= threhold: dist = 0
    return round(dist,ACC)

def calc_err_actual(agentPosNext, agentPos, action):
    '''calculate the absolute angular difference between predicted action and next position'''
    B = agentPos
    C = move(agentPos, action)
    A = agentPosNext
    BA = [A[0] - B[0], A[1] - B[1]]
    BC = [C[0] - B[0], C[1] - B[1]]
    prod = BA[0] * BC[0] + BA[1] * BC[1]
    BA_norm = math.hypot(BA[0], BA[1])
    BC_norm = math.hypot(BC[0], BC[1])
    temp = min(1, prod / float(BA_norm * BC_norm))
    theta = math.copysign(1, BA[0]) * math.acos(temp) # in radians
    theta = math.degrees(theta) # -180 ~ 180
    return abs(theta) 

def facing(agentPos, angle, dist):
    '''return a pos that indicates agent's current facing angle'''
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
    #print(in_vcone([0,0], 182, [1,-1]))
    print(get_angle([0,1], [1,0]))
    #print(calc_err_actual([1,1], [0,0], L))
