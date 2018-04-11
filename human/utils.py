import math
import copy as cp
from config import *
import numpy as np

def calc_dist(posA, posB):
    '''euclidean distance'''
    return math.sqrt((posA[0] - posB[0]) ** 2 + (posA[1] - posB[1]) ** 2)

def calc_angle(posA, posB):
    '''find angle of an action: -180 ~ 180'''
    x_diff = posB[0] - posA[0]; z_diff = posB[1] - posA[1]
    return math.degrees(math.atan2(z_diff, x_diff))

def calc_bin(angle):
    '''find the action according to the bin'''
    '''RIGHT: 0; UPRIGHT: -45; UP: -90; UPLEFT: -135; LEFT: 180; DOWNLEFT: 135; DOWN: 90; DOWNRIGHT: 45;'''
    halfbin = float(360) / (len(ACTIONS)) / 2
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
        print("16 actions version not supported.")
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
    if BA_norm * BC_norm == 0: return 0 # ??
    temp = min(1, prod / float(BA_norm * BC_norm))
    theta = math.copysign(1, BA[0]) * math.acos(temp) # in radians
    theta = math.degrees(theta) # -180 ~ 180
    return abs(theta) 

def calc_err_actual2(agentPosNext, agentPos, predPos):
    '''calculate the absolute angular difference between predicted position and next position'''
    B = agentPos
    C = predPos
    A = agentPosNext
    BA = [A[0] - B[0], A[1] - B[1]]
    BC = [C[0] - B[0], C[1] - B[1]]
    prod = BA[0] * BC[0] + BA[1] * BC[1]
    BA_norm = math.hypot(BA[0], BA[1])
    BC_norm = math.hypot(BC[0], BC[1])
    if BA_norm * BC_norm == 0: return 0 # ??
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
    '''this angle is in 360 degrees range?'''
    if VISCONE:
        if calc_dist(B,A) > VIS_DIST: return False
        else: return True
  #      C = facing(B, angle, 1)
  #      BA = [A[0] - B[0], A[1] - B[1]]
  #      BC = [C[0] - B[0], C[1] - B[1]]
  #      prod = BA[0] * BC[0] + BA[1] * BC[1]
  #      BA_norm = math.hypot(BA[0], BA[1])
  #      BC_norm = math.hypot(BC[0], BC[1])
  #      if BA_norm == 0: # object is really close to agent's position
  #          return True
  #      theta = math.copysign(1, BA[0]) * math.acos(prod / float(BA_norm * BC_norm)) # in radians
  #      theta = math.degrees(theta) # -180 ~ 180
  #      if -VIS_CONE <= theta <= VIS_CONE: return True
  #      else: return False
    else: return True

def to360(angle):
    '''calc_angle result is in current world frame, but angentAngle from .mat file is using a different coordinate frame'''
    if angle < 0: angle = angle + 360
    angle = 360 - angle 
    return (angle + 90) % 360

def nearest_obj(agentPos, objs):
    '''return the index of nearest object'''
    dists = np.zeros(len(objs))
    for i, obj in enumerate(objs):
        dists[i] = calc_dist(agentPos, obj)
    return np.argmin(dists)

# if using elevator, save for future
#def acc_dists(objs, index, order):
#    '''return accumulated distance of a list of objects, starting at an index'''
#
#
#def dist_elev(agentPos, paths, elevPos, lastPath):
#    '''calculate the distance (along path only) to elevator, and the current way point'''
#    if paths.index(elevPos) == 0: 
#        curPath = len(paths) - 1
#
#    else:
#        nearest_path = nearest_obj(agentPos, paths)
#        if nearest_path >= lastPath + 2: # cannot skip more than 2 paths
#            curPath = lastPath
#        else: pass
#    return dist,curPath

def point_on_line(pos1, pos2, pos3):
    '''return if pos3 is on line segment btw pos1 and pos2. Threshold: tolerance'''
    thresh = 1e-4 # meters
    return abs(calc_dist(pos1, pos2) - (calc_dist(pos1, pos3) + calc_dist(pos2, pos3))) <= thresh 

def intersect_circle(pos1, pos2, c_pos, r):
    '''determine if a circle with c_pos and radius r intersects a line segement btw pos1, pos2'''
    # pos needs to be transformed so circle is at (0,0)
    x1, y1, x2, y2 = pos1[0] - c_pos[0], pos1[1] - c_pos[1], pos2[0] - c_pos[0], pos2[1] - c_pos[1]
    if x1 == x2 and y1 == y2: 
        return calc_dist([x1,y1], [0,0]) <= r 
    dx = x2 - x1
    dy = y2 - y1
    dr = math.sqrt(dx**2 + dy**2)
    D = x1 * y2 - x2 * y1
    sign = -1 if dy < 0 else 1

    delta = r**2 * (dr**2) - D**2
    if delta < 0: return False
    if delta == 0: # one intersection
        x = D * dy / (dr**2)
        y = -D * dx / (dr**2)
        return point_on_line([x1,y1], [x2,y2], [x,y])
    if delta > 0: 
        x_1 = (D * dy + sign * dx * math.sqrt(delta)) / (dr**2)
        y_1 = (-D * dx + abs(dy) * math.sqrt(delta)) / (dr**2) 
        x_2 = (D * dy - sign * dx * math.sqrt(delta)) / (dr**2)
        y_2 = (-D * dx - abs(dy) * math.sqrt(delta)) / (dr**2)
        return point_on_line([x1,y1], [x2,y2], [x_1,y_1]) or point_on_line([x1,y1], [x2,y2], [x_2,y_2])



''' See https://www.geeksforgeeks.org/orientation-3-ordered-points for details of below formula for line-line intersection'''
def onSegment(p, q, r):
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        return True
    return False

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]);
    if val == 0: return 0  # colinear
    return 1 if val > 0 else 2

def doIntersect(line1, line2):
    p1, q1 = line1[0], line1[1]
    p2, q2 = line2[0], line2[1]
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2 and o3 != o4):
        return True
    if (o1 == 0 and onSegment(p1, p2, q1)): return True
    if (o2 == 0 and onSegment(p1, q2, q1)): return True
    if (o3 == 0 and onSegment(p2, p1, q2)): return True
    if (o4 == 0 and onSegment(p2, q1, q2)): return True
 
    return False 
 
def intersect_square(pos1, pos2, s_pos, r):
    '''determine if a square with s_pos as center and r as half width intersects a line segment btw pos1, pos2'''
    ul = [s_pos[0] - r, s_pos[1] - r]
    ur = [s_pos[0] - r, s_pos[1] + r]
    ll = [s_pos[0] + r, s_pos[1] - r]  
    lr = [s_pos[0] + r, s_pos[1] + r]    
    base = [pos1, pos2]
    return doIntersect(base, [ul, ur]) or doIntersect(base, [ul, ll]) or doIntersect(base, [ur, lr]) or doIntersect(base, [ll, lr])

if __name__ == '__main__':
    #print(calc_bin(calc_angle([0,0], [1,1])))
    #print(in_vcone([0,0], 182, [1,-1]))
    #print(get_angle([0,1], [1,0]))
    #print(calc_err_actual([1,1], [0,0], L))
    print(nearest_obj([0,0],[[0,1],[2,0],[3,3],[0,0.5]]))
