'''Environment'''
import re
import copy as cp
import graphics as cg

ROOM_X = 8.534
ROOM_Z = 7.315
SIZE = 100

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
            agentX = float(agentX); agentZ = float(agentZ)
            curAgent.append([agentX, agentZ])
            self.agents.append(cp.deepcopy(curAgent))

            # targets
            curTargets = [] # stores all target at this time step
            targetField = fields[2]
            targets = targetField.split(';')
            for i in range(len(targets) - 1): # last one is empty
                targetX, targetZ = targets[i].split(',')
                targetX = float(targetX); targetZ = float(targetZ)
                curTargets.append([targetX, targetZ])
            self.targets.append(cp.deepcopy(curTargets))
            # obstacles
            curObsts = [] # stores all target at this time step
            obstField = fields[3]
            obsts = obstField.split(';')
            for i in range(len(obsts) - 1): # last one is empty
                obstX, obstZ = obsts[i].split(',')
                obstX = float(obstX); obstZ = float(obstZ)
                curObsts.append([obstX, obstZ])
            self.obsts.append(cp.deepcopy(curObsts))
            # paths
            curPaths = [] # stores all target at this time step
            pathField = fields[4]
            paths = pathField.split(';')
            for i in range(len(paths) - 1): # last one is empty
                pathX, pathZ = paths[i].split(',')
                pathX = float(pathX); pathZ = float(pathZ)
                curPaths.append([pathX, pathZ])
            self.paths.append(cp.deepcopy(curPaths))
            # elevator
            curElev = [] 
            elevField = fields[5]
            elevX, elevZ = elevField.split(',')
            elevX = float(elevX); elevZ = float(elevZ)
            curElev.append([elevX, elevZ])
            self.elevs.append(cp.deepcopy(curElev))
        
        print("Read in obejcts done")
        data_file.close()

    def draw(self):
        # draw the world and agent path
        self.window = cg.GraphWin(title = "A Single Trial", width = ROOM_X * SIZE, height = ROOM_Z * SIZE)
        time = 0
        # draw all targets
        for targetPos in self.targets[time]:
            targetPos[0], targetPos[1]
        # draw all obsts

        # draw all paths

        # draw the elevator

        # draw agent path over time


if __name__ == '__main__':
    trial0 = Trial("data/subj26/26_5_1.data")
    trial0.draw()


raw_input("Please press enter to exit")


CELL_SIZE = 10

class Environment:
    def __init__(self,rows,columns):
        self.rows = rows
        self.columns = columns

        #represent maze map as a 2D array
        self.mazeMap = [[0 for x in range(columns)] for x in range(rows)]
    
    def draw(self, objInst):
        width_ = (self.columns + 2) * CELL_SIZE
        height_ = (self.rows + 2) * CELL_SIZE
        #Draw maze grid:
        self.window = cg.GraphWin(title = "Maze", width = width_, height = height_)
        cells = []
        for i in range(self.rows):
            for j in range(self.columns):
                cell = cg.Rectangle(cg.Point(j * CELL_SIZE, i * CELL_SIZE), cg.Point((j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE))
                cell.draw(self.window)

        #Draw position labels
        #Row labels
        for i in range(self.rows):
            label = cg.Text(cg.Point((self.columns + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE),str(i))
            label.draw(self.window)
        #Column labels
        for i in range(self.columns):
            label = cg.Text(cg.Point((i + 0.5) * CELL_SIZE, (self.rows + 0.5) * CELL_SIZE),str(i))
            label.draw(self.window)

    



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
            
