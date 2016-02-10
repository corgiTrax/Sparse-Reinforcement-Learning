'''Environment'''
import re
import copy as cp
import graphics as cg
import math
from config import *

class Trial:
    def __init__(self, filename):
        '''read in all objects from data_file and their positions'''
        self.agents = []
        self.targets = []
        self.obsts = []
        self.paths = []
        self.elevs = []
        
        data_file = open(filename,'r')
        for lineNum, line in enumerate(data_file):
            fields = re.split('#|\n', line)
            # agent
            curAgent = [] 
            agentField = fields[1]
            agentX, agentZ = agentField.split(',')
            agentX = float(agentX) + OFF_X; agentZ = float(agentZ) + OFF_Z
            curAgent.append([agentX, agentZ])
            self.agents.append(cp.deepcopy(curAgent))

            # targets
            curTargets = [] # stores all target at this time step
            targetField = fields[2]
            targets = targetField.split(';')
            for i in range(len(targets) - 1): # last one is empty
                targetX, targetZ = targets[i].split(',')
                targetX = float(targetX) + OFF_X; targetZ = float(targetZ) + OFF_Z
                curTargets.append([targetX, targetZ])
            self.targets.append(cp.deepcopy(curTargets))
            # obstacles
            curObsts = [] # stores all target at this time step
            obstField = fields[3]
            obsts = obstField.split(';')
            for i in range(len(obsts) - 1): # last one is empty
                obstX, obstZ = obsts[i].split(',')
                obstX = float(obstX) + OFF_X; obstZ = float(obstZ) + OFF_Z
                curObsts.append([obstX, obstZ])
            self.obsts.append(cp.deepcopy(curObsts))
            # paths
            curPaths = [] # stores all target at this time step
            pathField = fields[4]
            paths = pathField.split(';')
            for i in range(len(paths) - 1): # last one is empty
                pathX, pathZ = paths[i].split(',')
                pathX = float(pathX) + OFF_X; pathZ = float(pathZ) + OFF_Z
                curPaths.append([pathX, pathZ])
            self.paths.append(cp.deepcopy(curPaths))
            # elevator
            curElev = [] 
            elevField = fields[5]
            elevX, elevZ = elevField.split(',')
            elevX = float(elevX) + OFF_X; elevZ = float(elevZ) + OFF_Z
            curElev.append([elevX, elevZ])
            self.elevs.append(cp.deepcopy(curElev))
        
        self.timeSteps = len(self.targets)
        print("Read in obejcts done")
        data_file.close()

    def draw(self):
        '''draw the world and agent path from data'''
        self.window = cg.GraphWin(title = "A Single Trial", width = ROOM_X * SIZE + 50, height = ROOM_Z * SIZE + 200)
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

        for time in range(1): #(self.timeSteps):
            # draw all targets
            targetPics = []
            for targetPos in self.targets[time]:
                targetPic = cg.Circle(cg.Point(targetPos[0] * SIZE, targetPos[1] * SIZE ), TAR_SIZE)
                targetPic.setFill("darkblue"); targetPic.setOutline("darkblue")
                targetPic.draw(self.window)
                targetPics.append(targetPic)
            # draw all obsts
            obstPics = []
            for obstPos in self.obsts[time]:
                topLeftPt = cg.Point(obstPos[0] * SIZE - OBS_SIZE, obstPos[1] * SIZE - OBS_SIZE)
                bottomRightPt = cg.Point(obstPos[0] * SIZE + OBS_SIZE, obstPos[1] * SIZE + OBS_SIZE)
                obstPic = cg.Rectangle(topLeftPt,bottomRightPt)
                obstPic.setFill("darkred"); obstPic.setOutline("darkred")
                obstPic.draw(self.window)
                obstPics.append(obstPic)
            # draw all paths
            for pathPos in self.paths[time]:
                pathPic = cg.Circle(cg.Point(pathPos[0] * SIZE, pathPos[1] * SIZE), TAR_SIZE/2)
                pathPic.setFill("white"); pathPic.setOutline("white")
                pathPic.draw(self.window)
            # draw the elevator
            for elevPos in self.elevs[time]:
                elevPic = cg.Circle(cg.Point(elevPos[0] * SIZE, elevPos[1] * SIZE), TAR_SIZE * 2)
                elevPic.setFill("yellow"); elevPic.setOutline("yellow")
                elevPic.draw(self.window)
            # draw agent path over time
            for agentPos in self.agents[time]:
                agentPic = cg.Circle(cg.Point(agentPos[0] * SIZE, agentPos[1] * SIZE ), TAR_SIZE/2)
                agentPic.setFill("green"); agentPic.setOutline("green")
                agentPic.draw(self.window)
            # click to go to next step
            self.window.getMouse()
            for targetPic in targetPics: targetPic.undraw()
            for obstPic in obstPics: obstPic.undraw()
           
    def discretize(self):
        '''using CELL(SIZE) to discretize the data and build a new data file to be used for IRL
        i.e., translate object continuous coordinates into cell coordinates; determine actions for the agent'''
        self.timeSteps; 


if __name__ == '__main__':
    trial0 = Trial("data/subj26/26_40_4.data")
    trial0.draw()


raw_input("Please press enter to exit")



    



## not in use   
#def findNearestPrize(agentPos, maze):
#    '''find nearest prize, return its coordinate'''
#    minDist = maze.rows + maze.columns
#    for i in range(len(maze.prizes)):
#        curPrize = maze.prizes[i]
#        rowDist = abs(agentPos[ROW] - curPrize[ROW])
#        colDist = abs(agentPos[COL] - curPrize[COL])
#        dist = rowDist + colDist
#        if (dist < minDist):
#            minDist = dist
#            nearestPrize = curPrize
#        elif (dist == minDist): #Break tie randomly
#            if (random.random() >= 0.5):
#                minDist = dist
#                nearestPrize = curPrize
#    return nearestPrize
            
