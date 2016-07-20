'''Environment'''
import re
import copy as cp
import graphics as cg
import math
from config import *
import utils
import sys
import numpy as np

np.set_printoptions(precision = 3, suppress = True, linewidth = 1000, threshold = 'nan')

class Trial:
    def __init__(self, filename):
        '''read in all objects from data_file and their positions'''
        ''' positions are translated to the new coordinate system by adding OFF_X and OFF_Z, 
        where (0,0) is at upperleft corner instead of at the center; coordinates are translated by * SIZE as well'''
        self.agents = []; self.agentAngles = []; self.targets = []; self.obsts = []; self.paths = []; self.elevs = []
        self.allTargets = []; self.allObsts = []; self.allElevs = []

        data_file = open(filename,'r')
        self.file_continuous = filename
        for lineNum, line in enumerate(data_file): # each line is a time step
            fields = re.split('#|\n', line)
            # agent
            curAgent = [] 
            agentField = fields[1]
            agentX, agentZ, agentAngle = agentField.split(',')
            agentX = float(agentX) * SIZE + OFF_X; agentZ = float(agentZ) * SIZE + OFF_Z
            curAgent.append([agentX, agentZ])
            agentPos = [agentX, agentZ]
            self.agents.append(cp.deepcopy(curAgent))
            agentAngle = float(agentAngle)
            # agentAngle = utils.to360(utils.calc_angle(agentPos, agentPosNext))
            self.agentAngles.append(agentAngle)

            # targets
            curAllTargets = []
            curTargets = [] # stores all target visible at this time step
            targetField = fields[2]
            targets = targetField.split(';')
            for i in range(len(targets) - 1): # last one is empty
                targetX, targetZ = targets[i].split(',')
                targetX = float(targetX) * SIZE + OFF_X; targetZ = float(targetZ) * SIZE + OFF_Z
                curAllTargets.append([targetX, targetZ])
                if utils.in_vcone(agentPos, agentAngle, [targetX, targetZ]):
                    curTargets.append([targetX, targetZ])
            self.allTargets.append(cp.deepcopy(curAllTargets))    
            self.targets.append(cp.deepcopy(curTargets))
            # obstacles
            curAllObsts = []
            curObsts = [] # stores all obst visible at this time step
            obstField = fields[3]
            obsts = obstField.split(';')
            for i in range(len(obsts) - 1): # last one is empty
                obstX, obstZ = obsts[i].split(',')
                obstX = float(obstX) * SIZE + OFF_X; obstZ = float(obstZ) * SIZE + OFF_Z
                curAllObsts.append([obstX, obstZ])
                if utils.in_vcone(agentPos, agentAngle, [obstX, obstZ]):
                    curObsts.append([obstX, obstZ])
            self.allObsts.append(cp.deepcopy(curAllObsts))
            self.obsts.append(cp.deepcopy(curObsts))
            # elevator
            curAllElevs = []
            curElevs = [] 
            elevField = fields[5]
            elevX, elevZ = elevField.split(',')
            elevX = float(elevX) * SIZE + OFF_X; elevZ = float(elevZ) * SIZE + OFF_Z
            curAllElevs.append([elevX, elevZ])
            if utils.in_vcone(agentPos, agentAngle, [elevX, elevZ]):
                curElevs.append([elevX, elevZ])
            self.elevs.append(cp.deepcopy(curElevs))
            self.allElevs.append(cp.deepcopy(curAllElevs))

            # paths
            if lineNum == 0:
                self.allPaths = [] # stores all paths at the beginning since they can't be removed
                pathField = fields[4]
                paths = pathField.split(';')
                for i in range(len(paths) - 1): # last one is empty
                    pathX, pathZ = paths[i].split(',')
                    pathX = float(pathX) * SIZE + OFF_X; pathZ = float(pathZ) * SIZE + OFF_Z
                    self.allPaths.append([pathX, pathZ])
                if self.allPaths.index([elevX, elevZ]) == 0: 
                    self.startSide = 1 # which side the agent starts, alternate by trials
                    pass_index = len(self.allPaths) - 1
                else: 
                    self.startSide = 0
                    pass_index = 0
            curPaths = []
            if PATH_LOOKAHEAD:
            # determine which paths are for current time step
            # identify which paths are still ahead and store them
                nearest = utils.nearest_obj([agentX, agentZ], self.allPaths) 
                if self.startSide == 0: # start from the last path, 21, 20, ...,
                    # update passed_index
                    if pass_index - nearest > NUM_PATH_LOOKAHEAD + 2: # do nothing, probably at another seg of path
                        pass
                    else: pass_index = nearest
                    for ct,path in enumerate(self.allPaths):
                        if pass_index - NUM_PATH_LOOKAHEAD < ct <= pass_index:
                            curPaths.append(cp.deepcopy(path))
            
                elif self.startSide == 1: # start from the first path, 0, 1, ..., 
                    # update passed_index
                    if nearest - pass_index > NUM_PATH_LOOKAHEAD + 2: # do nothing, probably at another seg of path
                        pass
                    else: pass_index = nearest
                    for ct,path in enumerate(self.allPaths):
                        if pass_index <= ct < pass_index + NUM_PATH_LOOKAHEAD:
                            curPaths.append(cp.deepcopy(path))
            else: # use visual cone
                for path in self.allPaths:
                    if utils.in_vcone(agentPos, agentAngle, path):
                        curPaths.append(cp.deepcopy(path))
            self.paths.append(cp.deepcopy(curPaths)) 
        
        self.timeSteps = len(self.targets)
        data_file.close()


    def build_irl_data(self):
        '''build a new data file to be used for IRL
        i.e., determine actions for the agent, note that all coordinates assumes upperleft is (0,0).
        data format per time step, per module instance, separated by space:
        module class number, unit reward(-1 or 1), action chosen, distance to this instance after taken an action'''
        self.file_discrete = self.file_continuous + ".dis"
        data_file = open(self.file_discrete, 'w')
        curPath = 0
        for time in range(self.timeSteps - 1): # exclude the last one which we can't compute action
            # agent
            agentPos = utils.tile(self.agents[time][0]) # note that when DISCRETE is set to False in config, utils.tile does not do anything
            # discard the data where agent is too close to elevators
            if utils.calc_dist(agentPos, self.allPaths[0]) < EXCLUDE \
            or utils.calc_dist(agentPos, self.allPaths[-1]) < EXCLUDE: continue 
            # action
            agentPosNext = utils.tile(self.agents[time + 1][0])
            action = utils.calc_bin(utils.calc_angle(agentPos, agentPosNext))
            # targets
            unit_r = 1; module = 0
            for targetPos in self.targets[time]:
                data_file.write(str(module) + ',' + str(unit_r) + ',' + str(action) + ',')
                for count, act in enumerate(ACTIONS):
                    data_file.write(str(utils.conseq(agentPos, utils.tile(targetPos), act, TAR_SIZE)))
                    if count != len(ACTIONS) - 1: data_file.write(',')
                data_file.write(' ')
            # obstacles
            unit_r = -1; module = 1
            for obstPos in self.obsts[time]:
                data_file.write(str(module) + ',' + str(unit_r) + ',' + str(action) + ',')
                for count, act in enumerate(ACTIONS):
                    data_file.write(str(utils.conseq(agentPos, utils.tile(obstPos), act, OBS_SIZE)))
                    if count != len(ACTIONS) - 1: data_file.write(',')
                data_file.write(' ')
            # paths
            unit_r = 1; module = 2
            for pathPos in self.paths[time]:
                data_file.write(str(module) + ',' + str(unit_r) + ',' + str(action) + ',')
                for count, act in enumerate(ACTIONS):
                    data_file.write(str(utils.conseq(agentPos, utils.tile(pathPos), act, PATH_SIZE)))
                    if count != len(ACTIONS) - 1: data_file.write(',')
                data_file.write(' ')
            # elevator
            if ELEVATOR:
                unit_r = 1; module = 3
                for elevPos in self.elevs[time]:
                    data_file.write(str(module) + ',' + str(unit_r) + ',' + str(action) + ',')
                    for count, act in enumerate(ACTIONS):
                        dist, curPath = utils.dist_elev(utils.move(agentPos,act), self.paths[time], elevPos, curPath)
                        data_file.write(str(dist))
                        # data_file.write(str(utils.conseq(agentPos, utils.tile(elevPos), act, PATH_SIZE)))
                        if count != len(ACTIONS) - 1: data_file.write(',')
                    data_file.write(' ')
            
            data_file.write('\n')
        data_file.close()
        
        print("process data and write to file done: " + self.file_continuous)
    
    def visualize_result(self, sol_file_name):
        '''given rewards and gammas estimated from sol_file, visualize the chosen action'''
        # get estimated reward and gamma from a file
        sol_file = open(sol_file_name, 'r')
        params = np.zeros(NUM_MODULE * 2)
        for ct, line in enumerate(sol_file):
            params[ct] = float(line)
        # print("The parameters we use are: "),; print(params)
        angularErrs = []
        angularErrsFw = [] # if the agent just walk forward

        # visualization
        if VIS:
            self.window = cg.GraphWin(title = "A Single Trial", width = ROOM_X * FACTOR + 50, height = ROOM_Z * FACTOR + 200)
            self.window.setBackground("gray")

        curPath = 0 # current path segment
        for time in range(self.timeSteps - 1): # exclude the last one which we can't compute action
            agentPos = utils.tile(self.agents[time][0])
            # print(agentAngle)
            # discard the data where agent is too close to elevators
            if utils.calc_dist(agentPos, self.allPaths[0]) < EXCLUDE \
            or utils.calc_dist(agentPos, self.allPaths[-1]) < EXCLUDE: continue 
            agentPosNext = self.agents[time + 1][0]
            agentAngle = self.agentAngles[time]
            # agentAngle = utils.to360(utils.calc_angle(agentPos, agentPosNext))
            # get actual agent action
            action = utils.calc_bin(utils.calc_angle(agentPos, agentPosNext))

            # 1.0 calculate predicted action
            # true action
            global_Q = np.zeros(len(ACTIONS))
            # targets
            unit_r = 1; module = 0
            r = params[0]; gamma = params[1]
            for targetPos in self.targets[time]:
                for act in ACTIONS:
                    global_Q[act] += r * unit_r * (gamma ** utils.conseq(agentPos, utils.tile(targetPos), act, TAR_SIZE))
            # obstacles
            unit_r = -1; module = 1
            r = params[2]; gamma = params[3]
            for obstPos in self.obsts[time]:
                for act in ACTIONS:
                    global_Q[act] += r * unit_r * (gamma ** utils.conseq(agentPos, utils.tile(obstPos), act, OBS_SIZE))
            # paths
            unit_r = 1; module = 2
            r = params[4]; gamma = params[5]
            for pathPos in self.paths[time]:
                for act in ACTIONS:
                    global_Q[act] += r * unit_r * (gamma ** utils.conseq(agentPos, utils.tile(pathPos), act, PATH_SIZE))
            # elevators
            if ELEVATOR:
                unit_r = 1; module = 3
                r = params[6]; gamma = params[7]
                for elevPos in self.elevs[time]:
                    for act in ACTIONS:
                        dist, curPath = utils.dist_elev(utils.move(agentPos, act), self.paths[time], elevPos, curPath)
                        global_Q[act] += r * unit_r * (gamma ** dist)
            pred_action = np.argmax(global_Q)
            # record prediction error 
            # angularErrs.append(utils.calc_err_actual(utils.move(agentPos, action), agentPos, pred_action)) # this compares with discretized actual action
            angularErrs.append(utils.calc_err_actual(agentPosNext, agentPos, pred_action)) # this compares with actual agentNextPos
            land = utils.facing(agentPos, agentAngle, 0.15 * SIZE)
            angularErrsFw.append(utils.calc_err_actual2(agentPosNext, agentPos, land)) # this compares with actual agentNextPos

            # 2.0 visualize results
            if VIS:
                # draw all targets
                targetPics = []
                for targetPos in self.allTargets[time]:
                    targetPic = cg.Circle(cg.Point(targetPos[0] * FACTOR, targetPos[1] * FACTOR), TAR_SIZE * FACTOR)
                    if targetPos in self.targets[time]:
                        targetPic.setFill("darkblue"); targetPic.setOutline("darkblue")
                    else:
                        targetPic.setFill("darkgray"); targetPic.setOutline("black")
                    targetPic.draw(self.window)
                    targetPics.append(targetPic)
                # draw all obsts
                obstPics = []
                for obstPos in self.allObsts[time]:
                    topLeftPt = cg.Point(obstPos[0] * FACTOR - OBS_SIZE * FACTOR, obstPos[1] * FACTOR - OBS_SIZE * FACTOR)
                    bottomRightPt = cg.Point(obstPos[0] * FACTOR + OBS_SIZE * FACTOR, obstPos[1] * FACTOR + OBS_SIZE * FACTOR)
                    obstPic = cg.Rectangle(topLeftPt,bottomRightPt)
                    if obstPos in self.obsts[time]:
                        obstPic.setFill("darkred"); obstPic.setOutline("darkred")
                    else:
                        obstPic.setFill("darkgray"); obstPic.setOutline("black")
                    obstPic.draw(self.window)
                    obstPics.append(obstPic)
                # draw all paths
                pathPics = []
                for pathPos in self.allPaths:
                    pathPic = cg.Circle(cg.Point(pathPos[0] * FACTOR, pathPos[1] * FACTOR), TAR_SIZE/4 * FACTOR)
                    if pathPos in self.paths[time]:
                        pathPic.setFill("white"); pathPic.setOutline("white")
                    else:
                        pathPic.setFill("darkgray"); pathPic.setOutline("black")
                    pathPic.draw(self.window)
                    pathPics.append(pathPic)
                # draw the elevator
                for elevPos in self.allElevs[time]:
                    elevPic = cg.Circle(cg.Point(elevPos[0] * FACTOR, elevPos[1] * FACTOR), TAR_SIZE * FACTOR)
                    if elevPos in self.elevs[time]:
                        elevPic.setFill("yellow"); elevPic.setOutline("yellow")
                    else:
                        elevPic.setFill("darkgray"); elevPic.setOutline("black")
                    elevPic.draw(self.window)
                # draw agent path over time
                agentPos = self.agents[time][0]
                agentPic = cg.Circle(cg.Point(agentPos[0] * FACTOR, agentPos[1] * FACTOR), AGENT_SIZE * FACTOR)
                agentPic.setFill("green"); agentPic.setOutline("green")
                agentPic.draw(self.window)

                # visualize agent angle
                land = utils.facing(agentPos, agentAngle, 0.15 * SIZE)
                # print(land[0] - agentPos[0], land[1] - agentPos[1])
                anglePic = cg.Line(cg.Point(agentPos[0] * FACTOR, agentPos[1] * FACTOR), cg.Point(land[0] * FACTOR, land[1] * FACTOR))
                anglePic.setFill("black"); anglePic.setArrow("last"); anglePic.setWidth(5)
                anglePic.draw(self.window)

                # visualize predicted action
                print("predicted action is: "),; print(ACT_NAMES[pred_action])
                land = utils.move(agentPos, pred_action)
                # dont draw the acutal landing position, since CELL is large
                land = [(land[0] + agentPos[0]) / 2, (land[1] + agentPos[1]) / 2]
                predActPic = cg.Line(cg.Point(agentPos[0] * FACTOR, agentPos[1] * FACTOR), cg.Point(land[0] * FACTOR, land[1] * FACTOR))
                predActPic.setFill("red"); predActPic.setArrow("last"); predActPic.setWidth(2)
                predActPic.draw(self.window)
        
                # visualize agent action:
                print("discreteized actual action: "),; print(ACT_NAMES[action])
                land = utils.move(agentPos, action)
                land = [(land[0] + agentPos[0]) / 2, (land[1] + agentPos[1]) / 2]
                actualActPic = cg.Line(cg.Point(agentPos[0] * FACTOR, agentPos[1] * FACTOR), cg.Point(land[0] * FACTOR, land[1] * FACTOR)) # could also use actual next position
                actualActPic.setFill("green"); actualActPic.setArrow("last"); actualActPic.setWidth(2)
                actualActPic.draw(self.window)

                # click to go to next step
                if MOUSE: self.window.getMouse()
                for targetPic in targetPics: targetPic.undraw()
                for obstPic in obstPics: obstPic.undraw()
                for pathPic in pathPics: pathPic.undraw()
                #predActPic.undraw()
                #actualActPic.undraw()
        
        err = (sum(angularErrs)/float(len(angularErrs)))
        print("Average absolute prediction error is, in degrees: {}".format(err))
        errFw = (sum(angularErrsFw)/float(len(angularErrsFw)))
        print("Walking forward average absolute prediction error is, in degrees: {}".format(errFw))
        return err         

    def free_run(self, sol_file_name):
        '''given rewards and gammas estimated from sol_file, visualize the free trajectory path'''
        # get estimated reward and gamma from a file
        sol_file = open(sol_file_name, 'r')
        params = np.zeros(NUM_MODULE * 2)
        for ct, line in enumerate(sol_file):
            params[ct] = float(line)
        # print("The parameters we use are: "),; print(params)

        # visualization
        if VIS:
            self.window = cg.GraphWin(title = "A Single Trial", width = ROOM_X * FACTOR + 50, height = ROOM_Z * FACTOR + 200)
            self.window.setBackground("gray")
        
        for time in range(self.timeSteps - 1):
            agentAngle = self.agentAngles[time]
            agentPos = utils.tile(self.agents[time][0]) 

            # discard the data where agent is too close to elevators
            if utils.calc_dist(agentPos, self.allPaths[0]) < EXCLUDE \
            or utils.calc_dist(agentPos, self.allPaths[-1]) < EXCLUDE: continue 
            else: break # the stored agentPos and agent angle is the start
        
        targets = cp.deepcopy(self.allTargets[time])
        obsts = cp.deepcopy(self.allObsts[time])
        paths = cp.deepcopy(self.allPaths)
        elevs = cp.deepcopy(self.allElevs[time])
        if self.startSide == 0: # which side the agent starts, alternate by trials
            pass_index = 0
        else: 
            pass_index = len(self.allPaths) - 1

        arrived = False
        # begin iterations
        while not(arrived): 
            # print(agentAngle)
            # 1.0 calculate predicted action
            # true action
            global_Q = np.zeros(len(ACTIONS))
            # targets
            unit_r = 1; module = 0
            r = params[0]; gamma = params[1]
            if targets != []:
                targetPos  = targets[utils.nearest_obj(agentPos,targets)]
                for act in ACTIONS:
                    global_Q[act] += r * unit_r * (gamma ** utils.conseq(agentPos, utils.tile(targetPos), act, TAR_SIZE))
            # obstacles
            unit_r = -1; module = 1
            r = params[2]; gamma = params[3]
            obstPos = obsts[utils.nearest_obj(agentPos,obsts)]
            for act in ACTIONS:
                global_Q[act] += r * unit_r * (gamma ** utils.conseq(agentPos, utils.tile(obstPos), act, OBS_SIZE))
            # paths
            unit_r = 1; module = 2
            r = params[4]; gamma = params[5]
            # paths
            curPaths = []
            if PATH_LOOKAHEAD:
            # determine which paths are for current time step
            # identify which paths are still ahead and store them
                nearest = utils.nearest_obj(agentPos, paths) 
                if self.startSide == 0: # start from the last path, 21, 20, ...,
                    # update passed_index
                    if pass_index - nearest > NUM_PATH_LOOKAHEAD + THROW_OUT: # do nothing, probably at another seg of path
                        pass
                    else: pass_index = nearest
                    for ct,path in enumerate(self.allPaths):
                        if pass_index - NUM_PATH_LOOKAHEAD < ct <= pass_index:
                            curPaths.append(cp.deepcopy(path))
                elif self.startSide == 1: # start from the first path, 0, 1, ..., 
                    # update passed_index
                    if nearest - pass_index > NUM_PATH_LOOKAHEAD + THROW_OUT: # do nothing, probably at another seg of path
                        pass
                    else: pass_index = nearest
                    for ct,path in enumerate(self.allPaths):
                        if pass_index <= ct < pass_index + NUM_PATH_LOOKAHEAD:
                            curPaths.append(cp.deepcopy(path))
                for pathPos in curPaths:
                    if utils.in_vcone(agentPos, agentAngle, pathPos):
                        for act in ACTIONS:
                            global_Q[act] += r * unit_r * (gamma ** utils.conseq(agentPos, utils.tile(pathPos), act, PATH_SIZE))
            else:
                cur_path = utils.nearest_obj(agentPos,paths)
                print(pass_index, cur_path)
                if abs(cur_path - pass_index) > 2:
                    cur_path = pass_index
                else:
                    if self.startSide == 0: # which side the agent starts, alternate by trials
                        if pass_index >= cur_path: # move to next waypoint
                            cur_path += 1
                    if self.startSide == 1: # which side the agent starts, alternate by trials
                        if pass_index <= cur_path: # move to next waypoint
                            cur_path -= 1

                pathPos = paths[cur_path]
                pass_index = cur_path
                for act in ACTIONS:
                    global_Q[act] += r * unit_r * (gamma ** utils.conseq(agentPos, utils.tile(pathPos), act, PATH_SIZE))

            # elevators
            if ELEVATOR:
                unit_r = 1; module = 3
                r = params[6]; gamma = params[7]
                for elevPos in elevs:
                    if utils.in_vcone(agentPos, agentAngle, elevPos):
                        for act in ACTIONS:
                            global_Q[act] += r * unit_r * (gamma ** utils.conseq(agentPos, utils.tile(elevPos), act, PATH_SIZE))
            pred_action = np.argmax(global_Q)
            
            # touched obstacles and targets removed
            # 2.0 visualize results
            if VIS:
                # draw all targets
                targetPics = []
                for targetPos in targets:
                    targetPic = cg.Circle(cg.Point(targetPos[0] * FACTOR, targetPos[1] * FACTOR), TAR_SIZE * FACTOR)
                    targetPic.setFill("darkblue"); targetPic.setOutline("darkblue")
                    targetPic.draw(self.window)
                    targetPics.append(targetPic)
                # draw all obsts
                obstPics = []
                for obstPos in obsts:
                    topLeftPt = cg.Point(obstPos[0] * FACTOR - OBS_SIZE * FACTOR, obstPos[1] * FACTOR - OBS_SIZE * FACTOR)
                    bottomRightPt = cg.Point(obstPos[0] * FACTOR + OBS_SIZE * FACTOR, obstPos[1] * FACTOR + OBS_SIZE * FACTOR)
                    obstPic = cg.Rectangle(topLeftPt,bottomRightPt)
                    obstPic.setFill("darkred"); obstPic.setOutline("darkred")
                    obstPic.draw(self.window)
                    obstPics.append(obstPic)
                # draw all paths
                pathPics = []
                for pathPos in paths:
                    pathPic = cg.Circle(cg.Point(pathPos[0] * FACTOR, pathPos[1] * FACTOR), TAR_SIZE/4 * FACTOR)
                    pathPic.setFill("white"); pathPic.setOutline("white")
                    pathPic.draw(self.window)
                    pathPics.append(pathPic)
                # draw the elevator
                for elevPos in elevs:
                    elevPic = cg.Circle(cg.Point(elevPos[0] * FACTOR, elevPos[1] * FACTOR), TAR_SIZE * FACTOR)
                    elevPic.setFill("yellow"); elevPic.setOutline("yellow")
                    elevPic.draw(self.window)
                # draw agent path over time
                agentPic = cg.Circle(cg.Point(agentPos[0] * FACTOR, agentPos[1] * FACTOR), AGENT_SIZE * FACTOR)
                agentPic.setFill("green"); agentPic.setOutline("green")
                agentPic.draw(self.window)

                # visualize agent angle
                land = utils.facing(agentPos, agentAngle, 0.15 * SIZE)
                anglePic = cg.Line(cg.Point(agentPos[0] * FACTOR, agentPos[1] * FACTOR), cg.Point(land[0] * FACTOR, land[1] * FACTOR))
                anglePic.setFill("black"); anglePic.setArrow("last"); anglePic.setWidth(5)
                anglePic.draw(self.window)

                # click to go to next step
                if MOUSE: self.window.getMouse()
                if not(arrived):
                    for targetPic in targetPics: targetPic.undraw()
                    for obstPic in obstPics: obstPic.undraw()
                    for pathPic in pathPics: pathPic.undraw()
                #predActPic.undraw()
                #actualActPic.undraw()

            # action consequences
            agentAngle = utils.calc_angle(agentPos, utils.move(agentPos, pred_action))
            # to 360 degree range and different coordinate frame (agreed with the ones from .mat files)
            agentAngle = utils.to360(agentAngle)
            agentPos = utils.move(agentPos, pred_action) # agent moves
            # remove touched stuff
            for targetPos in targets[:]:
                if utils.calc_dist(agentPos, targetPos) < TAR_SIZE: targets.remove(targetPos)  
            # obstacles
            for obstPos in obsts[:]:
                if utils.calc_dist(agentPos, obstPos) < OBS_SIZE: obsts.remove(obstPos)  
            if self.startSide == 0: # which side the agent starts, alternate by trials
                if pass_index == len(self.allPaths) - 1: arrived = True
            else: 
                if pass_index == 0: arrived = True



if __name__ == '__main__':
    trial0 = Trial(sys.argv[1]) # the first argument being the data filename
    if sys.argv[2] == 'b': # build irl data, called by the .sh script 
        trial0.build_irl_data()
    elif sys.argv[2] == 'v': # visualize fitted action
        VIS = True; MOUSE = False
        trial0.visualize_result(sys.argv[3]) # solution filename
        raw_input("Please press enter to exit")
    elif sys.argv[2] == 'a': # just run trial and get angular error
        VIS = True; MOUSE = False
        trial0.visualize_result(sys.argv[3]) # solution filename
    elif sys.argv[2] == 'd': # draw data
        VIS = True; MOUSE = True
        trial0.draw()
    elif sys.argv[2] == 'f': # 
        VIS = True; MOUSE = False
        trial0.free_run(sys.argv[3]) # solution filename
        raw_input("Please press enter to exit")


