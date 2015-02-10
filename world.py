'''Environment'''

from config import *

#Enums for objects in the maze
Obstacle = 256
Prize = 255
Empty = 254

class Maze:
    def __init__(self,rows,columns, pPrize = P_PRIZE, pObs = P_OBS):
        self.rows = rows
        self.columns = columns
        self.prizes = [] #stores positions of prizes
        self.originalNumPrizes = 0
        self.obstacles = [] #stores positions of obstacles
        self.targetPrize = None #Agent's current target prize
        self.pPrize = pPrize
        self.pObs = pObs
 
        #represent maze map as a 2D array
        self.mazeMap = [[0 for x in range(columns)] for x in range(rows)]
        for i in range(rows):
            for j in range(columns):
                self.mazeMap[i][j] = Empty
        
        for i in range(rows):
           for j in range(columns):
                if (random.random() <= self.pPrize):
                    self.mazeMap[i][j] = Prize
                    self.prizes.append([i,j])
                    self.originalNumPrizes += 1
                #This is not exactly correct, pPrize and pObstacle should be independent
                elif (random.random() <= self.pObs):
                    self.mazeMap[i][j] = Obstacle
                    self.obstacles.append([i,j])

   	    #This map keeps a backup of original map
        self.originalMap = py_copy.deepcopy(self.mazeMap)
    
    def drawSelf(self, isnew):
        if (isnew == True):
            width_ = (self.columns + 2) * CELL_SIZE
            height_ = (self.rows + 2) * CELL_SIZE
        #Draw maze grid:
            self.window = cg.GraphWin(title = "Maze", width = width_, height = height_)
            cells = []
            for i in range(self.rows):
                for j in range(self.columns):
                    cell = cg.Rectangle(cg.Point(j * CELL_SIZE, i * CELL_SIZE), cg.Point((j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE))
                    cell.draw(self.window)

            #Draw prizes, since some prizes need to be removed, keep a list of all prize pics
            self.prizePics = []
            for i in range(len(self.prizes)):
                cur_prize = self.prizes[i]
                prizePic = cg.Circle(cg.Point((cur_prize[COL] + 0.5) * CELL_SIZE, (cur_prize[ROW] + 0.5) * CELL_SIZE), CELL_SIZE/6)
                prizePic.setFill('orange')
                self.prizePics.append(prizePic)
                prizePic.draw(self.window)
    
            #Draw obstacles
            for i in range(len(self.obstacles)):
                cur_obs = self.obstacles[i]
                topLeftPt = cg.Point(cur_obs[COL] * CELL_SIZE, cur_obs[ROW] * CELL_SIZE)
                bottomRightPt = cg.Point((cur_obs[COL] + 1) * CELL_SIZE, (cur_obs[ROW] + 1) * CELL_SIZE)
                obsPic = cg.Rectangle(topLeftPt,bottomRightPt)
                obsPic.setFill('blue')
                obsPic.draw(self.window)

            #Draw position labels
            #Row labels
            for i in range(self.rows):
                label = cg.Text(cg.Point((self.columns + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE),str(i))
                label.draw(self.window)
            #Column labels
            for i in range(self.columns):
                label = cg.Text(cg.Point((i + 0.5) * CELL_SIZE, (self.rows + 0.5) * CELL_SIZE),str(i))
                label.draw(self.window)

        else:#if this is not a new maze
            #redraw all prizes
            for i in range(len(self.prizePics)):
                self.prizePics[i].undraw()
            self.prizePics = []
            for i in range(len(self.prizes)):
                cur_prize = self.prizes[i]
                prizePic = cg.Circle(cg.Point((cur_prize[COL] + 0.5) * CELL_SIZE, (cur_prize[ROW] + 0.5) * CELL_SIZE), CELL_SIZE/6)
                prizePic.setFill('orange')
                self.prizePics.append(prizePic)
                prizePic.draw(self.window)
            
    def drawTargetPrize(self,targetPrize_):
        if(not(self.targetPrize is None)):
            self.targetPrize.undraw()
        self.targetPrize = cg.Circle(cg.Point((targetPrize_[COL] + 0.5) * CELL_SIZE, (targetPrize_[ROW] + 0.5) * CELL_SIZE), CELL_SIZE/6)
        self.targetPrize.setFill('green')
        self.targetPrize.draw(self.window)

    #given agent position, calulate agent reward, if agent collects prize, remove it from mazeMap
    def calc_reward(self,agentPos):
        if (self.mazeMap[agentPos[ROW]][agentPos[COL]] == Prize):
	    #These 2 lines removes collected prize
            if (agentPos in self.prizes):
                self.prizes.remove(agentPos)
                self.mazeMap[agentPos[ROW]][agentPos[COL]] = Empty
            return R_PRIZE
        if (self.mazeMap[agentPos[ROW]][agentPos[COL]] == Obstacle):
	        return R_OBS
        if (self.mazeMap[agentPos[ROW]][agentPos[COL]] == Empty):
	        return 0

   
def findNearestPrize(agentPos, maze):
    '''find nearest prize, return its coordinate'''
    minDist = maze.rows + maze.columns
    for i in range(len(maze.prizes)):
        curPrize = maze.prizes[i]
        rowDist = abs(agentPos[ROW] - curPrize[ROW])
        colDist = abs(agentPos[COL] - curPrize[COL])
        dist = rowDist + colDist
        if (dist < minDist):
            minDist = dist
            nearestPrize = curPrize
        elif (dist == minDist): #Break tie randomly
            if (random.random() >= 0.5):
                minDist = dist
                nearestPrize = curPrize
    return nearestPrize
            
