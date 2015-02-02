'''reinforcement learning agent'''

from config import *

class Agent:
    '''agent class that moves in the 2D world'''
    def __init__(self, initPos, world):
        '''2D position of the agent'''
        self.pos = initPos
        '''the world this agent lives in'''
        self.world = world

    def move(self, action):
        if (action == UP):self.pos[0] -=1
        if (action == DOWN):self.pos[0] +=1
        if (action == LEFT):self.pos[1] -=1
        if (action == RIGHT):self.pos[1] +=1
        if (self.pos[0] >= self.world.rows):self.pos[0] = self.world.rows - 1;
        if (self.pos[0] < 0):self.pos[0] = 0;
        if (self.pos[1] >= self.world.columns):self.pos[1] = self.world.columns - 1;        
        if (self.pos[1] < 0):self.pos[1] = 0;

    def drawSelf(self, isnew, color = 'red'):
        '''if object is new draw a new object'''
        if (isnew == True):
            self.picCenter = graph.Point((self.pos[COL] + 0.5) * CELL_SIZE, (self.pos[ROW] + 0.5) * CELL_SIZE)
            self.agentPic = graph.Circle(self.picCenter, CELL_SIZE/4)
            self.agentPic.setFill(color)
            self.agentPic.draw(self.world.window)
        '''if it is not new just move it'''
        else:
            dx = -self.agentPic.getCenter().getX() + (self.pos[COL] + 0.5) * CELL_SIZE
            dy = -self.agentPic.getCenter().getY() + (self.pos[ROW] + 0.5) * CELL_SIZE
            self.agentPic.move(dx,dy)

    
#Predator class
class Predator:
    def __init__(self,initPos):
        self.pos = py_copy.deepcopy(initPos)
  
    def move(self, action, maze):
        if (action == Stay):pass
        if (action == Up):self.pos[0] -=1
        if (action == Down):self.pos[0] +=1
        if (action == Left):self.pos[1] -=1
        if (action == Right):self.pos[1] +=1
        if (self.pos[0] >= maze.rows):self.pos[0] = maze.rows - 1;
        if (self.pos[0] < 0):self.pos[0] = 0;
        if (self.pos[1] >= maze.columns):self.pos[1] = maze.columns - 1;        
        if (self.pos[1] < 0):self.pos[1] = 0;

    def drawSelf(self, window, isnew):
        if (isnew == True):
            self.picCenter = graph.Point((self.pos[COL] + 0.5) * CELL_SIZE, (self.pos[ROW] + 0.5) * CELL_SIZE)
            self.agentPic = graph.Circle(self.picCenter, CELL_SIZE/4)
            self.agentPic.setFill('black')
            self.agentPic.draw(window)
           
        else:
            dx = -self.agentPic.getCenter().getX() + (self.pos[COL] + 0.5) * CELL_SIZE
            dy = -self.agentPic.getCenter().getY() + (self.pos[ROW] + 0.5) * CELL_SIZE
            self.agentPic.move(dx,dy)
    
    #Predator always tries to select action to approach agent
    def chase(self, agentPos, pChase):
        diffRow = -self.pos[ROW] + agentPos[ROW]
        diffCol = -self.pos[COL] + agentPos[COL]

        if (random.random() > pChase):
            action = random.choice(range(NUM_ACT))
            return action
        elif (diffRow == 0 and diffCol == 0):
            action = random.choice(range(NUM_ACT))
        elif (diffCol == 0):
            if (diffRow > 0):#agent is below the predator   
                action = Down
            elif (diffRow < 0):#agent is above of the predator
                action = Up
        elif (diffRow == 0):
            if (diffCol > 0):#agent is on right of the predator
                action = Right
            elif (diffCol < 0):#agent is on left of the predator
                action = Left
        else:# (diffRow != 0 and diffCol != 0):
            if (random.random() >= 0.5):#listen to row
                if (diffRow > 0):#agent is below of the predator   
                    action = Down
                elif (diffRow < 0):#agent is above the predator
                    action = Up
            else:#listen to column
                if (diffCol > 0):#agent is on right of the predator
                    action = Right
                elif (diffCol < 0):#agent is on left of the predator
                    action = Left
     
        return action



