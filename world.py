'''Environment'''

from config import *

#Domain: Maze
#Enums for objects in the maze
Obstacle = 256
Price = 255
Empty = 254

ROW = config.ROW
COL = config.COL

class Maze:
    def __init__(self,rows,columns, mazeType, objPos = [0,0], pPrice = config.pPrice, pObstacle = config.pObstacle):
        self.rows = py_copy.deepcopy(rows)
        self.columns = py_copy.deepcopy(columns)
        self.prices = []#stores positions of prices
        self.originalNumPrices = 0
        self.obstacles = []#stores positions of obstacles
        self.objectPos = py_copy.deepcopy(objPos)
        self.targetPrice = None #Agent's current target price
        self.pPrice = pPrice
        self.pObstacle = pObstacle
 
        #represent maze map as a 2D array
        self.mazeMap = [[0 for x in range(columns)] for x in range(rows)]
        for i in range(rows):
            for j in range(columns):
                self.mazeMap[i][j] = Empty
        
        if (mazeType == 'price'):#generate a maze with single price
            self.mazeMap[self.objectPos[0]][self.objectPos[1]] = Price
            self.prices.append(self.objectPos)
        if (mazeType == 'obstacle'):#generate a maze with single obstacle
            self.mazeMap[self.objectPos[0]][self.objectPos[1]] = Obstacle
            self.obstacles.append(self.objectPos)
        if (mazeType == 'predator'):#generate an empty maze
            pass
        if (mazeType == 'test'):#generate a random map, and store in map file
            for i in range(rows):
               for j in range(columns):
#                    if (i == 0 or j == 0 or i == self.rows - 1 or j == self.columns - 1):#place obstacles at edges
#                        self.mazeMap[i][j] = Obstacle
#                        self.obstacles.append([i,j])
                    if (random.random() <= self.pPrice):
                        self.mazeMap[i][j] = Price
                        self.prices.append([i,j])
                        self.originalNumPrices += 1
                    #This is not exactly correct, pPrice and pObstacle should be indepedent
                    elif (random.random() <= self.pObstacle):
                        self.mazeMap[i][j] = Obstacle
                        self.obstacles.append([i,j])
        #if (mazeType == 'file'): #read map form a file
        
        #This map records agent path
        self.pathMap = py_copy.deepcopy(self.mazeMap)
	    #This map keeps a backup of original map
        self.originalMap = py_copy.deepcopy(self.mazeMap)
    
#    def writeMapToFile(self,filename):
#        for i in range(self.rows):
#            for j in range(self.columns):
#        pass
    
    def drawSelf(self, isnew):
        if (isnew == True):
            width_ = (self.columns + 2) * config.CELL_SIZE
            height_ = (self.rows + 2) * config.CELL_SIZE
        #Draw maze grid:
            self.window = graph.GraphWin(title = "Maze", width = width_, height = height_)
            cells = []
            for i in range(self.rows):
                for j in range(self.columns):
                    cell = graph.Rectangle(graph.Point(j * config.CELL_SIZE, i * config.CELL_SIZE),graph.Point((j + 1) * config.CELL_SIZE, (i + 1) * config.CELL_SIZE))
                    cell.draw(self.window)

            #Draw prices, since some prices need to be removed, keep a list of all price pics
            self.pricePics = []
            for i in range(len(self.prices)):
                cur_price = self.prices[i]
                pricePic = graph.Circle(graph.Point((cur_price[COL] + 0.5) * config.CELL_SIZE, (cur_price[ROW] + 0.5) * config.CELL_SIZE), config.CELL_SIZE/6)
                pricePic.setFill('orange')
                self.pricePics.append(pricePic)
                pricePic.draw(self.window)
    
            #Draw obstacles
            for i in range(len(self.obstacles)):
                cur_obs = self.obstacles[i]
                topLeftPt = graph.Point(cur_obs[COL] * config.CELL_SIZE, cur_obs[ROW] * config.CELL_SIZE)
                bottomRightPt = graph.Point((cur_obs[COL] + 1) * config.CELL_SIZE, (cur_obs[ROW] + 1) * config.CELL_SIZE)
    
                obsPic = graph.Rectangle(topLeftPt,bottomRightPt)
                obsPic.setFill('blue')
                obsPic.draw(self.window)

            #Draw position labels
            #Row labels
            for i in range(self.rows):
                label = graph.Text(graph.Point((self.columns + 0.5) * config.CELL_SIZE, (i + 0.5) * config.CELL_SIZE),str(i))
                label.draw(self.window)
            #Column labels
            for i in range(self.columns):
                label = graph.Text(graph.Point((i + 0.5) * config.CELL_SIZE, (self.rows + 0.5) * config.CELL_SIZE),str(i))
                label.draw(self.window)

        else:#if this is not a new maze
            #redraw all prices
            for i in range(len(self.pricePics)):
                self.pricePics[i].undraw()
                
            self.pricePics = []
            for i in range(len(self.prices)):
                cur_price = self.prices[i]
                pricePic = graph.Circle(graph.Point((cur_price[COL] + 0.5) * config.CELL_SIZE, (cur_price[ROW] + 0.5) * config.CELL_SIZE), config.CELL_SIZE/6)
                pricePic.setFill('orange')
                self.pricePics.append(pricePic)
                pricePic.draw(self.window)
            
    def drawTargetPrice(self,targetPrice_):
        if(not(self.targetPrice is None)):
            self.targetPrice.undraw()
        self.targetPrice = graph.Circle(graph.Point((targetPrice_[COL] + 0.5) * config.CELL_SIZE, (targetPrice_[ROW] + 0.5) * config.CELL_SIZE), config.CELL_SIZE/6)
        self.targetPrice.setFill('green')
        self.targetPrice.draw(self.window)

    def printMap(self, mapRequest):
        if (mapRequest == 'original'):
            print('This is original map')
            mapToPrint = self.originalMap
        if (mapRequest == 'path'):
            print('This is navigation path')
            mapToPrint = self.pathMap
        if (mapRequest == 'maze'):
            print('This is map after price collection')
            mapToPrint = self.mazeMap
        index = ' '
        for j in range(self.columns):
            index = index + ('%3s' % j)
        print(index)
        for i in range(self.rows):
            rowString = str(i)
            for j in range(self.columns):
                mark = ''
                if (mapToPrint[i][j] == Price):
                    mark = '$'#price
                elif (mapToPrint[i][j] == Empty):
                    mark = '-'#empty
                elif (mapToPrint[i][j] == Obstacle):
                    mark = '@'#obstacle
                elif (mapToPrint[i][j] == config.Up):
                    mark = '^'
                elif (mapToPrint[i][j] == config.Down):
                    mark = 'v'
                elif (mapToPrint[i][j] == config.Left):
                    mark = '<'
                elif (mapToPrint[i][j] == config.Right):
                    mark = '>'
                rowString =  rowString + ('%3s' % mark)
            print(rowString)

    #given agent position, calulate agent reward, if agent collects price, remove it from mazeMap
    #No need to deal with pathMap, since action will overwrite 
    def calc_reward(self,agentPos):
        if (self.mazeMap[agentPos[ROW]][agentPos[COL]] == Price):
	    #These 2 lines removes collected price
            if (agentPos in self.prices):
                self.prices.remove(agentPos)
                self.mazeMap[agentPos[ROW]][agentPos[COL]] = Empty
            return config.R_PRICE
        if (self.mazeMap[agentPos[ROW]][agentPos[COL]] == Obstacle):
	        return config.R_OBSTACLE
        if (self.mazeMap[agentPos[ROW]][agentPos[COL]] == Empty):
	        return config.R_EMPTY
    
    #Given agent position and action, record it in the pathMap
    def recordAction(self,agentPos,action):
        #self.pathMap = py_copy.deepcopy(self.mazeMap)
        self.pathMap[agentPos[ROW]][agentPos[COL]] = action


#Find nearby objects
def findNearbyObj(objType, agentPos, agentVRange, maze):
    objList = []
    if (objType == 'price'):
        for i in range(len(maze.prices)):
            curPrice = maze.prices[i]
            rowDist = abs(agentPos[ROW] - curPrice[ROW])
            colDist = abs(agentPos[COL] - curPrice[COL])
            if (rowDist <= agentVRange and colDist <=agentVRange):
                obj = py_copy.deepcopy(curPrice)
                objList.append(obj)

    if (objType == 'obstacle'):
        for i in range(len(maze.obstacles)):
            curObs = maze.obstacles[i]
            rowDist = abs(agentPos[ROW] - curObs[ROW])
            colDist = abs(agentPos[COL] - curObs[COL])
            if (rowDist <= agentVRange and colDist <=agentVRange):
                obj = py_copy.deepcopy(curObs)
                objList.append(obj)            

    return objList

#Find nearest price
def findNearestPrice(agentPos, maze):
    minDist = maze.rows + maze.columns
    for i in range(len(maze.prices)):
        curPrice = maze.prices[i]
        rowDist = abs(agentPos[ROW] - curPrice[ROW])
        colDist = abs(agentPos[COL] - curPrice[COL])
        dist = rowDist + colDist
        if (dist < minDist):
            minDist = dist
            nearestPrice = curPrice
        elif (dist == minDist):#Break tie randomly
            if (random.random() >= 0.5):
                minDist = dist
                nearestPrice = curPrice
    return nearestPrice
            
