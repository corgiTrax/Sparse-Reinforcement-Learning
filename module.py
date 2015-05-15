'''moduleClass'''
'''note that in order to ensure module independence, we have a 'transparent' world: different instance can exist on the same grid'''

from config import *

class moduleClass:
    def __init__(self, classID, world, collectable = True,  weight = 1, unit_reward = 1, gamma = 0.9, num_inst = 5, random_gen = True):
        self.classID = classID
        self.world = world
        self.collectable = collectable
        self.insts = []
        if (not random_gen):
            self.weight = weight
            self.unit_reward = unit_reward 
            self.gamma = gamma
            self.num_inst = num_inst
            self.collectable = collectable
        else: # randomly generate a module
            self.weight = random.randint(1,20) # 1<= N <=100, may be too large
            self.unit_reward = random.choice([1,-1])
            self.num_inst = random.randint(1, 10)

            if self.unit_reward == 1: # rewarding objects must be collected
                self.collectable = True
                self.gamma = round(random.uniform(0.5, 0.8), 2) 
            else:
                self.collectable = random.choice([True,False])
                self.gamma = round(random.uniform(0.1,0.4), 2)

        # construct a list of module instances that belong to the same module class

        for i in range(self.num_inst):
            # place instances randomly in the maze
            new_inst = [random.randint(0, self.world.rows - 1), random.randint(0, self.world.columns - 1)]
            self.insts.append(new_inst)

    def calc_reward_rm_inst(self, agentPos):
        cur_reward = 0
        if agentPos in self.insts:
            cur_reward = self.unit_reward * self.weight
            self.insts.remove(agentPos) # this is safe -- python is crazy, agentPos will stay unchanged
        return cur_reward 

    def draw(self, isNew):
        if isNew: # if this is the first time calling draw
            self.color = cg.COLORLIST[self.classID]
            self.window = self.world.window
            self.inst_pics = []
            for inst in self.insts:
                if self.unit_reward == 1: # this is some good stuff
                    pic = cg.Circle(cg.Point((inst[COL] + 0.5) * CELL_SIZE, (inst[ROW] + 0.5) * CELL_SIZE), CELL_SIZE/6)
                else: # this is something agent want to avoid
                    topLeftPt = cg.Point(inst[COL] * CELL_SIZE, inst[ROW] * CELL_SIZE)
                    bottomRightPt = cg.Point((inst[COL] + 1) * CELL_SIZE, (inst[ROW] + 1) * CELL_SIZE)
                    pic = cg.Rectangle(topLeftPt,bottomRightPt)
                pic.setFill(self.color)
                pic.draw(self.window)
                self.inst_pics.append(pic)
        else:
            if self.collectable:
                for pic in self.inst_pics:
                    pic.undraw()
                self.inst_pics = []
                for inst in self.insts:
                    if self.unit_reward == 1: # this is some good stuff
                        pic = cg.Circle(cg.Point((inst[COL] + 0.5) * CELL_SIZE, (inst[ROW] + 0.5) * CELL_SIZE), CELL_SIZE/6)
                    else: # this is something agent want to avoid
                        topLeftPt = cg.Point(inst[COL] * CELL_SIZE, inst[ROW] * CELL_SIZE)
                        bottomRightPt = cg.Point((inst[COL] + 1) * CELL_SIZE, (inst[ROW] + 1) * CELL_SIZE)
                        pic = cg.Rectangle(topLeftPt,bottomRightPt)
                    pic.setFill(self.color)
                    pic.draw(self.window)
                    self.inst_pics.append(pic)
            #else: if instances are not collectable, then do not need to redraw anything

            

if __name__ == '__main__':
    main()


