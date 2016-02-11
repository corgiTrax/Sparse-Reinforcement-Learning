'''Environment'''
import re
import copy as cp
import graphics as cg
import math
from config import *
import utils
import sys

class Trial:
    def __init__(self, filename):
        '''read in all objects from data_file and their positions'''
        ''' positions are translated to the new coordinate system by adding OFF_X and OFF_Z, 
        where (0,0) is at upperleft corner instead of at the center; coordinates are translated by * SIZE as well'''
        self.agents = []
        self.targets = []
        self.obsts = []
        self.paths = []
        self.elevs = []
        
        data_file = open(filename,'r')
        self.file_continuous = filename
        for lineNum, line in enumerate(data_file):
            fields = re.split('#|\n', line)
            # agent
            curAgent = [] 
            agentField = fields[1]
            agentX, agentZ = agentField.split(',')
            agentX = float(agentX) * SIZE + OFF_X; agentZ = float(agentZ) * SIZE + OFF_Z
            curAgent.append([agentX, agentZ])
            self.agents.append(cp.deepcopy(curAgent))

            # targets
            curTargets = [] # stores all target at this time step
            targetField = fields[2]
            targets = targetField.split(';')
            for i in range(len(targets) - 1): # last one is empty
                targetX, targetZ = targets[i].split(',')
                targetX = float(targetX) * SIZE + OFF_X; targetZ = float(targetZ) * SIZE + OFF_Z
                curTargets.append([targetX, targetZ])
            self.targets.append(cp.deepcopy(curTargets))
            # obstacles
            curObsts = [] # stores all target at this time step
            obstField = fields[3]
            obsts = obstField.split(';')
            for i in range(len(obsts) - 1): # last one is empty
                obstX, obstZ = obsts[i].split(',')
                obstX = float(obstX) * SIZE + OFF_X; obstZ = float(obstZ) * SIZE + OFF_Z
                curObsts.append([obstX, obstZ])
            self.obsts.append(cp.deepcopy(curObsts))
            # paths
            curPaths = [] # stores all target at this time step
            pathField = fields[4]
            paths = pathField.split(';')
            for i in range(len(paths) - 1): # last one is empty
                pathX, pathZ = paths[i].split(',')
                pathX = float(pathX) * SIZE + OFF_X; pathZ = float(pathZ) * SIZE + OFF_Z
                curPaths.append([pathX, pathZ])
            self.paths.append(cp.deepcopy(curPaths))
            # elevator
            curElev = [] 
            elevField = fields[5]
            elevX, elevZ = elevField.split(',')
            elevX = float(elevX) * SIZE + OFF_X; elevZ = float(elevZ) * SIZE + OFF_Z
            curElev.append([elevX, elevZ])
            self.elevs.append(cp.deepcopy(curElev))
        
        self.timeSteps = len(self.targets)
        print("Read in obejcts done")
        data_file.close()

    def draw(self):
        '''draw the world and agent path from data'''
        self.window = cg.GraphWin(title = "A Single Trial", width = ROOM_X + 50, height = ROOM_Z + 200)
        self.window.setBackground("gray")

        # discretization
        self.rows = int(math.ceil(ROOM_X / CELL))
        self.cols = int(math.ceil(ROOM_Z / CELL))

        if SHOW_GRID:
            #Draw maze grid:
            for i in range(self.rows):
                for j in range(self.cols):
                    cell = cg.Rectangle(cg.Point(j * CELL, i * CELL), cg.Point((j + 1) * CELL, (i + 1) * CELL))
                    cell.draw(self.window)
                    cell.setOutline("black")
            #Draw position labels
            #Row labels
            for i in range(self.rows):
                label = cg.Text(cg.Point((self.cols + 1) * CELL, (i + 0.5) * CELL),str(i))
                label.setSize(FONT_SIZE)
                label.draw(self.window)
            #Column labels
            for i in range(self.cols):
                label = cg.Text(cg.Point((i + 0.5) * CELL, (self.rows + 1) * CELL),str(i))
                label.setSize(FONT_SIZE)
                label.draw(self.window)

        for time in range(self.timeSteps - 1): # exclude the last one which we can't compute action
            # draw all targets
            targetPics = []
            for targetPos in self.targets[time]:
                targetPic = cg.Circle(cg.Point(targetPos[0], targetPos[1]), TAR_SIZE)
                targetPic.setFill("darkblue"); targetPic.setOutline("darkblue")
                targetPic.draw(self.window)
                targetPics.append(targetPic)
            # draw all obsts
            obstPics = []
            for obstPos in self.obsts[time]:
                topLeftPt = cg.Point(obstPos[0] - OBS_SIZE, obstPos[1] - OBS_SIZE)
                bottomRightPt = cg.Point(obstPos[0] + OBS_SIZE, obstPos[1] + OBS_SIZE)
                obstPic = cg.Rectangle(topLeftPt,bottomRightPt)
                obstPic.setFill("darkred"); obstPic.setOutline("darkred")
                obstPic.draw(self.window)
                obstPics.append(obstPic)
            # draw all paths
            for pathPos in self.paths[time]:
                pathPic = cg.Circle(cg.Point(pathPos[0], pathPos[1]), TAR_SIZE/4)
                pathPic.setFill("white"); pathPic.setOutline("white")
                pathPic.draw(self.window)
            # draw the elevator
            for elevPos in self.elevs[time]:
                elevPic = cg.Circle(cg.Point(elevPos[0], elevPos[1]), TAR_SIZE)
                elevPic.setFill("yellow"); elevPic.setOutline("yellow")
                elevPic.draw(self.window)
            # draw agent path over time
            agentPos = self.agents[time][0]
            agentPic = cg.Circle(cg.Point(agentPos[0], agentPos[1]), AGENT_SIZE)
            agentPic.setFill("green"); agentPic.setOutline("green")
            agentPic.draw(self.window)
#            agentX, agentZ = utils.tile(agentPos)
#            print("discretized position: "),; print(agentX, agentZ)
            # calculate agent action:
            agentPosNext = self.agents[time + 1][0]
            if abs(utils.calc_dist(agentPos, agentPosNext)) < CELL: action = STAY
            else: action = utils.calc_bin(utils.calc_angle(agentPos, agentPosNext))
            print("discreteized actual action: "),; print(ACT_NAMES[action])
            # click to go to next step
            self.window.getMouse()
            for targetPic in targetPics: targetPic.undraw()
            for obstPic in obstPics: obstPic.undraw()
           
    def build_irl_data(self):
        '''build a new data file to be used for IRL
        i.e., determine actions for the agent, note that all coordinates assumes upperleft is (0,0).
        data format per time step, per module instance, separated by space:
        module class number, unit reward(-1 or 1), action chosen, distance to this instance after taken an action'''
        self.file_discrete = self.file_continuous + ".dis"
        data_file = open(self.file_discrete, 'w')
        for time in range(self.timeSteps - 1): # exclude the last one which we can't compute action
            # agent
            agentPos = self.agents[time][0]
            # action
            agentPosNext = self.agents[time + 1][0]
            if abs(utils.calc_dist(agentPos, agentPosNext)) < CELL: action = STAY
            else: action = utils.calc_bin(utils.calc_angle(agentPos, agentPosNext))
            # targets
            unit_r = 1; module = 0
            for targetPos in self.targets[time]:
                data_file.write(str(module) + ',' + str(unit_r) + ',' + str(action) + ',')
                for count, act in enumerate(ACTIONS):
                    data_file.write(str(utils.conseq(agentPos, targetPos, act)))
                    if count != len(ACTIONS) - 1: data_file.write(',')
                data_file.write(' ')
            # obstacles
            unit_r = -1; module = 1
            for obstPos in self.obsts[time]:
                data_file.write(str(module) + ',' + str(unit_r) + ',' + str(action) + ',')
                for count, act in enumerate(ACTIONS):
                    data_file.write(str(utils.conseq(agentPos, obstPos, act)))
                    if count != len(ACTIONS) - 1: data_file.write(',')
                data_file.write(' ')
            # paths
            unit_r = 1; module = 2
            for pathPos in self.paths[time]:
                data_file.write(str(module) + ',' + str(unit_r) + ',' + str(action) + ',')
                for count, act in enumerate(ACTIONS):
                    data_file.write(str(utils.conseq(agentPos, pathPos, act)))
                    if count != len(ACTIONS) - 1: data_file.write(',')
                data_file.write(' ')
            # elevator
            unit_r = 1; module = 3
            for elevPos in self.elevs[time]:
                data_file.write(str(module) + ',' + str(unit_r) + ',' + str(action) + ',')
                for count, act in enumerate(ACTIONS):
                    data_file.write(str(utils.conseq(agentPos, elevPos, act)))
                    if count != len(ACTIONS) - 1: data_file.write(',')
                data_file.write(' ')
            data_file.write('\n')
        data_file.close()
        
        print("discretize data and write to file done")

if __name__ == '__main__':
    trial0 = Trial(sys.argv[1])
#    trial0.build_irl_data()
    trial0.draw()

# raw_input("Please press enter to exit")


           
