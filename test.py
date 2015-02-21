'''experiment file'''

from config import *
import world
import agent
import reinforcement 


class Experiment():
    def __init__(self):
        self.mouse = MOUSE 
        self.draw = DRAW
        #generate a Maze
        self.testMaze = world.Maze(TESTR, TESTC)

        #Predator starts at (0,0)
        self.predators = []
        for i in range(NUM_PREDATOR):
            predator = agent.Predator([0,0], self.testMaze)
            self.predators.append(predator)
        self.predator_chase = P_CHASE

        #Agent starts at middle
        self.myAgent = agent.Agent([int(TESTR/2),int(TESTC/2)], self.testMaze)
        self.captured = 0 #being captured by predator or not
        self.success = False
        self.stepCount = 0
        self.max_step = MAX_STEP

    def store_data(self, filename):
        pass

    def run(self):                
        if self.draw: 
            self.testMaze.drawSelf(True)
            self.myAgent.drawSelf(True)
            for predator in self.predators: predator.drawSelf(True)

        while (self.stepCount <= self.max_step and (self.captured == 0) and (not self.success)):
            #Module class #1: prize, calculate Q values for each of the prize object in the maze
            prizeQvalues = reinforcement.calc_Qvalues('prize', self.myAgent.pos, self.testMaze.prizes, self.testMaze)
             
            #Module class #2: obstacle, calculate Q values for each of the obstacle object in the maze
            obsQvalues = reinforcement.calc_Qvalues('obstacle', self.myAgent.pos, self.testMaze.obstacles, self.testMaze)
               
            #Module class #3: predator, calculate Q values for each of the predator object in the maze
            #predators move first
            predatorPos = []
            for predator in self.predators:
                predator.move(predator.chase(self.myAgent.pos, self.predator_chase))
                predatorPos.append(predator.pos)
            predatorQvalues = reinforcement.calc_Qvalues('predator', self.myAgent.pos, predatorPos, self.testMaze)
              
            #SumQ
            globalQvalue = reinforcement.sumQ(prizeQvalues + obsQvalues + predatorQvalues)
            #action = numpy.argmax(globalQvalue)
            action = reinforcement.softmax_act(globalQvalue)
            #print("prizes: ", testMaze.prizes)
            #print("prize Q values: ", prizeQvalues)
            #print("Global Q values: ", globalQvalue)
    
            #move one step only when mouse clicks
            if self.mouse: self.testMaze.window.getMouse()
                    
            #agent takes action
            self.myAgent.move(action)
    
            #Compute consequences
            for predator in self.predators:
                self.captured += (self.myAgent.pos == predator.pos)
            self.myAgent.cum_reward += self.testMaze.calc_reward(self.myAgent.pos)
            
            if (self.captured > 0): 
                print("Captured by predator!")
                self.myAgent.cum_reward -= R_PRED #config
    
            #Visualization
            if self.draw:
                self.testMaze.drawSelf(False)   
                self.myAgent.drawSelf(False)
                for predator in self.predators:
                    predator.drawSelf(False)
                     
            if len(self.testMaze.prizes) == 0:
                print("Success!")
                self.success = True
                
            self.stepCount +=1
            #print("StepCount: ", stepCount)
       
        self.testMaze.window.close()

#Experiment
total_success = 0
 
for trial in range(MAX_TRIAL):
    print("trial #", trial)
    experiment = Experiment()
    experiment.run()
    total_success += experiment.success

print("total success: ", total_success)     
#Hold graph window
#raw_input("Press enter to exit")

