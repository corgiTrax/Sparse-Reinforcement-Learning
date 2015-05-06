'''moduleClass'''
'''note that in order to ensure module independence, we have a 'transparent' world: different instance can exist on the same grid'''

from config import *

class moduleClass:
    def __init__(self, classID, world,  weight = 1, unit_reward = 1, gamma = 0.9, random_gen = True, max_instance = 5):
        self.classID = classID
        self.world.world
        self.instances = []
        self.max_instance = max_instance
        if (not random_gen):
            self.weight = weight
            self.unit_reward = reward 
            self.gamma = gamma
        else:
            self.weight = random.randint(1,100) # 1<= N <=100, may be too large
            self.unit_reward = random.choice([1,-1])
            self.gamma = random.random # 0<= gamma < 1

        # return a list of module instances that belong to the same module class
        num_instance = random.randint(1,max_instance)
        for i in range(num_instance):
            # place instances randomly in the maze
            new_instance = [random.randint(0, self.world.rows), random.randint(0, self.world.columns)]
            self.instances.append(new_instance)

    def drawAllInstances(self):
        # self.color
        for instance in self.instances:
            
    def drawSelf(self):
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







