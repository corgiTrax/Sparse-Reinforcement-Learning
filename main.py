#! /usr/bin/python
'''experiment file'''

from config import *
import maze
import agent
import module
import reinforcement 
import modularIRL

class Experiment():
    def __init__(self, trial, data_file):
        self.data_file = data_file
        self.trial = trial
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
            new_module = module.moduleClass(world = self.testMaze, random_gen = RAND_MODULE)
            self.moduleClasses.append(new_module)            

    def run(self):                
        # draw environment
        if self.draw: 
            # draw maze
            self.testMaze.drawSelf(True)
            # draw agent
            self.myAgent.drawSelf(True)
            # draw module instances
            for module in self.moduleClass: module.drawInstances(True)

        while (self.stepCount <= self.max_step and (self.captured == 0) and (not self.success)):
            # for each module class, for each instance, calculate Q values
            prizeQvalues = reinforcement.calc_Qvalues('prize', self.myAgent.pos, self.testMaze.prizes, self.testMaze)
              
            # SumQ
            globalQvalue = reinforcement.sumQ(prizeQvalues + obsQvalues + predatorQvalues)

            # chooses action using softmax, according to global Q values
            action = reinforcement.softmax_act(globalQvalue)

            '''IRL data recording''' #TODO: write this as a single line function
            if RECORDING:
                new_instances = []
                #prize instances
                for prizePos in self.testMaze.prizes:
                    xs = reinforcement.calc_dists(self.myAgent.pos, prizePos, self.testMaze)
                    new_instance = modularIRL.observed_instance(self.trial, self.stepCount, PRIZE, action, xs)
                    new_instances.append(new_instance)
            
                #obstacle instances
                for obsPos in self.testMaze.obstacles:
                    xs = reinforcement.calc_dists(self.myAgent.pos, obsPos, self.testMaze)
                    new_instance = modularIRL.observed_instance(self.trial, self.stepCount, OBS, action, xs)
                    new_instances.append(new_instance)

                self.data_file.write(str(self.trial) + ',' + str(self.stepCount))
                for instance in new_instances:
                    self.data_file.write(',')
                    instance.record(self.data_file)
                    #print(instance)
                self.data_file.write('\n')
                del new_instances
            '''end IRL part'''

            # move one step only when mouse clicks
            if self.mouse: self.testMaze.window.getMouse()
                    
            # agent takes action
            self.myAgent.move(action)
    
            # compute consequences
            self.myAgent.cum_reward += self.testMaze.calc_reward(self.myAgent.pos)
  
            # visualization
            if self.draw:
                self.testMaze.drawSelf(False)   
                self.myAgent.drawSelf(False)
                for predator in self.predators:
                    predator.drawSelf(False)
          
            self.stepCount +=1
            #print("StepCount: ", stepCount)
        
        # upon finished, close window
        if self.draw: self.testMaze.window.close()

if __name__ == "main":
    #Experiment
    total_success = 0
    data_file = open(RECORD_FILENAME,'w')
    data_file.write(str(R_PRIZE) + ',' + str(R_OBS) + ',' + str(GAMMA_PRIZE) + ',' + str(GAMMA_OBS) + ',' + str(ETA) + '\n')

    for trial in range(MAX_TRIAL):
        print("trial #", trial)
        experiment = Experiment(trial, data_file)
        experiment.run()
        total_success += experiment.success

    print("total success: ", total_success)
    data_file.close()

    #Hold graph window
    #raw_input("Press enter to exit")

