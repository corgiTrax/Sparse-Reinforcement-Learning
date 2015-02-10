'''experiment file'''

from config import *
import world
import agent
import reinforcement 

total_success = 0
for trial in range(MAX_TRIAL):
    print("trial #", trial)
    #generate a Maze
    testMaze = world.Maze(TESTR, TESTC)
    if DRAW: testMaze.drawSelf(True)
             
    #Predator starts at (0,0)
    predators = []
    for i in range(NUM_PREDATOR):
        predator = agent.Predator([0,0], testMaze)
        if DRAW: predator.drawSelf(True)
        predators.append(predator)
                
    #Agent starts at middle
    myAgent = agent.Agent([int(TESTR/2),int(TESTC/2)], testMaze)
    if DRAW: myAgent.drawSelf(True)
    Captured = 0 #being captured by predator or not
    success = False #collect all prices
    stepCount = 0
                
    while (stepCount <= MAX_STEP and (Captured == 0) and (not success)):
        #Module class #1: prize, calculate Q values for each of the prize object in the maze
        prizeQvalues = reinforcement.calc_Qvalues('prize', myAgent.pos, testMaze.prizes, testMaze)
             
        #Module class #2: obstacle, calculate Q values for each of the obstacle object in the maze
        obsQvalues = reinforcement.calc_Qvalues('obstacle', myAgent.pos, testMaze.obstacles, testMaze)
               
        #Module class #3: predator, calculate Q values for each of the predator object in the maze
        #predators move first
        predatorPos = []
        for i in range(len(predators)):
            predators[i].move(predator.chase(myAgent.pos, P_CHASE))
            predatorPos.append(predators[i].pos)
        predatorQvalues = reinforcement.calc_Qvalues('predator', myAgent.pos, predatorPos, testMaze)
              
        #SumQ
        globalQvalue = reinforcement.sumQ(prizeQvalues + obsQvalues + predatorQvalues)
        #action = numpy.argmax(globalQvalue)
        action = reinforcement.softmax_act(globalQvalue)
        #print("prizes: ", testMaze.prizes)
        #print("prize Q values: ", prizeQvalues)
        #print("Global Q values: ", globalQvalue)
    
        #move one step only when mouse clicks
        if MOUSE: testMaze.window.getMouse()
                    
        #agent takes action
        myAgent.move(action)
    
        #Compute consequences
        for i in range(len(predators)):
            Captured += (myAgent.pos == predators[i].pos)
        myAgent.cum_reward += testMaze.calc_reward(myAgent.pos)
        if (Captured > 0): 
            print("Captured!")
            myAgent.cum_reward -= R_PRED
    
        #Visualization
        if DRAW:
            testMaze.drawSelf(False)   
            myAgent.drawSelf(False)
            for i in range(len(predators)):
                predators[i].drawSelf(False)
    
                     
        if len(testMaze.prizes) == 0:
            #print("Success!")
            success = True
            total_success += 1        
        stepCount +=1
    
        #print("StepCount: ", stepCount)
       
print("total success: ", total_success)     
#Hold graph window
#raw_input("Press enter to exit")

 

