#! /usr/bin/python
'''experiment file'''

from config import *
import world
import agent
import module
import reinforcement 
import inverseRL

class Experiment():
    def __init__(self, data_file):
        self.data_file = data_file
        self.mouse = MOUSE 
        self.draw = DRAW
        # init maze
        self.testMaze = world.Maze(MAZE_ROW, MAZE_COL)

        # init agent
        self.myAgent = agent.Agent([int(self.testMaze.rows/2),int(self.testMaze.columns/2)], self.testMaze)
        self.stepCount = 0
        self.max_step = MAX_STEP

        # init module classes and instances
        self.moduleClass = []
        for i in range(NUM_MODULE_CLASS):
            new_module = module.moduleClass(classID = i, world = self.testMaze,  random_gen = RAND_GENS[i],\
            collectable = COLLECTABLES[i], unit_reward = UNIT_REWARDS[i], weight = WEIGHTS[i],\
            gamma = GAMMAS[i], num_inst = NUM_INSTS[i])
#            new_module = module.moduleClass(classID = i , world = self.testMaze, random_gen = True)
            self.moduleClass.append(new_module)            

    def run(self):                
        # draw environment
        if self.draw: 
            # draw maze
            self.testMaze.draw()
            # draw agent
            self.myAgent.draw(True)
            # draw module instances
            for module in self.moduleClass: module.draw(True)

        while (self.stepCount <= self.max_step):
            # for each module class, for each instance, calculate Q values
            module_Qvalues = []
            for module in self.moduleClass:
                # use '+=' instead of 'append' to concatenate lists
                module_Qvalues += reinforcement.calc_Qvalues(module, self.myAgent.pos, self.testMaze)
            # SumQ
            globalQvalue = reinforcement.sumQ(module_Qvalues)

            # chooses action using softmax, according to global Q values
            action = reinforcement.softmax_act(globalQvalue)

            '''IRL data recording''' #TODO: write this as a single line function
            if RECORDING:
                new_insts = []
                for module in self.moduleClass:
                    for inst in module.insts:
                        ds = reinforcement.calc_dists(self.myAgent.pos, inst, self.testMaze) 
                        new_inst = inverseRL.observed_inst(self.stepCount, module.classID, module.unit_reward, action, ds)
                        new_insts.append(new_inst)

#                self.data_file.write(str(self.trial) + ',' + str(self.stepCount))
                for inst in new_insts:
                    inst.record(self.data_file)
                    self.data_file.write(' ')
#                    print(inst)
                self.data_file.write('\n')
                del new_insts
            '''end IRL part'''

            # move one step only when mouse clicks
            if self.mouse: self.testMaze.window.getMouse()
                    
            # agent takes action
            self.myAgent.move(action)
    
            # compute reward for agent and remove collecable instances
            for module in self.moduleClass:
                self.myAgent.cum_reward += module.calc_reward_rm_inst(self.myAgent.pos)

            # visualization
            if self.draw:
                # self.testMaze.window.flush()
                self.myAgent.draw(False)
                for module in self.moduleClass:
                    module.draw(False)
          
            self.stepCount +=1
            #print("StepCount: ", stepCount)
        
        # upon finished, close window
        if self.draw: self.testMaze.window.close()




#Experiment
data_file = open(sys.argv[1],'w')
#data_file.write(str(R_PRIZE) + ',' + str(R_OBS) + ',' + str(GAMMA_PRIZE) + ',' + str(GAMMA_OBS) + ',' + str(ETA) + '\n')

for trial in range(MAX_TRIAL):
    print("trial #", trial)
    experiment = Experiment(data_file)
    experiment.run()

data_file.close()

#Hold graph window
#raw_input("Press enter to exit")

